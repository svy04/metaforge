import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import {
  buildTraceEventName,
  describeTraceObservation,
  enrichTraceEvent,
} from './product-trace-event-enrichment'

type JsonObject = Record<string, unknown>

type PortableCheck = {
  label: string
  ok: boolean
  detail: string
}

type RealTraceEvalReport = {
  mode: string
  traceDirectory: string
  traceFileCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  traces: Array<{
    path: string
    sha256: string
    traceKind: string
    eventCount: number
  }>
}

type TraceSchemaContractReport = {
  mode: string
  sourceRealTraceEvalReportPath: string
  sourceTraceFileCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  aggregate: {
    traceCount: number
    eventCount: number
    missingRecommendedEventNameCount: number
    missingRecommendedTraceContextCount: number
    missingRecommendedActionObservationCount: number
    currentGeneratedTraceProducerTraceCount: number
    currentGeneratedTraceProducerEventCount: number
    currentGeneratedTraceProducerMissingEventNameCount: number
    currentGeneratedTraceProducerMissingTraceContextCount: number
    currentGeneratedTraceProducerMissingActionObservationCount: number
  }
  schemaContractChecks: PortableCheck[]
}

type PortableTraceEvent = {
  sourceTracePath: string
  sourceTraceSha256: string
  sourceLineNumber: number
  sourceEventSha256: string
  sourceTraceKind: string
  sourceEventAlreadyEnriched: boolean
  normalizedFromHistoricalGap: boolean
  timestamp: string
  role: string
  model: string
  querySource: string
  status: string
  turnCount: number
  eventName: string
  traceId: string
  spanId: string
  actionName?: string
  observationSummary?: string
  commandName?: string
  toolName?: string
  phaseLabel?: string
  exitCode?: number | null
  passed?: boolean
  promptSha256?: string
  promptByteLength?: number
  stdoutSha256?: string
  stderrSha256?: string
  stdoutByteLength?: number
  stderrByteLength?: number
  testCaseCount?: number
}

