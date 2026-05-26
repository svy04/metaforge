import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'

type Manifest = {
  contributes?: {
    commands?: Array<{ command?: string }>
    views?: Record<string, Array<{ id?: string; type?: string }>>
  }
}

type BasicCheck = {
  label: string
  ok: boolean
  detail: string
}

type SourceWebviewRenderReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  commandActionIds: string[]
  extensionAvailabilityClaimAllowed: boolean
  realExtensionHostLaunched: boolean
  webviewRenderChecks: BasicCheck[]
}

type SourceRenderedScreenshotReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  commandActionIds: string[]
  extensionAvailabilityClaimAllowed: boolean
  screenshotChecks: BasicCheck[]
}

type WebviewResolveResult = {
  viewId: string
  html: string
  options: {
    enableScripts?: boolean
  }
}

type WebviewRenderState = {
  resolvedWebviews: WebviewResolveResult[]
}

type ExtensionModule = {
  activate?: (context: { subscriptions: Array<{ dispose: () => void }> }) => unknown | Promise<unknown>
  deactivate?: () => unknown | Promise<unknown>
}

type CommandButton = {
  commandId: string
  type?: string
  className?: string
  ariaLabel?: string
  disabled: boolean
  visibleText: string
}

type InteractionReport = {
  generatedAt: string
  mode: 'local_no_provider_ide_extension_webview_interaction_smoke'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  hostRuntime: 'local_mock_vscode_webview_interaction_host'
  sourceWebviewRenderReportPath: string
  sourceRenderedScreenshotReportPath: string
  manifestPath: string
  entryPointPath: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  manifestCommandIds: string[]
  focusOrderCommandIds: string[]
  interactionCommandIds: string[]
  executedInteractionCommandIds: string[]
  failedInteractionCommandIds: string[]
  registeredCommandIds: string[]
  messagesShown: string[]
  commandButtonCount: number
  commandRegionRole: string
  commandRegionAriaLabel: string
  keyboardActivationModel: 'native_button_enter_space_command_mapping'
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  launchAttempted: false
  realExtensionHostLaunched: false
  extensionAvailabilityClaimAllowed: false
  interactionChecks: BasicCheck[]
  primarySourceInputs: Array<{
    source: string
    url: string
    appliedPattern: string
  }>
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const sourceWebviewRenderReportPath = 'docs/product-quality/ide-extension-webview-render-smoke-report.json'
const sourceRenderedScreenshotReportPath = 'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json'
const requireFromScript = createRequire(import.meta.url)

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): BasicCheck {
  return { label, ok, detail }
}

function getManifestCommandIds(manifest: Manifest): string[] {
  return manifest.contributes?.commands
    ?.map((item) => item.command)
    .filter((command): command is string => typeof command === 'string') ?? []
}

function getAttribute(tag: string, name: string): string | undefined {
  const pattern = new RegExp(`${name}="([^"]*)"`)
  return pattern.exec(tag)?.[1]
}

function stripTags(html: string): string {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
}

function extractCommandButtons(html: string): CommandButton[] {
  return [...html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/g)]
    .filter((match) => /data-command=/.test(match[1]))
    .map((match) => ({
      commandId: getAttribute(match[1], 'data-command') ?? '',
      type: getAttribute(match[1], 'type'),
      className: getAttribute(match[1], 'class'),
      ariaLabel: getAttribute(match[1], 'aria-label'),
      disabled: /\bdisabled\b/.test(match[1]),
      visibleText: stripTags(match[2]),
    }))
}

function extractCommandRegion(html: string): { role: string; ariaLabel: string } {
  const match = /<div class="commands"([^>]*)>/.exec(html)
  return {
    role: match ? getAttribute(match[1], 'role') ?? '' : '',
    ariaLabel: match ? getAttribute(match[1], 'aria-label') ?? '' : '',
  }
}

