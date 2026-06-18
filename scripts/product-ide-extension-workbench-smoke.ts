import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import {
  buildSanitizedIdeSmokeEnv,
  collectVscodeEnvironmentBlockers,
  getVscodeCliVersion,
  waitForJsonResult,
  withCliEnvironmentBlockers,
} from './product-ide-smoke-helpers'
import { scrubPublicArtifactText, scrubPublicArtifactValue } from './product-report-sanitizer'

type Manifest = {
  publisher?: string
  name?: string
  contributes?: {
    commands?: Array<{ command?: string }>
    views?: Record<string, Array<{ id?: string; type?: string }>>
  }
}

type WorkbenchCheck = {
  label: string
  ok: boolean
  detail: string
}

type WorkbenchRunnerResult = {
  extensionId: string
  extensionActivated: boolean
  contributedViewIds: string[]
  registeredTreeViewIds: string[]
  treeProviderViewIds: string[]
  focusedViewIds: string[]
  failedFocusViewIds: string[]
  viewItemCounts: Record<string, number>
  viewItemCommandIds: string[]
  executedViewCommandIds: string[]
  failedViewCommandIds: string[]
  viewItems: Record<string, Array<{
    label: unknown
    description: unknown
    command: unknown
  }>>
}

type WorkbenchReport = {
  generatedAt: string
  mode: 'local_no_provider_real_vscode_workbench_tree_view_smoke'
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
  contributedViewIds: string[]
  registeredTreeViewIds: string[]
  treeProviderViewIds: string[]
  focusedViewIds: string[]
  failedFocusViewIds: string[]
  viewItemCounts: Record<string, number>
  viewItemCommandIds: string[]
  executedViewCommandIds: string[]
  failedViewCommandIds: string[]
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  productLaunchAttempted: false
  extensionAvailabilityClaimAllowed: false
  workbenchSmokeChecks: WorkbenchCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const tempRoot = resolve(root, '.tmp-product-ide-extension-workbench-smoke')
const tempDir = resolve(tempRoot, `run-${Date.now()}-${process.pid}`)
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const extensionDevelopmentPath = resolve(root, 'packages/openclaude-vscode')
const extensionTestsPath = resolve(tempDir, 'workbench-smoke-runner.cjs')
const workspacePath = resolve(tempDir, 'workspace')
const resultPath = resolve(tempDir, 'workbench-smoke-result.json')

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): WorkbenchCheck {
  return { label, ok, detail }
}

function sha256(input: string): string {
  return createHash('sha256').update(input).digest('hex')
}

function getManifestViewIds(manifest: Manifest): string[] {
  return Object.values(manifest.contributes?.views ?? {})
    .flat()
    .filter((item) => item.type !== 'webview')
    .map((item) => item.id)
    .filter((id): id is string => typeof id === 'string')
}

function getManifestCommandIds(manifest: Manifest): string[] {
  return (manifest.contributes?.commands ?? [])
    .map((item) => item.command)
    .filter((id): id is string => typeof id === 'string')
}

function sanitizedEnv(viewIds: string[], extensionId: string): NodeJS.ProcessEnv {
  return buildSanitizedIdeSmokeEnv({
    OPENCLAUDE_WORKBENCH_SMOKE_VIEW_IDS: JSON.stringify(viewIds),
    OPENCLAUDE_WORKBENCH_SMOKE_EXTENSION_ID: extensionId,
    OPENCLAUDE_WORKBENCH_SMOKE_RESULT_PATH: resultPath,
  })
}

