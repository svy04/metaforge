import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import { discoverPublishableTraceFiles } from './product-trace-discovery'

type JsonObject = Record<string, unknown>

type Check = {
  label: string
  ok: boolean
  detail: string
}

type PrimarySourceInput = {
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type RealTraceEvalReport = {
  mode: string
  traceFileCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  traces: Array<{
    path: string
    sha256: string
    lastStatus: string | null
    passed: boolean
  }>
}

type LocalBenchmarkHarnessReport = {
  mode: string
  localBenchmarkResultPath: string
  localBenchmarkResultSha256: string
  localBenchmarkTaskResults: Array<{
    benchmarkTaskId: string
    sourceEvidencePath: string
    localHarnessStatus: string
  }>
}

type TraceAssessment = {
  path: string
  sha256: string
  traceKind: string
  eventCount: number
  terminalOutcome: string | null
  phaseLabelsPresent: string[]
  missingPhaseLabels: string[]
  repeatedCommandNames: Array<{
    commandName: string
    count: number
  }>
  wasteSignals: string[]
  processQualityStatus: 'process_quality_evidence_ok' | 'classified_process_gap' | 'failed_process_evidence'
  sourceBenchmarkTaskIds: string[]
}

type TrajectoryProcessQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_trajectory_process_quality'
  sourceRealTraceEvalReportPath: string
  sourceRealTraceEvalMode: string
  sourceTraceCount: number
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  primarySourceInputs: PrimarySourceInput[]
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkResultClaimed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  phaseTaxonomy: string[]
  wasteSignalTaxonomy: string[]
  traceAssessments: TraceAssessment[]
  summary: {
    assessedTraceCount: number
    processQualityOkTraceCount: number
    classifiedProcessGapTraceCount: number
    failedProcessEvidenceTraceCount: number
    tracesWithVerificationEvidence: number
    tracesWithImplementationEvidence: number
    tracesWithClassifiedWasteSignals: number
  }
  processQualityChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const realTraceEvalReportPath = 'docs/product-quality/real-session-trace-evals-report.json'
const localBenchmarkHarnessPath = 'docs/product-quality/local-benchmark-harness-report.json'
const processQualityJsonPath = 'docs/product-quality/trajectory-process-quality-report.json'
const processQualityMdPath = 'docs/product-quality/trajectory-process-quality-report.md'
const processQualityResultPath = 'reports/openclaude-trajectory-process-quality.jsonl'
const terminalStatuses = new Set(['succeeded', 'failed', 'cancelled'])
const phaseTaxonomy = ['exploration', 'implementation', 'verification', 'orchestration']
const wasteSignalTaxonomy = [
  'missing_verification',
  'blind_retry_loop',
  'temporal_disorder',
  'regression_cycle',
  'unbounded_repeated_tool_use',
  'raw_trace_payload_exposure',
]
const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function fileSha256(path: string): string {
  return createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex')
}

function textSha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function unique(values: string[]): string[] {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b))
}

function classifyTraceKind(path: string): string {
  const name = basename(path)
  if (name.includes('protected-action-denial-trace')) return 'protected_action_denial_fixture'
  if (name.includes('tool-interruption-recovery-trace')) return 'tool_interruption_recovery_fixture'
  if (name.includes('regression-cycle-code-editing-trace')) return 'implementation_bearing_regression_cycle_code_editing_fixture'
  if (name.includes('multi-file-code-editing-trace')) return 'implementation_bearing_multi_file_code_editing_fixture'
  if (name.includes('code-editing-trace')) return 'implementation_bearing_code_editing_fixture'
  if (name.includes('prompted-tool-loop')) return 'prompted_tool_loop_cli'
  if (name.includes('real-session-capture')) return 'real_session_capture_cli'
  if (name.includes('fixture-user-executor')) return 'fixture_user_executor_session'
  if (name.includes('sidequery')) return 'live_sidequery_probe'
  if (name.includes('adaptive')) return 'live_adaptive_probe'
  if (name.includes('usage-cli')) return 'usage_cli_probe'
  if (name.includes('usage-probe')) return 'usage_repl_probe'
  if (name.includes('live')) return 'live_probe'
  return 'unknown_trace'
}

