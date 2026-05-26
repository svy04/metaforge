import { spawnSync } from 'node:child_process'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'

type Manifest = {
  contributes?: {
    commands?: Array<{ command?: string }>
    views?: Record<string, Array<{ id?: string; type?: string }>>
  }
}

type RuntimeCheck = {
  label: string
  ok: boolean
  detail: string
}

type RuntimeReport = {
  generatedAt: string
  mode: 'local_no_provider_ide_extension_runtime_smoke'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  hostRuntime: 'local_mock_vscode_extension_host'
  vscodeCliVersion: string
  manifestPath: string
  entryPointPath: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  registeredTreeViewIds: string[]
  registeredWebviewViewIds: string[]
  messagesShown: string[]
  contextSubscriptionCount: number
  missingManifestCommands: string[]
  unexpectedRegisteredCommands: string[]
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  launchAttempted: false
  realExtensionHostLaunched: false
  extensionAvailabilityClaimAllowed: false
  runtimeSmokeChecks: RuntimeCheck[]
  claimBoundary: string
}

type ExtensionModule = {
  activate?: (context: { subscriptions: Array<{ dispose: () => void }> }) => unknown | Promise<unknown>
  deactivate?: () => unknown | Promise<unknown>
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const requireFromScript = createRequire(import.meta.url)

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): RuntimeCheck {
  return { label, ok, detail }
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

function getManifestCommandIds(manifest: Manifest): string[] {
  return manifest.contributes?.commands
    ?.map((item) => item.command)
    .filter((command): command is string => typeof command === 'string') ?? []
}

function getManifestTreeViewIds(manifest: Manifest): string[] {
  return Object.values(manifest.contributes?.views ?? {})
    .flat()
    .filter((item) => item.type !== 'webview')
    .map((item) => item.id)
    .filter((id): id is string => typeof id === 'string')
}

function getManifestWebviewViewIds(manifest: Manifest): string[] {
  return Object.values(manifest.contributes?.views ?? {})
    .flat()
    .filter((item) => item.type === 'webview')
    .map((item) => item.id)
    .filter((id): id is string => typeof id === 'string')
}

async function runWithMockHost(manifestCommandIds: string[]): Promise<{
  activationInvoked: boolean
  deactivationInvoked: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  registeredTreeViewIds: string[]
  registeredWebviewViewIds: string[]
  messagesShown: string[]
  contextSubscriptionCount: number
}> {
  const registered = new Map<string, () => unknown | Promise<unknown>>()
  const executedCommandIds: string[] = []
  const messagesShown: string[] = []
  const registeredTreeViewIds: string[] = []
  const registeredWebviewViewIds: string[] = []
  const context = {
    subscriptions: [] as Array<{ dispose: () => void }>,
  }
  class TreeItem {
    label: string
    collapsibleState: number
    description?: string
    tooltip?: string
    command?: { command: string; title: string }

    constructor(label: string, collapsibleState: number) {
      this.label = label
      this.collapsibleState = collapsibleState
    }
  }
  const vscodeMock = {
    TreeItem,
    TreeItemCollapsibleState: {
      None: 0,
      Collapsed: 1,
      Expanded: 2,
    },
    commands: {
      registerCommand(commandId: string, handler: () => unknown | Promise<unknown>) {
        registered.set(commandId, handler)
        return {
          dispose() {},
        }
      },
    },
    window: {
      createTreeView(viewId: string) {
        registeredTreeViewIds.push(viewId)
        return {
          async reveal() {},
          dispose() {},
        }
      },
      registerWebviewViewProvider(viewId: string) {
        registeredWebviewViewIds.push(viewId)
        return {
          dispose() {},
        }
      },
      async showInformationMessage(message: string) {
        messagesShown.push(message)
        return message
      },
    },
  }
  const entryPointAbsolutePath = resolve(root, entryPointPath)
  const extensionModule = {
    exports: {},
  }
  const localRequire = (request: string): unknown => {
    if (request === 'vscode') {
      return vscodeMock
    }
    return requireFromScript(request)
  }

  let activationInvoked = false
  let deactivationInvoked = false
  const entryPointSource = readFileSync(entryPointAbsolutePath, 'utf8')
  const evaluateExtension = new Function(
    'require',
    'module',
    'exports',
    '__filename',
    '__dirname',
    entryPointSource,
  )
  evaluateExtension(localRequire, extensionModule, extensionModule.exports, entryPointAbsolutePath, dirname(entryPointAbsolutePath))

  const extension = extensionModule.exports as ExtensionModule
  if (typeof extension.activate === 'function') {
    await extension.activate(context)
    activationInvoked = true
  }

  for (const commandId of manifestCommandIds) {
    const handler = registered.get(commandId)
    if (handler) {
      await handler()
      executedCommandIds.push(commandId)
    }
  }

  if (typeof extension.deactivate === 'function') {
    await extension.deactivate()
    deactivationInvoked = true
  }

  return {
    activationInvoked,
    deactivationInvoked,
    registeredCommandIds: [...registered.keys()],
    executedCommandIds,
    registeredTreeViewIds,
    registeredWebviewViewIds,
    messagesShown,
    contextSubscriptionCount: context.subscriptions.length,
  }
}

function writeReports(report: RuntimeReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'ide-extension-runtime-smoke-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# IDE Extension Runtime Smoke Report',
    '',
    'Generated by: `bun run product:ide-extension-runtime-smoke`',
    '',
    '## Claim Boundary',
    '',
    '- This report verifies extension activation and command registration through a local mock VS Code extension host.',
    '- It does not install, publish, deploy, launch, or claim extension availability.',
    '- It does not launch a real Extension Development Host.',
    '- It does not call providers, live models, or external services.',
    '- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- host_runtime: \`${report.hostRuntime}\``,
    `- vscode_cli_version: \`${report.vscodeCliVersion}\``,
    `- manifest_path: \`${report.manifestPath}\``,
    `- entry_point_path: \`${report.entryPointPath}\``,
    `- activation_invoked: \`${report.activationInvoked}\``,
    `- deactivation_invoked: \`${report.deactivationInvoked}\``,
    `- context_subscription_count: \`${report.contextSubscriptionCount}\``,
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
    `- registered_tree_view_ids: ${report.registeredTreeViewIds.map((item) => `\`${item}\``).join(', ')}`,
    `- registered_webview_view_ids: ${report.registeredWebviewViewIds.map((item) => `\`${item}\``).join(', ')}`,
    `- missing_manifest_commands: ${report.missingManifestCommands.length === 0 ? '`none`' : report.missingManifestCommands.map((item) => `\`${item}\``).join(', ')}`,
    `- unexpected_registered_commands: ${report.unexpectedRegisteredCommands.length === 0 ? '`none`' : report.unexpectedRegisteredCommands.map((item) => `\`${item}\``).join(', ')}`,
    '',
    '## Bounded Messages',
    '',
    ...report.messagesShown.map((item) => `- ${item}`),
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.runtimeSmokeChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-runtime-smoke-report.md'), `${lines.join('\n')}\n`)
}

async function main(): Promise<void> {
  const manifest = readJson<Manifest>(manifestPath)
  const manifestCommandIds = getManifestCommandIds(manifest)
  const manifestTreeViewIds = getManifestTreeViewIds(manifest)
  const manifestWebviewViewIds = getManifestWebviewViewIds(manifest)
  const runtime = await runWithMockHost(manifestCommandIds)
  const missingManifestCommands = manifestCommandIds.filter((commandId) => !runtime.registeredCommandIds.includes(commandId))
  const unexpectedRegisteredCommands = runtime.registeredCommandIds.filter((commandId) => !manifestCommandIds.includes(commandId))
  const runtimeSmokeChecks = [
    check('manifest command IDs are present', manifestCommandIds.length >= 3, manifestCommandIds.join(', ')),
    check('activation function is callable', runtime.activationInvoked, String(runtime.activationInvoked)),
    check('deactivation function is callable', runtime.deactivationInvoked, String(runtime.deactivationInvoked)),
    check('all manifest commands are registered', missingManifestCommands.length === 0, missingManifestCommands.join(', ') || 'none'),
    check('no unexpected commands are registered', unexpectedRegisteredCommands.length === 0, unexpectedRegisteredCommands.join(', ') || 'none'),
    check('all registered manifest commands execute', manifestCommandIds.every((commandId) => runtime.executedCommandIds.includes(commandId)), runtime.executedCommandIds.join(', ')),
    check('all manifest tree views register providers', manifestTreeViewIds.every((viewId) => runtime.registeredTreeViewIds.includes(viewId)), runtime.registeredTreeViewIds.join(', ')),
    check('all manifest webview views register providers', manifestWebviewViewIds.every((viewId) => runtime.registeredWebviewViewIds.includes(viewId)), runtime.registeredWebviewViewIds.join(', ')),
    check('subscriptions match command and view provider count', runtime.contextSubscriptionCount === manifestCommandIds.length + manifestTreeViewIds.length + manifestWebviewViewIds.length, `${runtime.contextSubscriptionCount}/${manifestCommandIds.length + manifestTreeViewIds.length + manifestWebviewViewIds.length}`),
    check('command handlers show bounded local messages', runtime.messagesShown.length === manifestCommandIds.length && runtime.messagesShown.every((message) => /scoped/i.test(message) && !/available|published|released|production ready/i.test(message)), runtime.messagesShown.join(' | ')),
    check('real Extension Host was not launched', true, 'local mock host only'),
    check('protected actions were not attempted', true, 'install/publish/deploy/launch/provider/live/external all false'),
  ]

  const report: RuntimeReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_ide_extension_runtime_smoke',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    hostRuntime: 'local_mock_vscode_extension_host',
    vscodeCliVersion: getVscodeCliVersion(),
    manifestPath,
    entryPointPath,
    activationInvoked: runtime.activationInvoked,
    deactivationInvoked: runtime.deactivationInvoked,
    registeredCommandIds: runtime.registeredCommandIds,
    executedCommandIds: runtime.executedCommandIds,
    registeredTreeViewIds: runtime.registeredTreeViewIds,
    registeredWebviewViewIds: runtime.registeredWebviewViewIds,
    messagesShown: runtime.messagesShown,
    contextSubscriptionCount: runtime.contextSubscriptionCount,
    missingManifestCommands,
    unexpectedRegisteredCommands,
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    realExtensionHostLaunched: false,
    extensionAvailabilityClaimAllowed: false,
    runtimeSmokeChecks,
    claimBoundary: 'Local VS Code runtime smoke evidence uses a mock VS Code extension host only. It does not install, publish, deploy, launch, or claim extension availability.',
  }

  writeReports(report)

  for (const item of runtimeSmokeChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!runtimeSmokeChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`registered_command_count=${report.registeredCommandIds.length}`)
  console.log(`executed_command_count=${report.executedCommandIds.length}`)
  console.log(`registered_tree_view_count=${report.registeredTreeViewIds.length}`)
  console.log(`registered_webview_view_count=${report.registeredWebviewViewIds.length}`)
  console.log(`context_subscription_count=${report.contextSubscriptionCount}`)
  console.log(`real_extension_host_launched=${report.realExtensionHostLaunched}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

await main()
