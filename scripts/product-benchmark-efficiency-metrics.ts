import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type LocalBenchmarkTaskResult = {
  benchmarkTaskId: string
  benchmarkFamily: string
  sourceEvidencePath: string
  sourceEvidenceExists: boolean
  actualSourceEvidenceSha256: string | null
  sourceEvidenceHashMatches: boolean
  requiredEvidenceCount: number
  terminalOutcomeClass: string
  localHarnessStatus: string
  protectedActionExecuted: boolean
  externalBenchmarkResultClaimed: boolean
  providerCallsPerformed: number
  liveModelCallsPerformed: number
  externalCallsPerformed: number
}

type LocalBenchmarkHarnessReport = {
  mode: string
  localBenchmarkResultPath: string
  localBenchmarkResultSha256: string
  localBenchmarkTaskResults: LocalBenchmarkTaskResult[]
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkResultClaimed: boolean
}

type BenchmarkEfficiencyRecord = {
  benchmarkTaskId: string
  benchmarkFamily: string
  localHarnessStatus: string
  localOutcomeForReplayOnly: string
  sourceEvidencePath: string
  sourceEvidenceSha256: string | null
  sourceEvidenceSizeBytes: number | null
  sourceEvidenceLineCount: number | null
  comparableMetricFields: {
    agent: 'openclaude_local_no_provider'
    model: null
    inputTokens: null
    outputTokens: null
    costUsd: null
    numTurns: null
    durationMs: null
    resolved: null
  }
  metricAvailability: {
    tokenUsageMeasured: false
    costMeasured: false
    durationMeasured: false
    turnCountMeasured: false
    externalResolvedMeasured: false
  }
  metricGapStatus: 'classified_unresolved_external_or_live_run_required'
  protectedActionExecuted: false
  externalBenchmarkResultClaimed: false
}

type BenchmarkEfficiencyMetricsReport = {
  generatedAt: string
  mode: 'local_no_provider_benchmark_efficiency_metrics'
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  metricSchemaFields: string[]
  metricsJsonlPath: string
  metricsJsonlSha256: string
  benchmarkEfficiencyRecords: BenchmarkEfficiencyRecord[]
  summary: {
    sourceTaskCount: number
    comparableRecordCount: number
    recordsWithComparableMetricFields: number
    recordsWithMeasuredTokenCostDuration: number
    classifiedMetricGapCount: number
  }
  unresolvedMetricGaps: Array<{
    id: string
    status: 'classified_unresolved'
    requiredBeforeExternalComparisonClaim: boolean
    protectedActionRequired: boolean
    protectedActionExecuted: false
  }>
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkResultClaimed: false
  externalComparisonClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  efficiencyChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceHarnessPath = 'docs/product-quality/local-benchmark-harness-report.json'
const metricsJsonlPath = 'reports/openclaude-benchmark-efficiency-metrics.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function sha256Text(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function fileLineCount(path: string): number | null {
  if (!existsSync(resolve(root, path))) return null
  const text = readFileSync(resolve(root, path), 'utf8').trim()
  if (text.length === 0) return 0
  return text.split(/\r?\n/).length
}

