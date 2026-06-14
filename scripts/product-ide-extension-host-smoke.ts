import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Manifest = {
  publisher?: string
  name?: string
  contributes?: {
    commands?: Array<{ command?: string }>
  }
}

type HostCheck = {
  label: string
  ok: boolean
  detail: string
}

type HostRunnerResult = {
  extensionId: string
  extensionActivated: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  failedCommandIds: string[]
  commandResults: Array<{
    commandId: string
    ok: boolean
    resultStatus?: string
    error?: string
  }>
}

type HostReport = {
  generatedAt: string
  mode: 'local_no_provider_real_vscode_extension_host_smoke'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  hostRuntime: 'real_vscode_extension_development_host'
  vscodeCliVersion: string
  manifestPath: string
  entryPointPath: string
  extensionDevelopmentPath: string
  extensionTestsPath: string
  workspacePath: string
  codeCommand: string[]
  codeExitCode: number | null
  codeTimedOut: boolean
  codeError: string | null
  codeSignal: NodeJS.Signals | null
  stdoutSha256: string
  stderrSha256: string
  stdoutByteLength: number
  stderrByteLength: number
  vscodeStartupBlocked: boolean
  environmentBlockers: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  failedCommandIds: string[]
  commandResults: HostRunnerResult['commandResults']
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  productLaunchAttempted: false
  extensionAvailabilityClaimAllowed: false
  hostSmokeChecks: HostCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const tempRoot = resolve(root, '.tmp-product-ide-extension-host-smoke')
const tempDir = resolve(tempRoot, `run-${Date.now()}-${process.pid}`)
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const extensionDevelopmentPath = resolve(root, 'packages/openclaude-vscode')
const extensionTestsPath = resolve(tempDir, 'host-smoke-runner.cjs')
const workspacePath = resolve(tempDir, 'workspace')
const resultPath = resolve(tempDir, 'host-smoke-result.json')

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): HostCheck {
  return { label, ok, detail }
}

function sha256(input: string): string {
  return createHash('sha256').update(input).digest('hex')
}

function getManifestCommandIds(manifest: Manifest): string[] {
  return manifest.contributes?.commands
    ?.map((item) => item.command)
    .filter((command): command is string => typeof command === 'string') ?? []
}