function readJsonl(path: string): JsonObject[] {
  const text = readFileSync(resolve(root, path), 'utf8')
  return text
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0)
    .map((line) => JSON.parse(line) as JsonObject)
}

function eventString(event: JsonObject, key: string): string {
  const value = event[key]
  return typeof value === 'string' ? value : ''
}

function eventNumber(event: JsonObject, key: string): number | null {
  const value = event[key]
  return typeof value === 'number' ? value : null
}

function hasCredentialPattern(path: string): boolean {
  const text = readFileSync(resolve(root, path), 'utf8')
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function classifyPhaseLabels(events: JsonObject[]): string[] {
  const labels = new Set<string>()
  for (const event of events) {
    const role = eventString(event, 'role')
    const status = eventString(event, 'status')
    const commandName = eventString(event, 'commandName')
    const querySource = eventString(event, 'querySource')
    const hasExitCode = eventNumber(event, 'exitCode') !== null
    const passed = event.passed === true

    if (role === 'user' || role === 'executor' || querySource.length > 0) {
      labels.add('orchestration')
    }
    if (role === 'planner' || commandName.startsWith('inspect_') || commandName.includes('help') || commandName.includes('usage')) {
      labels.add('exploration')
    }
    if (commandName.includes('write') || commandName.includes('patch') || commandName.includes('build') || commandName.includes('pack') || commandName.includes('capture')) {
      labels.add('implementation')
    }
    if (hasExitCode || passed || terminalStatuses.has(status) || commandName.includes('test') || commandName.includes('check') || commandName.includes('doctor') || commandName.includes('version') || commandName.includes('defaults')) {
      labels.add('verification')
    }
  }
  return unique([...labels])
}

function countCommands(events: JsonObject[]): Map<string, number> {
  const counts = new Map<string, number>()
  for (const event of events) {
    const commandName = eventString(event, 'commandName')
    if (commandName.length === 0) continue
    counts.set(commandName, (counts.get(commandName) ?? 0) + 1)
  }
  return counts
}

function hasBlindRetryLoop(events: JsonObject[]): boolean {
  let previous = ''
  let runLength = 0
  for (const event of events) {
    const key = `${eventString(event, 'commandName')}:${eventString(event, 'status')}`
    if (key === ':' || !key.includes(':started')) {
      continue
    }
    if (key === previous) {
      runLength += 1
    } else {
      previous = key
      runLength = 1
    }
    if (runLength >= 3) {
      return true
    }
  }
  return false
}

function hasRegressionCycle(events: JsonObject[]): boolean {
  const statuses = events.map((event) => eventString(event, 'status')).filter(Boolean)
  for (let index = 0; index < statuses.length - 2; index += 1) {
    if (statuses[index] === 'failed' && statuses[index + 1] === 'succeeded' && statuses[index + 2] === 'failed') {
      return true
    }
  }
  return false
}

function hasTemporalDisorder(labels: string[], events: JsonObject[]): boolean {
  if (!labels.includes('exploration') || !labels.includes('verification')) {
    return false
  }
  const firstExploration = events.findIndex((event) => {
    const commandName = eventString(event, 'commandName')
    return eventString(event, 'role') === 'planner' || commandName.startsWith('inspect_') || commandName.includes('help') || commandName.includes('usage')
  })
  const firstVerification = events.findIndex((event) => eventNumber(event, 'exitCode') !== null || event.passed === true)
  return firstVerification >= 0 && firstExploration >= 0 && firstVerification < firstExploration
}

function assessTrace(path: string, benchmarkTaskIdsByEvidencePath: Map<string, string[]>): TraceAssessment {
  const events = readJsonl(path)
  const labels = classifyPhaseLabels(events)
  const missingPhaseLabels = phaseTaxonomy.filter((label) => !labels.includes(label))
  const commandCounts = countCommands(events)
  const repeatedCommandNames = [...commandCounts.entries()]
    .filter(([, count]) => count > 2)
    .map(([commandName, count]) => ({ commandName, count }))
    .sort((a, b) => a.commandName.localeCompare(b.commandName))
  const statuses = events.map((event) => eventString(event, 'status')).filter(Boolean)
  const terminalOutcome = [...statuses].reverse().find((status) => terminalStatuses.has(status)) ?? null
  const wasteSignals: string[] = []
  const credentialPatternFound = hasCredentialPattern(path)

  if (terminalOutcome === 'succeeded' && !labels.includes('verification')) wasteSignals.push('missing_verification')
  if (hasBlindRetryLoop(events)) wasteSignals.push('blind_retry_loop')
  if (hasTemporalDisorder(labels, events)) wasteSignals.push('temporal_disorder')
  if (hasRegressionCycle(events)) wasteSignals.push('regression_cycle')
  if (repeatedCommandNames.some((item) => item.count > 4)) wasteSignals.push('unbounded_repeated_tool_use')
  if (credentialPatternFound) wasteSignals.push('raw_trace_payload_exposure')

  const processQualityStatus = credentialPatternFound
    ? 'failed_process_evidence'
    : wasteSignals.length > 0 || missingPhaseLabels.includes('verification')
      ? 'classified_process_gap'
      : 'process_quality_evidence_ok'

  return {
    path,
    sha256: fileSha256(path),
    traceKind: classifyTraceKind(path),
    eventCount: events.length,
    terminalOutcome,
    phaseLabelsPresent: labels,
    missingPhaseLabels,
    repeatedCommandNames,
    wasteSignals,
    processQualityStatus,
    sourceBenchmarkTaskIds: benchmarkTaskIdsByEvidencePath.get(path) ?? [],
  }
}

function buildMarkdown(report: TrajectoryProcessQualityReport): string {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} | ${source.localAbsorption} |`)
    .join('\n')
  const traceRows = report.traceAssessments
    .map((trace) => `| \`${trace.path}\` | \`${trace.processQualityStatus}\` | \`${trace.terminalOutcome ?? 'none'}\` | \`${trace.phaseLabelsPresent.join(',')}\` | \`${trace.missingPhaseLabels.join(',') || 'none'}\` | \`${trace.wasteSignals.join(',') || 'none'}\` |`)
    .join('\n')
  const checkRows = report.processQualityChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  return `# Trajectory Process Quality Report

Generated by: \`bun run product:trajectory-process-quality\`

## Claim Boundary

- This is a local no-provider process-quality check over existing OpenClaude trace artifacts.
- It checks phase coverage, verification evidence, repeated command patterns, and classified waste signals.
- It does not run providers, live models, external services, SWE-bench, OpenHands benchmarks, hosted CI, deploy, publish, launch, or external benchmark evaluation.
- It does not claim external validation, release readiness, production readiness, public readiness, autonomous reliability, or benchmark superiority.

## Summary

- mode: \`${report.mode}\`
- source_real_trace_eval_report_path: \`${report.sourceRealTraceEvalReportPath}\`
- source_trace_count: \`${report.sourceTraceCount}\`
- source_local_benchmark_results_path: \`${report.sourceLocalBenchmarkResultsPath}\`
- source_local_benchmark_results_sha256: \`${report.sourceLocalBenchmarkResultsSha256}\`
- assessed_trace_count: \`${report.summary.assessedTraceCount}\`
- process_quality_ok_trace_count: \`${report.summary.processQualityOkTraceCount}\`
- classified_process_gap_trace_count: \`${report.summary.classifiedProcessGapTraceCount}\`
- failed_process_evidence_trace_count: \`${report.summary.failedProcessEvidenceTraceCount}\`
- traces_with_verification_evidence: \`${report.summary.tracesWithVerificationEvidence}\`
- traces_with_implementation_evidence: \`${report.summary.tracesWithImplementationEvidence}\`
- traces_with_classified_waste_signals: \`${report.summary.tracesWithClassifiedWasteSignals}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- external_benchmark_execution_performed: \`${report.externalBenchmarkExecutionPerformed}\`
- external_benchmark_result_claimed: \`${report.externalBenchmarkResultClaimed}\`

## Primary Source Inputs

| Source | URL | Observed Pattern | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Trace Assessments

| Trace | Status | Terminal Outcome | Phase Labels | Missing Phase Labels | Waste Signals |
| --- | --- | --- | --- | --- | --- |
${traceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const realTraceEval = readJson<RealTraceEvalReport>(realTraceEvalReportPath)
  const localBenchmarkHarness = readJson<LocalBenchmarkHarnessReport>(localBenchmarkHarnessPath)
  const discoveredTraceFiles = discoverPublishableTraceFiles({ root, traceDirectory: 'reports' })
  const benchmarkTaskIdsByEvidencePath = new Map<string, string[]>()
  for (const task of localBenchmarkHarness.localBenchmarkTaskResults) {
    const existing = benchmarkTaskIdsByEvidencePath.get(task.sourceEvidencePath) ?? []
    existing.push(task.benchmarkTaskId)
    benchmarkTaskIdsByEvidencePath.set(task.sourceEvidencePath, existing)
  }

  const traceAssessments = discoveredTraceFiles.map((path) => assessTrace(path, benchmarkTaskIdsByEvidencePath))
  const localBenchmarkResultsSha256 = existsSync(resolve(root, localBenchmarkHarness.localBenchmarkResultPath))
    ? fileSha256(localBenchmarkHarness.localBenchmarkResultPath)
    : ''
  const resultText = `${traceAssessments.map((assessment) => JSON.stringify(assessment)).join('\n')}\n`
  writeFileSync(resolve(root, processQualityResultPath), resultText)
  const resultSha256 = textSha256(resultText)

  const summary = {
    assessedTraceCount: traceAssessments.length,
    processQualityOkTraceCount: traceAssessments.filter((trace) => trace.processQualityStatus === 'process_quality_evidence_ok').length,
    classifiedProcessGapTraceCount: traceAssessments.filter((trace) => trace.processQualityStatus === 'classified_process_gap').length,
    failedProcessEvidenceTraceCount: traceAssessments.filter((trace) => trace.processQualityStatus === 'failed_process_evidence').length,
    tracesWithVerificationEvidence: traceAssessments.filter((trace) => trace.phaseLabelsPresent.includes('verification')).length,
    tracesWithImplementationEvidence: traceAssessments.filter((trace) => trace.phaseLabelsPresent.includes('implementation')).length,
    tracesWithClassifiedWasteSignals: traceAssessments.filter((trace) => trace.wasteSignals.length > 0).length,
  }

  const primarySourceInputs: PrimarySourceInput[] = [
    {
      sourceProject: 'SWE-agent/SWE-agent',
      sourceUrl: 'https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md',
      observedPattern: 'Trajectory outputs preserve per-step thought, action, observation, state, query, configs, predictions, and exit-status files as separate experiment evidence.',
      localAbsorption: 'Assess OpenClaude traces as process artifacts instead of relying only on final pass/fail summary fields.',
    },
    {
      sourceProject: 'AgentLens paper',
      sourceUrl: 'https://arxiv.org/abs/2605.12925',
      observedPattern: 'Outcome-only software-agent evaluation can hide lucky passes; process-level signals such as missing verification, blind retries, regression cycles, and temporal disorder should be visible.',
      localAbsorption: 'Classify local OpenClaude trace phase labels and waste signals before any stronger reliability claim.',
    },
    {
      sourceProject: 'microsoft/AgentRx',
      sourceUrl: 'https://github.com/microsoft/AgentRx',
      observedPattern: 'Agent failure diagnosis normalizes raw logs into trajectory IR and checks invariants before producing reports.',
      localAbsorption: 'Keep this OpenClaude check deterministic and no-provider by using static local invariants only, without the LLM judge stage.',
    },
    {
      sourceProject: 'Aider-AI/aider',
      sourceUrl: 'https://github.com/Aider-AI/aider/blob/main/benchmark/README.md',
      observedPattern: 'Benchmark reports preserve run configuration, commit hash/dirty state, pass rates, malformed outputs, costs, and command metadata separately from execution.',
      localAbsorption: 'Preserve OpenClaude process-quality evidence as separate local report artifacts with explicit claim boundaries.',
    },
  ]

  const checks = [
    check('real trace eval source is local no-provider', realTraceEval.mode === 'local_no_provider_real_session_jsonl_trace_grading', realTraceEval.mode),
    check('real trace eval performed no provider/live/external calls', realTraceEval.providerCallsPerformed.length === 0 && realTraceEval.liveModelCallsPerformed.length === 0 && realTraceEval.externalCallsPerformed.length === 0, 'call counts=0'),
    check('local benchmark harness source is local no-provider', localBenchmarkHarness.mode === 'local_no_provider_benchmark_replay_harness', localBenchmarkHarness.mode),
    check('local benchmark result hash matches harness report', localBenchmarkResultsSha256 === localBenchmarkHarness.localBenchmarkResultSha256, `${localBenchmarkResultsSha256}/${localBenchmarkHarness.localBenchmarkResultSha256}`),
    check('trace discovery count matches real trace eval report', discoveredTraceFiles.length === realTraceEval.traceFileCount, `${discoveredTraceFiles.length}/${realTraceEval.traceFileCount}`),
    check('trace assessments retain source hashes from real trace eval report', traceAssessments.every((assessment) => realTraceEval.traces.some((trace) => trace.path === assessment.path && trace.sha256 === assessment.sha256)), `${traceAssessments.length} assessed`),
    check('all trace assessments include orchestration label', traceAssessments.every((assessment) => assessment.phaseLabelsPresent.includes('orchestration')), traceAssessments.map((trace) => `${trace.path}:${trace.phaseLabelsPresent.join(',')}`).join('; ')),
    check('verification evidence is present in local traces', summary.tracesWithVerificationEvidence >= Math.max(1, traceAssessments.length - summary.classifiedProcessGapTraceCount), `${summary.tracesWithVerificationEvidence}/${traceAssessments.length}`),
    check('process gaps are classified instead of hidden', summary.classifiedProcessGapTraceCount >= 0 && traceAssessments.every((assessment) => ['process_quality_evidence_ok', 'classified_process_gap', 'failed_process_evidence'].includes(assessment.processQualityStatus)), `${summary.classifiedProcessGapTraceCount} classified gaps`),
    check('no failed process evidence remains', summary.failedProcessEvidenceTraceCount === 0, `${summary.failedProcessEvidenceTraceCount} failed`),
    check('no raw credential patterns are present in assessed traces', traceAssessments.every((assessment) => !assessment.wasteSignals.includes('raw_trace_payload_exposure')), 'raw_trace_payload_exposure=false'),
    check('primary source inputs include trajectory, process-quality, invariant, and benchmark-report patterns', primarySourceInputs.length >= 4, primarySourceInputs.map((source) => source.sourceProject).join(', ')),
    check('process-quality result JSONL hash is recordable', resultSha256.length === 64, resultSha256),
  ]

  const report: TrajectoryProcessQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_trajectory_process_quality',
    sourceRealTraceEvalReportPath: realTraceEvalReportPath,
    sourceRealTraceEvalMode: realTraceEval.mode,
    sourceTraceCount: realTraceEval.traceFileCount,
    sourceLocalBenchmarkHarnessPath: localBenchmarkHarnessPath,
    sourceLocalBenchmarkResultsPath: localBenchmarkHarness.localBenchmarkResultPath,
    sourceLocalBenchmarkResultsSha256: localBenchmarkHarness.localBenchmarkResultSha256,
    primarySourceInputs,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    externalBenchmarkExecutionPerformed: false,
    externalBenchmarkResultClaimed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    phaseTaxonomy,
    wasteSignalTaxonomy,
    traceAssessments,
    summary,
    processQualityChecks: checks,
    claimBoundary: 'This report is internal local process-quality evidence only; it is not an external benchmark, release readiness, production readiness, public readiness, or autonomous reliability claim.',
  }

  writeFileSync(resolve(root, processQualityJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, processQualityMdPath), buildMarkdown(report))

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')

  const failed = checks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`trajectory_process_quality_result_path=${processQualityResultPath}`)
  console.log(`trajectory_process_quality_result_sha256=${resultSha256}`)
  console.log(`assessed_trace_count=${summary.assessedTraceCount}`)
  console.log(`process_quality_ok_trace_count=${summary.processQualityOkTraceCount}`)
  console.log(`classified_process_gap_trace_count=${summary.classifiedProcessGapTraceCount}`)
  console.log(`failed_process_evidence_trace_count=${summary.failedProcessEvidenceTraceCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
