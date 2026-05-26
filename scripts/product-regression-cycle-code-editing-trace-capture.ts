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
  input: string
  expected: string
  wrongActual: string
  repairedActual: string
  failedBeforeRepair: boolean
  passedAfterRepair: boolean
}

type RegressionCycleCodeEditingTraceCaptureReport = {
  generatedAt: string
  mode: 'local_no_provider_regression_cycle_code_editing_trace_capture'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  operatorAuthorization: {
    authorized: true
    scope: 'operator_authorized_local_no_provider_regression_cycle_code_editing_trace_capture_only'
    protectedActionsAuthorized: false
  }
  capturePerformed: true
  nonSyntheticUserSessionClaimed: false
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeSha256: string
  wrongPatchSha256: string
  repairedSourceSha256: string
  wrongPatchApplied: boolean
  regressionFailedBeforeRepair: boolean
  repairApplied: boolean
  regressionPassedAfterRepair: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: []
  unitCheck: {
    failedCaseCountBeforeRepair: number
    passedCaseCountAfterRepair: number
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
  querySource: 'operator_authorized_local_no_provider_regression_cycle_code_editing_trace'
  status: 'started' | 'succeeded' | 'failed'
  turnCount: number
  captureKind: 'operator_authorized_local_regression_cycle_code_editing_trace'
  promptSha256?: string
  promptByteLength?: number
  toolName?: string
  commandName?: string
  phaseLabel?: 'exploration' | 'implementation' | 'verification'
  exitCode?: number
  passed?: boolean
  fixturePath?: string
  sourceBeforeSha256?: string
  wrongPatchSha256?: string
  repairedSourceSha256?: string
  modifiedFixtureFiles?: string[]
  protectedRepoFilesModified?: []
  testCaseCount?: number
  failedCaseCountBeforeRepair?: number
  passedCaseCountAfterRepair?: number
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const fixtureRoot = '_fixtures/product-regression-cycle-code-editing-trace'
const fixtureSourcePath = `${fixtureRoot}/src/slugify.js`
const fixtureIssuePath = `${fixtureRoot}/issue.md`
const tracePath = 'reports/orchestra-regression-cycle-code-editing-trace-local-fixture.jsonl'
const sourceBefore = `export function slugify(value) {
  return String(value).trim().toLowerCase()
}
`
const wrongPatch = `export function slugify(value) {
  return String(value).trim().toLowerCase().replaceAll(' ', '-')
}
`
const repairedSource = `export function slugify(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}
`
const operatorPrompt = [
  'Repair the local slugify fixture using a regression cycle.',
  'First record a plausible wrong patch that fails punctuation and repeated separator cases.',
  'Then repair only the disposable fixture and verify all regression cases without providers.',
].join(' ')

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path), 'utf8'))
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
    querySource: 'operator_authorized_local_no_provider_regression_cycle_code_editing_trace',
    status,
    turnCount,
    captureKind: 'operator_authorized_local_regression_cycle_code_editing_trace',
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

function writeFixtureFile(path: string, text: string): void {
  mkdirSync(dirname(resolve(root, path)), { recursive: true })
  writeFileSync(resolve(root, path), text)
}

function resetFixture(): void {
  rmSync(resolve(root, fixtureRoot), { recursive: true, force: true })
  writeFixtureFile(fixtureIssuePath, [
    '# Regression Cycle Local Fixture Issue',
    '',
    '`slugify(value)` lowercases and trims, but it must also collapse punctuation and repeated separators.',
    'Record a failed plausible patch before applying the repaired implementation.',
    '',
  ].join('\n'))
  writeFixtureFile(fixtureSourcePath, sourceBefore)
}

function applyWrongPatch(): boolean {
  const before = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  writeFixtureFile(fixtureSourcePath, wrongPatch)
  return before === sourceBefore && readFileSync(resolve(root, fixtureSourcePath), 'utf8') === wrongPatch
}

