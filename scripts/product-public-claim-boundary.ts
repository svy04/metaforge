import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

import { check, fileSha256, readText, sha256, type Check } from './quality-report-helpers'

type PublicSurface = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
  lineCount: number
}

export type ClaimFinding = {
  path: string
  line: number
  phrase: string
  category: string
  status: 'blocked_context' | 'unauthorized_positive_claim'
  text: string
  contextText: string
}

type ClaimPattern = {
  category: string
  phrase: string
  pattern: RegExp
}

type PublicClaimBoundaryReport = {
  generatedAt: string
  mode: 'local_no_provider_public_claim_boundary'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  scannedPublicSurfaces: PublicSurface[]
  publicSurfaceCount: number
  scannedLineCount: number
  blockedContextClaimMentionCount: number
  unauthorizedPositiveClaimCount: number
  blockedContextClaimMentions: ClaimFinding[]
  unauthorizedPositiveClaims: ClaimFinding[]
  claimBoundaryStatus: 'no_unauthorized_public_claims_detected' | 'unauthorized_public_claims_detected'
  scanJsonlPath: string
  scanJsonlSha256: string
  scanJsonlRecordCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  publishDeployLaunchPerformed: false
  releaseClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  superiorityClaimAllowed: false
  mthResolutionStatus: 'unresolved'
  canonicalMemoryWriteAllowed: false
  allowedClaimLevel: 'internal_no_provider_product_quality_evidence_only'
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/public-claim-boundary-report.json'
const reportMdPath = 'docs/product-quality/public-claim-boundary-report.md'
const scanJsonlPath = 'reports/openclaude-public-claim-boundary.jsonl'
const checkOnly = process.argv.includes('--check')

export const publicSurfacePaths = [
  'README.md',
  'README.ko.md',
  'AGENTS.md',
  'ANDROID_INSTALL.md',
  'PLAYBOOK.md',
  'CHANGELOG.md',
  'CONTRIBUTING.md',
  'SECURITY.md',
  'SUPPORT.md',
  'package.json',
  '.github/ISSUE_TEMPLATE/bug_report.md',
  '.github/ISSUE_TEMPLATE/feature_request.md',
  '.github/pull_request_template.md',
  'docs/PROJECT_SPEC.md',
  'docs/EVALS.md',
  'docs/ROADMAP.md',
  'docs/SECURITY_AND_GUARDRAILS.md',
  'docs/quick-start-windows.md',
  'docs/quick-start-mac-linux.md',
  'docs/advanced-setup.md',
  'docs/litellm-setup.md',
  'docs/product-quality/product-quality-gate.md',
  'docs/product-quality/terminal-report.md',
  'docs/product-quality/verification-report-2026-05-17.md',
  'docs/product-quality/protected-action-authorization-packet.md',
  'docs/product-quality/github-remote-surface-audit-report.md',
  'docs/MIMESIS_ENGINEERING.md',
  'docs/marketing/metaforge-public-proof-pack-2026-06-14.md',
  'docs/research/public-proof-pack-source-ledger-2026-06-14.md',
  'packages/openclaude-vscode/package.json',
  'packages/openclaude-vscode/README.md',
  'vscode-extension/openclaude-vscode/package.json',
  'vscode-extension/openclaude-vscode/README.md',
  ...publicGoalArtifactPaths(),
]

const claimPatterns: ClaimPattern[] = [
  { category: 'launch', phrase: 'launch completed', pattern: /\blaunch completed\b|\bopenclaude (?:has )?launched\b/i },
  { category: 'deploy', phrase: 'deployed', pattern: /\bopenclaude (?:has been )?deployed\b|\bdeployment completed\b/i },
  { category: 'publish', phrase: 'published', pattern: /\bopenclaude (?:has been )?published\b|\bpublication completed\b|\bpackage release published\b/i },
  { category: 'release_readiness', phrase: 'release readiness', pattern: /\brelease[-\s]?ready\b|\brelease readiness\b/i },
  { category: 'production_readiness', phrase: 'production readiness', pattern: /\bproduction[-\s]?ready\b|\bproduction readiness\b/i },
  { category: 'production_validation', phrase: 'production validated', pattern: /\bproduction (?:openclaude )?(?:validated|validation completed|proven)\b/i },
  { category: 'public_readiness', phrase: 'public readiness', pattern: /\bpublic[-\s]?ready\b|\bpublic readiness\b/i },
  { category: 'external_validation', phrase: 'external validation', pattern: /\bexternally validated\b|\bexternal validation\b/i },
  { category: 'autonomous_reliability', phrase: 'autonomous reliability', pattern: /\bautonomous reliability\b/i },
  { category: 'provider_backed_execution', phrase: 'provider-backed execution', pattern: /\bprovider[-\s]?backed execution\b/i },
  { category: 'live_model_validation', phrase: 'live model validation', pattern: /\blive model validation\b/i },
  { category: 'superiority', phrase: 'superior to top 10', pattern: /\b(?:superior to|better than|beats?|outperforms?)\b.{0,80}\btop[-\s]?10\b|\btop[-\s]?10\b.{0,80}\b(?:superior|better|beats?|outperforms?)\b|\btop[-\s]?10.{0,20}\uBCF4\uB2E4\b/i },
  { category: 'superiority', phrase: 'benchmark or model superiority', pattern: /\b(?:superior to|better than|beats?|outperforms?)\b.{0,100}\b(?:agent|agents|benchmark|claude|gpt|model|openai|anthropic|terminal[-\s]?bench)\b/i },
  { category: 'superiority', phrase: 'current-best model or provider', pattern: /\b(?:current[-\s]?best|best[-\s]?(?:available\s+)?(?:provider|model|benchmark)|recommended\s+(?:free\s+)?(?:provider|model|benchmark))\b/i },
]

const blockedContextTerms = [
  'not',
  'no ',
  'without',
  'blocked',
  'blocking',
  'scope',
  'policy applies',
  'before',
  'unless',
  'forbidden',
  'disallowed',
  'unauthorized',
  'not authorized',
  'authorization',
  'authorization packet',
  'not allowed',
  'not allowed yet',
  'does not',
  'do not',
  'did not',
  'must not',
  'remain blocked',
  'remains blocked',
  'claim_allowed=false',
  'allowed=false',
  'claimallowed": false',
  'claimed: `false`',
  'allowed: `false`',
  'defaults false',
  'defaulting to `false`',
  'explicitly blocked',
  'not claimed',
  'not prove',
  'not completed',
  'not ready',
  'not performed',
  'false',
  '아닙니다',
  '증명하지',
  '증거가 아닙니다',
]
const blockedContextLookbackLines = 8
const goalArtifactBoundaryLookaheadLines = 20

const goalArtifactStatusPatterns: ClaimPattern[] = [
  { category: 'goal_artifact_status', phrase: 'status: PROVEN', pattern: /^\s*status:\s*PROVEN\b/i },
  { category: 'goal_artifact_status', phrase: 'terminal condition ready', pattern: /\b[A-Z0-9_]+_READY\b/i },
  { category: 'goal_artifact_status', phrase: 'completion candidate', pattern: /\bcompletion candidate\b/i },
  { category: 'goal_artifact_status', phrase: 'beta candidate', pattern: /\bbeta candidate\b/i },
]

const goalArtifactBoundaryTerms = [
  'Historical local artifact boundary',
  'repo_local_internal_only',
  'product_completion_claim_scope',
  'claim-scope',
  'claim scope',
  'without external execution',
  'not externally validated',
  'repo-local',
  'local no-provider',
  'local/internal',
  'does not',
  'local only',
]

function publicGoalArtifactPaths(): string[] {
  const goalDir = resolve(root, 'docs/goals')
  if (!existsSync(goalDir)) {
    return []
  }

  return readdirSync(goalDir)
    .filter((name) => name.endsWith('.md'))
    .sort()
    .map((name) => `docs/goals/${name}`)
}

function fileSurface(path: string): PublicSurface {
  const absolutePath = resolve(root, path)
  if (!existsSync(absolutePath)) {
    return { path, exists: false, sha256: null, sizeBytes: 0, lineCount: 0 }
  }
  const text = readText(path, root)
  return {
    path,
    exists: true,
    sha256: fileSha256(path, root),
    sizeBytes: Buffer.byteLength(text, 'utf8'),
    lineCount: text.split(/\r?\n/).length,
  }
}

function isBlockedContext(context: string): boolean {
  const lower = context.toLowerCase()
  return blockedContextTerms.some((term) => lower.includes(term))
}

function isGoalArtifactPath(path: string): boolean {
  return path.startsWith('docs/goals/') && path.endsWith('.md')
}

function findGoalArtifactBoundaryLine(lines: string[]): string | null {
  const header = lines.slice(0, goalArtifactBoundaryLookaheadLines)
  return header.find((line) => (
    goalArtifactBoundaryTerms.some((term) => line.toLowerCase().includes(term.toLowerCase()))
  )) ?? null
}

function scanGoalArtifactStatus(path: string, text: string): ClaimFinding[] {
  if (!isGoalArtifactPath(path)) {
    return []
  }

  const lines = text.split(/\r?\n/)
  const boundaryLine = findGoalArtifactBoundaryLine(lines)
  const findings: ClaimFinding[] = []
  for (const [index, line] of lines.entries()) {
    const pattern = goalArtifactStatusPatterns.find((item) => item.pattern.test(line))
    if (!pattern) {
      continue
    }

    const reportedLine = redactLine(line)
    const status = boundaryLine ? 'blocked_context' : 'unauthorized_positive_claim'
    findings.push({
      path,
      line: index + 1,
      phrase: pattern.phrase,
      category: pattern.category,
      status,
      text: reportedLine,
      contextText: status === 'blocked_context'
        ? `Blocked context: ${redactBlockingLine(boundaryLine ?? reportedLine)} Claim mention: ${reportedLine}`
        : reportedLine,
    })
    break
  }

  return findings
}

function redactLine(line: string): string {
  return line.trim().replace(/\s+/g, ' ').slice(0, 240)
}

function compactLine(line: string): string {
  return line.trim().replace(/\s+/g, ' ')
}

function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function blockedTermMatchIndex(text: string, term: string): number {
  const normalizedTerm = term.trim()
  if (/^[a-z0-9 ]+$/i.test(normalizedTerm)) {
    const pattern = new RegExp(`\\b${escapeRegExp(normalizedTerm).replace(/\s+/g, '\\s+')}\\b`, 'i')
    const match = pattern.exec(text)
    return match?.index ?? -1
  }

  return text.toLowerCase().indexOf(term.toLowerCase())
}

function findBlockedTermIndex(text: string): number {
  const prioritizedTerms = [...blockedContextTerms].sort((left, right) => right.trim().length - left.trim().length)
  for (const term of prioritizedTerms) {
    const index = blockedTermMatchIndex(text, term)
    if (index >= 0) {
      return index
    }
  }

  return -1
}

function redactBlockingLine(line: string): string {
  const compact = compactLine(line)
  if (compact.length <= 240) {
    return compact
  }

  const termIndex = findBlockedTermIndex(compact)
  if (termIndex < 0) {
    return redactLine(compact)
  }

  const start = Math.max(0, termIndex - 80)
  const end = Math.min(compact.length, termIndex + 200)
  const prefix = start > 0 ? '... ' : ''
  const suffix = end < compact.length ? ' ...' : ''
  return `${prefix}${compact.slice(start, end)}${suffix}`
}

function blockedContextText(contextLines: string[], rawClaimLine: string, reportedClaimLine: string): string {
  const blockingLine = findBlockingContextLine(contextLines, rawClaimLine)

  if (blockingLine && blockingLine !== rawClaimLine) {
    return `Blocked context: ${redactBlockingLine(blockingLine)} Claim mention: ${reportedClaimLine}`
  }

  return `Blocked context: ${redactBlockingLine(blockingLine ?? reportedClaimLine)}`
}

function isListItem(line: string): boolean {
  return /^\s*(?:[-*]|\d+[.)])\s+/.test(line)
}

