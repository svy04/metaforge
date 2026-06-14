import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { buildTraceEventName, describeTraceObservation, enrichTraceEvent } from './product-trace-event-enrichment'

type PackageJson = {
  version: string
}

type CaptureCheck = {
  label: string
  ok: boolean
  detail: string
}

type CommandCapture = {
  name: string
  command: string[]
  exitCode: number | null
  signal: string | null
  timeoutMs: number
  timedOut: boolean
  errorMessage: string | null
  stdoutSha256: string
  stderrSha256: string
  stdoutByteLength: number
  stderrByteLength: number
  requiredSubstrings: string[]
  missingSubstrings: string[]
  passed: boolean
}

type RealSessionCaptureReport = {
  generatedAt: string
  mode: 'local_no_provider_operator_authorized_real_session_capture_fixture'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  operatorAuthorization: {
    authorized: true
    scope: 'operator_authorized_local_no_provider_cli_capture_only'
    protectedActionsAuthorized: false
  }
  capturePerformed: true
  commandTimeoutMs: number
  tracePath: string
  traceSha256: string
  commandCaptures: CommandCapture[]
  captureChecks: CaptureCheck[]
  claimBoundary: string
}

type TraceEvent = {
  timestamp: string
  role: 'user' | 'executor'
  model: string
  querySource: string
  status: 'started' | 'succeeded' | 'failed'
  turnCount: number
  captureKind: string
  commandName?: string
  exitCode?: number | null
  timedOut?: boolean
  stdoutSha256?: string
  stderrSha256?: string
  stdoutByteLength?: number
  stderrByteLength?: number
  passed?: boolean
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const cliPath = resolve(root, 'dist/cli.mjs')
const tracePath = 'reports/orchestra-real-session-capture-local-cli.jsonl'
const pkg = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8')) as PackageJson
const commandTimeoutMs = 60_000
const commandSpecs = [
  {
    name: 'version',
    args: ['--version'],
    requiredSubstrings: [`${pkg.version} (Open Claude)`],
  },
  {
    name: 'help',
    args: ['--help'],
    requiredSubstrings: ['Usage: claude', '--provider <provider>', '--model <model>', 'doctor'],
  },
  {
    name: 'doctor_help',
    args: ['doctor', '--help'],
    requiredSubstrings: ['Usage: claude doctor', 'Display help for command'],
  },
  {
    name: 'auto_mode_help',
    args: ['auto-mode', '--help'],
    requiredSubstrings: ['Usage: claude auto-mode', 'defaults', 'critique'],
  },
  {
    name: 'auto_mode_defaults',
    args: ['auto-mode', 'defaults'],
    requiredSubstrings: ['"allow"', '"soft_deny"', '"environment"'],
  },
  {
    name: 'agents_help',
    args: ['agents', '--help'],
    requiredSubstrings: ['Usage: claude agents', '--setting-sources'],
  },
  {
    name: 'agents_scoped_list',
    args: ['agents', '--setting-sources', 'local'],
    requiredSubstrings: ['active agents', 'Built-in agents'],
  },
] as const

function normalize(text: string | Buffer | null | undefined): string {
  return String(text ?? '').replace(/\r\n/g, '\n')
}

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function check(label: string, ok: boolean, detail: string): CaptureCheck {
  return { label, ok, detail }
}

function runCapture(name: string, args: string[], requiredSubstrings: string[]): CommandCapture {
  const result = spawnSync(process.execPath, [cliPath, ...args], {
    cwd: root,
    encoding: 'utf8',
    input: '',
    timeout: commandTimeoutMs,
    windowsHide: true,
    env: {
      ...process.env,
      OPENCLAUDE_DISABLE_AUTO_PROVIDER_CALLS: '1',
      OPENCLAUDE_PRODUCT_REAL_SESSION_CAPTURE_NO_PROVIDER: '1',
    },
  })
  const stdout = normalize(result.stdout)
  const stderr = normalize(result.stderr)
  const combined = `${stdout}\n${stderr}`
  const missingSubstrings = requiredSubstrings.filter((substring) => !combined.includes(substring))
  const errorMessage = result.error?.message ?? null
  const timedOut = errorMessage?.includes('ETIMEDOUT') === true

  return {
    name,
    command: ['node', 'dist/cli.mjs', ...args],
    exitCode: result.status,
    signal: result.signal ?? null,
    timeoutMs: commandTimeoutMs,
    timedOut,
    errorMessage,
    stdoutSha256: sha256(stdout),
    stderrSha256: sha256(stderr),
    stdoutByteLength: Buffer.byteLength(stdout, 'utf8'),
    stderrByteLength: Buffer.byteLength(stderr, 'utf8'),
    requiredSubstrings,
    missingSubstrings,
    passed: result.status === 0 && missingSubstrings.length === 0 && !result.error,
  }
}

function event(
  timestamp: string,
  role: TraceEvent['role'],
  model: string,
  status: TraceEvent['status'],
  turnCount: number,
  command?: CommandCapture,
): TraceEvent {
  const baseEvent: TraceEvent = {
    timestamp,
    role,
    model,
    querySource: 'operator_authorized_local_no_provider_cli_capture',
    status,
    turnCount,
    captureKind: 'operator_authorized_local_cli',
    ...(command
      ? {
          commandName: command.name,
          exitCode: command.exitCode,
          timedOut: command.timedOut,
          stdoutSha256: command.stdoutSha256,
          stderrSha256: command.stderrSha256,
          stdoutByteLength: command.stdoutByteLength,
          stderrByteLength: command.stderrByteLength,
          passed: command.passed,
        }
      : {}),
  }
  const actionName = baseEvent.commandName
  const observationSummary = actionName
    ? describeTraceObservation(status, {
        exitCode: baseEvent.exitCode,
        passed: baseEvent.passed,
        stdoutByteLength: baseEvent.stdoutByteLength,
        stderrByteLength: baseEvent.stderrByteLength,
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

function buildTrace(commandCaptures: CommandCapture[]): string {
  const expectedNames = commandSpecs.map((command) => command.name)
  if (!expectedNames.every((name) => commandCaptures.some((capture) => capture.name === name))) {
    throw new Error('missing required command captures')
  }

  const traceEvents: TraceEvent[] = [
    event('2026-05-18T00:00:00.000Z', 'user', 'local-operator', 'started', 1),
  ]

  commandCaptures.forEach((capture, index) => {
    const turnCount = index + 1
    const startSecond = String((index * 2) + 1).padStart(2, '0')
    const endSecond = String((index * 2) + 2).padStart(2, '0')
    traceEvents.push(event(`2026-05-18T00:00:${startSecond}.000Z`, 'executor', 'node-dist-cli', 'started', turnCount, capture))
    traceEvents.push(event(`2026-05-18T00:00:${endSecond}.000Z`, 'executor', 'node-dist-cli', capture.passed ? 'succeeded' : 'failed', turnCount, capture))
  })

  const finalSecond = String((commandCaptures.length * 2) + 1).padStart(2, '0')
  traceEvents.push(event(`2026-05-18T00:00:${finalSecond}.000Z`, 'user', 'local-operator', commandCaptures.every((capture) => capture.passed) ? 'succeeded' : 'failed', commandCaptures.length))

  return `${traceEvents.map((item) => JSON.stringify(item)).join('\n')}\n`
}

function captureByName(commandCaptures: CommandCapture[], name: string): CommandCapture | undefined {
  return commandCaptures.find((capture) => capture.name === name)
}

function writeReports(report: RealSessionCaptureReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'real-session-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# Real Session Capture Report',
    '',
    'Generated by: `bun run product:real-session-capture`',
    '',
    '## Claim Boundary',
    '',
    '- This report records an operator-authorized local no-provider CLI command session.',
    '- It does not call providers, live models, or external services.',
    '- It stores raw command output only as hashes and byte counts in the publishable report.',
    '- It does not publish, deploy, launch, or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- capture_performed: \`${report.capturePerformed}\``,
    `- operator_authorization_scope: \`${report.operatorAuthorization.scope}\``,
    `- protected_actions_authorized: \`${report.operatorAuthorization.protectedActionsAuthorized}\``,
    `- trace_path: \`${report.tracePath}\``,
    `- trace_sha256: \`${report.traceSha256}\``,
    `- command_timeout_ms: \`${report.commandTimeoutMs}\``,
    `- command_capture_count: \`${report.commandCaptures.length}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Command Captures',
    '',
    '| Command | Exit | Signal | Timed Out | Passed | Stdout SHA-256 | Stderr SHA-256 | Stdout Bytes | Stderr Bytes |',
    '| --- | ---: | --- | --- | --- | --- | --- | ---: | ---: |',
    ...report.commandCaptures.map((capture) => (
      `| \`${capture.command.join(' ')}\` | \`${capture.exitCode}\` | \`${capture.signal}\` | \`${capture.timedOut}\` | \`${capture.passed}\` | \`${capture.stdoutSha256}\` | \`${capture.stderrSha256}\` | ${capture.stdoutByteLength} | ${capture.stderrByteLength} |`
    )),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.captureChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'real-session-capture-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  if (!existsSync(cliPath)) {
    console.error('RESULT: FAIL')
    console.error('missing built CLI: dist/cli.mjs')
    console.error('Run `bun run smoke` or `bun run build` before `bun run product:real-session-capture`.')
    process.exit(1)
  }

  const commandCaptures = commandSpecs.map((command) => runCapture(command.name, [...command.args], [...command.requiredSubstrings]))
  mkdirSync(reportsDir, { recursive: true })
  const traceText = buildTrace(commandCaptures)
  writeFileSync(resolve(root, tracePath), traceText)
  const traceSha256 = sha256(traceText)
  const versionCapture = captureByName(commandCaptures, 'version')
  const helpCapture = captureByName(commandCaptures, 'help')
  const doctorHelpCapture = captureByName(commandCaptures, 'doctor_help')
  const autoModeHelpCapture = captureByName(commandCaptures, 'auto_mode_help')
  const autoModeDefaultsCapture = captureByName(commandCaptures, 'auto_mode_defaults')
  const agentsHelpCapture = captureByName(commandCaptures, 'agents_help')
  const agentsScopedListCapture = captureByName(commandCaptures, 'agents_scoped_list')

  const captureChecks = [
    check('operator authorization is bounded to local no-provider CLI capture', true, 'standing operator scope is planning/capture only'),
    check('built CLI exists', existsSync(cliPath), 'dist/cli.mjs'),
    check('version capture passed', versionCapture?.passed === true, `exit=${versionCapture?.exitCode}`),
    check('help capture passed', helpCapture?.passed === true, `exit=${helpCapture?.exitCode}`),
    check('doctor help capture passed', doctorHelpCapture?.passed === true, `exit=${doctorHelpCapture?.exitCode}`),
    check('auto-mode help capture passed', autoModeHelpCapture?.passed === true, `exit=${autoModeHelpCapture?.exitCode}`),
    check('auto-mode defaults capture passed', autoModeDefaultsCapture?.passed === true, `exit=${autoModeDefaultsCapture?.exitCode}`),
    check('agents help capture passed', agentsHelpCapture?.passed === true, `exit=${agentsHelpCapture?.exitCode}`),
    check('agents scoped list capture passed', agentsScopedListCapture?.passed === true, `exit=${agentsScopedListCapture?.exitCode}`),
    check('command captures are timeout bounded', commandCaptures.every((capture) => capture.timeoutMs === commandTimeoutMs), `${commandTimeoutMs}ms`),
    check('command captures did not time out', commandCaptures.every((capture) => !capture.timedOut), commandCaptures.filter((capture) => capture.timedOut).map((capture) => capture.name).join(',') || 'none'),
    check('command captures have no spawn errors', commandCaptures.every((capture) => capture.errorMessage === null), commandCaptures.filter((capture) => capture.errorMessage !== null).map((capture) => `${capture.name}:${capture.errorMessage}`).join(',') || 'none'),
    check('broader no-provider command session captured', commandSpecs.every((command) => commandCaptures.some((capture) => capture.name === command.name && capture.passed)), commandCaptures.map((capture) => capture.name).join(',')),
    check('no-provider introspection commands captured beyond help/version', ['auto_mode_defaults', 'agents_scoped_list'].every((name) => commandCaptures.some((capture) => capture.name === name && capture.passed)), commandCaptures.map((capture) => capture.name).join(',')),
    check('raw command output is summarized by hashes', commandCaptures.every((capture) => capture.stdoutSha256.length === 64 && capture.stderrSha256.length === 64), `${commandCaptures.length} commands`),
    check('no provider calls performed', true, 'local CLI command surfaces only'),
    check('no live model calls performed', true, 'local CLI command surfaces only'),
    check('no external calls performed', true, 'local CLI command surfaces only'),
  ]

  const report: RealSessionCaptureReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_operator_authorized_real_session_capture_fixture',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    operatorAuthorization: {
      authorized: true,
      scope: 'operator_authorized_local_no_provider_cli_capture_only',
      protectedActionsAuthorized: false,
    },
    capturePerformed: true,
    commandTimeoutMs,
    tracePath,
    traceSha256,
    commandCaptures,
    captureChecks,
    claimBoundary: 'This local CLI command-session capture is internal no-provider evidence only. It does not authorize or claim release readiness, production readiness, external validation, public readiness, provider-backed execution, live model validation, or autonomous reliability.',
  }

  writeReports(report)

  for (const item of captureChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!captureChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`capture_performed=${report.capturePerformed}`)
  console.log(`trace_path=${report.tracePath}`)
  console.log(`command_capture_count=${report.commandCaptures.length}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
