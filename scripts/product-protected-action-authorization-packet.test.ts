import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'

const root = process.cwd()
const scriptPath = resolve(root, 'scripts/product-protected-action-authorization-packet.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-protected-authorization-'))
  tempDirs.push(dir)
  return dir
}

function writeJson(rootDir: string, path: string, value: Record<string, any>): void {
  const absolutePath = join(rootDir, path)
  mkdirSync(dirname(absolutePath), { recursive: true })
  writeFileSync(absolutePath, JSON.stringify(value, null, 2) + '\n')
}

const localNoProvider = {
  providerCallsPerformed: [],
  liveModelCallsPerformed: [],
  externalCallsPerformed: [],
  protectedActionsExecuted: [],
  releaseReadinessClaimAllowed: false,
  productionReadinessClaimAllowed: false,
  publicReadinessClaimAllowed: false,
  externalValidationClaimAllowed: false,
  autonomousReliabilityClaimAllowed: false,
}

function writeFixtureReports(rootDir: string): void {
  writeJson(rootDir, 'docs/product-quality/quality-blocker-taxonomy-report.json', {
    ...localNoProvider,
    currentProductQualityGateStatus: 'blocked_by_known_vscode_update_dependent_failures',
    expectedProductQualityGateFailureCount: 1,
  })
  writeJson(rootDir, 'docs/product-quality/vscode-update-boundary-report.json', {
    ...localNoProvider,
    boundaryStatus: 'blocked_wait_for_local_vscode_update_or_explicit_owner_process_action',
  })
  writeJson(rootDir, 'docs/product-quality/vscode-startup-diagnostics-report.json', {
    ...localNoProvider,
    diagnosisStatus: 'vscode_core_update_guard_with_visible_codesetup_process',
  })
  writeJson(rootDir, 'docs/product-quality/git-release-hygiene-report.json', {
    ...localNoProvider,
    workspaceGitStatus: 'git_repo_detected',
    commitPushAttempted: false,
    releaseActionPerformed: false,
  })
  writeJson(rootDir, 'docs/product-quality/external-benchmark-boundary-report.json', {
    ...localNoProvider,
    externalBenchmarkExecutionAuthorized: false,
    externalBenchmarkExecutionPerformed: false,
  })
  writeJson(rootDir, 'docs/product-quality/benchmark-submission-readiness-report.json', {
    ...localNoProvider,
    summary: { officialExternalSubmissionReady: false },
  })
  writeJson(rootDir, 'docs/product-quality/benchmark-policy-compliance-report.json', {
    ...localNoProvider,
    summary: { officialSWEbenchVerifiedSubmissionClaimAllowed: false },
  })
  writeJson(rootDir, 'docs/product-quality/terminal-bench-readiness-report.json', {
    ...localNoProvider,
    summary: { officialTerminalBenchExecutionReady: false },
  })
  writeJson(rootDir, 'docs/product-quality/oss-benchmark-comparison-matrix-report.json', localNoProvider)
  writeJson(rootDir, 'docs/product-quality/oss-comparison-readiness-index-report.json', localNoProvider)
  writeJson(rootDir, 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json', {
    ...localNoProvider,
    hostSmokeRealHostBlockedByVscodeCli: true,
    workbenchSmokePass: false,
    reconciliationRecords: [{ workbenchSmokeStatus: 'blocked_by_vscode_cli_unavailable' }],
    extensionAvailabilityClaimAllowed: false,
    terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY',
  })
  writeJson(rootDir, 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json', localNoProvider)
  writeJson(rootDir, 'docs/product-quality/license-boundary-authorization-report.json', {
    ...localNoProvider,
    allProtectedAuthorizationsDefaultFalse: true,
    protectedAuthorizationRequestCreated: true,
    protectedAuthorizationRequestCount: 9,
  })
  writeJson(rootDir, 'docs/product-quality/oss-provider-breadth-evidence-report.json', {
    ...localNoProvider,
    providerCallsAllowed: false,
    liveModelCallsAllowed: false,
    externalCallsAllowed: false,
    liveProviderValidationAllowed: false,
    providerCompatibilityClaimAllowed: false,
  })
  writeJson(rootDir, 'docs/product-quality/oss-release-hygiene-evidence-report.json', {
    ...localNoProvider,
    commitAllowed: false,
    pushAllowed: false,
    publishAllowed: false,
    deployAllowed: false,
    launchAllowed: false,
    signedProvenanceGenerated: false,
    signedProvenanceClaimAllowed: false,
  })
  writeJson(rootDir, 'docs/product-quality/verification-report-consistency-report.json', {
    ...localNoProvider,
    sourceTerminalCondition: 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_CLI_UNAVAILABLE',
  })
  writeJson(rootDir, 'docs/product-quality/public-claim-boundary-report.json', {
    ...localNoProvider,
    claimBoundaryStatus: 'no_unauthorized_public_claims_detected',
    unauthorizedPositiveClaimCount: 0,
    releaseClaimAllowed: false,
    superiorityClaimAllowed: false,
  })
  writeJson(rootDir, 'docs/product-quality/github-hosted-trust-posture-report.json', {
    status: 'hosted_trust_risks_detected',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: ['github_repository_api'],
    protectedActionsExecuted: [],
    settingsMutationsPerformed: [],
    publicSecurityPostureClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
  })
  writeJson(rootDir, 'docs/product-quality/code-scanning-remediation-queue-report.json', {
    status: 'remediation_queue_required',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: ['github_code_scanning_alert_sample_discovery'],
    protectedActionsExecuted: [],
    settingsMutationsPerformed: [],
    publicSecurityPostureClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    alertResolutionClaimAllowed: false,
  })
}

