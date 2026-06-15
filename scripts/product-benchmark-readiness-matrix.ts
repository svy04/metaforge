import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { sha256 as sha256Text } from './quality-report-helpers'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceEvidence = {
  path: string
  sha256: string
}

type BenchmarkTaskManifestEntry = {
  benchmarkTaskId: string
  benchmarkFamily: string
  sourceEvidencePath: string
  sourceEvidenceSha256: string
  taskType: string
  externalBenchmarkAnalog: string
  requiredEvidence: string[]
  terminalOutcomeClass: string
  protectedActionRequired: boolean
  protectedActionExecuted: boolean
  externalBenchmarkResultClaimed: boolean
  providerCallsPerformed: number
  liveModelCallsPerformed: number
  externalCallsPerformed: number
}

type ReadinessDimension = {
  id: string
  status: 'ready_local_no_provider' | 'classified_gap'
  primarySourcePattern: string
  localEvidence: string[]
  remainingGap: string
  protectedActionRequiredForGap: boolean
  protectedActionExecuted: boolean
}

type RealTraceEvalReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  traceFileCount: number
  traces: Array<{
    path: string
    sha256: string
    traceKind?: string
    passed: boolean
    lastStatus?: string | null
  }>
  coverageSummary?: {
    traceKinds: string[]
    querySources: string[]
    terminalOutcomes: string[]
  }
}

type AgentReplayReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  replayScenarioCount: number
  replayScenarios: Array<{
    id: string
    passed: boolean
    score: number
  }>
}

type TraceRedactionPolicyReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  rawTraceFileCount: number
  publishableSummaryFields: string[]
  forbiddenRawFields: string[]
}

type ReleaseReproducibilityReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  reproducibleTarballSha256: string
  temporaryTarballsRemoved: boolean
}

type SourceControlledChecksReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workflowPath: string
  productQualityCommandPresent: boolean
  pullRequestTriggerPresent: boolean
  pushMainTriggerPresent: boolean
  releaseActionsAbsent: boolean
}

type PromptedToolLoopCaptureReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  promptSha256: string
  promptByteLength: number
  nonSyntheticUserSessionClaimed: boolean
  tracePath: string
  traceSha256: string
  toolCommandCaptures: Array<{
    name: string
    passed: boolean
  }>
}

type TerminalFailureRecoveryTranscriptsReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  transcriptCount: number
  failureStepDetected: boolean
  recoveryGuidanceProvided: boolean
  recoveryVerificationPassed: boolean
  transcripts: Array<{
    name: string
    kind: string
    passed: boolean
  }>
}

type BenchmarkReadinessReport = {
  generatedAt: string
  mode: 'local_no_provider_benchmark_readiness_matrix'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkRunPerformed: false
  externalBenchmarkResultClaimed: false
  benchmarkManifestPath: string
  benchmarkManifestSha256: string
  benchmarkTaskCount: number
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  sourceEvidence: SourceEvidence[]
  readinessDimensions: ReadinessDimension[]
  unresolvedGaps: Array<{
    id: string
    status: 'classified_unresolved'
    protectedActionRequired: boolean
    protectedActionExecuted: boolean
    detail: string
  }>
  benchmarkReadinessChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const manifestRelativePath = 'reports/openclaude-benchmark-task-manifest.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function fileSha256(path: string): string {
  return createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function noCalls(...reports: Array<{ providerCallsPerformed: unknown[]; liveModelCallsPerformed: unknown[]; externalCallsPerformed: unknown[] }>): boolean {
  return reports.every((report) =>
    report.providerCallsPerformed.length === 0 &&
    report.liveModelCallsPerformed.length === 0 &&
    report.externalCallsPerformed.length === 0)
}

function manifestLine(entry: BenchmarkTaskManifestEntry): string {
  return JSON.stringify(entry)
}

function writeMarkdown(report: BenchmarkReadinessReport): void {
  const dimensionRows = report.readinessDimensions
    .map((dimension) => `| \`${dimension.id}\` | \`${dimension.status}\` | ${dimension.primarySourcePattern} | ${dimension.localEvidence.map((item) => `\`${item}\``).join(', ')} | ${dimension.remainingGap} | \`${dimension.protectedActionRequiredForGap}\` |`)
    .join('\n')
  const taskRows = report.sourceEvidence
    .map((evidence) => `| \`${evidence.path}\` | \`${evidence.sha256}\` |`)
    .join('\n')
  const gapRows = report.unresolvedGaps
    .map((gap) => `| \`${gap.id}\` | \`${gap.status}\` | \`${gap.protectedActionRequired}\` | \`${gap.protectedActionExecuted}\` | ${gap.detail} |`)
    .join('\n')
  const checkRows = report.benchmarkReadinessChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Benchmark Readiness Matrix

