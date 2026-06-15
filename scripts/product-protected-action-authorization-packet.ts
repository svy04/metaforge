import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = { label: string; ok: boolean; detail: string }

type SourceReportBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type ProtectedActionAuthorization = {
  id: string
  category:
    | 'local_environment'
    | 'source_control'
    | 'release_execution'
    | 'provenance'
    | 'legal_license'
    | 'provider_validation'
    | 'external_benchmark'
    | 'hosted_security'
    | 'claim_boundary'
  protectedActionRequired: true
  authorized: false
  executed: false
  sourceReports: string[]
  currentEvidence: string
  requiredOwnerDecision: string
  forbiddenShortcuts: string[]
  validationMethod: string
}

type ProtectedActionAuthorizationPacket = {
  generatedAt: string
  mode: 'local_no_provider_protected_action_authorization_packet'
  terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY'
  packetStatus: 'owner_authorization_required_before_protected_actions'
  sourceReportBindings: SourceReportBinding[]
  sourceReportCount: number
  authorizationItemCount: number
  allSafeBacklogEvidenceGatesCreated: boolean
  protectedActionExecutionAllowed: false
  protectedActionExecuted: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  commitPushPerformed: false
  publishDeployLaunchPerformed: false
  signedProvenanceGenerated: false
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
  requiredOwnerAuthorizations: ProtectedActionAuthorization[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/protected-action-authorization-packet.json'
const reportMdPath = 'docs/product-quality/protected-action-authorization-packet.md'
const reportJsonlPath = 'reports/openclaude-protected-action-authorization-packet.jsonl'

const sourceReportPaths = [
  'docs/product-quality/quality-blocker-taxonomy-report.json',
  'docs/product-quality/vscode-update-boundary-report.json',
  'docs/product-quality/vscode-startup-diagnostics-report.json',
  'docs/product-quality/git-release-hygiene-report.json',
  'docs/product-quality/external-benchmark-boundary-report.json',
  'docs/product-quality/benchmark-submission-readiness-report.json',
  'docs/product-quality/benchmark-policy-compliance-report.json',
  'docs/product-quality/terminal-bench-readiness-report.json',
  'docs/product-quality/oss-benchmark-comparison-matrix-report.json',
  'docs/product-quality/oss-comparison-readiness-index-report.json',
  'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json',
  'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json',
  'docs/product-quality/license-boundary-authorization-report.json',
  'docs/product-quality/oss-provider-breadth-evidence-report.json',
  'docs/product-quality/oss-release-hygiene-evidence-report.json',
  'docs/product-quality/verification-report-consistency-report.json',
  'docs/product-quality/public-claim-boundary-report.json',
  'docs/product-quality/github-hosted-trust-posture-report.json',
  'docs/product-quality/code-scanning-remediation-queue-report.json',
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function bindSource(path: string): SourceReportBinding {
  const absolutePath = resolve(root, path)
  if (!existsSync(absolutePath)) {
    return { path, exists: false, sha256: null, sizeBytes: 0 }
  }
  const content = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(content), sizeBytes: content.byteLength }
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function hasEmptyCallArrays(report: Record<string, unknown>): boolean {
  const providerCalls = report.providerCallsPerformed
  const liveCalls = report.liveModelCallsPerformed
  const externalCalls = report.externalCallsPerformed
  const protectedActions = report.protectedActionsExecuted
  const protectedActionsPerformed = report.protectedActionsPerformed
  return Array.isArray(providerCalls) && providerCalls.length === 0 &&
    Array.isArray(liveCalls) && liveCalls.length === 0 &&
    Array.isArray(externalCalls) && externalCalls.length === 0 &&
    (
      (Array.isArray(protectedActions) && protectedActions.length === 0) ||
      (Array.isArray(protectedActionsPerformed) && protectedActionsPerformed.length === 0)
    )
}

function hasNoProviderLiveOrProtectedActions(report: Record<string, unknown>): boolean {
  const providerCalls = report.providerCallsPerformed
  const liveCalls = report.liveModelCallsPerformed
  const protectedActions = report.protectedActionsExecuted
  const protectedActionsPerformed = report.protectedActionsPerformed
  return Array.isArray(providerCalls) && providerCalls.length === 0 &&
    Array.isArray(liveCalls) && liveCalls.length === 0 &&
    (
      (Array.isArray(protectedActions) && protectedActions.length === 0) ||
      (Array.isArray(protectedActionsPerformed) && protectedActionsPerformed.length === 0)
    )
}

function hasNoHostedSettingsMutation(report: Record<string, unknown>): boolean {
  const settingsMutations = report.settingsMutationsPerformed
  const protectedActions = report.protectedActionsExecuted
  return Array.isArray(settingsMutations) && settingsMutations.length === 0 &&
    Array.isArray(protectedActions) && protectedActions.length === 0
}

function bool(report: Record<string, unknown>, key: string): boolean | undefined {
  const value = report[key]
  return typeof value === 'boolean' ? value : undefined
}

function authorizationItems(): ProtectedActionAuthorization[] {
  return [
    {
      id: 'authorize_local_vscode_cli_path_or_install_state_repair',
      category: 'local_environment',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/quality-blocker-taxonomy-report.json',
        'docs/product-quality/vscode-update-boundary-report.json',
        'docs/product-quality/vscode-startup-diagnostics-report.json',
        'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json',
      ],
      currentEvidence: 'Product-quality gate remains blocked by a protected local VS Code boundary (vscode_cli_unavailable or vscode_update_in_progress), with real Extension Host evidence requiring explicit owner authorization before VS Code/PATH/install-state/update intervention.',
      requiredOwnerDecision: 'Authorize or deny local VS Code CLI/PATH/install-state/update intervention, then rerun the real host/workbench/replay gates if authorized.',
      forbiddenShortcuts: [
        'Do not install or repair VS Code without explicit owner authorization.',
        'Do not modify user PATH or VS Code install state without explicit owner authorization.',
        'Do not claim VS Code Extension Host availability from mock-host evidence.',
      ],
      validationMethod: 'After authorization and intervention, rerun product:ide-extension-host-smoke, product:ide-extension-workbench-smoke, product:vscode-update-boundary, product:agent-replay-evals, product:quality-blocker-taxonomy, and product:quality.',
    },
    {
      id: 'authorize_real_git_repository_commit_push_boundary',
      category: 'source_control',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: ['docs/product-quality/git-release-hygiene-report.json'],
      currentEvidence: 'Current workspace is classified for Git release hygiene, and this local product-quality gate did not attempt commit or push.',
      requiredOwnerDecision: 'Authorize an explicit source-control publish workflow before any commit, push, hosted CI, or source-controlled release claim.',
      forbiddenShortcuts: [
        'Do not claim commit or push completion from package metadata.',
        'Do not create or rewrite repository history as part of this local evidence gate.',
      ],
      validationMethod: 'Verify git rev-parse, git status, git remote, then run the source-controlled checks and hosted CI boundary gates when authorized.',
    },
    {
      id: 'authorize_publish_deploy_launch_or_release_execution',
      category: 'release_execution',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/oss-release-hygiene-evidence-report.json',
        'docs/product-quality/git-release-hygiene-report.json',
      ],
      currentEvidence: 'Release hygiene evidence is local and no-provider; publish, deploy, launch, release execution, and readiness claims remain blocked.',
      requiredOwnerDecision: 'Explicitly authorize any publish, deploy, launch, or release execution step only after protected blockers are reviewed.',
      forbiddenShortcuts: [
        'Do not treat artifact reproducibility as release execution.',
        'Do not publish, deploy, launch, or mark release ready from this packet.',
      ],
      validationMethod: 'Require a separate release execution gate with command transcript, artifact hashes, rollback plan, and owner authorization.',
    },
    {
      id: 'authorize_signed_provenance_or_external_attestation',
      category: 'provenance',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/oss-release-hygiene-evidence-report.json',
        'docs/product-quality/benchmark-submission-readiness-report.json',
      ],
      currentEvidence: 'Local artifact hashes and manifest evidence exist, but signed provenance and external attestation have not been generated.',
      requiredOwnerDecision: 'Authorize signing identity, signing workflow, and attestation publication boundary before any signed provenance claim.',
      forbiddenShortcuts: [
        'Do not call a local hash manifest a signed attestation.',
        'Do not publish provenance or use signing credentials inside this no-provider gate.',
      ],
      validationMethod: 'Run a separate signed-provenance gate after a real Git/release boundary and signing authorization exist.',
    },
    {
      id: 'authorize_license_notice_reuse_or_legal_decisions',
      category: 'legal_license',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: ['docs/product-quality/license-boundary-authorization-report.json'],
      currentEvidence: 'License inventories and source metadata gaps are classified, with owner/legal authorization required before legal review, NOTICE, REUSE, SPDX, source-file rewrites, or compliance claims.',
      requiredOwnerDecision: 'Authorize specific owner/legal decisions for license review, NOTICE generation, REUSE/SPDX artifacts, and source metadata updates.',
      forbiddenShortcuts: [
        'Do not infer legal approval from package metadata or a root LICENSE file.',
        'Do not create REUSE.toml, LICENSES artifacts, NOTICE files, or source SPDX rewrites without explicit owner/legal scope.',
      ],
      validationMethod: 'Complete a separate owner/legal gate, then rerun license-boundary, third-party license, source-license metadata, and evidence-manifest gates.',
    },
    {
      id: 'authorize_live_provider_or_model_validation',
      category: 'provider_validation',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/oss-provider-breadth-evidence-report.json',
        'docs/product-quality/external-benchmark-boundary-report.json',
      ],
      currentEvidence: 'Provider capability and fallback evidence is local fixture evidence only; no provider call, live model call, live provider validation, compatibility claim, or model-behavior claim has been authorized.',
      requiredOwnerDecision: 'Authorize specific providers, models, credentials, budgets, redaction boundaries, and validation commands before live-provider evidence is gathered.',
      forbiddenShortcuts: [
        'Do not convert local provider configuration rows into provider-backed execution evidence.',
        'Do not call providers, live models, or external services from this packet.',
      ],
      validationMethod: 'Run a separate live-provider validation gate with redacted credential handling, command transcripts, model identifiers, and failure-mode records.',
    },
    {
      id: 'authorize_external_benchmark_execution_or_submission',
      category: 'external_benchmark',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/external-benchmark-boundary-report.json',
        'docs/product-quality/oss-benchmark-comparison-matrix-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/benchmark-submission-readiness-report.json',
        'docs/product-quality/benchmark-policy-compliance-report.json',
        'docs/product-quality/terminal-bench-readiness-report.json',
      ],
      currentEvidence: 'External benchmark datasets, container runtimes, remote services, official submissions, leaderboards, policy eligibility, and Terminal-Bench/Harbor execution remain protected and unexecuted.',
      requiredOwnerDecision: 'Authorize the exact benchmark suite, runtime/container setup, remote services, provider/live model usage, submission assets, and public result boundary before execution.',
      forbiddenShortcuts: [
        'Do not call local benchmark readiness external validation.',
        'Do not submit to a benchmark or cite leaderboard results from local no-provider artifacts.',
      ],
      validationMethod: 'Run a separate external benchmark execution/submission gate with dataset provenance, runtime transcript, provider usage record, official assets, and claim review.',
    },
    {
      id: 'authorize_hosted_github_security_controls',
      category: 'hosted_security',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/github-hosted-trust-posture-report.json',
        'docs/product-quality/code-scanning-remediation-queue-report.json',
      ],
      currentEvidence: 'Hosted GitHub trust posture records branch protection, rulesets, secret scanning, push protection, Dependabot security updates, vulnerability alerts, code scanning backlog, main workflow status, and claim-safe CodeQL remediation queue status as read-only evidence.',
      requiredOwnerDecision: 'Authorize or deny hosted GitHub security setting changes, including branch protection or rulesets, secret scanning, push protection, Dependabot security updates, vulnerability alerts, and code scanning remediation workflow.',
      forbiddenShortcuts: [
        'Do not enable, disable, or mutate GitHub repository settings without explicit owner authorization.',
        'Do not claim hosted security posture, public readiness, or release readiness while hosted trust risks remain recorded.',
        'Do not treat local privacy scans as a substitute for hosted secret scanning or push protection.',
        'Do not claim CodeQL alerts are resolved from a remediation queue; require hosted CodeQL closure evidence.',
      ],
      validationMethod: 'After authorization and hosted setting changes or CodeQL fixes, rerun product:github-hosted-trust-posture, product:code-scanning-remediation-queue, product:github-remote-surface-audit, product:openssf-security-posture, product:public-claim-boundary, verify:privacy, and hosted GitHub Actions checks.',
    },
    {
      id: 'authorize_release_public_production_external_or_autonomous_claims',
      category: 'claim_boundary',
      protectedActionRequired: true,
      authorized: false,
      executed: false,
      sourceReports: [
        'docs/product-quality/verification-report-consistency-report.json',
        'docs/product-quality/quality-blocker-taxonomy-report.json',
        'docs/product-quality/external-benchmark-boundary-report.json',
        'docs/product-quality/oss-benchmark-comparison-matrix-report.json',
        'docs/product-quality/oss-comparison-readiness-index-report.json',
        'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json',
        'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json',
        'docs/product-quality/license-boundary-authorization-report.json',
        'docs/product-quality/public-claim-boundary-report.json',
      ],
      currentEvidence: 'Internal no-provider evidence is extensive and public surfaces scan clean for unauthorized positive claims, but release, public, production, external-validation, superiority, and autonomous-reliability claims remain explicitly blocked.',
      requiredOwnerDecision: 'Authorize any public comparison, superiority, release readiness, production readiness, public readiness, external validation, or autonomous reliability claim only after the relevant protected evidence gates pass.',
      forbiddenShortcuts: [
        'Do not claim top-10 superiority from local planning evidence.',
        'Do not claim release, production, public readiness, external validation, or autonomous reliability from this packet.',
      ],
      validationMethod: 'Require all applicable protected evidence gates, a refreshed claim review, and explicit owner claim authorization before any stronger public statement.',
    },
  ]
}

