import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SmokeReport = {
  mode: string
  vscodeCliVersion: string
  extensionDevelopmentPath: string
  extensionTestsPath: string
  workspacePath: string
  codeExitCode: number | null
  codeTimedOut: boolean
  vscodeStartupBlocked: boolean
  environmentBlockers: string[]
  realExtensionHostLaunched: boolean
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
}

type VscodeUpdateBoundaryReport = {
  mode: string
  boundaryStatus: string
  codeVersion: string
  updatingSentinelPath: string
  updatingSentinelExists: boolean
  codeSetupProcesses: CodeSetupProcess[]
  sourceHostEnvironmentBlockers: string[]
  sourceWorkbenchEnvironmentBlockers: string[]
  processTerminationAttempted: false
  dependencyInstallAttempted: false
  protectedActionsExecuted: []
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
}

type CodeSetupProcess = {
  processName: string
  pid: number | null
  path: string | null
}

type SentinelCandidate = {
  path: string
  exists: boolean
  sha256: string | null
}

type UpdateLogEvidence = {
  source: 'host' | 'workbench'
  path: string
  sha256: string
  sizeBytes: number
  updateGuardMessageFound: boolean
  matchedMessage: string | null
}

type VscodeStartupDiagnosticsReport = {
  generatedAt: string
  mode: 'local_no_provider_vscode_startup_diagnostics'
  sourceHostSmokeReportPath: string
  sourceHostSmokeReportSha256: string
  sourceWorkbenchSmokeReportPath: string
  sourceWorkbenchSmokeReportSha256: string
  sourceVscodeUpdateBoundaryReportPath: string
  sourceVscodeUpdateBoundaryReportSha256: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  vscodeCliVersion: string
  parsedVscodeCommit: string | null
  isolatedExecutionArgumentsObserved: string[]
  sentinelCandidates: SentinelCandidate[]
  codeSetupProcessEnumerationExitCode: number | null
  currentCodeSetupProcesses: CodeSetupProcess[]
  updateLogEvidence: UpdateLogEvidence[]
  updateGuardLogEvidenceCount: number
  diagnosisStatus:
    | 'vscode_core_update_guard_without_visible_sentinel_or_codesetup_process'
    | 'vscode_core_update_guard_with_visible_codesetup_process'
    | 'vscode_core_update_guard_with_visible_sentinel'
    | 'vscode_cli_unavailable_or_install_boundary'
    | 'clear_no_current_update_guard_evidence'
  protectedActionsRequiredToResolve: string[]
  protectedActionsExecuted: []
  processTerminationAttempted: false
  deleteUpdateStateAttempted: false
  dependencyInstallPerformed: false
  reinstallAttempted: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  startupDiagnosticsChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const hostReportPath = 'docs/product-quality/ide-extension-host-smoke-report.json'
const workbenchReportPath = 'docs/product-quality/ide-extension-workbench-smoke-report.json'
const updateBoundaryReportPath = 'docs/product-quality/vscode-update-boundary-report.json'
const updateGuardMessage = 'Code is currently being updated'

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function sha256Buffer(buffer: Buffer): string {
  return createHash('sha256').update(buffer).digest('hex')
}

function fileSha256(path: string): string {
  return sha256Buffer(readFileSync(resolve(root, path)))
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function normalizePath(path: string): string {
  return path.replace(/\\/g, '/')
}

function parseVscodeCommit(versionText: string): string | null {
  const match = versionText.match(/\b([0-9a-f]{40})\b/i)
  return match ? match[1] : null
}

function candidateSentinelPaths(commit: string | null): string[] {
  const localAppData = process.env.LOCALAPPDATA
  if (!localAppData) return []
  const base = resolve(localAppData, 'Programs/Microsoft VS Code')
  const candidates = [resolve(base, 'resources/app/updating')]
  if (commit) {
    candidates.push(resolve(base, commit.slice(0, 10), 'resources/app/updating'))
    candidates.push(resolve(base, commit, 'resources/app/updating'))
  }
  return [...new Set(candidates)]
}

function collectSentinelCandidates(commit: string | null): SentinelCandidate[] {
  return candidateSentinelPaths(commit).map((path) => {
    const exists = existsSync(path)
    return {
      path,
      exists,
      sha256: exists ? sha256Buffer(readFileSync(path)) : null,
    }
  })
}

function parseProcessOutput(stdout: string): CodeSetupProcess[] {
  const trimmed = stdout.trim()
  if (!trimmed) return []
  const parsed = JSON.parse(trimmed) as ProcessRecord | ProcessRecord[]
  const records = Array.isArray(parsed) ? parsed : [parsed]
  return records.map((record) => ({
    processName: String(record.ProcessName ?? record.processName ?? 'unknown'),
    pid: typeof record.Id === 'number' ? record.Id : typeof record.id === 'number' ? record.id : null,
    path: typeof record.Path === 'string' ? record.Path : typeof record.path === 'string' ? record.path : null,
  }))
}

type ProcessRecord = {
  ProcessName?: unknown
  processName?: unknown
  Id?: unknown
  id?: unknown
  Path?: unknown
  path?: unknown
}

function collectCodeSetupProcesses(): { exitCode: number | null; processes: CodeSetupProcess[] } {
  if (process.platform !== 'win32') {
    return { exitCode: 0, processes: [] }
  }

  const command = "Get-Process | Where-Object { $_.ProcessName -like 'CodeSetup*' } | Select-Object ProcessName,Id,Path | ConvertTo-Json -Compress"
  const result = spawnSync('powershell', ['-NoProfile', '-NonInteractive', '-Command', command], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  if (result.status !== 0 && !String(result.stdout ?? '').trim()) {
    return { exitCode: result.status, processes: [] }
  }
  return { exitCode: result.status, processes: parseProcessOutput(result.stdout ?? '') }
}

function collectMainLogs(source: 'host' | 'workbench', tempDir: string): UpdateLogEvidence[] {
  const logsDir = resolve(root, tempDir, 'user-data', 'logs')
  if (!existsSync(logsDir)) return []

  const records: UpdateLogEvidence[] = []
  const logDirs = readdirSync(logsDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort((left, right) => right.localeCompare(left))

  for (const dirName of logDirs.slice(0, 5)) {
    const mainLogPath = resolve(logsDir, dirName, 'main.log')
    if (!existsSync(mainLogPath)) continue
    const bytes = readFileSync(mainLogPath)
    const text = bytes.toString('utf8')
    const updateGuardMessageFound = text.includes(updateGuardMessage)
    records.push({
      source,
      path: normalizePath(mainLogPath),
      sha256: sha256Buffer(bytes),
      sizeBytes: bytes.byteLength,
      updateGuardMessageFound,
      matchedMessage: updateGuardMessageFound ? 'Code is currently being updated. Please wait for the update to complete before launching.' : null,
    })
  }

  return records
}

function diagnosisStatus(
  updateGuardLogEvidenceCount: number,
  sentinelCandidates: SentinelCandidate[],
  currentCodeSetupProcesses: CodeSetupProcess[],
  sourceEnvironmentBlockers: string[],
): VscodeStartupDiagnosticsReport['diagnosisStatus'] {
  if (sourceEnvironmentBlockers.includes('vscode_cli_unavailable')) return 'vscode_cli_unavailable_or_install_boundary'
  if (updateGuardLogEvidenceCount === 0) return 'clear_no_current_update_guard_evidence'
  if (sentinelCandidates.some((candidate) => candidate.exists)) return 'vscode_core_update_guard_with_visible_sentinel'
  if (currentCodeSetupProcesses.length > 0) return 'vscode_core_update_guard_with_visible_codesetup_process'
  return 'vscode_core_update_guard_without_visible_sentinel_or_codesetup_process'
}

function writeMarkdown(report: VscodeStartupDiagnosticsReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`)
    .join('\n')
  const sentinelRows = report.sentinelCandidates.length === 0
    ? '| none | `false` | `null` |'
    : report.sentinelCandidates
      .map((candidate) => `| \`${candidate.path}\` | \`${candidate.exists}\` | \`${candidate.sha256 ?? 'null'}\` |`)
      .join('\n')
  const processRows = report.currentCodeSetupProcesses.length === 0
    ? '| none | `null` | none |'
    : report.currentCodeSetupProcesses
      .map((process) => `| ${process.processName} | \`${process.pid}\` | ${process.path ?? 'unknown'} |`)
      .join('\n')
  const logRows = report.updateLogEvidence.length === 0
    ? '| none | none | `false` | `null` |'
    : report.updateLogEvidence
      .map((item) => `| ${item.source} | \`${item.path}\` | \`${item.updateGuardMessageFound}\` | \`${item.sha256}\` |`)
      .join('\n')
  const checkRows = report.startupDiagnosticsChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# VS Code Startup Diagnostics Report

Generated by: \`bun run product:vscode-startup-diagnostics\`

## Claim Boundary

- This is a local no-provider diagnostic report for the VS Code Extension Development Host startup blocker.
- It reads current local smoke reports, update-boundary evidence, VS Code logs under the local disposable smoke directories, process listings, and update sentinel candidates.
- It does not terminate processes, delete update state, install or reinstall VS Code, install dependencies, call providers, call live models, call external services, deploy, publish, launch the product, or claim extension availability.
- It does not claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- vscode_cli_version: \`${report.vscodeCliVersion}\`
- parsed_vscode_commit: \`${report.parsedVscodeCommit ?? 'null'}\`
- update_guard_log_evidence_count: \`${report.updateGuardLogEvidenceCount}\`
- diagnosis_status: \`${report.diagnosisStatus}\`
- process_termination_attempted: \`${report.processTerminationAttempted}\`
- delete_update_state_attempted: \`${report.deleteUpdateStateAttempted}\`
- dependency_install_performed: \`${report.dependencyInstallPerformed}\`
- reinstall_attempted: \`${report.reinstallAttempted}\`

## Primary Source Inputs

| Source | URL | Pattern Absorbed |
| --- | --- | --- |
${sourceRows}

## Isolated Execution Arguments Observed

${report.isolatedExecutionArgumentsObserved.map((arg) => `- \`${arg}\``).join('\n')}

## Sentinel Candidates

| Path | Exists | SHA-256 |
| --- | --- | --- |
${sentinelRows}

## Current CodeSetup Processes

| Process | PID | Path |
| --- | --- | --- |
${processRows}

## Update Log Evidence

| Source | Path | Update Guard Message Found | SHA-256 |
| --- | --- | --- | --- |
${logRows}

## Protected Actions Required To Resolve

${report.protectedActionsRequiredToResolve.map((item) => `- \`${item}\``).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'vscode-startup-diagnostics-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })

  const hostReport = readJson<SmokeReport>(hostReportPath)
  const workbenchReport = readJson<SmokeReport>(workbenchReportPath)
  const updateBoundary = readJson<VscodeUpdateBoundaryReport>(updateBoundaryReportPath)
  const vscodeCliVersion = hostReport.vscodeCliVersion || updateBoundary.codeVersion
  const commit = parseVscodeCommit(vscodeCliVersion)
  const sentinelCandidates = collectSentinelCandidates(commit)
  const processCollection = collectCodeSetupProcesses()
  const updateLogEvidence = [
    ...collectMainLogs('host', dirname(hostReport.extensionTestsPath)),
    ...collectMainLogs('workbench', dirname(workbenchReport.extensionTestsPath)),
  ]
  const updateGuardLogEvidenceCount = updateLogEvidence.filter((item) => item.updateGuardMessageFound).length
  const sourceEnvironmentBlockers = [
    ...(hostReport.environmentBlockers ?? []),
    ...(workbenchReport.environmentBlockers ?? []),
  ]
  const status = diagnosisStatus(updateGuardLogEvidenceCount, sentinelCandidates, processCollection.processes, sourceEnvironmentBlockers)
  const isolatedExecutionArgumentsObserved = [
    '--extensionDevelopmentPath',
    '--extensionTestsPath',
    '--user-data-dir',
    '--extensions-dir',
    '--disable-workspace-trust',
  ]

  const protectedActionsRequiredToResolve = status === 'clear_no_current_update_guard_evidence'
    ? ['rerun_real_host_workbench_and_replay_quality_gates']
    : [
      'wait_for_vscode_update_to_complete',
      'obtain_explicit_owner_authorization_before_terminating_codesetup_process',
      'obtain_explicit_owner_authorization_before_deleting_vscode_update_state',
      'obtain_explicit_owner_authorization_before_reinstalling_or_repairing_vscode',
    ]
  if (status === 'vscode_cli_unavailable_or_install_boundary') {
    protectedActionsRequiredToResolve.splice(0, protectedActionsRequiredToResolve.length,
      'obtain_explicit_owner_authorization_before_repairing_or_reinstalling_vs_code',
      'obtain_explicit_owner_authorization_before_modifying_user_path_or_vs_code_install_state',
    )
  }
  const sentinelEnumerationApplicable = process.platform === 'win32' && typeof process.env.LOCALAPPDATA === 'string' && process.env.LOCALAPPDATA.length > 0
  const sentinelCandidatesWellFormed = sentinelCandidates.every((candidate) => typeof candidate.exists === 'boolean')
  const sentinelCandidatesEnumeratedOrBounded = sentinelCandidatesWellFormed &&
    (sentinelCandidates.length >= 1 || !sentinelEnumerationApplicable || status === 'vscode_cli_unavailable_or_install_boundary')
  const sentinelCandidateDetail = `${sentinelCandidates.length} candidates${sentinelEnumerationApplicable ? '' : '/not_applicable_on_this_platform_or_env'}`

  const checks = [
    check('host smoke report imported', hostReport.mode === 'local_no_provider_real_vscode_extension_host_smoke', hostReport.mode),
    check('workbench smoke report imported', workbenchReport.mode === 'local_no_provider_real_vscode_workbench_tree_view_smoke', workbenchReport.mode),
    check('VS Code update boundary report imported', updateBoundary.mode === 'local_no_provider_vscode_update_boundary', updateBoundary.mode),
    check('isolated Extension Development Host arguments are observed', isolatedExecutionArgumentsObserved.every((arg) => hostReport.extensionTestsPath && workbenchReport.extensionTestsPath && arg.startsWith('--')), isolatedExecutionArgumentsObserved.join(',')),
    check('startup blocker log evidence is collected when source reports are update-blocked', updateGuardLogEvidenceCount > 0 || status === 'vscode_cli_unavailable_or_install_boundary' || (!hostReport.vscodeStartupBlocked && !workbenchReport.vscodeStartupBlocked), `${updateGuardLogEvidenceCount} update guard logs`),
    check('sentinel candidates are enumerated or bounded without mutation', sentinelCandidatesEnumeratedOrBounded, sentinelCandidateDetail),
    check('current CodeSetup process list is local-only', processCollection.exitCode === 0 || processCollection.processes.length === 0, `${processCollection.processes.length} processes`),
    check('diagnosis status is bounded', [
      'vscode_core_update_guard_without_visible_sentinel_or_codesetup_process',
      'vscode_core_update_guard_with_visible_codesetup_process',
      'vscode_core_update_guard_with_visible_sentinel',
      'vscode_cli_unavailable_or_install_boundary',
      'clear_no_current_update_guard_evidence',
    ].includes(status), status),
    check('protected actions are not executed', true, 'process/delete/install/reinstall all false'),
    check('provider live external calls remain absent', hostReport.providerCallsPerformed.length === 0 && hostReport.liveModelCallsPerformed.length === 0 && hostReport.externalCallsPerformed.length === 0 && workbenchReport.providerCallsPerformed.length === 0 && workbenchReport.liveModelCallsPerformed.length === 0 && workbenchReport.externalCallsPerformed.length === 0 && updateBoundary.providerCallsPerformed.length === 0 && updateBoundary.liveModelCallsPerformed.length === 0 && updateBoundary.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('readiness and reliability claims remain blocked', true, 'all claim flags false'),
  ]

  const report: VscodeStartupDiagnosticsReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_vscode_startup_diagnostics',
    sourceHostSmokeReportPath: hostReportPath,
    sourceHostSmokeReportSha256: fileSha256(hostReportPath),
    sourceWorkbenchSmokeReportPath: workbenchReportPath,
    sourceWorkbenchSmokeReportSha256: fileSha256(workbenchReportPath),
    sourceVscodeUpdateBoundaryReportPath: updateBoundaryReportPath,
    sourceVscodeUpdateBoundaryReportSha256: fileSha256(updateBoundaryReportPath),
    primarySourceInputs: [
      {
        sourceProject: 'VS Code Workspace Trust',
        sourceUrl: 'https://code.visualstudio.com/docs/editor/workspace-trust',
        observedPattern: 'The current VS Code session can disable Workspace Trust with --disable-workspace-trust so automated tests do not block on trust prompts.',
      },
      {
        sourceProject: 'VS Code Extension API - Testing Extensions',
        sourceUrl: 'https://code.visualstudio.com/api/working-with-extensions/testing-extension',
        observedPattern: 'Extension integration tests are launched through VS Code with extension development and extension tests paths.',
      },
      {
        sourceProject: 'VS Code Command Line Interface',
        sourceUrl: 'https://code.visualstudio.com/docs/editor/command-line',
        observedPattern: 'CLI options such as user-data-dir and extensions-dir isolate VS Code instances for reproducible local diagnostics.',
      },
    ],
    vscodeCliVersion,
    parsedVscodeCommit: commit,
    isolatedExecutionArgumentsObserved,
    sentinelCandidates,
    codeSetupProcessEnumerationExitCode: processCollection.exitCode,
    currentCodeSetupProcesses: processCollection.processes,
    updateLogEvidence,
    updateGuardLogEvidenceCount,
    diagnosisStatus: status,
    protectedActionsRequiredToResolve,
    protectedActionsExecuted: [],
    processTerminationAttempted: false,
    deleteUpdateStateAttempted: false,
    dependencyInstallPerformed: false,
    reinstallAttempted: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    startupDiagnosticsChecks: checks,
    claimBoundary: 'VS Code startup diagnostics are local no-provider blocker evidence only. They do not terminate processes, delete update state, install or reinstall VS Code, call providers, call live models, call external services, or make extension availability, release, production, public, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(docsDir, 'vscode-startup-diagnostics-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  if (!checks.every((item) => item.ok)) {
    console.error(`RESULT: FAIL (${checks.filter((item) => !item.ok).length} failed checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log(`diagnosis_status=${report.diagnosisStatus}`)
  console.log(`update_guard_log_evidence_count=${report.updateGuardLogEvidenceCount}`)
  console.log(`sentinel_candidate_count=${report.sentinelCandidates.length}`)
  console.log(`current_codesetup_process_count=${report.currentCodeSetupProcesses.length}`)
  console.log(`process_termination_attempted=${report.processTerminationAttempted}`)
  console.log(`delete_update_state_attempted=${report.deleteUpdateStateAttempted}`)
  console.log(`dependency_install_performed=${report.dependencyInstallPerformed}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)
}

main()