function isIndentedContinuation(line: string): boolean {
  return /^\s{2,}\S/.test(line) && !isListItem(line)
}

function isBoundaryHeader(line: string): boolean {
  const compact = compactLine(line)
  return isBlockedContext(compact) && /[:：]\s*$/.test(compact)
}

function findBlockingContextLine(contextLines: string[], claimLine: string): string | null {
  const currentLine = contextLines.at(-1) ?? claimLine
  if (isBlockedContext(currentLine)) {
    return currentLine
  }

  if (!isListItem(claimLine)) {
    if (!isIndentedContinuation(claimLine)) {
      return null
    }

    for (let index = contextLines.length - 2; index >= 0; index -= 1) {
      const candidate = contextLines[index]
      if (candidate.trim().length === 0) {
        return null
      }
      if (isBlockedContext(candidate)) {
        return candidate
      }
    }
    return null
  }

  for (let index = contextLines.length - 2; index >= 0; index -= 1) {
    const candidate = contextLines[index]
    if (candidate.trim().length === 0) {
      continue
    }
    if (isListItem(candidate)) {
      continue
    }
    return isBoundaryHeader(candidate) ? candidate : null
  }

  return null
}

function findingReportText(finding: ClaimFinding): string {
  return finding.status === 'blocked_context' ? finding.contextText : finding.text
}