function writeMarkdown(report: ProtectedActionAuthorizationPacket): void {
  const sourceRows = report.sourceReportBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const authorizationRows = report.requiredOwnerAuthorizations
    .map((item) => `| \`${item.id}\` | \`${item.category}\` | \`${item.authorized}\` | \`${item.executed}\` | ${item.requiredOwnerDecision} |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Protected Action Authorization Packet

Generated by: \`bun run product:protected-action-authorization-packet\`

## Claim Boundary

- This packet is internal local no-provider evidence for the first real protected-action boundary.
- It does not execute protected actions, call providers, call live models, call external services, install dependencies, commit, push, publish, deploy, launch, generate signed provenance, or make release/public/production/external/autonomous claims.
- Every protected authorization defaults to \`false\` until a later explicit owner decision exists.

## Terminal Status

- terminal_condition: \`${report.terminalCondition}\`
- packet_status: \`${report.packetStatus}\`
- protected_action_execution_allowed: \`${report.protectedActionExecutionAllowed}\`
- protected_action_executed: \`${report.protectedActionExecuted}\`
- allowed_claim_level: \`${report.allowedClaimLevel}\`
- mth_resolution_status: \`${report.mthResolutionStatus}\`
- canonical_memory_write_allowed: \`${report.canonicalMemoryWriteAllowed}\`

## Source Report Bindings

| Source report | Exists | SHA-256 | Size |
| --- | --- | --- | ---: |
${sourceRows}

## Required Owner Authorizations

| Authorization | Category | Authorized | Executed | Required owner decision |
| --- | --- | --- | --- | --- |
${authorizationRows}

## Validation Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`
  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const sourceReportBindings = sourceReportPaths.map(bindSource)
  const qualityBlockerTaxonomy = readJson<Record<string, unknown>>('docs/product-quality/quality-blocker-taxonomy-report.json')
  const vscodeUpdateBoundary = readJson<Record<string, unknown>>('docs/product-quality/vscode-update-boundary-report.json')
  const vscodeStartupDiagnostics = readJson<Record<string, unknown>>('docs/product-quality/vscode-startup-diagnostics-report.json')
  const gitReleaseHygiene = readJson<Record<string, unknown>>('docs/product-quality/git-release-hygiene-report.json')
  const externalBenchmarkBoundary = readJson<Record<string, unknown>>('docs/product-quality/external-benchmark-boundary-report.json')
  const benchmarkSubmissionReadiness = readJson<Record<string, unknown>>('docs/product-quality/benchmark-submission-readiness-report.json')
  const benchmarkPolicyCompliance = readJson<Record<string, unknown>>('docs/product-quality/benchmark-policy-compliance-report.json')
  const terminalBenchReadiness = readJson<Record<string, unknown>>('docs/product-quality/terminal-bench-readiness-report.json')
  const ossBenchmarkComparisonMatrix = readJson<Record<string, unknown>>('docs/product-quality/oss-benchmark-comparison-matrix-report.json')
  const ossComparisonReadinessIndex = readJson<Record<string, unknown>>('docs/product-quality/oss-comparison-readiness-index-report.json')
  const ossIdeOrEditorSurfaceEvidence = readJson<Record<string, unknown>>('docs/product-quality/oss-ide-or-editor-surface-evidence-report.json')
  const ossPrivacyNoPhoneHomeEvidence = readJson<Record<string, unknown>>('docs/product-quality/oss-privacy-no-phone-home-evidence-report.json')
  const licenseBoundaryAuthorization = readJson<Record<string, unknown>>('docs/product-quality/license-boundary-authorization-report.json')
  const ossProviderBreadthEvidence = readJson<Record<string, unknown>>('docs/product-quality/oss-provider-breadth-evidence-report.json')
  const ossReleaseHygieneEvidence = readJson<Record<string, unknown>>('docs/product-quality/oss-release-hygiene-evidence-report.json')
  const verificationReportConsistency = readJson<Record<string, unknown>>('docs/product-quality/verification-report-consistency-report.json')
  const publicClaimBoundary = readJson<Record<string, unknown>>('docs/product-quality/public-claim-boundary-report.json')
  const githubHostedTrustPosture = readJson<Record<string, unknown>>('docs/product-quality/github-hosted-trust-posture-report.json')
  const codeScanningRemediationQueue = readJson<Record<string, unknown>>('docs/product-quality/code-scanning-remediation-queue-report.json')
  const requiredOwnerAuthorizations = authorizationItems()

  const allLocalSourceReportsNoProviderLiveExternalOrProtected = [
    qualityBlockerTaxonomy,
    vscodeUpdateBoundary,
    vscodeStartupDiagnostics,
    gitReleaseHygiene,
    externalBenchmarkBoundary,
    benchmarkSubmissionReadiness,
    benchmarkPolicyCompliance,
    terminalBenchReadiness,
    ossBenchmarkComparisonMatrix,
    ossComparisonReadinessIndex,
    ossIdeOrEditorSurfaceEvidence,
    ossPrivacyNoPhoneHomeEvidence,
    licenseBoundaryAuthorization,
    ossProviderBreadthEvidence,
    ossReleaseHygieneEvidence,
    verificationReportConsistency,
    publicClaimBoundary,
  ].every(hasEmptyCallArrays)
  const allSourceReportsNoProviderLiveOrProtectedActions = [
    qualityBlockerTaxonomy,
    vscodeUpdateBoundary,
    vscodeStartupDiagnostics,
    gitReleaseHygiene,
    externalBenchmarkBoundary,
    benchmarkSubmissionReadiness,
    benchmarkPolicyCompliance,
    terminalBenchReadiness,
    ossBenchmarkComparisonMatrix,
    ossComparisonReadinessIndex,
    ossIdeOrEditorSurfaceEvidence,
    ossPrivacyNoPhoneHomeEvidence,
    licenseBoundaryAuthorization,
    ossProviderBreadthEvidence,
    ossReleaseHygieneEvidence,
    verificationReportConsistency,
    publicClaimBoundary,
    githubHostedTrustPosture,
    codeScanningRemediationQueue,
  ].every(hasNoProviderLiveOrProtectedActions)
  const hostedTrustReadOnlyBoundaryHeld = hasNoHostedSettingsMutation(githubHostedTrustPosture) &&
    bool(githubHostedTrustPosture, 'publicSecurityPostureClaimAllowed') === false &&
    bool(githubHostedTrustPosture, 'releaseReadinessClaimAllowed') === false &&
    bool(githubHostedTrustPosture, 'productionReadinessClaimAllowed') === false &&
    bool(githubHostedTrustPosture, 'externalValidationClaimAllowed') === false
  const codeScanningQueueBoundaryHeld = hasNoHostedSettingsMutation(codeScanningRemediationQueue) &&
    bool(codeScanningRemediationQueue, 'publicSecurityPostureClaimAllowed') === false &&
    bool(codeScanningRemediationQueue, 'releaseReadinessClaimAllowed') === false &&
    bool(codeScanningRemediationQueue, 'productionReadinessClaimAllowed') === false &&
    bool(codeScanningRemediationQueue, 'externalValidationClaimAllowed') === false &&
    bool(codeScanningRemediationQueue, 'alertResolutionClaimAllowed') === false

  const claimFlags = [
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
  ]
  const claimFlagsBlocked = [
    qualityBlockerTaxonomy,
    vscodeUpdateBoundary,
    externalBenchmarkBoundary,
    benchmarkSubmissionReadiness,
    benchmarkPolicyCompliance,
    terminalBenchReadiness,
    ossBenchmarkComparisonMatrix,
    ossComparisonReadinessIndex,
    ossIdeOrEditorSurfaceEvidence,
    ossPrivacyNoPhoneHomeEvidence,
    licenseBoundaryAuthorization,
    ossProviderBreadthEvidence,
    ossReleaseHygieneEvidence,
    verificationReportConsistency,
    publicClaimBoundary,
  ].every((report) => claimFlags.every((flag) => bool(report, flag) === false || bool(report, flag) === undefined))

  const externalBenchmarkAuthorizationFalse = bool(externalBenchmarkBoundary, 'externalBenchmarkExecutionAuthorized') === false &&
    bool(externalBenchmarkBoundary, 'externalBenchmarkExecutionPerformed') === false
  const licenseAuthorizationsFalse = bool(licenseBoundaryAuthorization, 'allProtectedAuthorizationsDefaultFalse') === true &&
    bool(licenseBoundaryAuthorization, 'protectedAuthorizationRequestCreated') === true
  const protectedVscodeQualityStatuses = ['blocked_by_vscode_cli_unavailable', 'blocked_by_known_vscode_update_dependent_failures']
  const protectedVscodeBoundaryStatuses = ['blocked_missing_vscode_cli_or_explicit_owner_repair_action', 'blocked_wait_for_local_vscode_update_or_explicit_owner_process_action']
  const protectedVscodeDiagnosisStatuses = [
    'vscode_cli_unavailable_or_install_boundary',
    'vscode_core_update_guard_without_visible_sentinel_or_codesetup_process',
    'vscode_core_update_guard_with_visible_codesetup_process',
    'vscode_core_update_guard_with_visible_sentinel',
  ]
  const vscodeBoundaryHeld = protectedVscodeQualityStatuses.includes(String(qualityBlockerTaxonomy.currentProductQualityGateStatus)) &&
    typeof qualityBlockerTaxonomy.expectedProductQualityGateFailureCount === 'number' &&
    qualityBlockerTaxonomy.expectedProductQualityGateFailureCount > 0 &&
    protectedVscodeBoundaryStatuses.includes(String(vscodeUpdateBoundary.boundaryStatus)) &&
    protectedVscodeDiagnosisStatuses.includes(String(vscodeStartupDiagnostics.diagnosisStatus))
  const ideReconciliationRecords = Array.isArray(ossIdeOrEditorSurfaceEvidence.reconciliationRecords)
    ? ossIdeOrEditorSurfaceEvidence.reconciliationRecords.filter((record): record is Record<string, unknown> => record !== null && typeof record === 'object')
    : []
  const workbenchProtectedBoundary = bool(ossIdeOrEditorSurfaceEvidence, 'workbenchSmokePass') === true ||
    (
      ideReconciliationRecords.length > 0 &&
      ideReconciliationRecords.every((record) => ['blocked_by_vscode_cli_unavailable', 'blocked_by_vscode_update_in_progress'].includes(String(record.workbenchSmokeStatus)))
    )
  const ideSurfaceBoundaryHeld = bool(ossIdeOrEditorSurfaceEvidence, 'hostSmokeRealHostBlockedByVscodeCli') === true &&
    workbenchProtectedBoundary &&
    bool(ossIdeOrEditorSurfaceEvidence, 'extensionAvailabilityClaimAllowed') === false &&
    ossIdeOrEditorSurfaceEvidence.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY'
  const gitBoundaryHeld = ['blocked_by_no_git_repo', 'git_repo_detected'].includes(String(gitReleaseHygiene.workspaceGitStatus)) &&
    bool(gitReleaseHygiene, 'commitPushAttempted') === false &&
    bool(gitReleaseHygiene, 'releaseActionPerformed') === false
  const providerBoundaryHeld = bool(ossProviderBreadthEvidence, 'providerCallsAllowed') === false &&
    bool(ossProviderBreadthEvidence, 'liveModelCallsAllowed') === false &&
    bool(ossProviderBreadthEvidence, 'externalCallsAllowed') === false &&
    bool(ossProviderBreadthEvidence, 'liveProviderValidationAllowed') === false &&
    bool(ossProviderBreadthEvidence, 'providerCompatibilityClaimAllowed') === false
  const releaseBoundaryHeld = bool(ossReleaseHygieneEvidence, 'commitAllowed') === false &&
    bool(ossReleaseHygieneEvidence, 'pushAllowed') === false &&
    bool(ossReleaseHygieneEvidence, 'publishAllowed') === false &&
    bool(ossReleaseHygieneEvidence, 'deployAllowed') === false &&
    bool(ossReleaseHygieneEvidence, 'launchAllowed') === false &&
    bool(ossReleaseHygieneEvidence, 'signedProvenanceGenerated') === false &&
    bool(ossReleaseHygieneEvidence, 'signedProvenanceClaimAllowed') === false
  const benchmarkPolicySummary = benchmarkPolicyCompliance.summary as Record<string, unknown> | undefined
  const benchmarkSubmissionSummary = benchmarkSubmissionReadiness.summary as Record<string, unknown> | undefined
  const terminalBenchSummary = terminalBenchReadiness.summary as Record<string, unknown> | undefined
  const benchmarkClaimsBlocked = bool(benchmarkSubmissionSummary ?? {}, 'officialExternalSubmissionReady') === false &&
    bool(benchmarkPolicySummary ?? {}, 'officialSWEbenchVerifiedSubmissionClaimAllowed') === false &&
    bool(terminalBenchSummary ?? {}, 'officialTerminalBenchExecutionReady') === false
  const publicClaimBoundaryHeld = publicClaimBoundary.claimBoundaryStatus === 'no_unauthorized_public_claims_detected' &&
    publicClaimBoundary.unauthorizedPositiveClaimCount === 0 &&
    bool(publicClaimBoundary, 'releaseClaimAllowed') === false &&
    bool(publicClaimBoundary, 'superiorityClaimAllowed') === false

  const jsonlText = requiredOwnerAuthorizations.map((item) => JSON.stringify(item)).join('\n') + '\n'
  writeFileSync(resolve(root, reportJsonlPath), jsonlText)
  const jsonlLines = readText(reportJsonlPath).trim().split(/\r?\n/)
  const jsonlParseable = jsonlLines.every((line) => {
    try {
      JSON.parse(line)
      return true
    } catch {
      return false
    }
  })

  const evidenceChecks = [
    check('all source reports are present and hash-bound', sourceReportBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${sourceReportBindings.length}/${sourceReportPaths.length}`),
    check('local source reports performed no provider live external or protected calls', allLocalSourceReportsNoProviderLiveExternalOrProtected, 'local no-provider source reports keep call/action arrays empty'),
    check('all source reports performed no provider live or protected actions', allSourceReportsNoProviderLiveOrProtectedActions, 'hosted GitHub report may record read-only discovery only'),
    check('hosted GitHub trust posture remains read-only and claim-blocked', hostedTrustReadOnlyBoundaryHeld, String(githubHostedTrustPosture.status)),
    check('CodeQL remediation queue remains read-only and claim-blocked', codeScanningQueueBoundaryHeld, String(codeScanningRemediationQueue.status)),
    check('VS Code CLI/PATH/install-state boundary remains protected', vscodeBoundaryHeld, `${String(qualityBlockerTaxonomy.currentProductQualityGateStatus)}/${String(vscodeUpdateBoundary.boundaryStatus)}/${String(vscodeStartupDiagnostics.diagnosisStatus)}`),
    check('IDE/editor surface availability boundary remains protected', ideSurfaceBoundaryHeld, `${String(ossIdeOrEditorSurfaceEvidence.hostSmokeRealHostBlockedByVscodeCli)}/${String(ossIdeOrEditorSurfaceEvidence.workbenchSmokePass)}/${String(ossIdeOrEditorSurfaceEvidence.extensionAvailabilityClaimAllowed)}`),
    check('Git repository commit/push boundary remains protected', gitBoundaryHeld, String(gitReleaseHygiene.workspaceGitStatus)),
    check('provider and live model validation boundary remains protected', providerBoundaryHeld, 'provider/live/external validation flags false'),
    check('release execution boundary remains protected', releaseBoundaryHeld, 'commit/push/publish/deploy/launch/signed provenance flags false'),
    check('external benchmark and official submission boundaries remain protected', externalBenchmarkAuthorizationFalse && benchmarkClaimsBlocked, 'external execution and official claim flags false'),
    check('license and legal authorization defaults remain false', licenseAuthorizationsFalse, `${String(licenseBoundaryAuthorization.protectedAuthorizationRequestCount)} items`),
    check('public surface claim boundary remains protected', publicClaimBoundaryHeld, `${String(publicClaimBoundary.claimBoundaryStatus)}/${String(publicClaimBoundary.unauthorizedPositiveClaimCount)}`),
    check('readiness and external claim flags remain blocked', claimFlagsBlocked, 'release/production/public/external/autonomous flags false'),
    check('every protected authorization item defaults false and unexecuted', requiredOwnerAuthorizations.every((item) => item.authorized === false && item.executed === false), `${requiredOwnerAuthorizations.length} authorizations`),
    check('authorization JSONL is parseable and complete', jsonlParseable && jsonlLines.length === requiredOwnerAuthorizations.length, `${jsonlLines.length}/${requiredOwnerAuthorizations.length}`),
    check('verification report consistency preserves current terminal condition', ['PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_CLI_UNAVAILABLE', 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_UPDATE'].includes(String(verificationReportConsistency.sourceTerminalCondition)), String(verificationReportConsistency.sourceTerminalCondition)),
  ]

  const report: ProtectedActionAuthorizationPacket = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_protected_action_authorization_packet',
    terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY',
    packetStatus: 'owner_authorization_required_before_protected_actions',
    sourceReportBindings,
    sourceReportCount: sourceReportBindings.length,
    authorizationItemCount: requiredOwnerAuthorizations.length,
    allSafeBacklogEvidenceGatesCreated: true,
    protectedActionExecutionAllowed: false,
    protectedActionExecuted: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    commitPushPerformed: false,
    publishDeployLaunchPerformed: false,
    signedProvenanceGenerated: false,
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
    requiredOwnerAuthorizations,
    evidenceChecks,
    claimBoundary: 'Protected-action authorization packet only. It records the owner decisions required for the first real protected boundary and does not execute protected actions or make release, public, production, external-validation, superiority, provider-backed, live-model, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), JSON.stringify(report, null, 2) + '\n')
  writeMarkdown(report)

  for (const item of evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = evidenceChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`terminal_condition=${report.terminalCondition}`)
  console.log(`source_report_count=${report.sourceReportCount}`)
  console.log(`authorization_item_count=${report.authorizationItemCount}`)
  console.log(`protected_action_execution_allowed=${report.protectedActionExecutionAllowed}`)
  console.log(`protected_action_executed=${report.protectedActionExecuted}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