function writeRunner(viewIds: string[], extensionId: string): void {
  const source = `'use strict'

const fs = require('node:fs')
const vscode = require('vscode')

const viewIds = JSON.parse(process.env.OPENCLAUDE_WORKBENCH_SMOKE_VIEW_IDS || '[]')
const extensionId = process.env.OPENCLAUDE_WORKBENCH_SMOKE_EXTENSION_ID || ${JSON.stringify(extensionId)}
const resultPath = process.env.OPENCLAUDE_WORKBENCH_SMOKE_RESULT_PATH

function withTimeout(promise, label) {
  let timer
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => reject(new Error('operation timed out: ' + label)), 5000)
  })
  return Promise.race([promise, timeout]).finally(() => clearTimeout(timer))
}

async function run() {
  const result = {
    extensionId,
    extensionActivated: false,
    contributedViewIds: viewIds,
    registeredTreeViewIds: [],
    treeProviderViewIds: [],
    focusedViewIds: [],
    failedFocusViewIds: [],
    viewItemCounts: {},
    viewItemCommandIds: [],
    executedViewCommandIds: [],
    failedViewCommandIds: [],
    viewItems: {},
  }

  try {
    const extension = vscode.extensions.getExtension(extensionId)
    if (!extension) {
      throw new Error('extension not found: ' + extensionId)
    }

    const api = await extension.activate()
    const extensionApi = api || extension.exports
    result.extensionActivated = extension.isActive

    const state = extensionApi && typeof extensionApi.getWorkbenchSmokeState === 'function'
      ? extensionApi.getWorkbenchSmokeState()
      : {}
    result.registeredTreeViewIds = Array.isArray(state.registeredTreeViewIds) ? state.registeredTreeViewIds : []
    result.treeProviderViewIds = Array.isArray(state.treeProviderViewIds) ? state.treeProviderViewIds : []

    for (const viewId of viewIds) {
      try {
        if (!extensionApi || typeof extensionApi.revealWorkbenchSmokeItem !== 'function') {
          throw new Error('missing revealWorkbenchSmokeItem API')
        }

        const revealed = await withTimeout(Promise.resolve(extensionApi.revealWorkbenchSmokeItem(viewId)), viewId)
        if (revealed !== true) {
          throw new Error('tree view reveal returned false: ' + viewId)
        }

        result.focusedViewIds.push(viewId)
      } catch {
        result.failedFocusViewIds.push(viewId)
      }

      if (extensionApi && typeof extensionApi.getWorkbenchSmokeItems === 'function') {
        const items = await withTimeout(Promise.resolve(extensionApi.getWorkbenchSmokeItems(viewId)), 'items:' + viewId)
        result.viewItems[viewId] = Array.isArray(items) ? items : []
        result.viewItemCounts[viewId] = result.viewItems[viewId].length
        for (const item of result.viewItems[viewId]) {
          if (item && typeof item.command === 'string' && !result.viewItemCommandIds.includes(item.command)) {
            result.viewItemCommandIds.push(item.command)
          }
        }
      } else {
        result.viewItems[viewId] = []
        result.viewItemCounts[viewId] = 0
      }
    }

    for (const commandId of result.viewItemCommandIds) {
      try {
        await withTimeout(Promise.resolve(vscode.commands.executeCommand(commandId)), 'command:' + commandId)
        result.executedViewCommandIds.push(commandId)
      } catch {
        result.failedViewCommandIds.push(commandId)
      }
    }
  } finally {
    if (resultPath) {
      fs.writeFileSync(resultPath, JSON.stringify(result, null, 2) + '\\n')
    }
  }

  if (
    !result.extensionActivated ||
    result.registeredTreeViewIds.length !== viewIds.length ||
    result.treeProviderViewIds.length !== viewIds.length ||
    result.failedFocusViewIds.length > 0 ||
    result.viewItemCommandIds.length === 0 ||
    result.failedViewCommandIds.length > 0 ||
    result.executedViewCommandIds.length !== result.viewItemCommandIds.length ||
    viewIds.some((viewId) => (result.viewItemCounts[viewId] || 0) === 0)
  ) {
    throw new Error('OpenClaude workbench smoke failed')
  }
}

module.exports = { run }
`

  if (viewIds.length === 0 || extensionId === 'undefined.undefined') {
    throw new Error('Cannot write workbench smoke runner without manifest view IDs and extension ID')
  }

  writeFileSync(extensionTestsPath, source)
}

