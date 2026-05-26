import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SmokeCheck = {
  label: string
  ok: boolean
  detail?: string
}

type HostSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
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
  hostSmokeChecks: SmokeCheck[]
}

type WorkbenchSmokeReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  registeredTreeViewIds: string[]
  treeProviderViewIds: string[]
  focusedViewIds: string[]
  viewItemCounts: Record<string, number>
  executedViewCommandIds?: string[]
  failedViewCommandIds?: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  productLaunchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  workbenchSmokeChecks: SmokeCheck[]
}

type AgentReplayReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  replayScenarioCount: number
  replayScenarios: Array<{
    id: string
    passed: boolean
  }>
  replayEvalChecks: SmokeCheck[]
}

type VscodeUpdateBoundaryReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  boundaryStatus: string
  sourceHostEnvironmentBlockers: string[]
  sourceWorkbenchEnvironmentBlockers: string[]
  codeSetupProcesses: Array<{
    processName: string
    pid: number | null
    path: string | null
  }>
  processTerminationAttempted: boolean
  dependencyInstallAttempted: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  boundaryChecks: SmokeCheck[]
}

type KnownFailureGroup = {
  id: string
  expectedFailureCount: number
  source: string
  blockingReason: string
  protectedActionRequired: boolean
  evidence: string[]
}

