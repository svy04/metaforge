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

export type PublicClaimSymbol =
  | 'Meta'
  | 'MFH'
  | 'Orchestra'
  | 'OpenClaude runtime'
  | 'Mimesis Engineering'
  | 'AVF Influence Factory'

export type PublicClaimEvidenceMapRow = {
  symbol: PublicClaimSymbol
  publicRole: string
  evidenceClass: string
  evidencePaths: string[]
  verificationCommand: string
  allowedClaim: string
  nonClaims: string[]
  unresolvedGap: string
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
  publicClaimEvidenceSymbolCount: number
  publicClaimEvidenceMap: PublicClaimEvidenceMapRow[]
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
const scanJsonlPath = 'reports/metaforge-public-claim-boundary.jsonl'
const checkOnly = process.argv.includes('--check')

const expectedPublicClaimSymbols: PublicClaimSymbol[] = [
  'Meta',
  'MFH',
  'Orchestra',
  'OpenClaude runtime',
  'Mimesis Engineering',
  'AVF Influence Factory',
]

export const publicClaimEvidenceMap: PublicClaimEvidenceMapRow[] = [
  {
    symbol: 'Meta',
    publicRole: 'Metaforge operating memory and state boundary for source ledgers, decisions, owner context, and goal state.',
    evidenceClass: 'governance/docs/gates',
    evidencePaths: [
      'docs/MFH_META_SYNTHESIS.md',
      'docs/GOAL_SCHEMA.md',
      'docs/AGENT_REGISTRY.md',
      'docs/PROJECT_SPEC.md',
    ],
    verificationCommand: 'bun run product:evidence-manifest',
    allowedClaim: 'Meta is the repo-local governance and operating-memory contract used to bind goals, decisions, and source-ledger state.',
    nonClaims: [
      'Meta is not a separately shipped runtime service in this checkout.',
      'Meta is not external validation of memory quality.',
      'Meta is not production readiness or autonomous reliability proof.',
    ],
    unresolvedGap: 'Runtime persistence and import paths beyond the documented governance surface still need behavior-level evidence before stronger module claims.',
  },
  {
    symbol: 'MFH',
    publicRole: 'Metaforge evidence-gated closure layer for claim boundaries, validation commands, and rollback-aware completion.',
    evidenceClass: 'governance/evidence-gate behavior docs',
    evidencePaths: [
      'docs/MFH_META_SYNTHESIS.md',
      'docs/EVALS.md',
      'docs/GOAL_SCHEMA.md',
      'docs/product-quality/goal-trace-validation-report.md',
      'docs/product-quality/goal-trace-validation-report.json',
      'docs/product-quality/real-session-trace-evals-report.md',
      'docs/product-quality/real-session-trace-evals-report.json',
      'docs/product-quality/public-claim-boundary-report.md',
      'docs/product-quality/product-evidence-manifest.md',
      'docs/goals/CG-002-static-analysis-ratchet.md',
      'docs/goals/traces/CG-001-goal-kernel-mvp.trace.json',
      'docs/goals/traces/CG-001-missing-evidence-rejected.trace.json',
      'docs/goals/traces/CG-001-protected-action-blocked.trace.json',
      'docs/goals/traces/CG-002-static-analysis-ratchet.trace.json',
      'docs/product-quality/dead-export-candidates-report.md',
      'docs/product-quality/dependency-topology-report.md',
      'docs/product-quality/script-duplication-audit-report.md',
      'docs/product-quality/static-analysis-remediation-queue-report.md',
    ],
    verificationCommand: 'bun run goals:validate && bun run product:real-trace-evals && bun run product:dead-export-candidates && bun run product:dependency-topology && bun run product:script-duplication-audit && bun run product:static-analysis-remediation-queue && bun run product:public-claim-boundary',
    allowedClaim: 'MFH is the repo-local evidence gate that constrains completion claims through docs, schemas, product-quality reports, representative cross-goal trace-validation evidence, local runtime behavior triad evidence, static-analysis ratchets, and a static-analysis remediation queue.',
    nonClaims: [
      'MFH is not a formal certification system.',
      'MFH is not external validation.',
      'MFH does not prove production, release, public, or autonomous reliability readiness.',
    ],
    unresolvedGap: 'live-provider evidence, broader non-fixture behavior coverage, and cross-environment side-effect coverage are still needed before MFH can carry broader reliability claims.',
  },
  {
    symbol: 'Orchestra',
    publicRole: 'Runtime routing, critique, review, promotion, and evidence-arbiter surface for Claude/Codex-backed agent roles.',
    evidenceClass: 'runtime-wired local no-provider evidence',
    evidencePaths: [
      'src/services/orchestra',
      'src/query/orchestra.test.ts',
      'docs/AGENT_REGISTRY.md',
      'docs/product-quality/real-session-trace-evals-report.md',
      'docs/product-quality/trace-schema-contract-report.md',
      'docs/product-quality/trajectory-process-quality-report.md',
      'docs/product-quality/protected-action-denial-trace-report.md',
    ],
    verificationCommand: 'bun test src/services/orchestra src/query/orchestra.test.ts',
    allowedClaim: 'Orchestra has repo-local runtime-wired source and test surfaces for routing, critique, review, promotion, and evidence arbitration.',
    nonClaims: [
      'Orchestra is not a hosted orchestration service.',
      'Orchestra is not live provider benchmark proof.',
      'Orchestra does not prove autonomous reliability.',
    ],
    unresolvedGap: 'Hosted execution, live-provider reliability, and external benchmark claims remain blocked until separately authorized and measured.',
  },
  {
    symbol: 'OpenClaude runtime',
    publicRole: 'Local CLI substrate for terminal UX, tools, MCP, slash commands, provider routing, streaming, and credential-backed model routes.',
    evidenceClass: 'runtime substrate',
    evidencePaths: [
      'src',
      'package.json',
      'docs/product-quality/provider-capability-matrix-report.md',
      'docs/product-quality/provider-compatibility-fixtures.md',
      'docs/product-quality/runtime-doctor-regression-fixtures.md',
      'docs/product-quality/permission-regression-fixtures.md',
      'docs/product-quality/origin-license-provenance-boundary-report.md',
      'docs/product-quality/oss-privacy-no-phone-home-evidence-report.md',
    ],
    verificationCommand: 'bun run build && bun run verify:privacy',
    allowedClaim: 'OpenClaude is the local CLI substrate that Metaforge rides on for tools, MCP, provider profiles, Claude routes, and Codex routes.',
    nonClaims: [
      'OpenClaude is not the product thesis.',
      'OpenClaude is not a blanket MIT-original CLI claim.',
      'OpenClaude is not production readiness, release readiness, or external validation.',
    ],
    unresolvedGap: 'Origin/license review, live-provider reachability, and stronger runtime behavior coverage remain prerequisites before heavier substrate promotion.',
  },
  {
    symbol: 'Mimesis Engineering',
    publicRole: 'Source-first improvement loop that absorbs proven OSS, papers, patents, standards, and product patterns into Metaforge work.',
    evidenceClass: 'source-ledger loop with non-public artifact guard',
    evidencePaths: [
      'docs/MIMESIS_ENGINEERING.md',
      'docs/research/mimesis-engineering-source-ledger-2026-06-14.md',
      'docs/product-quality/primary-source-registry-report.md',
      'docs/product-quality/product-evidence-manifest.md',
    ],
    verificationCommand: 'bun run product:primary-source-registry',
    allowedClaim: 'Mimesis Engineering is the repo-local source-first improvement method for turning primary sources into bounded product-quality work.',
    nonClaims: [
      'Mimesis Engineering is not a default runtime module.',
      'Mimesis Engineering is not external validation or a universal quality lift.',
      'Mimesis Engineering does not make unpublished pre-public artifacts public proof.',
    ],
    unresolvedGap: 'Non-public artifact evidence stays outside public proof until sanitized, source-controlled, and re-verified.',
  },
  {
    symbol: 'AVF Influence Factory',
    publicRole: 'Manual artifact lane for venture/factory packets, operator runbooks, routing policies, and owner-review artifacts.',
    evidenceClass: 'manual artifact lane',
    evidencePaths: [
      'avf',
      'avf/influence_factory/operator_runs.md',
      'avf/influence_factory/product_track_spec.md',
      'docs/avf/WEB_FIRST_AUTONOMOUS_VENTURE_FACTORY_SPEC.md',
      'docs/product-quality/public-claim-boundary-report.md',
      'docs/product-quality/dependency-topology-report.md',
      'docs/product-quality/dead-export-candidates-report.md',
    ],
    verificationCommand: 'python scripts\\validate_avf_influence_factory_completion_candidate_v42.py',
    allowedClaim: 'AVF Influence Factory is a repo-local manual artifact lane with tracked schemas, runbooks, product-track notes, and boundary documentation.',
    nonClaims: [
      'AVF Influence Factory is not a default CLI runtime import.',
      'AVF Influence Factory is not an active automation claim.',
      'AVF Influence Factory does not prove generated public artifacts, release readiness, or external validation.',
    ],
    unresolvedGap: 'Runtime imports, generated public artifacts, and behavior tests are still required before marketing AVF as an active module.',
  },
]

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
  'docs/marketing/metaforge-public-proof-pack-2026-06-18.md',
  'docs/marketing/metaforge-public-proof-pack-2026-06-14.md',
  'docs/profile/github-profile-refresh-evidence-2026-06-19.md',
  'docs/profile/github-profile-refresh-evidence-2026-06-14.md',
  'docs/research/public-proof-pack-source-ledger-2026-06-18.md',
  'docs/research/public-proof-pack-source-ledger-2026-06-14.md',
  'packages/openclaude-vscode/package.json',
  'packages/openclaude-vscode/README.md',
  'vscode-extension/openclaude-vscode/package.json',
  'vscode-extension/openclaude-vscode/README.md',
  ...publicMarkdownReportPaths(),
  ...publicGoalArtifactPaths(),
].filter((path, index, paths) => paths.indexOf(path) === index).sort()

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
  'required terms present',
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

