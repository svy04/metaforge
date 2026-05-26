import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type BenchmarkReadinessReport = {
  mode: 'local_no_provider_benchmark_readiness_matrix'
  benchmarkManifestPath: string
  benchmarkManifestSha256: string
  benchmarkTaskCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkRunPerformed: false
  externalBenchmarkResultClaimed: false
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

type TracePortabilityExportReport = {
  mode: 'local_no_provider_trace_portability_export'
  portableTraceExportPath: string
  portableTraceExportSha256: string
  portableEventCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
}

type BenchmarkPolicyComplianceReport = {
  mode: 'local_no_provider_benchmark_policy_compliance'
  summary: {
    officialSWEbenchVerifiedSubmissionClaimAllowed: false
    officialLeaderboardClaimAllowed: false
  }
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  officialBenchmarkSubmissionPerformed: false
  externalBenchmarkExecutionPerformed: false
  externalLeaderboardClaimAllowed: false
}

type TerminalBenchRequirementStatus =
  | 'local_equivalent_available'
  | 'partial_local_equivalent_available'
  | 'classified_unresolved_protected_action_required'
  | 'blocked_not_authorized'

type TerminalBenchRequirementRecord = {
  requirementId: string
  terminalBenchRequirement: string
  readinessStatus: TerminalBenchRequirementStatus
  localEquivalentPath: string | null
  localEquivalentSha256: string | null
  officialRunRequired: boolean
  protectedActionRequiredToComplete: boolean
  protectedActionExecuted: false
  officialResultClaimed: false
  notes: string
}

type TerminalBenchReadinessReport = {
  generatedAt: string
  mode: 'local_no_provider_terminal_bench_readiness'
  sourceBenchmarkReadinessPath: string
  sourceBenchmarkTaskManifestPath: string
  sourceBenchmarkTaskManifestSha256: string
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  sourceTracePortabilityExportPath: string
  sourcePortableTraceJsonlPath: string
  sourcePortableTraceJsonlSha256: string
  sourceBenchmarkPolicyCompliancePath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  taskMapJsonlPath: string
  taskMapJsonlSha256: string
  terminalBenchRequirementRecords: TerminalBenchRequirementRecord[]
  summary: {
    requirementCount: number
    localEquivalentAvailableCount: number
    partialLocalEquivalentCount: number
    classifiedUnresolvedProtectedGapCount: number
    blockedNotAuthorizedCount: number
    officialTerminalBenchExecutionReady: false
  }
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  dockerContainerRunPerformed: false
  harborInstallPerformed: false
  officialTerminalBenchExecutionPerformed: false
  officialTerminalBenchResultClaimed: false
  officialLeaderboardSubmissionPerformed: false
  officialLeaderboardClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  terminalBenchReadinessChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceBenchmarkReadinessPath = 'docs/product-quality/benchmark-readiness-matrix.json'
const sourceLocalBenchmarkHarnessPath = 'docs/product-quality/local-benchmark-harness-report.json'
const sourceTracePortabilityExportPath = 'docs/product-quality/trace-portability-export-report.json'
const sourceBenchmarkPolicyCompliancePath = 'docs/product-quality/benchmark-policy-compliance-report.json'
const terminalBenchTaskMapJsonlPath = 'reports/openclaude-terminal-bench-task-map.jsonl'

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

function requirement(
  requirementId: string,
  terminalBenchRequirement: string,
  readinessStatus: TerminalBenchRequirementStatus,
  localEquivalentPath: string | null,
  notes: string,
): TerminalBenchRequirementRecord {
  const protectedGap =
    readinessStatus === 'classified_unresolved_protected_action_required' ||
    readinessStatus === 'blocked_not_authorized'

  return {
    requirementId,
    terminalBenchRequirement,
    readinessStatus,
    localEquivalentPath,
    localEquivalentSha256: fileSha256(localEquivalentPath),
    officialRunRequired: protectedGap,
    protectedActionRequiredToComplete: protectedGap,
    protectedActionExecuted: false,
    officialResultClaimed: false,
    notes,
  }
}

function buildRequirements(
  readiness: BenchmarkReadinessReport,
  harness: LocalBenchmarkHarnessReport,
  traces: TracePortabilityExportReport,
): TerminalBenchRequirementRecord[] {
  const hasTaskManifest = readiness.benchmarkTaskCount > 0 && fileSha256(readiness.benchmarkManifestPath) === readiness.benchmarkManifestSha256
  const hasLocalResults =
    harness.localBenchmarkTaskResults.length === readiness.benchmarkTaskCount &&
    harness.localBenchmarkTaskResults.every((task) => task.sourceEvidenceHashMatches)
  const hasPortableTrajectories = traces.portableEventCount > 0 && fileSha256(traces.portableTraceExportPath) === traces.portableTraceExportSha256

  return [
    requirement(
      'instruction_or_task_description',
      'Terminal-Bench task instruction or task.yaml description',
      hasTaskManifest ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      sourceBenchmarkReadinessPath,
      'Local benchmark readiness maps OpenClaude evidence-backed tasks, but it is not an official Terminal-Bench task.yaml corpus.',
    ),
    requirement(
      'docker_environment',
      'Dockerfile and docker-compose environment for each task',
      'classified_unresolved_protected_action_required',
      null,
      'Docker/Harbor runtime setup is a protected dependency/runtime boundary and was not installed or executed.',
    ),
    requirement(
      'tests_or_verifier',
      'run-tests.sh or Harbor tests/test.sh verifier',
      hasLocalResults ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      sourceLocalBenchmarkHarnessPath,
      'Local harness verifies source evidence hashes and status records, but it is not an official Terminal-Bench verifier script.',
    ),
    requirement(
      'oracle_solution',
      'solution.sh or Harbor solution/solve.sh oracle solution',
      'partial_local_equivalent_available',
      sourceLocalBenchmarkHarnessPath,
      'Local no-provider fixture repairs and replay records provide solution-shaped evidence, but no official oracle solution script is generated.',
    ),
    requirement(
      'task_timeout_and_metadata',
      'Task metadata including timeout and difficulty fields',
      hasTaskManifest ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      readiness.benchmarkManifestPath,
      'Local task manifest preserves task IDs and evidence hashes, but official timeout/difficulty metadata is not claimed.',
    ),
    requirement(
      'agent_trajectory_artifacts',
      'Agent trajectory, terminal recording, action/observation, or job artifacts',
      hasPortableTrajectories ? 'local_equivalent_available' : 'classified_unresolved_protected_action_required',
      traces.portableTraceExportPath,
      'Portable local trace events provide source-hash-addressed trajectory-shaped evidence without external benchmark execution.',
    ),
    requirement(
      'result_and_reward_artifacts',
      'Job result.json, trial result, verifier reward, stdout, stderr, or CTRF artifacts',
      hasLocalResults ? 'partial_local_equivalent_available' : 'classified_unresolved_protected_action_required',
      harness.localBenchmarkResultPath,
      'Local benchmark replay results exist, but official Harbor job/trial/verifier outputs were not generated.',
    ),
    requirement(
      'human_review_and_exploit_audit',
      'Specificity, solvability, integrity, manual review, and adversarial exploit audit evidence',
      'partial_local_equivalent_available',
      sourceBenchmarkPolicyCompliancePath,
      'Local policy evidence preserves claim boundaries, but experienced reviewer and adversarial exploit audits remain unresolved.',
    ),
    requirement(
      'official_harbor_or_terminal_bench_run',
      'harbor run or tb run execution against Terminal-Bench',
      'blocked_not_authorized',
      null,
      'No Harbor install, Docker run, provider run, live model run, or official Terminal-Bench execution is authorized in this local gate.',
    ),
    requirement(
      'leaderboard_or_external_submission',
      'Leaderboard logs, external PR, HuggingFace log submission, or public result claim',
      'blocked_not_authorized',
      null,
      'No external repository interaction, public leaderboard claim, or external validation claim is authorized.',
    ),
  ]
}

function writeMarkdown(report: TerminalBenchReadinessReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`)
    .join('\n')
  const requirementRows = report.terminalBenchRequirementRecords
    .map((record) => `| \`${record.requirementId}\` | \`${record.readinessStatus}\` | \`${record.localEquivalentPath ?? 'none'}\` | \`${record.officialRunRequired}\` | \`${record.protectedActionExecuted}\` |`)
    .join('\n')
  const checkRows = report.terminalBenchReadinessChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Terminal-Bench Readiness Report

Generated by: \`bun run product:terminal-bench-readiness\`

## Claim Boundary

- This is a local no-provider Terminal-Bench/Harbor readiness and gap report.
- It maps official task-format and result-artifact expectations to current OpenClaude local evidence.
- It does not install Harbor, install Docker, run containers, run providers, run live models, call external services, submit leaderboard logs, open pull requests, publish, deploy, launch, or claim official Terminal-Bench results.
- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- source_benchmark_task_manifest_path: \`${report.sourceBenchmarkTaskManifestPath}\`
- source_local_benchmark_results_path: \`${report.sourceLocalBenchmarkResultsPath}\`
- source_portable_trace_jsonl_path: \`${report.sourcePortableTraceJsonlPath}\`
- task_map_jsonl_path: \`${report.taskMapJsonlPath}\`
- task_map_jsonl_sha256: \`${report.taskMapJsonlSha256}\`
- requirement_count: \`${report.summary.requirementCount}\`
- local_equivalent_available_count: \`${report.summary.localEquivalentAvailableCount}\`
- partial_local_equivalent_count: \`${report.summary.partialLocalEquivalentCount}\`
- classified_unresolved_protected_gap_count: \`${report.summary.classifiedUnresolvedProtectedGapCount}\`
- blocked_not_authorized_count: \`${report.summary.blockedNotAuthorizedCount}\`
- official_terminal_bench_execution_ready: \`${report.summary.officialTerminalBenchExecutionReady}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${sourceRows}

## Requirement Matrix

| Requirement | Status | Local Equivalent | Official/Protected Run Required | Protected Action Executed |
| --- | --- | --- | --- | --- |
${requirementRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'terminal-bench-readiness-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const readiness = readJson<BenchmarkReadinessReport>(sourceBenchmarkReadinessPath)
  const harness = readJson<LocalBenchmarkHarnessReport>(sourceLocalBenchmarkHarnessPath)
  const traces = readJson<TracePortabilityExportReport>(sourceTracePortabilityExportPath)
  const policy = readJson<BenchmarkPolicyComplianceReport>(sourceBenchmarkPolicyCompliancePath)
  const requirements = buildRequirements(readiness, harness, traces)
  const taskMapJsonl = `${requirements.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, terminalBenchTaskMapJsonlPath), taskMapJsonl)
  const taskMapJsonlSha256 = sha256Text(taskMapJsonl)

  const summary = {
    requirementCount: requirements.length,
    localEquivalentAvailableCount: requirements.filter((record) => record.readinessStatus === 'local_equivalent_available').length,
    partialLocalEquivalentCount: requirements.filter((record) => record.readinessStatus === 'partial_local_equivalent_available').length,
    classifiedUnresolvedProtectedGapCount: requirements.filter((record) => record.readinessStatus === 'classified_unresolved_protected_action_required').length,
    blockedNotAuthorizedCount: requirements.filter((record) => record.readinessStatus === 'blocked_not_authorized').length,
    officialTerminalBenchExecutionReady: false as const,
  }

  const checks = [
    check('benchmark readiness matrix is imported', readiness.mode === 'local_no_provider_benchmark_readiness_matrix', readiness.mode),
    check('local benchmark harness is imported', harness.mode === 'local_no_provider_benchmark_replay_harness', harness.mode),
    check('trace portability export is imported', traces.mode === 'local_no_provider_trace_portability_export', traces.mode),
    check('benchmark policy compliance is imported', policy.mode === 'local_no_provider_benchmark_policy_compliance', policy.mode),
    check('source manifest hash matches readiness report', fileSha256(readiness.benchmarkManifestPath) === readiness.benchmarkManifestSha256, readiness.benchmarkManifestPath),
    check('source local benchmark result hash matches harness report', fileSha256(harness.localBenchmarkResultPath) === harness.localBenchmarkResultSha256, harness.localBenchmarkResultPath),
    check('source portable trace hash matches trace export report', fileSha256(traces.portableTraceExportPath) === traces.portableTraceExportSha256, traces.portableTraceExportPath),
    check('Terminal-Bench requirement matrix covers task environment tests solution trajectories results audits run and submission', requirements.length >= 10 && ['instruction_or_task_description', 'docker_environment', 'tests_or_verifier', 'oracle_solution', 'agent_trajectory_artifacts', 'result_and_reward_artifacts', 'human_review_and_exploit_audit', 'official_harbor_or_terminal_bench_run', 'leaderboard_or_external_submission'].every((id) => requirements.some((record) => record.requirementId === id)), `${requirements.length} requirements`),
    check('local equivalents are source-hash-addressed when present', requirements.every((record) => record.localEquivalentPath === null || record.localEquivalentSha256?.length === 64), `${requirements.filter((record) => record.localEquivalentPath !== null).length} local equivalents`),
    check('official Terminal-Bench execution remains blocked', summary.officialTerminalBenchExecutionReady === false, 'officialTerminalBenchExecutionReady=false'),
    check('protected gaps are classified but not executed', requirements.some((record) => record.protectedActionRequiredToComplete) && requirements.every((record) => record.protectedActionExecuted === false && record.officialResultClaimed === false), `${summary.classifiedUnresolvedProtectedGapCount + summary.blockedNotAuthorizedCount} protected/blocked gaps`),
    check('policy boundary keeps official and leaderboard claims blocked', policy.summary.officialSWEbenchVerifiedSubmissionClaimAllowed === false && policy.summary.officialLeaderboardClaimAllowed === false && policy.officialBenchmarkSubmissionPerformed === false && policy.externalBenchmarkExecutionPerformed === false && policy.externalLeaderboardClaimAllowed === false, 'all official policy claims false'),
    check('task map JSONL hash is recorded', taskMapJsonlSha256.length === 64 && existsSync(resolve(root, terminalBenchTaskMapJsonlPath)), terminalBenchTaskMapJsonlPath),
    check('no provider live external dependency Docker Harbor or protected actions occurred', readiness.providerCallsPerformed.length === 0 && readiness.liveModelCallsPerformed.length === 0 && readiness.externalCallsPerformed.length === 0 && readiness.protectedActionsExecuted.length === 0 && harness.externalBenchmarkExecutionPerformed === false && traces.providerCallsPerformed.length === 0 && traces.liveModelCallsPerformed.length === 0 && traces.externalCallsPerformed.length === 0 && traces.protectedActionsExecuted.length === 0 && policy.providerCallsPerformed.length === 0 && policy.liveModelCallsPerformed.length === 0 && policy.externalCallsPerformed.length === 0 && policy.protectedActionsExecuted.length === 0 && policy.dependencyInstallPerformed === false, 'all call/action arrays empty and dependencyInstallPerformed=false'),
  ]

  const report: TerminalBenchReadinessReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_terminal_bench_readiness',
    sourceBenchmarkReadinessPath,
    sourceBenchmarkTaskManifestPath: readiness.benchmarkManifestPath,
    sourceBenchmarkTaskManifestSha256: readiness.benchmarkManifestSha256,
    sourceLocalBenchmarkHarnessPath,
    sourceLocalBenchmarkResultsPath: harness.localBenchmarkResultPath,
    sourceLocalBenchmarkResultsSha256: harness.localBenchmarkResultSha256,
    sourceTracePortabilityExportPath,
    sourcePortableTraceJsonlPath: traces.portableTraceExportPath,
    sourcePortableTraceJsonlSha256: traces.portableTraceExportSha256,
    sourceBenchmarkPolicyCompliancePath,
    primarySourceInputs: [
      {
        sourceProject: 'harbor-framework/terminal-bench',
        sourceUrl: 'https://github.com/harbor-framework/terminal-bench',
        observedPattern: 'Terminal-agent benchmarks use task instructions, Docker environments, tests, oracle solutions, and inspectable benchmark artifacts rather than prose-only quality claims.',
      },
      {
        sourceProject: 'Terminal-Bench task documentation',
        sourceUrl: 'https://www.tbench.ai/docs/task-overview',
        observedPattern: 'A task directory contains Docker environment files, task.yaml, solution.yaml or solution.sh, run-tests.sh, tests, and supporting dependencies.',
      },
      {
        sourceProject: 'Harbor Terminal-Bench runner documentation',
        sourceUrl: 'https://www.harborframework.com/docs/tutorials/running-terminal-bench',
        observedPattern: 'Official Terminal-Bench 2.0 execution goes through Harbor and requires Docker/runtime setup before any leaderboard submission path is used.',
      },
      {
        sourceProject: 'Harbor eval artifacts documentation',
        sourceUrl: 'https://harborframework.com/docs/run-jobs/run-evals',
        observedPattern: 'Benchmark jobs produce config, result, recording, trajectory, verifier reward, stdout, stderr, and CTRF artifacts for later inspection.',
      },
    ],
    taskMapJsonlPath: terminalBenchTaskMapJsonlPath,
    taskMapJsonlSha256,
    terminalBenchRequirementRecords: requirements,
    summary,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    dockerContainerRunPerformed: false,
    harborInstallPerformed: false,
    officialTerminalBenchExecutionPerformed: false,
    officialTerminalBenchResultClaimed: false,
    officialLeaderboardSubmissionPerformed: false,
    officialLeaderboardClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    terminalBenchReadinessChecks: checks,
    claimBoundary: 'Terminal-Bench readiness is local no-provider evidence only. It maps OpenClaude local evidence to Terminal-Bench/Harbor task and artifact expectations, but does not install Harbor or Docker, execute official benchmarks, submit leaderboard logs, call providers, call live models, call external services, or make release, production, public, external-validation, leaderboard, cost-efficiency, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(docsDir, 'terminal-bench-readiness-report.json'), `${JSON.stringify(report, null, 2)}\n`)
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
  console.log(`terminal_bench_task_map_jsonl_path=${terminalBenchTaskMapJsonlPath}`)
  console.log(`requirement_count=${summary.requirementCount}`)
  console.log(`local_equivalent_available_count=${summary.localEquivalentAvailableCount}`)
  console.log(`partial_local_equivalent_count=${summary.partialLocalEquivalentCount}`)
  console.log(`classified_unresolved_protected_gap_count=${summary.classifiedUnresolvedProtectedGapCount}`)
  console.log(`blocked_not_authorized_count=${summary.blockedNotAuthorizedCount}`)
  console.log(`official_terminal_bench_execution_ready=${summary.officialTerminalBenchExecutionReady}`)
  console.log(`official_leaderboard_claim_allowed=${report.officialLeaderboardClaimAllowed}`)
}

main()
