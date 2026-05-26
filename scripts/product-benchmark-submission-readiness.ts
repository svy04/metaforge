import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type LocalBenchmarkHarnessReport = {
  mode: 'local_no_provider_benchmark_replay_harness'
  localBenchmarkResultPath: string
  localBenchmarkResultSha256: string
  localBenchmarkTaskResults: Array<{
    benchmarkTaskId: string
    sourceEvidencePath: string
    sourceEvidenceHashMatches: boolean
    localHarnessStatus: string
    protectedActionExecuted: boolean
    externalBenchmarkResultClaimed: boolean
  }>
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkResultClaimed: false
}

type BenchmarkEfficiencyMetricsReport = {
  mode: 'local_no_provider_benchmark_efficiency_metrics'
  metricsJsonlPath: string
  metricsJsonlSha256: string
  benchmarkEfficiencyRecords: Array<{
    benchmarkTaskId: string
    metricGapStatus: string
  }>
  externalComparisonClaimAllowed: false
}

type RealTraceEvalsReport = {
  mode: string
  traceFileCount: number
  traces: Array<{
    path: string
    sha256: string
    eventCount: number
    statusSequenceValid: boolean
  }>
}

type SubmissionAssetStatus =
  | 'local_equivalent_available'
  | 'partial_local_equivalent_available'
  | 'classified_unresolved_protected_action_required'

type BenchmarkSubmissionAssetRecord = {
  assetId: string
  sweBenchRequiredAsset: string
  localEquivalentPath: string | null
  localEquivalentSha256: string | null
  readinessStatus: SubmissionAssetStatus
  requiredForExternalSubmission: boolean
  protectedActionRequiredToComplete: boolean
  protectedActionExecuted: false
  externalSubmissionClaimed: false
  notes: string
}