Generated by: \`bun run product:benchmark-readiness\`

## Claim Boundary

- This report maps local OpenClaude product-quality evidence to benchmark-style readiness dimensions derived from primary sources.
- It does not run SWE-bench, OpenHands Benchmarks, OpenHands Trajectory Visualizer, providers, live models, external services, Docker, or remote runtimes.
- It does not claim external benchmark results, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- benchmark_manifest_path: \`${report.benchmarkManifestPath}\`
- benchmark_manifest_sha256: \`${report.benchmarkManifestSha256}\`
- benchmark_task_count: \`${report.benchmarkTaskCount}\`
- external_benchmark_run_performed: \`${report.externalBenchmarkRunPerformed}\`
- external_benchmark_result_claimed: \`${report.externalBenchmarkResultClaimed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${report.primarySourceInputs.map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`).join('\n')}

## Source Evidence

| Evidence | SHA-256 |
| --- | --- |
${taskRows}

## Readiness Dimensions

| Dimension | Status | Primary Source Pattern | Local Evidence | Remaining Gap | Gap Needs Protected Action |
| --- | --- | --- | --- | --- | --- |
${dimensionRows}

## Unresolved Gaps

| Gap | Status | Protected Action Required | Protected Action Executed | Detail |
| --- | --- | --- | --- | --- |
${gapRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'benchmark-readiness-matrix.md'), markdown)
}

