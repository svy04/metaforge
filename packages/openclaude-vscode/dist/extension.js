'use strict'

const COMMANDS = [
  'openclaude.openChat',
  'openclaude.runSelection',
  'openclaude.explainSelection',
  'openclaude.openRuntimeDoctor',
]

const WORKBENCH_VIEWS = [
  {
    id: 'openclaude.chatView',
    items: [
      {
        label: 'OpenClaude Chat',
        description: 'Scoped CLI handoff',
        command: 'openclaude.openChat',
      },
      {
        label: 'Run Selection',
        description: 'Bounded command surface',
        command: 'openclaude.runSelection',
      },
    ],
  },
  {
    id: 'openclaude.traceEvidenceView',
    items: [
      {
        label: 'Runtime Doctor',
        description: 'Local no-provider diagnostics',
        command: 'openclaude.openRuntimeDoctor',
      },
      {
        label: 'Trace Evidence',
        description: 'Product-quality gate evidence',
        command: 'openclaude.explainSelection',
      },
    ],
  },
]

const WORKBENCH_WEBVIEWS = [
  {
    id: 'openclaude.controlCenterView',
    title: 'OpenClaude Control Center',
  },
]

const SCOPED_MESSAGE = 'OpenClaude VS Code surface is scoped. Use the verified OpenClaude CLI until full extension validation is complete.'

function activate(context) {
  const vscode = require('vscode')
  const treeProviders = new Map()
  const treeViews = new Map()
  const webviewProviders = new Map()
  const registeredTreeViewIds = []
  const registeredWebviewViewIds = []

  for (const command of COMMANDS) {
    context.subscriptions.push(
      vscode.commands.registerCommand(command, () => {
        void vscode.window.showInformationMessage(SCOPED_MESSAGE)
        return {
          status: 'scoped',
          command,
          message: SCOPED_MESSAGE,
        }
      }),
    )
  }

  for (const view of WORKBENCH_VIEWS) {
    const provider = createTreeProvider(vscode, view.items)
    const treeView = vscode.window.createTreeView(view.id, {
      treeDataProvider: provider,
      showCollapseAll: false,
    })
    treeProviders.set(view.id, provider)
    treeViews.set(view.id, treeView)
    registeredTreeViewIds.push(view.id)
    context.subscriptions.push(treeView)
  }

  for (const view of WORKBENCH_WEBVIEWS) {
    const provider = createWebviewViewProvider(view)
    const disposable = vscode.window.registerWebviewViewProvider(view.id, provider)
    webviewProviders.set(view.id, provider)
    registeredWebviewViewIds.push(view.id)
    context.subscriptions.push(disposable)
  }

  return {
    getWorkbenchSmokeState() {
      return {
        commandIds: [...COMMANDS],
        contributedViewIds: WORKBENCH_VIEWS.map((view) => view.id),
        contributedWebviewViewIds: WORKBENCH_WEBVIEWS.map((view) => view.id),
        registeredTreeViewIds: [...registeredTreeViewIds],
        registeredWebviewViewIds: [...registeredWebviewViewIds],
        treeProviderViewIds: [...treeProviders.keys()],
        viewItemCounts: Object.fromEntries(WORKBENCH_VIEWS.map((view) => [view.id, view.items.length])),
      }
    },
    async getWebviewRenderSmokeState() {
      const resolvedWebviews = []
      for (const [viewId, provider] of webviewProviders.entries()) {
        resolvedWebviews.push(await resolveWebviewForSmoke(viewId, provider))
      }

      return {
        webviewViewIds: WORKBENCH_WEBVIEWS.map((view) => view.id),
        registeredWebviewViewIds: [...registeredWebviewViewIds],
        resolvedWebviews,
      }
    },
    async revealWorkbenchSmokeItem(viewId) {
      const provider = treeProviders.get(viewId)
      const treeView = treeViews.get(viewId)
      if (!provider || !treeView) {
        return false
      }

      const children = await provider.getChildren()
      const firstChild = children[0]
      if (!firstChild) {
        return false
      }

      await treeView.reveal(firstChild, {
        focus: true,
        select: true,
      })
      return true
    },
    async getWorkbenchSmokeItems(viewId) {
      const provider = treeProviders.get(viewId)
      if (!provider) {
        return []
      }

      const children = await provider.getChildren()
      return children.map((item) => {
        const treeItem = provider.getTreeItem(item)
        return {
          label: treeItem.label,
          description: treeItem.description,
          command: treeItem.command && treeItem.command.command,
        }
      })
    },
  }
}

function deactivate() {}