type BenchmarkSubmissionReadinessReport = {
  generatedAt: string
  mode: 'local_no_provider_benchmark_submission_readiness'
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  sourceBenchmarkEfficiencyMetricsPath: string
  sourceBenchmarkEfficiencyMetricsJsonlPath: string
  sourceBenchmarkEfficiencyMetricsJsonlSha256: string
  sourceRealTraceEvalsPath: string
  sourceRealTraceCount: number
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  submissionAssetsJsonlPath: string
  submissionAssetsJsonlSha256: string
  requiredSubmissionAssets: string[]
  submissionAssetRecords: BenchmarkSubmissionAssetRecord[]
  summary: {
    requiredAssetCount: number
    localEquivalentAvailableCount: number
    partialLocalEquivalentCount: number
    classifiedUnresolvedProtectedGapCount: number
    officialExternalSubmissionReady: false
  }
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkSubmissionPerformed: false
  externalBenchmarkResultClaimed: false
  externalLeaderboardClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  submissionReadinessChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceHarnessPath = 'docs/product-quality/local-benchmark-harness-report.json'
const sourceEfficiencyPath = 'docs/product-quality/benchmark-efficiency-metrics-report.json'
const sourceRealTraceEvalsPath = 'docs/product-quality/real-session-trace-evals-report.json'
const submissionAssetsJsonlPath = 'reports/openclaude-benchmark-submission-assets.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function sha256Text(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function fileSha256(path: string | null): string | null {
  if (!path || !existsSync(resolve(root, path))) return null
  return createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function asset(
  assetId: string,
  sweBenchRequiredAsset: string,
  readinessStatus: SubmissionAssetStatus,
  localEquivalentPath: string | null,
  notes: string,
): BenchmarkSubmissionAssetRecord {
  const protectedGap = readinessStatus === 'classified_unresolved_protected_action_required'
  return {
    assetId,
    sweBenchRequiredAsset,
    localEquivalentPath,
    localEquivalentSha256: fileSha256(localEquivalentPath),
    readinessStatus,
    requiredForExternalSubmission: true,
    protectedActionRequiredToComplete: protectedGap,
    protectedActionExecuted: false,
    externalSubmissionClaimed: false,
    notes,
  }
}

function buildAssets(
  harness: LocalBenchmarkHarnessReport,
  efficiency: BenchmarkEfficiencyMetricsReport,
  traces: RealTraceEvalsReport,
): BenchmarkSubmissionAssetRecord[] {
  const allTaskHashesMatch = harness.localBenchmarkTaskResults.every((item) => item.sourceEvidenceHashMatches)
  const hasPerTaskLocalResults = harness.localBenchmarkTaskResults.length > 0 && allTaskHashesMatch
  const hasEfficiencyRecords = efficiency.benchmarkEfficiencyRecords.length === harness.localBenchmarkTaskResults.length
  const hasTraceCorpus = traces.traceFileCount > 0 && traces.traces.every((trace) => trace.statusSequenceValid)

  return [
    asset(
      'all_predictions_equivalent',
      'all_preds.jsonl or preds.json',
      hasPerTaskLocalResults ? 'local_equivalent_available' : 'classified_unresolved_protected_action_required',
      harness.localBenchmarkResultPath,
      'Local benchmark replay results are prediction/result-shaped evidence only; they are not an official SWE-bench prediction submission.',
    ),
    asset(
      'metadata_yaml',
      'metadata.yaml',
      'classified_unresolved_protected_action_required',
      null,
      'Official benchmark metadata is not generated because external submission and model/provider run authorization are absent.',
    ),
    asset(
      'submission_readme',
      'README.md',
      'partial_local_equivalent_available',
      'docs/product-quality/benchmark-readiness-matrix.md',
      'Local benchmark readiness documentation exists, but it is not an official external benchmark submission README.',
    ),
    asset(
      'reasoning_traces',
      'trajs/',
      hasTraceCorpus ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      'docs/product-quality/real-session-trace-evals-report.json',
      'Local trace corpus exists, but there is not yet one official reasoning trace per external SWE-bench task instance.',
    ),
    asset(
      'evaluation_logs',
      'logs/',
      'partial_local_equivalent_available',
      'docs/product-quality/local-benchmark-harness-report.json',
      'Local harness logs and result records exist, but no official SWE-bench evaluation logs were generated.',
    ),
    asset(
      'patch_diff_per_instance',
      'logs/<instance_id>/patch.diff',
      'classified_unresolved_protected_action_required',
      null,
      'No official per-instance model-generated benchmark patch exists in no-provider mode.',
    ),
    asset(
      'report_json_per_instance',
      'logs/<instance_id>/report.json',
      hasPerTaskLocalResults ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      harness.localBenchmarkResultPath,
      'Local per-task replay records exist, but they are not official SWE-bench per-instance report.json artifacts.',
    ),
    asset(
      'test_output_per_instance',
      'logs/<instance_id>/test_output.txt',
      'classified_unresolved_protected_action_required',
      null,
      'No official eval.sh test output exists because external benchmark execution is not authorized.',
    ),
    asset(
      'rollout_selection_trace',
      'best@k or multiple-rollout selection trace when applicable',
      'classified_unresolved_protected_action_required',
      null,
      'No provider/live multi-rollout benchmark run was executed, so rollout selection evidence remains unresolved.',
    ),
    asset(
      'efficiency_metrics',
      'cost, duration, token, turn, and resolved fields for comparison',
      hasEfficiencyRecords ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      efficiency.metricsJsonlPath,
      'Comparable metric fields are present, but token/cost/duration/turn/resolution values remain classified no-provider gaps.',
    ),
    asset(
      'verified_submission_instructions',
      'instructions for external result verification',
      'classified_unresolved_protected_action_required',
      null,
      'No external verification issue, hosted run, or public leaderboard submission was created.',
    ),
  ]
}

function writeMarkdown(report: BenchmarkSubmissionReadinessReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`)
    .join('\n')
  const assetRows = report.submissionAssetRecords
    .map((record) => `| \`${record.assetId}\` | \`${record.sweBenchRequiredAsset}\` | \`${record.readinessStatus}\` | \`${record.localEquivalentPath ?? 'none'}\` | \`${record.protectedActionRequiredToComplete}\` | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.submissionReadinessChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Benchmark Submission Readiness Report

Generated by: \`bun run product:benchmark-submission-readiness\`

## Claim Boundary

- This is a local no-provider benchmark submission readiness and gap report.
- It maps SWE-bench experiments submission asset expectations to current OpenClaude local evidence.
- It does not create an official SWE-bench submission folder, metadata.yaml, leaderboard PR, external verification issue, provider run, live model run, external service call, container run, hosted CI run, deploy, publish, launch, or public benchmark claim.
- It does not claim external benchmark results, cost efficiency, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- source_local_benchmark_results_path: \`${report.sourceLocalBenchmarkResultsPath}\`
- source_local_benchmark_results_sha256: \`${report.sourceLocalBenchmarkResultsSha256}\`
- source_benchmark_efficiency_metrics_jsonl_path: \`${report.sourceBenchmarkEfficiencyMetricsJsonlPath}\`
- source_benchmark_efficiency_metrics_jsonl_sha256: \`${report.sourceBenchmarkEfficiencyMetricsJsonlSha256}\`
- source_real_trace_count: \`${report.sourceRealTraceCount}\`
- submission_assets_jsonl_path: \`${report.submissionAssetsJsonlPath}\`
- submission_assets_jsonl_sha256: \`${report.submissionAssetsJsonlSha256}\`
- required_asset_count: \`${report.summary.requiredAssetCount}\`
- local_equivalent_available_count: \`${report.summary.localEquivalentAvailableCount}\`
- partial_local_equivalent_count: \`${report.summary.partialLocalEquivalentCount}\`
- classified_unresolved_protected_gap_count: \`${report.summary.classifiedUnresolvedProtectedGapCount}\`
- official_external_submission_ready: \`${report.summary.officialExternalSubmissionReady}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${sourceRows}

## Submission Asset Matrix

| Asset ID | SWE-bench Asset | Status | Local Equivalent | Protected Action Required | Protected Action Executed |
| --- | --- | --- | --- | --- | --- |
${assetRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'benchmark-submission-readiness-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const harness = readJson<LocalBenchmarkHarnessReport>(sourceHarnessPath)
  const efficiency = readJson<BenchmarkEfficiencyMetricsReport>(sourceEfficiencyPath)
  const traces = readJson<RealTraceEvalsReport>(sourceRealTraceEvalsPath)
  const assets = buildAssets(harness, efficiency, traces)
  const submissionAssetsJsonl = `${assets.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, submissionAssetsJsonlPath), submissionAssetsJsonl)
  const submissionAssetsJsonlSha256 = sha256Text(submissionAssetsJsonl)

  const summary = {
    requiredAssetCount: assets.length,
    localEquivalentAvailableCount: assets.filter((record) => record.readinessStatus === 'local_equivalent_available').length,
    partialLocalEquivalentCount: assets.filter((record) => record.readinessStatus === 'partial_local_equivalent_available').length,
    classifiedUnresolvedProtectedGapCount: assets.filter((record) => record.readinessStatus === 'classified_unresolved_protected_action_required').length,
    officialExternalSubmissionReady: false as const,
  }

  const checks = [
    check('local benchmark harness is imported', harness.mode === 'local_no_provider_benchmark_replay_harness', harness.mode),
    check('benchmark efficiency metrics are imported', efficiency.mode === 'local_no_provider_benchmark_efficiency_metrics', efficiency.mode),
    check('real trace eval report is imported', traces.traceFileCount > 0, `${traces.traceFileCount} traces`),
    check('source result hash matches harness report', fileSha256(harness.localBenchmarkResultPath) === harness.localBenchmarkResultSha256, harness.localBenchmarkResultPath),
    check('source efficiency JSONL hash matches metrics report', fileSha256(efficiency.metricsJsonlPath) === efficiency.metricsJsonlSha256, efficiency.metricsJsonlPath),
    check('SWE-bench submission asset matrix covers required assets', assets.length >= 10 && ['all_predictions_equivalent', 'metadata_yaml', 'reasoning_traces', 'evaluation_logs', 'patch_diff_per_instance', 'report_json_per_instance', 'test_output_per_instance'].every((id) => assets.some((assetRecord) => assetRecord.assetId === id)), `${assets.length} assets`),
    check('local equivalents are source-hash-addressed when present', assets.every((assetRecord) => assetRecord.localEquivalentPath === null || (assetRecord.localEquivalentSha256?.length === 64)), `${assets.filter((assetRecord) => assetRecord.localEquivalentPath !== null).length} local equivalents`),
    check('official external submission remains blocked', summary.officialExternalSubmissionReady === false, 'officialExternalSubmissionReady=false'),
    check('protected gaps are classified but not executed', assets.some((assetRecord) => assetRecord.protectedActionRequiredToComplete) && assets.every((assetRecord) => assetRecord.protectedActionExecuted === false), `${summary.classifiedUnresolvedProtectedGapCount} protected gaps`),
    check('submission JSONL hash is recorded', submissionAssetsJsonlSha256.length === 64, submissionAssetsJsonlPath),
  ]

  const report: BenchmarkSubmissionReadinessReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_benchmark_submission_readiness',
    sourceLocalBenchmarkHarnessPath: sourceHarnessPath,
    sourceLocalBenchmarkResultsPath: harness.localBenchmarkResultPath,
    sourceLocalBenchmarkResultsSha256: harness.localBenchmarkResultSha256,
    sourceBenchmarkEfficiencyMetricsPath: sourceEfficiencyPath,
    sourceBenchmarkEfficiencyMetricsJsonlPath: efficiency.metricsJsonlPath,
    sourceBenchmarkEfficiencyMetricsJsonlSha256: efficiency.metricsJsonlSha256,
    sourceRealTraceEvalsPath,
    sourceRealTraceCount: traces.traceFileCount,
    primarySourceInputs: [
      {
        sourceProject: 'SWE-bench/experiments',
        sourceUrl: 'https://github.com/swe-bench/experiments',
        observedPattern: 'Benchmark submissions preserve predictions, metadata, README, trajectories, logs, patch diffs, reports, test output, and verification instructions as inspectable assets.',
      },
      {
        sourceProject: 'SWE-bench/SWE-bench',
        sourceUrl: 'https://github.com/swe-bench/SWE-bench',
        observedPattern: 'External benchmark execution and per-instance evaluation artifacts must remain separate from local readiness evidence.',
      },
      {
        sourceProject: 'OpenHands/benchmarks',
        sourceUrl: 'https://github.com/OpenHands/benchmarks',
        observedPattern: 'Evaluation harnesses should keep runtime, logs, metrics, and remote/container boundaries explicit before large-scale benchmark claims.',
      },
    ],
    submissionAssetsJsonlPath,
    submissionAssetsJsonlSha256,
    requiredSubmissionAssets: assets.map((assetRecord) => assetRecord.sweBenchRequiredAsset),
    submissionAssetRecords: assets,
    summary,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    externalBenchmarkExecutionPerformed: false,
    externalBenchmarkSubmissionPerformed: false,
    externalBenchmarkResultClaimed: false,
    externalLeaderboardClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    submissionReadinessChecks: checks,
    claimBoundary: 'Benchmark submission readiness is local no-provider evidence only. It does not create official SWE-bench submissions, execute external benchmarks, call providers, call live models, call external services, or make leaderboard, release, production, public, external-validation, cost-efficiency, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(docsDir, 'benchmark-submission-readiness-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  if (!checks.every((item) => item.ok)) {
    console.error(`RESULT: FAIL (${checks.filter((item) => !item.ok).length} failed checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log(`submission_assets_jsonl_path=${submissionAssetsJsonlPath}`)
  console.log(`required_asset_count=${summary.requiredAssetCount}`)
  console.log(`local_equivalent_available_count=${summary.localEquivalentAvailableCount}`)
  console.log(`partial_local_equivalent_count=${summary.partialLocalEquivalentCount}`)
  console.log(`classified_unresolved_protected_gap_count=${summary.classifiedUnresolvedProtectedGapCount}`)
  console.log(`official_external_submission_ready=${summary.officialExternalSubmissionReady}`)
  console.log(`external_leaderboard_claim_allowed=${report.externalLeaderboardClaimAllowed}`)
}

main()
