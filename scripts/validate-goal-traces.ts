import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

export type GoalTraceEvent = {
  timestamp: string
  eventName: string
  status: 'started' | 'succeeded' | 'failed' | 'cancelled'
  actor: string
  summary: string
  checkpointId?: string
  command?: string
  exitCode?: number
  evidenceArtifacts?: string[]
  disallowedClaimsFound?: boolean
}

export type GoalTrace = {
  goalId: string
  traceId: string
  claimBoundary: {
    allowed: string[]
    forbidden: string[]
  }
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  events: GoalTraceEvent[]
}

type TraceInput = {
  path: string
  trace: GoalTrace
  sha256?: string
}

export type GoalTraceValidationResult = {
  path?: string
  goalId: string | null
  traceId: string | null
  ok: boolean
  errors: string[]
  eventSequence: string[]
  sha256?: string
}

export type GoalTraceValidationReport = {
  generatedAt: string
  mode: 'local_no_provider_goal_trace_validation'
  traceDirectory: string
  traceFileCount: number
  validTraceCount: number
  invalidTraceCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  validationResults: GoalTraceValidationResult[]
  traceChecks: Array<{
    label: string
    ok: boolean
    detail: string
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  claimBoundary: string
}

const root = process.cwd()
const traceDirectory = 'docs/goals/traces'
const goalDirectory = 'docs/goals'
const reportDir = 'docs/product-quality'
const reportJsonPath = 'docs/product-quality/goal-trace-validation-report.json'
const reportMdPath = 'docs/product-quality/goal-trace-validation-report.md'
const credentialPatterns = [
  /AKIA[0-9A-Z]{16}/,
  /ASIA[0-9A-Z]{16}/,
  /sk-[A-Za-z0-9_-]{20,}/,
  /xox[baprs]-[A-Za-z0-9-]{10,}/,
  /gh[pousr]_[A-Za-z0-9_]{30,}/,
  /github_pat_[A-Za-z0-9_]{30,}/,
  /-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----/,
]

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function hasNonEmptyString(value: unknown): value is string {
  return typeof value === 'string' && value.trim().length > 0
}

function hasCredentialPattern(value: unknown): boolean {
  return credentialPatterns.some((pattern) => pattern.test(JSON.stringify(value)))
}

function isValidTraceId(value: unknown): boolean {
  return hasNonEmptyString(value) && /^[a-f0-9]{32}$/i.test(value)
}

function isIsoTimestamp(value: unknown): value is string {
  return hasNonEmptyString(value) && !Number.isNaN(Date.parse(value))
}

function isNonEmptyArray(value: unknown): value is unknown[] {
  return Array.isArray(value) && value.length > 0
}

function arrayMustBeEmpty(trace: GoalTrace, field: keyof Pick<
  GoalTrace,
  'providerCallsPerformed' | 'liveModelCallsPerformed' | 'externalCallsPerformed' | 'protectedActionsExecuted'
>, errors: string[]): void {
  if (!Array.isArray(trace[field]) || trace[field].length > 0) {
    errors.push(`${field} must be empty`)
  }
}

function eventIndex(trace: GoalTrace, eventName: string): number {
  return trace.events.findIndex((event) => event.eventName === eventName)
}

function hasSuccessfulValidationEvidence(trace: GoalTrace): boolean {
  return trace.events.some((event) => (
    event.eventName === 'validation.ran' &&
    event.status === 'succeeded' &&
    hasNonEmptyString(event.command) &&
    event.exitCode === 0 &&
    isNonEmptyArray(event.evidenceArtifacts)
  ))
}

function hasCleanClaimReview(trace: GoalTrace): boolean {
  const reviewIndex = eventIndex(trace, 'claim.reviewed')
  const validatedIndex = eventIndex(trace, 'goal.validated')
  if (reviewIndex === -1 || validatedIndex === -1 || reviewIndex > validatedIndex) {
    return false
  }
  return trace.events.some((event) => (
    event.eventName === 'claim.reviewed' &&
    event.status === 'succeeded' &&
    event.disallowedClaimsFound === false
  ))
}

function eventSequenceIsChronological(events: GoalTraceEvent[]): boolean {
  let previous = 0
  for (const event of events) {
    if (!isIsoTimestamp(event.timestamp)) return false
    const current = Date.parse(event.timestamp)
    if (current < previous) return false
    previous = current
  }
  return true
}

export function evaluateGoalTrace(
  trace: GoalTrace,
  knownGoalIds: Set<string>,
  path?: string,
  sha256?: string,
): GoalTraceValidationResult {
  const errors: string[] = []

  if (!hasNonEmptyString(trace.goalId)) {
    errors.push('goalId must be a non-empty string')
  } else if (!knownGoalIds.has(trace.goalId)) {
    errors.push('goalId must refer to a known docs/goals/CG-*.md goal')
  }

  if (!isValidTraceId(trace.traceId)) {
    errors.push('traceId must be 32 hex characters')
  }

  if (!isRecord(trace.claimBoundary)) {
    errors.push('claimBoundary must be an object')
  } else {
    if (!isNonEmptyArray(trace.claimBoundary.allowed)) {
      errors.push('claimBoundary.allowed must contain at least one item')
    }
    if (!isNonEmptyArray(trace.claimBoundary.forbidden)) {
      errors.push('claimBoundary.forbidden must contain at least one item')
    }
  }

  arrayMustBeEmpty(trace, 'providerCallsPerformed', errors)
  arrayMustBeEmpty(trace, 'liveModelCallsPerformed', errors)
  arrayMustBeEmpty(trace, 'externalCallsPerformed', errors)
  arrayMustBeEmpty(trace, 'protectedActionsExecuted', errors)

  if (!isNonEmptyArray(trace.events)) {
    errors.push('events must contain at least one item')
  } else {
    trace.events.forEach((event, index) => {
      if (!hasNonEmptyString(event.eventName)) {
        errors.push(`events.${index}.eventName must be a non-empty string`)
      }
      if (!isIsoTimestamp(event.timestamp)) {
        errors.push(`events.${index}.timestamp must be an ISO-compatible timestamp`)
      }
      if (!hasNonEmptyString(event.actor)) {
        errors.push(`events.${index}.actor must be a non-empty string`)
      }
      if (!hasNonEmptyString(event.summary)) {
        errors.push(`events.${index}.summary must be a non-empty string`)
      }
    })

    if (!eventSequenceIsChronological(trace.events)) {
      errors.push('events must be chronological')
    }
  }

  const loadedIndex = eventIndex(trace, 'goal.loaded')
  const validatedIndex = eventIndex(trace, 'goal.validated')
  if (loadedIndex !== 0) {
    errors.push('trace must start with goal.loaded')
  }
  if (validatedIndex === -1) {
    errors.push('trace must include goal.validated')
  }
  if (validatedIndex !== -1 && loadedIndex !== -1 && validatedIndex <= loadedIndex) {
    errors.push('goal.validated must occur after goal.loaded')
  }
  if (eventIndex(trace, 'checkpoint.completed') === -1) {
    errors.push('trace must include at least one checkpoint.completed event')
  }
  if (validatedIndex !== -1 && !hasSuccessfulValidationEvidence(trace)) {
    errors.push('validated traces require a successful validation.ran event with command, exitCode 0, and evidence artifact')
  }
  if (validatedIndex !== -1 && !hasCleanClaimReview(trace)) {
    errors.push('validated traces require claim.reviewed with disallowedClaimsFound=false before goal.validated')
  }
  if (hasCredentialPattern(trace)) {
    errors.push('trace must not contain credential-like patterns')
  }

  return {
    path,
    goalId: hasNonEmptyString(trace.goalId) ? trace.goalId : null,
    traceId: hasNonEmptyString(trace.traceId) ? trace.traceId : null,
    ok: errors.length === 0,
    errors,
    eventSequence: Array.isArray(trace.events) ? trace.events.map((event) => event.eventName) : [],
    sha256,
  }
}

export function buildGoalTraceReport(
  traceFiles: TraceInput[],
  knownGoalIds: Set<string>,
): GoalTraceValidationReport {
  const validationResults = traceFiles.map((input) =>
    evaluateGoalTrace(input.trace, knownGoalIds, input.path, input.sha256),
  )
  const traceChecks = [
    {
      label: 'goal trace files discovered',
      ok: traceFiles.length > 0,
      detail: `${traceFiles.length} trace files`,
    },
    {
      label: 'all goal traces pass MFH closure policy',
      ok: validationResults.every((result) => result.ok),
      detail: `${validationResults.filter((result) => result.ok).length}/${validationResults.length} valid`,
    },
    {
      label: 'no provider/live/external/protected side effects recorded',
      ok: validationResults.every((result) => result.ok) && traceFiles.every((input) => (
        input.trace.providerCallsPerformed.length === 0 &&
        input.trace.liveModelCallsPerformed.length === 0 &&
        input.trace.externalCallsPerformed.length === 0 &&
        input.trace.protectedActionsExecuted.length === 0
      )),
      detail: 'side-effect arrays are empty in all valid traces',
    },
  ]

  return {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_goal_trace_validation',
    traceDirectory,
    traceFileCount: traceFiles.length,
    validTraceCount: validationResults.filter((result) => result.ok).length,
    invalidTraceCount: validationResults.filter((result) => !result.ok).length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    validationResults,
    traceChecks,
    primarySourceInputs: [
      {
        sourceProject: 'OpenTelemetry',
        sourceUrl: 'https://opentelemetry.io/',
        observedPattern: 'Trace-style evidence should preserve ordered events and no-provider boundaries before stronger observability claims.',
      },
      {
        sourceProject: 'Open Policy Agent',
        sourceUrl: 'https://www.openpolicyagent.org/docs',
        observedPattern: 'Policy decisions should be evaluated against structured input rather than prose-only claims.',
      },
      {
        sourceProject: 'OpenAI Agent Evals',
        sourceUrl: 'https://developers.openai.com/api/docs/guides/agent-evals',
        observedPattern: 'Agent workflow quality improves when traces, graders, datasets, and eval runs are separated by evidence level.',
      },
      {
        sourceProject: 'NIST AI RMF Playbook',
        sourceUrl: 'https://airc.nist.gov/airmf-resources/playbook/',
        observedPattern: 'Govern, Map, Measure, and Manage actions should be selected proportionally and recorded as voluntary risk-management evidence.',
      },
    ],
    claimBoundary: 'Goal trace validation is local no-provider behavioral governance evidence only. It does not prove production readiness, release readiness, public readiness, external validation, benchmark superiority, or autonomous reliability.',
  }
}

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function listKnownGoalIds(): Set<string> {
  const absoluteGoalDir = resolve(root, goalDirectory)
  if (!existsSync(absoluteGoalDir)) return new Set()
  return new Set(readdirSync(absoluteGoalDir)
    .map((name) => name.match(/^(CG-\d+)-.*\.md$/i)?.[1]?.toUpperCase())
    .filter((value): value is string => hasNonEmptyString(value)))
}

function listTraceFiles(): TraceInput[] {
  const absoluteTraceDir = resolve(root, traceDirectory)
  if (!existsSync(absoluteTraceDir)) return []
  return readdirSync(absoluteTraceDir)
    .filter((name) => /^CG-\d+-.*\.trace\.json$/i.test(name))
    .sort((left, right) => left.localeCompare(right))
    .map((name) => {
      const path = `${traceDirectory}/${name}`
      const text = readFileSync(resolve(root, path), 'utf8')
      return {
        path,
        trace: JSON.parse(text) as GoalTrace,
        sha256: sha256(text),
      }
    })
}

function writeReport(report: GoalTraceValidationReport): void {
  mkdirSync(resolve(root, reportDir), { recursive: true })
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# Goal Trace Validation Report',
    '',
    'Generated by: `bun run goals:trace:validate`',
    '',
    '## Claim Boundary',
    '',
    `- ${report.claimBoundary}`,
    '- The trace gate performs no provider, live model, external, or protected calls.',
    '',
    '## Summary',
    '',
    `- trace_directory: \`${report.traceDirectory}\``,
    `- trace_file_count: \`${report.traceFileCount}\``,
    `- valid_trace_count: \`${report.validTraceCount}\``,
    `- invalid_trace_count: \`${report.invalidTraceCount}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    `- protected_actions_executed: \`${report.protectedActionsExecuted.length}\``,
    '',
    '## Primary Source Inputs',
    '',
    '| Source | URL | Pattern Absorbed |',
    '| --- | --- | --- |',
    ...report.primarySourceInputs.map((source) => (
      `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`
    )),
    '',
    '## Trace Results',
    '',
    '| Trace | Goal | Events | Passed | SHA-256 | Errors |',
    '| --- | --- | --- | --- | --- | --- |',
    ...report.validationResults.map((result) => (
      `| \`${result.path ?? 'memory'}\` | \`${result.goalId ?? 'unknown'}\` | \`${result.eventSequence.join(' -> ')}\` | \`${result.ok}\` | \`${result.sha256 ?? 'n/a'}\` | ${result.errors.length === 0 ? 'none' : result.errors.map((error) => `\`${error}\``).join('<br>')} |`
    )),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.traceChecks.map((check) => `| ${check.label} | \`${check.ok}\` | ${check.detail} |`),
    '',
  ]

  writeFileSync(resolve(root, reportMdPath), `${lines.join('\n')}\n`)
}

function main(): void {
  const report = buildGoalTraceReport(listTraceFiles(), listKnownGoalIds())
  writeReport(report)

  for (const result of report.validationResults) {
    console.log(`${result.ok ? 'PASS' : 'FAIL'}: ${result.path} (${result.goalId ?? 'unknown'})`)
    for (const error of result.errors) {
      console.log(`  - ${error}`)
    }
  }
  for (const check of report.traceChecks) {
    console.log(`${check.ok ? 'PASS' : 'FAIL'}: ${check.label} (${check.detail})`)
  }
  console.log('')
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (report.traceFileCount === 0 || report.invalidTraceCount > 0 || !report.traceChecks.every((check) => check.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
}

if (import.meta.main) {
  main()
}
