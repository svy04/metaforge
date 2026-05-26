import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'

type JsonObject = Record<string, unknown>

type TraceCheck = {
  label: string
  ok: boolean
  detail: string
}

type TraceSummary = {
  path: string
  sha256: string
  traceKind: string
  lineCount: number
  eventCount: number
  parseErrorCount: number
  statuses: Record<string, number>
  statusSequence: string[]
  roles: string[]
  models: string[]
  querySources: string[]
  hasStarted: boolean
  firstStatus: string | null
  hasTerminalStatus: boolean
  hasStartedToTerminalTransition: boolean
  lastStatus: string | null
  requiredFieldsComplete: boolean
  credentialPatternFound: boolean
  passed: boolean
}

type CoverageGap = {
  id: string
  status: 'classified_unresolved' | 'not_present'
  detail: string
  protectedActionRequired: boolean
}

type CoverageSummary = {
  traceKinds: string[]
  terminalOutcomes: string[]
  roles: string[]
  models: string[]
  querySources: string[]
  passedTraceCount: number
  failedTraceCount: number
  succeededTraceCount: number
  classifiedCoverageGaps: CoverageGap[]
}

type RealTraceEvalReport = {
  generatedAt: string
  mode: 'local_no_provider_real_session_jsonl_trace_grading'
  traceDirectory: string
  traceFileCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  traces: TraceSummary[]
  coverageSummary: CoverageSummary
  traceChecks: TraceCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const traceDirectory = 'reports'
const terminalStatuses = new Set(['succeeded', 'failed', 'cancelled'])
const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

function check(label: string, ok: boolean, detail: string): TraceCheck {
  return { label, ok, detail }
}

function sortedKeys(map: Map<string, number>): string[] {
  return [...map.keys()].sort((a, b) => a.localeCompare(b))
}

function increment(map: Map<string, number>, key: unknown): void {
  if (typeof key !== 'string' || key.length === 0) {
    return
  }
  map.set(key, (map.get(key) ?? 0) + 1)
}

function toRecord(map: Map<string, number>): Record<string, number> {
  return Object.fromEntries([...map.entries()].sort(([a], [b]) => a.localeCompare(b)))
}

function unique(values: string[]): string[] {
  return [...new Set(values)].sort((a, b) => a.localeCompare(b))
}

function hasCredentialPattern(text: string): boolean {
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function hasRequiredFields(event: JsonObject): boolean {
  return typeof event.timestamp === 'string' &&
    typeof event.role === 'string' &&
    typeof event.model === 'string' &&
    typeof event.querySource === 'string' &&
    typeof event.status === 'string' &&
    typeof event.turnCount === 'number'
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

function summarizeTrace(path: string): TraceSummary {
  const absolutePath = resolve(root, path)
  const text = readFileSync(absolutePath, 'utf8')
  const lines = text.split(/\r?\n/).filter((line) => line.trim().length > 0)
  const statuses = new Map<string, number>()
  const roles = new Map<string, number>()
  const models = new Map<string, number>()
  const querySources = new Map<string, number>()
  let eventCount = 0
  let parseErrorCount = 0
  let requiredFieldsComplete = true
  let lastStatus: string | null = null
  const statusSequence: string[] = []

  for (const line of lines) {
    try {
      const event = JSON.parse(line) as JsonObject
      eventCount += 1
      if (!hasRequiredFields(event)) {
        requiredFieldsComplete = false
      }
      increment(statuses, event.status)
      increment(roles, event.role)
      increment(models, event.model)
      increment(querySources, event.querySource)
      if (typeof event.status === 'string') {
        lastStatus = event.status
        statusSequence.push(event.status)
      }
    } catch {
      parseErrorCount += 1
      requiredFieldsComplete = false
    }
  }

  const hasStarted = statuses.has('started')
  const firstStatus = statusSequence[0] ?? null
  const hasTerminalStatus = lastStatus !== null && terminalStatuses.has(lastStatus)
  const hasStartedToTerminalTransition = firstStatus === 'started' && hasTerminalStatus
  const credentialPatternFound = hasCredentialPattern(text)
  const passed = lines.length > 0 &&
    parseErrorCount === 0 &&
    requiredFieldsComplete &&
    hasStarted &&
    hasStartedToTerminalTransition &&
    !credentialPatternFound

  return {
    path,
    sha256: createHash('sha256').update(text).digest('hex'),
    traceKind: classifyTraceKind(path),
    lineCount: lines.length,
    eventCount,
    parseErrorCount,
    statuses: toRecord(statuses),
    statusSequence,
    roles: sortedKeys(roles),
    models: sortedKeys(models),
    querySources: sortedKeys(querySources),
    hasStarted,
    firstStatus,
    hasTerminalStatus,
    hasStartedToTerminalTransition,
    lastStatus,
    requiredFieldsComplete,
    credentialPatternFound,
    passed,
  }
}

function discoverTraceFiles(): string[] {
  return readdirSync(resolve(root, traceDirectory), { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .filter((name) => /^orchestra-.*\.jsonl$/.test(name))
    .sort((a, b) => a.localeCompare(b))
    .map((name) => `${traceDirectory}/${name}`)
}

function gap(id: string, status: CoverageGap['status'], detail: string, protectedActionRequired = false): CoverageGap {
  return { id, status, detail, protectedActionRequired }
}

function buildCoverageSummary(traces: TraceSummary[]): CoverageSummary {
  const terminalOutcomes = unique(traces
    .map((trace) => trace.lastStatus)
    .filter((status): status is string => status !== null && terminalStatuses.has(status)))
  const roles = unique(traces.flatMap((trace) => trace.roles))
  const models = unique(traces.flatMap((trace) => trace.models))
  const querySources = unique(traces.flatMap((trace) => trace.querySources))
  const traceKinds = unique(traces.map((trace) => trace.traceKind))
  const classifiedCoverageGaps: CoverageGap[] = []

  if (roles.length < 2) {
    classifiedCoverageGaps.push(gap(
      'single_role_trace_coverage',
      'classified_unresolved',
      `Only ${roles.length} role is represented in current local traces: ${roles.join(', ') || 'none'}. Broader user/executor traces are still needed before stronger reliability claims.`,
    ))
  } else {
    classifiedCoverageGaps.push(gap('single_role_trace_coverage', 'not_present', `${roles.length} roles represented.`))
  }

  if (models.length < 2) {
    classifiedCoverageGaps.push(gap(
      'single_model_trace_coverage',
      'classified_unresolved',
      `Only ${models.length} model is represented in current local traces: ${models.join(', ') || 'none'}. Multi-model trace evidence remains a later no-provider fixture target.`,
    ))
  } else {
    classifiedCoverageGaps.push(gap('single_model_trace_coverage', 'not_present', `${models.length} models represented.`))
  }

  return {
    traceKinds,
    terminalOutcomes,
    roles,
    models,
    querySources,
    passedTraceCount: traces.filter((trace) => trace.passed).length,
    failedTraceCount: traces.filter((trace) => trace.lastStatus === 'failed').length,
    succeededTraceCount: traces.filter((trace) => trace.lastStatus === 'succeeded').length,
    classifiedCoverageGaps,
  }
}

function writeReports(report: RealTraceEvalReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(
    resolve(docsDir, 'real-session-trace-evals-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )

  const lines = [
    '# Real Session Trace Evals Report',
    '',
    'Generated by: `bun run product:real-trace-evals`',
    '',
    '## Claim Boundary',
    '',
    '- This report grades existing local `reports/orchestra-*.jsonl` trace artifacts only.',
    '- It does not call providers, live models, or external services.',
    '- It does not dump raw trace lines or raw provider error payloads into this report.',
    '- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- trace_directory: \`${report.traceDirectory}\``,
    `- trace_file_count: \`${report.traceFileCount}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    `- trace_kinds: ${report.coverageSummary.traceKinds.map((item) => `\`${item}\``).join(', ')}`,
    `- terminal_outcomes: ${report.coverageSummary.terminalOutcomes.map((item) => `\`${item}\``).join(', ')}`,
    `- query_sources: ${report.coverageSummary.querySources.map((item) => `\`${item}\``).join(', ')}`,
    '',
    '## Traces',
    '',
    '| Trace | Kind | Events | Status Sequence | Started-to-Terminal | Fields Complete | Credential Pattern | Passed | SHA-256 |',
    '| --- | --- | ---: | --- | --- | --- | --- | --- | --- |',
    ...report.traces.map((trace) => (
      `| \`${trace.path}\` | \`${trace.traceKind}\` | ${trace.eventCount} | \`${trace.statusSequence.join(' -> ')}\` | \`${trace.hasStartedToTerminalTransition}\` | \`${trace.requiredFieldsComplete}\` | \`${trace.credentialPatternFound}\` | \`${trace.passed}\` | \`${trace.sha256}\` |`
    )),
    '',
    '## Coverage Gaps',
    '',
    '| Gap | Status | Protected Action Required | Detail |',
    '| --- | --- | --- | --- |',
    ...report.coverageSummary.classifiedCoverageGaps.map((item) => (
      `| \`${item.id}\` | \`${item.status}\` | \`${item.protectedActionRequired}\` | ${item.detail} |`
    )),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.traceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'real-session-trace-evals-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  const traceFiles = discoverTraceFiles()
  const traces = traceFiles.map((path) => summarizeTrace(path))
  const coverageSummary = buildCoverageSummary(traces)
  const statusSet = new Set(traces.flatMap((trace) => Object.keys(trace.statuses)))
  const serializedTraceSummaries = JSON.stringify(traces)
  const traceChecks = [
    check('real JSONL trace files discovered', traces.length >= 5, `${traces.length} traces`),
    check('all trace lines parsed as JSON', traces.every((trace) => trace.parseErrorCount === 0), `${traces.reduce((total, trace) => total + trace.parseErrorCount, 0)} parse errors`),
    check('all traces have required event fields', traces.every((trace) => trace.requiredFieldsComplete), 'timestamp, role, model, querySource, status, turnCount'),
    check('all traces have started event', traces.every((trace) => trace.hasStarted), 'started status present'),
    check('all traces end with terminal status', traces.every((trace) => trace.hasTerminalStatus), 'succeeded/failed/cancelled'),
    check('all traces have started-to-terminal ordering', traces.every((trace) => trace.hasStartedToTerminalTransition), 'first status started and last status terminal'),
    check('success and failure traces are both represented', statusSet.has('succeeded') && statusSet.has('failed'), [...statusSet].sort().join(',')),
    check('live and usage trace kinds are represented', coverageSummary.traceKinds.some((kind) => kind.startsWith('live_') || kind === 'live_probe') && coverageSummary.traceKinds.some((kind) => kind.startsWith('usage_')), coverageSummary.traceKinds.join(',')),
    check('query source diversity represented', coverageSummary.querySources.length >= 2, coverageSummary.querySources.join(',')),
    check('coverage gaps are explicitly classified', coverageSummary.classifiedCoverageGaps.every((item) => item.status === 'classified_unresolved' || item.status === 'not_present'), `${coverageSummary.classifiedCoverageGaps.length} gaps`),
    check('coverage gaps do not require protected action', coverageSummary.classifiedCoverageGaps.every((item) => item.protectedActionRequired === false), 'internal no-provider evidence only'),
    check('credential patterns absent from traces', traces.every((trace) => !trace.credentialPatternFound), 'known key/token/private-key patterns absent'),
    check('trace summaries omit raw provider request ids', !serializedTraceSummaries.includes('req_'), 'only status and hash summaries are reported'),
    check('all trace summaries pass', traces.every((trace) => trace.passed), `${traces.filter((trace) => trace.passed).length}/${traces.length}`),
  ]

  const report: RealTraceEvalReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_real_session_jsonl_trace_grading',
    traceDirectory,
    traceFileCount: traces.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    traces,
    coverageSummary,
    traceChecks,
    claimBoundary: 'Real session trace evals grade existing local JSONL trace artifacts only. They do not perform provider, live model, or external calls and do not claim release readiness, production readiness, external validation, public readiness, or autonomous reliability.',
  }

  writeReports(report)

  for (const trace of traces) {
    console.log(`${trace.passed ? 'PASS' : 'FAIL'}: ${basename(trace.path)} events=${trace.eventCount} last_status=${trace.lastStatus}`)
  }
  for (const item of traceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!traceChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`trace_file_count=${traces.length}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`trace_kind_count=${coverageSummary.traceKinds.length}`)
  console.log(`query_source_count=${coverageSummary.querySources.length}`)
  console.log(`classified_coverage_gaps=${coverageSummary.classifiedCoverageGaps.length}`)
}

main()
