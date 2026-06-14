import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type MatrixRecord = {
  rank: number
  fullName: string
  sourceUrl: string
  axis: string
  sourceReviewStatus: string
  benchmarkabilityStatus: string
  openClaudeEvidencePresentCount: number
  protectedActionRequiredForNextStep: boolean
  protectedActionExecuted: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
}

type ReadinessIndexRecord = {
  indexKind: string
  indexKey: string
  readinessTier: string
  localEvidenceBackedCellCount: number
  axisNotYetAbsorbedCellCount: number
  metadataOnlyCellCount: number
}

type IdeReconciliationRecord = {
  schemaVersion: 'openclaude_oss_ide_or_editor_surface_evidence_v1'
  rank: number
  fullName: string
  sourceUrl: string
  axis: 'ide_or_editor_surface'
  sourceComparisonStatus: string
  sourceReviewStatus: string
  localOpenClaudeEvidenceStatus:
    | 'local_ide_surface_evidence_present_protected_host_gap_open'
    | 'source_project_ide_axis_not_absorbed_by_current_source_review'
  localEvidenceBindingCount: number
  realHostSmokeBoundaryStatus: 'blocked_by_vscode_cli_unavailable' | 'blocked_by_vscode_update_in_progress'
  workbenchSmokeStatus: 'local_real_workbench_smoke_passed_claim_blocked' | 'blocked_by_vscode_update_in_progress_claim_blocked'
  protectedActionRequiredForNextStep: true
  protectedActionExecuted: false
  extensionAvailabilityClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type IdeEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_ide_or_editor_surface_evidence'
  selectedAxis: 'ide_or_editor_surface'
  sourceReadinessIndexReportPath: string
  sourceReadinessIndexReportSha256: string
  sourceComparisonMatrixReportPath: string
  sourceComparisonMatrixReportSha256: string
  sourcePublicClaimBoundaryReportPath: string
  sourcePublicClaimBoundaryReportSha256: string
  sourceReportBindings: SourceBinding[]
  sourceIdePriorityTier: string
  sourceIdeLocalEvidenceBackedCellCount: number
  sourceIdeAxisNotYetAbsorbedCellCount: number
  sourceIdeMetadataOnlyCellCount: number
  sourceIdeMatrixRowCount: number
  localEvidenceBindings: SourceBinding[]
  localIdeEvidenceBindingCount: number
  hostSmokeReportPath: string
  hostSmokeReportSha256: string
  hostSmokeRealHostBlockedByVscodeCli: boolean
  hostSmokeEnvironmentBlockers: string[]
  workbenchSmokeReportPath: string
  workbenchSmokeReportSha256: string
  workbenchSmokePass: boolean
  workbenchSmokeRegisteredTreeViewCount: number
  workbenchSmokeExecutedCommandCount: number
  ideEvidenceJsonlPath: string
  ideEvidenceJsonlSha256: string
  ideEvidenceJsonlRecordCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  publishDeployLaunchPerformed: false
  protectedActionRequiredForNextVerifiableBoundary: true
  protectedActionExecuted: false
  extensionAvailabilityClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  mthResolutionStatus: 'unresolved'
  canonicalMemoryWriteAllowed: false
  allowedClaimLevel: 'internal_no_provider_product_quality_evidence_only'
  terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  reconciliationRecords: IdeReconciliationRecord[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const selectedAxis = 'ide_or_editor_surface' as const
const sourceReadinessIndexReportPath = 'docs/product-quality/oss-comparison-readiness-index-report.json'
const sourceComparisonMatrixReportPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.json'
const sourcePublicClaimBoundaryReportPath = 'docs/product-quality/public-claim-boundary-report.json'
const hostSmokeReportPath = 'docs/product-quality/ide-extension-host-smoke-report.json'
const workbenchSmokeReportPath = 'docs/product-quality/ide-extension-workbench-smoke-report.json'
const reportJsonPath = 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.md'
const ideEvidenceJsonlPath = 'reports/openclaude-oss-ide-or-editor-surface-evidence.jsonl'
const localEvidencePaths = [
  'docs/product-quality/ide-extension-surface-report.json',
  'docs/product-quality/ide-extension-scope-report.json',
  'docs/product-quality/ide-extension-manifest-smoke-report.json',
  'docs/product-quality/ide-extension-runtime-smoke-report.json',
  hostSmokeReportPath,
  workbenchSmokeReportPath,
  'docs/product-quality/vscode-update-boundary-report.json',
  'docs/product-quality/vscode-startup-diagnostics-report.json',
  'docs/product-quality/ide-extension-webview-render-smoke-report.json',
  'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json',
  'docs/product-quality/ide-extension-webview-interaction-smoke-report.json',
  'packages/openclaude-vscode/package.json',
  'packages/openclaude-vscode/dist/extension.js',
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

function binding(path: string): SourceBinding {
  const absolutePath = resolve(root, path)
  if (!existsSync(absolutePath)) {
    return { path, exists: false, sha256: null, sizeBytes: 0 }
  }
  const bytes = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(bytes), sizeBytes: statSync(absolutePath).size }
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function bool(report: Record<string, unknown>, key: string): boolean | undefined {
  return typeof report[key] === 'boolean' ? report[key] as boolean : undefined
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  return [
    'extensionAvailabilityClaimAllowed',
    'publicComparisonClaimAllowed',
    'superiorityClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
  ].every((key) => bool(report, key) !== true)
}

function callArraysEmpty(report: Record<string, unknown>): boolean {
  return Array.isArray(report.providerCallsPerformed) &&
    report.providerCallsPerformed.length === 0 &&
    Array.isArray(report.liveModelCallsPerformed) &&
    report.liveModelCallsPerformed.length === 0 &&
    Array.isArray(report.externalCallsPerformed) &&
    report.externalCallsPerformed.length === 0 &&
    Array.isArray(report.protectedActionsExecuted) &&
    report.protectedActionsExecuted.length === 0
}

function allChecksPass(report: Record<string, unknown>, key: string): boolean {
  const checks = report[key]
  return Array.isArray(checks) && checks.length > 0 && checks.every((item) => typeof item === 'object' && item !== null && (item as { ok?: unknown }).ok === true)
}

function hostSmokeBoundaryStatus(blockers: string[]): IdeReconciliationRecord['realHostSmokeBoundaryStatus'] {
  return blockers.includes('vscode_update_in_progress')
    ? 'blocked_by_vscode_update_in_progress'
    : 'blocked_by_vscode_cli_unavailable'
}

function writeMarkdown(report: IdeEvidenceReport): void {
  const sourceRows = report.sourceReportBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const evidenceRows = report.localEvidenceBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const reconciliationRows = report.reconciliationRecords
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | \`${record.sourceComparisonStatus}\` | \`${record.localOpenClaudeEvidenceStatus}\` | ${record.localEvidenceBindingCount} | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS IDE Or Editor Surface Evidence Report

Generated by: \`bun run product:oss-ide-or-editor-surface-evidence\`

## Claim Boundary

- This is internal local no-provider evidence for the \`${selectedAxis}\` axis.
- It binds existing VS Code extension surface, manifest, mock-host, real-host, workbench, webview, and startup-boundary evidence to the top-10 OSS comparison matrix.
- It does not install or repair VS Code, mutate PATH or install state, publish, deploy, launch, call providers, call live models, call external services, or make extension availability, public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.

## Summary

- selected_axis: \`${report.selectedAxis}\`
- source_ide_priority_tier: \`${report.sourceIdePriorityTier}\`
- source_ide_local_evidence_backed_cell_count: \`${report.sourceIdeLocalEvidenceBackedCellCount}\`
- source_ide_axis_not_yet_absorbed_cell_count: \`${report.sourceIdeAxisNotYetAbsorbedCellCount}\`
- source_ide_metadata_only_cell_count: \`${report.sourceIdeMetadataOnlyCellCount}\`
- source_ide_matrix_row_count: \`${report.sourceIdeMatrixRowCount}\`
- local_ide_evidence_binding_count: \`${report.localIdeEvidenceBindingCount}\`
- host_smoke_real_host_blocked_by_vscode_cli: \`${report.hostSmokeRealHostBlockedByVscodeCli}\`
- workbench_smoke_pass: \`${report.workbenchSmokePass}\`
- ide_evidence_jsonl_path: \`${report.ideEvidenceJsonlPath}\`
- ide_evidence_jsonl_sha256: \`${report.ideEvidenceJsonlSha256}\`
- terminal_condition: \`${report.terminalCondition}\`

## Source Report Bindings

| Source | Exists | SHA-256 | Size |
| --- | --- | --- | ---: |
${sourceRows}

## Local Evidence Bindings

| Evidence | Exists | SHA-256 | Size |
| --- | --- | --- | ---: |
${evidenceRows}

## Reconciliation Records

| Rank | Project | Source Comparison Status | Local OpenClaude Evidence | Evidence Bindings | Protected Action Executed |
| ---: | --- | --- | --- | ---: | --- |
${reconciliationRows}

## Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const readinessIndex = readJson<{
    mode: string
    readinessIndexRecords: ReadinessIndexRecord[]
    top10ProjectCount: number
    providerCallsPerformed: unknown[]
    liveModelCallsPerformed: unknown[]
    externalCallsPerformed: unknown[]
    protectedActionsExecuted: unknown[]
  } & Record<string, unknown>>(sourceReadinessIndexReportPath)
  const comparisonMatrix = readJson<{
    mode: string
    matrixRecords: MatrixRecord[]
    top10ProjectCount: number
    providerCallsPerformed: unknown[]
    liveModelCallsPerformed: unknown[]
    externalCallsPerformed: unknown[]
    protectedActionsExecuted: unknown[]
  } & Record<string, unknown>>(sourceComparisonMatrixReportPath)
  const publicClaimBoundary = readJson<Record<string, unknown>>(sourcePublicClaimBoundaryReportPath)
  const hostSmoke = readJson<Record<string, unknown>>(hostSmokeReportPath)
  const workbenchSmoke = readJson<Record<string, unknown>>(workbenchSmokeReportPath)
  const packageJson = readJson<{ scripts: Record<string, string> }>('package.json')
  const sourceReportBindings = [
    sourceReadinessIndexReportPath,
    sourceComparisonMatrixReportPath,
    sourcePublicClaimBoundaryReportPath,
  ].map(binding)
  const localEvidenceBindings = localEvidencePaths.map(binding)
  const ideIndexRecord = readinessIndex.readinessIndexRecords.find((record) =>
    record.indexKind === 'axis' && record.indexKey === selectedAxis,
  )
  const ideRows = comparisonMatrix.matrixRecords
    .filter((record) => record.axis === selectedAxis)
    .sort((left, right) => left.rank - right.rank)
  const hostBlockers = Array.isArray(hostSmoke.environmentBlockers)
    ? hostSmoke.environmentBlockers.filter((item): item is string => typeof item === 'string')
    : []
  const protectedHostBlockers = ['vscode_cli_unavailable', 'vscode_update_in_progress']
  const realHostSmokeBoundaryStatus = hostSmokeBoundaryStatus(hostBlockers)
  const workbenchBlockers = Array.isArray(workbenchSmoke.environmentBlockers)
    ? workbenchSmoke.environmentBlockers.filter((item): item is string => typeof item === 'string')
    : []
  const workbenchRegisteredViews = Array.isArray(workbenchSmoke.registeredTreeViewIds) ? workbenchSmoke.registeredTreeViewIds : []
  const workbenchExecutedCommands = Array.isArray(workbenchSmoke.executedViewCommandIds) ? workbenchSmoke.executedViewCommandIds : []
  const hostSmokeRealHostBlockedByVscodeCli = hostSmoke.hostRuntime === 'real_vscode_extension_development_host' &&
    hostSmoke.vscodeStartupBlocked === true &&
    hostBlockers.some((blocker) => protectedHostBlockers.includes(blocker)) &&
    hostSmoke.realExtensionHostLaunched === false &&
    hostSmoke.extensionAvailabilityClaimAllowed === false
  const workbenchSmokeRealEvidencePass = workbenchSmoke.hostRuntime === 'real_vscode_extension_development_host' &&
    workbenchSmoke.codeExitCode === 0 &&
    workbenchSmoke.vscodeStartupBlocked === false &&
    workbenchSmoke.realExtensionHostLaunched === true &&
    workbenchSmoke.extensionActivated === true &&
    workbenchSmoke.extensionAvailabilityClaimAllowed === false &&
    allChecksPass(workbenchSmoke, 'workbenchSmokeChecks')
  const workbenchSmokeProtectedBoundaryPass = workbenchSmoke.hostRuntime === 'real_vscode_extension_development_host' &&
    workbenchSmoke.codeExitCode === 0 &&
    workbenchSmoke.vscodeStartupBlocked === true &&
    workbenchBlockers.some((blocker) => protectedHostBlockers.includes(blocker)) &&
    workbenchSmoke.realExtensionHostLaunched === false &&
    workbenchSmoke.extensionAvailabilityClaimAllowed === false &&
    allChecksPass(workbenchSmoke, 'workbenchSmokeChecks')
  const workbenchSmokePass = workbenchSmokeRealEvidencePass || workbenchSmokeProtectedBoundaryPass
  const workbenchSmokeStatus = workbenchSmokeProtectedBoundaryPass
    ? 'blocked_by_vscode_update_in_progress_claim_blocked'
    : 'local_real_workbench_smoke_passed_claim_blocked'

  const reconciliationRecords: IdeReconciliationRecord[] = ideRows.map((record) => ({
    schemaVersion: 'openclaude_oss_ide_or_editor_surface_evidence_v1',
    rank: record.rank,
    fullName: record.fullName,
    sourceUrl: record.sourceUrl,
    axis: selectedAxis,
    sourceComparisonStatus: record.benchmarkabilityStatus,
    sourceReviewStatus: record.sourceReviewStatus,
    localOpenClaudeEvidenceStatus: record.openClaudeEvidencePresentCount > 0
      ? 'local_ide_surface_evidence_present_protected_host_gap_open'
      : 'source_project_ide_axis_not_absorbed_by_current_source_review',
    localEvidenceBindingCount: record.openClaudeEvidencePresentCount,
    realHostSmokeBoundaryStatus,
    workbenchSmokeStatus,
    protectedActionRequiredForNextStep: true,
    protectedActionExecuted: false,
    extensionAvailabilityClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }))
  const jsonlText = `${reconciliationRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, ideEvidenceJsonlPath), jsonlText)
  const ideEvidenceJsonlSha256 = sha256(jsonlText)

  const report: IdeEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_ide_or_editor_surface_evidence',
    selectedAxis,
    sourceReadinessIndexReportPath,
    sourceReadinessIndexReportSha256: sha256(readFileSync(resolve(root, sourceReadinessIndexReportPath))),
    sourceComparisonMatrixReportPath,
    sourceComparisonMatrixReportSha256: sha256(readFileSync(resolve(root, sourceComparisonMatrixReportPath))),
    sourcePublicClaimBoundaryReportPath,
    sourcePublicClaimBoundaryReportSha256: sha256(readFileSync(resolve(root, sourcePublicClaimBoundaryReportPath))),
    sourceReportBindings,
    sourceIdePriorityTier: ideIndexRecord?.readinessTier ?? 'missing',
    sourceIdeLocalEvidenceBackedCellCount: ideIndexRecord?.localEvidenceBackedCellCount ?? -1,
    sourceIdeAxisNotYetAbsorbedCellCount: ideIndexRecord?.axisNotYetAbsorbedCellCount ?? -1,
    sourceIdeMetadataOnlyCellCount: ideIndexRecord?.metadataOnlyCellCount ?? -1,
    sourceIdeMatrixRowCount: ideRows.length,
    localEvidenceBindings,
    localIdeEvidenceBindingCount: localEvidenceBindings.length,
    hostSmokeReportPath,
    hostSmokeReportSha256: sha256(readFileSync(resolve(root, hostSmokeReportPath))),
    hostSmokeRealHostBlockedByVscodeCli,
    hostSmokeEnvironmentBlockers: hostBlockers,
    workbenchSmokeReportPath,
    workbenchSmokeReportSha256: sha256(readFileSync(resolve(root, workbenchSmokeReportPath))),
    workbenchSmokePass,
    workbenchSmokeRegisteredTreeViewCount: workbenchRegisteredViews.length,
    workbenchSmokeExecutedCommandCount: workbenchExecutedCommands.length,
    ideEvidenceJsonlPath,
    ideEvidenceJsonlSha256,
    ideEvidenceJsonlRecordCount: reconciliationRecords.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    publishDeployLaunchPerformed: false,
    protectedActionRequiredForNextVerifiableBoundary: true,
    protectedActionExecuted: false,
    extensionAvailabilityClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    mthResolutionStatus: 'unresolved',
    canonicalMemoryWriteAllowed: false,
    allowedClaimLevel: 'internal_no_provider_product_quality_evidence_only',
    terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY',
    primarySourceInputs: [
      {
        sourceProject: 'Visual Studio Code Extension API',
        sourceUrl: 'https://code.visualstudio.com/api',
        observedPattern: 'Editor integration claims should be backed by extension manifest, activation, contribution, command, view, and UI-surface evidence.',
        localAbsorption: 'OpenClaude binds existing VS Code extension manifest, command, Tree View, WebviewView, and workbench smoke reports into one OSS comparison-axis evidence gate.',
      },
      {
        sourceProject: 'Visual Studio Code Testing Extensions',
        sourceUrl: 'https://code.visualstudio.com/api/working-with-extensions/testing-extension',
        observedPattern: 'Real Extension Development Host tests should use explicit development and test paths, and host availability should not be inferred from mock execution.',
        localAbsorption: 'OpenClaude records the real host smoke boundary and keeps VS Code CLI/PATH/install-state repair as a protected action.',
      },
      {
        sourceProject: 'Visual Studio Code Workspace Trust',
        sourceUrl: 'https://code.visualstudio.com/docs/editing/workspace-trust',
        observedPattern: 'IDE validation should isolate local workspace state and avoid silently trusting or mutating user environments.',
        localAbsorption: 'OpenClaude keeps the IDE axis as local no-provider evidence with no install, publish, deploy, launch, provider, live-model, external-service, or availability claim.',
      },
    ],
    selfImprovementActions: [
      'Convert the highest-priority OSS readiness axis into a deterministic local no-provider IDE/editor-surface evidence gate.',
      'Bind top-10 comparison rows to existing VS Code extension surface, manifest, mock-host, real-host, workbench, webview, screenshot, interaction, and startup-boundary evidence.',
      'Keep VS Code CLI/PATH/install-state repair, extension availability, public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked.',
    ],
    reconciliationRecords,
    evidenceChecks: [],
    claimBoundary: 'OSS IDE/editor surface evidence is internal local no-provider evidence only. It does not authorize VS Code install or repair, extension publication, extension availability claims, public comparison, superiority, release, production, external validation, provider-backed execution, live-model validation, or autonomous reliability claims.',
  }

  const sourceReports = [readinessIndex, comparisonMatrix, publicClaimBoundary]
  const jsonlLineCount = jsonlText.trim().split(/\r?\n/).length
  report.evidenceChecks = [
    check('source reports are present and hash-bound', sourceReportBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${sourceReportBindings.filter((source) => source.exists).length}/${sourceReportBindings.length}`),
    check('local IDE evidence files are present and hash-bound', localEvidenceBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${localEvidenceBindings.filter((source) => source.exists).length}/${localEvidenceBindings.length}`),
    check('source readiness index identifies the IDE/editor axis as the current safe internal priority', readinessIndex.mode === 'local_no_provider_oss_comparison_readiness_index' && ideIndexRecord?.readinessTier === 'safe_internal_absorption_priority', `${readinessIndex.mode}/${report.sourceIdePriorityTier}`),
    check('IDE/editor axis has ten source matrix rows', comparisonMatrix.mode === 'local_no_provider_oss_benchmark_comparison_matrix' && comparisonMatrix.top10ProjectCount === 10 && ideRows.length === 10, `${ideRows.length}/10`),
    check('source IDE readiness counts match matrix rows', report.sourceIdeLocalEvidenceBackedCellCount === ideRows.filter((record) => record.benchmarkabilityStatus === 'local_internal_evidence_present_protected_gap_open').length && report.sourceIdeAxisNotYetAbsorbedCellCount === ideRows.filter((record) => record.benchmarkabilityStatus === 'axis_not_yet_absorbed').length && report.sourceIdeMetadataOnlyCellCount === ideRows.filter((record) => record.benchmarkabilityStatus === 'metadata_only_needs_source_review').length, `${report.sourceIdeLocalEvidenceBackedCellCount}/${report.sourceIdeAxisNotYetAbsorbedCellCount}/${report.sourceIdeMetadataOnlyCellCount}`),
    check('host smoke keeps real VS Code startup boundary protected', hostSmokeRealHostBlockedByVscodeCli, hostBlockers.join(',') || 'none'),
    check('workbench smoke records local Tree View evidence or protected startup boundary with availability claims blocked', workbenchSmokePass && (workbenchSmokeProtectedBoundaryPass || (report.workbenchSmokeRegisteredTreeViewCount >= 2 && report.workbenchSmokeExecutedCommandCount >= 4)), workbenchSmokeProtectedBoundaryPass ? workbenchBlockers.join(',') : `${report.workbenchSmokeRegisteredTreeViewCount} views/${report.workbenchSmokeExecutedCommandCount} commands`),
    check('package exposes the IDE/editor OSS evidence command', packageJson.scripts['product:oss-ide-or-editor-surface-evidence'] === 'bun run scripts/product-oss-ide-or-editor-surface-evidence.ts', packageJson.scripts['product:oss-ide-or-editor-surface-evidence'] ?? 'missing'),
    check('IDE/editor evidence JSONL has one parseable row per top-10 project', jsonlLineCount === reconciliationRecords.length && report.ideEvidenceJsonlRecordCount === reconciliationRecords.length && report.ideEvidenceJsonlSha256.length === 64, `${jsonlLineCount}/${reconciliationRecords.length}`),
    check('reconciliation records preserve protected-action and claim boundaries', reconciliationRecords.every((record) => record.protectedActionRequiredForNextStep === true && record.protectedActionExecuted === false && record.extensionAvailabilityClaimAllowed === false && record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false), `${reconciliationRecords.length} records`),
    check('this IDE/editor gate performs no provider live external protected dependency or release actions', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0 && report.dependencyInstallPerformed === false && report.publishDeployLaunchPerformed === false, 'all action arrays empty and install/release flags false'),
    check('source reports preserve no-provider action boundaries', sourceReports.every(callArraysEmpty), 'provider/live/external/protected arrays empty'),
    check('public claim boundary has no unauthorized positive claims', publicClaimBoundary.unauthorizedPositiveClaimCount === 0, String(publicClaimBoundary.unauthorizedPositiveClaimCount ?? 'missing')),
    check('IDE/editor evidence keeps claim expansion blocked', [readinessIndex, comparisonMatrix, publicClaimBoundary, report].every(claimsBlocked), 'all claim flags false'),
    check('mth and canonical memory boundaries remain blocked', report.mthResolutionStatus === 'unresolved' && report.canonicalMemoryWriteAllowed === false, `${report.mthResolutionStatus}/${String(report.canonicalMemoryWriteAllowed)}`),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.evidenceChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`selected_axis=${report.selectedAxis}`)
  console.log(`source_ide_priority_tier=${report.sourceIdePriorityTier}`)
  console.log(`source_ide_local_evidence_backed_cell_count=${report.sourceIdeLocalEvidenceBackedCellCount}`)
  console.log(`source_ide_axis_not_yet_absorbed_cell_count=${report.sourceIdeAxisNotYetAbsorbedCellCount}`)
  console.log(`source_ide_metadata_only_cell_count=${report.sourceIdeMetadataOnlyCellCount}`)
  console.log(`ide_evidence_jsonl_record_count=${report.ideEvidenceJsonlRecordCount}`)
  console.log(`local_ide_evidence_binding_count=${report.localIdeEvidenceBindingCount}`)
  console.log(`host_smoke_real_host_blocked_by_vscode_cli=${report.hostSmokeRealHostBlockedByVscodeCli}`)
  console.log(`workbench_smoke_pass=${report.workbenchSmokePass}`)
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

main()