async function resolveWebviewForSmoke(viewId, provider) {
  const webviewView = {
    webview: {
      html: '',
      options: {},
    },
  }
  await provider.resolveWebviewView(webviewView)

  return {
    viewId,
    html: webviewView.webview.html,
    options: webviewView.webview.options,
  }
}

function createTreeProvider(vscode, items) {
  return {
    getChildren(element) {
      return Promise.resolve(element ? [] : items)
    },
    getParent() {
      return undefined
    },
    getTreeItem(item) {
      const treeItem = new vscode.TreeItem(item.label, vscode.TreeItemCollapsibleState.None)
      treeItem.description = item.description
      treeItem.tooltip = `${item.label}: ${item.description}`
      treeItem.command = {
        command: item.command,
        title: item.label,
      }
      return treeItem
    },
  }
}

function createWebviewViewProvider(view) {
  return {
    resolveWebviewView(webviewView) {
      webviewView.webview.options = {
        enableScripts: false,
      }
      webviewView.webview.html = renderControlCenterWebviewHtml(view)
    },
  }
}

function renderControlCenterWebviewHtml(view) {
  const commandButtons = COMMANDS.map((command) => `
        <button type="button" class="command" data-command="${escapeHtml(command)}" aria-label="${escapeHtml(command)}">
          <span class="command-id">${escapeHtml(command)}</span>
        </button>`).join('')

  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'none'; style-src 'unsafe-inline'; script-src 'none';">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${escapeHtml(view.title)}</title>
    <style>
      :root {
        color-scheme: light dark;
      }

      body {
        margin: 0;
        padding: 14px;
        color: var(--vscode-editor-foreground);
        background: var(--vscode-sideBar-background);
        font-family: var(--vscode-font-family);
        font-size: var(--vscode-font-size);
      }

      main {
        display: grid;
        gap: 14px;
      }

      h1,
      h2,
      p {
        margin: 0;
      }

      h1 {
        font-size: 1.15rem;
        font-weight: 600;
      }

      h2 {
        font-size: 0.95rem;
        font-weight: 600;
      }

      section {
        display: grid;
        gap: 8px;
        border: 1px solid var(--vscode-panel-border);
        padding: 10px;
      }

      .grid {
        display: grid;
        gap: 6px;
      }

      .row {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        border-bottom: 1px solid var(--vscode-panel-border);
        padding-bottom: 6px;
      }

      .row:last-child {
        border-bottom: 0;
        padding-bottom: 0;
      }

      .label {
        color: var(--vscode-descriptionForeground);
      }

      .value {
        color: var(--vscode-editor-foreground);
        font-weight: 600;
        text-align: right;
      }

      .commands {
        display: grid;
        gap: 6px;
      }

      .command {
        width: 100%;
        border: 1px solid var(--vscode-button-border, transparent);
        color: var(--vscode-button-foreground);
        background: var(--vscode-button-background);
        padding: 7px 9px;
        text-align: left;
        font: inherit;
      }

      .command-id {
        overflow-wrap: anywhere;
      }

      .boundary {
        color: var(--vscode-descriptionForeground);
        line-height: 1.45;
      }
    </style>
  </head>
  <body>
    <main data-openclaude-render-contract="control-center" aria-labelledby="openclaude-control-title">
      <header>
        <h1 id="openclaude-control-title">OpenClaude Control Center</h1>
      </header>
      <section aria-labelledby="local-runtime-state">
        <h2 id="local-runtime-state">Local Runtime State</h2>
        <div class="grid">
          <div class="row"><span class="label">Provider profile</span><span class="value">local</span></div>
          <div class="row"><span class="label">Permission mode</span><span class="value">default</span></div>
          <div class="row"><span class="label">Telemetry</span><span class="value">blocked by default</span></div>
          <div class="row"><span class="label">Trace capture</span><span class="value">operator-gated</span></div>
        </div>
      </section>
      <section aria-labelledby="command-actions">
        <h2 id="command-actions">Command Actions</h2>
        <div class="commands" role="list" aria-label="OpenClaude command action contract">
${commandButtons}
        </div>
      </section>
      <section aria-labelledby="claim-boundary">
        <h2 id="claim-boundary">Claim Boundary</h2>
        <p class="boundary">This local webview render contract is internal no-provider evidence only. Install, publish, deploy, product launch, provider calls, live model calls, external calls, extension availability claims, production-readiness claims, public claims, external-validation claims, and autonomous-reliability claims remain blocked.</p>
      </section>
    </main>
  </body>
</html>`
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

module.exports = {
  activate,
  deactivate,
}