function publicMarkdownReportPaths(): string[] {
  return [
    ...markdownPathsUnder('docs/product-quality', new Set([
      reportMdPath,
      'docs/product-quality/product-evidence-manifest.md',
    ])),
    ...markdownPathsUnder('docs/marketing'),
  ]
}

function markdownPathsUnder(relativeDir: string, excludedPaths = new Set<string>()): string[] {
  const dir = resolve(root, relativeDir)
  if (!existsSync(dir)) {
    return []
  }

  const paths: string[] = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const relativePath = `${relativeDir}/${entry.name}`
    if (entry.isDirectory()) {
      paths.push(...markdownPathsUnder(relativePath, excludedPaths))
      continue
    }
    if (entry.isFile() && entry.name.endsWith('.md') && !excludedPaths.has(relativePath)) {
      paths.push(relativePath)
    }
  }
  return paths.sort()
}

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
  return isBlockedContext(compact) && (/[:：]\s*$/.test(compact) || /^#{1,6}\s+/.test(compact))
}

function isMarkdownTableRow(line: string): boolean {
  return /^\s*\|.*\|\s*$/.test(line)
}

function findTableBlockingContextLine(contextLines: string[]): string | null {
  for (let index = contextLines.length - 2; index >= 0; index -= 1) {
    const candidate = contextLines[index]
    if (candidate.trim().length === 0) {
      return null
    }
    if (!isMarkdownTableRow(candidate)) {
      return null
    }
    if (isBlockedContext(candidate)) {
      return candidate
    }
  }

  return null
}

