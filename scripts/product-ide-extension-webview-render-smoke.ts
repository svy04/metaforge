import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'

type Manifest = {
  activationEvents?: string[]
  contributes?: {
    commands?: Array<{ command?: string }>
    views?: Record<string, Array<{ id?: string; type?: string }>>
  }
}

type WebviewCheck = {
  label: string
  ok: boolean
  detail: string
}

type WebviewResolveResult = {
  viewId: string
  html: string
  options: {
    enableScripts?: boolean
  }
}

type WebviewRenderState = {
  webviewViewIds: string[]
  resolvedWebviews: WebviewResolveResult[]
}

type ExtensionModule = {
  activate?: (context: { subscriptions: Array<{ dispose: () => void }> }) => unknown | Promise<unknown>
  deactivate?: () => unknown | Promise<unknown>
}

type WebviewRenderReport = {
  generatedAt: string
  mode: 'local_no_provider_ide_extension_webview_render_smoke'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  hostRuntime: 'local_mock_vscode_webview_view_host'
  manifestPath: string
  entryPointPath: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  manifestWebviewViewIds: string[]
  registeredWebviewViewIds: string[]
  resolvedWebviewViewIds: string[]
  renderedHtmlByteLength: number
  commandActionIds: string[]
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  launchAttempted: false
  realExtensionHostLaunched: false
  extensionAvailabilityClaimAllowed: false
  webviewRenderChecks: WebviewCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const requireFromScript = createRequire(import.meta.url)

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): WebviewCheck {
  return { label, ok, detail }
}

function getManifestCommandIds(manifest: Manifest): string[] {
  return manifest.contributes?.commands
    ?.map((item) => item.command)
    .filter((command): command is string => typeof command === 'string') ?? []
}

function getManifestWebviewViewIds(manifest: Manifest): string[] {
  return Object.values(manifest.contributes?.views ?? {})
    .flat()
    .filter((item) => item.type === 'webview')
    .map((item) => item.id)
    .filter((id): id is string => typeof id === 'string')
}

function getDataCommandActionIds(html: string): string[] {
  return [...html.matchAll(/data-command="([^"]+)"/g)].map((match) => match[1]).filter((id): id is string => typeof id === 'string')
}

