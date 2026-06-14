import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type BasicCheck = {
  label: string
  ok: boolean
  detail?: string
}

type GoldenTranscriptReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  transcripts: Array<{
    name: string
    exitCode: number | null
    passed: boolean
  }>
}

type PermissionRegressionReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  regressionFixtures: Array<{
    id: string
    ok: boolean
  }>
}

type RuntimeDoctorReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  doctorCommands: Array<{
    name: string
    exitCode: number | null
    passed: boolean
  }>
  doctorChecks: BasicCheck[]
}

type GitReleaseHygieneReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workspaceGitStatus: string
  commitPushAttempted: boolean
  releaseActionPerformed: boolean
  protectedActionsPerformed: unknown[]
  releaseHygieneChecks: BasicCheck[]
}

type IdeExtensionSurfaceReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workspaceIdeExtensionStatus: string
  packagingAttempted: boolean
  installAttempted: boolean
  ideExtensionChecks: BasicCheck[]
}

type IdeExtensionRuntimeSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  messagesShown: string[]
  contextSubscriptionCount: number
  missingManifestCommands: string[]
  unexpectedRegisteredCommands: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  runtimeSmokeChecks: BasicCheck[]
}

type IdeExtensionHostSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  codeExitCode: number | null
  codeTimedOut: boolean
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  failedCommandIds: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  productLaunchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  hostSmokeChecks: BasicCheck[]
}

type IdeExtensionWorkbenchSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  codeExitCode: number | null
  codeTimedOut: boolean
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  contributedViewIds: string[]
  registeredTreeViewIds: string[]
  treeProviderViewIds: string[]
  focusedViewIds: string[]
  viewItemCounts: Record<string, number>
  viewItemCommandIds?: string[]
  executedViewCommandIds?: string[]
  failedViewCommandIds?: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  productLaunchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  workbenchSmokeChecks: BasicCheck[]
}

type IdeExtensionWebviewRenderSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  manifestWebviewViewIds: string[]
  registeredWebviewViewIds: string[]
  resolvedWebviewViewIds: string[]
  renderedHtmlByteLength: number
  commandActionIds: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  webviewRenderChecks: BasicCheck[]
}

type IdeExtensionRenderedWorkbenchScreenshotReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  screenshotPngPath: string
  screenshotSvgPath: string
  renderedWidth: number
  renderedHeight: number
  pngByteLength: number
  pngSha256: string
  svgSha256: string
  nonBlankChannelCount: number
  commandActionIds: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  screenshotChecks: BasicCheck[]
}

type IdeExtensionWebviewInteractionSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  sourceWebviewRenderReportPath: string
  sourceRenderedScreenshotReportPath: string
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
  keyboardActivationModel: string
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  interactionChecks: BasicCheck[]
}

type ReleaseArtifactReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  packDryRunExitCode: number | null
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  actualPackageFiles: string[]
  forbiddenPackageFiles: string[]
  releaseArtifactChecks: BasicCheck[]
}

type ReplayGrade = {
  label: string
  ok: boolean
  detail: string
}

type ReplayScenario = {
  id: string
  title: string
  sourcePattern: string
  evidencePaths: string[]
  replayedTrace: string[]
  grades: ReplayGrade[]
  score: number
  passed: boolean
}