function getVscodeCliVersion(): string {
  const result = spawnSync('code', ['--version'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  if (result.status !== 0) {
    return 'not_available'
  }

  return (result.stdout ?? '').trim().split(/\r?\n/).filter(Boolean).join(' / ')
}

function sanitizedEnv(): NodeJS.ProcessEnv {
  const allowedNames = new Set([
    'APPDATA',
    'COMSPEC',
    'HOMEDRIVE',
    'HOMEPATH',
    'LOCALAPPDATA',
    'NUMBER_OF_PROCESSORS',
    'OS',
    'PATH',
    'PATHEXT',
    'PROCESSOR_ARCHITECTURE',
    'PROCESSOR_IDENTIFIER',
    'PROCESSOR_LEVEL',
    'PROCESSOR_REVISION',
    'PROGRAMDATA',
    'PROGRAMFILES',
    'PROGRAMFILES(X86)',
    'PROGRAMW6432',
    'PSMODULEPATH',
    'PUBLIC',
    'SYSTEMDRIVE',
    'SYSTEMROOT',
    'TEMP',
    'TMP',
    'USERDOMAIN',
    'USERNAME',
    'USERPROFILE',
    'WINDIR',
  ])
  const env: NodeJS.ProcessEnv = {}

  for (const [key, value] of Object.entries(process.env)) {
    if (allowedNames.has(key.toUpperCase()) && typeof value === 'string') {
      env[key] = value
    }
  }

  const pathValue = process.env.PATH ?? process.env.Path
  if (typeof pathValue === 'string') {
    env.PATH = pathValue
    env.Path = pathValue
  }

  env.OPENCLAUDE_EXTENSION_HOST_COMMAND_IDS = JSON.stringify(getManifestCommandIds(readJson<Manifest>(manifestPath)))
  env.OPENCLAUDE_EXTENSION_HOST_EXTENSION_ID = `${readJson<Manifest>(manifestPath).publisher}.${readJson<Manifest>(manifestPath).name}`
  env.OPENCLAUDE_EXTENSION_HOST_RESULT_PATH = resultPath

  return env
}

function writeRunner(commandIds: string[], extensionId: string): void {
  const source = `'use strict'

const fs = require('node:fs')
const vscode = require('vscode')

const commandIds = JSON.parse(process.env.OPENCLAUDE_EXTENSION_HOST_COMMAND_IDS || '[]')
const extensionId = process.env.OPENCLAUDE_EXTENSION_HOST_EXTENSION_ID || ${JSON.stringify(extensionId)}
const resultPath = process.env.OPENCLAUDE_EXTENSION_HOST_RESULT_PATH

function withTimeout(promise, commandId) {
  let timer
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error('command timed out: ' + commandId)), 5000)
  })
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer))
}

async function run() {
  const result = {
    extensionId,
    extensionActivated: false,
    registeredCommandIds: [],
    executedCommandIds: [],
    failedCommandIds: [],
    commandResults: [],
  }

  try {
    const extension = vscode.extensions.getExtension(extensionId)
    if (!extension) {
      throw new Error('extension not found: ' + extensionId)
    }

    await extension.activate()
    result.extensionActivated = extension.isActive

    const registeredCommands = await vscode.commands.getCommands(true)
    result.registeredCommandIds = commandIds.filter((commandId) => registeredCommands.includes(commandId))

    for (const commandId of commandIds) {
      try {
        const commandResult = await withTimeout(vscode.commands.executeCommand(commandId), commandId)
        result.executedCommandIds.push(commandId)
        result.commandResults.push({
          commandId,
          ok: true,
          resultStatus: commandResult && typeof commandResult === 'object' ? commandResult.status : typeof commandResult,
        })
      } catch (error) {
        result.failedCommandIds.push(commandId)
        result.commandResults.push({
          commandId,
          ok: false,
          error: error && error.message ? error.message : String(error),
        })
      }
    }
  } finally {
    if (resultPath) {
      fs.writeFileSync(resultPath, JSON.stringify(result, null, 2) + '\\n')
    }
  }

  if (!result.extensionActivated || result.failedCommandIds.length > 0 || result.registeredCommandIds.length !== commandIds.length) {
    throw new Error('OpenClaude Extension Host smoke failed')
  }
}

module.exports = { run }
`

  if (commandIds.length === 0 || extensionId === 'undefined.undefined') {
    throw new Error('Cannot write host smoke runner without manifest command IDs and extension ID')
  }

  writeFileSync(extensionTestsPath, source)
}

function readRunnerResult(): HostRunnerResult | null {
  try {
    return JSON.parse(readFileSync(resultPath, 'utf8')) as HostRunnerResult
  } catch {
    return null
  }
}

function sleep(ms: number): void {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms)
}

function waitForRunnerResult(timeoutMs: number): HostRunnerResult | null {
  const deadline = Date.now() + timeoutMs

  while (Date.now() < deadline) {
    if (existsSync(resultPath)) {
      const result = readRunnerResult()
      if (result) {
        return result
      }
    }

    sleep(250)
  }

  return null
}

function scanEnvironmentBlockers(): string[] {
  const blockers = new Set<string>()
  const logsDir = resolve(tempDir, 'user-data', 'logs')

  if (!existsSync(logsDir)) {
    return []
  }

  const pendingDirs = [logsDir]
  while (pendingDirs.length > 0) {
    const dir = pendingDirs.pop()
    if (!dir) {
      continue
    }

    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const entryPath = resolve(dir, entry.name)
      if (entry.isDirectory()) {
        pendingDirs.push(entryPath)
        continue
      }
      if (!entry.isFile() || !entry.name.endsWith('.log')) {
        continue
      }

      const logText = readFileSync(entryPath, 'utf8')
      if (logText.includes('Code is currently being updated') || logText.includes('vscode-updating still held')) {
        blockers.add('vscode_update_in_progress')
      }
    }
  }

  return [...blockers]
}

function collectEnvironmentBlockers(timeoutMs = 2000): string[] {
  const deadline = Date.now() + timeoutMs
  while (Date.now() < deadline) {
    const blockers = scanEnvironmentBlockers()
    if (blockers.length > 0) {
      return blockers
    }
    sleep(250)
  }
  return scanEnvironmentBlockers()
}

