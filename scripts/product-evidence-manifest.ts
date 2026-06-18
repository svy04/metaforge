import { createHash } from 'node:crypto'
import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { check, sha256 as sha256Text } from './quality-report-helpers'
import { isHistoricalLiveProbeTracePath } from './product-trace-discovery'

export type EvidenceCheck = {
  label: string
  ok: boolean
  detail: string
}

export type EvidenceRecord = {
  path: string
  sha256: string
  sizeBytes: number
  role: 'source' | 'evidence_report' | 'evidence_artifact' | 'quality_gate' | 'workflow'
}

export type EvidenceProofClass =
  | 'behavioral_runtime'
  | 'static_analysis'
  | 'governance_boundary'
  | 'source_control'
  | 'structural_inventory'

export type ProductEvidenceManifestReport = {
  generatedAt: string
  mode: 'local_no_provider_product_evidence_manifest'
  manifestFormat: 'openclaude_product_evidence_manifest_v1'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  manifestJsonlPath: string
  manifestJsonlSha256: string
  evidenceRecordCount: number
  evidenceTotalSizeBytes: number
  evidenceRoles: Record<EvidenceRecord['role'], number>
  evidenceProofClasses: Record<EvidenceProofClass, number>
  requiredEvidencePaths: string[]
  missingRequiredEvidencePaths: string[]
  recursiveSelfInputsExcluded: string[]
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalAttestationGenerated: false
  signedProvenanceGenerated: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  evidenceRecords: EvidenceRecord[]
  evidenceChecks: EvidenceCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const manifestJsonlPath = 'reports/openclaude-product-evidence-manifest.jsonl'
export const selfReportPaths = [
  'docs/product-quality/product-evidence-manifest.json',
  'docs/product-quality/product-evidence-manifest.md',
  manifestJsonlPath,
]

const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /github_pat_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

export const rawRequiredEvidencePaths = [
  'package.json',
  'bun.lock',
  'knip.jsonc',
  '.jscpd.json',
  '.dependency-cruiser.mjs',
  '.dependency-cruiser-known-violations.json',
  '.github/CODEOWNERS',
  '.github/workflows/pr-checks.yml',
  '.github/workflows/codeql.yml',
  '.github/workflows/dependency-review.yml',
  '.github/dependabot.yml',
  'docs/product-quality/oss-top10-baseline-2026-05-17.json',
  'docs/product-quality/oss-top10-baseline-2026-05-21.json',
  'docs/product-quality/oss-baseline-refresh-report.json',
  'docs/product-quality/oss-baseline-refresh-report.md',
  'reports/openclaude-oss-baseline-refresh-provenance.jsonl',
  'docs/product-quality/oss-baseline-freshness-report.json',
  'docs/product-quality/oss-baseline-freshness-report.md',
  'reports/openclaude-oss-baseline-provenance.jsonl',
  'docs/product-quality/oss-source-review-report.json',
  'docs/product-quality/oss-source-review-report.md',
  'reports/openclaude-oss-source-review-provenance.jsonl',
  'docs/product-quality/oss-architecture-absorption-targets-report.json',
  'docs/product-quality/oss-architecture-absorption-targets-report.md',
  'reports/openclaude-oss-architecture-absorption-targets.jsonl',
  'docs/product-quality/oss-architecture-gap-review-report.json',
  'docs/product-quality/oss-architecture-gap-review-report.md',
  'reports/openclaude-oss-architecture-gap-review.jsonl',
  'docs/product-quality/oss-axis-architecture-review-report.json',
  'docs/product-quality/oss-axis-architecture-review-report.md',
  'reports/openclaude-oss-axis-architecture-review.jsonl',
  'docs/product-quality/oss-safe-backlog-plan-report.json',
  'docs/product-quality/oss-safe-backlog-plan-report.md',
  'reports/openclaude-oss-safe-backlog-plan.jsonl',
  'docs/product-quality/oss-safe-backlog-closure-report.json',
  'docs/product-quality/oss-safe-backlog-closure-report.md',
  'reports/openclaude-oss-safe-backlog-closure.jsonl',
  'docs/product-quality/oss-baseline-drift-closure-report.json',
  'docs/product-quality/oss-baseline-drift-closure-report.md',
  'reports/openclaude-oss-baseline-drift-closure.jsonl',
  'docs/product-quality/oss-benchmark-comparison-matrix-report.json',
  'docs/product-quality/oss-benchmark-comparison-matrix-report.md',
  'reports/openclaude-oss-benchmark-comparison-matrix.jsonl',
  'docs/product-quality/oss-comparison-readiness-index-report.json',
  'docs/product-quality/oss-comparison-readiness-index-report.md',
  'reports/openclaude-oss-comparison-readiness-index.jsonl',
  'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json',
  'docs/product-quality/oss-ide-or-editor-surface-evidence-report.md',
  'reports/openclaude-oss-ide-or-editor-surface-evidence.jsonl',
  'docs/product-quality/oss-eval-quality-gate-checklist-report.json',
  'docs/product-quality/oss-eval-quality-gate-checklist-report.md',
  'reports/openclaude-oss-eval-quality-gate-checklist.jsonl',
  'docs/product-quality/oss-terminal-workflow-evidence-report.json',
  'docs/product-quality/oss-terminal-workflow-evidence-report.md',
  'reports/openclaude-oss-terminal-workflow-evidence.jsonl',
  'docs/product-quality/oss-onboarding-docs-evidence-report.json',
  'docs/product-quality/oss-onboarding-docs-evidence-report.md',
  'reports/openclaude-oss-onboarding-docs-evidence.jsonl',
  'docs/product-quality/oss-runtime-doctoring-evidence-report.json',
  'docs/product-quality/oss-runtime-doctoring-evidence-report.md',
  'reports/openclaude-oss-runtime-doctoring-evidence.jsonl',
  'docs/product-quality/oss-security-permissions-evidence-report.json',
  'docs/product-quality/oss-security-permissions-evidence-report.md',
  'reports/openclaude-oss-security-permissions-evidence.jsonl',
  'docs/product-quality/oss-tool-loop-reliability-evidence-report.json',
  'docs/product-quality/oss-tool-loop-reliability-evidence-report.md',
  'reports/openclaude-oss-tool-loop-reliability-evidence.jsonl',
  'docs/product-quality/oss-provider-breadth-evidence-report.json',
  'docs/product-quality/oss-provider-breadth-evidence-report.md',
  'reports/openclaude-oss-provider-breadth-evidence.jsonl',
  'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json',
  'docs/product-quality/oss-privacy-no-phone-home-evidence-report.md',
  'reports/openclaude-oss-privacy-no-phone-home-evidence.jsonl',
  'docs/product-quality/oss-release-hygiene-evidence-report.json',
  'docs/product-quality/oss-release-hygiene-evidence-report.md',
  'reports/openclaude-oss-release-hygiene-evidence.jsonl',
  'docs/product-quality/provider-capability-matrix-report.json',
  'docs/product-quality/provider-capability-matrix-report.md',
  'reports/openclaude-provider-capability-matrix.jsonl',
  'docs/product-quality/terminal-failure-recovery-transcripts-report.json',
  'docs/product-quality/terminal-failure-recovery-transcripts-report.md',
  'docs/product-quality/tool-interruption-recovery-trace-report.json',
  'docs/product-quality/tool-interruption-recovery-trace-report.md',
  'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
  'docs/product-quality/protected-action-denial-trace-report.json',
  'docs/product-quality/protected-action-denial-trace-report.md',
  'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
  'docs/product-quality/product-quality-gate.md',
  'docs/product-quality/terminal-report.md',
  'docs/product-quality/verification-report-2026-05-17.md',
  'docs/product-quality/primary-source-registry-report.json',
  'docs/product-quality/primary-source-registry-report.md',
  'reports/openclaude-primary-source-registry.jsonl',
  'docs/product-quality/agent-instructions-quality-report.json',
  'docs/product-quality/community-intake-quality-report.json',
  'docs/product-quality/community-profile-quality-report.json',
  'docs/product-quality/dependency-topology-report.json',
  'docs/product-quality/dependency-topology-report.md',
  'docs/product-quality/script-duplication-audit-report.json',
  'docs/product-quality/script-duplication-audit-report.md',
  'docs/product-quality/dead-export-candidates-report.json',
  'docs/product-quality/dead-export-candidates-report.md',
  'docs/product-quality/dead-export-candidate-triage.json',
  'docs/product-quality/maintainer-ownership-quality-report.json',
  'docs/product-quality/dependency-governance-quality-report.json',
  'docs/product-quality/lockfile-sbom-quality-report.json',
  'reports/openclaude-lockfile-sbom-inventory.jsonl',
  'docs/product-quality/third-party-license-quality-report.json',
  'reports/openclaude-third-party-license-inventory.jsonl',
  'docs/product-quality/source-license-metadata-quality-report.json',
  'reports/openclaude-source-license-metadata-inventory.jsonl',
  'docs/product-quality/license-boundary-authorization-report.json',
  'docs/product-quality/license-boundary-authorization-request.md',
  'reports/openclaude-license-boundary-authorization-items.jsonl',
  'docs/product-quality/quality-blocker-taxonomy-report.json',
  'docs/product-quality/public-claim-boundary-report.json',
  'docs/product-quality/public-claim-boundary-report.md',
  'reports/openclaude-public-claim-boundary.jsonl',
  'docs/product-quality/github-remote-surface-audit-report.json',
  'docs/product-quality/github-remote-surface-audit-report.md',
  'reports/openclaude-github-remote-surface-audit.jsonl',
  'docs/product-quality/github-hosted-trust-posture-report.json',
  'docs/product-quality/github-hosted-trust-posture-report.md',
  'reports/openclaude-github-hosted-trust-posture.jsonl',
  'docs/product-quality/code-scanning-remediation-queue-report.json',
  'docs/product-quality/code-scanning-remediation-queue-report.md',
  'reports/openclaude-code-scanning-remediation-queue.jsonl',
  'docs/product-quality/origin-license-provenance-boundary-report.json',
  'docs/product-quality/origin-license-provenance-boundary-report.md',
  'reports/openclaude-origin-license-provenance-boundary.jsonl',
  'docs/product-quality/protected-action-authorization-packet.json',
  'docs/product-quality/protected-action-authorization-packet.md',
  'reports/openclaude-protected-action-authorization-packet.jsonl',
  'docs/product-quality/trace-portability-export-report.json',
  'docs/product-quality/benchmark-readiness-matrix.json',
  'docs/product-quality/vscode-startup-diagnostics-report.json',
  'docs/product-quality/local-benchmark-harness-report.json',
  'docs/product-quality/benchmark-efficiency-metrics-report.json',
  'docs/product-quality/benchmark-submission-readiness-report.json',
  'docs/product-quality/benchmark-policy-compliance-report.json',
  'docs/product-quality/terminal-bench-readiness-report.json',
  'docs/product-quality/openssf-security-posture-report.json',
  'reports/openclaude-portable-trace-events.jsonl',
  'reports/openclaude-benchmark-task-manifest.jsonl',
  'reports/openclaude-local-benchmark-results.jsonl',
  'reports/openclaude-benchmark-efficiency-metrics.jsonl',
  'reports/openclaude-benchmark-submission-assets.jsonl',
  'reports/openclaude-benchmark-policy-compliance.jsonl',
  'reports/openclaude-terminal-bench-task-map.jsonl',
]

function listGitTrackedPaths(prefix: string): string[] {
  const result = spawnSync('git', ['ls-files', '--', prefix], {
    cwd: root,
    encoding: 'utf8',
  })
  if (result.status !== 0) {
    return []
  }
  return result.stdout
    .split(/\r?\n/)
    .map((path) => normalizePath(path.trim()))
    .filter((path) => path.length > 0)
}

export function filterSourceControlledEvidencePaths(paths: string[], trackedPaths: Set<string>): string[] {
  return paths.filter((path) => !normalizePath(path).startsWith('reports/') || trackedPaths.has(normalizePath(path)))
}

export const requiredEvidencePaths = filterSourceControlledEvidencePaths(
  rawRequiredEvidencePaths,
  new Set(listGitTrackedPaths('reports')),
)

function sha256Buffer(buffer: Buffer): string {
  return createHash('sha256').update(buffer).digest('hex')
}

export function hasCredentialPattern(text: string): boolean {
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function normalizePath(path: string): string {
  return path.replace(/\\/g, '/')
}

function listFiles(prefix: string): string[] {
  const absolutePrefix = resolve(root, prefix)
  if (!existsSync(absolutePrefix)) return []
  const files: string[] = []
  const walk = (absoluteDir: string, relativeDir: string): void => {
    for (const entry of readdirSync(absoluteDir, { withFileTypes: true })) {
      const absolutePath = join(absoluteDir, entry.name)
      const relativePath = normalizePath(join(relativeDir, entry.name))
      if (entry.isDirectory()) {
        walk(absolutePath, relativePath)
      } else if (entry.isFile()) {
        files.push(relativePath)
      }
    }
  }
  walk(absolutePrefix, prefix)
  return files.sort((left, right) => left.localeCompare(right))
}

export function roleFor(path: string): EvidenceRecord['role'] {
  if (path === 'package.json') return 'source'
  if (path === 'bun.lock') return 'source'
  if (path.startsWith('.github/')) return 'workflow'
  if (path === 'docs/product-quality/product-quality-gate.md') return 'quality_gate'
  if (path.startsWith('docs/product-quality/')) return 'evidence_report'
  return 'evidence_artifact'
}

export function proofClassFor(path: string): EvidenceProofClass {
  const normalized = normalizePath(path).toLowerCase()
  if (
    normalized.includes('transcript') ||
    normalized.includes('trace') ||
    normalized.includes('smoke') ||
    normalized.includes('runtime-doctor') ||
    normalized.includes('permission-regression') ||
    normalized.includes('provider-compatibility') ||
    normalized.includes('local-benchmark') ||
    normalized.includes('agent-replay') ||
    normalized.includes('real-session') ||
    normalized.includes('tool-interruption') ||
    normalized.includes('protected-action-denial') ||
    normalized.includes('prompted-tool-loop') ||
    normalized.includes('code-editing-trace')
  ) {
    return 'behavioral_runtime'
  }
  if (
    normalized.includes('jscpd') ||
    normalized.includes('dependency-cruiser') ||
    normalized.includes('dependency-topology') ||
    normalized.includes('dead-export') ||
    normalized.includes('script-duplication') ||
    normalized.includes('knip')
  ) {
    return 'static_analysis'
  }
  if (
    normalized.includes('claim') ||
    normalized.includes('license') ||
    normalized.includes('authorization') ||
    normalized.includes('openssf') ||
    normalized.includes('governance') ||
    normalized.includes('policy') ||
    normalized.includes('readiness') ||
    normalized.includes('quality-blocker') ||
    normalized.includes('public-feedback') ||
    normalized.includes('agent-instructions') ||
    normalized.includes('community')
  ) {
    return 'governance_boundary'
  }
  if (
    normalized === 'package.json' ||
    normalized === 'bun.lock' ||
    normalized.startsWith('.github/') ||
    normalized.endsWith('product-quality-gate.md')
  ) {
    return 'source_control'
  }
  return 'structural_inventory'
}

function buildEvidenceRecords(): EvidenceRecord[] {
  const trackedReportPaths = listGitTrackedPaths('reports')
  const candidatePaths = [
    'package.json',
    'bun.lock',
    'knip.jsonc',
    '.jscpd.json',
    '.dependency-cruiser.mjs',
    '.dependency-cruiser-known-violations.json',
    ...listFiles('docs/product-quality'),
    ...trackedReportPaths
      .filter((path) => /^reports\/(openclaude-|orchestra-)/.test(path))
      .filter((path) => !isHistoricalLiveProbeTracePath(path)),
    ...listFiles('.github').filter((path) => /\.(ya?ml)$/.test(path) || path === '.github/CODEOWNERS'),
  ]
  const uniquePaths = [...new Set(candidatePaths)]
    .filter((path) => !selfReportPaths.includes(path))
    .filter((path) => existsSync(resolve(root, path)))
    .sort((left, right) => left.localeCompare(right))

  return uniquePaths.map((path) => {
    const absolutePath = resolve(root, path)
    const bytes = readFileSync(absolutePath)
    return {
      path,
      sha256: sha256Buffer(bytes),
      sizeBytes: statSync(absolutePath).size,
      role: roleFor(path),
    }
  })
}

export function countRoles(records: EvidenceRecord[]): Record<EvidenceRecord['role'], number> {
  return {
    source: records.filter((record) => record.role === 'source').length,
    evidence_report: records.filter((record) => record.role === 'evidence_report').length,
    evidence_artifact: records.filter((record) => record.role === 'evidence_artifact').length,
    quality_gate: records.filter((record) => record.role === 'quality_gate').length,
    workflow: records.filter((record) => record.role === 'workflow').length,
  }
}

export function countProofClasses(records: EvidenceRecord[]): Record<EvidenceProofClass, number> {
  return {
    behavioral_runtime: records.filter((record) => proofClassFor(record.path) === 'behavioral_runtime').length,
    static_analysis: records.filter((record) => proofClassFor(record.path) === 'static_analysis').length,
    governance_boundary: records.filter((record) => proofClassFor(record.path) === 'governance_boundary').length,
    source_control: records.filter((record) => proofClassFor(record.path) === 'source_control').length,
    structural_inventory: records.filter((record) => proofClassFor(record.path) === 'structural_inventory').length,
  }
}

export function buildEvidenceManifestJsonl(evidenceRecords: EvidenceRecord[]): string {
  return `${evidenceRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
}

export function buildProductEvidenceManifestReport({
  evidenceRecords,
  generatedAt = new Date().toISOString(),
  requiredPaths = requiredEvidencePaths,
  recursiveSelfInputs = selfReportPaths,
  outputManifestJsonlPath = manifestJsonlPath,
}: {
  evidenceRecords: EvidenceRecord[]
  generatedAt?: string
  requiredPaths?: string[]
  recursiveSelfInputs?: string[]
  outputManifestJsonlPath?: string
}): { report: ProductEvidenceManifestReport, manifestText: string } {
  const manifestText = buildEvidenceManifestJsonl(evidenceRecords)
  const manifestJsonlSha256 = sha256Text(manifestText)
  const missingRequiredEvidencePaths = requiredPaths.filter((path) => !evidenceRecords.some((record) => record.path === path))
  const evidenceRoles = countRoles(evidenceRecords)
  const evidenceProofClasses = countProofClasses(evidenceRecords)
  const evidenceTotalSizeBytes = evidenceRecords.reduce((total, record) => total + record.sizeBytes, 0)
  const manifestHasCredentialPattern = hasCredentialPattern(manifestText)

  const evidenceChecks = [
    check('required evidence paths are present', missingRequiredEvidencePaths.length === 0, missingRequiredEvidencePaths.join(',') || 'all present'),
    check('evidence records have SHA-256 digests', evidenceRecords.every((record) => /^[a-f0-9]{64}$/.test(record.sha256)), `${evidenceRecords.length} records`),
    check('evidence records have nonzero sizes', evidenceRecords.every((record) => record.sizeBytes > 0), `${evidenceTotalSizeBytes} total bytes`),
    check('manifest JSONL has one line per evidence record', manifestText.trim().split(/\r?\n/).length === evidenceRecords.length, `${evidenceRecords.length} lines`),
    check('manifest JSONL hash is recorded', manifestJsonlSha256.length === 64, outputManifestJsonlPath),
    check('recursive self inputs are excluded', recursiveSelfInputs.every((path) => !evidenceRecords.some((record) => record.path === path)), recursiveSelfInputs.join(',')),
    check('evidence roles cover reports, artifacts, workflows, source, and gate', Object.values(evidenceRoles).every((count) => count > 0), JSON.stringify(evidenceRoles)),
    check(
      'behavioral evidence is separated from structural audit evidence',
      evidenceProofClasses.behavioral_runtime > 0 && evidenceProofClasses.static_analysis > 0,
      JSON.stringify(evidenceProofClasses),
    ),
    check('manifest contains no credential patterns', !manifestHasCredentialPattern, 'known key/token/private-key patterns absent'),
    check('primary source patterns are recorded', true, 'SLSA provenance, in-toto Statement, OpenSSF Scorecard'),
    check('protected actions are not executed', true, 'protectedActionsExecuted=[]'),
    check('release and external claims remain blocked', true, 'all claim flags false'),
  ]

  const report: ProductEvidenceManifestReport = {
    generatedAt,
    mode: 'local_no_provider_product_evidence_manifest',
    manifestFormat: 'openclaude_product_evidence_manifest_v1',
    primarySourceInputs: [
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Provenance records identify subjects, build definitions, run details, and dependencies so artifacts can be traced back to how they were produced.',
      },
      {
        sourceProject: 'in-toto Attestation Framework',
        sourceUrl: 'https://github.com/in-toto/attestation',
        observedPattern: 'A Statement binds subjects to a typed predicate, making evidence packages machine-checkable instead of narrative-only.',
      },
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'Open-source security posture is stronger when checks, evidence, and remediation boundaries are explicit and repeatable.',
      },
    ],
    manifestJsonlPath: outputManifestJsonlPath,
    manifestJsonlSha256,
    evidenceRecordCount: evidenceRecords.length,
    evidenceTotalSizeBytes,
    evidenceRoles,
    evidenceProofClasses,
    requiredEvidencePaths: requiredPaths,
    missingRequiredEvidencePaths,
    recursiveSelfInputsExcluded: recursiveSelfInputs,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    externalAttestationGenerated: false,
    signedProvenanceGenerated: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    evidenceRecords,
    evidenceChecks,
    claimBoundary: 'Product evidence manifest is local no-provider evidence packaging only. Proof classes are path-derived evidence buckets for claim hygiene, not external validation. The manifest is not a signed attestation and does not authorize release, production, public, external-validation, or autonomous-reliability claims.',
  }

  return { report, manifestText }
}

function writeMarkdown(report: ProductEvidenceManifestReport): void {
  const requiredRows = report.requiredEvidencePaths
    .map((path) => `| \`${path}\` | \`${!report.missingRequiredEvidencePaths.includes(path)}\` |`)
    .join('\n')
  const roleRows = Object.entries(report.evidenceRoles)
    .map(([role, count]) => `| \`${role}\` | ${count} |`)
    .join('\n')
  const proofClassRows = Object.entries(report.evidenceProofClasses)
    .map(([proofClass, count]) => `| \`${proofClass}\` | ${count} |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Product Evidence Manifest

Generated by: \`bun run product:evidence-manifest\`

## Claim Boundary

- This is a local no-provider manifest of OpenClaude product-quality evidence files.
- It follows SLSA/in-toto-style subject/materials discipline as an unsigned local evidence package, not as a signed external attestation.
- It does not call providers, live models, or external services.
- It does not publish, deploy, launch, modify production, sign provenance, or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- manifest_format: \`${report.manifestFormat}\`
- manifest_jsonl_path: \`${report.manifestJsonlPath}\`
- manifest_jsonl_sha256: \`${report.manifestJsonlSha256}\`
- evidence_record_count: \`${report.evidenceRecordCount}\`
- evidence_total_size_bytes: \`${report.evidenceTotalSizeBytes}\`
- external_attestation_generated: \`${report.externalAttestationGenerated}\`
- signed_provenance_generated: \`${report.signedProvenanceGenerated}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${report.primarySourceInputs.map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`).join('\n')}

## Evidence Roles

| Role | Count |
| --- | ---: |
${roleRows}

## Evidence Proof Classes

Proof classes are local path-derived buckets for claim hygiene. They distinguish behavior-level evidence from structural/static/governance evidence; they are not external validation.

| Proof Class | Count |
| --- | ---: |
${proofClassRows}

## Required Evidence Coverage

| Required Evidence | Present |
| --- | --- |
${requiredRows}

## Recursive Self Inputs Excluded

${report.recursiveSelfInputsExcluded.map((path) => `- \`${path}\``).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'product-evidence-manifest.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const evidenceRecords = buildEvidenceRecords()
  const { report, manifestText } = buildProductEvidenceManifestReport({ evidenceRecords })
  writeFileSync(resolve(root, manifestJsonlPath), manifestText)

  writeFileSync(resolve(docsDir, 'product-evidence-manifest.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!report.evidenceChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`manifest_jsonl_path=${manifestJsonlPath}`)
  console.log(`evidence_record_count=${evidenceRecords.length}`)
  console.log(`evidence_total_size_bytes=${report.evidenceTotalSizeBytes}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)
}

if (import.meta.main) {
  main()
}
