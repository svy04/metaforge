import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type Binding = {
  path: string
  exists: boolean
  sha256: string | null
}

type DriftRecord = {
  project: string
  driftKind: 'newly_discovered_top10' | 'removed_previous_top10'
  presentInCurrentBaseline: boolean
  presentInSourceReview: boolean
  presentInArchitectureTargets: boolean
  presentInGapReview: boolean
  presentInAxisHighPriorityReview: boolean
  status: 'propagated_to_current_internal_evidence' | 'removed_from_current_top10_only'
}

type DriftClosureReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_baseline_drift_closure'
  sourceRefreshReportPath: string
  sourceRefreshReportSha256: string
  sourceBaselinePath: string
  sourceBaselineSha256: string
  baselineSnapshotDate: string
  top10ProjectCount: number
  newlyDiscoveredTop10Projects: string[]
  removedPreviousTop10Projects: string[]
  propagatedNewDiscoveryCount: number
  removedPreviousTop10Count: number
  driftRecordCount: number
  driftJsonlPath: string
  driftJsonlSha256: string
  driftJsonlRecordCount: number
  sourceReportBindings: Binding[]
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  sourceExternalGitHubRefreshPerformed: boolean
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  driftRecords: DriftRecord[]
  driftChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceRefreshReportPath = 'docs/product-quality/oss-baseline-refresh-report.json'
const sourceBaselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
const sourceReviewReportPath = 'docs/product-quality/oss-source-review-report.json'
const architectureTargetsReportPath = 'docs/product-quality/oss-architecture-absorption-targets-report.json'
const gapReviewReportPath = 'docs/product-quality/oss-architecture-gap-review-report.json'
const axisReviewReportPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
const safeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const safeBacklogClosureReportPath = 'docs/product-quality/oss-safe-backlog-closure-report.json'
const reportJsonPath = 'docs/product-quality/oss-baseline-drift-closure-report.json'
const reportMdPath = 'docs/product-quality/oss-baseline-drift-closure-report.md'
const driftJsonlPath = 'reports/openclaude-oss-baseline-drift-closure.jsonl'

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

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function binding(path: string): Binding {
  return {
    path,
    exists: existsSync(resolve(root, path)),
    sha256: fileSha256(path),
  }
}

function stringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === 'string') : []
}

function fullNamesFromRecords(value: unknown): string[] {
  if (!Array.isArray(value)) return []
  return value
    .map((item) => item && typeof item === 'object' && 'fullName' in item ? (item as { fullName?: unknown }).fullName : null)
    .filter((item): item is string => typeof item === 'string')
}

function hasNoCalls(report: Record<string, unknown>): boolean {
  return ['providerCallsPerformed', 'liveModelCallsPerformed', 'externalCallsPerformed', 'protectedActionsExecuted']
    .every((key) => Array.isArray(report[key]) && (report[key] as unknown[]).length === 0)
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  return [
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'publicComparisonClaimAllowed',
    'superiorityClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
  ].every((key) => report[key] !== true)
}