type TracePortabilityExportReport = {
  generatedAt: string
  mode: 'local_no_provider_trace_portability_export'
  sourceRealTraceEvalReportPath: string
  sourceRealTraceEvalReportSha256: string
  sourceTraceSchemaContractReportPath: string
  sourceTraceSchemaContractReportSha256: string
  portableTraceExportPath: string
  portableTraceExportSha256: string
  sourceTraceCount: number
  sourceEventCount: number
  portableEventCount: number
  sourceHistoricalMissingEventNameCount: number
  sourceHistoricalMissingTraceContextCount: number
  sourceHistoricalMissingActionObservationCount: number
  portableMissingEventNameCount: number
  portableMissingTraceContextCount: number
  portableMissingActionObservationCount: number
  sourceEventsAlreadyEnrichedCount: number
  portableEventsSynthesizedFromHistoricalGapsCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  sourceTraceHashes: Array<{
    path: string
    sha256: string
    eventCount: number
  }>
  portabilityChecks: PortableCheck[]
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const sourceRealTraceEvalReportPath = 'docs/product-quality/real-session-trace-evals-report.json'
const sourceTraceSchemaContractReportPath = 'docs/product-quality/trace-schema-contract-report.json'
const portableTraceExportPath = 'reports/openclaude-portable-trace-events.jsonl'

const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /github_pat_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function check(label: string, ok: boolean, detail: string): PortableCheck {
  return { label, ok, detail }
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0
}

function isValidTraceId(value: unknown): value is string {
  return isNonEmptyString(value) && /^[a-f0-9]{32}$/i.test(value)
}

function isValidSpanId(value: unknown): value is string {
  return isNonEmptyString(value) && /^[a-f0-9]{16}$/i.test(value)
}

function hasCredentialPattern(text: string): boolean {
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function optionalString(event: JsonObject, key: string): string | undefined {
  const value = event[key]
  return isNonEmptyString(value) ? value : undefined
}

function optionalNumber(event: JsonObject, key: string): number | undefined {
  const value = event[key]
  return typeof value === 'number' && Number.isFinite(value) ? value : undefined
}

function optionalNullableNumber(event: JsonObject, key: string): number | null | undefined {
  if (event[key] === null) return null
  return optionalNumber(event, key)
}

function optionalBoolean(event: JsonObject, key: string): boolean | undefined {
  const value = event[key]
  return typeof value === 'boolean' ? value : undefined
}

function isActionLikeEvent(event: JsonObject): boolean {
  return isNonEmptyString(event.commandName) ||
    isNonEmptyString(event.toolName) ||
    event.exitCode !== undefined ||
    event.passed !== undefined ||
    event.stdoutByteLength !== undefined ||
    event.stderrByteLength !== undefined ||
    event.testCaseCount !== undefined
}

function actionNameFor(event: JsonObject): string | undefined {
  return optionalString(event, 'actionName') ??
    optionalString(event, 'commandName') ??
    optionalString(event, 'toolName') ??
    optionalString(event, 'phaseLabel') ??
    (isActionLikeEvent(event) ? optionalString(event, 'role') : undefined)
}

function observationFor(event: JsonObject): string | undefined {
  return optionalString(event, 'observationSummary') ?? (isActionLikeEvent(event)
    ? describeTraceObservation(String(event.status), {
        exitCode: optionalNullableNumber(event, 'exitCode'),
        passed: optionalBoolean(event, 'passed'),
        stdoutByteLength: optionalNumber(event, 'stdoutByteLength'),
        stderrByteLength: optionalNumber(event, 'stderrByteLength'),
        testCaseCount: optionalNumber(event, 'testCaseCount'),
      })
    : undefined)
}

function sourceEventAlreadyEnriched(event: JsonObject): boolean {
  const actionFieldsOk = !isActionLikeEvent(event) || (
    isNonEmptyString(event.actionName) && isNonEmptyString(event.observationSummary)
  )
  return isNonEmptyString(event.eventName) &&
    isValidTraceId(event.traceId) &&
    isValidSpanId(event.spanId) &&
    actionFieldsOk
}

function normalizeEvent(
  event: JsonObject,
  sourceTracePath: string,
  sourceTraceSha256: string,
  sourceTraceKind: string,
  sourceLineNumber: number,
  sourceEventSha256: string,
): PortableTraceEvent {
  const actionName = actionNameFor(event)
  const eventName = optionalString(event, 'eventName') ??
    buildTraceEventName(
      sourceTraceKind || optionalString(event, 'querySource') || basename(sourceTracePath, '.jsonl'),
      String(event.role),
      String(event.status),
      actionName,
    )
  const observationSummary = observationFor(event)
  const alreadyEnriched = sourceEventAlreadyEnriched(event)
  const enriched = enrichTraceEvent(
    {
      sourceTracePath,
      sourceTraceSha256,
      sourceLineNumber,
      sourceEventSha256,
      sourceTraceKind,
      sourceEventAlreadyEnriched: alreadyEnriched,
      normalizedFromHistoricalGap: !alreadyEnriched,
      timestamp: String(event.timestamp),
      role: String(event.role),
      model: String(event.model),
      querySource: String(event.querySource),
      status: String(event.status),
      turnCount: Number(event.turnCount),
    },
    {
      traceSeed: `${sourceTracePath}:${sourceTraceSha256}`,
      spanSeed: `${sourceLineNumber}:${sourceEventSha256}`,
      eventName,
      actionName,
      observationSummary,
    },
  )

  const portable: PortableTraceEvent = {
    ...enriched,
    traceId: isValidTraceId(event.traceId) ? event.traceId.toLowerCase() : enriched.traceId,
    spanId: isValidSpanId(event.spanId) ? event.spanId.toLowerCase() : enriched.spanId,
  }

  for (const key of ['commandName', 'toolName', 'phaseLabel', 'promptSha256', 'stdoutSha256', 'stderrSha256']) {
    const value = optionalString(event, key)
    if (value !== undefined) {
      portable[key as 'commandName'] = value
    }
  }
  for (const key of ['promptByteLength', 'stdoutByteLength', 'stderrByteLength', 'testCaseCount']) {
    const value = optionalNumber(event, key)
    if (value !== undefined) {
      portable[key as 'promptByteLength'] = value
    }
  }
  const exitCode = optionalNullableNumber(event, 'exitCode')
  if (exitCode !== undefined) portable.exitCode = exitCode
  const passed = optionalBoolean(event, 'passed')
  if (passed !== undefined) portable.passed = passed

  return portable
}

function readJson<T>(path: string): { text: string, value: T } {
  const text = readFileSync(resolve(root, path), 'utf8')
  return { text, value: JSON.parse(text) as T }
}

function readTraceEvents(trace: RealTraceEvalReport['traces'][number]): PortableTraceEvent[] {
  const text = readFileSync(resolve(root, trace.path), 'utf8')
  const actualSha256 = sha256(text)
  if (actualSha256 !== trace.sha256) {
    throw new Error(`trace hash mismatch for ${trace.path}: ${actualSha256} != ${trace.sha256}`)
  }
  return text
    .split(/\r?\n/)
    .map((line, index) => ({ line, sourceLineNumber: index + 1 }))
    .filter((item) => item.line.trim().length > 0)
    .map((item) => normalizeEvent(
      JSON.parse(item.line) as JsonObject,
      trace.path,
      trace.sha256,
      trace.traceKind,
      item.sourceLineNumber,
      sha256(item.line),
    ))
}

function missingEventNameCount(events: PortableTraceEvent[]): number {
  return events.filter((event) => !isNonEmptyString(event.eventName)).length
}

function missingTraceContextCount(events: PortableTraceEvent[]): number {
  return events.filter((event) => !isValidTraceId(event.traceId) || !isValidSpanId(event.spanId)).length
}

function missingActionObservationCount(events: PortableTraceEvent[]): number {
  return events.filter((event) => {
    const actionLike = event.commandName !== undefined ||
      event.toolName !== undefined ||
      event.exitCode !== undefined ||
      event.passed !== undefined ||
      event.stdoutByteLength !== undefined ||
      event.stderrByteLength !== undefined ||
      event.testCaseCount !== undefined
    return actionLike && (!isNonEmptyString(event.actionName) || !isNonEmptyString(event.observationSummary))
  }).length
}

function writeReports(report: TracePortabilityExportReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(
    resolve(docsDir, 'trace-portability-export-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )
  const lines = [
    '# Trace Portability Export Report',
    '',
    'Generated by: `bun run product:trace-portability-export`',
    '',
    '## Claim Boundary',
    '',
    '- This report exports a local portable JSONL view from existing `reports/orchestra-*.jsonl` trace artifacts.',
    '- It preserves source trace path, source trace hash, source line number, and source event hash for each portable event.',
    '- It does not rewrite historical raw trace artifacts.',
    '- It does not call providers, live models, or external services.',
    '- It does not execute protected actions or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- source_real_trace_eval_report: \`${report.sourceRealTraceEvalReportPath}\``,
    `- source_trace_schema_contract_report: \`${report.sourceTraceSchemaContractReportPath}\``,
    `- portable_trace_export: \`${report.portableTraceExportPath}\``,
    `- source_trace_count: \`${report.sourceTraceCount}\``,
    `- source_event_count: \`${report.sourceEventCount}\``,
    `- portable_event_count: \`${report.portableEventCount}\``,
    `- source_historical_missing_event_name_count: \`${report.sourceHistoricalMissingEventNameCount}\``,
    `- source_historical_missing_trace_context_count: \`${report.sourceHistoricalMissingTraceContextCount}\``,
    `- source_historical_missing_action_observation_count: \`${report.sourceHistoricalMissingActionObservationCount}\``,
    `- portable_missing_event_name_count: \`${report.portableMissingEventNameCount}\``,
    `- portable_missing_trace_context_count: \`${report.portableMissingTraceContextCount}\``,
    `- portable_missing_action_observation_count: \`${report.portableMissingActionObservationCount}\``,
    `- source_events_already_enriched_count: \`${report.sourceEventsAlreadyEnrichedCount}\``,
    `- portable_events_synthesized_from_historical_gaps_count: \`${report.portableEventsSynthesizedFromHistoricalGapsCount}\``,
    `- portable_trace_export_sha256: \`${report.portableTraceExportSha256}\``,
    '',
    '## Source Trace Hashes',
    '',
    '| Trace | Events | SHA-256 |',
    '| --- | ---: | --- |',
    ...report.sourceTraceHashes.map((trace) => `| \`${trace.path}\` | ${trace.eventCount} | \`${trace.sha256}\` |`),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.portabilityChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]
  writeFileSync(resolve(docsDir, 'trace-portability-export-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  const realTraceEvalSource = readJson<RealTraceEvalReport>(sourceRealTraceEvalReportPath)
  const traceSchemaContractSource = readJson<TraceSchemaContractReport>(sourceTraceSchemaContractReportPath)
  const portableEvents = realTraceEvalSource.value.traces.flatMap(readTraceEvents)
  const portableText = portableEvents.map((event) => JSON.stringify(event)).join('\n') + '\n'
  mkdirSync(resolve(root, 'reports'), { recursive: true })
  writeFileSync(resolve(root, portableTraceExportPath), portableText)

  const portableMissingEventName = missingEventNameCount(portableEvents)
  const portableMissingTraceContext = missingTraceContextCount(portableEvents)
  const portableMissingActionObservation = missingActionObservationCount(portableEvents)
  const sourceEventCount = realTraceEvalSource.value.traces.reduce((total, trace) => total + trace.eventCount, 0)
  const sourceEventsAlreadyEnrichedCount = portableEvents.filter((event) => event.sourceEventAlreadyEnriched).length
  const synthesizedCount = portableEvents.filter((event) => event.normalizedFromHistoricalGap).length
  const portableSha256 = sha256(portableText)
  const exportHasCredentialPattern = hasCredentialPattern(portableText)

  const portabilityChecks = [
    check('real trace eval report is local no-provider source', realTraceEvalSource.value.mode === 'local_no_provider_real_session_jsonl_trace_grading', realTraceEvalSource.value.mode),
    check('trace schema contract report is local no-provider source', traceSchemaContractSource.value.mode === 'local_no_provider_trace_schema_contract', traceSchemaContractSource.value.mode),
    check('source reports performed no provider calls', realTraceEvalSource.value.providerCallsPerformed.length === 0 && traceSchemaContractSource.value.providerCallsPerformed.length === 0, 'provider calls are zero'),
    check('source reports performed no live model calls', realTraceEvalSource.value.liveModelCallsPerformed.length === 0 && traceSchemaContractSource.value.liveModelCallsPerformed.length === 0, 'live model calls are zero'),
    check('source reports performed no external calls', realTraceEvalSource.value.externalCallsPerformed.length === 0 && traceSchemaContractSource.value.externalCallsPerformed.length === 0, 'external calls are zero'),
    check('source schema contract executed no protected actions', traceSchemaContractSource.value.protectedActionsExecuted.length === 0, 'protected actions are zero'),
    check('trace count matches schema contract', realTraceEvalSource.value.traceFileCount === traceSchemaContractSource.value.sourceTraceFileCount && realTraceEvalSource.value.traceFileCount === traceSchemaContractSource.value.aggregate.traceCount, `${realTraceEvalSource.value.traceFileCount}/${traceSchemaContractSource.value.aggregate.traceCount}`),
    check('portable export has one event per source event', portableEvents.length === sourceEventCount && portableEvents.length === traceSchemaContractSource.value.aggregate.eventCount, `${portableEvents.length}/${sourceEventCount}`),
    check('portable export preserves source trace hashes', realTraceEvalSource.value.traces.every((trace) => portableEvents.some((event) => event.sourceTracePath === trace.path && event.sourceTraceSha256 === trace.sha256)), `${realTraceEvalSource.value.traces.length} traces`),
    check('portable export has event names for every event', portableMissingEventName === 0, `${portableMissingEventName} missing`),
    check('portable export has trace context for every event', portableMissingTraceContext === 0, `${portableMissingTraceContext} missing`),
    check('portable export has action-observation fields for action events', portableMissingActionObservation === 0, `${portableMissingActionObservation} missing`),
    check('portable export normalizes historical gaps without raw mutation', traceSchemaContractSource.value.aggregate.missingRecommendedEventNameCount > 0 && synthesizedCount === traceSchemaContractSource.value.aggregate.missingRecommendedEventNameCount, `${synthesizedCount} synthesized`),
    check('portable export contains no credential patterns', !exportHasCredentialPattern, 'known key/token/private-key patterns absent'),
    check('portable export writes hash-addressed JSONL', portableSha256.length === 64 && portableTraceExportPath.endsWith('.jsonl'), portableTraceExportPath),
  ]

  const report: TracePortabilityExportReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_trace_portability_export',
    sourceRealTraceEvalReportPath,
    sourceRealTraceEvalReportSha256: sha256(realTraceEvalSource.text),
    sourceTraceSchemaContractReportPath,
    sourceTraceSchemaContractReportSha256: sha256(traceSchemaContractSource.text),
    portableTraceExportPath,
    portableTraceExportSha256: portableSha256,
    sourceTraceCount: realTraceEvalSource.value.traceFileCount,
    sourceEventCount,
    portableEventCount: portableEvents.length,
    sourceHistoricalMissingEventNameCount: traceSchemaContractSource.value.aggregate.missingRecommendedEventNameCount,
    sourceHistoricalMissingTraceContextCount: traceSchemaContractSource.value.aggregate.missingRecommendedTraceContextCount,
    sourceHistoricalMissingActionObservationCount: traceSchemaContractSource.value.aggregate.missingRecommendedActionObservationCount,
    portableMissingEventNameCount: portableMissingEventName,
    portableMissingTraceContextCount: portableMissingTraceContext,
    portableMissingActionObservationCount: portableMissingActionObservation,
    sourceEventsAlreadyEnrichedCount,
    portableEventsSynthesizedFromHistoricalGapsCount: synthesizedCount,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    sourceTraceHashes: realTraceEvalSource.value.traces.map((trace) => ({
      path: trace.path,
      sha256: trace.sha256,
      eventCount: trace.eventCount,
    })),
    portabilityChecks,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    claimBoundary: 'Portable trace export evidence only; no provider/live/external calls, protected actions, release readiness, production readiness, public readiness, external validation, or autonomous reliability claim is authorized.',
  }

  writeReports(report)

  for (const item of portabilityChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  if (!portabilityChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`portable_trace_export=${portableTraceExportPath}`)
  console.log(`source_trace_count=${report.sourceTraceCount}`)
  console.log(`source_event_count=${report.sourceEventCount}`)
  console.log(`portable_event_count=${report.portableEventCount}`)
  console.log(`portable_missing_event_name_count=${report.portableMissingEventNameCount}`)
  console.log(`portable_missing_trace_context_count=${report.portableMissingTraceContextCount}`)
  console.log(`portable_missing_action_observation_count=${report.portableMissingActionObservationCount}`)
  console.log(`portable_events_synthesized_from_historical_gaps=${report.portableEventsSynthesizedFromHistoricalGapsCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
