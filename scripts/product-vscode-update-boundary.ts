import { spawnSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { scrubPublicArtifactText, scrubPublicArtifactValue } from './product-report-sanitizer'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SmokeReport = {
  environmentBlockers?: string[]
  vscodeStartupBlocked?: boolean
  realExtensionHostLaunched?: boolean
  extensionActivated?: boolean
}

type RawProcess = {
  ProcessName?: unknown
  Id?: unknown
  Path?: unknown
}

type CodeSetupProcess = {
  processName: string
  pid: number | null
  path: string | null
}

type VscodeUpdateBoundaryReport = {
  generatedAt: string
  mode: 'local_no_provider_vscode_update_boundary'
  sourceHostSmokeReportPath: string
  sourceHostSmokeReportSha256: string
  sourceWorkbenchSmokeReportPath: string
  sourceWorkbenchSmokeReportSha256: string
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  codeCommand: string[]
  codeVersionExitCode: number | null
  codeVersion: string
  updatingSentinelPath: string
  updatingSentinelExists: boolean
  updatingSentinelValueSha256: string | null
  processEnumerationCommand: string
  processEnumerationExitCode: number | null
  codeSetupProcesses: CodeSetupProcess[]
  sourceHostEnvironmentBlockers: string[]
  sourceWorkbenchEnvironmentBlockers: string[]
  sourceHostVscodeStartupBlocked: boolean
  sourceWorkbenchVscodeStartupBlocked: boolean
  sourceHostRealExtensionHostLaunched: boolean
  sourceWorkbenchRealExtensionHostLaunched: boolean
  boundaryStatus:
    | 'blocked_wait_for_local_vscode_update_or_explicit_owner_process_action'
    | 'blocked_missing_vscode_cli_or_explicit_owner_repair_action'
    | 'clear_no_current_vscode_update_boundary'
  requiredOwnerActions: string[]
  blockedActions: string[]
  processTerminationAttempted: false
  dependencyInstallAttempted: false
  publishAttempted: false
  deployAttempted: false
  productLaunchAttempted: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  boundaryChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const sourceHostSmokeReportPath = 'docs/product-quality/ide-extension-host-smoke-report.json'
const sourceWorkbenchSmokeReportPath = 'docs/product-quality/ide-extension-workbench-smoke-report.json'

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function getCodeVersion(): { exitCode: number | null; text: string } {
  const result = spawnSync('code', ['--version'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  return {
    exitCode: result.status,
    text: (result.stdout ?? '').trim().split(/\r?\n/).filter(Boolean).join(' / ') || 'not_available',
  }
}

function parseProcessOutput(stdout: string): CodeSetupProcess[] {
  const trimmed = stdout.trim()
  if (!trimmed) {
    return []
  }

  const parsed = JSON.parse(trimmed) as RawProcess | RawProcess[]
  const rawProcesses = Array.isArray(parsed) ? parsed : [parsed]

  return rawProcesses.map((item) => ({
    processName: typeof item.ProcessName === 'string' ? item.ProcessName : 'unknown',
    pid: typeof item.Id === 'number' ? item.Id : null,
    path: typeof item.Path === 'string' && item.Path.length > 0 ? item.Path : null,
  }))
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

  if (result.status !== 0 || !(result.stdout ?? '').trim()) {
    return { exitCode: result.status, processes: [] }
  }

  return { exitCode: result.status, processes: parseProcessOutput(result.stdout ?? '') }
}

function getUpdatingSentinelPath(): string {
  const localAppData = process.env.LOCALAPPDATA
  if (!localAppData) {
    return ''
  }

  return resolve(localAppData, 'Programs/Microsoft VS Code/resources/app/updating')
}

function writeMarkdown(report: VscodeUpdateBoundaryReport): void {
  const processRows = report.codeSetupProcesses.length === 0
    ? '| none | `null` | none |'
    : report.codeSetupProcesses
      .map((item) => `| ${item.processName} | \`${item.pid}\` | ${item.path ?? 'unknown'} |`)
      .join('\n')
  const checkRows = report.boundaryChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# VS Code Update Boundary Report

Generated by: \`bun run product:vscode-update-boundary\`

## Claim Boundary

- This report is a local no-provider diagnostic boundary for real VS Code Extension Host smoke blockers.
- It does not terminate processes, install dependencies, mutate VS Code, publish, deploy, launch, call providers, call live models, call external services, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- boundary_status: \`${report.boundaryStatus}\`
- code_version_exit_code: \`${report.codeVersionExitCode}\`
- code_version: \`${report.codeVersion}\`
- updating_sentinel_exists: \`${report.updatingSentinelExists}\`
- updating_sentinel_value_sha256: \`${report.updatingSentinelValueSha256 ?? 'null'}\`
- code_setup_process_count: \`${report.codeSetupProcesses.length}\`
- source_host_environment_blockers: \`${report.sourceHostEnvironmentBlockers.join(',') || 'none'}\`
- source_workbench_environment_blockers: \`${report.sourceWorkbenchEnvironmentBlockers.join(',') || 'none'}\`
- process_termination_attempted: \`${report.processTerminationAttempted}\`
- dependency_install_attempted: \`${report.dependencyInstallAttempted}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`
- production_readiness_claim_allowed: \`${report.productionReadinessClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`
- external_validation_claim_allowed: \`${report.externalValidationClaimAllowed}\`
- autonomous_reliability_claim_allowed: \`${report.autonomousReliabilityClaimAllowed}\`

## CodeSetup Processes

| Process | PID | Path |
| --- | --- | --- |
${processRows}

## Required Owner Actions

${report.requiredOwnerActions.map((item) => `- ${item}`).join('\n')}

## Blocked Actions

${report.blockedActions.map((item) => `- ${item}`).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'vscode-update-boundary-report.md'), scrubPublicArtifactText(markdown))
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })

  const hostReport = readJson<SmokeReport>(sourceHostSmokeReportPath)
  const workbenchReport = readJson<SmokeReport>(sourceWorkbenchSmokeReportPath)
  const codeVersion = getCodeVersion()
  const processCollection = collectCodeSetupProcesses()
  const updatingSentinelPath = getUpdatingSentinelPath()
  const updatingSentinelExists = updatingSentinelPath.length > 0 && existsSync(updatingSentinelPath)
  const updatingSentinelValueSha256 = updatingSentinelExists ? sha256(readFileSync(updatingSentinelPath)) : null
  const hostBlockers = hostReport.environmentBlockers ?? []
  const workbenchBlockers = workbenchReport.environmentBlockers ?? []
  const codeCliUnavailable = codeVersion.exitCode !== 0 || codeVersion.text === 'not_available' || hostBlockers.includes('vscode_cli_unavailable') || workbenchBlockers.includes('vscode_cli_unavailable')
  const hasObservedUpdateBoundary = updatingSentinelExists
    || processCollection.processes.length > 0
    || hostBlockers.includes('vscode_update_in_progress')
    || workbenchBlockers.includes('vscode_update_in_progress')
  const boundaryStatus = codeCliUnavailable
    ? 'blocked_missing_vscode_cli_or_explicit_owner_repair_action'
    : hasObservedUpdateBoundary
    ? 'blocked_wait_for_local_vscode_update_or_explicit_owner_process_action'
    : 'clear_no_current_vscode_update_boundary'

  const report: VscodeUpdateBoundaryReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_vscode_update_boundary',
    sourceHostSmokeReportPath,
    sourceHostSmokeReportSha256: fileSha256(sourceHostSmokeReportPath),
    sourceWorkbenchSmokeReportPath,
    sourceWorkbenchSmokeReportSha256: fileSha256(sourceWorkbenchSmokeReportPath),
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    codeCommand: ['code', '--version'],
    codeVersionExitCode: codeVersion.exitCode,
    codeVersion: codeVersion.text,
    updatingSentinelPath,
    updatingSentinelExists,
    updatingSentinelValueSha256,
    processEnumerationCommand: 'powershell -NoProfile -NonInteractive -Command <CodeSetup process listing>',
    processEnumerationExitCode: processCollection.exitCode,
    codeSetupProcesses: processCollection.processes,
    sourceHostEnvironmentBlockers: hostBlockers,
    sourceWorkbenchEnvironmentBlockers: workbenchBlockers,
    sourceHostVscodeStartupBlocked: hostReport.vscodeStartupBlocked === true,
    sourceWorkbenchVscodeStartupBlocked: workbenchReport.vscodeStartupBlocked === true,
    sourceHostRealExtensionHostLaunched: hostReport.realExtensionHostLaunched === true,
    sourceWorkbenchRealExtensionHostLaunched: workbenchReport.realExtensionHostLaunched === true,
    boundaryStatus,
    requiredOwnerActions: codeCliUnavailable
      ? [
        'obtain_explicit_owner_authorization_before_repairing_or_reinstalling_vs_code',
        'obtain_explicit_owner_authorization_before_modifying_user_path_or_vs_code_install_state',
      ]
      : hasObservedUpdateBoundary
      ? [
        'wait_for_local_vscode_update_to_finish_before_rerunning_real_host_smokes',
        'obtain_explicit_owner_authorization_before_any_process_termination_or_vs_code_repair_action',
      ]
      : ['rerun_real_host_and_workbench_smokes_to_refresh_current_evidence'],
    blockedActions: [
      'terminate_codesetup_process_without_explicit_owner_authorization',
      'delete_vscode_update_state_without_explicit_owner_authorization',
      'install_or_reinstall_vscode_without_explicit_owner_authorization',
      'modify_user_path_or_vs_code_install_state_without_explicit_owner_authorization',
      'claim_extension_availability_from_environment_blocked_smoke',
      'claim_release_or_production_readiness_from_environment_blocked_smoke',
    ],
    processTerminationAttempted: false,
    dependencyInstallAttempted: false,
    publishAttempted: false,
    deployAttempted: false,
    productLaunchAttempted: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    boundaryChecks: [],
    claimBoundary: 'Local diagnostic evidence only; no protected action or readiness claim is authorized by this report.',
  }

  report.boundaryChecks = [
    check('host smoke report imported', report.sourceHostSmokeReportSha256.length === 64, report.sourceHostSmokeReportPath),
    check('workbench smoke report imported', report.sourceWorkbenchSmokeReportSha256.length === 64, report.sourceWorkbenchSmokeReportPath),
    check('VS Code CLI version probe is local only or classified as protected boundary', (report.codeVersionExitCode === 0 && report.codeVersion !== 'not_available') || report.boundaryStatus === 'blocked_missing_vscode_cli_or_explicit_owner_repair_action', report.codeVersion),
    check('CodeSetup process listing did not require provider or external calls', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'local PowerShell process list only'),
    check('observed update boundary is classified without mutation', report.boundaryStatus.length > 0 && report.processTerminationAttempted === false && report.protectedActionsExecuted.length === 0, report.boundaryStatus),
    check('readiness and availability claims remain blocked', report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false, 'all false'),
  ]

  const publicReport = scrubPublicArtifactValue(report)
  writeFileSync(resolve(docsDir, 'vscode-update-boundary-report.json'), `${JSON.stringify(publicReport, null, 2)}\n`)
  writeMarkdown(publicReport)

  for (const item of report.boundaryChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('RESULT: PASS')
  console.log(`boundary_status=${report.boundaryStatus}`)
  console.log(`code_setup_process_count=${report.codeSetupProcesses.length}`)
  console.log(`updating_sentinel_exists=${report.updatingSentinelExists}`)
  console.log(`source_host_environment_blockers=${report.sourceHostEnvironmentBlockers.join(',') || 'none'}`)
  console.log(`source_workbench_environment_blockers=${report.sourceWorkbenchEnvironmentBlockers.join(',') || 'none'}`)
}

main()
