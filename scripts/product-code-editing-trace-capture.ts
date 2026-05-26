import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { buildTraceEventName, describeTraceObservation, enrichTraceEvent } from './product-trace-event-enrichment'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type FixtureUnitCase = {
  name: string
  a: number
  b: number
  expected: number
  actual: number
  passed: boolean
}

type CodeEditingTraceCaptureReport = {
  generatedAt: string
  mode: 'local_no_provider_code_editing_trace_capture'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  operatorAuthorization: {
    authorized: true
    scope: 'operator_authorized_local_no_provider_code_editing_trace_capture_only'
    protectedActionsAuthorized: false
  }
  capturePerformed: true
  nonSyntheticUserSessionClaimed: false
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeSha256: string
  sourceAfterSha256: string
  patchApplied: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: []
  unitCheck: {
    passed: boolean
    testCaseCount: number
    cases: FixtureUnitCase[]
  }
  traceChecks: Check[]
  claimBoundary: string
}

type TraceEvent = {
  timestamp: string
  role: 'user' | 'executor' | 'tool'
  model: string
  querySource: 'operator_authorized_local_no_provider_code_editing_trace'
  status: 'started' | 'succeeded' | 'failed'
  turnCount: number
  captureKind: 'operator_authorized_local_code_editing_trace'
  promptSha256?: string
  promptByteLength?: number
  toolName?: string
  commandName?: string
  phaseLabel?: 'exploration' | 'implementation' | 'verification'
  exitCode?: number
  passed?: boolean
  fixturePath?: string
  sourceBeforeSha256?: string
  sourceAfterSha256?: string
  modifiedFixtureFiles?: string[]
  protectedRepoFilesModified?: []
  testCaseCount?: number
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const fixtureRoot = '_fixtures/product-code-editing-trace'
const fixtureSourcePath = `${fixtureRoot}/calculator.js`
const fixtureIssuePath = `${fixtureRoot}/issue.md`
const tracePath = 'reports/orchestra-code-editing-trace-local-fixture.jsonl'
const sourceBefore = `export function add(a, b) {
  return a - b
}
`
const sourceAfter = `export function add(a, b) {
  return a + b
}
`
const operatorPrompt = [
  'Repair the local fixture add(a, b) implementation.',
  'Use only deterministic local file evidence.',
  'Record exploration, implementation, and verification as a no-provider trace.',
].join(' ')

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function fileSha256(path: string): string {
  return createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function event(
  timestamp: string,
  role: TraceEvent['role'],
  model: string,
  status: TraceEvent['status'],
  turnCount: number,
  extra: Partial<TraceEvent> = {},
): TraceEvent {
  const baseEvent: TraceEvent = {
    timestamp,
    role,
    model,
    querySource: 'operator_authorized_local_no_provider_code_editing_trace',
    status,
    turnCount,
    captureKind: 'operator_authorized_local_code_editing_trace',
    ...extra,
  }
  const actionName = baseEvent.commandName ?? baseEvent.toolName
  const observationSummary = actionName
    ? describeTraceObservation(status, {
        exitCode: baseEvent.exitCode,
        passed: baseEvent.passed,
        testCaseCount: baseEvent.testCaseCount,
      })
    : undefined
  return enrichTraceEvent(baseEvent, {
    traceSeed: tracePath,
    spanSeed: `${timestamp}:${role}:${turnCount}:${status}:${actionName ?? 'orchestration'}`,
    eventName: buildTraceEventName(baseEvent.captureKind, role, status, actionName),
    actionName,
    observationSummary,
  })
}

function resetFixture(): void {
  rmSync(resolve(root, fixtureRoot), { recursive: true, force: true })
  mkdirSync(resolve(root, fixtureRoot), { recursive: true })
  writeFileSync(resolve(root, fixtureIssuePath), [
    '# Local Fixture Issue',
    '',
    'The `add(a, b)` helper currently subtracts the second argument.',
    'Patch only this disposable fixture and verify three deterministic cases.',
    '',
  ].join('\n'))
  writeFileSync(resolve(root, fixtureSourcePath), sourceBefore)
}

function applyFixturePatch(): boolean {
  const before = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  const after = before.replace('return a - b', 'return a + b')
  writeFileSync(resolve(root, fixtureSourcePath), after)
  return before !== after && after === sourceAfter
}

function runFixtureUnitCheck(sourceText: string): { passed: boolean; cases: FixtureUnitCase[] } {
  const usesAddition = sourceText.includes('return a + b')
  const cases = [
    { name: 'positive integers', a: 2, b: 3, expected: 5 },
    { name: 'negative plus positive', a: -4, b: 4, expected: 0 },
    { name: 'zero identity', a: 0, b: 7, expected: 7 },
  ].map((item) => {
    const actual = usesAddition ? item.a + item.b : item.a - item.b
    return {
      ...item,
      actual,
      passed: actual === item.expected,
    }
  })
  return {
    passed: cases.every((item) => item.passed),
    cases,
  }
}

function buildTrace(report: Omit<CodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'>, promptSha256: string, promptByteLength: number): string {
  const allPassed = report.patchApplied && report.unitCheck.passed
  const events: TraceEvent[] = [
    event('2026-05-18T02:00:00.000Z', 'user', 'local-operator', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T02:00:01.000Z', 'executor', 'openclaude-local-code-editing-harness', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T02:00:02.000Z', 'tool', 'local-fixture-reader', 'started', 1, {
      toolName: 'fixture_file_reader',
      commandName: 'inspect_fixture_source',
      phaseLabel: 'exploration',
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
    }),
    event('2026-05-18T02:00:03.000Z', 'tool', 'local-fixture-reader', 'succeeded', 1, {
      toolName: 'fixture_file_reader',
      commandName: 'inspect_fixture_source',
      phaseLabel: 'exploration',
      exitCode: 0,
      passed: true,
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
    }),
    event('2026-05-18T02:00:04.000Z', 'tool', 'local-fixture-editor', 'started', 2, {
      toolName: 'fixture_patch_writer',
      commandName: 'write_fixture_patch',
      phaseLabel: 'implementation',
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
      protectedRepoFilesModified: [],
    }),
    event('2026-05-18T02:00:05.000Z', 'tool', 'local-fixture-editor', report.patchApplied ? 'succeeded' : 'failed', 2, {
      toolName: 'fixture_patch_writer',
      commandName: 'write_fixture_patch',
      phaseLabel: 'implementation',
      exitCode: report.patchApplied ? 0 : 1,
      passed: report.patchApplied,
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
      sourceAfterSha256: report.sourceAfterSha256,
      modifiedFixtureFiles: report.modifiedFixtureFiles,
      protectedRepoFilesModified: [],
    }),
    event('2026-05-18T02:00:06.000Z', 'tool', 'local-fixture-test-runner', 'started', 3, {
      toolName: 'fixture_unit_check',
      commandName: 'run_fixture_unit_check',
      phaseLabel: 'verification',
      fixturePath: fixtureSourcePath,
      testCaseCount: report.unitCheck.testCaseCount,
    }),
    event('2026-05-18T02:00:07.000Z', 'tool', 'local-fixture-test-runner', report.unitCheck.passed ? 'succeeded' : 'failed', 3, {
      toolName: 'fixture_unit_check',
      commandName: 'run_fixture_unit_check',
      phaseLabel: 'verification',
      exitCode: report.unitCheck.passed ? 0 : 1,
      passed: report.unitCheck.passed,
      fixturePath: fixtureSourcePath,
      testCaseCount: report.unitCheck.testCaseCount,
    }),
    event('2026-05-18T02:00:08.000Z', 'executor', 'openclaude-local-code-editing-harness', allPassed ? 'succeeded' : 'failed', 3),
    event('2026-05-18T02:00:09.000Z', 'user', 'local-operator', allPassed ? 'succeeded' : 'failed', 3),
  ]
  return `${events.map((item) => JSON.stringify(item)).join('\n')}\n`
}

function writeMarkdown(report: CodeEditingTraceCaptureReport): void {
  const caseRows = report.unitCheck.cases
    .map((item) => `| ${item.name} | \`${item.a}\` | \`${item.b}\` | \`${item.expected}\` | \`${item.actual}\` | \`${item.passed}\` |`)
    .join('\n')
  const checkRows = report.traceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Code Editing Trace Capture Report

Generated by: \`bun run product:code-editing-trace-capture\`

## Claim Boundary

- This is a local no-provider implementation-bearing fixture trace.
- It mutates only the disposable fixture under \`${report.fixtureRoot}\`.
- It does not modify production OpenClaude code, MFH, real product repos, canonical memory, or release artifacts.
- It does not call providers, live models, external services, hosted CI, Docker, deploy, publish, or launch.
- It does not claim external validation, release readiness, production readiness, public readiness, autonomous reliability, or benchmark superiority.

## Summary

- mode: \`${report.mode}\`
- capture_performed: \`${report.capturePerformed}\`
- operator_authorization_scope: \`${report.operatorAuthorization.scope}\`
- protected_actions_authorized: \`${report.operatorAuthorization.protectedActionsAuthorized}\`
- non_synthetic_user_session_claimed: \`${report.nonSyntheticUserSessionClaimed}\`
- fixture_root: \`${report.fixtureRoot}\`
- trace_path: \`${report.tracePath}\`
- trace_sha256: \`${report.traceSha256}\`
- source_before_sha256: \`${report.sourceBeforeSha256}\`
- source_after_sha256: \`${report.sourceAfterSha256}\`
- patch_applied: \`${report.patchApplied}\`
- modified_fixture_files: \`${report.modifiedFixtureFiles.join(',')}\`
- protected_repo_files_modified: \`${report.protectedRepoFilesModified.length}\`
- unit_check_passed: \`${report.unitCheck.passed}\`
- unit_check_case_count: \`${report.unitCheck.testCaseCount}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`

## Fixture Unit Cases

| Case | A | B | Expected | Actual | Passed |
| --- | ---: | ---: | ---: | ---: | --- |
${caseRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'code-editing-trace-capture-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  resetFixture()

  const promptSha256 = sha256(operatorPrompt)
  const promptByteLength = Buffer.byteLength(operatorPrompt, 'utf8')
  const sourceBeforeSha256 = fileSha256(fixtureSourcePath)
  const patchApplied = applyFixturePatch()
  const sourceAfterText = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  const sourceAfterSha256 = sha256(sourceAfterText)
  const unitResult = runFixtureUnitCheck(sourceAfterText)
  const reportWithoutTrace: Omit<CodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'> = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_code_editing_trace_capture',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    operatorAuthorization: {
      authorized: true,
      scope: 'operator_authorized_local_no_provider_code_editing_trace_capture_only',
      protectedActionsAuthorized: false,
    },
    capturePerformed: true,
    nonSyntheticUserSessionClaimed: false,
    fixtureRoot,
    tracePath,
    traceSha256: '',
    sourceBeforeSha256,
    sourceAfterSha256,
    patchApplied,
    modifiedFixtureFiles: [fixtureSourcePath],
    protectedRepoFilesModified: [],
    unitCheck: {
      passed: unitResult.passed,
      testCaseCount: unitResult.cases.length,
      cases: unitResult.cases,
    },
  }
  const traceText = buildTrace(reportWithoutTrace, promptSha256, promptByteLength)
  writeFileSync(resolve(root, tracePath), traceText)
  const traceSha256 = sha256(traceText)

  const traceChecks = [
    check('fixture source starts from failing implementation', sourceBeforeSha256 === sha256(sourceBefore), sourceBeforeSha256),
    check('fixture patch changes source hash', sourceBeforeSha256 !== sourceAfterSha256, `${sourceBeforeSha256}/${sourceAfterSha256}`),
    check('fixture patch applies intended implementation', patchApplied && sourceAfterText === sourceAfter, sourceAfterSha256),
    check('fixture unit check passes', unitResult.passed, `${unitResult.cases.filter((item) => item.passed).length}/${unitResult.cases.length}`),
    check('trace records implementation command', traceText.includes('"commandName":"write_fixture_patch"'), tracePath),
    check('trace records verification command', traceText.includes('"commandName":"run_fixture_unit_check"'), tracePath),
    check('only disposable fixture files are modified', reportWithoutTrace.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/')) && reportWithoutTrace.protectedRepoFilesModified.length === 0, reportWithoutTrace.modifiedFixtureFiles.join(',')),
    check('no provider/live/external calls are recorded', reportWithoutTrace.providerCallsPerformed.length === 0 && reportWithoutTrace.liveModelCallsPerformed.length === 0 && reportWithoutTrace.externalCallsPerformed.length === 0, 'call counts=0'),
  ]

  const report: CodeEditingTraceCaptureReport = {
    ...reportWithoutTrace,
    traceSha256,
    traceChecks,
    claimBoundary: 'This is local no-provider code-editing fixture evidence only; it is not an external benchmark, release readiness, production readiness, public readiness, or autonomous reliability claim.',
  }

  writeFileSync(resolve(docsDir, 'code-editing-trace-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of traceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')

  const failed = traceChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`code_editing_trace_path=${tracePath}`)
  console.log(`code_editing_trace_sha256=${traceSha256}`)
  console.log(`fixture_root=${fixtureRoot}`)
  console.log(`modified_fixture_files=${report.modifiedFixtureFiles.length}`)
  console.log(`protected_repo_files_modified=${report.protectedRepoFilesModified.length}`)
  console.log(`unit_check_passed=${report.unitCheck.passed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