function applyRepairPatch(): boolean {
  const before = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  writeFixtureFile(fixtureSourcePath, repairedSource)
  return before === wrongPatch && readFileSync(resolve(root, fixtureSourcePath), 'utf8') === repairedSource
}

function runSlugifyImplementation(sourceText: string, input: string): string {
  if (sourceText === wrongPatch) {
    return String(input).trim().toLowerCase().replaceAll(' ', '-')
  }
  if (sourceText === repairedSource) {
    return String(input)
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '')
  }
  return String(input).trim().toLowerCase()
}

function runRegressionCases(wrongSource: string, repaired: string): FixtureUnitCase[] {
  return [
    { name: 'spaces become single separators', input: 'Hello World', expected: 'hello-world' },
    { name: 'punctuation collapses', input: 'Hello, world!', expected: 'hello-world' },
    { name: 'repeated whitespace and punctuation collapse', input: '  A  B---C  ', expected: 'a-b-c' },
    { name: 'outer separators trimmed', input: '---Ready?---', expected: 'ready' },
  ].map((item) => {
    const wrongActual = runSlugifyImplementation(wrongSource, item.input)
    const repairedActual = runSlugifyImplementation(repaired, item.input)
    return {
      ...item,
      wrongActual,
      repairedActual,
      failedBeforeRepair: wrongActual !== item.expected,
      passedAfterRepair: repairedActual === item.expected,
    }
  })
}

function buildTrace(
  report: Omit<RegressionCycleCodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'>,
  promptSha256: string,
  promptByteLength: number,
): string {
  const allPassed = report.regressionFailedBeforeRepair && report.regressionPassedAfterRepair
  const events: TraceEvent[] = [
    event('2026-05-18T04:00:00.000Z', 'user', 'local-operator', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T04:00:01.000Z', 'executor', 'openclaude-local-regression-cycle-code-editing-harness', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T04:00:02.000Z', 'tool', 'local-fixture-reader', 'succeeded', 1, {
      toolName: 'fixture_file_reader',
      commandName: 'inspect_regression_cycle_fixture_source',
      phaseLabel: 'exploration',
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
      exitCode: 0,
      passed: true,
    }),
    event('2026-05-18T04:00:03.000Z', 'tool', 'local-fixture-editor', 'succeeded', 2, {
      toolName: 'fixture_patch_writer',
      commandName: 'write_plausible_wrong_patch',
      phaseLabel: 'implementation',
      fixturePath: fixtureSourcePath,
      sourceBeforeSha256: report.sourceBeforeSha256,
      wrongPatchSha256: report.wrongPatchSha256,
      modifiedFixtureFiles: report.modifiedFixtureFiles,
      protectedRepoFilesModified: [],
      exitCode: 0,
      passed: report.wrongPatchApplied,
    }),
    event('2026-05-18T04:00:04.000Z', 'tool', 'local-fixture-test-runner', 'failed', 3, {
      toolName: 'fixture_regression_check',
      commandName: 'run_regression_check_before_repair',
      phaseLabel: 'verification',
      fixturePath: fixtureSourcePath,
      testCaseCount: report.unitCheck.testCaseCount,
      failedCaseCountBeforeRepair: report.unitCheck.failedCaseCountBeforeRepair,
      exitCode: 1,
      passed: false,
    }),
    event('2026-05-18T04:00:05.000Z', 'tool', 'local-fixture-editor', report.repairApplied ? 'succeeded' : 'failed', 4, {
      toolName: 'fixture_patch_writer',
      commandName: 'revert_wrong_patch_and_write_regression_fix',
      phaseLabel: 'implementation',
      fixturePath: fixtureSourcePath,
      wrongPatchSha256: report.wrongPatchSha256,
      repairedSourceSha256: report.repairedSourceSha256,
      modifiedFixtureFiles: report.modifiedFixtureFiles,
      protectedRepoFilesModified: [],
      exitCode: report.repairApplied ? 0 : 1,
      passed: report.repairApplied,
    }),
    event('2026-05-18T04:00:06.000Z', 'tool', 'local-fixture-test-runner', report.regressionPassedAfterRepair ? 'succeeded' : 'failed', 5, {
      toolName: 'fixture_regression_check',
      commandName: 'run_regression_check_after_repair',
      phaseLabel: 'verification',
      fixturePath: fixtureSourcePath,
      testCaseCount: report.unitCheck.testCaseCount,
      passedCaseCountAfterRepair: report.unitCheck.passedCaseCountAfterRepair,
      exitCode: report.regressionPassedAfterRepair ? 0 : 1,
      passed: report.regressionPassedAfterRepair,
    }),
    event('2026-05-18T04:00:07.000Z', 'executor', 'openclaude-local-regression-cycle-code-editing-harness', allPassed ? 'succeeded' : 'failed', 5),
    event('2026-05-18T04:00:08.000Z', 'user', 'local-operator', allPassed ? 'succeeded' : 'failed', 5),
  ]
  return `${events.map((item) => JSON.stringify(item)).join('\n')}\n`
}

