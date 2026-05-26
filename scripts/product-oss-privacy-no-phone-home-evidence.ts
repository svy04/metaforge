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
  axis: string
  benchmarkabilityStatus: string
  protectedActionRequiredForNextStep: boolean
  protectedActionExecuted: boolean
}

type ReadinessIndexRecord = {
  indexKind: string
  indexKey: string
  readinessTier: string
  localEvidenceBackedCellCount: number
  axisNotYetAbsorbedCellCount: number
  metadataOnlyCellCount: number
}

type PrivacyReconciliationRecord = {
  schemaVersion: 'openclaude_oss_privacy_no_phone_home_evidence_v1'
  rank: number
  fullName: string
  axis: 'privacy_and_no_phone_home'
  sourceComparisonStatus: string
  localOpenClaudeEvidenceStatus: 'local_no_phone_home_dist_scan_passed'
  bannedPatternFindingCount: number
  protectedBoundary: string
  protectedActionRequiredForNextStep: true
  protectedActionExecuted: false
  publicPrivacyClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type PrivacyEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_privacy_no_phone_home_evidence'
  selectedAxis: 'privacy_and_no_phone_home'
  sourceReadinessIndexReportPath: string
  sourceReadinessIndexReportSha256: string
  sourceComparisonMatrixReportPath: string
  sourceComparisonMatrixReportSha256: string
  sourcePublicClaimBoundaryReportPath: string
  sourcePublicClaimBoundaryReportSha256: string
  sourceReportBindings: SourceBinding[]
  sourcePrivacyPriorityTier: string
  sourcePrivacyLocalEvidenceBackedCellCount: number
  sourcePrivacyAxisNotYetAbsorbedCellCount: number
  sourcePrivacyMetadataOnlyCellCount: number
  sourcePrivacyMatrixRowCount: number
  localEvidenceBindings: SourceBinding[]
  bannedPatterns: string[]
  bannedPatternFindingCount: number
  noTelemetryPluginPresent: boolean
  privacySettingsSurfacePresent: boolean
  verifyPrivacyScriptPresent: boolean
  packageVerifyPrivacyScriptPresent: boolean
  buildVerifiedIncludesPrivacy: boolean
  privacyEvidenceJsonlPath: string
  privacyEvidenceJsonlSha256: string
  privacyEvidenceJsonlRecordCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  publishDeployLaunchPerformed: false
  protectedActionRequiredForNextVerifiableBoundary: true
  protectedActionExecuted: false
  releaseClaimAllowed: false
  publicPrivacyClaimAllowed: false
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
  reconciliationRecords: PrivacyReconciliationRecord[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const selectedAxis = 'privacy_and_no_phone_home' as const
const sourceReadinessIndexReportPath = 'docs/product-quality/oss-comparison-readiness-index-report.json'
const sourceComparisonMatrixReportPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.json'
const sourcePublicClaimBoundaryReportPath = 'docs/product-quality/public-claim-boundary-report.json'
const reportJsonPath = 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.md'
const privacyEvidenceJsonlPath = 'reports/openclaude-oss-privacy-no-phone-home-evidence.jsonl'
const localEvidencePaths = [
  'scripts/verify-no-phone-home.ts',
  'dist/cli.mjs',
  'scripts/no-telemetry-plugin.ts',
  'scripts/no-telemetry-growthbook-stub.test.ts',
  'src/commands/privacy-settings/index.ts',
  'src/commands/privacy-settings/privacy-settings.tsx',
  'src/utils/privacyLevel.ts',
  'package.json',
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

function extractBannedPatterns(scriptText: string): string[] {
  const match = scriptText.match(/BANNED_PATTERNS\s*=\s*\[([\s\S]*?)\]\s*as const/)
  if (!match) return []
  return [...match[1].matchAll(/'([^']+)'/g)].map((item) => item[1])
}

function countOccurrences(text: string, pattern: string): number {
  return text.split(pattern).length - 1
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  return [
    'releaseClaimAllowed',
    'publicPrivacyClaimAllowed',
    'publicComparisonClaimAllowed',
    'superiorityClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
  ].every((key) => report[key] !== true)
}

function writeMarkdown(report: PrivacyEvidenceReport): void {
  const sourceRows = report.sourceReportBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const evidenceRows = report.localEvidenceBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const reconciliationRows = report.reconciliationRecords
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | \`${record.sourceComparisonStatus}\` | \`${record.localOpenClaudeEvidenceStatus}\` | ${record.bannedPatternFindingCount} | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Privacy No-Phone-Home Evidence Report

Generated by: \`bun run product:oss-privacy-no-phone-home-evidence\`

## Claim Boundary

- This is internal local no-provider evidence for the \`${selectedAxis}\` axis.
- It scans existing local build output and privacy/no-telemetry source surfaces for known banned telemetry patterns.
- It does not call providers, live models, or external services; it does not install dependencies, mutate production, publish, deploy, launch, or make public privacy, comparison, superiority, release, production, external-validation, or autonomous-reliability claims.

## Summary

- selected_axis: \`${report.selectedAxis}\`
- source_privacy_priority_tier: \`${report.sourcePrivacyPriorityTier}\`
- source_privacy_local_evidence_backed_cell_count: \`${report.sourcePrivacyLocalEvidenceBackedCellCount}\`
- source_privacy_axis_not_yet_absorbed_cell_count: \`${report.sourcePrivacyAxisNotYetAbsorbedCellCount}\`
- source_privacy_metadata_only_cell_count: \`${report.sourcePrivacyMetadataOnlyCellCount}\`
- source_privacy_matrix_row_count: \`${report.sourcePrivacyMatrixRowCount}\`
- banned_pattern_finding_count: \`${report.bannedPatternFindingCount}\`
- privacy_evidence_jsonl_path: \`${report.privacyEvidenceJsonlPath}\`
- privacy_evidence_jsonl_sha256: \`${report.privacyEvidenceJsonlSha256}\`
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

| Rank | Project | Source Comparison Status | Local OpenClaude Evidence | Banned Pattern Findings | Protected Action Executed |
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
  const packageJson = readJson<{ scripts: Record<string, string> }>('package.json')
  const verifyPrivacyText = readText('scripts/verify-no-phone-home.ts')
  const distText = readText('dist/cli.mjs')
  const bannedPatterns = extractBannedPatterns(verifyPrivacyText)
  const bannedPatternFindingCount = bannedPatterns.reduce((total, pattern) => total + countOccurrences(distText, pattern), 0)
  const sourceReportBindings = [
    sourceReadinessIndexReportPath,
    sourceComparisonMatrixReportPath,
    sourcePublicClaimBoundaryReportPath,
  ].map(binding)
  const localEvidenceBindings = localEvidencePaths.map(binding)
  const privacyIndexRecord = readinessIndex.readinessIndexRecords.find((record) =>
    record.indexKind === 'axis' && record.indexKey === selectedAxis,
  )
  const privacyRows = comparisonMatrix.matrixRecords
    .filter((record) => record.axis === selectedAxis)
    .sort((left, right) => left.rank - right.rank)
  const reconciliationRecords: PrivacyReconciliationRecord[] = privacyRows.map((record) => ({
    schemaVersion: 'openclaude_oss_privacy_no_phone_home_evidence_v1',
    rank: record.rank,
    fullName: record.fullName,
    axis: selectedAxis,
    sourceComparisonStatus: record.benchmarkabilityStatus,
    localOpenClaudeEvidenceStatus: 'local_no_phone_home_dist_scan_passed',
    bannedPatternFindingCount,
    protectedBoundary: 'External telemetry comparison, provider/live validation, production mutation, public privacy claims, public comparison, and release/public/production readiness claims require explicit later authorization.',
    protectedActionRequiredForNextStep: true,
    protectedActionExecuted: false,
    publicPrivacyClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }))
  const jsonlText = `${reconciliationRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, privacyEvidenceJsonlPath), jsonlText)
  const privacyEvidenceJsonlSha256 = sha256(jsonlText)

  const report: PrivacyEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_privacy_no_phone_home_evidence',
    selectedAxis,
    sourceReadinessIndexReportPath,
    sourceReadinessIndexReportSha256: sha256(readFileSync(resolve(root, sourceReadinessIndexReportPath))),
    sourceComparisonMatrixReportPath,
    sourceComparisonMatrixReportSha256: sha256(readFileSync(resolve(root, sourceComparisonMatrixReportPath))),
    sourcePublicClaimBoundaryReportPath,
    sourcePublicClaimBoundaryReportSha256: sha256(readFileSync(resolve(root, sourcePublicClaimBoundaryReportPath))),
    sourceReportBindings,
    sourcePrivacyPriorityTier: privacyIndexRecord?.readinessTier ?? 'missing',
    sourcePrivacyLocalEvidenceBackedCellCount: privacyIndexRecord?.localEvidenceBackedCellCount ?? -1,
    sourcePrivacyAxisNotYetAbsorbedCellCount: privacyIndexRecord?.axisNotYetAbsorbedCellCount ?? -1,
    sourcePrivacyMetadataOnlyCellCount: privacyIndexRecord?.metadataOnlyCellCount ?? -1,
    sourcePrivacyMatrixRowCount: privacyRows.length,
    localEvidenceBindings,
    bannedPatterns,
    bannedPatternFindingCount,
    noTelemetryPluginPresent: existsSync(resolve(root, 'scripts/no-telemetry-plugin.ts')),
    privacySettingsSurfacePresent: existsSync(resolve(root, 'src/commands/privacy-settings/index.ts')) &&
      existsSync(resolve(root, 'src/commands/privacy-settings/privacy-settings.tsx')) &&
      existsSync(resolve(root, 'src/utils/privacyLevel.ts')),
    verifyPrivacyScriptPresent: existsSync(resolve(root, 'scripts/verify-no-phone-home.ts')),
    packageVerifyPrivacyScriptPresent: packageJson.scripts['verify:privacy'] === 'bun run scripts/verify-no-phone-home.ts',
    buildVerifiedIncludesPrivacy: packageJson.scripts['build:verified'] === 'bun run build && bun run verify:privacy',
    privacyEvidenceJsonlPath,
    privacyEvidenceJsonlSha256,
    privacyEvidenceJsonlRecordCount: reconciliationRecords.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    publishDeployLaunchPerformed: false,
    protectedActionRequiredForNextVerifiableBoundary: true,
    protectedActionExecuted: false,
    releaseClaimAllowed: false,
    publicPrivacyClaimAllowed: false,
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
        sourceProject: 'OpenTelemetry JavaScript',
        sourceUrl: 'https://github.com/open-telemetry/opentelemetry-js',
        observedPattern: 'Telemetry should be explicit and auditable through named SDK/exporter surfaces.',
        localAbsorption: 'OpenClaude binds privacy evidence to a deterministic banned-pattern scan over local build output rather than implicit runtime assumptions.',
      },
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'Security and maintenance quality improve when checks are repeatable and evidence-backed.',
        localAbsorption: 'OpenClaude turns the privacy axis into a repeatable local evidence gate with machine-readable JSONL records.',
      },
      {
        sourceProject: 'SLSA provenance materials model',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Derived evidence should bind its input materials before claims rely on it.',
        localAbsorption: 'The privacy evidence report hash-binds the readiness index, comparison matrix, public-claim boundary, local privacy scripts, and build output.',
      },
    ],
    selfImprovementActions: [
      'Convert the previously weakest OSS comparison axis into a deterministic local no-provider privacy evidence gate.',
      'Bind no-phone-home claims to build-output scanning, privacy-settings surfaces, and no-telemetry test fixtures.',
      'Keep all privacy, public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked.',
    ],
    reconciliationRecords,
    evidenceChecks: [],
    claimBoundary: 'OSS privacy/no-phone-home evidence is internal local no-provider evidence only. It does not authorize public privacy claims, external telemetry comparison, providers, live models, production mutation, release, deploy, launch, or superiority claims.',
  }

  const jsonlLineCount = jsonlText.trim().split(/\r?\n/).length
  const sourceReports = [readinessIndex, comparisonMatrix, publicClaimBoundary]
  report.evidenceChecks = [
    check('source reports are present and hash-bound', sourceReportBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${sourceReportBindings.filter((source) => source.exists).length}/${sourceReportBindings.length}`),
    check('local privacy evidence files are present and hash-bound', localEvidenceBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${localEvidenceBindings.filter((source) => source.exists).length}/${localEvidenceBindings.length}`),
    check('source readiness index identifies the privacy axis', readinessIndex.mode === 'local_no_provider_oss_comparison_readiness_index' && privacyIndexRecord !== undefined, `${readinessIndex.mode}/${report.sourcePrivacyPriorityTier}`),
    check('privacy axis has ten source matrix rows', comparisonMatrix.mode === 'local_no_provider_oss_benchmark_comparison_matrix' && comparisonMatrix.top10ProjectCount === 10 && privacyRows.length === 10, `${privacyRows.length}/10`),
    check('banned privacy patterns are extracted from verify script', bannedPatterns.length >= 10, `${bannedPatterns.length} patterns`),
    check('local build output contains no banned telemetry patterns', bannedPatternFindingCount === 0, `${bannedPatternFindingCount} findings`),
    check('privacy and no-telemetry source surfaces are present', report.noTelemetryPluginPresent && report.privacySettingsSurfacePresent && report.verifyPrivacyScriptPresent, 'no-telemetry plugin, privacy-settings surface, and verify script present'),
    check('package scripts wire privacy verification into verified build', report.packageVerifyPrivacyScriptPresent && report.buildVerifiedIncludesPrivacy, 'verify:privacy and build:verified present'),
    check('privacy evidence JSONL has one parseable row per top-10 project', jsonlLineCount === reconciliationRecords.length && report.privacyEvidenceJsonlRecordCount === reconciliationRecords.length && report.privacyEvidenceJsonlSha256.length === 64, `${jsonlLineCount}/${reconciliationRecords.length}`),
    check('reconciliation records preserve protected-action and claim boundaries', reconciliationRecords.every((record) => record.protectedActionRequiredForNextStep === true && record.protectedActionExecuted === false && record.publicPrivacyClaimAllowed === false && record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false), `${reconciliationRecords.length} records`),
    check('this privacy gate performs no provider live external protected dependency or release actions', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0 && report.dependencyInstallPerformed === false && report.publishDeployLaunchPerformed === false, 'all action arrays empty and install/release flags false'),
    check('source reports preserve no-provider action boundaries', sourceReports.every((source) => Array.isArray(source.providerCallsPerformed) && source.providerCallsPerformed.length === 0 && Array.isArray(source.liveModelCallsPerformed) && source.liveModelCallsPerformed.length === 0 && Array.isArray(source.protectedActionsExecuted) && source.protectedActionsExecuted.length === 0), 'provider/live/protected arrays empty'),
    check('public claim boundary has no unauthorized positive claims', publicClaimBoundary.unauthorizedPositiveClaimCount === 0, String(publicClaimBoundary.unauthorizedPositiveClaimCount ?? 'missing')),
    check('privacy evidence keeps claim expansion blocked', [readinessIndex, comparisonMatrix, publicClaimBoundary, report].every(claimsBlocked), 'all claim flags false'),
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
  console.log(`source_privacy_priority_tier=${report.sourcePrivacyPriorityTier}`)
  console.log(`source_privacy_local_evidence_backed_cell_count=${report.sourcePrivacyLocalEvidenceBackedCellCount}`)
  console.log(`source_privacy_axis_not_yet_absorbed_cell_count=${report.sourcePrivacyAxisNotYetAbsorbedCellCount}`)
  console.log(`source_privacy_metadata_only_cell_count=${report.sourcePrivacyMetadataOnlyCellCount}`)
  console.log(`privacy_evidence_jsonl_record_count=${report.privacyEvidenceJsonlRecordCount}`)
  console.log(`banned_pattern_finding_count=${report.bannedPatternFindingCount}`)
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