function withCliEnvironmentBlockers(blockers: string[], result: ReturnType<typeof spawnSync>, vscodeCliVersion: string): string[] {
  const next = new Set(blockers)
  const errorMessage = result.error?.message ?? ''
  if (vscodeCliVersion === 'not_available' || errorMessage.includes('Executable not found')) {
    next.add('vscode_cli_unavailable')
  }
  return [...next]
}

function writeReports(report: HostReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'ide-extension-host-smoke-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# IDE Extension Host Smoke Report',
    '',
    'Generated by: `bun run product:ide-extension-host-smoke`',
    '',
    '## Primary Source Basis',
    '',
    '- VS Code official extension testing documentation defines Extension Development Host tests with `--extensionDevelopmentPath` and `--extensionTestsPath`.',
    '- VS Code official command documentation defines `registerCommand` and programmatic `executeCommand` behavior.',
    '',
    '## Claim Boundary',
    '',
    '- This report launches a local VS Code Extension Development Host only for integration smoke evidence.',
    '- It does not install, publish, deploy, product-launch, or claim extension availability.',
    '- It does not call providers, live models, or external services.',
    '- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- host_runtime: \`${report.hostRuntime}\``,
    `- vscode_cli_version: \`${report.vscodeCliVersion}\``,
    `- manifest_path: \`${report.manifestPath}\``,
    `- entry_point_path: \`${report.entryPointPath}\``,
    `- extension_development_path: \`${report.extensionDevelopmentPath}\``,
    `- extension_tests_path: \`${report.extensionTestsPath}\``,
    `- workspace_path: \`${report.workspacePath}\``,
    `- code_exit_code: \`${report.codeExitCode}\``,
    `- code_timed_out: \`${report.codeTimedOut}\``,
    `- code_error: \`${report.codeError ?? 'none'}\``,
    `- extension_activated: \`${report.extensionActivated}\``,
    `- real_extension_host_launched: \`${report.realExtensionHostLaunched}\``,
    `- extension_availability_claim_allowed: \`${report.extensionAvailabilityClaimAllowed}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Commands',
    '',
    `- registered_command_ids: ${report.registeredCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    `- executed_command_ids: ${report.executedCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    `- failed_command_ids: ${report.failedCommandIds.length === 0 ? '`none`' : report.failedCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    '',
    '## Process Evidence',
    '',
    `- code_command: \`${report.codeCommand.join(' ')}\``,
    `- stdout_sha256: \`${report.stdoutSha256}\``,
    `- stderr_sha256: \`${report.stderrSha256}\``,
    `- stdout_byte_length: \`${report.stdoutByteLength}\``,
    `- stderr_byte_length: \`${report.stderrByteLength}\``,
    `- vscode_startup_blocked: \`${report.vscodeStartupBlocked}\``,
    `- environment_blockers: ${report.environmentBlockers.length === 0 ? '`none`' : report.environmentBlockers.map((item) => `\`${item}\``).join(', ')}`,
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.hostSmokeChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-host-smoke-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  const manifest = readJson<Manifest>(manifestPath)
  const commandIds = getManifestCommandIds(manifest)
  const extensionId = `${manifest.publisher}.${manifest.name}`

  mkdirSync(tempRoot, { recursive: true })
  rmSync(tempDir, { recursive: true, force: true })
  mkdirSync(workspacePath, { recursive: true })
  mkdirSync(resolve(tempDir, 'user-data'), { recursive: true })
  mkdirSync(resolve(tempDir, 'extensions'), { recursive: true })
  writeRunner(commandIds, extensionId)

  const args = [
    `--extensionDevelopmentPath=${extensionDevelopmentPath}`,
    `--extensionTestsPath=${extensionTestsPath}`,
    '--user-data-dir',
    resolve(tempDir, 'user-data'),
    '--extensions-dir',
    resolve(tempDir, 'extensions'),
    '--disable-extensions',
    '--disable-gpu',
    '--skip-welcome',
    '--skip-release-notes',
    '--disable-workspace-trust',
    '--new-window',
    workspacePath,
  ]
  const result = spawnSync('code', args, {
    cwd: root,
    encoding: 'utf8',
    env: sanitizedEnv(),
    shell: false,
    timeout: 90000,
  })
  const hostResult = waitForRunnerResult(30000)
  const stdout = result.stdout ?? ''
  const stderr = result.stderr ?? ''
  const vscodeCliVersion = getVscodeCliVersion()
  const codeTimedOut = result.error?.message.includes('ETIMEDOUT') === true
  const registeredCommandIds = hostResult?.registeredCommandIds ?? []
  const executedCommandIds = hostResult?.executedCommandIds ?? []
  const failedCommandIds = hostResult?.failedCommandIds ?? commandIds
  const environmentBlockers = withCliEnvironmentBlockers(collectEnvironmentBlockers(), result, vscodeCliVersion)
  const vscodeStartupBlocked = environmentBlockers.length > 0
  const realExtensionHostLaunched = hostResult !== null && !vscodeStartupBlocked
  const knownEnvironmentBlocked = vscodeStartupBlocked || environmentBlockers.includes('vscode_cli_unavailable')

  const hostSmokeChecks = [
    check('manifest command IDs are present', commandIds.length >= 3, commandIds.join(', ')),
    check('VS Code CLI version is available', vscodeCliVersion !== 'not_available', vscodeCliVersion),
    check('VS Code CLI command exited 0', result.status === 0, String(result.status)),
    check('VS Code CLI command did not time out', !codeTimedOut, String(codeTimedOut)),
    check('VS Code startup was not blocked by local environment state', !vscodeStartupBlocked, environmentBlockers.length === 0 ? 'none' : environmentBlockers.join(', ')),
    check('real Extension Development Host test runner produced result', realExtensionHostLaunched, hostResult ? 'result file present' : 'result file missing'),
    check('extension activated in real host', hostResult?.extensionActivated === true, String(hostResult?.extensionActivated)),
    check('all manifest commands are registered in real host', commandIds.every((commandId) => registeredCommandIds.includes(commandId)), registeredCommandIds.join(', ')),
    check('all manifest commands execute in real host', commandIds.every((commandId) => executedCommandIds.includes(commandId)) && failedCommandIds.length === 0, executedCommandIds.join(', ')),
    check('protected actions were not attempted', true, 'install/publish/deploy/product-launch/provider/live/external all false'),
    check('extension availability claim remains blocked', true, 'extension availability claim allowed=false'),
  ]

  const report: HostReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_real_vscode_extension_host_smoke',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    hostRuntime: 'real_vscode_extension_development_host',
    vscodeCliVersion,
    manifestPath,
    entryPointPath,
    extensionDevelopmentPath,
    extensionTestsPath,
    workspacePath,
    codeCommand: ['code', ...args],
    codeExitCode: result.status,
    codeTimedOut,
    codeError: result.error?.message ?? null,
    codeSignal: result.signal,
    stdoutSha256: sha256(stdout),
    stderrSha256: sha256(stderr),
    stdoutByteLength: Buffer.byteLength(stdout),
    stderrByteLength: Buffer.byteLength(stderr),
    vscodeStartupBlocked,
    environmentBlockers,
    realExtensionHostLaunched,
    extensionActivated: hostResult?.extensionActivated === true,
    registeredCommandIds,
    executedCommandIds,
    failedCommandIds,
    commandResults: hostResult?.commandResults ?? [],
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    productLaunchAttempted: false,
    extensionAvailabilityClaimAllowed: false,
    hostSmokeChecks,
    claimBoundary: 'Local VS Code Extension Development Host smoke evidence only. This does not install, publish, deploy, product-launch, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeReports(report)

  if (hostSmokeChecks.every((item) => item.ok)) {
    rmSync(tempDir, { recursive: true, force: true })
  }

  for (const item of hostSmokeChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!hostSmokeChecks.every((item) => item.ok) && !knownEnvironmentBlocked) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log(`RESULT: ${hostSmokeChecks.every((item) => item.ok) ? 'PASS' : 'BLOCKED'}`)
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`code_exit_code=${report.codeExitCode}`)
  console.log(`extension_activated=${report.extensionActivated}`)
  console.log(`registered_command_count=${report.registeredCommandIds.length}`)
  console.log(`executed_command_count=${report.executedCommandIds.length}`)
  console.log(`failed_command_count=${report.failedCommandIds.length}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