function fileSize(path: string): number | null {
  if (!existsSync(resolve(root, path))) return null
  return statSync(resolve(root, path)).size
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function readJsonl<T>(path: string): T[] {
  const text = readFileSync(resolve(root, path), 'utf8').trim()
  if (text.length === 0) return []
  return text.split(/\r?\n/).map((line) => JSON.parse(line) as T)
}

function toEfficiencyRecord(task: LocalBenchmarkTaskResult): BenchmarkEfficiencyRecord {
  return {
    benchmarkTaskId: task.benchmarkTaskId,
    benchmarkFamily: task.benchmarkFamily,
    localHarnessStatus: task.localHarnessStatus,
    localOutcomeForReplayOnly: task.terminalOutcomeClass,
    sourceEvidencePath: task.sourceEvidencePath,
    sourceEvidenceSha256: task.actualSourceEvidenceSha256,
    sourceEvidenceSizeBytes: fileSize(task.sourceEvidencePath),
    sourceEvidenceLineCount: fileLineCount(task.sourceEvidencePath),
    comparableMetricFields: {
      agent: 'openclaude_local_no_provider',
      model: null,
      inputTokens: null,
      outputTokens: null,
      costUsd: null,
      numTurns: null,
      durationMs: null,
      resolved: null,
    },
    metricAvailability: {
      tokenUsageMeasured: false,
      costMeasured: false,
      durationMeasured: false,
      turnCountMeasured: false,
      externalResolvedMeasured: false,
    },
    metricGapStatus: 'classified_unresolved_external_or_live_run_required',
    protectedActionExecuted: false,
    externalBenchmarkResultClaimed: false,
  }
}

function writeMarkdown(report: BenchmarkEfficiencyMetricsReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`)
    .join('\n')
  const metricRows = report.benchmarkEfficiencyRecords
    .map((record) => `| \`${record.benchmarkTaskId}\` | \`${record.localHarnessStatus}\` | \`${record.localOutcomeForReplayOnly}\` | \`${record.sourceEvidenceLineCount ?? 'missing'}\` | \`${record.metricGapStatus}\` |`)
    .join('\n')
  const gapRows = report.unresolvedMetricGaps
    .map((gap) => `| \`${gap.id}\` | \`${gap.status}\` | \`${gap.protectedActionRequired}\` | \`${gap.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.efficiencyChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Benchmark Efficiency Metrics Report

Generated by: \`bun run product:benchmark-efficiency-metrics\`

## Claim Boundary

- This is a local no-provider benchmark efficiency schema and gap report.
- It imports OpenClaude's local benchmark replay results and adds explicit cost, token, turn, duration, and external-resolution fields as null/classified gaps.
- It does not run SWE-bench, Vexp SWE-bench, OpenHands benchmarks, providers, live models, external services, containers, hosted CI, deploy, publish, launch, or external benchmark evaluation.
- It does not claim external benchmark results, cost efficiency, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- source_local_benchmark_results_path: \`${report.sourceLocalBenchmarkResultsPath}\`
- source_local_benchmark_results_sha256: \`${report.sourceLocalBenchmarkResultsSha256}\`
- metrics_jsonl_path: \`${report.metricsJsonlPath}\`
- metrics_jsonl_sha256: \`${report.metricsJsonlSha256}\`
- comparable_record_count: \`${report.summary.comparableRecordCount}\`
- records_with_comparable_metric_fields: \`${report.summary.recordsWithComparableMetricFields}\`
- records_with_measured_token_cost_duration: \`${report.summary.recordsWithMeasuredTokenCostDuration}\`
- classified_metric_gap_count: \`${report.summary.classifiedMetricGapCount}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${sourceRows}

## Metric Schema Fields

${report.metricSchemaFields.map((field) => `- \`${field}\``).join('\n')}

## Local Metric Records

| Task | Harness Status | Local Outcome Only | Source Lines | Metric Gap |
| --- | --- | --- | ---: | --- |
${metricRows}

## Unresolved Metric Gaps