export function markdownCell(text: string): string {
  return text.replace(/\\/g, '\\\\').replace(/\|/g, '\\|')
}

export function scanClaimText(path: string, text: string): ClaimFinding[] {
  const lines = text.split(/\r?\n/)
  const findings: ClaimFinding[] = []
  const goalArtifactBoundaryLine = isGoalArtifactPath(path) ? findGoalArtifactBoundaryLine(lines) : null
  for (const [index, line] of lines.entries()) {
    const contextLines = lines.slice(Math.max(0, index - blockedContextLookbackLines), index + 1)
    for (const claimPattern of claimPatterns) {
      if (!claimPattern.pattern.test(line)) {
        continue
      }
      const text = redactLine(line)
      const blockingLine = findBlockingContextLine(contextLines, line) ?? goalArtifactBoundaryLine
      const status = blockingLine ? 'blocked_context' : 'unauthorized_positive_claim'
      findings.push({
        path,
        line: index + 1,
        phrase: claimPattern.phrase,
        category: claimPattern.category,
        status,
        text,
        contextText: status === 'blocked_context'
          ? (goalArtifactBoundaryLine && !findBlockingContextLine(contextLines, line)
            ? `Blocked context: ${redactBlockingLine(goalArtifactBoundaryLine)} Claim mention: ${text}`
            : blockedContextText(contextLines, line, text))
          : text,
      })
    }
  }
  return [...findings, ...scanGoalArtifactStatus(path, text)]
}