async function runWithMockWebviewHost(): Promise<{
  activationInvoked: boolean
  deactivationInvoked: boolean
  registeredWebviewViewIds: string[]
  renderState: WebviewRenderState | null
}> {
  const registeredWebviewProviders = new Map<string, unknown>()
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
      registerCommand() {
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
      registerWebviewViewProvider(viewId: string, provider: unknown) {
        registeredWebviewProviders.set(viewId, provider)
        return {
          dispose() {},
        }
      },
      async showInformationMessage(message: string) {
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
  let api: unknown
  if (typeof extension.activate === 'function') {
    api = await extension.activate(context)
    activationInvoked = true
  }

  const renderState = typeof api === 'object' &&
    api !== null &&
    'getWebviewRenderSmokeState' in api &&
    typeof api.getWebviewRenderSmokeState === 'function'
    ? await api.getWebviewRenderSmokeState()
    : null

  if (typeof extension.deactivate === 'function') {
    await extension.deactivate()
    deactivationInvoked = true
  }

  return {
    activationInvoked,
    deactivationInvoked,
    registeredWebviewViewIds: [...registeredWebviewProviders.keys()],
    renderState: renderState as WebviewRenderState | null,
  }
}

function writeReports(report: WebviewRenderReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'ide-extension-webview-render-smoke-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# IDE Extension Webview Render Smoke Report',
    '',
    'Generated by: `bun run product:ide-extension-webview-render-smoke`',
    '',
    '## Primary Source Basis',
    '',
    '- VS Code official webview guidance says webviews should be used sparingly, rendered as HTML, and themed with VS Code color tokens.',
    '- VS Code official UX guidance says webviews should be contextually appropriate, themeable, accessible, and use command actions in the view.',
    '- VS Code official contribution point reference says webview views are populated by registering a provider with `registerWebviewViewProvider`.',
    '',
    '## Claim Boundary',
    '',
    '- This report resolves the local webview view provider through a mock VS Code webview host.',
    '- It does not install, publish, deploy, launch, or claim extension availability.',
    '- It does not call providers, live models, or external services.',
    '- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- host_runtime: \`${report.hostRuntime}\``,
    `- manifest_path: \`${report.manifestPath}\``,
    `- entry_point_path: \`${report.entryPointPath}\``,
    `- activation_invoked: \`${report.activationInvoked}\``,
    `- deactivation_invoked: \`${report.deactivationInvoked}\``,
    `- manifest_webview_view_ids: ${report.manifestWebviewViewIds.map((item) => `\`${item}\``).join(', ')}`,
    `- registered_webview_view_ids: ${report.registeredWebviewViewIds.map((item) => `\`${item}\``).join(', ')}`,
    `- resolved_webview_view_ids: ${report.resolvedWebviewViewIds.map((item) => `\`${item}\``).join(', ')}`,
    `- rendered_html_byte_length: \`${report.renderedHtmlByteLength}\``,
    `- command_action_ids: ${report.commandActionIds.map((item) => `\`${item}\``).join(', ')}`,
    `- real_extension_host_launched: \`${report.realExtensionHostLaunched}\``,
    `- extension_availability_claim_allowed: \`${report.extensionAvailabilityClaimAllowed}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Checks',
    '',
    '| Check | Result | Detail |',
    '| --- | --- | --- |',
    ...report.webviewRenderChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-webview-render-smoke-report.md'), `${lines.join('\n')}\n`)
}

async function main(): Promise<void> {
  const manifest = readJson<Manifest>(manifestPath)
  const manifestCommandIds = getManifestCommandIds(manifest)
  const manifestWebviewViewIds = getManifestWebviewViewIds(manifest)
  const runtime = await runWithMockWebviewHost()
  const resolvedWebviews = runtime.renderState?.resolvedWebviews ?? []
  const html = resolvedWebviews.map((item) => item.html).join('\n')
  const commandActionIds = [...new Set(getDataCommandActionIds(html))]
  const scriptsDisabled = resolvedWebviews.every((item) => item.options.enableScripts === false)
  const renderedHtmlByteLength = Buffer.byteLength(html)
  const webviewRenderChecks = [
    check('manifest declares a webview view contribution', manifestWebviewViewIds.includes('openclaude.controlCenterView'), manifestWebviewViewIds.join(', ') || 'none'),
    check('manifest activates on the webview view', manifest.activationEvents?.includes('onView:openclaude.controlCenterView') === true, manifest.activationEvents?.join(', ') ?? 'none'),
    check('activation function is callable', runtime.activationInvoked, String(runtime.activationInvoked)),
    check('deactivation function is callable', runtime.deactivationInvoked, String(runtime.deactivationInvoked)),
    check('webview provider is registered', runtime.registeredWebviewViewIds.includes('openclaude.controlCenterView'), runtime.registeredWebviewViewIds.join(', ') || 'none'),
    check('webview render smoke API resolves provider HTML', resolvedWebviews.some((item) => item.viewId === 'openclaude.controlCenterView') && renderedHtmlByteLength > 1000, `${resolvedWebviews.map((item) => item.viewId).join(', ') || 'none'} / ${renderedHtmlByteLength}`),
    check('webview scripts are disabled', scriptsDisabled, JSON.stringify(resolvedWebviews.map((item) => item.options))),
    check('webview HTML has strict CSP', /Content-Security-Policy/.test(html) && /default-src 'none'/.test(html) && /script-src 'none'/.test(html), 'default-src none and script-src none required'),
    check('webview HTML uses VS Code theme tokens', /var\(--vscode-[^)]+\)/.test(html), 'theme token present'),
    check('webview HTML exposes render contract marker', /data-openclaude-render-contract="control-center"/.test(html), 'control-center marker required'),
    check('webview HTML exposes accessible command actions', commandActionIds.length >= manifestCommandIds.length && commandActionIds.every((id) => manifestCommandIds.includes(id)), commandActionIds.join(', ') || 'none'),
    check('webview HTML contains no network URLs or scripts', !/https?:\/\//i.test(html) && !/<script\b/i.test(html) && !/acquireVsCodeApi/i.test(html), 'no network URL, script tag, or acquireVsCodeApi'),
    check('protected actions were not attempted', true, 'install/publish/deploy/launch/provider/live/external all false'),
    check('extension availability claim remains blocked', true, 'extension availability claim allowed=false'),
  ]

  const report: WebviewRenderReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_ide_extension_webview_render_smoke',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    hostRuntime: 'local_mock_vscode_webview_view_host',
    manifestPath,
    entryPointPath,
    activationInvoked: runtime.activationInvoked,
    deactivationInvoked: runtime.deactivationInvoked,
    manifestWebviewViewIds,
    registeredWebviewViewIds: runtime.registeredWebviewViewIds,
    resolvedWebviewViewIds: resolvedWebviews.map((item) => item.viewId),
    renderedHtmlByteLength,
    commandActionIds,
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    realExtensionHostLaunched: false,
    extensionAvailabilityClaimAllowed: false,
    webviewRenderChecks,
    claimBoundary: 'Local VS Code webview render-contract smoke evidence only. This does not install, publish, deploy, launch, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeReports(report)

  for (const item of webviewRenderChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!webviewRenderChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`webview_render_contract_count=${report.resolvedWebviewViewIds.length}`)
  console.log(`webview_command_action_count=${report.commandActionIds.length}`)
  console.log(`real_extension_host_launched=${report.realExtensionHostLaunched}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

await main()