function writeMarkdown(report: DriftClosureReport): void {
  const bindingRows = report.sourceReportBindings
    .map((item) => `| \`${item.path}\` | \`${item.exists}\` | \`${item.sha256 ?? 'missing'}\` |`)
    .join('\n')
  const recordRows = report.driftRecords
    .map((record) => `| \`${record.project}\` | \`${record.driftKind}\` | \`${record.presentInCurrentBaseline}\` | \`${record.presentInSourceReview}\` | \`${record.presentInArchitectureTargets}\` | \`${record.presentInAxisHighPriorityReview}\` | \`${record.status}\` |`)
    .join('\n')
  const checkRows = report.driftChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Baseline Drift Closure Report

Generated by: \`bun run product:oss-baseline-drift-closure\`

## Claim Boundary

- This report verifies that a fresh GitHub top-10 baseline change is propagated into local no-provider planning and evidence reports.
- It performs no provider calls, live model calls, dependency installs, protected actions, release actions, public comparison claims, or superiority claims.
- It does not claim OpenClaude is better than the top projects; it only verifies that benchmark-discovery drift is not left stale.

## Summary

- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- top10_project_count: \`${report.top10ProjectCount}\`
- newly_discovered_top10_projects: \`${report.newlyDiscoveredTop10Projects.join(',') || 'none'}\`
- removed_previous_top10_projects: \`${report.removedPreviousTop10Projects.join(',') || 'none'}\`
- propagated_new_discovery_count: \`${report.propagatedNewDiscoveryCount}\`
- removed_previous_top10_count: \`${report.removedPreviousTop10Count}\`
- drift_jsonl_path: \`${report.driftJsonlPath}\`
- drift_jsonl_sha256: \`${report.driftJsonlSha256}\`

## Source Bindings

| Source | Exists | SHA-256 |
| --- | --- | --- |
${bindingRows}

## Drift Records

| Project | Drift Kind | In Current Baseline | In Source Review | In Architecture Targets | In Axis High Priority Review | Status |
| --- | --- | --- | --- | --- | --- | --- |
${recordRows}

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

  const refreshReport = readJson<Record<string, unknown>>(sourceRefreshReportPath)
  const baseline = readJson<{ top10: Array<{ full_name: string }> }>(sourceBaselinePath)
  const sourceReview = readJson<Record<string, unknown>>(sourceReviewReportPath)
  const architectureTargets = readJson<Record<string, unknown>>(architectureTargetsReportPath)
  const gapReview = readJson<Record<string, unknown>>(gapReviewReportPath)
  const axisReview = readJson<Record<string, unknown>>(axisReviewReportPath)
  const safeBacklogPlan = readJson<Record<string, unknown>>(safeBacklogPlanReportPath)
  const safeBacklogClosure = readJson<Record<string, unknown>>(safeBacklogClosureReportPath)

  const currentBaselineProjects = baseline.top10.map((project) => project.full_name)
  const sourceReviewProjects = fullNamesFromRecords(sourceReview.reviewRecords)
  const architectureTargetProjects = fullNamesFromRecords(architectureTargets.targetRecords)
  const gapReviewProjects = fullNamesFromRecords(gapReview.gapRecords)
  const axisReviewProjects = Array.from(new Set(fullNamesFromRecords(axisReview.axisReviewRecords)))
  const newlyDiscoveredTop10Projects = stringArray(refreshReport.newlyDiscoveredTop10Projects)
  const removedPreviousTop10Projects = stringArray(refreshReport.removedPreviousTop10Projects)

  const newRecords: DriftRecord[] = newlyDiscoveredTop10Projects.map((project) => ({
    project,
    driftKind: 'newly_discovered_top10',
    presentInCurrentBaseline: currentBaselineProjects.includes(project),
    presentInSourceReview: sourceReviewProjects.includes(project),
    presentInArchitectureTargets: architectureTargetProjects.includes(project),
    presentInGapReview: gapReviewProjects.includes(project),
    presentInAxisHighPriorityReview: axisReviewProjects.includes(project),
    status: 'propagated_to_current_internal_evidence',
  }))

  const removedRecords: DriftRecord[] = removedPreviousTop10Projects.map((project) => ({
    project,
    driftKind: 'removed_previous_top10',
    presentInCurrentBaseline: currentBaselineProjects.includes(project),
    presentInSourceReview: sourceReviewProjects.includes(project),
    presentInArchitectureTargets: architectureTargetProjects.includes(project),
    presentInGapReview: gapReviewProjects.includes(project),
    presentInAxisHighPriorityReview: axisReviewProjects.includes(project),
    status: 'removed_from_current_top10_only',
  }))

  const driftRecords = [...newRecords, ...removedRecords]
  const driftJsonlText = driftRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, driftJsonlPath), driftJsonlText)
  const driftJsonlSha256 = sha256(driftJsonlText)

  const sourceReportBindings = [
    sourceRefreshReportPath,
    sourceBaselinePath,
    sourceReviewReportPath,
    architectureTargetsReportPath,
    gapReviewReportPath,
    axisReviewReportPath,
    safeBacklogPlanReportPath,
    safeBacklogClosureReportPath,
  ].map(binding)

  const propagatedNewDiscoveries = newRecords.filter((record) =>
    record.presentInCurrentBaseline &&
    record.presentInSourceReview &&
    record.presentInArchitectureTargets &&
    record.presentInGapReview &&
    record.presentInAxisHighPriorityReview,
  )
  const removedFromCurrentBaseline = removedRecords.filter((record) =>
    !record.presentInCurrentBaseline &&
    !record.presentInSourceReview &&
    !record.presentInArchitectureTargets &&
    !record.presentInGapReview &&
    !record.presentInAxisHighPriorityReview,
  )

  const report: DriftClosureReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_baseline_drift_closure',
    sourceRefreshReportPath,
    sourceRefreshReportSha256: sha256(readFileSync(resolve(root, sourceRefreshReportPath))),
    sourceBaselinePath,
    sourceBaselineSha256: sha256(readFileSync(resolve(root, sourceBaselinePath))),
    baselineSnapshotDate: String(refreshReport.snapshotDate ?? 'unknown'),
    top10ProjectCount: baseline.top10.length,
    newlyDiscoveredTop10Projects,
    removedPreviousTop10Projects,
    propagatedNewDiscoveryCount: propagatedNewDiscoveries.length,
    removedPreviousTop10Count: removedFromCurrentBaseline.length,
    driftRecordCount: driftRecords.length,
    driftJsonlPath,
    driftJsonlSha256,
    driftJsonlRecordCount: driftRecords.length,
    sourceReportBindings,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    sourceExternalGitHubRefreshPerformed: refreshReport.externalGitHubRefreshPerformed === true,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST repository metadata',
        sourceUrl: 'https://docs.github.com/en/rest/repos/repos',
        observedPattern: 'Mutable repository metadata must be treated as dated evidence and synchronized through downstream review reports.',
        localAbsorption: 'OpenClaude verifies that new and removed top-10 baseline projects are reflected in source review, architecture targeting, and safe backlog closure evidence.',
      },
      {
        sourceProject: 'SLSA provenance materials model',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence chains are stronger when downstream materials remain hash-bound to refreshed upstream inputs.',
        localAbsorption: 'OpenClaude records report bindings and a drift JSONL record so stale benchmark inputs cannot masquerade as current evidence.',
      },
    ],
    selfImprovementActions: [
      'Add a drift-closure gate so newly discovered high-star OSS candidates must propagate through local evidence reports before benchmark planning is considered current.',
      'Record removed prior top-10 projects as no longer current top-10 inputs instead of silently leaving them in benchmark target reports.',
      'Keep public comparison, superiority, release, production, external-validation, and autonomous-reliability claims blocked after baseline drift is closed.',
    ],
    driftRecords,
    driftChecks: [],
    claimBoundary: 'OSS baseline drift closure is internal benchmark-discovery evidence only and does not authorize public comparison, superiority claims, release actions, provider calls, live model calls, or protected mutations.',
  }

  report.driftChecks = [
    check('all source reports are present and hash-bound', sourceReportBindings.every((item) => item.exists && typeof item.sha256 === 'string' && item.sha256.length === 64), `${sourceReportBindings.filter((item) => item.exists).length}/${sourceReportBindings.length}`),
    check('fresh refresh report still has 10 top projects', report.top10ProjectCount === 10 && refreshReport.top10ProjectCount === 10, `${report.top10ProjectCount}/${String(refreshReport.top10ProjectCount)}`),
    check('newly discovered top-10 projects propagated to downstream evidence', newlyDiscoveredTop10Projects.length > 0 && propagatedNewDiscoveries.length === newlyDiscoveredTop10Projects.length, `${propagatedNewDiscoveries.length}/${newlyDiscoveredTop10Projects.length}`),
    check('removed prior top-10 projects are absent from current downstream target reports', removedPreviousTop10Projects.length > 0 && removedFromCurrentBaseline.length === removedPreviousTop10Projects.length, `${removedFromCurrentBaseline.length}/${removedPreviousTop10Projects.length}`),
    check('source review covers every current baseline project', sourceReviewProjects.length === currentBaselineProjects.length && currentBaselineProjects.every((project) => sourceReviewProjects.includes(project)), `${sourceReviewProjects.length}/${currentBaselineProjects.length}`),
    check('architecture targets cover every current baseline project', architectureTargetProjects.length === currentBaselineProjects.length && currentBaselineProjects.every((project) => architectureTargetProjects.includes(project)), `${architectureTargetProjects.length}/${currentBaselineProjects.length}`),
    check('gap review covers every current baseline project', gapReviewProjects.length === currentBaselineProjects.length && currentBaselineProjects.every((project) => gapReviewProjects.includes(project)), `${gapReviewProjects.length}/${currentBaselineProjects.length}`),
    check('axis high-priority review covers the newly discovered projects', newlyDiscoveredTop10Projects.every((project) => axisReviewProjects.includes(project)), axisReviewProjects.join(',') || 'none'),
    check('safe backlog plan and closure remain synchronized', safeBacklogClosure.sourceCandidateCount === safeBacklogPlan.nextSafeInternalGateCandidateCount && safeBacklogClosure.openCandidateCount === 0, `${String(safeBacklogClosure.closedCandidateCount)}/${String(safeBacklogPlan.nextSafeInternalGateCandidateCount)}`),
    check('drift JSONL has one record per changed baseline project', report.driftJsonlRecordCount === newlyDiscoveredTop10Projects.length + removedPreviousTop10Projects.length, `${report.driftJsonlRecordCount}/${newlyDiscoveredTop10Projects.length + removedPreviousTop10Projects.length}`),
    check('this drift closure gate performs no provider live external or protected calls', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0, 'all arrays empty'),
    check('downstream no-provider reports preserve call boundaries', [architectureTargets, gapReview, axisReview, safeBacklogPlan, safeBacklogClosure].every(hasNoCalls), 'all downstream local reports empty call arrays'),
    check('claim expansion remains blocked across drift closure sources', [refreshReport, sourceReview, architectureTargets, gapReview, axisReview, safeBacklogPlan, safeBacklogClosure, report].every(claimsBlocked), 'all claim flags false'),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.driftChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.driftChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`baseline_snapshot_date=${report.baselineSnapshotDate}`)
  console.log(`newly_discovered_top10_count=${report.newlyDiscoveredTop10Projects.length}`)
  console.log(`propagated_new_discovery_count=${report.propagatedNewDiscoveryCount}`)
  console.log(`removed_previous_top10_count=${report.removedPreviousTop10Count}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
