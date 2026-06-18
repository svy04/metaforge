import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { basename, resolve } from 'node:path'
import { discoverPublishableTraceFiles } from './product-trace-discovery'

type JsonObject = Record<string, unknown>

type ContractCheck = {
  label: string
  ok: boolean
  detail: string
}

type RealTraceEvalReport = {
  traceDirectory: string
  traceFileCount: number
  traces: Array<{
    path: string
    sha256: string
    eventCount: number
  }>
}

type TraceSchemaSummary = {
  path: string
  sha256: string
  currentGeneratedTraceProducer: boolean
  eventCount: number
  parseErrorCount: number
  requiredFieldViolationCount: number
  invalidTimestampCount: number
  invalidStatusCount: number
  invalidTraceContextCount: number
  missingRecommendedEventNameCount: number
  missingRecommendedTraceContextCount: number
  missingRecommendedActionObservationCount: number
  missingSweAgentTripletFieldCount: number
  credentialPatternFound: boolean
  schemaContractPassed: boolean
}

type AlignmentGap = {
  id: string
  status: 'classified_unresolved' | 'not_present'
  protectedActionRequired: boolean
  detail: string
}

type TraceSchemaContractReport = {
  generatedAt: string
  mode: 'local_no_provider_trace_schema_contract'
  schemaContractVersion: 'openclaude_trace_schema_contract_v1'
  sourceRealTraceEvalReportPath: string
  sourceRealTraceEvalReportSha256: string
  sourceTraceDirectory: string
  sourceTraceFileCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  requiredEventFields: string[]
  optionalRecommendedFields: string[]
  allowedStatuses: string[]
  traceSchemaSummaries: TraceSchemaSummary[]
  aggregate: {
    traceCount: number
    eventCount: number
    schemaPassedTraceCount: number
    schemaFailedTraceCount: number
    missingRecommendedEventNameCount: number
    missingRecommendedTraceContextCount: number
    missingRecommendedActionObservationCount: number
    missingSweAgentTripletFieldCount: number
    currentGeneratedTraceProducerTraceCount: number
    currentGeneratedTraceProducerEventCount: number
    currentGeneratedTraceProducerMissingEventNameCount: number
    currentGeneratedTraceProducerMissingTraceContextCount: number
    currentGeneratedTraceProducerMissingActionObservationCount: number
  }
  recommendedAlignmentGaps: AlignmentGap[]
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  schemaContractChecks: ContractCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const traceDirectory = 'reports'
const sourceRealTraceEvalReportPath = 'docs/product-quality/real-session-trace-evals-report.json'
const allowedStatuses = ['started', 'succeeded', 'failed', 'cancelled']
const requiredEventFields = ['timestamp', 'role', 'model', 'querySource', 'status', 'turnCount']
const optionalRecommendedFields = ['eventName', 'traceId', 'spanId', 'commandName', 'phaseLabel', 'actionName', 'observationSummary']
const currentGeneratedTraceProducerPaths = new Set([
  'reports/orchestra-code-editing-trace-local-fixture.jsonl',
  'reports/orchestra-multi-file-code-editing-trace-local-fixture.jsonl',
  'reports/orchestra-prompted-tool-loop-local-cli.jsonl',
  'reports/orchestra-real-session-capture-local-cli.jsonl',
  'reports/orchestra-regression-cycle-code-editing-trace-local-fixture.jsonl',
  'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
  'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
])
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

function check(label: string, ok: boolean, detail: string): ContractCheck {
  return { label, ok, detail }
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0
}

function hasCredentialPattern(text: string): boolean {
  return credentialPatterns.some((pattern) => pattern.test(text))
}

function isIsoTimestamp(value: unknown): boolean {
  return isNonEmptyString(value) && !Number.isNaN(Date.parse(value))
}

function isValidTraceId(value: unknown): boolean {
  return isNonEmptyString(value) && /^[a-f0-9]{32}$/i.test(value)
}

function isValidSpanId(value: unknown): boolean {
  return isNonEmptyString(value) && /^[a-f0-9]{16}$/i.test(value)
}

function hasRequiredFields(event: JsonObject): boolean {
  return isIsoTimestamp(event.timestamp) &&
    isNonEmptyString(event.role) &&
    isNonEmptyString(event.model) &&
    isNonEmptyString(event.querySource) &&
    isNonEmptyString(event.status) &&
    Number.isInteger(event.turnCount) &&
    Number(event.turnCount) >= 1
}

function hasInvalidTraceContext(event: JsonObject): boolean {
  const traceIdPresent = event.traceId !== undefined
  const spanIdPresent = event.spanId !== undefined
  if (!traceIdPresent && !spanIdPresent) return false
  if (spanIdPresent && !traceIdPresent) return true
  if (traceIdPresent && !isValidTraceId(event.traceId)) return true
  if (spanIdPresent && !isValidSpanId(event.spanId)) return true
  return false
}

function isActionLikeEvent(event: JsonObject): boolean {
  return isNonEmptyString(event.commandName) ||
    isNonEmptyString(event.toolName) ||
    event.exitCode !== undefined ||
    event.passed !== undefined
}

function summarizeTrace(path: string): TraceSchemaSummary {
  const absolutePath = resolve(root, path)
  const text = readFileSync(absolutePath, 'utf8')
  const lines = text.split(/\r?\n/).filter((line) => line.trim().length > 0)
  let parseErrorCount = 0
  let requiredFieldViolationCount = 0
  let invalidTimestampCount = 0
  let invalidStatusCount = 0
  let invalidTraceContextCount = 0
  let missingRecommendedEventNameCount = 0
  let missingRecommendedTraceContextCount = 0
  let missingRecommendedActionObservationCount = 0
  let missingSweAgentTripletFieldCount = 0

  for (const line of lines) {
    try {
      const event = JSON.parse(line) as JsonObject
      if (!hasRequiredFields(event)) {
        requiredFieldViolationCount += 1
      }
      if (!isIsoTimestamp(event.timestamp)) {
        invalidTimestampCount += 1
      }
      if (!isNonEmptyString(event.status) || !allowedStatuses.includes(event.status)) {
        invalidStatusCount += 1
      }
      if (hasInvalidTraceContext(event)) {
        invalidTraceContextCount += 1
      }
      if (!isNonEmptyString(event.eventName)) {
        missingRecommendedEventNameCount += 1
      }
      if (!isValidTraceId(event.traceId) || !isValidSpanId(event.spanId)) {
        missingRecommendedTraceContextCount += 1
      }
      if (isActionLikeEvent(event) && (!isNonEmptyString(event.actionName) || !isNonEmptyString(event.observationSummary))) {
        missingRecommendedActionObservationCount += 1
      }
      if (isActionLikeEvent(event) && !isNonEmptyString(event.commandName)) {
        missingSweAgentTripletFieldCount += 1
      }
    } catch {
      parseErrorCount += 1
      requiredFieldViolationCount += 1
    }
  }

  const credentialPatternFound = hasCredentialPattern(text)
  const schemaContractPassed = lines.length > 0 &&
    parseErrorCount === 0 &&
    requiredFieldViolationCount === 0 &&
    invalidTimestampCount === 0 &&
    invalidStatusCount === 0 &&
    invalidTraceContextCount === 0 &&
    !credentialPatternFound

  return {
    path,
    sha256: sha256(text),
    currentGeneratedTraceProducer: currentGeneratedTraceProducerPaths.has(path),
    eventCount: lines.length,
    parseErrorCount,
    requiredFieldViolationCount,
    invalidTimestampCount,
    invalidStatusCount,
    invalidTraceContextCount,
    missingRecommendedEventNameCount,
    missingRecommendedTraceContextCount,
    missingRecommendedActionObservationCount,
    missingSweAgentTripletFieldCount,
    credentialPatternFound,
    schemaContractPassed,
  }
}

function buildAlignmentGaps(summaries: TraceSchemaSummary[]): AlignmentGap[] {
  const missingEventName = summaries.reduce((total, summary) => total + summary.missingRecommendedEventNameCount, 0)
  const missingTraceContext = summaries.reduce((total, summary) => total + summary.missingRecommendedTraceContextCount, 0)
  const missingActionObservation = summaries.reduce((total, summary) => total + summary.missingRecommendedActionObservationCount, 0)
  return [
    {
      id: 'otel_event_name_not_universal',
      status: missingEventName > 0 ? 'classified_unresolved' : 'not_present',
      protectedActionRequired: false,
      detail: missingEventName > 0
        ? `${missingEventName} current trace events lack optional OTel-style eventName; this blocks stronger schema portability claims but not the local v1 contract.`
        : 'All current trace events include eventName.',
    },
    {
      id: 'otel_trace_context_not_universal',
      status: missingTraceContext > 0 ? 'classified_unresolved' : 'not_present',
      protectedActionRequired: false,
      detail: missingTraceContext > 0
        ? `${missingTraceContext} current trace events lack complete traceId/spanId context; this blocks stronger observability interoperability claims.`
        : 'All current trace events include complete traceId/spanId context.',
    },
    {
      id: 'swe_agent_action_observation_triplet_not_universal',
      status: missingActionObservation > 0 ? 'classified_unresolved' : 'not_present',
      protectedActionRequired: false,
      detail: missingActionObservation > 0
        ? `${missingActionObservation} action-like events lack actionName/observationSummary fields; this remains an internal trace-shape gap before claiming SWE-agent trajectory parity.`
        : 'Action-like events include actionName and observationSummary.',
    },
  ]
}

function writeReports(report: TraceSchemaContractReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(
    resolve(docsDir, 'trace-schema-contract-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )

  const lines = [
    '# Trace Schema Contract Report',
    '',
    'Generated by: `bun run product:trace-schema-contract`',
    '',
    '## Claim Boundary',
    '',
    '- This report validates existing local `reports/orchestra-*.jsonl` trace artifacts only.',
    '- It does not call providers, live models, or external services.',
    '- It does not execute protected actions or mutate production repositories.',
    '- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Primary Sources',
    '',
    ...report.primarySourceInputs.map((source) => `- ${source.sourceProject}: ${source.sourceUrl}`),
    '',
    '## Summary',
    '',
    `- schema_contract_version: \`${report.schemaContractVersion}\``,
    `- source_real_trace_eval_report: \`${report.sourceRealTraceEvalReportPath}\``,
    `- trace_count: \`${report.aggregate.traceCount}\``,
    `- event_count: \`${report.aggregate.eventCount}\``,
    `- schema_passed_trace_count: \`${report.aggregate.schemaPassedTraceCount}\``,
    `- schema_failed_trace_count: \`${report.aggregate.schemaFailedTraceCount}\``,
    `- missing_recommended_event_name_count: \`${report.aggregate.missingRecommendedEventNameCount}\``,
    `- missing_recommended_trace_context_count: \`${report.aggregate.missingRecommendedTraceContextCount}\``,
    `- missing_recommended_action_observation_count: \`${report.aggregate.missingRecommendedActionObservationCount}\``,
    `- missing_swe_agent_triplet_field_count: \`${report.aggregate.missingSweAgentTripletFieldCount}\``,
    `- current_generated_trace_producer_trace_count: \`${report.aggregate.currentGeneratedTraceProducerTraceCount}\``,
    `- current_generated_trace_producer_event_count: \`${report.aggregate.currentGeneratedTraceProducerEventCount}\``,
    `- current_generated_trace_producer_missing_event_name_count: \`${report.aggregate.currentGeneratedTraceProducerMissingEventNameCount}\``,
    `- current_generated_trace_producer_missing_trace_context_count: \`${report.aggregate.currentGeneratedTraceProducerMissingTraceContextCount}\``,
    `- current_generated_trace_producer_missing_action_observation_count: \`${report.aggregate.currentGeneratedTraceProducerMissingActionObservationCount}\``,
    '',
    '## Trace Summaries',
    '',
    '| Trace | Current Producer | Events | Parse Errors | Required Field Violations | Invalid Timestamp | Invalid Status | Invalid Trace Context | Missing Event Name | Missing Trace Context | Missing Action Observation | Credential Pattern | Contract Passed | SHA-256 |',
    '| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |',
    ...report.traceSchemaSummaries.map((summary) => (
      `| \`${summary.path}\` | \`${summary.currentGeneratedTraceProducer}\` | ${summary.eventCount} | ${summary.parseErrorCount} | ${summary.requiredFieldViolationCount} | ${summary.invalidTimestampCount} | ${summary.invalidStatusCount} | ${summary.invalidTraceContextCount} | ${summary.missingRecommendedEventNameCount} | ${summary.missingRecommendedTraceContextCount} | ${summary.missingRecommendedActionObservationCount} | \`${summary.credentialPatternFound}\` | \`${summary.schemaContractPassed}\` | \`${summary.sha256}\` |`
    )),
    '',
    '## Recommended Alignment Gaps',
    '',
    '| Gap | Status | Protected Action Required | Detail |',
    '| --- | --- | --- | --- |',
    ...report.recommendedAlignmentGaps.map((gap) => (
      `| \`${gap.id}\` | \`${gap.status}\` | \`${gap.protectedActionRequired}\` | ${gap.detail} |`
    )),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.schemaContractChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'trace-schema-contract-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  const sourceText = readFileSync(resolve(root, sourceRealTraceEvalReportPath), 'utf8')
  const sourceRealTraceEval = JSON.parse(sourceText) as RealTraceEvalReport
  const traceFiles = discoverPublishableTraceFiles({ root, traceDirectory })
  const traceSchemaSummaries = traceFiles.map((path) => summarizeTrace(path))
  const currentGeneratedTraceProducerSummaries = traceSchemaSummaries.filter((summary) => summary.currentGeneratedTraceProducer)
  const sourceTraceHashesMatch = traceSchemaSummaries.every((summary) => (
    sourceRealTraceEval.traces.some((trace) => trace.path === summary.path && trace.sha256 === summary.sha256)
  ))
  const aggregate = {
    traceCount: traceSchemaSummaries.length,
    eventCount: traceSchemaSummaries.reduce((total, summary) => total + summary.eventCount, 0),
    schemaPassedTraceCount: traceSchemaSummaries.filter((summary) => summary.schemaContractPassed).length,
    schemaFailedTraceCount: traceSchemaSummaries.filter((summary) => !summary.schemaContractPassed).length,
    missingRecommendedEventNameCount: traceSchemaSummaries.reduce((total, summary) => total + summary.missingRecommendedEventNameCount, 0),
    missingRecommendedTraceContextCount: traceSchemaSummaries.reduce((total, summary) => total + summary.missingRecommendedTraceContextCount, 0),
    missingRecommendedActionObservationCount: traceSchemaSummaries.reduce((total, summary) => total + summary.missingRecommendedActionObservationCount, 0),
    missingSweAgentTripletFieldCount: traceSchemaSummaries.reduce((total, summary) => total + summary.missingSweAgentTripletFieldCount, 0),
    currentGeneratedTraceProducerTraceCount: currentGeneratedTraceProducerSummaries.length,
    currentGeneratedTraceProducerEventCount: currentGeneratedTraceProducerSummaries.reduce((total, summary) => total + summary.eventCount, 0),
    currentGeneratedTraceProducerMissingEventNameCount: currentGeneratedTraceProducerSummaries.reduce((total, summary) => total + summary.missingRecommendedEventNameCount, 0),
    currentGeneratedTraceProducerMissingTraceContextCount: currentGeneratedTraceProducerSummaries.reduce((total, summary) => total + summary.missingRecommendedTraceContextCount, 0),
    currentGeneratedTraceProducerMissingActionObservationCount: currentGeneratedTraceProducerSummaries.reduce((total, summary) => total + summary.missingRecommendedActionObservationCount, 0),
  }
  const recommendedAlignmentGaps = buildAlignmentGaps(traceSchemaSummaries)
  const schemaContractChecks = [
    check('real trace eval report imported', sourceRealTraceEval.traceFileCount >= 1, sourceRealTraceEvalReportPath),
    check('trace files discovered', traceFiles.length === sourceRealTraceEval.traceFileCount, `${traceFiles.length}/${sourceRealTraceEval.traceFileCount}`),
    check('trace hashes match real-trace eval source', sourceTraceHashesMatch, sourceRealTraceEvalReportPath),
    check('all trace lines parse as JSON', traceSchemaSummaries.every((summary) => summary.parseErrorCount === 0), `${traceSchemaSummaries.reduce((total, summary) => total + summary.parseErrorCount, 0)} parse errors`),
    check('all trace events satisfy required v1 fields', traceSchemaSummaries.every((summary) => summary.requiredFieldViolationCount === 0), requiredEventFields.join(',')),
    check('all timestamps are parseable', traceSchemaSummaries.every((summary) => summary.invalidTimestampCount === 0), 'ISO-compatible timestamp strings'),
    check('all statuses are in contract enum', traceSchemaSummaries.every((summary) => summary.invalidStatusCount === 0), allowedStatuses.join(',')),
    check('trace context is valid when present', traceSchemaSummaries.every((summary) => summary.invalidTraceContextCount === 0), 'spanId requires valid traceId'),
    check('credential patterns absent from traces', traceSchemaSummaries.every((summary) => !summary.credentialPatternFound), 'known key/token/private-key patterns absent'),
    check('recommended gaps are classified without protected action', recommendedAlignmentGaps.every((gap) => ['classified_unresolved', 'not_present'].includes(gap.status) && gap.protectedActionRequired === false), `${recommendedAlignmentGaps.length} gaps`),
    check('current generated trace producer paths are assessed', aggregate.currentGeneratedTraceProducerTraceCount === currentGeneratedTraceProducerPaths.size, `${aggregate.currentGeneratedTraceProducerTraceCount}/${currentGeneratedTraceProducerPaths.size}`),
    check('current generated trace producers include recommended event names', aggregate.currentGeneratedTraceProducerMissingEventNameCount === 0, `${aggregate.currentGeneratedTraceProducerMissingEventNameCount} missing`),
    check('current generated trace producers include recommended trace context', aggregate.currentGeneratedTraceProducerMissingTraceContextCount === 0, `${aggregate.currentGeneratedTraceProducerMissingTraceContextCount} missing`),
    check('current generated trace producers include action-observation fields on action events', aggregate.currentGeneratedTraceProducerMissingActionObservationCount === 0, `${aggregate.currentGeneratedTraceProducerMissingActionObservationCount} missing`),
    check('all traces pass the local v1 schema contract', aggregate.schemaFailedTraceCount === 0, `${aggregate.schemaPassedTraceCount}/${aggregate.traceCount}`),
  ]

  const report: TraceSchemaContractReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_trace_schema_contract',
    schemaContractVersion: 'openclaude_trace_schema_contract_v1',
    sourceRealTraceEvalReportPath,
    sourceRealTraceEvalReportSha256: sha256(sourceText),
    sourceTraceDirectory: traceDirectory,
    sourceTraceFileCount: sourceRealTraceEval.traceFileCount,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    primarySourceInputs: [
      {
        sourceProject: 'OpenTelemetry Logs Data Model',
        sourceUrl: 'https://opentelemetry.io/docs/specs/otel/logs/data-model/',
        observedPattern: 'portable event records use named fields for timestamps, trace context, severity, body, attributes, and event names where semantics are stable.',
      },
      {
        sourceProject: 'SWE-agent trajectories',
        sourceUrl: 'https://github.com/SWE-agent/SWE-agent/blob/main/docs/usage/trajectories.md',
        observedPattern: 'software-engineering agent trajectories preserve per-step thought/action/observation style structure plus state and query context.',
      },
      {
        sourceProject: 'AgentLens',
        sourceUrl: 'https://arxiv.org/abs/2605.12925',
        observedPattern: 'process-level assessment needs structured trajectories rather than binary outcome-only pass/fail evidence.',
      },
    ],
    requiredEventFields,
    optionalRecommendedFields,
    allowedStatuses,
    traceSchemaSummaries,
    aggregate,
    recommendedAlignmentGaps,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    schemaContractChecks,
    claimBoundary: 'Local trace schema contract evidence only; no provider/live/external calls, protected actions, release readiness, production readiness, public readiness, external validation, or autonomous reliability claim is authorized.',
  }

  writeReports(report)

  for (const item of schemaContractChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  if (!schemaContractChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`schema_contract_version=${report.schemaContractVersion}`)
  console.log(`trace_count=${aggregate.traceCount}`)
  console.log(`event_count=${aggregate.eventCount}`)
  console.log(`schema_failed_trace_count=${aggregate.schemaFailedTraceCount}`)
  console.log(`recommended_alignment_gap_count=${recommendedAlignmentGaps.length}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