function runPacket(cwd: string): void {
  const result = spawnSync('bun', ['run', scriptPath], {
    cwd,
    encoding: 'utf8',
    shell: false,
  })

  expect(result.status, result.stderr || result.stdout).toBe(0)
}

function readPacket(cwd: string): Record<string, any> {
  return JSON.parse(readFileSync(join(cwd, 'docs/product-quality/protected-action-authorization-packet.json'), 'utf8'))
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('protected action authorization packet', () => {
  test('routes hosted GitHub trust gaps into an owner authorization item', () => {
    const repo = makeTempRepo()
    writeFixtureReports(repo)

    runPacket(repo)
    const packet = readPacket(repo)
    const authorizations = packet.requiredOwnerAuthorizations as Array<Record<string, any>>
    const sourceBindings = packet.sourceReportBindings as Array<Record<string, any>>

    expect(sourceBindings.map((source) => source.path)).toContain('docs/product-quality/github-hosted-trust-posture-report.json')
    expect(sourceBindings.map((source) => source.path)).toContain('docs/product-quality/code-scanning-remediation-queue-report.json')

    const hostedAuthorization = authorizations.find((item) => item.id === 'authorize_hosted_github_security_controls')
    expect(hostedAuthorization).toBeDefined()
    expect(hostedAuthorization?.category).toBe('hosted_security')
    expect(hostedAuthorization?.authorized).toBe(false)
    expect(hostedAuthorization?.executed).toBe(false)
    expect(hostedAuthorization?.sourceReports).toContain('docs/product-quality/github-hosted-trust-posture-report.json')
    expect(hostedAuthorization?.sourceReports).toContain('docs/product-quality/code-scanning-remediation-queue-report.json')
    expect(hostedAuthorization?.currentEvidence).toContain('branch protection')
    expect(hostedAuthorization?.currentEvidence).toContain('secret scanning')
    expect(hostedAuthorization?.currentEvidence).toContain('code scanning')
    expect(hostedAuthorization?.validationMethod).toContain('product:github-hosted-trust-posture')
    expect(hostedAuthorization?.validationMethod).toContain('product:code-scanning-remediation-queue')
  })

  test('accepts a clear current VS Code environment while keeping claim boundaries blocked', () => {
    const repo = makeTempRepo()
    writeFixtureReports(repo)
    writeJson(repo, 'docs/product-quality/quality-blocker-taxonomy-report.json', {
      ...localNoProvider,
      currentProductQualityGateStatus: 'clear_no_current_vscode_update_dependent_failures',
      expectedProductQualityGateFailureCount: 0,
    })
    writeJson(repo, 'docs/product-quality/vscode-update-boundary-report.json', {
      ...localNoProvider,
      boundaryStatus: 'clear_no_current_vscode_update_boundary',
    })
    writeJson(repo, 'docs/product-quality/vscode-startup-diagnostics-report.json', {
      ...localNoProvider,
      diagnosisStatus: 'clear_no_current_update_guard_evidence',
    })

    runPacket(repo)
    const packet = readPacket(repo)
    const vscodeCheck = (packet.evidenceChecks as Array<Record<string, any>>).find(
      (item) => item.label === 'VS Code CLI/PATH/install-state boundary is classified',
    )
    const localEnvironmentAuthorization = (packet.requiredOwnerAuthorizations as Array<Record<string, any>>).find(
      (item) => item.id === 'authorize_local_vscode_cli_path_or_install_state_repair',
    )

    expect(vscodeCheck).toBeDefined()
    expect(vscodeCheck?.ok).toBe(true)
    expect(vscodeCheck?.detail).toContain('clear_no_current_vscode_update_boundary')
    expect(localEnvironmentAuthorization?.authorized).toBe(false)
    expect(localEnvironmentAuthorization?.executed).toBe(false)
    expect(packet.releaseReadinessClaimAllowed).toBe(false)
    expect(packet.publicReadinessClaimAllowed).toBe(false)
    expect(packet.externalValidationClaimAllowed).toBe(false)
  })

  test('accepts real IDE host and workbench evidence while keeping availability claims blocked', () => {
    const repo = makeTempRepo()
    writeFixtureReports(repo)
    writeJson(repo, 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json', {
      ...localNoProvider,
      hostSmokePass: true,
      hostSmokeRealHostBlockedByVscodeCli: false,
      workbenchSmokePass: true,
      reconciliationRecords: [{ workbenchSmokeStatus: 'local_real_workbench_smoke_passed_claim_blocked' }],
      extensionAvailabilityClaimAllowed: false,
      terminalCondition: 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY',
    })

    runPacket(repo)
    const packet = readPacket(repo)
    const ideCheck = (packet.evidenceChecks as Array<Record<string, any>>).find(
      (item) => item.label === 'IDE/editor surface availability boundary remains protected',
    )

    expect(ideCheck).toBeDefined()
    expect(ideCheck?.ok).toBe(true)
    expect(packet.protectedActionExecutionAllowed).toBe(false)
    expect(packet.releaseReadinessClaimAllowed).toBe(false)
    expect(packet.publicReadinessClaimAllowed).toBe(false)
    expect(packet.externalValidationClaimAllowed).toBe(false)
  })
})