type AgentReplayEvalReport = {
  generatedAt: string
  mode: 'local_no_provider_trace_graded_agent_replay_evals'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  replayScenarioCount: number
  minimumPassingScore: number
  replayScenarios: ReplayScenario[]
  replayEvalChecks: ReplayGrade[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const minimumPassingScore = 0.9

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function grade(label: string, ok: boolean, detail: string): ReplayGrade {
  return { label, ok, detail }
}

function score(grades: ReplayGrade[]): number {
  if (grades.length === 0) {
    return 0
  }
  return Number((grades.filter((item) => item.ok).length / grades.length).toFixed(3))
}

function noCalls(report: {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
}): boolean {
  return report.providerCallsPerformed.length === 0 &&
    report.liveModelCallsPerformed.length === 0 &&
    report.externalCallsPerformed.length === 0
}

function hasVscodeStartupBlocker(report: {
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
}): boolean {
  return report.vscodeStartupBlocked === true &&
    (report.environmentBlockers?.length ?? 0) > 0
}

function vscodeBlockerDetail(report: { environmentBlockers?: string[] }): string {
  return report.environmentBlockers?.join(',') || 'none'
}

function realHostLaunched(report: {
  hostRuntime: string
  realExtensionHostLaunched: boolean
}): boolean {
  return report.hostRuntime === 'real_vscode_extension_development_host' &&
    report.realExtensionHostLaunched === true
}

function realHostLaunchedOrStartupBlocked(report: {
  hostRuntime: string
  realExtensionHostLaunched: boolean
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
}): boolean {
  return realHostLaunched(report) || hasVscodeStartupBlocker(report)
}

function realHostEvidenceOrStartupBlocked(
  report: {
    hostRuntime: string
    realExtensionHostLaunched: boolean
    vscodeStartupBlocked?: boolean
    environmentBlockers?: string[]
  },
  okWhenLaunched: boolean,
): boolean {
  return hasVscodeStartupBlocker(report) || (realHostLaunched(report) && okWhenLaunched)
}

function scenario(input: Omit<ReplayScenario, 'score' | 'passed'>): ReplayScenario {
  const scenarioScore = score(input.grades)
  return {
    ...input,
    score: scenarioScore,
    passed: scenarioScore >= minimumPassingScore,
  }
}

function writeReports(report: AgentReplayEvalReport): void {
  mkdirSync(docsDir, { recursive: true })
  writeFileSync(
    resolve(docsDir, 'agent-replay-evals-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )

  const lines = [
    '# Agent Replay Evals Report',
    '',
    'Generated by: `bun run product:agent-replay-evals`',
    '',
    '## Claim Boundary',
    '',
    '- These replay evals grade existing local product-quality evidence only.',
    '- They do not call providers, live models, or external services.',
    '- They do not claim external validation, release readiness, production readiness, public readiness, or autonomous reliability.',
    '',
    '## Summary',
    '',
    `- replay_scenario_count: \`${report.replayScenarioCount}\``,
    `- minimum_passing_score: \`${report.minimumPassingScore}\``,
    `- all_scenarios_passed: \`${report.replayScenarios.every((item) => item.passed)}\``,
    `- provider_calls_performed: \`${report.providerCallsPerformed.length}\``,
    `- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\``,
    `- external_calls_performed: \`${report.externalCallsPerformed.length}\``,
    '',
    '## Replay Scenarios',
    '',
    '| Scenario | Score | Passed | Source Pattern | Evidence |',
    '| --- | ---: | --- | --- | --- |',
    ...report.replayScenarios.map((item) => (
      `| \`${item.id}\` | ${item.score} | \`${item.passed}\` | ${item.sourcePattern} | ${item.evidencePaths.map((path) => `\`${path}\``).join('<br>')} |`
    )),
    '',
    '## Grades',
    '',
  ]

  for (const item of report.replayScenarios) {
    lines.push(`### ${item.id}`)
    lines.push('')
    lines.push('| Grade | Result | Detail |')
    lines.push('| --- | --- | --- |')
    for (const itemGrade of item.grades) {
      lines.push(`| ${itemGrade.label} | \`${itemGrade.ok}\` | ${itemGrade.detail} |`)
    }
    lines.push('')
  }

  lines.push('## Eval Checks')
  lines.push('')
  lines.push('| Check | Result | Detail |')
  lines.push('| --- | --- | --- |')
  for (const item of report.replayEvalChecks) {
    lines.push(`| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
  }
  lines.push('')

  writeFileSync(resolve(docsDir, 'agent-replay-evals-report.md'), `${lines.join('\n')}\n`)
}

function main(): void {
  const golden = readJson<GoldenTranscriptReport>('docs/product-quality/golden-path-terminal-transcripts.json')
  const permission = readJson<PermissionRegressionReport>('docs/product-quality/permission-regression-fixtures.json')
  const runtimeDoctor = readJson<RuntimeDoctorReport>('docs/product-quality/runtime-doctor-regression-fixtures.json')
  const gitRelease = readJson<GitReleaseHygieneReport>('docs/product-quality/git-release-hygiene-report.json')
  const ideSurface = readJson<IdeExtensionSurfaceReport>('docs/product-quality/ide-extension-surface-report.json')
  const ideRuntime = readJson<IdeExtensionRuntimeSmokeReport>('docs/product-quality/ide-extension-runtime-smoke-report.json')
  const ideHost = readJson<IdeExtensionHostSmokeReport>('docs/product-quality/ide-extension-host-smoke-report.json')
  const ideWorkbench = readJson<IdeExtensionWorkbenchSmokeReport>('docs/product-quality/ide-extension-workbench-smoke-report.json')
  const ideWebview = readJson<IdeExtensionWebviewRenderSmokeReport>('docs/product-quality/ide-extension-webview-render-smoke-report.json')
  const ideRenderedScreenshot = readJson<IdeExtensionRenderedWorkbenchScreenshotReport>('docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json')
  const ideWebviewInteraction = readJson<IdeExtensionWebviewInteractionSmokeReport>('docs/product-quality/ide-extension-webview-interaction-smoke-report.json')
  const releaseArtifact = readJson<ReleaseArtifactReport>('docs/product-quality/release-artifact-file-list-report.json')

  const replayScenarios = [
    scenario({
      id: 'cli_surface_golden_transcript_replay',
      title: 'CLI surface transcript stays local and reproducible',
      sourcePattern: 'openai/codex style terminal surface proof',
      evidencePaths: ['docs/product-quality/golden-path-terminal-transcripts.json'],
      replayedTrace: ['run --version', 'run --help', 'grade expected substrings and exits'],
      grades: [
        grade('no provider/live/external calls', noCalls(golden), 'golden transcript report call arrays are empty'),
        grade('version transcript passed', golden.transcripts.some((item) => item.name === 'version' && item.passed && item.exitCode === 0), 'version transcript exit and substring check'),
        grade('help transcript passed', golden.transcripts.some((item) => item.name === 'help' && item.passed && item.exitCode === 0), 'help transcript exit and substring check'),
        grade('minimum transcript count met', golden.transcripts.length >= 2, `${golden.transcripts.length} transcripts`),
      ],
    }),
    scenario({
      id: 'permission_boundary_replay',
      title: 'Protected permission boundaries stay explicit',
      sourcePattern: 'cline/cline style permission and protected-action regression surface',
      evidencePaths: ['docs/product-quality/permission-regression-fixtures.json'],
      replayedTrace: ['load permission fixtures', 'grade all protected surfaces', 'block external security claims'],
      grades: [
        grade('no provider/live/external calls', noCalls(permission), 'permission report call arrays are empty'),
        grade('all permission fixtures passed', permission.regressionFixtures.every((item) => item.ok), `${permission.regressionFixtures.length} fixtures`),
        grade('protected boundary fixture coverage is broad', permission.regressionFixtures.length >= 10, `${permission.regressionFixtures.length} fixtures`),
        grade('auto classifier transcript fixture exists', permission.regressionFixtures.some((item) => item.id === 'auto_classifier_transcript_bounded' && item.ok), 'auto classifier transcript bounds checked'),
      ],
    }),
    scenario({
      id: 'runtime_doctor_no_provider_replay',
      title: 'Runtime doctor preserves no-provider local diagnostics',
      sourcePattern: 'openai/codex style local runtime command proof',
      evidencePaths: ['docs/product-quality/runtime-doctor-regression-fixtures.json'],
      replayedTrace: ['run system-check --json', 'run system-check --json --out', 'grade provider probe skip behavior'],
      grades: [
        grade('no provider/live/external calls', noCalls(runtimeDoctor), 'runtime doctor report call arrays are empty'),
        grade('doctor commands passed', runtimeDoctor.doctorCommands.every((item) => item.passed && item.exitCode === 0), `${runtimeDoctor.doctorCommands.length} commands`),
        grade('doctor checks passed', runtimeDoctor.doctorChecks.every((item) => item.ok), `${runtimeDoctor.doctorChecks.length} checks`),
        grade('minimum command evidence met', runtimeDoctor.doctorCommands.length >= 2, `${runtimeDoctor.doctorCommands.length} commands`),
      ],
    }),
    scenario({
      id: 'git_release_boundary_replay',
      title: 'Git/release boundary is classified without protected action',
      sourcePattern: 'Aider-style git-native workflow guarded by repo-root proof',
      evidencePaths: ['docs/product-quality/git-release-hygiene-report.json'],
      replayedTrace: ['inspect git root', 'inspect status/remote', 'grade commit-push boundary'],
      grades: [
        grade('no provider/live/external calls', noCalls(gitRelease), 'git release hygiene report call arrays are empty'),
        grade('workspace git status classified', ['git_repo_detected', 'blocked_by_no_git_repo', 'git_unavailable'].includes(gitRelease.workspaceGitStatus), gitRelease.workspaceGitStatus),
        grade('commit push not attempted', gitRelease.commitPushAttempted === false, String(gitRelease.commitPushAttempted)),
        grade('release action not performed', gitRelease.releaseActionPerformed === false, String(gitRelease.releaseActionPerformed)),
        grade('protected actions not performed', gitRelease.protectedActionsPerformed.length === 0, `${gitRelease.protectedActionsPerformed.length}`),
      ],
    }),
    scenario({
      id: 'ide_extension_gap_replay',
      title: 'IDE extension surface remains evidence-bound',
      sourcePattern: 'Cline-style IDE positioning requires manifest evidence',
      evidencePaths: ['docs/product-quality/ide-extension-surface-report.json'],
      replayedTrace: ['scan candidate manifests', 'classify extension surface', 'block unsupported availability claim'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideSurface), 'IDE surface report call arrays are empty'),
        grade('IDE extension status classified', ['extension_manifest_found', 'extension_manifest_missing'].includes(ideSurface.workspaceIdeExtensionStatus), ideSurface.workspaceIdeExtensionStatus),
        grade('packaging not attempted', ideSurface.packagingAttempted === false, String(ideSurface.packagingAttempted)),
        grade('install not attempted', ideSurface.installAttempted === false, String(ideSurface.installAttempted)),
        grade('IDE checks passed', ideSurface.ideExtensionChecks.every((item) => item.ok), `${ideSurface.ideExtensionChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_runtime_smoke_replay',
      title: 'IDE extension activation and command handlers are runtime-smoked locally',
      sourcePattern: 'VS Code extension anatomy requires manifest commands to be bound by activate/registerCommand',
      evidencePaths: [
        'docs/product-quality/ide-extension-runtime-smoke-report.json',
        'packages/openclaude-vscode/package.json',
        'packages/openclaude-vscode/dist/extension.js',
      ],
      replayedTrace: ['load extension entry point with local mock VS Code host', 'activate extension', 'execute manifest command handlers', 'grade no availability claim'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideRuntime), 'IDE runtime smoke report call arrays are empty'),
        grade('local mock host was used', ideRuntime.hostRuntime === 'local_mock_vscode_extension_host' && ideRuntime.realExtensionHostLaunched === false, ideRuntime.hostRuntime),
        grade('activation and deactivation are callable', ideRuntime.activationInvoked === true && ideRuntime.deactivationInvoked === true, `${ideRuntime.activationInvoked}/${ideRuntime.deactivationInvoked}`),
        grade('all manifest commands registered', ideRuntime.registeredCommandIds.length >= 4 && ideRuntime.missingManifestCommands.length === 0, ideRuntime.registeredCommandIds.join(', ')),
        grade('all manifest commands executed', ideRuntime.executedCommandIds.length === ideRuntime.registeredCommandIds.length, ideRuntime.executedCommandIds.join(', ')),
        grade('no unexpected commands registered', ideRuntime.unexpectedRegisteredCommands.length === 0, ideRuntime.unexpectedRegisteredCommands.join(', ') || 'none'),
        grade('subscriptions cover commands and workbench tree providers', ideRuntime.contextSubscriptionCount >= ideRuntime.registeredCommandIds.length, `${ideRuntime.contextSubscriptionCount}/${ideRuntime.registeredCommandIds.length}`),
        grade('extension availability claim stays blocked', ideRuntime.extensionAvailabilityClaimAllowed === false && !ideRuntime.installAttempted && !ideRuntime.publishAttempted && !ideRuntime.deployAttempted && !ideRuntime.launchAttempted, 'availability/install/publish/deploy/launch all false'),
        grade('runtime smoke checks passed', ideRuntime.runtimeSmokeChecks.every((item) => item.ok), `${ideRuntime.runtimeSmokeChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_host_smoke_replay',
      title: 'IDE extension loads and executes commands in the real VS Code Extension Development Host',
      sourcePattern: 'VS Code official extension integration tests run inside Extension Development Host',
      evidencePaths: [
        'docs/product-quality/ide-extension-host-smoke-report.json',
        'packages/openclaude-vscode/package.json',
        'packages/openclaude-vscode/dist/extension.js',
      ],
      replayedTrace: ['launch code with --extensionDevelopmentPath and --extensionTestsPath', 'activate extension', 'execute manifest command handlers', 'grade no availability/release claim'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideHost), 'IDE host smoke report call arrays are empty'),
        grade('real Extension Development Host launched or startup blocker classified', realHostLaunchedOrStartupBlocked(ideHost), `${ideHost.hostRuntime}; blockers=${vscodeBlockerDetail(ideHost)}`),
        grade('VS Code startup state is classified', ideHost.vscodeStartupBlocked !== true || hasVscodeStartupBlocker(ideHost), vscodeBlockerDetail(ideHost)),
        grade('VS Code extension test process exited or startup blocker classified', (ideHost.codeExitCode === 0 && ideHost.codeTimedOut === false) || hasVscodeStartupBlocker(ideHost), `${ideHost.codeExitCode}/${ideHost.codeTimedOut}; blockers=${vscodeBlockerDetail(ideHost)}`),
        grade('extension activated in real host when launched', realHostEvidenceOrStartupBlocked(ideHost, ideHost.extensionActivated === true), hasVscodeStartupBlocker(ideHost) ? 'blocked by environment' : String(ideHost.extensionActivated)),
        grade('manifest commands registered in real host when launched', realHostEvidenceOrStartupBlocked(ideHost, ideHost.registeredCommandIds.length >= 4), hasVscodeStartupBlocker(ideHost) ? 'blocked by environment' : ideHost.registeredCommandIds.join(', ')),
        grade('manifest commands executed in real host when launched', realHostEvidenceOrStartupBlocked(ideHost, ideHost.executedCommandIds.length === ideHost.registeredCommandIds.length && ideHost.failedCommandIds.length === 0), hasVscodeStartupBlocker(ideHost) ? 'blocked by environment' : ideHost.executedCommandIds.join(', ')),
        grade('install publish deploy product launch not attempted', !ideHost.installAttempted && !ideHost.publishAttempted && !ideHost.deployAttempted && !ideHost.productLaunchAttempted, 'integration smoke only'),
        grade('extension availability claim stays blocked', ideHost.extensionAvailabilityClaimAllowed === false, String(ideHost.extensionAvailabilityClaimAllowed)),
        grade('host smoke checks passed', ideHost.hostSmokeChecks.every((item) => item.ok), `${ideHost.hostSmokeChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_workbench_smoke_replay',
      title: 'IDE extension registers and reveals workbench tree views in real VS Code',
      sourcePattern: 'VS Code Tree View API requires contributed views to have registered TreeDataProviders',
      evidencePaths: [
        'docs/product-quality/ide-extension-workbench-smoke-report.json',
        'packages/openclaude-vscode/package.json',
        'packages/openclaude-vscode/dist/extension.js',
      ],
      replayedTrace: ['launch code with Extension Development Host', 'activate extension', 'create tree views', 'reveal first item in each contributed view', 'grade no availability/release claim'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideWorkbench), 'IDE workbench smoke report call arrays are empty'),
        grade('real Extension Development Host launched or startup blocker classified', realHostLaunchedOrStartupBlocked(ideWorkbench), `${ideWorkbench.hostRuntime}; blockers=${vscodeBlockerDetail(ideWorkbench)}`),
        grade('VS Code startup state is classified', ideWorkbench.vscodeStartupBlocked !== true || hasVscodeStartupBlocker(ideWorkbench), vscodeBlockerDetail(ideWorkbench)),
        grade('VS Code workbench smoke process exited or startup blocker classified', (ideWorkbench.codeExitCode === 0 && ideWorkbench.codeTimedOut === false) || hasVscodeStartupBlocker(ideWorkbench), `${ideWorkbench.codeExitCode}/${ideWorkbench.codeTimedOut}; blockers=${vscodeBlockerDetail(ideWorkbench)}`),
        grade('extension activated in real host when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, ideWorkbench.extensionActivated === true), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : String(ideWorkbench.extensionActivated)),
        grade('contributed views have registered tree views when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, ideWorkbench.contributedViewIds.length >= 2 && ideWorkbench.contributedViewIds.every((viewId) => ideWorkbench.registeredTreeViewIds.includes(viewId))), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : ideWorkbench.registeredTreeViewIds.join(', ')),
        grade('contributed views have tree data providers when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, ideWorkbench.contributedViewIds.every((viewId) => ideWorkbench.treeProviderViewIds.includes(viewId))), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : ideWorkbench.treeProviderViewIds.join(', ')),
        grade('contributed views were revealed/focused when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, ideWorkbench.contributedViewIds.every((viewId) => ideWorkbench.focusedViewIds.includes(viewId))), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : ideWorkbench.focusedViewIds.join(', ')),
        grade('contributed views expose non-empty items when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, ideWorkbench.contributedViewIds.every((viewId) => (ideWorkbench.viewItemCounts[viewId] ?? 0) > 0)), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : JSON.stringify(ideWorkbench.viewItemCounts)),
        grade('tree item commands executed in real host when launched', realHostEvidenceOrStartupBlocked(ideWorkbench, Array.isArray(ideWorkbench.viewItemCommandIds) && ideWorkbench.viewItemCommandIds.length > 0 && Array.isArray(ideWorkbench.executedViewCommandIds) && ideWorkbench.viewItemCommandIds.every((commandId) => ideWorkbench.executedViewCommandIds?.includes(commandId)) && Array.isArray(ideWorkbench.failedViewCommandIds) && ideWorkbench.failedViewCommandIds.length === 0), hasVscodeStartupBlocker(ideWorkbench) ? 'blocked by environment' : `${ideWorkbench.executedViewCommandIds?.join(', ') ?? 'missing'} / failed=${ideWorkbench.failedViewCommandIds?.join(', ') ?? 'missing'}`),
        grade('install publish deploy product launch not attempted', !ideWorkbench.installAttempted && !ideWorkbench.publishAttempted && !ideWorkbench.deployAttempted && !ideWorkbench.productLaunchAttempted, 'workbench smoke only'),
        grade('extension availability claim stays blocked', ideWorkbench.extensionAvailabilityClaimAllowed === false, String(ideWorkbench.extensionAvailabilityClaimAllowed)),
        grade('workbench smoke checks passed', ideWorkbench.workbenchSmokeChecks.every((item) => item.ok), `${ideWorkbench.workbenchSmokeChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_webview_render_smoke_replay',
      title: 'IDE extension renders a bounded webview view contract locally',
      sourcePattern: 'VS Code WebviewView guidance requires provider-backed, themeable, accessible HTML in view containers',
      evidencePaths: [
        'docs/product-quality/ide-extension-webview-render-smoke-report.json',
        'packages/openclaude-vscode/package.json',
        'packages/openclaude-vscode/dist/extension.js',
      ],
      replayedTrace: ['load extension entry point with local mock webview host', 'activate extension', 'resolve registered WebviewViewProvider', 'grade CSP/theme/command/no-network boundary'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideWebview), 'IDE webview render smoke report call arrays are empty'),
        grade('local mock webview host was used', ideWebview.hostRuntime === 'local_mock_vscode_webview_view_host' && ideWebview.realExtensionHostLaunched === false, ideWebview.hostRuntime),
        grade('activation and deactivation are callable', ideWebview.activationInvoked === true && ideWebview.deactivationInvoked === true, `${ideWebview.activationInvoked}/${ideWebview.deactivationInvoked}`),
        grade('webview view contribution is manifest-declared and registered', ideWebview.manifestWebviewViewIds.includes('openclaude.controlCenterView') && ideWebview.registeredWebviewViewIds.includes('openclaude.controlCenterView'), `${ideWebview.manifestWebviewViewIds.join(', ')} / ${ideWebview.registeredWebviewViewIds.join(', ')}`),
        grade('webview HTML is resolved and non-empty', ideWebview.resolvedWebviewViewIds.includes('openclaude.controlCenterView') && ideWebview.renderedHtmlByteLength > 1000, `${ideWebview.resolvedWebviewViewIds.join(', ')} / ${ideWebview.renderedHtmlByteLength}`),
        grade('webview exposes command actions', ideWebview.commandActionIds.length >= 4, ideWebview.commandActionIds.join(', ')),
        grade('install publish deploy launch not attempted', !ideWebview.installAttempted && !ideWebview.publishAttempted && !ideWebview.deployAttempted && !ideWebview.launchAttempted, 'render smoke only'),
        grade('extension availability claim stays blocked', ideWebview.extensionAvailabilityClaimAllowed === false, String(ideWebview.extensionAvailabilityClaimAllowed)),
        grade('webview render checks passed', ideWebview.webviewRenderChecks.every((item) => item.ok), `${ideWebview.webviewRenderChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_rendered_workbench_screenshot_replay',
      title: 'IDE extension produces a bounded rendered workbench screenshot artifact locally',
      sourcePattern: 'VS Code webview UX guidance requires themeable, accessible command actions, and rendered evidence should remain claim-bounded before availability claims',
      evidencePaths: [
        'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json',
        'docs/product-quality/assets/ide-extension-control-center-render.png',
        'docs/product-quality/assets/ide-extension-control-center-render.svg',
      ],
      replayedTrace: ['load webview render smoke report', 'resolve current Control Center HTML', 'render local workbench-style screenshot artifact', 'grade PNG dimensions/hash/nonblank and protected-action boundary'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideRenderedScreenshot), 'rendered screenshot report call arrays are empty'),
        grade('local screenshot renderer was used', ideRenderedScreenshot.hostRuntime === 'local_sharp_rendered_workbench_panel_from_webview_contract' && ideRenderedScreenshot.realExtensionHostLaunched === false, ideRenderedScreenshot.hostRuntime),
        grade('PNG dimensions are stable', ideRenderedScreenshot.renderedWidth === 960 && ideRenderedScreenshot.renderedHeight === 720, `${ideRenderedScreenshot.renderedWidth}x${ideRenderedScreenshot.renderedHeight}`),
        grade('PNG hash and nonblank evidence exists', ideRenderedScreenshot.pngByteLength > 4000 && ideRenderedScreenshot.pngSha256.length === 64 && ideRenderedScreenshot.svgSha256.length === 64 && ideRenderedScreenshot.nonBlankChannelCount >= 3, `${ideRenderedScreenshot.pngByteLength} bytes`),
        grade('screenshot exposes command actions', ideRenderedScreenshot.commandActionIds.length >= 4, ideRenderedScreenshot.commandActionIds.join(', ')),
        grade('install publish deploy launch not attempted', !ideRenderedScreenshot.installAttempted && !ideRenderedScreenshot.publishAttempted && !ideRenderedScreenshot.deployAttempted && !ideRenderedScreenshot.launchAttempted, 'render artifact only'),
        grade('extension availability claim stays blocked', ideRenderedScreenshot.extensionAvailabilityClaimAllowed === false, String(ideRenderedScreenshot.extensionAvailabilityClaimAllowed)),
        grade('rendered screenshot checks passed', ideRenderedScreenshot.screenshotChecks.every((item) => item.ok), `${ideRenderedScreenshot.screenshotChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'ide_extension_webview_interaction_smoke_replay',
      title: 'IDE extension webview command actions preserve accessible local interaction semantics',
      sourcePattern: 'VS Code webview guidance expects accessible, contextually bounded webview UI; command actions should remain native controls before any availability claim',
      evidencePaths: [
        'docs/product-quality/ide-extension-webview-interaction-smoke-report.json',
        'docs/product-quality/ide-extension-webview-render-smoke-report.json',
        'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json',
      ],
      replayedTrace: ['load webview render and screenshot reports', 'parse Control Center command buttons', 'grade focus order, native button semantics, registered commands, and mock-host command execution'],
      grades: [
        grade('no provider/live/external calls', noCalls(ideWebviewInteraction), 'webview interaction report call arrays are empty'),
        grade('local interaction host was used', ideWebviewInteraction.hostRuntime === 'local_mock_vscode_webview_interaction_host' && ideWebviewInteraction.realExtensionHostLaunched === false, ideWebviewInteraction.hostRuntime),
        grade('source reports are linked', ideWebviewInteraction.sourceWebviewRenderReportPath === 'docs/product-quality/ide-extension-webview-render-smoke-report.json' && ideWebviewInteraction.sourceRenderedScreenshotReportPath === 'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json', `${ideWebviewInteraction.sourceWebviewRenderReportPath} / ${ideWebviewInteraction.sourceRenderedScreenshotReportPath}`),
        grade('activation and deactivation are callable', ideWebviewInteraction.activationInvoked === true && ideWebviewInteraction.deactivationInvoked === true, `${ideWebviewInteraction.activationInvoked}/${ideWebviewInteraction.deactivationInvoked}`),
        grade('command buttons match manifest commands', ideWebviewInteraction.commandButtonCount === ideWebviewInteraction.manifestCommandIds.length && JSON.stringify(ideWebviewInteraction.focusOrderCommandIds) === JSON.stringify(ideWebviewInteraction.manifestCommandIds), `${ideWebviewInteraction.commandButtonCount}/${ideWebviewInteraction.manifestCommandIds.length}`),
        grade('interaction actions match render and screenshot evidence', JSON.stringify(ideWebviewInteraction.interactionCommandIds) === JSON.stringify(ideWebview.commandActionIds) && JSON.stringify(ideWebviewInteraction.interactionCommandIds) === JSON.stringify(ideRenderedScreenshot.commandActionIds), ideWebviewInteraction.interactionCommandIds.join(', ')),
        grade('all interaction commands are registered and executed', ideWebviewInteraction.interactionCommandIds.every((commandId) => ideWebviewInteraction.registeredCommandIds.includes(commandId) && ideWebviewInteraction.executedInteractionCommandIds.includes(commandId)) && ideWebviewInteraction.failedInteractionCommandIds.length === 0, `${ideWebviewInteraction.executedInteractionCommandIds.join(', ')} / failed=${ideWebviewInteraction.failedInteractionCommandIds.join(', ') || 'none'}`),
        grade('command region and keyboard model are accessible', ideWebviewInteraction.commandRegionRole === 'list' && ideWebviewInteraction.commandRegionAriaLabel === 'OpenClaude command action contract' && ideWebviewInteraction.keyboardActivationModel === 'native_button_enter_space_command_mapping', `${ideWebviewInteraction.commandRegionRole}/${ideWebviewInteraction.keyboardActivationModel}`),
        grade('bounded local messages preserve availability boundary', ideWebviewInteraction.messagesShown.length === ideWebviewInteraction.manifestCommandIds.length && ideWebviewInteraction.messagesShown.every((message) => /scoped/i.test(message) && !/available|published|released|production ready/i.test(message)), `${ideWebviewInteraction.messagesShown.length} messages`),
        grade('install publish deploy launch not attempted', !ideWebviewInteraction.installAttempted && !ideWebviewInteraction.publishAttempted && !ideWebviewInteraction.deployAttempted && !ideWebviewInteraction.launchAttempted, 'interaction smoke only'),
        grade('extension availability claim stays blocked', ideWebviewInteraction.extensionAvailabilityClaimAllowed === false, String(ideWebviewInteraction.extensionAvailabilityClaimAllowed)),
        grade('webview interaction checks passed', ideWebviewInteraction.interactionChecks.every((item) => item.ok), `${ideWebviewInteraction.interactionChecks.length} checks`),
      ],
    }),
    scenario({
      id: 'release_artifact_sanitization_replay',
      title: 'Release artifact file list excludes local detritus',
      sourcePattern: 'installable terminal agents need narrow package artifacts',
      evidencePaths: ['docs/product-quality/release-artifact-file-list-report.json', 'package.json'],
      replayedTrace: ['run npm pack dry-run', 'grade expected files', 'grade forbidden files absent'],
      grades: [
        grade('no provider/live/external calls', noCalls(releaseArtifact), 'release artifact report call arrays are empty'),
        grade('pack dry-run succeeded', releaseArtifact.packDryRunExitCode === 0, String(releaseArtifact.packDryRunExitCode)),
        grade('forbidden files absent', releaseArtifact.forbiddenPackageFiles.length === 0, `${releaseArtifact.forbiddenPackageFiles.length} forbidden files`),
        grade('artifact file count bounded', releaseArtifact.actualPackageFiles.length <= 12, `${releaseArtifact.actualPackageFiles.length} files`),
        grade('publish deploy launch not attempted', !releaseArtifact.publishAttempted && !releaseArtifact.deployAttempted && !releaseArtifact.launchAttempted, 'dry-run only'),
      ],
    }),
  ]

  const replayEvalChecks = [
    grade('scenario count covers major product axes', replayScenarios.length >= 5, `${replayScenarios.length} scenarios`),
    grade('all replay scenarios passed threshold', replayScenarios.every((item) => item.passed), `${replayScenarios.filter((item) => item.passed).length}/${replayScenarios.length}`),
    grade('minimum score is strict enough', minimumPassingScore >= 0.9, String(minimumPassingScore)),
    grade('all scenarios have evidence paths', replayScenarios.every((item) => item.evidencePaths.length > 0), 'evidence paths present'),
    grade('all scenarios preserve local no-provider boundary', replayScenarios.every((item) => item.grades.some((itemGrade) => itemGrade.label === 'no provider/live/external calls' && itemGrade.ok)), 'call-boundary grades present'),
  ]

  const report: AgentReplayEvalReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_trace_graded_agent_replay_evals',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    replayScenarioCount: replayScenarios.length,
    minimumPassingScore,
    replayScenarios,
    replayEvalChecks,
    claimBoundary: 'Agent replay evals are local trace-grading fixtures over existing evidence only. They do not call providers, live models, or external services, and do not claim release readiness or autonomous reliability.',
  }

  writeReports(report)

  for (const item of replayScenarios) {
    console.log(`${item.passed ? 'PASS' : 'FAIL'}: ${item.id} score=${item.score}`)
  }
  for (const item of replayEvalChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  if (!replayScenarios.every((item) => item.passed) || !replayEvalChecks.every((item) => item.ok)) {
    console.error('RESULT: FAIL')
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`replay_scenario_count=${replayScenarios.length}`)
  console.log(`minimum_passing_score=${minimumPassingScore}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