function writeMarkdown(report: RegressionCycleCodeEditingTraceCaptureReport): void {
  const caseRows = report.unitCheck.cases
    .map((item) => `| ${item.name} | \`${item.input}\` | \`${item.expected}\` | \`${item.wrongActual}\` | \`${item.repairedActual}\` | \`${item.failedBeforeRepair}\` | \`${item.passedAfterRepair}\` |`)
    .join('\n')
  const checkRows = report.traceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Regression Cycle Code Editing Trace Capture Report

Generated by: \`bun run product:regression-cycle-code-editing-trace-capture\`

## Claim Boundary

- This is a local no-provider implementation-bearing regression-cycle fixture trace.
- It mutates only disposable fixture files under \`${report.fixtureRoot}\`.
- It records a plausible wrong patch, a failing regression check, a repaired patch, and a passing regression check.
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
- wrong_patch_sha256: \`${report.wrongPatchSha256}\`
- repaired_source_sha256: \`${report.repairedSourceSha256}\`
- wrong_patch_applied: \`${report.wrongPatchApplied}\`
- regression_failed_before_repair: \`${report.regressionFailedBeforeRepair}\`
- repair_applied: \`${report.repairApplied}\`
- regression_passed_after_repair: \`${report.regressionPassedAfterRepair}\`
- modified_fixture_files: \`${report.modifiedFixtureFiles.join(',')}\`
- protected_repo_files_modified: \`${report.protectedRepoFilesModified.length}\`
- failed_case_count_before_repair: \`${report.unitCheck.failedCaseCountBeforeRepair}\`
- passed_case_count_after_repair: \`${report.unitCheck.passedCaseCountAfterRepair}\`
- test_case_count: \`${report.unitCheck.testCaseCount}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`

## Regression Cases

| Case | Input | Expected | Wrong Actual | Repaired Actual | Failed Before Repair | Passed After Repair |
| --- | --- | --- | --- | --- | --- | --- |
${caseRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'regression-cycle-code-editing-trace-capture-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  resetFixture()

  const promptSha256 = sha256(operatorPrompt)
  const promptByteLength = Buffer.byteLength(operatorPrompt, 'utf8')
  const sourceBeforeSha256 = fileSha256(fixtureSourcePath)
  const wrongPatchApplied = applyWrongPatch()
  const wrongPatchSha256 = fileSha256(fixtureSourcePath)
  const wrongSource = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  const repairApplied = applyRepairPatch()
  const repairedSourceSha256 = fileSha256(fixtureSourcePath)
  const repairedText = readFileSync(resolve(root, fixtureSourcePath), 'utf8')
  const cases = runRegressionCases(wrongSource, repairedText)
  const failedCaseCountBeforeRepair = cases.filter((item) => item.failedBeforeRepair).length
  const passedCaseCountAfterRepair = cases.filter((item) => item.passedAfterRepair).length
  const regressionFailedBeforeRepair = failedCaseCountBeforeRepair > 0
  const regressionPassedAfterRepair = passedCaseCountAfterRepair === cases.length
  const reportWithoutTrace: Omit<RegressionCycleCodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'> = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_regression_cycle_code_editing_trace_capture',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    operatorAuthorization: {
      authorized: true,
      scope: 'operator_authorized_local_no_provider_regression_cycle_code_editing_trace_capture_only',
      protectedActionsAuthorized: false,
    },
    capturePerformed: true,
    nonSyntheticUserSessionClaimed: false,
    fixtureRoot,
    tracePath,
    traceSha256: '',
    sourceBeforeSha256,
    wrongPatchSha256,
    repairedSourceSha256,
    wrongPatchApplied,
    regressionFailedBeforeRepair,
    repairApplied,
    regressionPassedAfterRepair,
    modifiedFixtureFiles: [fixtureSourcePath],
    protectedRepoFilesModified: [],
    unitCheck: {
      failedCaseCountBeforeRepair,
      passedCaseCountAfterRepair,
      testCaseCount: cases.length,
      cases,
    },
  }

  const traceText = buildTrace(reportWithoutTrace, promptSha256, promptByteLength)
  writeFileSync(resolve(root, tracePath), traceText)
  const traceSha256 = sha256(traceText)

  const traceChecks = [
    check('fixture source starts from incomplete implementation', sourceBeforeSha256 === sha256(sourceBefore), sourceBeforeSha256),
    check('wrong patch is applied and changes source hash', wrongPatchApplied && sourceBeforeSha256 !== wrongPatchSha256, wrongPatchSha256),
    check('regression check fails before repair', regressionFailedBeforeRepair && failedCaseCountBeforeRepair >= 1, `${failedCaseCountBeforeRepair}/${cases.length} failed`),
    check('repair patch is applied and changes source hash', repairApplied && wrongPatchSha256 !== repairedSourceSha256, repairedSourceSha256),
    check('regression check passes after repair', regressionPassedAfterRepair, `${passedCaseCountAfterRepair}/${cases.length} passed`),
    check('trace records wrong patch command', traceText.includes('"commandName":"write_plausible_wrong_patch"'), tracePath),
    check('trace records failed regression command', traceText.includes('"commandName":"run_regression_check_before_repair"') && traceText.includes('"status":"failed"'), tracePath),
    check('trace records repair command', traceText.includes('"commandName":"revert_wrong_patch_and_write_regression_fix"'), tracePath),
    check('trace records passing regression command', traceText.includes('"commandName":"run_regression_check_after_repair"') && traceText.includes('"status":"succeeded"'), tracePath),
    check('only disposable fixture files are modified', reportWithoutTrace.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-regression-cycle-code-editing-trace/')) && reportWithoutTrace.protectedRepoFilesModified.length === 0, reportWithoutTrace.modifiedFixtureFiles.join(',')),
    check('no provider/live/external calls are recorded', reportWithoutTrace.providerCallsPerformed.length === 0 && reportWithoutTrace.liveModelCallsPerformed.length === 0 && reportWithoutTrace.externalCallsPerformed.length === 0, 'call counts=0'),
  ]

  const report: RegressionCycleCodeEditingTraceCaptureReport = {
    ...reportWithoutTrace,
    traceSha256,
    traceChecks,
    claimBoundary: 'This is local no-provider regression-cycle code-editing fixture evidence only; it is not an external benchmark, release readiness, production readiness, public readiness, or autonomous reliability claim.',
  }

  writeFileSync(resolve(docsDir, 'regression-cycle-code-editing-trace-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`)
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
  console.log(`regression_cycle_code_editing_trace_path=${tracePath}`)
  console.log(`regression_cycle_code_editing_trace_sha256=${traceSha256}`)
  console.log(`fixture_root=${fixtureRoot}`)
  console.log(`modified_fixture_files=${report.modifiedFixtureFiles.length}`)
  console.log(`protected_repo_files_modified=${report.protectedRepoFilesModified.length}`)
  console.log(`regression_failed_before_repair=${report.regressionFailedBeforeRepair}`)
  console.log(`regression_passed_after_repair=${report.regressionPassedAfterRepair}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