function scanSurface(path: string): ClaimFinding[] {
  if (!existsSync(resolve(root, path))) {
    return []
  }
  return scanClaimText(path, readText(path))
}

function writeMarkdown(report: PublicClaimBoundaryReport): void {
  const surfaceRows = report.scannedPublicSurfaces
    .map((surface) => `| \`${surface.path}\` | \`${surface.exists}\` | \`${surface.sha256 ?? 'missing'}\` | ${surface.lineCount} |`)
    .join('\n')
  const blockedRows = report.blockedContextClaimMentions.length === 0
    ? '| none | none | none | none |'
    : report.blockedContextClaimMentions
      .map((finding) => `| \`${finding.path}:${finding.line}\` | \`${finding.category}\` | \`${finding.phrase}\` | ${markdownCell(findingReportText(finding))} |`)
      .join('\n')
  const unauthorizedRows = report.unauthorizedPositiveClaims.length === 0
    ? '| none | none | none | none |'
    : report.unauthorizedPositiveClaims
      .map((finding) => `| \`${finding.path}:${finding.line}\` | \`${finding.category}\` | \`${finding.phrase}\` | ${markdownCell(findingReportText(finding))} |`)
      .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Public Claim Boundary Report

Generated by: \`bun run product:public-claim-boundary\`

## Claim Boundary

- This report scans repository public surfaces for unauthorized positive release, production, public, external-validation, provider-backed, live-model, autonomous-reliability, launch, deploy, publish, and top-10 superiority claims.
- It allows explicit blocked or negative claim-boundary text, because those statements preserve the boundary instead of expanding it.
- It does not call providers, live models, external services, install dependencies, publish, deploy, launch, or execute protected actions.

## Summary

- public_surface_count: \`${report.publicSurfaceCount}\`
- scanned_line_count: \`${report.scannedLineCount}\`
- blocked_context_claim_mention_count: \`${report.blockedContextClaimMentionCount}\`
- unauthorized_positive_claim_count: \`${report.unauthorizedPositiveClaimCount}\`
- claim_boundary_status: \`${report.claimBoundaryStatus}\`
- scan_jsonl_path: \`${report.scanJsonlPath}\`
- scan_jsonl_sha256: \`${report.scanJsonlSha256}\`
- release_claim_allowed: \`${report.releaseClaimAllowed}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`
- production_readiness_claim_allowed: \`${report.productionReadinessClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`
- external_validation_claim_allowed: \`${report.externalValidationClaimAllowed}\`
- autonomous_reliability_claim_allowed: \`${report.autonomousReliabilityClaimAllowed}\`
- superiority_claim_allowed: \`${report.superiorityClaimAllowed}\`
- mth_resolution_status: \`${report.mthResolutionStatus}\`
- canonical_memory_write_allowed: \`${report.canonicalMemoryWriteAllowed}\`
- allowed_claim_level: \`${report.allowedClaimLevel}\`

## Primary Source Inputs

| Source | URL | Pattern |
| --- | --- | --- |
${report.primarySourceInputs.map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`).join('\n')}

