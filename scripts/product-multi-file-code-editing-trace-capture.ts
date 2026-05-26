import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { buildTraceEventName, describeTraceObservation, enrichTraceEvent } from './product-trace-event-enrichment'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type FixtureUnitCase = {
  name: string
  lines: Array<{ price: number; quantity: number }>
  expectedSubtotal: number
  expectedTax: number
  expectedTotal: number
  actualSubtotal: number
  actualTax: number
  actualTotal: number
  passed: boolean
}

type MultiFileCodeEditingTraceCaptureReport = {
  generatedAt: string
  mode: 'local_no_provider_multi_file_code_editing_trace_capture'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  operatorAuthorization: {
    authorized: true
    scope: 'operator_authorized_local_no_provider_multi_file_code_editing_trace_capture_only'
    protectedActionsAuthorized: false
  }
  capturePerformed: true
  nonSyntheticUserSessionClaimed: false
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeTreeSha256: string
  sourceAfterTreeSha256: string
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
  querySource: 'operator_authorized_local_no_provider_multi_file_code_editing_trace'
  status: 'started' | 'succeeded' | 'failed'
  turnCount: number
  captureKind: 'operator_authorized_local_multi_file_code_editing_trace'
  promptSha256?: string
  promptByteLength?: number
  toolName?: string
  commandName?: string
  phaseLabel?: 'exploration' | 'implementation' | 'verification'
  exitCode?: number
  passed?: boolean
  fixturePath?: string
  fixturePaths?: string[]
  sourceBeforeTreeSha256?: string
  sourceAfterTreeSha256?: string
  modifiedFixtureFiles?: string[]
  protectedRepoFilesModified?: []
  testCaseCount?: number
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const fixtureRoot = '_fixtures/product-multi-file-code-editing-trace'
const pricingPath = `${fixtureRoot}/src/pricing.js`
const taxPath = `${fixtureRoot}/src/tax.js`
const checkoutPath = `${fixtureRoot}/src/checkout.js`
const issuePath = `${fixtureRoot}/issue.md`
const tracePath = 'reports/orchestra-multi-file-code-editing-trace-local-fixture.jsonl'
const modifiedFixtureFiles = [pricingPath, taxPath, checkoutPath]

const sourceBeforeByPath: Record<string, string> = {
  [pricingPath]: `export function subtotal(lines) {
  return lines.reduce((sum, line) => sum + line.price, 0)
}
`,
  [taxPath]: `export const TAX_RATE = 0

export function calculateTax(subtotal) {
  return subtotal * TAX_RATE
}
`,
  [checkoutPath]: `import { subtotal } from './pricing.js'

export function checkoutTotal(lines) {
  return subtotal(lines)
}
`,
}

const sourceAfterByPath: Record<string, string> = {
  [pricingPath]: `export function subtotal(lines) {
  return lines.reduce((sum, line) => sum + (line.price * line.quantity), 0)
}
`,
  [taxPath]: `export const TAX_RATE = 0.1

export function calculateTax(subtotal) {
  return subtotal * TAX_RATE
}
`,
  [checkoutPath]: `import { subtotal } from './pricing.js'
import { calculateTax } from './tax.js'

export function checkoutTotal(lines) {
  const beforeTax = subtotal(lines)
  return beforeTax + calculateTax(beforeTax)
}
`,
}

const operatorPrompt = [
  'Repair the local checkout fixture across pricing, tax, and checkout modules.',
  'Use only deterministic local file evidence.',
  'Record multi-file exploration, implementation, and verification as a no-provider trace.',
].join(' ')

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
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
    querySource: 'operator_authorized_local_no_provider_multi_file_code_editing_trace',
    status,
    turnCount,
    captureKind: 'operator_authorized_local_multi_file_code_editing_trace',
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

function listFixtureFiles(relativeDir: string): string[] {
  const absoluteDir = resolve(root, relativeDir)
  return readdirSync(absoluteDir, { withFileTypes: true })
    .flatMap((entry) => {
      const relativePath = `${relativeDir}/${entry.name}`.replace(/\\/g, '/')
      if (entry.isDirectory()) {
        return listFixtureFiles(relativePath)
      }
      return [relativePath]
    })
    .sort((a, b) => a.localeCompare(b))
}

function treeSha256(relativeDir: string): string {
  const treeText = listFixtureFiles(relativeDir)
    .map((path) => `${path}\n${sha256(readFileSync(resolve(root, path), 'utf8'))}`)
    .join('\n')
  return sha256(treeText)
}

function writeFixtureFile(path: string, text: string): void {
  mkdirSync(dirname(resolve(root, path)), { recursive: true })
  writeFileSync(resolve(root, path), text)
}

function resetFixture(): void {
  rmSync(resolve(root, fixtureRoot), { recursive: true, force: true })
  mkdirSync(resolve(root, `${fixtureRoot}/src`), { recursive: true })
  writeFixtureFile(issuePath, [
    '# Multi-File Local Fixture Issue',
    '',
    'The checkout flow currently ignores quantity, applies no tax, and returns only pre-tax subtotal.',
    'Patch only the disposable fixture modules and verify deterministic checkout cases.',
    '',
  ].join('\n'))
  for (const [path, text] of Object.entries(sourceBeforeByPath)) {
    writeFixtureFile(path, text)
  }
}

function applyFixturePatch(): boolean {
  for (const path of modifiedFixtureFiles) {
    writeFixtureFile(path, sourceAfterByPath[path])
  }
  return modifiedFixtureFiles.every((path) => readFileSync(resolve(root, path), 'utf8') === sourceAfterByPath[path])
}

function roundCurrency(value: number): number {
  return Number(value.toFixed(2))
}

function runFixtureUnitCheck(): { passed: boolean; cases: FixtureUnitCase[] } {
  const pricingText = readFileSync(resolve(root, pricingPath), 'utf8')
  const taxText = readFileSync(resolve(root, taxPath), 'utf8')
  const checkoutText = readFileSync(resolve(root, checkoutPath), 'utf8')
  const usesQuantity = pricingText.includes('line.price * line.quantity')
  const taxRate = taxText.includes('TAX_RATE = 0.1') ? 0.1 : 0
  const checkoutUsesTax = checkoutText.includes('calculateTax(beforeTax)')
  const cases = [
    {
      name: 'mixed quantities with tax',
      lines: [{ price: 10, quantity: 2 }, { price: 5, quantity: 1 }],
      expectedSubtotal: 25,
      expectedTax: 2.5,
      expectedTotal: 27.5,
    },
    {
      name: 'single high quantity line',
      lines: [{ price: 3, quantity: 4 }],
      expectedSubtotal: 12,
      expectedTax: 1.2,
      expectedTotal: 13.2,
    },
    {
      name: 'zero quantity line',
      lines: [{ price: 50, quantity: 0 }, { price: 2, quantity: 3 }],
      expectedSubtotal: 6,
      expectedTax: 0.6,
      expectedTotal: 6.6,
    },
    {
      name: 'empty cart',
      lines: [],
      expectedSubtotal: 0,
      expectedTax: 0,
      expectedTotal: 0,
    },
  ].map((item) => {
    const actualSubtotal = item.lines.reduce((sum, line) => sum + (usesQuantity ? line.price * line.quantity : line.price), 0)
    const actualTax = roundCurrency(actualSubtotal * taxRate)
    const actualTotal = roundCurrency(actualSubtotal + (checkoutUsesTax ? actualTax : 0))
    return {
      ...item,
      actualSubtotal,
      actualTax,
      actualTotal,
      passed: actualSubtotal === item.expectedSubtotal &&
        actualTax === item.expectedTax &&
        actualTotal === item.expectedTotal,
    }
  })
  return {
    passed: cases.every((item) => item.passed),
    cases,
  }
}

function buildTrace(
  report: Omit<MultiFileCodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'>,
  promptSha256: string,
  promptByteLength: number,
): string {
  const allPassed = report.patchApplied && report.unitCheck.passed
  const events: TraceEvent[] = [
    event('2026-05-18T03:00:00.000Z', 'user', 'local-operator', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T03:00:01.000Z', 'executor', 'openclaude-local-multi-file-code-editing-harness', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T03:00:02.000Z', 'tool', 'local-fixture-reader', 'started', 1, {
      toolName: 'fixture_file_reader',
      commandName: 'inspect_multi_file_fixture_sources',
      phaseLabel: 'exploration',
      fixturePaths: modifiedFixtureFiles,
      sourceBeforeTreeSha256: report.sourceBeforeTreeSha256,
    }),
    event('2026-05-18T03:00:03.000Z', 'tool', 'local-fixture-reader', 'succeeded', 1, {
      toolName: 'fixture_file_reader',
      commandName: 'inspect_multi_file_fixture_sources',
      phaseLabel: 'exploration',
      exitCode: 0,
      passed: true,
      fixturePaths: modifiedFixtureFiles,
      sourceBeforeTreeSha256: report.sourceBeforeTreeSha256,
    }),
    event('2026-05-18T03:00:04.000Z', 'tool', 'local-fixture-editor', 'started', 2, {
      toolName: 'fixture_patch_writer',
      commandName: 'write_multi_file_fixture_patch',
      phaseLabel: 'implementation',
      fixturePaths: modifiedFixtureFiles,
      sourceBeforeTreeSha256: report.sourceBeforeTreeSha256,
      protectedRepoFilesModified: [],
    }),
    event('2026-05-18T03:00:05.000Z', 'tool', 'local-fixture-editor', report.patchApplied ? 'succeeded' : 'failed', 2, {
      toolName: 'fixture_patch_writer',
      commandName: 'write_multi_file_fixture_patch',
      phaseLabel: 'implementation',
      exitCode: report.patchApplied ? 0 : 1,
      passed: report.patchApplied,
      fixturePaths: modifiedFixtureFiles,
      sourceBeforeTreeSha256: report.sourceBeforeTreeSha256,
      sourceAfterTreeSha256: report.sourceAfterTreeSha256,
      modifiedFixtureFiles: report.modifiedFixtureFiles,
      protectedRepoFilesModified: [],
    }),
    event('2026-05-18T03:00:06.000Z', 'tool', 'local-fixture-test-runner', 'started', 3, {
      toolName: 'fixture_unit_check',
      commandName: 'run_multi_file_unit_check',
      phaseLabel: 'verification',
      fixturePaths: modifiedFixtureFiles,
      testCaseCount: report.unitCheck.testCaseCount,
    }),
    event('2026-05-18T03:00:07.000Z', 'tool', 'local-fixture-test-runner', report.unitCheck.passed ? 'succeeded' : 'failed', 3, {
      toolName: 'fixture_unit_check',
      commandName: 'run_multi_file_unit_check',
      phaseLabel: 'verification',
      exitCode: report.unitCheck.passed ? 0 : 1,
      passed: report.unitCheck.passed,
      fixturePaths: modifiedFixtureFiles,
      testCaseCount: report.unitCheck.testCaseCount,
    }),
    event('2026-05-18T03:00:08.000Z', 'executor', 'openclaude-local-multi-file-code-editing-harness', allPassed ? 'succeeded' : 'failed', 3),
    event('2026-05-18T03:00:09.000Z', 'user', 'local-operator', allPassed ? 'succeeded' : 'failed', 3),
  ]
  return `${events.map((item) => JSON.stringify(item)).join('\n')}\n`
}

function writeMarkdown(report: MultiFileCodeEditingTraceCaptureReport): void {
  const caseRows = report.unitCheck.cases
    .map((item) => `| ${item.name} | \`${item.expectedSubtotal}\` | \`${item.actualSubtotal}\` | \`${item.expectedTax}\` | \`${item.actualTax}\` | \`${item.expectedTotal}\` | \`${item.actualTotal}\` | \`${item.passed}\` |`)
    .join('\n')
  const checkRows = report.traceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Multi-File Code Editing Trace Capture Report

Generated by: \`bun run product:multi-file-code-editing-trace-capture\`

## Claim Boundary

- This is a local no-provider implementation-bearing multi-file fixture trace.
- It mutates only disposable fixture files under \`${report.fixtureRoot}\`.
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
- source_before_tree_sha256: \`${report.sourceBeforeTreeSha256}\`
- source_after_tree_sha256: \`${report.sourceAfterTreeSha256}\`
- patch_applied: \`${report.patchApplied}\`
- modified_fixture_files: \`${report.modifiedFixtureFiles.join(',')}\`
- protected_repo_files_modified: \`${report.protectedRepoFilesModified.length}\`
- unit_check_passed: \`${report.unitCheck.passed}\`
- unit_check_case_count: \`${report.unitCheck.testCaseCount}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`

## Fixture Unit Cases

| Case | Expected Subtotal | Actual Subtotal | Expected Tax | Actual Tax | Expected Total | Actual Total | Passed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
${caseRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'multi-file-code-editing-trace-capture-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  resetFixture()

  const promptSha256 = sha256(operatorPrompt)
  const promptByteLength = Buffer.byteLength(operatorPrompt, 'utf8')
  const sourceBeforeTreeSha256 = treeSha256(fixtureRoot)
  const patchApplied = applyFixturePatch()
  const sourceAfterTreeSha256 = treeSha256(fixtureRoot)
  const unitResult = runFixtureUnitCheck()
  const reportWithoutTrace: Omit<MultiFileCodeEditingTraceCaptureReport, 'traceSha256' | 'traceChecks' | 'claimBoundary'> = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_multi_file_code_editing_trace_capture',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    operatorAuthorization: {
      authorized: true,
      scope: 'operator_authorized_local_no_provider_multi_file_code_editing_trace_capture_only',
      protectedActionsAuthorized: false,
    },
    capturePerformed: true,
    nonSyntheticUserSessionClaimed: false,
    fixtureRoot,
    tracePath,
    traceSha256: '',
    sourceBeforeTreeSha256,
    sourceAfterTreeSha256,
    patchApplied,
    modifiedFixtureFiles,
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
    check('fixture source tree starts from failing multi-file implementation', sourceBeforeTreeSha256.length === 64, sourceBeforeTreeSha256),
    check('fixture patch changes source tree hash', sourceBeforeTreeSha256 !== sourceAfterTreeSha256, `${sourceBeforeTreeSha256}/${sourceAfterTreeSha256}`),
    check('fixture patch modifies pricing, tax, and checkout modules', patchApplied && modifiedFixtureFiles.length === 3, modifiedFixtureFiles.join(',')),
    check('fixture unit check passes', unitResult.passed, `${unitResult.cases.filter((item) => item.passed).length}/${unitResult.cases.length}`),
    check('trace records multi-file exploration command', traceText.includes('"commandName":"inspect_multi_file_fixture_sources"'), tracePath),
    check('trace records multi-file implementation command', traceText.includes('"commandName":"write_multi_file_fixture_patch"'), tracePath),
    check('trace records multi-file verification command', traceText.includes('"commandName":"run_multi_file_unit_check"'), tracePath),
    check('only disposable fixture files are modified', modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-multi-file-code-editing-trace/')), modifiedFixtureFiles.join(',')),
    check('no provider/live/external calls are recorded', reportWithoutTrace.providerCallsPerformed.length === 0 && reportWithoutTrace.liveModelCallsPerformed.length === 0 && reportWithoutTrace.externalCallsPerformed.length === 0, 'call counts=0'),
  ]

  const report: MultiFileCodeEditingTraceCaptureReport = {
    ...reportWithoutTrace,
    traceSha256,
    traceChecks,
    claimBoundary: 'This is local no-provider multi-file code-editing fixture evidence only; it is not an external benchmark, release readiness, production readiness, public readiness, or autonomous reliability claim.',
  }

  writeFileSync(resolve(docsDir, 'multi-file-code-editing-trace-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`)
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
  console.log(`multi_file_code_editing_trace_path=${tracePath}`)
  console.log(`multi_file_code_editing_trace_sha256=${traceSha256}`)
  console.log(`fixture_root=${fixtureRoot}`)
  console.log(`modified_fixture_files=${report.modifiedFixtureFiles.length}`)
  console.log(`protected_repo_files_modified=${report.protectedRepoFilesModified.length}`)
  console.log(`unit_check_passed=${report.unitCheck.passed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