| Gap | Status | Protected Action Required | Protected Action Executed |
| --- | --- | --- | --- |
${gapRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'benchmark-efficiency-metrics-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const harness = readJson<LocalBenchmarkHarnessReport>(sourceHarnessPath)
  const sourceResults = readJsonl<LocalBenchmarkTaskResult>(harness.localBenchmarkResultPath)
  const records = sourceResults.map(toEfficiencyRecord)
  const metricsJsonl = `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, metricsJsonlPath), metricsJsonl)
  const metricsJsonlSha256 = sha256Text(metricsJsonl)
  const metricSchemaFields = [
    'benchmarkTaskId',
    'agent',
    'model',
    'inputTokens',
    'outputTokens',
    'costUsd',
    'numTurns',
    'durationMs',
    'resolved',
    'sourceEvidenceSha256',
  ]
  const unresolvedMetricGaps: BenchmarkEfficiencyMetricsReport['unresolvedMetricGaps'] = [
    'provider_token_accounting',
    'cost_model_or_billing_source',
    'wall_clock_duration_measurement',
    'agentic_turn_count_measurement',
    'external_same_task_resolution_evaluation',
    'unique_win_comparison_dataset',
  ].map((id) => ({
    id,
    status: 'classified_unresolved',
    requiredBeforeExternalComparisonClaim: true,
    protectedActionRequired: true,
    protectedActionExecuted: false,
  }))

  const summary = {
    sourceTaskCount: harness.localBenchmarkTaskResults.length,
    comparableRecordCount: records.length,
    recordsWithComparableMetricFields: records.filter((record) => Object.keys(record.comparableMetricFields).length === 8).length,
    recordsWithMeasuredTokenCostDuration: records.filter(
      (record) => record.metricAvailability.tokenUsageMeasured || record.metricAvailability.costMeasured || record.metricAvailability.durationMeasured,
    ).length,
    classifiedMetricGapCount: records.filter((record) => record.metricGapStatus === 'classified_unresolved_external_or_live_run_required').length,
  }

  const checks = [
    check('local benchmark harness is imported', harness.mode === 'local_no_provider_benchmark_replay_harness', harness.mode),
    check('source result hash matches harness report', sha256Text(readFileSync(resolve(root, harness.localBenchmarkResultPath), 'utf8')) === harness.localBenchmarkResultSha256, harness.localBenchmarkResultPath),
    check('one efficiency record exists per local benchmark task', records.length === harness.localBenchmarkTaskResults.length, `${records.length}/${harness.localBenchmarkTaskResults.length}`),
    check('all records carry benchmark-comparable metric fields', summary.recordsWithComparableMetricFields === records.length, `${summary.recordsWithComparableMetricFields}/${records.length}`),
    check('cost token duration metrics are classified as unmeasured in no-provider mode', summary.recordsWithMeasuredTokenCostDuration === 0, `${summary.recordsWithMeasuredTokenCostDuration} measured`),
    check('metric gaps are classified for every record', summary.classifiedMetricGapCount === records.length, `${summary.classifiedMetricGapCount}/${records.length}`),
    check('unresolved metric gaps require later authorization', unresolvedMetricGaps.length >= 5 && unresolvedMetricGaps.every((gap) => gap.requiredBeforeExternalComparisonClaim && gap.protectedActionRequired && gap.protectedActionExecuted === false), `${unresolvedMetricGaps.length} gaps`),
    check('metrics JSONL hash is recorded', metricsJsonlSha256.length === 64, metricsJsonlPath),
    check('records execute no protected action or external benchmark claim', records.every((record) => !record.protectedActionExecuted && !record.externalBenchmarkResultClaimed), 'all false'),
  ]

  const report: BenchmarkEfficiencyMetricsReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_benchmark_efficiency_metrics',
    sourceLocalBenchmarkHarnessPath: sourceHarnessPath,
    sourceLocalBenchmarkResultsPath: harness.localBenchmarkResultPath,
    sourceLocalBenchmarkResultsSha256: harness.localBenchmarkResultSha256,
    primarySourceInputs: [
      {
        sourceProject: 'Vexp-ai/vexp-swe-bench',
        sourceUrl: 'https://github.com/Vexp-ai/vexp-swe-bench',
        observedPattern: 'Coding-agent benchmark results should preserve pass@1, cost per task, duration, token usage, and unique-win comparison fields rather than only final pass/fail status.',
      },
      {
        sourceProject: 'SWE-bench/SWE-bench',
        sourceUrl: 'https://github.com/swe-bench/SWE-bench',
        observedPattern: 'Issue-resolution benchmarks need per-instance result records that can be evaluated later without collapsing setup and result claims.',
      },
      {
        sourceProject: 'OpenHands/benchmarks',
        sourceUrl: 'https://github.com/OpenHands/benchmarks',
        observedPattern: 'Agent benchmark evidence should preserve structured task records and explicit runtime boundaries before stronger public comparisons.',
      },
    ],
    metricSchemaFields,
    metricsJsonlPath,
    metricsJsonlSha256,
    benchmarkEfficiencyRecords: records,
    summary,
    unresolvedMetricGaps,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    externalBenchmarkExecutionPerformed: false,
    externalBenchmarkResultClaimed: false,
    externalComparisonClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    efficiencyChecks: checks,
    claimBoundary: 'Benchmark efficiency metrics are local no-provider schema/gap evidence only. They do not claim external benchmark performance, cost efficiency, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeFileSync(resolve(docsDir, 'benchmark-efficiency-metrics-report.json'), `${JSON.stringify(report, null, 2)}\n`)
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
  console.log(`metrics_jsonl_path=${metricsJsonlPath}`)
  console.log(`benchmark_efficiency_records=${records.length}`)
  console.log(`measured_token_cost_duration_records=${summary.recordsWithMeasuredTokenCostDuration}`)
  console.log(`classified_metric_gap_count=${summary.classifiedMetricGapCount}`)
  console.log(`external_comparison_claim_allowed=${report.externalComparisonClaimAllowed}`)
}

main()