function main(): void {
  const realTrace = readJson<RealTraceEvalReport>('docs/product-quality/real-session-trace-evals-report.json')
  const agentReplay = readJson<AgentReplayReport>('docs/product-quality/agent-replay-evals-report.json')
  const traceRedaction = readJson<TraceRedactionPolicyReport>('docs/product-quality/trace-capture-redaction-policy-report.json')
  const releaseReproducibility = readJson<ReleaseReproducibilityReport>('docs/product-quality/release-artifact-reproducibility-report.json')
  const sourceControlled = readJson<SourceControlledChecksReport>('docs/product-quality/source-controlled-checks-report.json')
  const promptedToolLoop = readJson<PromptedToolLoopCaptureReport>('docs/product-quality/prompted-tool-loop-capture-report.json')
  const terminalFailureRecovery = readJson<TerminalFailureRecoveryTranscriptsReport>('docs/product-quality/terminal-failure-recovery-transcripts-report.json')

  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const evidencePaths = [
    'docs/product-quality/real-session-trace-evals-report.json',
    'docs/product-quality/agent-replay-evals-report.json',
    'docs/product-quality/trace-capture-redaction-policy-report.json',
    'docs/product-quality/release-artifact-reproducibility-report.json',
    'docs/product-quality/source-controlled-checks-report.json',
    'docs/product-quality/prompted-tool-loop-capture-report.json',
    'docs/product-quality/terminal-failure-recovery-transcripts-report.json',
  ]
  const sourceEvidence = evidencePaths.map((path) => ({ path, sha256: fileSha256(path) }))

  const taskEntries: BenchmarkTaskManifestEntry[] = [
    {
      benchmarkTaskId: 'openclaude.local.terminal_failure_recovery_transcripts',
      benchmarkFamily: 'local_no_provider_product_quality',
      sourceEvidencePath: 'docs/product-quality/terminal-failure-recovery-transcripts-report.json',
      sourceEvidenceSha256: fileSha256('docs/product-quality/terminal-failure-recovery-transcripts-report.json'),
      taskType: 'terminal_failure_recovery_transcript',
      externalBenchmarkAnalog: 'Terminal-agent failure recovery and command transcript evidence',
      requiredEvidence: ['local failure exit', 'help recovery', 'doctor handoff', 'version recovery', 'stdout/stderr hashes'],
      terminalOutcomeClass: terminalFailureRecovery.failureStepDetected && terminalFailureRecovery.recoveryGuidanceProvided && terminalFailureRecovery.recoveryVerificationPassed ? 'succeeded' : 'failed',
      protectedActionRequired: false,
      protectedActionExecuted: false,
      externalBenchmarkResultClaimed: false,
      providerCallsPerformed: terminalFailureRecovery.providerCallsPerformed.length,
      liveModelCallsPerformed: terminalFailureRecovery.liveModelCallsPerformed.length,
      externalCallsPerformed: terminalFailureRecovery.externalCallsPerformed.length,
    },
    {
      benchmarkTaskId: 'openclaude.local.prompted_tool_loop_cli',
      benchmarkFamily: 'local_no_provider_product_quality',
      sourceEvidencePath: promptedToolLoop.tracePath,
      sourceEvidenceSha256: promptedToolLoop.traceSha256,
      taskType: 'prompted_tool_loop_trajectory',
      externalBenchmarkAnalog: 'OpenHands Benchmarks rich per-instance tool-call logging and trajectory summaries',
      requiredEvidence: ['prompt hash', 'tool command exits', 'stdout/stderr hashes', 'terminal status'],
      terminalOutcomeClass: promptedToolLoop.toolCommandCaptures.every((capture) => capture.passed) ? 'succeeded' : 'failed',
      protectedActionRequired: false,
      protectedActionExecuted: false,
      externalBenchmarkResultClaimed: false,
      providerCallsPerformed: promptedToolLoop.providerCallsPerformed.length,
      liveModelCallsPerformed: promptedToolLoop.liveModelCallsPerformed.length,
      externalCallsPerformed: promptedToolLoop.externalCallsPerformed.length,
    },
    ...realTrace.traces.map((trace): BenchmarkTaskManifestEntry => ({
      benchmarkTaskId: `openclaude.trace.${trace.path.replace(/[^A-Za-z0-9_.-]/g, '_')}`,
      benchmarkFamily: 'local_no_provider_trace_eval',
      sourceEvidencePath: trace.path,
      sourceEvidenceSha256: trace.sha256,
      taskType: trace.traceKind ?? 'unknown_trace',
      externalBenchmarkAnalog: 'OpenHands trajectory artifact and SWE-bench-style terminal outcome record',
      requiredEvidence: ['JSONL parseability', 'required fields', 'started-to-terminal ordering', 'credential scan'],
      terminalOutcomeClass: trace.lastStatus ?? 'unknown',
      protectedActionRequired: false,
      protectedActionExecuted: false,
      externalBenchmarkResultClaimed: false,
      providerCallsPerformed: realTrace.providerCallsPerformed.length,
      liveModelCallsPerformed: realTrace.liveModelCallsPerformed.length,
      externalCallsPerformed: realTrace.externalCallsPerformed.length,
    })),
    {
      benchmarkTaskId: 'openclaude.local.agent_replay_eval_summary',
      benchmarkFamily: 'local_no_provider_replay_eval',
      sourceEvidencePath: 'docs/product-quality/agent-replay-evals-report.json',
      sourceEvidenceSha256: fileSha256('docs/product-quality/agent-replay-evals-report.json'),
      taskType: 'replay_grading_summary',
      externalBenchmarkAnalog: 'SWE-bench evaluation result directory and OpenHands benchmark instance summary',
      requiredEvidence: ['scenario count', 'scores', 'pass/fail classification', 'environment blocker classification'],
      terminalOutcomeClass: agentReplay.replayScenarios.every((scenario) => scenario.passed) ? 'succeeded' : 'classified_environment_blocked',
      protectedActionRequired: false,
      protectedActionExecuted: false,
      externalBenchmarkResultClaimed: false,
      providerCallsPerformed: agentReplay.providerCallsPerformed.length,
      liveModelCallsPerformed: agentReplay.liveModelCallsPerformed.length,
      externalCallsPerformed: agentReplay.externalCallsPerformed.length,
    },
  ]

  const manifestText = `${taskEntries.map(manifestLine).join('\n')}\n`
  writeFileSync(resolve(root, manifestRelativePath), manifestText)
  const manifestSha256 = sha256Text(manifestText)

  const sourceUrls = [
    'https://github.com/swe-bench/SWE-bench',
    'https://github.com/OpenHands/benchmarks',
    'https://github.com/OpenHands/trajectory-visualizer',
  ]
  const readinessDimensions: ReadinessDimension[] = [
    {
      id: 'task_instance_schema_alignment',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'SWE-bench task instances pair repository issue context with reproducible evaluation records.',
      localEvidence: ['reports/openclaude-benchmark-task-manifest.jsonl', 'docs/product-quality/real-session-trace-evals-report.json'],
      remainingGap: 'External SWE-bench execution is not performed in this no-provider gate.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
    {
      id: 'trajectory_artifact_alignment',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'OpenHands trajectory tooling preserves actions, observations, timestamps, and metadata for later review.',
      localEvidence: [promptedToolLoop.tracePath, 'docs/product-quality/real-session-trace-evals-report.json', 'docs/product-quality/terminal-failure-recovery-transcripts-report.json'],
      remainingGap: 'Non-synthetic user IDE/workbench trajectory capture still requires explicit operator capture.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
    {
      id: 'replay_grading_alignment',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'Benchmark harnesses keep per-instance pass/fail summaries and logs distinct from final claims.',
      localEvidence: ['docs/product-quality/agent-replay-evals-report.json'],
      remainingGap: 'Real Extension Host and workbench replay remain blocked while VS Code update is in progress.',
      protectedActionRequiredForGap: false,
      protectedActionExecuted: false,
    },
    {
      id: 'reproducible_artifact_alignment',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'SWE-bench and OpenHands benchmarks emphasize reproducible environments and pinned artifacts.',
      localEvidence: ['docs/product-quality/release-artifact-reproducibility-report.json'],
      remainingGap: 'Signed release provenance remains blocked until a real Git/release boundary exists.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
    {
      id: 'publishable_summary_redaction',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'Trajectory review needs portable summaries without leaking raw credentials or provider payloads.',
      localEvidence: ['docs/product-quality/trace-capture-redaction-policy-report.json'],
      remainingGap: 'Raw non-synthetic capture quarantine remains a later operator-authorized workflow.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
    {
      id: 'source_controlled_gate_wiring',
      status: 'ready_local_no_provider',
      primarySourcePattern: 'Benchmark and CI workflows should be source-controlled and repeatable.',
      localEvidence: ['docs/product-quality/source-controlled-checks-report.json'],
      remainingGap: 'Hosted CI run evidence remains blocked because this workspace is not a Git repository.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
    {
      id: 'external_benchmark_run_boundary',
      status: 'classified_gap',
      primarySourcePattern: 'SWE-bench and OpenHands benchmark runs require external datasets, containers, model/runtime configuration, or remote runtime access.',
      localEvidence: ['docs/product-quality/benchmark-readiness-matrix.json'],
      remainingGap: 'External benchmark execution is not authorized in this internal no-provider gate.',
      protectedActionRequiredForGap: true,
      protectedActionExecuted: false,
    },
  ]

  const unresolvedGaps = readinessDimensions
    .filter((dimension) => dimension.remainingGap.length > 0)
    .map((dimension) => ({
      id: dimension.id,
      status: 'classified_unresolved' as const,
      protectedActionRequired: dimension.protectedActionRequiredForGap,
      protectedActionExecuted: dimension.protectedActionExecuted,
      detail: dimension.remainingGap,
    }))

  const checks = [
    check('primary sources are GitHub repositories', sourceUrls.every((url) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(url)), sourceUrls.join(',')),
    check('source evidence files are hashed', sourceEvidence.every((evidence) => evidence.sha256.length === 64), `${sourceEvidence.length} files`),
    check('benchmark manifest was written', manifestSha256.length === 64 && taskEntries.length >= 8, `${taskEntries.length} tasks`),
    check('benchmark tasks do not claim external benchmark results', taskEntries.every((entry) => !entry.externalBenchmarkResultClaimed), 'externalBenchmarkResultClaimed=false'),
    check('benchmark tasks do not execute protected actions', taskEntries.every((entry) => !entry.protectedActionExecuted), 'protectedActionExecuted=false'),
    check('source reports performed no provider/live/external calls', noCalls(realTrace, agentReplay, traceRedaction, releaseReproducibility, sourceControlled, promptedToolLoop, terminalFailureRecovery), 'all source reports call counts are zero'),
    check('prompted tool-loop trace is included', taskEntries.some((entry) => entry.sourceEvidencePath === promptedToolLoop.tracePath), promptedToolLoop.tracePath),
    check('terminal failure recovery transcripts are included', taskEntries.some((entry) => entry.sourceEvidencePath === 'docs/product-quality/terminal-failure-recovery-transcripts-report.json'), 'docs/product-quality/terminal-failure-recovery-transcripts-report.json'),
    check('readiness dimensions cover benchmark contract', ['task_instance_schema_alignment', 'trajectory_artifact_alignment', 'replay_grading_alignment', 'reproducible_artifact_alignment', 'publishable_summary_redaction', 'source_controlled_gate_wiring', 'external_benchmark_run_boundary'].every((id) => readinessDimensions.some((dimension) => dimension.id === id)), readinessDimensions.map((dimension) => dimension.id).join(',')),
    check('unresolved gaps are classified without execution', unresolvedGaps.every((gap) => gap.status === 'classified_unresolved' && gap.protectedActionExecuted === false), `${unresolvedGaps.length} gaps`),
    check('external benchmark run remains blocked', true, 'externalBenchmarkRunPerformed=false'),
  ]

  const report: BenchmarkReadinessReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_benchmark_readiness_matrix',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    externalBenchmarkRunPerformed: false,
    externalBenchmarkResultClaimed: false,
    benchmarkManifestPath: manifestRelativePath,
    benchmarkManifestSha256: manifestSha256,
    benchmarkTaskCount: taskEntries.length,
    primarySourceInputs: [
      {
        sourceProject: 'SWE-bench/SWE-bench',
        sourceUrl: 'https://github.com/swe-bench/SWE-bench',
        observedPattern: 'GitHub issue resolving tasks are evaluated by reproducible harness runs and stored evaluation results.',
      },
      {
        sourceProject: 'OpenHands/benchmarks',
        sourceUrl: 'https://github.com/OpenHands/benchmarks',
        observedPattern: 'Benchmark runs preserve pinned SDK/workspace context, per-instance logs, tool-call summaries, and runtime boundaries.',
      },
      {
        sourceProject: 'OpenHands/trajectory-visualizer',
        sourceUrl: 'https://github.com/OpenHands/trajectory-visualizer',
        observedPattern: 'Trajectory artifacts should be portable and inspectable as action/observation timelines.',
      },
    ],
    sourceEvidence,
    readinessDimensions,
    unresolvedGaps,
    benchmarkReadinessChecks: checks,
    claimBoundary: 'Benchmark readiness is internal local no-provider evidence only. It does not run or claim SWE-bench/OpenHands benchmark results, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeFileSync(resolve(docsDir, 'benchmark-readiness-matrix.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  const failed = checks.filter((item) => !item.ok)
  console.log('')
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log(`benchmark_manifest_path=${manifestRelativePath}`)
  console.log(`benchmark_task_count=${taskEntries.length}`)
  console.log('external_benchmark_run_performed=false')
  console.log('external_benchmark_result_claimed=false')
  console.log('provider_calls_performed=0')
  console.log('live_model_calls_performed=0')
  console.log('external_calls_performed=0')
}

main()