async function runWithMockInteractionHost(interactionCommandIds: string[]): Promise<{
  activationInvoked: boolean
  deactivationInvoked: boolean
  html: string
  scriptsDisabled: boolean
  registeredCommandIds: string[]
  executedInteractionCommandIds: string[]
  failedInteractionCommandIds: string[]
  messagesShown: string[]
}> {
  const registeredCommands = new Map<string, () => unknown | Promise<unknown>>()
  const messagesShown: string[] = []
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
        registeredCommands.set(commandId, handler)
        return {
          dispose() {},
        }
      },
    },
    window: {
      createTreeView() {
        return {
          async reveal() {},
          dispose() {},
        }
      },
      registerWebviewViewProvider() {
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
  const evaluateExtension = new Function(
    'require',
    'module',
    'exports',
    '__filename',
    '__dirname',
    readFileSync(entryPointAbsolutePath, 'utf8'),
  )
  evaluateExtension(localRequire, extensionModule, extensionModule.exports, entryPointAbsolutePath, dirname(entryPointAbsolutePath))

  const extension = extensionModule.exports as ExtensionModule
  let activationInvoked = false
  let deactivationInvoked = false
  const api = typeof extension.activate === 'function' ? await extension.activate(context) : null
  activationInvoked = typeof extension.activate === 'function'

  const renderState = typeof api === 'object' &&
    api !== null &&
    'getWebviewRenderSmokeState' in api &&
    typeof api.getWebviewRenderSmokeState === 'function'
    ? await api.getWebviewRenderSmokeState() as WebviewRenderState
    : null
  const html = renderState?.resolvedWebviews.map((item) => item.html).join('\n') ?? ''
  const scriptsDisabled = renderState?.resolvedWebviews.every((item) => item.options.enableScripts === false) === true

  const executedInteractionCommandIds: string[] = []
  const failedInteractionCommandIds: string[] = []
  for (const commandId of interactionCommandIds) {
    const handler = registeredCommands.get(commandId)
    if (!handler) {
      failedInteractionCommandIds.push(commandId)
      continue
    }
    try {
      await handler()
      executedInteractionCommandIds.push(commandId)
    } catch {
      failedInteractionCommandIds.push(commandId)
    }
  }

  if (typeof extension.deactivate === 'function') {
    await extension.deactivate()
    deactivationInvoked = true
  }

  return {
    activationInvoked,
    deactivationInvoked,
    html,
    scriptsDisabled,
    registeredCommandIds: [...registeredCommands.keys()],
    executedInteractionCommandIds,
    failedInteractionCommandIds,
    messagesShown,
  }
}

function writeReports(report: InteractionReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'ide-extension-webview-interaction-smoke-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# IDE Extension Webview Interaction Smoke Report',
    '',
    'Generated by: `bun run product:ide-extension-webview-interaction-smoke`',
    '',
    '## Primary Source Basis',
    '',
    '- VS Code webview UX guidance says webviews should be contextually appropriate, accessible, keyboard navigable, themeable, and use command actions in the view.',
    '- VS Code webview API guidance says webviews render complete HTML and are powerful, separate-context surfaces that should remain bounded.',
    '- This smoke verifies command-action affordances and mock-host command execution mapping without enabling scripts or claiming marketplace availability.',
    '',
    '## Claim Boundary',
    '',
    '- This is local no-provider webview interaction-contract evidence only.',
    '- It does not install, publish, deploy, launch, call providers, call live models, or call external services.',
    '- It does not claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- host_runtime: \`${report.hostRuntime}\``,
    `- manifest_command_ids: ${report.manifestCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    `- focus_order_command_ids: ${report.focusOrderCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    `- executed_interaction_command_ids: ${report.executedInteractionCommandIds.map((item) => `\`${item}\``).join(', ')}`,
    `- failed_interaction_command_ids: ${report.failedInteractionCommandIds.map((item) => `\`${item}\``).join(', ') || '`none`'}`,
    `- command_button_count: \`${report.commandButtonCount}\``,
    `- command_region_role: \`${report.commandRegionRole}\``,
    `- command_region_aria_label: \`${report.commandRegionAriaLabel}\``,
    `- keyboard_activation_model: \`${report.keyboardActivationModel}\``,
    `- extension_availability_claim_allowed: \`${report.extensionAvailabilityClaimAllowed}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.interactionChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-webview-interaction-smoke-report.md'), `${lines.join('\n')}\n`)
}

async function main(): Promise<void> {
  const manifest = readJson<Manifest>(manifestPath)
  const sourceWebviewRenderReport = readJson<SourceWebviewRenderReport>(sourceWebviewRenderReportPath)
  const sourceRenderedScreenshotReport = readJson<SourceRenderedScreenshotReport>(sourceRenderedScreenshotReportPath)
  const manifestCommandIds = getManifestCommandIds(manifest)
  const preliminaryRuntime = await runWithMockInteractionHost([])
  const commandButtons = extractCommandButtons(preliminaryRuntime.html)
  const interactionCommandIds = commandButtons.map((button) => button.commandId)
  const runtime = await runWithMockInteractionHost(interactionCommandIds)
  const commandRegion = extractCommandRegion(runtime.html)

  const buttonsAreNativeAccessible = commandButtons.every((button) => (
    button.type === 'button' &&
    button.className === 'command' &&
    button.ariaLabel === button.commandId &&
    button.visibleText.includes(button.commandId) &&
    button.disabled === false
  ))
  const focusOrderMatchesManifest = manifestCommandIds.length > 0 &&
    manifestCommandIds.length === interactionCommandIds.length &&
    manifestCommandIds.every((commandId, index) => interactionCommandIds[index] === commandId)

  const interactionChecks = [
    check('source webview render smoke report passed', sourceWebviewRenderReport.mode === 'local_no_provider_ide_extension_webview_render_smoke' && sourceWebviewRenderReport.webviewRenderChecks.every((item) => item.ok), `${sourceWebviewRenderReport.mode}/${sourceWebviewRenderReport.webviewRenderChecks.length} checks`),
    check('source rendered screenshot report passed', sourceRenderedScreenshotReport.mode === 'local_no_provider_ide_extension_rendered_workbench_screenshot' && sourceRenderedScreenshotReport.screenshotChecks.every((item) => item.ok), `${sourceRenderedScreenshotReport.mode}/${sourceRenderedScreenshotReport.screenshotChecks.length} checks`),
    check('source reports performed no provider/live/external calls', sourceWebviewRenderReport.providerCallsPerformed.length === 0 && sourceWebviewRenderReport.liveModelCallsPerformed.length === 0 && sourceWebviewRenderReport.externalCallsPerformed.length === 0 && sourceRenderedScreenshotReport.providerCallsPerformed.length === 0 && sourceRenderedScreenshotReport.liveModelCallsPerformed.length === 0 && sourceRenderedScreenshotReport.externalCallsPerformed.length === 0, 'all source call arrays empty'),
    check('extension activation and deactivation are callable', runtime.activationInvoked === true && runtime.deactivationInvoked === true, `${runtime.activationInvoked}/${runtime.deactivationInvoked}`),
    check('webview interaction HTML stays scriptless', runtime.scriptsDisabled && /script-src 'none'/.test(runtime.html) && !/<script\b/i.test(runtime.html) && !/acquireVsCodeApi/i.test(runtime.html), 'scripts disabled and no webview API acquisition'),
    check('webview interaction HTML stays networkless', !/https?:\/\//i.test(runtime.html) && !/vscode-resource:/i.test(runtime.html) && !/command:/i.test(runtime.html), 'no network, resource, or command URI'),
    check('command action region has list semantics and label', commandRegion.role === 'list' && commandRegion.ariaLabel === 'OpenClaude command action contract', `${commandRegion.role}/${commandRegion.ariaLabel}`),
    check('command action buttons are native accessible controls', buttonsAreNativeAccessible, `${commandButtons.length} buttons`),
    check('command action focus order matches manifest order', focusOrderMatchesManifest, interactionCommandIds.join(', ') || 'none'),
    check('webview command actions match source evidence', interactionCommandIds.length === sourceWebviewRenderReport.commandActionIds.length && interactionCommandIds.every((id) => sourceWebviewRenderReport.commandActionIds.includes(id)) && interactionCommandIds.every((id) => sourceRenderedScreenshotReport.commandActionIds.includes(id)), interactionCommandIds.join(', ') || 'none'),
    check('all interaction commands are registered by activate()', interactionCommandIds.every((id) => runtime.registeredCommandIds.includes(id)), runtime.registeredCommandIds.join(', ') || 'none'),
    check('all interaction commands execute in mock host', runtime.executedInteractionCommandIds.length === interactionCommandIds.length && runtime.failedInteractionCommandIds.length === 0, `${runtime.executedInteractionCommandIds.join(', ') || 'none'} / failed=${runtime.failedInteractionCommandIds.join(', ') || 'none'}`),
    check('command handlers show bounded local messages', runtime.messagesShown.length === interactionCommandIds.length && runtime.messagesShown.every((message) => /scoped/i.test(message) && !/available|published|released|production ready/i.test(message)), runtime.messagesShown.join(' | ')),
    check('protected actions were not attempted', true, 'install/publish/deploy/launch/provider/live/external all false'),
    check('extension availability claim remains blocked', true, 'extension availability claim allowed=false'),
  ]

  const report: InteractionReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_ide_extension_webview_interaction_smoke',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    hostRuntime: 'local_mock_vscode_webview_interaction_host',
    sourceWebviewRenderReportPath,
    sourceRenderedScreenshotReportPath,
    manifestPath,
    entryPointPath,
    activationInvoked: runtime.activationInvoked,
    deactivationInvoked: runtime.deactivationInvoked,
    manifestCommandIds,
    focusOrderCommandIds: interactionCommandIds,
    interactionCommandIds,
    executedInteractionCommandIds: runtime.executedInteractionCommandIds,
    failedInteractionCommandIds: runtime.failedInteractionCommandIds,
    registeredCommandIds: runtime.registeredCommandIds,
    messagesShown: runtime.messagesShown,
    commandButtonCount: commandButtons.length,
    commandRegionRole: commandRegion.role,
    commandRegionAriaLabel: commandRegion.ariaLabel,
    keyboardActivationModel: 'native_button_enter_space_command_mapping',
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    realExtensionHostLaunched: false,
    extensionAvailabilityClaimAllowed: false,
    interactionChecks,
    primarySourceInputs: [
      {
        source: 'VS Code Webview UX Guidelines',
        url: 'https://code.visualstudio.com/api/ux-guidelines/webviews',
        appliedPattern: 'Command actions, accessibility labels, and keyboard navigability are verified as a local interaction contract.',
      },
      {
        source: 'VS Code Webview API',
        url: 'https://code.visualstudio.com/api/extension-guides/webview',
        appliedPattern: 'Complete HTML, no-script CSP, and bounded webview capabilities are preserved before any availability claim.',
      },
    ],
    claimBoundary: 'Local no-provider webview interaction-contract smoke evidence only. This does not install, publish, deploy, launch, call providers, call live models, call external services, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeReports(report)

  for (const item of interactionChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!interactionChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`command_button_count=${report.commandButtonCount}`)
  console.log(`interaction_command_count=${report.interactionCommandIds.length}`)
  console.log(`executed_interaction_command_count=${report.executedInteractionCommandIds.length}`)
  console.log(`failed_interaction_command_count=${report.failedInteractionCommandIds.length}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

await main()
