import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type BaselineProject = {
  rank: number
  full_name: string
  stars: number
  license: string
  source_url: string
}

type Baseline = {
  snapshot_date: string
  top10: BaselineProject[]
  required_product_axes: string[]
}

type SourceReviewRecord = {
  fullName: string
  sourceReviewStatus: string
  absorptionCandidate: boolean
  readmeFetched: boolean
  rootContentsFetched: boolean
}

type EvidenceBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type OpenClaudeEvidence = {
  axis: string
  currentLocalEvidence: string[]
  unresolvedGap: string
  protectedBoundary: string
}

type GapRecord = {
  fullName: string
  openClaudeEvidence: OpenClaudeEvidence[]
}

type AxisReviewRecord = {
  fullName: string
  axis: string
}

type MatrixRecord = {
  schemaVersion: 'openclaude_oss_benchmark_comparison_matrix_v1'
  baselineSnapshotDate: string
  rank: number
  fullName: string
  sourceUrl: string
  stars: number
  license: string
  axis: string
  sourceReviewStatus: string
  sourceSupportedCandidate: boolean
  axisReviewPresent: boolean
  openClaudeEvidenceBindings: EvidenceBinding[]
  openClaudeEvidencePresentCount: number
  unresolvedGap: string
  protectedBoundary: string
  benchmarkabilityStatus:
    | 'local_internal_evidence_present_protected_gap_open'
    | 'metadata_only_needs_source_review'
    | 'axis_not_yet_absorbed'
    | 'local_evidence_reference_missing'
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

type Binding = {
  path: string
  exists: boolean
  sha256: string | null
}

type ComparisonMatrixReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_benchmark_comparison_matrix'
  sourceBaselinePath: string
  sourceBaselineSha256: string
  sourceReviewReportPath: string
  sourceReviewReportSha256: string
  sourceGapReviewReportPath: string
  sourceGapReviewReportSha256: string
  sourceAxisReviewReportPath: string
  sourceAxisReviewReportSha256: string
  sourcePublicClaimBoundaryReportPath: string
  sourcePublicClaimBoundaryReportSha256: string
  sourceProtectedActionAuthorizationPacketPath: string
  sourceProtectedActionAuthorizationPacketSha256: string
  baselineSnapshotDate: string
  top10ProjectCount: number
  requiredProductAxisCount: number
  matrixRecordCount: number
  projectAxisCoverageExpectedCount: number
  recordsWithLocalEvidenceCount: number
  recordsNeedingProtectedActionCount: number
  metadataOnlyRecordCount: number
  axisNotYetAbsorbedRecordCount: number
  comparisonMatrixJsonlPath: string
  comparisonMatrixJsonlSha256: string
  comparisonMatrixJsonlRecordCount: number
  sourceReportBindings: Binding[]
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  matrixRecords: MatrixRecord[]
  matrixChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceBaselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
const sourceReviewReportPath = 'docs/product-quality/oss-source-review-report.json'
const sourceGapReviewReportPath = 'docs/product-quality/oss-architecture-gap-review-report.json'
const sourceAxisReviewReportPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
const sourcePublicClaimBoundaryReportPath = 'docs/product-quality/public-claim-boundary-report.json'
const sourceProtectedActionAuthorizationPacketPath = 'docs/product-quality/protected-action-authorization-packet.json'
const reportJsonPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.json'
const reportMdPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.md'
const comparisonMatrixJsonlPath = 'reports/openclaude-oss-benchmark-comparison-matrix.jsonl'

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function fileSha256(path: string): string | null {
  const absolutePath = resolve(root, path)
  return existsSync(absolutePath) ? sha256(readFileSync(absolutePath)) : null
}

function binding(path: string): Binding {
  return {
    path,
    exists: existsSync(resolve(root, path)),
    sha256: fileSha256(path),
  }
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function evidenceBinding(path: string): EvidenceBinding {
  const absolutePath = resolve(root, path)
  return {
    path,
    exists: existsSync(absolutePath),
    sha256: existsSync(absolutePath) ? sha256(readFileSync(absolutePath)) : null,
    sizeBytes: existsSync(absolutePath) ? statSync(absolutePath).size : 0,
  }
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  return [
    'publicComparisonClaimAllowed',
    'superiorityClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
    'releaseClaimAllowed',
  ].every((key) => report[key] !== true)
}

function arrayIsEmpty(report: Record<string, unknown>, key: string): boolean {
  const value = report[key]
  return Array.isArray(value) && value.length === 0
}

function matrixRecord(
  baselineSnapshotDate: string,
  project: BaselineProject,
  axis: string,
  sourceReview: SourceReviewRecord | undefined,
  gap: GapRecord | undefined,
  axisReviews: AxisReviewRecord[],
): MatrixRecord {
  const evidence = gap?.openClaudeEvidence.find((item) => item.axis === axis)
  const evidenceBindings = (evidence?.currentLocalEvidence ?? []).map(evidenceBinding)
  const sourceSupportedCandidate = sourceReview?.sourceReviewStatus === 'source_supported_candidate' && sourceReview.absorptionCandidate === true
  const axisReviewPresent = axisReviews.some((item) => item.fullName === project.full_name && item.axis === axis)
  const evidenceReferencesPresent = evidenceBindings.every((item) => item.exists && item.sha256 !== null && item.sizeBytes > 0)
  const benchmarkabilityStatus: MatrixRecord['benchmarkabilityStatus'] =
    evidence && evidenceReferencesPresent
      ? 'local_internal_evidence_present_protected_gap_open'
      : evidence && !evidenceReferencesPresent
        ? 'local_evidence_reference_missing'
        : !sourceSupportedCandidate
          ? 'metadata_only_needs_source_review'
          : 'axis_not_yet_absorbed'

  return {
    schemaVersion: 'openclaude_oss_benchmark_comparison_matrix_v1',
    baselineSnapshotDate,
    rank: project.rank,
    fullName: project.full_name,
    sourceUrl: project.source_url,
    stars: project.stars,
    license: project.license,
    axis,
    sourceReviewStatus: sourceReview?.sourceReviewStatus ?? 'missing_source_review',
    sourceSupportedCandidate,
    axisReviewPresent,
    openClaudeEvidenceBindings: evidenceBindings,
    openClaudeEvidencePresentCount: evidenceBindings.filter((item) => item.exists).length,
    unresolvedGap: evidence?.unresolvedGap ?? 'No current OpenClaude axis evidence has been bound for this project-axis pair yet.',
    protectedBoundary: evidence?.protectedBoundary ?? 'Further source review, implementation absorption, external validation, or public comparison requires a later bounded authorization gate.',
    benchmarkabilityStatus,
    protectedActionRequiredForNextStep: true,
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

function writeMarkdown(report: ComparisonMatrixReport): void {
  const statusCounts = report.matrixRecords.reduce<Record<string, number>>((counts, record) => {
    counts[record.benchmarkabilityStatus] = (counts[record.benchmarkabilityStatus] ?? 0) + 1
    return counts
  }, {})
  const statusRows = Object.entries(statusCounts)
    .map(([status, count]) => `| \`${status}\` | ${count} |`)
    .join('\n')
  const sourceRows = report.sourceReportBindings
    .map((item) => `| \`${item.path}\` | \`${item.exists}\` | \`${item.sha256 ?? 'missing'}\` |`)
    .join('\n')
  const matrixRows = report.matrixRecords
    .slice(0, 40)
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | \`${record.axis}\` | \`${record.benchmarkabilityStatus}\` | ${record.openClaudeEvidencePresentCount} | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.matrixChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Benchmark Comparison Matrix Report

Generated by: \`bun run product:oss-benchmark-comparison-matrix\`

## Claim Boundary

- This matrix makes OpenClaude more benchmarkable against the current related GitHub top 10 by binding every project-axis pair to local evidence or an explicit gap.
- It performs no provider calls, live model calls, dependency installs, protected actions, external benchmark execution, public comparison claims, or superiority claims.
- It does not claim OpenClaude beats any project. It records what can be internally compared and what still requires protected authorization.

## Summary

- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- top10_project_count: \`${report.top10ProjectCount}\`
- required_product_axis_count: \`${report.requiredProductAxisCount}\`
- project_axis_coverage_expected_count: \`${report.projectAxisCoverageExpectedCount}\`
- matrix_record_count: \`${report.matrixRecordCount}\`
- records_with_local_evidence_count: \`${report.recordsWithLocalEvidenceCount}\`
- records_needing_protected_action_count: \`${report.recordsNeedingProtectedActionCount}\`
- metadata_only_record_count: \`${report.metadataOnlyRecordCount}\`
- axis_not_yet_absorbed_record_count: \`${report.axisNotYetAbsorbedRecordCount}\`
- comparison_matrix_jsonl_path: \`${report.comparisonMatrixJsonlPath}\`
- comparison_matrix_jsonl_sha256: \`${report.comparisonMatrixJsonlSha256}\`

## Status Counts

| Status | Count |
| --- | ---: |
${statusRows}

## Source Bindings

| Source | Exists | SHA-256 |
| --- | --- | --- |
${sourceRows}

## Matrix Preview

First 40 of ${report.matrixRecordCount} rows.

| Rank | Project | Axis | Status | Local Evidence Bindings | Protected Action Executed |
| ---: | --- | --- | --- | ---: | --- |
${matrixRows}

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

  const baseline = readJson<Baseline>(sourceBaselinePath)
  const sourceReviewReport = readJson<{ reviewRecords: SourceReviewRecord[] } & Record<string, unknown>>(sourceReviewReportPath)
  const gapReviewReport = readJson<{ gapRecords: GapRecord[] } & Record<string, unknown>>(sourceGapReviewReportPath)
  const axisReviewReport = readJson<{ axisReviewRecords: AxisReviewRecord[] } & Record<string, unknown>>(sourceAxisReviewReportPath)
  const publicClaimBoundaryReport = readJson<Record<string, unknown>>(sourcePublicClaimBoundaryReportPath)
  const protectedActionAuthorizationPacket = readJson<Record<string, unknown>>(sourceProtectedActionAuthorizationPacketPath)

  const matrixRecords = baseline.top10.flatMap((project) => {
    const sourceReview = sourceReviewReport.reviewRecords.find((record) => record.fullName === project.full_name)
    const gap = gapReviewReport.gapRecords.find((record) => record.fullName === project.full_name)
    return baseline.required_product_axes.map((axis) =>
      matrixRecord(baseline.snapshot_date, project, axis, sourceReview, gap, axisReviewReport.axisReviewRecords),
    )
  })

  const matrixJsonlText = matrixRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, comparisonMatrixJsonlPath), matrixJsonlText)
  const comparisonMatrixJsonlSha256 = sha256(matrixJsonlText)
  const sourceReportBindings = [
    sourceBaselinePath,
    sourceReviewReportPath,
    sourceGapReviewReportPath,
    sourceAxisReviewReportPath,
    sourcePublicClaimBoundaryReportPath,
    sourceProtectedActionAuthorizationPacketPath,
  ].map(binding)
  const recordsWithLocalEvidence = matrixRecords.filter((record) =>
    record.benchmarkabilityStatus === 'local_internal_evidence_present_protected_gap_open',
  )
  const metadataOnlyRecords = matrixRecords.filter((record) =>
    record.benchmarkabilityStatus === 'metadata_only_needs_source_review',
  )
  const axisNotYetAbsorbedRecords = matrixRecords.filter((record) =>
    record.benchmarkabilityStatus === 'axis_not_yet_absorbed',
  )
  const expectedCount = baseline.top10.length * baseline.required_product_axes.length

  const report: ComparisonMatrixReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_benchmark_comparison_matrix',
    sourceBaselinePath,
    sourceBaselineSha256: sha256(readFileSync(resolve(root, sourceBaselinePath))),
    sourceReviewReportPath,
    sourceReviewReportSha256: sha256(readFileSync(resolve(root, sourceReviewReportPath))),
    sourceGapReviewReportPath,
    sourceGapReviewReportSha256: sha256(readFileSync(resolve(root, sourceGapReviewReportPath))),
    sourceAxisReviewReportPath,
    sourceAxisReviewReportSha256: sha256(readFileSync(resolve(root, sourceAxisReviewReportPath))),
    sourcePublicClaimBoundaryReportPath,
    sourcePublicClaimBoundaryReportSha256: sha256(readFileSync(resolve(root, sourcePublicClaimBoundaryReportPath))),
    sourceProtectedActionAuthorizationPacketPath,
    sourceProtectedActionAuthorizationPacketSha256: sha256(readFileSync(resolve(root, sourceProtectedActionAuthorizationPacketPath))),
    baselineSnapshotDate: baseline.snapshot_date,
    top10ProjectCount: baseline.top10.length,
    requiredProductAxisCount: baseline.required_product_axes.length,
    matrixRecordCount: matrixRecords.length,
    projectAxisCoverageExpectedCount: expectedCount,
    recordsWithLocalEvidenceCount: recordsWithLocalEvidence.length,
    recordsNeedingProtectedActionCount: matrixRecords.filter((record) => record.protectedActionRequiredForNextStep).length,
    metadataOnlyRecordCount: metadataOnlyRecords.length,
    axisNotYetAbsorbedRecordCount: axisNotYetAbsorbedRecords.length,
    comparisonMatrixJsonlPath,
    comparisonMatrixJsonlSha256,
    comparisonMatrixJsonlRecordCount: matrixRecords.length,
    sourceReportBindings,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST repository metadata',
        sourceUrl: 'https://docs.github.com/en/rest/repos/repos',
        observedPattern: 'Benchmark candidate sets are mutable repository facts and need dated, source-bound project identifiers.',
        localAbsorption: 'OpenClaude creates one comparison row for every current top-10 project and required product axis.',
      },
      {
        sourceProject: 'OpenSSF Scorecard',
        sourceUrl: 'https://github.com/ossf/scorecard',
        observedPattern: 'High-quality open-source comparisons are stronger when checks are explicit, repeatable, and separated from unsupported claims.',
        localAbsorption: 'OpenClaude records benchmarkability status, local evidence bindings, and protected gaps separately from public or superiority claims.',
      },
      {
        sourceProject: 'SLSA provenance materials model',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence consumers need traceable materials and hash-bound inputs before trusting derived reports.',
        localAbsorption: 'OpenClaude binds the comparison matrix to baseline, source review, gap review, public-claim, and protected-action reports.',
      },
    ],
    selfImprovementActions: [
      'Add a top-10-by-axis benchmark comparison matrix so benchmark planning is not only project-level but project-axis complete.',
      'Separate local internal evidence presence from metadata-only, not-yet-absorbed, and protected-action-required statuses.',
      'Keep comparison, superiority, release, production, public, external-validation, and autonomous-reliability claims blocked until later protected gates pass.',
    ],
    matrixRecords,
    matrixChecks: [],
    claimBoundary: 'OSS benchmark comparison matrix is internal local no-provider benchmarkability evidence only. It does not execute external benchmarks, protected actions, providers, live models, or public comparison/superiority/readiness claims.',
  }

  const uniqueProjectAxisKeys = new Set(matrixRecords.map((record) => `${record.fullName}\u0000${record.axis}`))
  report.matrixChecks = [
    check('all source reports are present and hash-bound', sourceReportBindings.every((item) => item.exists && typeof item.sha256 === 'string' && item.sha256.length === 64), `${sourceReportBindings.filter((item) => item.exists).length}/${sourceReportBindings.length}`),
    check('baseline covers current top 10 projects', report.top10ProjectCount === 10, `${report.top10ProjectCount}/10`),
    check('required product axes are complete for benchmark planning', report.requiredProductAxisCount === 10, `${report.requiredProductAxisCount}/10`),
    check('matrix has one row per project-axis pair', report.matrixRecordCount === expectedCount && uniqueProjectAxisKeys.size === expectedCount, `${report.matrixRecordCount}/${expectedCount}`),
    check('matrix JSONL has one parseable row per matrix record', matrixJsonlText.trim().split(/\r?\n/).length === matrixRecords.length && report.comparisonMatrixJsonlRecordCount === matrixRecords.length, `${report.comparisonMatrixJsonlRecordCount}/${matrixRecords.length}`),
    check('local evidence bindings point to existing hashable files', matrixRecords.every((record) => record.openClaudeEvidenceBindings.every((item) => item.exists && item.sha256 !== null && item.sizeBytes > 0)), `${recordsWithLocalEvidence.length} evidence-backed rows`),
    check('matrix records preserve protected-action boundary', matrixRecords.every((record) => record.protectedActionRequiredForNextStep === true && record.protectedActionExecuted === false), `${report.recordsNeedingProtectedActionCount}/${matrixRecords.length}`),
    check('matrix records block comparison superiority and readiness claims', matrixRecords.every((record) => record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false), 'all record claim flags false'),
    check('this matrix gate performs no provider live external or protected calls', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0, 'all arrays empty'),
    check('source boundary reports keep claims blocked', [sourceReviewReport, gapReviewReport, axisReviewReport, publicClaimBoundaryReport, protectedActionAuthorizationPacket, report].every(claimsBlocked), 'all claim flags false'),
    check('public claim boundary has no unauthorized positive claims', publicClaimBoundaryReport.unauthorizedPositiveClaimCount === 0, String(publicClaimBoundaryReport.unauthorizedPositiveClaimCount ?? 'missing')),
    check('protected authorizations remain default false', Array.isArray(protectedActionAuthorizationPacket.requiredOwnerAuthorizations) && protectedActionAuthorizationPacket.requiredOwnerAuthorizations.every((item) => item && typeof item === 'object' && (item as { authorized?: unknown; executed?: unknown }).authorized === false && (item as { executed?: unknown }).executed === false), String((protectedActionAuthorizationPacket.requiredOwnerAuthorizations as unknown[] | undefined)?.length ?? 0)),
    check('upstream provider live and protected actions remain empty where required', [sourceReviewReport, gapReviewReport, axisReviewReport, publicClaimBoundaryReport, protectedActionAuthorizationPacket].every((item) => arrayIsEmpty(item, 'providerCallsPerformed') && arrayIsEmpty(item, 'liveModelCallsPerformed') && arrayIsEmpty(item, 'protectedActionsExecuted')), 'provider/live/protected arrays empty'),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.matrixChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.matrixChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`baseline_snapshot_date=${report.baselineSnapshotDate}`)
  console.log(`top10_project_count=${report.top10ProjectCount}`)
  console.log(`required_product_axis_count=${report.requiredProductAxisCount}`)
  console.log(`matrix_record_count=${report.matrixRecordCount}`)
  console.log(`records_with_local_evidence=${report.recordsWithLocalEvidenceCount}`)
  console.log(`metadata_only_record_count=${report.metadataOnlyRecordCount}`)
  console.log(`axis_not_yet_absorbed_record_count=${report.axisNotYetAbsorbedRecordCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
