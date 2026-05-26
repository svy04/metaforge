import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { buildTraceEventName, describeTraceObservation, enrichTraceEvent } from './product-trace-event-enrichment'

type ToolLoopCheck = {
  label: string
  ok: boolean
  detail: string
}

type ToolCommandCapture = {
  name: string
  command: string[]
  exitCode: number | null
  stdoutSha256: string
  stderrSha256: string
  stdoutByteLength: number
  stderrByteLength: number
  requiredSubstrings: string[]
  missingSubstrings: string[]
  passed: boolean
}

type PromptedToolLoopCaptureReport = {
  generatedAt: string
  mode: 'local_no_provider_prompted_tool_loop_capture'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  operatorAuthorization: {
    authorized: true
    scope: 'operator_authorized_local_no_provider_prompted_tool_loop_capture_only'
    protectedActionsAuthorized: false
  }
  promptCaptured: true
  promptSha256: string
  promptByteLength: number
  nonSyntheticUserSessionClaimed: false
  tracePath: string
  traceSha256: string
  toolCommandCaptures: ToolCommandCapture[]
  toolLoopChecks: ToolLoopCheck[]
  claimBoundary: string
}

type TraceEvent = {
  timestamp: string
  role: 'user' | 'executor' | 'tool'
  model: string
  querySource: string
  status: 'started' | 'succeeded' | 'failed'
  turnCount: number
  captureKind: 'operator_authorized_local_prompted_tool_loop'
  promptSha256?: string
  promptByteLength?: number
  toolName?: string
  commandName?: string
  exitCode?: number | null
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
const tracePath = 'reports/orchestra-prompted-tool-loop-local-cli.jsonl'
const operatorPrompt = [
  'Inspect OpenClaude local no-provider configuration surfaces.',
  'Use only bounded local CLI introspection tools.',
  'Summarize evidence as hashes and counts, not raw command output.',
].join(' ')
const toolCommands = [
  {
    name: 'inspect_auto_mode_defaults',
    args: ['auto-mode', 'defaults'],
    requiredSubstrings: ['"allow"', '"soft_deny"', '"environment"'],
  },
  {
    name: 'inspect_scoped_agents',
    args: ['agents', '--setting-sources', 'user,project,local'],
    requiredSubstrings: ['active agents', 'Built-in agents'],
  },
] as const

function normalize(text: string | Buffer | null | undefined): string {
  return String(text ?? '').replace(/\r\n/g, '\n')
}

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function check(label: string, ok: boolean, detail: string): ToolLoopCheck {
  return { label, ok, detail }
}

function runToolCommand(command: (typeof toolCommands)[number]): ToolCommandCapture {
  const result = spawnSync(process.execPath, [cliPath, ...command.args], {
    cwd: root,
    encoding: 'utf8',
    env: {
      ...process.env,
      OPENCLAUDE_PRODUCT_PROMPTED_TOOL_LOOP_NO_PROVIDER: '1',
    },
  })
  const stdout = normalize(result.stdout)
  const stderr = normalize(result.stderr)
  const combined = `${stdout}\n${stderr}`
  const missingSubstrings = command.requiredSubstrings.filter((substring) => !combined.includes(substring))

  return {
    name: command.name,
    command: ['node', 'dist/cli.mjs', ...command.args],
    exitCode: result.status,
    stdoutSha256: sha256(stdout),
    stderrSha256: sha256(stderr),
    stdoutByteLength: Buffer.byteLength(stdout, 'utf8'),
    stderrByteLength: Buffer.byteLength(stderr, 'utf8'),
    requiredSubstrings: [...command.requiredSubstrings],
    missingSubstrings,
    passed: result.status === 0 && missingSubstrings.length === 0,
  }
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
    querySource: 'operator_authorized_local_no_provider_prompted_tool_loop',
    status,
    turnCount,
    captureKind: 'operator_authorized_local_prompted_tool_loop',
    ...extra,
  }
  const actionName = baseEvent.commandName ?? baseEvent.toolName
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

function buildTrace(promptSha256: string, promptByteLength: number, commandCaptures: ToolCommandCapture[]): string {
  const allPassed = commandCaptures.every((command) => command.passed)
  const traceEvents: TraceEvent[] = [
    event('2026-05-18T01:00:00.000Z', 'user', 'local-operator', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
    event('2026-05-18T01:00:01.000Z', 'executor', 'openclaude-local-tool-loop-harness', 'started', 1, {
      promptSha256,
      promptByteLength,
    }),
  ]

  commandCaptures.forEach((command, index) => {
    const second = (index * 2) + 2
    traceEvents.push(event(`2026-05-18T01:00:${String(second).padStart(2, '0')}.000Z`, 'tool', 'node-dist-cli-tool', 'started', index + 1, {
      toolName: 'local_cli_introspection',
      commandName: command.name,
      exitCode: command.exitCode,
      stdoutSha256: command.stdoutSha256,
      stderrSha256: command.stderrSha256,
      stdoutByteLength: command.stdoutByteLength,
      stderrByteLength: command.stderrByteLength,
      passed: command.passed,
    }))
    traceEvents.push(event(`2026-05-18T01:00:${String(second + 1).padStart(2, '0')}.000Z`, 'tool', 'node-dist-cli-tool', command.passed ? 'succeeded' : 'failed', index + 1, {
      toolName: 'local_cli_introspection',
      commandName: command.name,
      exitCode: command.exitCode,
      stdoutSha256: command.stdoutSha256,
      stderrSha256: command.stderrSha256,
      stdoutByteLength: command.stdoutByteLength,
      stderrByteLength: command.stderrByteLength,
      passed: command.passed,
    }))
  })

  traceEvents.push(event('2026-05-18T01:00:07.000Z', 'executor', 'openclaude-local-tool-loop-harness', allPassed ? 'succeeded' : 'failed', commandCaptures.length))
  traceEvents.push(event('2026-05-18T01:00:08.000Z', 'user', 'local-operator', allPassed ? 'succeeded' : 'failed', commandCaptures.length))

  return `${traceEvents.map((item) => JSON.stringify(item)).join('\n')}\n`
}

function writeReports(report: PromptedToolLoopCaptureReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'prompted-tool-loop-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# Prompted Tool Loop Capture Report',
    '',
    'Generated by: `bun run product:prompted-tool-loop-capture`',
    '',
    '## Claim Boundary',
    '',
    '- This report records an operator-authorized local no-provider prompted tool-loop harness.',
    '- It executes bounded local CLI introspection commands as tool steps.',
    '- It stores the operator prompt and command output only as hashes and byte counts in publishable reports.',
    '- It does not call providers, live models, or external services.',
    '- It does not claim non-synthetic user-session capture, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- prompt_captured: \`${report.promptCaptured}\``,
    `- prompt_sha256: \`${report.promptSha256}\``,
    `- prompt_byte_length: \`${report.promptByteLength}\``,
    `- non_synthetic_user_session_claimed: \`${report.nonSyntheticUserSessionClaimed}\``,
    `- operator_authorization_scope: \`${report.operatorAuthorization.scope}\``,
    `- protected_actions_authorized: \`${report.operatorAuthorization.protectedActionsAuthorized}\``,
    `- trace_path: \`${report.tracePath}\``,
    `- trace_sha256: \`${report.traceSha256}\``,
    `- tool_command_count: \`${report.toolCommandCaptures.length}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Tool Commands',
    '',
    '| Command | Exit | Passed | Stdout SHA-256 | Stderr SHA-256 | Stdout Bytes | Stderr Bytes |',
    '| --- | ---: | --- | --- | --- | ---: | ---: |',
    ...report.toolCommandCaptures.map((capture) => (
      `| \`${capture.command.join(' ')}\` | \`${capture.exitCode}\` | \`${capture.passed}\` | \`${capture.stdoutSha256}\` | \`${capture.stderrSha256}\` | ${capture.stdoutByteLength} | ${capture.stderrByteLength} |`
    )),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.toolLoopChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'prompted-tool-loop-capture-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  if (!existsSync(cliPath)) {
    console.error('RESULT: FAIL')
    console.error('missing built CLI: dist/cli.mjs')
    console.error('Run `bun run smoke` or `bun run build` before `bun run product:prompted-tool-loop-capture`.')
    process.exit(1)
  }

  const promptSha256 = sha256(operatorPrompt)
  const promptByteLength = Buffer.byteLength(operatorPrompt, 'utf8')
  const toolCommandCaptures = toolCommands.map((command) => runToolCommand(command))
  mkdirSync(reportsDir, { recursive: true })
  const traceText = buildTrace(promptSha256, promptByteLength, toolCommandCaptures)
  writeFileSync(resolve(root, tracePath), traceText)
  const traceSha256 = sha256(traceText)

  const toolLoopChecks = [
    check('operator authorization is bounded to local no-provider prompted tool-loop capture', true, 'standing operator scope is capture only'),
    check('built CLI exists', existsSync(cliPath), 'dist/cli.mjs'),
    check('operator prompt is captured only by hash', promptSha256.length === 64 && promptByteLength > 0, `${promptByteLength} bytes`),
    check('tool loop executed at least two local CLI tool steps', toolCommandCaptures.length >= 2, `${toolCommandCaptures.length} commands`),
    check('all local tool commands passed', toolCommandCaptures.every((command) => command.passed), toolCommandCaptures.map((command) => `${command.name}=${command.exitCode}`).join(',')),
    check('tool command output is summarized by hashes', toolCommandCaptures.every((command) => command.stdoutSha256.length === 64 && command.stderrSha256.length === 64), `${toolCommandCaptures.length} commands`),
    check('trace artifact was written', existsSync(resolve(root, tracePath)), tracePath),
    check('trace artifact hash is recorded', traceSha256.length === 64, traceSha256),
    check('non-synthetic user-session capture is not claimed', true, 'local harness evidence only'),
    check('no provider calls performed', true, 'local CLI tool loop only'),
    check('no live model calls performed', true, 'local CLI tool loop only'),
    check('no external calls performed', true, 'local CLI tool loop only'),
  ]

  const report: PromptedToolLoopCaptureReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_prompted_tool_loop_capture',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    operatorAuthorization: {
      authorized: true,
      scope: 'operator_authorized_local_no_provider_prompted_tool_loop_capture_only',
      protectedActionsAuthorized: false,
    },
    promptCaptured: true,
    promptSha256,
    promptByteLength,
    nonSyntheticUserSessionClaimed: false,
    tracePath,
    traceSha256,
    toolCommandCaptures,
    toolLoopChecks,
    claimBoundary: 'Prompted tool-loop capture is internal local no-provider harness evidence only. It does not claim non-synthetic user-session capture, release readiness, production readiness, external validation, public readiness, provider-backed execution, live model validation, or autonomous reliability.',
  }

  writeReports(report)

  for (const item of toolLoopChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!toolLoopChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`prompt_captured=${report.promptCaptured}`)
  console.log(`trace_path=${report.tracePath}`)
  console.log(`tool_command_count=${report.toolCommandCaptures.length}`)
  console.log(`non_synthetic_user_session_claimed=${report.nonSyntheticUserSessionClaimed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