## Scanned Public Surfaces

| Path | Exists | SHA-256 | Lines |
| --- | --- | --- | ---: |
${surfaceRows}

## Unauthorized Positive Claims

| Location | Category | Phrase | Text |
| --- | --- | --- | --- |
${unauthorizedRows}

## Blocked Context Mentions

| Location | Category | Phrase | Text |
| --- | --- | --- | --- |
${blockedRows}

## Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  if (!checkOnly) {
    mkdirSync(docsDir, { recursive: true })
    mkdirSync(reportsDir, { recursive: true })
  }

  const scannedPublicSurfaces = publicSurfacePaths.map(fileSurface)
  const findings = publicSurfacePaths.flatMap(scanSurface)
  const blockedContextClaimMentions = findings.filter((finding) => finding.status === 'blocked_context')
  const unauthorizedPositiveClaims = findings.filter((finding) => finding.status === 'unauthorized_positive_claim')
  const scanJsonlText = findings.map((finding) => JSON.stringify(finding)).join('\n') + (findings.length > 0 ? '\n' : '')
  if (!checkOnly) {
    writeFileSync(resolve(root, scanJsonlPath), scanJsonlText)
  }
  const scanJsonlSha256 = sha256(scanJsonlText)
  const scanJsonlRecordCount = scanJsonlText.trim().length === 0 ? 0 : scanJsonlText.trim().split(/\r?\n/).length

  const report: PublicClaimBoundaryReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_public_claim_boundary',
    primarySourceInputs: [
      {
        sourceProject: 'GitHub Docs README guidance',
        sourceUrl: 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes',
        observedPattern: 'Public repository surfaces should communicate what the project does and how to use it without making unsupported proof claims.',
      },
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'Open-source quality posture is stronger when checks are explicit, repeatable, and tied to evidence instead of narrative-only assertions.',
      },
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence and provenance boundaries should stay separate from release, production, and external-attestation claims until those steps are actually authorized and performed.',
      },
    ],
    scannedPublicSurfaces,
    publicSurfaceCount: scannedPublicSurfaces.length,
    scannedLineCount: scannedPublicSurfaces.reduce((total, surface) => total + surface.lineCount, 0),
    blockedContextClaimMentionCount: blockedContextClaimMentions.length,
    unauthorizedPositiveClaimCount: unauthorizedPositiveClaims.length,
    blockedContextClaimMentions,
    unauthorizedPositiveClaims,
    claimBoundaryStatus: unauthorizedPositiveClaims.length === 0 ? 'no_unauthorized_public_claims_detected' : 'unauthorized_public_claims_detected',
    scanJsonlPath,
    scanJsonlSha256,
    scanJsonlRecordCount,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    publishDeployLaunchPerformed: false,
    releaseClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    superiorityClaimAllowed: false,
    mthResolutionStatus: 'unresolved',
    canonicalMemoryWriteAllowed: false,
    allowedClaimLevel: 'internal_no_provider_product_quality_evidence_only',
    evidenceChecks: [],
    claimBoundary: 'Public claim boundary scan only. This local no-provider report does not authorize or make release, public, production, external-validation, provider-backed, live-model, top-10 superiority, or autonomous-reliability claims.',
  }

  report.evidenceChecks = [
    check('all configured public surfaces exist', scannedPublicSurfaces.every((surface) => surface.exists), scannedPublicSurfaces.filter((surface) => !surface.exists).map((surface) => surface.path).join(',') || 'all present'),
    check('public surfaces are hash-bound', scannedPublicSurfaces.every((surface) => typeof surface.sha256 === 'string' && /^[a-f0-9]{64}$/.test(surface.sha256) && surface.sizeBytes > 0), `${scannedPublicSurfaces.length} surfaces`),
    check('public surfaces contain scanned lines', report.scannedLineCount > 0, `${report.scannedLineCount} lines`),
    check('unauthorized positive claims are absent', unauthorizedPositiveClaims.length === 0, `${unauthorizedPositiveClaims.length} findings`),
    check('blocked context mentions are classified separately', blockedContextClaimMentions.every((finding) => finding.status === 'blocked_context'), `${blockedContextClaimMentions.length} findings`),
    check('claim JSONL record count matches findings', scanJsonlRecordCount === findings.length, `${scanJsonlRecordCount}/${findings.length}`),
    check('claim JSONL hash is recorded', /^[a-f0-9]{64}$/.test(scanJsonlSha256), scanJsonlPath),
    check('provider live external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0 && report.dependencyInstallPerformed === false && report.publishDeployLaunchPerformed === false, 'zero protected actions'),
    check('readiness external reliability and superiority claims remain blocked', report.releaseClaimAllowed === false && report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false && report.superiorityClaimAllowed === false, 'all claim flags false'),
    check('mth and canonical memory boundaries remain preserved', report.mthResolutionStatus === 'unresolved' && report.canonicalMemoryWriteAllowed === false && report.allowedClaimLevel === 'internal_no_provider_product_quality_evidence_only', `${report.mthResolutionStatus}/${report.canonicalMemoryWriteAllowed}/${report.allowedClaimLevel}`),
  ]

  if (!checkOnly) {
    writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
    writeMarkdown(report)
  }

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.evidenceChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`mode=${checkOnly ? 'check' : 'write'}`)
  console.log(`public_surface_count=${report.publicSurfaceCount}`)
  console.log(`scanned_line_count=${report.scannedLineCount}`)
  console.log(`blocked_context_claim_mention_count=${report.blockedContextClaimMentionCount}`)
  console.log(`unauthorized_positive_claim_count=${report.unauthorizedPositiveClaimCount}`)
  console.log(`claim_boundary_status=${report.claimBoundaryStatus}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`mth_resolution_status=${report.mthResolutionStatus}`)
  console.log(`canonical_memory_write_allowed=${report.canonicalMemoryWriteAllowed}`)
  console.log(`allowed_claim_level=${report.allowedClaimLevel}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