function writeReports(report: WorkbenchReport): void {
  mkdirSync(docsDir, { recursive: true })
  const publicReport = scrubPublicArtifactValue(report)
  writeFileSync(resolve(docsDir, 'ide-extension-workbench-smoke-report.json'), `${JSON.stringify(publicReport, null, 2)}\n`)

  const formatList = (items: string[]): string => items.length === 0 ? '`none`' : items.map((item) => `\`${item}\``).join(', ')
  const lines = [
    '# IDE Extension Workbench Smoke Report',
    '',
    'Generated by: `bun run product:ide-extension-workbench-smoke`',
    '',
    '## Primary Source Basis',
    '',
    '- VS Code official Tree View API documentation defines package view contributions, TreeDataProvider registration, and workbench view activation.',
    '- VS Code official extension testing documentation defines Extension Development Host integration tests with `--extensionDevelopmentPath` and `--extensionTestsPath`.',
    '',
    '## Claim Boundary',
    '',
    '- This report launches a local VS Code Extension Development Host only for workbench tree-view smoke evidence.',
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
    '## Views',
    '',
    `- contributed_view_ids: ${formatList(report.contributedViewIds)}`,
    `- registered_tree_view_ids: ${formatList(report.registeredTreeViewIds)}`,
    `- tree_provider_view_ids: ${formatList(report.treeProviderViewIds)}`,
    `- focused_view_ids: ${formatList(report.focusedViewIds)}`,
    `- failed_focus_view_ids: ${formatList(report.failedFocusViewIds)}`,
    `- view_item_counts: \`${JSON.stringify(report.viewItemCounts)}\``,
    `- view_item_command_ids: ${formatList(report.viewItemCommandIds)}`,
    `- executed_view_command_ids: ${formatList(report.executedViewCommandIds)}`,
    `- failed_view_command_ids: ${formatList(report.failedViewCommandIds)}`,
    '',
    '## Process Evidence',
    '',
    `- code_command: \`${report.codeCommand.join(' ')}\``,
    `- stdout_sha256: \`${report.stdoutSha256}\``,
    `- stderr_sha256: \`${report.stderrSha256}\``,
    `- stdout_byte_length: \`${report.stdoutByteLength}\``,
    `- stderr_byte_length: \`${report.stderrByteLength}\``,
    `- vscode_startup_blocked: \`${report.vscodeStartupBlocked}\``,
    `- environment_blockers: ${formatList(report.environmentBlockers)}`,
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.workbenchSmokeChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-workbench-smoke-report.md'), `${scrubPublicArtifactText(lines.join('\n'))}\n`)
}

function main(): void {
  const manifest = readJson<Manifest>(manifestPath)
  const viewIds = getManifestViewIds(manifest)
  const manifestCommandIds = getManifestCommandIds(manifest)
  const extensionId = `${manifest.publisher}.${manifest.name}`

  mkdirSync(tempRoot, { recursive: true })
  rmSync(tempDir, { recursive: true, force: true })
  mkdirSync(workspacePath, { recursive: true })
  mkdirSync(resolve(tempDir, 'user-data'), { recursive: true })
  mkdirSync(resolve(tempDir, 'extensions'), { recursive: true })
  writeRunner(viewIds, extensionId)

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
    env: sanitizedEnv(viewIds, extensionId),
    shell: false,
    timeout: 90000,
  })
  const runnerResult = waitForJsonResult<WorkbenchRunnerResult>(resultPath, 30000)
  const stdout = result.stdout ?? ''
  const stderr = result.stderr ?? ''
  const vscodeCliVersion = getVscodeCliVersion(root)
  const codeTimedOut = result.error?.message.includes('ETIMEDOUT') === true
  const environmentBlockers = withCliEnvironmentBlockers(
    collectVscodeEnvironmentBlockers(resolve(tempDir, 'user-data', 'logs')),
    result,
    vscodeCliVersion,
  )
  const vscodeStartupBlocked = environmentBlockers.length > 0
  const realExtensionHostLaunched = runnerResult !== null && !vscodeStartupBlocked
  const knownEnvironmentBlocked = vscodeStartupBlocked || environmentBlockers.includes('vscode_cli_unavailable')
  const registeredTreeViewIds = runnerResult?.registeredTreeViewIds ?? []
  const treeProviderViewIds = runnerResult?.treeProviderViewIds ?? []
  const focusedViewIds = runnerResult?.focusedViewIds ?? []
  const failedFocusViewIds = runnerResult?.failedFocusViewIds ?? viewIds
  const viewItemCounts = runnerResult?.viewItemCounts ?? Object.fromEntries(viewIds.map((viewId) => [viewId, 0]))
  const viewItemCommandIds = runnerResult?.viewItemCommandIds ?? []
  const executedViewCommandIds = runnerResult?.executedViewCommandIds ?? []
  const failedViewCommandIds = runnerResult?.failedViewCommandIds ?? viewItemCommandIds

  const workbenchSmokeChecks = [
    check('manifest view IDs are present', viewIds.length >= 2, viewIds.join(', ')),
    check('VS Code CLI version is available', vscodeCliVersion !== 'not_available', vscodeCliVersion),
    check('VS Code CLI command exited 0', result.status === 0, String(result.status)),
    check('VS Code CLI command did not time out', !codeTimedOut, String(codeTimedOut)),
    check('VS Code startup was not blocked by local environment state', !vscodeStartupBlocked, environmentBlockers.length === 0 ? 'none' : environmentBlockers.join(', ')),
    check('real Extension Development Host test runner produced result', realExtensionHostLaunched, runnerResult ? 'result file present' : 'result file missing'),
    check('extension activated in real host', runnerResult?.extensionActivated === true, String(runnerResult?.extensionActivated)),
    check('all contributed tree views are registered', viewIds.every((viewId) => registeredTreeViewIds.includes(viewId)), registeredTreeViewIds.join(', ')),
    check('all contributed tree views have providers', viewIds.every((viewId) => treeProviderViewIds.includes(viewId)), treeProviderViewIds.join(', ')),
    check('all contributed tree views can be focused', viewIds.every((viewId) => focusedViewIds.includes(viewId)) && failedFocusViewIds.length === 0, focusedViewIds.join(', ')),
    check('all contributed tree views provide items', viewIds.every((viewId) => (viewItemCounts[viewId] ?? 0) > 0), JSON.stringify(viewItemCounts)),
    check('tree item commands are declared manifest commands', viewItemCommandIds.length > 0 && viewItemCommandIds.every((commandId) => manifestCommandIds.includes(commandId)), viewItemCommandIds.join(', ')),
    check('all tree item commands execute in real host', viewItemCommandIds.length > 0 && viewItemCommandIds.every((commandId) => executedViewCommandIds.includes(commandId)) && failedViewCommandIds.length === 0, `${executedViewCommandIds.join(', ') || 'none'} / failed=${failedViewCommandIds.join(', ') || 'none'}`),
    check('protected actions were not attempted', true, 'install/publish/deploy/product-launch/provider/live/external all false'),
    check('extension availability claim remains blocked', true, 'extension availability claim allowed=false'),
  ]

  const report: WorkbenchReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_real_vscode_workbench_tree_view_smoke',
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
    extensionActivated: runnerResult?.extensionActivated === true,
    contributedViewIds: viewIds,
    registeredTreeViewIds,
    treeProviderViewIds,
    focusedViewIds,
    failedFocusViewIds,
    viewItemCounts,
    viewItemCommandIds,
    executedViewCommandIds,
    failedViewCommandIds,
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    productLaunchAttempted: false,
    extensionAvailabilityClaimAllowed: false,
    workbenchSmokeChecks,
    claimBoundary: 'Local VS Code Extension Development Host workbench tree-view smoke evidence only. This does not install, publish, deploy, product-launch, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeReports(report)

  if (workbenchSmokeChecks.every((item) => item.ok)) {
    rmSync(tempDir, { recursive: true, force: true })
  }

  for (const item of workbenchSmokeChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!workbenchSmokeChecks.every((item) => item.ok) && !knownEnvironmentBlocked) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log(`RESULT: ${workbenchSmokeChecks.every((item) => item.ok) ? 'PASS' : 'BLOCKED'}`)
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`code_exit_code=${report.codeExitCode}`)
  console.log(`extension_activated=${report.extensionActivated}`)
  console.log(`registered_tree_view_count=${report.registeredTreeViewIds.length}`)
  console.log(`focused_tree_view_count=${report.focusedViewIds.length}`)
  console.log(`executed_view_command_count=${report.executedViewCommandIds.length}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