function findBlockingContextLine(contextLines: string[], claimLine: string): string | null {
  const currentLine = contextLines.at(-1) ?? claimLine
  if (isBlockedContext(currentLine)) {
    return currentLine
  }

  if (isMarkdownTableRow(claimLine)) {
    return findTableBlockingContextLine(contextLines)
  }

  if (!isListItem(claimLine)) {
    if (!isIndentedContinuation(claimLine)) {
      const previousLine = contextLines.at(-2)
      if (previousLine?.trim() && isBlockedContext(previousLine)) {
        return previousLine
      }
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
    if (isListItem(candidate) && isBlockedContext(candidate)) {
      return candidate
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

function publicClaimEvidenceMissingPaths(): string[] {
  return publicClaimEvidenceMap
    .flatMap((row) => row.evidencePaths)
    .filter((path, index, paths) => paths.indexOf(path) === index)
    .filter((path) => !existsSync(resolve(root, path)))
}

function publicClaimSymbolsMatchExpectedOrder(): boolean {
  return JSON.stringify(publicClaimEvidenceMap.map((row) => row.symbol)) === JSON.stringify(expectedPublicClaimSymbols)
}

type GeneratedArtifact = {
  path: string
  content: string
}

function renderMarkdown(report: PublicClaimBoundaryReport): string {
  const surfaceRows = report.scannedPublicSurfaces
    .map((surface) => `| \`${surface.path}\` | \`${surface.exists}\` | \`${surface.sha256 ?? 'missing'}\` | ${surface.lineCount} |`)
    .join('\n')
  const publicClaimEvidenceRows = report.publicClaimEvidenceMap
    .map((row) => `| \`${row.symbol}\` | ${markdownCell(row.publicRole)} | \`${row.evidenceClass}\` | ${markdownCell(row.allowedClaim)} | ${markdownCell(row.nonClaims.join('; '))} | ${markdownCell(row.unresolvedGap)} |`)
    .join('\n')
  const publicClaimEvidencePathSections = report.publicClaimEvidenceMap
    .map((row) => [
      `### ${row.symbol}`,
      '',
      `- verification_command: \`${row.verificationCommand}\``,
      ...row.evidencePaths.map((path) => `- \`${path}\``),
    ].join('\n'))
    .join('\n\n')
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

  return `# Public Claim Boundary Report

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
- public_claim_evidence_symbol_count: \`${report.publicClaimEvidenceSymbolCount}\`
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

## Public Claim Evidence Map

This map binds public Metaforge symbols to local evidence, allowed claims, explicit non-claims, and unresolved gaps. It is local no-provider evidence mapping only, not external validation.

| Symbol | Public role | Evidence class | Allowed claim | Non-claims | Unresolved gap |
| --- | --- | --- | --- | --- | --- |
${publicClaimEvidenceRows}

## Public Claim Evidence Paths

${publicClaimEvidencePathSections}

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
}

function renderReportJson(report: PublicClaimBoundaryReport): string {
  return `${JSON.stringify(report, null, 2)}\n`
}

function generatedArtifactChecks(artifacts: GeneratedArtifact[]): Check[] {
  return artifacts.map((artifact) => {
    const absolutePath = resolve(root, artifact.path)
    if (!existsSync(absolutePath)) {
      return check(`generated ${artifact.path} is current`, false, 'missing: run bun run product:public-claim-boundary')
    }

    const actual = readText(artifact.path)
    return check(
      `generated ${artifact.path} is current`,
      actual === artifact.content,
      actual === artifact.content ? 'current' : 'stale: run bun run product:public-claim-boundary',
    )
  })
}

function existingReportGeneratedAt(): string | null {
  if (!existsSync(resolve(root, reportJsonPath))) {
    return null
  }

  try {
    const parsed = JSON.parse(readText(reportJsonPath)) as { generatedAt?: unknown }
    return typeof parsed.generatedAt === 'string' && parsed.generatedAt.length > 0
      ? parsed.generatedAt
      : null
  } catch {
    return null
  }
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
    generatedAt: checkOnly ? existingReportGeneratedAt() ?? new Date().toISOString() : new Date().toISOString(),
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
        sourceProject: 'in-toto Attestation Framework',
        sourceUrl: 'https://github.com/in-toto/attestation/blob/main/spec/README.md',
        observedPattern: 'Subject-to-predicate evidence binding keeps proof surfaces explicit instead of narrative-only.',
      },
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence and provenance boundaries should stay separate from release, production, and external-attestation claims until those steps are actually authorized and performed.',
      },
      {
        sourceProject: 'NIST SSDF SP 800-218',
        sourceUrl: 'https://csrc.nist.gov/pubs/sp/800/218/final',
        observedPattern: 'Secure-development practices and evidence records reduce communication and vulnerability risk without implying compliance from local reports alone.',
      },
      {
        sourceProject: 'W3C PROV',
        sourceUrl: 'https://www.w3.org/TR/prov-overview/',
        observedPattern: 'Provenance should bind produced artifacts to activities and responsible actors so reliability and trustworthiness assessments do not depend on narrative alone.',
      },
      {
        sourceProject: 'NIST AI RMF Core',
        sourceUrl: 'https://airc.nist.gov/airmf-resources/airmf/5-sec-core/',
        observedPattern: 'AI risk work should be governed, mapped, measured, and managed continuously rather than reduced to a one-time checklist.',
      },
      {
        sourceProject: 'OpenAI Evals',
        sourceUrl: 'https://github.com/openai/evals',
        observedPattern: 'LLM-system quality claims should be tied to explicit evals or private workflow evals instead of broad model or agent assertions.',
      },
      {
        sourceProject: 'GitHub CodeQL code scanning',
        sourceUrl: 'https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning',
        observedPattern: 'CodeQL-backed public security signals should distinguish configured analysis and alerts from stronger hosted-execution or remediation claims.',
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
    publicClaimEvidenceSymbolCount: publicClaimEvidenceMap.length,
    publicClaimEvidenceMap,
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
    check('public claim evidence map covers expected symbols', publicClaimSymbolsMatchExpectedOrder(), publicClaimEvidenceMap.map((row) => row.symbol).join(',')),
    check('public claim evidence paths exist', publicClaimEvidenceMissingPaths().length === 0, publicClaimEvidenceMissingPaths().join(',') || 'all present'),
    check('public claim evidence rows include allowed claims non-claims and gaps', publicClaimEvidenceMap.every((row) => row.allowedClaim.length > 0 && row.nonClaims.length > 0 && row.unresolvedGap.length > 0), `${publicClaimEvidenceMap.length} rows`),
    check('MFH behavior evidence is bound to trace validation', publicClaimEvidenceMap.some((row) => (
      row.symbol === 'MFH' &&
      row.evidenceClass.includes('behavior') &&
      row.evidencePaths.includes('docs/product-quality/goal-trace-validation-report.md') &&
      row.evidencePaths.includes('docs/product-quality/goal-trace-validation-report.json') &&
      row.evidencePaths.includes('docs/product-quality/real-session-trace-evals-report.md') &&
      row.evidencePaths.includes('docs/product-quality/real-session-trace-evals-report.json') &&
      row.evidencePaths.includes('docs/goals/traces/CG-001-goal-kernel-mvp.trace.json') &&
      row.evidencePaths.includes('docs/goals/traces/CG-001-missing-evidence-rejected.trace.json') &&
      row.evidencePaths.includes('docs/goals/traces/CG-001-protected-action-blocked.trace.json') &&
      row.evidencePaths.includes('docs/goals/CG-002-static-analysis-ratchet.md') &&
      row.evidencePaths.includes('docs/goals/traces/CG-002-static-analysis-ratchet.trace.json') &&
      row.evidencePaths.includes('docs/product-quality/dead-export-candidates-report.md') &&
      row.evidencePaths.includes('docs/product-quality/dependency-topology-report.md') &&
      row.evidencePaths.includes('docs/product-quality/script-duplication-audit-report.md') &&
      row.evidencePaths.includes('docs/product-quality/static-analysis-remediation-queue-report.md') &&
      row.verificationCommand.includes('goals:validate') &&
      row.verificationCommand.includes('product:real-trace-evals') &&
      row.verificationCommand.includes('product:dead-export-candidates') &&
      row.verificationCommand.includes('product:dependency-topology') &&
      row.verificationCommand.includes('product:script-duplication-audit') &&
      row.verificationCommand.includes('product:static-analysis-remediation-queue') &&
      row.allowedClaim.includes('representative cross-goal trace-validation evidence') &&
      row.allowedClaim.includes('local runtime behavior triad evidence') &&
      row.allowedClaim.includes('static-analysis ratchets') &&
      row.allowedClaim.includes('static-analysis remediation queue') &&
      row.unresolvedGap.includes('broader non-fixture behavior coverage') &&
      row.unresolvedGap.includes('live-provider evidence') &&
      !row.unresolvedGap.includes('Runtime traces beyond docs-governance and static-analysis goals')
    )), 'MFH row includes representative trace fixtures, runtime behavior triad evidence, CG-002 static-analysis ratchet evidence, remediation queue evidence, goals validation, and remaining live-provider/non-fixture gaps'),
    check('OpenClaude remains substrate rather than thesis', publicClaimEvidenceMap.some((row) => row.symbol === 'OpenClaude runtime' && row.publicRole.includes('substrate') && row.allowedClaim.includes('local CLI substrate') && row.nonClaims.some((item) => item.includes('not the product thesis'))), 'substrate boundary present'),
    check('AVF remains manual artifact lane not default runtime', publicClaimEvidenceMap.some((row) => row.symbol === 'AVF Influence Factory' && row.evidenceClass.includes('manual artifact') && row.nonClaims.some((item) => item.includes('not a default CLI runtime import'))), 'AVF manual lane boundary present'),
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

  const generatedArtifacts: GeneratedArtifact[] = [
    { path: scanJsonlPath, content: scanJsonlText },
    { path: reportJsonPath, content: renderReportJson(report) },
    { path: reportMdPath, content: renderMarkdown(report) },
  ]

  if (!checkOnly) {
    for (const artifact of generatedArtifacts) {
      writeFileSync(resolve(root, artifact.path), artifact.content)
    }
  }

  const outputChecks = [...report.evidenceChecks, ...generatedArtifactChecks(generatedArtifacts)]

  for (const item of outputChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = outputChecks.filter((item) => !item.ok)
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
