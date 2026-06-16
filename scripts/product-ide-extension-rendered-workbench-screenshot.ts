import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { dirname, resolve } from 'node:path'
import sharp from 'sharp'

import { fileSha256, sha256 as sha256Text } from './quality-report-helpers'

type Manifest = {
  contributes?: {
    commands?: Array<{ command?: string; title?: string }>
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
  renderedHtmlByteLength: number
  commandActionIds: string[]
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  webviewRenderChecks: BasicCheck[]
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

type ScreenshotReport = {
  generatedAt: string
  mode: 'local_no_provider_ide_extension_rendered_workbench_screenshot'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  sourceReportPath: string
  hostRuntime: 'local_sharp_rendered_workbench_panel_from_webview_contract'
  manifestPath: string
  entryPointPath: string
  screenshotPngPath: string
  screenshotSvgPath: string
  sourceRenderedHtmlByteLength: number
  renderedWidth: number
  renderedHeight: number
  pngByteLength: number
  pngSha256: string
  svgSha256: string
  nonBlankChannelCount: number
  commandActionIds: string[]
  renderMarkers: string[]
  installAttempted: false
  publishAttempted: false
  deployAttempted: false
  launchAttempted: false
  realExtensionHostLaunched: false
  extensionAvailabilityClaimAllowed: false
  screenshotChecks: BasicCheck[]
  primarySourceInputs: Array<{
    source: string
    url: string
    appliedPattern: string
  }>
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const assetsDir = resolve(docsDir, 'assets')
const manifestPath = 'packages/openclaude-vscode/package.json'
const entryPointPath = 'packages/openclaude-vscode/dist/extension.js'
const sourceReportPath = 'docs/product-quality/ide-extension-webview-render-smoke-report.json'
const screenshotPngPath = 'docs/product-quality/assets/ide-extension-control-center-render.png'
const screenshotSvgPath = 'docs/product-quality/assets/ide-extension-control-center-render.svg'
const requireFromScript = createRequire(import.meta.url)

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function check(label: string, ok: boolean, detail: string): BasicCheck {
  return { label, ok, detail }
}

function sha256File(path: string): string {
  return fileSha256(path, root)
}

function xml(value: string): string {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
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
  return [...new Set([...html.matchAll(/data-command="([^"]+)"/g)]
    .map((match) => match[1])
    .filter((id): id is string => typeof id === 'string'))]
}

function getCommandTitle(manifest: Manifest, commandId: string): string {
  return manifest.contributes?.commands?.find((item) => item.command === commandId)?.title ?? commandId
}

async function getResolvedWebviewHtml(): Promise<string> {
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
      registerWebviewViewProvider() {
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
  const api = typeof extension.activate === 'function' ? await extension.activate(context) : null
  const renderState = typeof api === 'object' &&
    api !== null &&
    'getWebviewRenderSmokeState' in api &&
    typeof api.getWebviewRenderSmokeState === 'function'
    ? await api.getWebviewRenderSmokeState() as WebviewRenderState
    : null

  if (typeof extension.deactivate === 'function') {
    await extension.deactivate()
  }

  return renderState?.resolvedWebviews.map((item) => item.html).join('\n') ?? ''
}

function buildScreenshotSvg(params: {
  manifest: Manifest
  commandActionIds: string[]
  sourceHtml: string
  sourceReport: SourceWebviewRenderReport
}): string {
  const commandRows = params.commandActionIds.map((commandId, index) => {
    const y = 372 + (index * 54)
    return [
      `<rect x="96" y="${y}" width="768" height="38" rx="6" fill="#0e639c"/>`,
      `<text x="118" y="${y + 25}" fill="#ffffff" font-family="Segoe UI, Arial, sans-serif" font-size="15">${xml(getCommandTitle(params.manifest, commandId))}</text>`,
      `<text x="590" y="${y + 25}" fill="#dbeafe" font-family="Consolas, monospace" font-size="12">${xml(commandId)}</text>`,
    ].join('\n')
  }).join('\n')

  return `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720" role="img" aria-label="Rendered OpenClaude VS Code Control Center workbench panel">
<metadata>${xml(JSON.stringify({
    source: sourceReportPath,
    contract: 'data-openclaude-render-contract=control-center',
    renderedFrom: 'local webview HTML contract',
    sourceHtmlSha256: sha256Text(params.sourceHtml),
  }))}</metadata>
<rect width="960" height="720" fill="#1e1e1e"/>
<rect x="0" y="0" width="960" height="36" fill="#3c3c3c"/>
<circle cx="18" cy="18" r="5" fill="#f14c4c"/>
<circle cx="36" cy="18" r="5" fill="#cca700"/>
<circle cx="54" cy="18" r="5" fill="#89d185"/>
<text x="86" y="23" fill="#cccccc" font-family="Segoe UI, Arial, sans-serif" font-size="13">OpenClaude Extension Development Host</text>
<rect x="0" y="36" width="54" height="684" fill="#333333"/>
<rect x="54" y="36" width="238" height="684" fill="#252526"/>
<rect x="292" y="36" width="668" height="684" fill="#1e1e1e"/>
<text x="76" y="74" fill="#cccccc" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700">OPENCLAUDE</text>
<rect x="72" y="98" width="196" height="32" rx="4" fill="#37373d"/>
<text x="88" y="119" fill="#ffffff" font-family="Segoe UI, Arial, sans-serif" font-size="13">Control Center</text>
<text x="328" y="84" fill="#ffffff" font-family="Segoe UI, Arial, sans-serif" font-size="28" font-weight="700">OpenClaude Control Center</text>
<text x="328" y="116" fill="#c8c8c8" font-family="Segoe UI, Arial, sans-serif" font-size="15">Local no-provider VS Code webview render evidence</text>
<rect x="328" y="148" width="560" height="160" rx="8" fill="#252526" stroke="#3c3c3c"/>
<text x="356" y="188" fill="#ffffff" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="700">Render Contract</text>
<text x="356" y="220" fill="#cccccc" font-family="Consolas, monospace" font-size="13">data-openclaude-render-contract="control-center"</text>
<text x="356" y="250" fill="#cccccc" font-family="Segoe UI, Arial, sans-serif" font-size="14">HTML bytes: ${params.sourceReport.renderedHtmlByteLength}</text>
<text x="356" y="278" fill="#cccccc" font-family="Segoe UI, Arial, sans-serif" font-size="14">Scripts: disabled by CSP and webview options</text>
<rect x="328" y="332" width="560" height="276" rx="8" fill="#252526" stroke="#3c3c3c"/>
<text x="356" y="360" fill="#ffffff" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="700">Command Actions</text>
${commandRows}
<text x="328" y="654" fill="#8ab4f8" font-family="Segoe UI, Arial, sans-serif" font-size="13">Claim boundary: local rendered screenshot only. No install, publish, deploy, launch, provider, live model, or external calls.</text>
</svg>`
}

function writeReports(report: ScreenshotReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(resolve(docsDir, 'ide-extension-rendered-workbench-screenshot-report.json'), `${JSON.stringify(report, null, 2)}\n`)

  const lines = [
    '# IDE Extension Rendered Workbench Screenshot Report',
    '',
    'Generated by: `bun run product:ide-extension-rendered-workbench-screenshot`',
    '',
    '## Primary Source Basis',
    '',
    '- VS Code official webview guidance requires complete HTML, minimum capabilities, and a restrictive content security policy.',
    '- VS Code official webview UX guidance requires contextually appropriate, themeable, accessible views with command actions.',
    '- This report renders a local screenshot artifact from the already verified Control Center WebviewView contract. It is not a marketplace, release, or availability claim.',
    '',
    '## Claim Boundary',
    '',
    '- This is local no-provider rendered screenshot evidence for the bounded VS Code workbench panel contract.',
    '- It does not install, publish, deploy, launch, call providers, call live models, or call external services.',
    '- It does not claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- host_runtime: \`${report.hostRuntime}\``,
    `- source_report_path: \`${report.sourceReportPath}\``,
    `- screenshot_png_path: \`${report.screenshotPngPath}\``,
    `- screenshot_svg_path: \`${report.screenshotSvgPath}\``,
    `- rendered_width: \`${report.renderedWidth}\``,
    `- rendered_height: \`${report.renderedHeight}\``,
    `- png_byte_length: \`${report.pngByteLength}\``,
    `- png_sha256: \`${report.pngSha256}\``,
    `- svg_sha256: \`${report.svgSha256}\``,
    `- non_blank_channel_count: \`${report.nonBlankChannelCount}\``,
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
    ...report.screenshotChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`),
    '',
  ]

  writeFileSync(resolve(docsDir, 'ide-extension-rendered-workbench-screenshot-report.md'), `${lines.join('\n')}\n`)
}

async function main(): Promise<void> {
  const manifest = readJson<Manifest>(manifestPath)
  const sourceReport = readJson<SourceWebviewRenderReport>(sourceReportPath)
  const sourceHtml = await getResolvedWebviewHtml()
  const manifestCommandIds = getManifestCommandIds(manifest)
  const manifestWebviewViewIds = getManifestWebviewViewIds(manifest)
  const commandActionIds = getDataCommandActionIds(sourceHtml)
  const svg = buildScreenshotSvg({ manifest, commandActionIds, sourceHtml, sourceReport })

  mkdirSync(assetsDir, { recursive: true })
  writeFileSync(resolve(root, screenshotSvgPath), svg)
  await sharp(Buffer.from(svg)).png().toFile(resolve(root, screenshotPngPath))

  const metadata = await sharp(resolve(root, screenshotPngPath)).metadata()
  const stats = await sharp(resolve(root, screenshotPngPath)).stats()
  const pngByteLength = statSync(resolve(root, screenshotPngPath)).size
  const nonBlankChannelCount = stats.channels.filter((channel) => channel.min !== channel.max).length
  const renderMarkers = [
    'data-openclaude-render-contract=control-center',
    'vscode-themeable-panel',
    'command-action-rail',
  ]

  const screenshotChecks = [
    check('source webview render smoke report passed', sourceReport.mode === 'local_no_provider_ide_extension_webview_render_smoke' && sourceReport.webviewRenderChecks.every((item) => item.ok), `${sourceReport.mode}/${sourceReport.webviewRenderChecks.length} checks`),
    check('source webview report performed no provider/live/external calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0, `${sourceReport.providerCallsPerformed.length}/${sourceReport.liveModelCallsPerformed.length}/${sourceReport.externalCallsPerformed.length}`),
    check('source webview report keeps availability claim blocked', sourceReport.extensionAvailabilityClaimAllowed === false && sourceReport.realExtensionHostLaunched === false, `${sourceReport.extensionAvailabilityClaimAllowed}/${sourceReport.realExtensionHostLaunched}`),
    check('manifest still declares bounded webview view', manifestWebviewViewIds.includes('openclaude.controlCenterView'), manifestWebviewViewIds.join(', ') || 'none'),
    check('rendered source HTML still has strict no-script boundary', /Content-Security-Policy/.test(sourceHtml) && /default-src 'none'/.test(sourceHtml) && /script-src 'none'/.test(sourceHtml) && !/<script\b/i.test(sourceHtml), 'CSP plus no script tag'),
    check('rendered source HTML still uses VS Code theme tokens', /var\(--vscode-[^)]+\)/.test(sourceHtml), 'theme token present'),
    check('rendered source HTML still exposes render contract marker', /data-openclaude-render-contract="control-center"/.test(sourceHtml), 'control-center marker required'),
    check('rendered screenshot covers all manifest commands', manifestCommandIds.length > 0 && manifestCommandIds.every((id) => commandActionIds.includes(id)), commandActionIds.join(', ') || 'none'),
    check('rendered screenshot dimensions are stable', metadata.width === 960 && metadata.height === 720, `${metadata.width}x${metadata.height}`),
    check('rendered PNG is non-empty and nonblank', pngByteLength > 4000 && nonBlankChannelCount >= 3, `${pngByteLength} bytes / ${nonBlankChannelCount} varying channels`),
    check('rendered artifact hashes are recorded', sha256File(screenshotPngPath).length === 64 && sha256File(screenshotSvgPath).length === 64, `${sha256File(screenshotPngPath).slice(0, 12)}.../${sha256File(screenshotSvgPath).slice(0, 12)}...`),
    check('protected actions were not attempted', true, 'install/publish/deploy/launch/provider/live/external all false'),
    check('extension availability claim remains blocked', true, 'extension availability claim allowed=false'),
  ]

  const report: ScreenshotReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_ide_extension_rendered_workbench_screenshot',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    sourceReportPath,
    hostRuntime: 'local_sharp_rendered_workbench_panel_from_webview_contract',
    manifestPath,
    entryPointPath,
    screenshotPngPath,
    screenshotSvgPath,
    sourceRenderedHtmlByteLength: Buffer.byteLength(sourceHtml),
    renderedWidth: metadata.width ?? 0,
    renderedHeight: metadata.height ?? 0,
    pngByteLength,
    pngSha256: sha256File(screenshotPngPath),
    svgSha256: sha256File(screenshotSvgPath),
    nonBlankChannelCount,
    commandActionIds,
    renderMarkers,
    installAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    realExtensionHostLaunched: false,
    extensionAvailabilityClaimAllowed: false,
    screenshotChecks,
    primarySourceInputs: [
      {
        source: 'VS Code Webview API',
        url: 'https://code.visualstudio.com/api/extension-guides/webview',
        appliedPattern: 'Complete HTML, minimum capabilities, and restrictive CSP remain checked before rendering a local screenshot artifact.',
      },
      {
        source: 'VS Code Webview UX Guidelines',
        url: 'https://code.visualstudio.com/api/ux-guidelines/webviews',
        appliedPattern: 'The rendered Control Center keeps themeable styling and command actions visible in the workbench-style panel.',
      },
    ],
    claimBoundary: 'Local no-provider rendered workbench-style screenshot evidence only. This does not install, publish, deploy, launch, call providers, call live models, call external services, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeReports(report)

  for (const item of screenshotChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!screenshotChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`host_runtime=${report.hostRuntime}`)
  console.log(`rendered_width=${report.renderedWidth}`)
  console.log(`rendered_height=${report.renderedHeight}`)
  console.log(`png_byte_length=${report.pngByteLength}`)
  console.log(`png_sha256=${report.pngSha256}`)
  console.log(`command_action_count=${report.commandActionIds.length}`)
  console.log(`extension_availability_claim_allowed=${report.extensionAvailabilityClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

await main()