type QualityBlockerTaxonomyReport = {
  generatedAt: string
  mode: 'local_no_provider_quality_blocker_taxonomy'
  sourceHostSmokeReportPath: string
  sourceHostSmokeReportSha256: string
  sourceWorkbenchSmokeReportPath: string
  sourceWorkbenchSmokeReportSha256: string
  sourceAgentReplayReportPath: string
  sourceAgentReplayReportSha256: string
  sourceVscodeUpdateBoundaryReportPath: string
  sourceVscodeUpdateBoundaryReportSha256: string
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  currentProductQualityGateStatus:
    | 'blocked_by_known_vscode_update_dependent_failures'
    | 'blocked_by_vscode_cli_unavailable'
    | 'clear_no_current_vscode_update_dependent_failures'
  blockerStatus:
    | 'classified_known_environment_boundary'
    | 'classified_protected_local_vscode_install_boundary'
    | 'resolved_environment_boundary'
  expectedProductQualityGateFailureCount: number
  knownFailureGroups: KnownFailureGroup[]
  unexpectedFailureGroups: string[]
  nextUnblockedAction: string
  processTerminationAttempted: false
  dependencyInstallAttempted: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  taxonomyChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const sourceHostSmokeReportPath = 'docs/product-quality/ide-extension-host-smoke-report.json'
const sourceWorkbenchSmokeReportPath = 'docs/product-quality/ide-extension-workbench-smoke-report.json'
const sourceAgentReplayReportPath = 'docs/product-quality/agent-replay-evals-report.json'
const sourceVscodeUpdateBoundaryReportPath = 'docs/product-quality/vscode-update-boundary-report.json'

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function failedCheckLabels(checks: SmokeCheck[]): string[] {
  return checks.filter((item) => !item.ok).map((item) => item.label)
}

function writeMarkdown(report: QualityBlockerTaxonomyReport): void {
  const groups = report.knownFailureGroups
    .map((group) => `| ${group.id} | \`${group.expectedFailureCount}\` | ${group.source} | ${group.blockingReason} | \`${group.protectedActionRequired}\` |`)
    .join('\n')
  const checks = report.taxonomyChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Quality Blocker Taxonomy Report

Generated by: \`bun run product:quality-blocker-taxonomy\`

## Claim Boundary

- This is a local no-provider classification of the current product-quality failure envelope.
- It does not terminate VS Code updater processes, install dependencies, call providers, call live models, call external services, publish, deploy, launch, or claim extension availability, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- current_product_quality_gate_status: \`${report.currentProductQualityGateStatus}\`
- blocker_status: \`${report.blockerStatus}\`
- expected_product_quality_gate_failure_count: \`${report.expectedProductQualityGateFailureCount}\`
- unexpected_failure_group_count: \`${report.unexpectedFailureGroups.length}\`
- next_unblocked_action: \`${report.nextUnblockedAction}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- process_termination_attempted: \`${report.processTerminationAttempted}\`
- dependency_install_attempted: \`${report.dependencyInstallAttempted}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`
- production_readiness_claim_allowed: \`${report.productionReadinessClaimAllowed}\`
- public_readiness_claim_allowed: \`${report.publicReadinessClaimAllowed}\`
- external_validation_claim_allowed: \`${report.externalValidationClaimAllowed}\`
- autonomous_reliability_claim_allowed: \`${report.autonomousReliabilityClaimAllowed}\`

## Known Failure Groups

| Group | Expected failed checks | Source | Blocking reason | Protected action required |
| --- | ---: | --- | --- | --- |
${groups}

## Unexpected Failure Groups

${report.unexpectedFailureGroups.length === 0 ? '- none' : report.unexpectedFailureGroups.map((item) => `- ${item}`).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checks}
`

  writeFileSync(resolve(docsDir, 'quality-blocker-taxonomy-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })

  const host = readJson<HostSmokeReport>(sourceHostSmokeReportPath)
  const workbench = readJson<WorkbenchSmokeReport>(sourceWorkbenchSmokeReportPath)
  const replay = readJson<AgentReplayReport>(sourceAgentReplayReportPath)
  const boundary = readJson<VscodeUpdateBoundaryReport>(sourceVscodeUpdateBoundaryReportPath)
  const hostFailedLabels = failedCheckLabels(host.hostSmokeChecks)
  const workbenchFailedLabels = failedCheckLabels(workbench.workbenchSmokeChecks)
  const replayFailedScenarioIds = replay.replayScenarios.filter((item) => !item.passed).map((item) => item.id)
  const replayFailedCheckLabels = failedCheckLabels(replay.replayEvalChecks)
  const hostBlocked = host.vscodeStartupBlocked === true && (host.environmentBlockers ?? []).includes('vscode_update_in_progress')
  const workbenchBlocked = workbench.vscodeStartupBlocked === true && (workbench.environmentBlockers ?? []).includes('vscode_update_in_progress')
  const hostCliUnavailable = (host.environmentBlockers ?? []).includes('vscode_cli_unavailable')
  const workbenchCliUnavailable = (workbench.environmentBlockers ?? []).includes('vscode_cli_unavailable')
  const boundaryBlocked = boundary.boundaryStatus === 'blocked_wait_for_local_vscode_update_or_explicit_owner_process_action'
  const boundaryCliUnavailable = boundary.boundaryStatus === 'blocked_missing_vscode_cli_or_explicit_owner_repair_action'
  const boundaryClear = boundary.boundaryStatus === 'clear_no_current_vscode_update_boundary'
  const hostClear = !hostBlocked && hostFailedLabels.length === 0 && host.realExtensionHostLaunched && host.extensionActivated && host.failedCommandIds.length === 0
  const workbenchClear = !workbenchBlocked && workbenchFailedLabels.length === 0 && workbench.realExtensionHostLaunched && workbench.extensionActivated && (workbench.failedViewCommandIds ?? []).length === 0
  const replayClear = replayFailedScenarioIds.length === 0 && replayFailedCheckLabels.length === 0
  const updateDependentFailuresClear = hostClear && workbenchClear && replayClear && boundaryClear
  const vscodeCliUnavailableBlocked = boundaryCliUnavailable && (hostCliUnavailable || workbenchCliUnavailable)

  const blockedFailureGroups: KnownFailureGroup[] = [
    {
      id: 'ide_extension_host_smoke_vscode_update_blocked',
      expectedFailureCount: 6,
      source: sourceHostSmokeReportPath,
      blockingReason: 'vscode_update_in_progress prevented a current real Extension Development Host result file, activation, command registration, and command execution evidence.',
      protectedActionRequired: true,
      evidence: hostFailedLabels,
    },
    {
      id: 'ide_extension_workbench_smoke_vscode_update_blocked',
      expectedFailureCount: 9,
      source: sourceWorkbenchSmokeReportPath,
      blockingReason: 'vscode_update_in_progress prevented a current real workbench result file, activation, tree-view provider, focus, item, and TreeItem command execution evidence.',
      protectedActionRequired: true,
      evidence: workbenchFailedLabels,
    },
    {
      id: 'agent_replay_vscode_update_dependent_failures',
      expectedFailureCount: 4,
      source: sourceAgentReplayReportPath,
      blockingReason: 'The replay gate correctly fails the host and workbench replay scenarios while their source evidence remains blocked by the local VS Code update boundary.',
      protectedActionRequired: false,
      evidence: [...replayFailedScenarioIds, ...replayFailedCheckLabels],
    },
  ]
  const cliUnavailableFailureGroups: KnownFailureGroup[] = [
    {
      id: 'ide_extension_smoke_vscode_cli_unavailable',
      expectedFailureCount: hostFailedLabels.length + workbenchFailedLabels.length,
      source: sourceHostSmokeReportPath,
      blockingReason: 'The local VS Code CLI is unavailable, so real Extension Development Host evidence requires explicit owner authorization for VS Code/PATH/install-state repair before rerunning the full gate.',
      protectedActionRequired: true,
      evidence: [...hostFailedLabels, ...workbenchFailedLabels],
    },
  ]
  const knownFailureGroups = updateDependentFailuresClear ? [] : vscodeCliUnavailableBlocked ? cliUnavailableFailureGroups : blockedFailureGroups

  const unexpectedFailureGroups: string[] = []
  if (!hostBlocked && !hostClear && !hostCliUnavailable) {
    unexpectedFailureGroups.push('host_smoke_failure_not_explained_by_vscode_update')
  }
  if (!workbenchBlocked && !workbenchClear && !workbenchCliUnavailable) {
    unexpectedFailureGroups.push('workbench_smoke_failure_not_explained_by_vscode_update')
  }
  if (!boundaryBlocked && !boundaryClear && !boundaryCliUnavailable) {
    unexpectedFailureGroups.push('vscode_update_boundary_not_blocked')
  }
  if (replayFailedScenarioIds.some((id) => !['ide_extension_host_smoke_replay', 'ide_extension_workbench_smoke_replay'].includes(id))) {
    unexpectedFailureGroups.push('agent_replay_failure_outside_host_workbench')
  } else if (!replayClear && !(replayFailedScenarioIds.join(',') === 'ide_extension_host_smoke_replay,ide_extension_workbench_smoke_replay' && replayFailedCheckLabels.join(',') === 'all replay scenarios passed threshold')) {
    unexpectedFailureGroups.push('agent_replay_failure_not_explained_by_host_workbench')
  }

  const report: QualityBlockerTaxonomyReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_quality_blocker_taxonomy',
    sourceHostSmokeReportPath,
    sourceHostSmokeReportSha256: fileSha256(sourceHostSmokeReportPath),
    sourceWorkbenchSmokeReportPath,
    sourceWorkbenchSmokeReportSha256: fileSha256(sourceWorkbenchSmokeReportPath),
    sourceAgentReplayReportPath,
    sourceAgentReplayReportSha256: fileSha256(sourceAgentReplayReportPath),
    sourceVscodeUpdateBoundaryReportPath,
    sourceVscodeUpdateBoundaryReportSha256: fileSha256(sourceVscodeUpdateBoundaryReportPath),
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    currentProductQualityGateStatus: vscodeCliUnavailableBlocked
      ? 'blocked_by_vscode_cli_unavailable'
      : updateDependentFailuresClear
      ? 'clear_no_current_vscode_update_dependent_failures'
      : 'blocked_by_known_vscode_update_dependent_failures',
    blockerStatus: vscodeCliUnavailableBlocked
      ? 'classified_protected_local_vscode_install_boundary'
      : updateDependentFailuresClear
      ? 'resolved_environment_boundary'
      : 'classified_known_environment_boundary',
    expectedProductQualityGateFailureCount: knownFailureGroups.reduce((sum, group) => sum + group.expectedFailureCount, 0),
    knownFailureGroups,
    unexpectedFailureGroups,
    nextUnblockedAction: vscodeCliUnavailableBlocked
      ? 'obtain_explicit_owner_authorization_before_repairing_vs_code_cli_path_or_install_state_then_rerun_real_host_workbench_replay_quality_gates'
      : updateDependentFailuresClear
      ? 'rerun_full_product_quality_gate_and_keep_release_readiness_claims_blocked_until_remaining_protected_boundaries_are_authorized'
      : 'wait_for_local_vscode_update_or_obtain_explicit_owner_authorization_before_process_intervention_then_rerun_real_host_workbench_replay_quality_gates',
    processTerminationAttempted: false,
    dependencyInstallAttempted: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    taxonomyChecks: [],
    claimBoundary: 'Known blocker taxonomy only; no protected action, external validation, release readiness, production readiness, public readiness, or autonomous reliability claim is authorized.',
  }

  report.taxonomyChecks = [
    check('host smoke report imported', report.sourceHostSmokeReportSha256.length === 64, report.sourceHostSmokeReportPath),
    check('workbench smoke report imported', report.sourceWorkbenchSmokeReportSha256.length === 64, report.sourceWorkbenchSmokeReportPath),
    check('agent replay report imported', report.sourceAgentReplayReportSha256.length === 64, report.sourceAgentReplayReportPath),
    check('VS Code update boundary imported', report.sourceVscodeUpdateBoundaryReportSha256.length === 64, report.sourceVscodeUpdateBoundaryReportPath),
    check('all source reports remain local no-provider', [host, workbench, replay, boundary].every((item) => item.providerCallsPerformed.length === 0 && item.liveModelCallsPerformed.length === 0 && item.externalCallsPerformed.length === 0), 'all call arrays empty'),
    check('host smoke is either clear or explained by VS Code boundary', hostClear || hostCliUnavailable || (hostBlocked && hostFailedLabels.length === 5), `${host.environmentBlockers?.join(',') ?? 'none'} / ${hostFailedLabels.length} source checks`),
    check('workbench smoke is either clear or explained by VS Code boundary', workbenchClear || workbenchCliUnavailable || (workbenchBlocked && workbenchFailedLabels.length === 9), `${workbench.environmentBlockers?.join(',') ?? 'none'} / ${workbenchFailedLabels.length} source checks`),
    check('agent replay is either clear or host/workbench dependent', replayClear || (replayFailedScenarioIds.join(',') === 'ide_extension_host_smoke_replay,ide_extension_workbench_smoke_replay' && replayFailedCheckLabels.join(',') === 'all replay scenarios passed threshold'), `${replayFailedScenarioIds.join(',')} / ${replayFailedCheckLabels.join(',')}`),
    check('expected quality-gate failure envelope matches current blocker status', report.expectedProductQualityGateFailureCount === (vscodeCliUnavailableBlocked ? hostFailedLabels.length + workbenchFailedLabels.length : updateDependentFailuresClear ? 0 : 19), String(report.expectedProductQualityGateFailureCount)),
    check('unexpected failure groups are absent', report.unexpectedFailureGroups.length === 0, report.unexpectedFailureGroups.join(',') || 'none'),
    check('protected process and dependency actions were not attempted', report.processTerminationAttempted === false && report.dependencyInstallAttempted === false && boundary.processTerminationAttempted === false && boundary.dependencyInstallAttempted === false && boundary.protectedActionsExecuted.length === 0, 'all false/empty'),
    check('readiness and reliability claims remain blocked', report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false, 'all false'),
  ]

  writeFileSync(resolve(docsDir, 'quality-blocker-taxonomy-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.taxonomyChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.taxonomyChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`current_product_quality_gate_status=${report.currentProductQualityGateStatus}`)
  console.log(`expected_product_quality_gate_failure_count=${report.expectedProductQualityGateFailureCount}`)
  console.log(`known_failure_group_count=${report.knownFailureGroups.length}`)
  console.log(`unexpected_failure_group_count=${report.unexpectedFailureGroups.length}`)
  console.log(`next_unblocked_action=${report.nextUnblockedAction}`)
}

main()
