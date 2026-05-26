import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type BenchmarkabilityStatus =
  | 'local_internal_evidence_present_protected_gap_open'
  | 'metadata_only_needs_source_review'
  | 'axis_not_yet_absorbed'
  | 'local_evidence_reference_missing'

type MatrixRecord = {
  rank: number
  fullName: string
  axis: string
  benchmarkabilityStatus: BenchmarkabilityStatus
  protectedActionRequiredForNextStep: boolean
  protectedActionExecuted: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type ComparisonMatrixReport = {
  mode: string
  baselineSnapshotDate: string
  top10ProjectCount: number
  requiredProductAxisCount: number
  matrixRecordCount: number
  recordsWithLocalEvidenceCount: number
  recordsNeedingProtectedActionCount: number
  metadataOnlyRecordCount: number
  axisNotYetAbsorbedRecordCount: number
  matrixRecords: MatrixRecord[]
  matrixChecks: Check[]
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type SourceBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type IndexKind = 'axis' | 'project'

type ReadinessIndexRecord = {
  schemaVersion: 'openclaude_oss_comparison_readiness_index_v1'
  indexKind: IndexKind
  indexKey: string
  baselineSnapshotDate: string
  rank: number | null
  fullName: string | null
  axis: string | null
  totalMatrixCellCount: number
  localEvidenceBackedCellCount: number
  axisNotYetAbsorbedCellCount: number
  metadataOnlyCellCount: number
  localEvidenceReferenceMissingCellCount: number
  protectedActionRequiredCellCount: number
  priorityScore: number
  readinessTier:
    | 'local_evidence_reference_repair_first'
    | 'source_review_priority'
    | 'safe_internal_absorption_priority'
    | 'protected_action_boundary_after_local_evidence'
  nextSafeInternalAction: string
  protectedBoundary: string
  protectedActionExecuted: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type ComparisonReadinessIndexReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_comparison_readiness_index'
  sourceComparisonMatrixReportPath: string
  sourceComparisonMatrixReportSha256: string
  sourceProtectedActionAuthorizationPacketPath: string
  sourceProtectedActionAuthorizationPacketSha256: string
  sourceProductEvidenceManifestPath: string
  sourceProductEvidenceManifestSha256: string
  sourcePublicClaimBoundaryReportPath: string
  sourcePublicClaimBoundaryReportSha256: string
  sourceReportBindings: SourceBinding[]
  baselineSnapshotDate: string
  matrixRecordCount: number
  top10ProjectCount: number
  requiredProductAxisCount: number
  statusCounts: Record<BenchmarkabilityStatus, number>
  indexRecordCount: number
  axisIndexRecordCount: number
  projectIndexRecordCount: number
  highestPrioritySafeInternalAxis: string
  highestPrioritySafeInternalProject: string
  readinessIndexJsonlPath: string
  readinessIndexJsonlSha256: string
  readinessIndexJsonlRecordCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  publishDeployLaunchPerformed: false
  protectedActionRequiredForNextVerifiableBoundary: true
  protectedActionExecuted: false
  releaseClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  mthResolutionStatus: 'unresolved'
  canonicalMemoryWriteAllowed: false
  allowedClaimLevel: string
  terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  readinessIndexRecords: ReadinessIndexRecord[]
  topPriorityRecords: ReadinessIndexRecord[]
  indexChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceComparisonMatrixReportPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.json'
const sourceProtectedActionAuthorizationPacketPath = 'docs/product-quality/protected-action-authorization-packet.json'
const sourceProductEvidenceManifestPath = 'docs/product-quality/product-evidence-manifest.json'
const sourcePublicClaimBoundaryReportPath = 'docs/product-quality/public-claim-boundary-report.json'
const reportJsonPath = 'docs/product-quality/oss-comparison-readiness-index-report.json'
const reportMdPath = 'docs/product-quality/oss-comparison-readiness-index-report.md'
const readinessIndexJsonlPath = 'reports/openclaude-oss-comparison-readiness-index.jsonl'

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
  const content = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(content), sizeBytes: statSync(absolutePath).size }
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function statusCounts(records: MatrixRecord[]): Record<BenchmarkabilityStatus, number> {
  return {
    local_internal_evidence_present_protected_gap_open: records.filter((record) => record.benchmarkabilityStatus === 'local_internal_evidence_present_protected_gap_open').length,
    metadata_only_needs_source_review: records.filter((record) => record.benchmarkabilityStatus === 'metadata_only_needs_source_review').length,
    axis_not_yet_absorbed: records.filter((record) => record.benchmarkabilityStatus === 'axis_not_yet_absorbed').length,
    local_evidence_reference_missing: records.filter((record) => record.benchmarkabilityStatus === 'local_evidence_reference_missing').length,
  }
}

function readinessTier(counts: Record<BenchmarkabilityStatus, number>): ReadinessIndexRecord['readinessTier'] {
  if (counts.local_evidence_reference_missing > 0) {
    return 'local_evidence_reference_repair_first'
  }
  if (counts.metadata_only_needs_source_review > 0) {
    return 'source_review_priority'
  }
  if (counts.axis_not_yet_absorbed > 0) {
    return 'safe_internal_absorption_priority'
  }
  return 'protected_action_boundary_after_local_evidence'
}

function nextSafeAction(tier: ReadinessIndexRecord['readinessTier'], kind: IndexKind): string {
  if (tier === 'local_evidence_reference_repair_first') {
    return `repair_missing_local_${kind}_evidence_bindings_before_any_claim_expansion`
  }
  if (tier === 'source_review_priority') {
    return `perform_bounded_local_${kind}_source_review_reconciliation_from_existing_artifacts`
  }
  if (tier === 'safe_internal_absorption_priority') {
    return `create_or_extend_internal_no_provider_${kind}_evidence_gate_without_protected_actions`
  }
  return `defer_to_protected_action_authorization_packet_after_internal_${kind}_evidence_review`
}

function priorityScore(counts: Record<BenchmarkabilityStatus, number>, total: number): number {
  const localEvidence = counts.local_internal_evidence_present_protected_gap_open
  return counts.local_evidence_reference_missing * 100 +
    counts.metadata_only_needs_source_review * 50 +
    counts.axis_not_yet_absorbed * 25 +
    (total - localEvidence) * 10 +
    total
}

function makeIndexRecord(kind: IndexKind, key: string, records: MatrixRecord[]): ReadinessIndexRecord {
  const counts = statusCounts(records)
  const tier = readinessTier(counts)
  const first = records[0]
  return {
    schemaVersion: 'openclaude_oss_comparison_readiness_index_v1',
    indexKind: kind,
    indexKey: key,
    baselineSnapshotDate: first?.rank ? '' : '',
    rank: kind === 'project' ? first.rank : null,
    fullName: kind === 'project' ? first.fullName : null,
    axis: kind === 'axis' ? first.axis : null,
    totalMatrixCellCount: records.length,
    localEvidenceBackedCellCount: counts.local_internal_evidence_present_protected_gap_open,
    axisNotYetAbsorbedCellCount: counts.axis_not_yet_absorbed,
    metadataOnlyCellCount: counts.metadata_only_needs_source_review,
    localEvidenceReferenceMissingCellCount: counts.local_evidence_reference_missing,
    protectedActionRequiredCellCount: records.filter((record) => record.protectedActionRequiredForNextStep).length,
    priorityScore: priorityScore(counts, records.length),
    readinessTier: tier,
    nextSafeInternalAction: nextSafeAction(tier, kind),
    protectedBoundary: 'This index only prioritizes internal no-provider evidence work. External benchmark execution, provider/live validation, production mutation, publish/deploy/launch, and public/superiority/readiness claims require explicit later authorization.',
    protectedActionExecuted: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function withBaselineDate(record: ReadinessIndexRecord, baselineSnapshotDate: string): ReadinessIndexRecord {
  return { ...record, baselineSnapshotDate }
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  return [
    'releaseClaimAllowed',
    'publicComparisonClaimAllowed',
    'superiorityClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
  ].every((key) => report[key] !== true)
}

function callArraysEmpty(report: Record<string, unknown>): boolean {
  return ['providerCallsPerformed', 'liveModelCallsPerformed', 'externalCallsPerformed', 'protectedActionsExecuted']
    .every((key) => Array.isArray(report[key]) && (report[key] as unknown[]).length === 0)
}

function writeMarkdown(report: ComparisonReadinessIndexReport): void {
  const statusRows = Object.entries(report.statusCounts)
    .map(([status, count]) => `| \`${status}\` | ${count} |`)
    .join('\n')
  const sourceRows = report.sourceReportBindings
    .map((source) => `| \`${source.path}\` | \`${source.exists}\` | \`${source.sha256 ?? 'missing'}\` | ${source.sizeBytes} |`)
    .join('\n')
  const priorityRows = report.topPriorityRecords
    .map((record) => `| ${record.priorityScore} | \`${record.indexKind}\` | \`${record.indexKey}\` | \`${record.readinessTier}\` | ${record.localEvidenceBackedCellCount}/${record.totalMatrixCellCount} | ${record.axisNotYetAbsorbedCellCount} | ${record.metadataOnlyCellCount} | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.indexChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Comparison Readiness Index Report

Generated by: \`bun run product:oss-comparison-readiness-index\`

## Claim Boundary

- This is an internal no-provider readiness index over the existing top-10-by-axis comparison matrix.
- It ranks safe internal evidence work and protected-action boundaries; it does not execute external benchmarks, providers, live models, production changes, dependency installs, publish/deploy/launch, or public comparison claims.
- It does not claim OpenClaude beats any project. It records where internal evidence is strongest, where gaps remain, and where explicit authorization is required.

## Summary

- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- matrix_record_count: \`${report.matrixRecordCount}\`
- top10_project_count: \`${report.top10ProjectCount}\`
- required_product_axis_count: \`${report.requiredProductAxisCount}\`
- index_record_count: \`${report.indexRecordCount}\`
- axis_index_record_count: \`${report.axisIndexRecordCount}\`
- project_index_record_count: \`${report.projectIndexRecordCount}\`
- highest_priority_safe_internal_axis: \`${report.highestPrioritySafeInternalAxis}\`
- highest_priority_safe_internal_project: \`${report.highestPrioritySafeInternalProject}\`
- readiness_index_jsonl_path: \`${report.readinessIndexJsonlPath}\`
- readiness_index_jsonl_sha256: \`${report.readinessIndexJsonlSha256}\`
- terminal_condition: \`${report.terminalCondition}\`

## Status Counts

| Status | Count |
| --- | ---: |
${statusRows}

## Source Bindings

| Source | Exists | SHA-256 | Size |
| --- | --- | --- | ---: |
${sourceRows}

## Priority Preview

| Score | Kind | Key | Tier | Local Evidence | Not Yet Absorbed | Metadata Only | Protected Action Executed |
| ---: | --- | --- | --- | ---: | ---: | ---: | --- |
${priorityRows}

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

  const matrix = readJson<ComparisonMatrixReport>(sourceComparisonMatrixReportPath)
  const protectedPacket = readJson<Record<string, unknown>>(sourceProtectedActionAuthorizationPacketPath)
  const evidenceManifest = readJson<Record<string, unknown>>(sourceProductEvidenceManifestPath)
  const publicClaimBoundary = readJson<Record<string, unknown>>(sourcePublicClaimBoundaryReportPath)
  const sourceReportBindings = [
    sourceComparisonMatrixReportPath,
    sourceProtectedActionAuthorizationPacketPath,
    sourceProductEvidenceManifestPath,
    sourcePublicClaimBoundaryReportPath,
  ].map(binding)
  const counts = statusCounts(matrix.matrixRecords)
  const axes = [...new Set(matrix.matrixRecords.map((record) => record.axis))].sort()
  const projects = [...new Map(matrix.matrixRecords.map((record) => [record.fullName, { rank: record.rank, fullName: record.fullName }])).values()]
    .sort((a, b) => a.rank - b.rank)
  const axisIndexRecords = axes
    .map((axis) => withBaselineDate(makeIndexRecord('axis', axis, matrix.matrixRecords.filter((record) => record.axis === axis)), matrix.baselineSnapshotDate))
    .sort((a, b) => b.priorityScore - a.priorityScore || a.indexKey.localeCompare(b.indexKey))
  const projectIndexRecords = projects
    .map((project) => withBaselineDate(makeIndexRecord('project', project.fullName, matrix.matrixRecords.filter((record) => record.fullName === project.fullName)), matrix.baselineSnapshotDate))
    .sort((a, b) => b.priorityScore - a.priorityScore || (a.rank ?? 0) - (b.rank ?? 0))
  const readinessIndexRecords = [...axisIndexRecords, ...projectIndexRecords]
  const readinessIndexJsonlText = readinessIndexRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, readinessIndexJsonlPath), readinessIndexJsonlText)
  const readinessIndexJsonlSha256 = sha256(readinessIndexJsonlText)
  const requiredAuthorizations = protectedPacket.requiredOwnerAuthorizations
  const allAuthorizationsFalse = Array.isArray(requiredAuthorizations) &&
    requiredAuthorizations.every((item) => item && typeof item === 'object' && (item as { authorized?: unknown; executed?: unknown }).authorized === false && (item as { executed?: unknown }).executed === false)
  const manifestRequiredPaths = Array.isArray(evidenceManifest.requiredEvidencePaths) ? evidenceManifest.requiredEvidencePaths as string[] : []
  const manifestMissingPaths = Array.isArray(evidenceManifest.missingRequiredEvidencePaths) ? evidenceManifest.missingRequiredEvidencePaths as string[] : []

  const report: ComparisonReadinessIndexReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_comparison_readiness_index',
    sourceComparisonMatrixReportPath,
    sourceComparisonMatrixReportSha256: sha256(readFileSync(resolve(root, sourceComparisonMatrixReportPath))),
    sourceProtectedActionAuthorizationPacketPath,
    sourceProtectedActionAuthorizationPacketSha256: sha256(readFileSync(resolve(root, sourceProtectedActionAuthorizationPacketPath))),
    sourceProductEvidenceManifestPath,
    sourceProductEvidenceManifestSha256: sha256(readFileSync(resolve(root, sourceProductEvidenceManifestPath))),
    sourcePublicClaimBoundaryReportPath,
    sourcePublicClaimBoundaryReportSha256: sha256(readFileSync(resolve(root, sourcePublicClaimBoundaryReportPath))),
    sourceReportBindings,
    baselineSnapshotDate: matrix.baselineSnapshotDate,
    matrixRecordCount: matrix.matrixRecordCount,
    top10ProjectCount: matrix.top10ProjectCount,
    requiredProductAxisCount: matrix.requiredProductAxisCount,
    statusCounts: counts,
    indexRecordCount: readinessIndexRecords.length,
    axisIndexRecordCount: axisIndexRecords.length,
    projectIndexRecordCount: projectIndexRecords.length,
    highestPrioritySafeInternalAxis: axisIndexRecords[0]?.indexKey ?? 'none',
    highestPrioritySafeInternalProject: projectIndexRecords[0]?.indexKey ?? 'none',
    readinessIndexJsonlPath,
    readinessIndexJsonlSha256,
    readinessIndexJsonlRecordCount: readinessIndexRecords.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    publishDeployLaunchPerformed: false,
    protectedActionRequiredForNextVerifiableBoundary: true,
    protectedActionExecuted: false,
    releaseClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    mthResolutionStatus: 'unresolved',
    canonicalMemoryWriteAllowed: false,
    allowedClaimLevel: typeof protectedPacket.allowedClaimLevel === 'string'
      ? protectedPacket.allowedClaimLevel
      : 'internal_no_provider_product_quality_evidence_only',
    terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY',
    primarySourceInputs: [
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'Reusable quality programs benefit from explicit checks with transparent remediation targets.',
        localAbsorption: 'OpenClaude turns the comparison matrix into ranked remediation priorities while keeping claim boundaries false.',
      },
      {
        sourceProject: 'SLSA provenance materials model',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Derived evidence should bind source materials before consumers rely on it.',
        localAbsorption: 'The readiness index is hash-bound to the comparison matrix, protected-action packet, evidence manifest, and public-claim boundary report.',
      },
      {
        sourceProject: 'in-toto Attestation Framework',
        sourceUrl: 'https://github.com/in-toto/attestation',
        observedPattern: 'Machine-checkable statements make evidence packages stronger than narrative-only assertions.',
        localAbsorption: 'The readiness index emits JSON, Markdown, and JSONL records that can be checked by the product quality gate.',
      },
    ],
    selfImprovementActions: [
      'Add a deterministic readiness index over the 100-row OSS benchmark comparison matrix.',
      'Rank remaining internal evidence work by axis and project without executing protected actions.',
      'Keep top-10 comparison, superiority, release, production, public, external-validation, and autonomous-reliability claims blocked.',
    ],
    readinessIndexRecords,
    topPriorityRecords: readinessIndexRecords.slice().sort((a, b) => b.priorityScore - a.priorityScore || a.indexKind.localeCompare(b.indexKind) || a.indexKey.localeCompare(b.indexKey)).slice(0, 10),
    indexChecks: [],
    claimBoundary: 'This readiness index is internal no-provider prioritization evidence only. It does not authorize or perform external benchmark execution, provider/live validation, production mutation, release/public claims, or superiority claims.',
  }

  const statusTotal = Object.values(report.statusCounts).reduce((total, count) => total + count, 0)
  const jsonlLineCount = readinessIndexJsonlText.trim().split(/\r?\n/).length
  report.indexChecks = [
    check('source reports are present and hash-bound', sourceReportBindings.every((source) => source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0), `${sourceReportBindings.filter((source) => source.exists).length}/${sourceReportBindings.length}`),
    check('comparison matrix is local no-provider source', matrix.mode === 'local_no_provider_oss_benchmark_comparison_matrix' && Array.isArray(matrix.matrixRecords), String(matrix.mode)),
    check('comparison matrix still covers top-10 by required axes', matrix.matrixRecordCount === matrix.top10ProjectCount * matrix.requiredProductAxisCount && matrix.matrixRecordCount === matrix.matrixRecords.length && matrix.top10ProjectCount === 10 && matrix.requiredProductAxisCount === 10, `${matrix.matrixRecordCount}/${matrix.top10ProjectCount * matrix.requiredProductAxisCount}`),
    check('status counts total the matrix records', statusTotal === matrix.matrixRecordCount && counts.local_internal_evidence_present_protected_gap_open === matrix.recordsWithLocalEvidenceCount && counts.metadata_only_needs_source_review === matrix.metadataOnlyRecordCount && counts.axis_not_yet_absorbed === matrix.axisNotYetAbsorbedRecordCount, `${statusTotal}/${matrix.matrixRecordCount}`),
    check('readiness index has one axis and one project record per source dimension', report.axisIndexRecordCount === matrix.requiredProductAxisCount && report.projectIndexRecordCount === matrix.top10ProjectCount && report.indexRecordCount === matrix.requiredProductAxisCount + matrix.top10ProjectCount, `${report.indexRecordCount}/${matrix.requiredProductAxisCount + matrix.top10ProjectCount}`),
    check('readiness JSONL has one parseable row per index record', jsonlLineCount === report.indexRecordCount && report.readinessIndexJsonlRecordCount === report.indexRecordCount && typeof report.readinessIndexJsonlSha256 === 'string' && report.readinessIndexJsonlSha256.length === 64, `${jsonlLineCount}/${report.indexRecordCount}`),
    check('index records preserve protected-action and claim boundaries', readinessIndexRecords.every((record) => record.protectedActionExecuted === false && record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false), `${readinessIndexRecords.length} records`),
    check('this index gate performs no provider live external protected dependency or release actions', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0 && report.dependencyInstallPerformed === false && report.publishDeployLaunchPerformed === false, 'all action arrays empty and install/release flags false'),
    check('source reports preserve no-provider call arrays', [matrix, protectedPacket, evidenceManifest, publicClaimBoundary].every(callArraysEmpty), 'source call arrays empty'),
    check('source reports keep public comparison superiority and readiness claims blocked', [matrix, protectedPacket, evidenceManifest, publicClaimBoundary, report].every(claimsBlocked), 'all claim flags false'),
    check('protected-action packet keeps all owner authorizations false', Number(protectedPacket.sourceReportCount) >= 14 && allAuthorizationsFalse && protectedPacket.protectedActionExecuted === false, `${String(protectedPacket.sourceReportCount)}/${String(Array.isArray(requiredAuthorizations) ? requiredAuthorizations.length : 0)}`),
    check('evidence manifest includes comparison matrix evidence and has no missing required paths', manifestRequiredPaths.includes(sourceComparisonMatrixReportPath) && manifestRequiredPaths.includes('reports/openclaude-oss-benchmark-comparison-matrix.jsonl') && manifestMissingPaths.length === 0, `${manifestRequiredPaths.length} required paths`),
    check('public claim boundary has no unauthorized positive claims', publicClaimBoundary.unauthorizedPositiveClaimCount === 0, String(publicClaimBoundary.unauthorizedPositiveClaimCount ?? 'missing')),
    check('terminal protected-action boundary remains explicit', report.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY' && report.protectedActionRequiredForNextVerifiableBoundary === true && report.protectedActionExecuted === false, report.terminalCondition),
    check('mth and canonical memory boundaries remain blocked', report.mthResolutionStatus === 'unresolved' && report.canonicalMemoryWriteAllowed === false, `${report.mthResolutionStatus}/${String(report.canonicalMemoryWriteAllowed)}`),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.indexChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.indexChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`matrix_record_count=${report.matrixRecordCount}`)
  console.log(`index_record_count=${report.indexRecordCount}`)
  console.log(`axis_index_record_count=${report.axisIndexRecordCount}`)
  console.log(`project_index_record_count=${report.projectIndexRecordCount}`)
  console.log(`highest_priority_safe_internal_axis=${report.highestPrioritySafeInternalAxis}`)
  console.log(`highest_priority_safe_internal_project=${report.highestPrioritySafeInternalProject}`)
  console.log(`protected_action_required_for_next_verifiable_boundary=${report.protectedActionRequiredForNextVerifiableBoundary}`)
  console.log(`protected_action_executed=${report.protectedActionExecuted}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`mth_resolution_status=${report.mthResolutionStatus}`)
  console.log(`canonical_memory_write_allowed=${report.canonicalMemoryWriteAllowed}`)
  console.log(`allowed_claim_level=${report.allowedClaimLevel}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
