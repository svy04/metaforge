import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceInput = {
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type DependencyEntry = {
  name: string
  version: string
  scope: 'runtime' | 'development'
  rangeKind: 'exact' | 'semver_range' | 'other'
}

type PackageJson = {
  name?: string
  version?: string
  packageManager?: string
  dependencies?: Record<string, string>
  devDependencies?: Record<string, string>
  overrides?: Record<string, string>
}

type DependencyGovernanceQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_dependency_governance_quality'
  primarySourceInputs: SourceInput[]
  packageJsonPath: string
  packageJsonSha256: string
  packageManagerField: string | null
  packageManagerFieldPresent: boolean
  workflowBunVersions: string[]
  packageManagerMatchesWorkflowBunVersion: boolean
  bunLockPath: string
  bunLockSha256: string
  bunLockSizeBytes: number
  bunLockTextStructureRecognized: boolean
  bunLockfileVersion: number | null
  bunLockRootWorkspacePresent: boolean
  bunLockCoversPackageManifestDependencies: boolean
  missingManifestDependenciesInLockfile: string[]
  dependencyEntries: DependencyEntry[]
  runtimeDependencyCount: number
  developmentDependencyCount: number
  exactVersionCount: number
  semverRangeCount: number
  otherVersionSpecifierCount: number
  overridesPresent: boolean
  overrideNames: string[]
  dependabotConfigPath: string
  dependabotConfigSha256: string
  dependabotCoversNpm: boolean
  dependabotCoversGitHubActions: boolean
  dependabotSchedulesPresent: boolean
  dependencyReviewWorkflowPath: string
  dependencyReviewWorkflowSha256: string
  dependencyReviewWorkflowPresent: boolean
  dependencyReviewActionConfigured: boolean
  dependencyReviewActionPinned: boolean
  dependencyReviewWorkflowPullRequestOnly: boolean
  dependencyReviewWorkflowPermissionsReadOnly: boolean
  dependencyReviewHostedRunPerformed: false
  dependencyReviewRequiredStatusClaimAllowed: false
  prWorkflowPath: string
  releaseWorkflowPath: string
  frozenDependencyInstallPresent: boolean
  externalVulnerabilityScanPerformed: false
  npmAuditPerformed: false
  githubApiCallsPerformed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  vulnerabilityFreeClaimAllowed: false
  dependencyReviewPassClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  claimBoundary: string
  governanceChecks: Check[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const packageJsonPath = 'package.json'
const bunLockPath = 'bun.lock'
const dependabotConfigPath = '.github/dependabot.yml'
const dependencyReviewWorkflowPath = '.github/workflows/dependency-review.yml'
const prWorkflowPath = '.github/workflows/pr-checks.yml'
const releaseWorkflowPath = '.github/workflows/release.yml'

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function packageManagerVersion(packageManager: string | undefined): string | null {
  const match = packageManager?.match(/^bun@(.+)$/)
  return match?.[1] ?? null
}

function workflowBunVersions(...texts: string[]): string[] {
  const matches = texts.flatMap((text) => [...text.matchAll(/bun-version:\s*["']?([^"'\s]+)/g)].map((match) => match[1]))
  return [...new Set(matches)].sort((left, right) => left.localeCompare(right))
}

function actionReferencesArePinned(text: string): boolean {
  const usesLines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith('uses: '))

  return usesLines.length > 0 && usesLines.every((line) => /@[a-f0-9]{40}(?:\s|$)/i.test(line))
}

function rangeKind(version: string): DependencyEntry['rangeKind'] {
  if (/^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$/.test(version)) {
    return 'exact'
  }
  if (/^[~^]|[<>=*xX|]/.test(version)) {
    return 'semver_range'
  }
  return 'other'
}

function dependencyEntries(packageJson: PackageJson): DependencyEntry[] {
  const runtime = Object.entries(packageJson.dependencies ?? {}).map(([name, version]) => ({
    name,
    version,
    scope: 'runtime' as const,
    rangeKind: rangeKind(version),
  }))
  const development = Object.entries(packageJson.devDependencies ?? {}).map(([name, version]) => ({
    name,
    version,
    scope: 'development' as const,
    rangeKind: rangeKind(version),
  }))
  return [...runtime, ...development].sort((left, right) => left.name.localeCompare(right.name))
}

function lockHasManifestEntry(lockText: string, entry: DependencyEntry): boolean {
  const needle = `${JSON.stringify(entry.name)}: ${JSON.stringify(entry.version)}`
  return lockText.includes(needle)
}

function lockfileVersion(lockText: string): number | null {
  const match = lockText.match(/"lockfileVersion":\s*(\d+)/)
  return match ? Number(match[1]) : null
}

function hasRootWorkspace(lockText: string): boolean {
  return /"workspaces":\s*\{\s*"":\s*\{/.test(lockText)
}

function missingManifestDependenciesInLockfile(packageJson: PackageJson, lockText: string): string[] {
  if (!hasRootWorkspace(lockText)) {
    return dependencyEntries(packageJson).map((entry) => entry.name)
  }
  return dependencyEntries(packageJson)
    .filter((entry) => !lockHasManifestEntry(lockText, entry))
    .map((entry) => entry.name)
}

function writeMarkdown(report: DependencyGovernanceQualityReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const dependencyRows = report.dependencyEntries
    .map((entry) => `| \`${entry.name}\` | \`${entry.scope}\` | \`${entry.version}\` | \`${entry.rangeKind}\` |`)
    .join('\n')
  const checkRows = report.governanceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Dependency Governance Quality Report

Generated by: \`bun run product:dependency-governance-quality\`

## Claim Boundary

- This report verifies local source-controlled dependency governance evidence only.
- It does not run \`bun install\`, \`npm audit\`, GitHub APIs, hosted dependency review, providers, live models, or external services.
- It does not claim dependency-review success, vulnerability-free status, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- package_json_sha256: \`${report.packageJsonSha256}\`
- package_manager_field: \`${report.packageManagerField ?? 'null'}\`
- package_manager_matches_workflow_bun_version: \`${report.packageManagerMatchesWorkflowBunVersion}\`
- workflow_bun_versions: \`${report.workflowBunVersions.join(',')}\`
- bun_lock_sha256: \`${report.bunLockSha256}\`
- bun_lock_size_bytes: \`${report.bunLockSizeBytes}\`
- bun_lock_text_structure_recognized: \`${report.bunLockTextStructureRecognized}\`
- bun_lockfile_version: \`${report.bunLockfileVersion ?? 'null'}\`
- bun_lock_root_workspace_present: \`${report.bunLockRootWorkspacePresent}\`
- bun_lock_covers_package_manifest_dependencies: \`${report.bunLockCoversPackageManifestDependencies}\`
- runtime_dependency_count: \`${report.runtimeDependencyCount}\`
- development_dependency_count: \`${report.developmentDependencyCount}\`
- exact_version_count: \`${report.exactVersionCount}\`
- semver_range_count: \`${report.semverRangeCount}\`
- other_version_specifier_count: \`${report.otherVersionSpecifierCount}\`
- overrides_present: \`${report.overridesPresent}\`
- override_names: \`${report.overrideNames.join(',') || 'none'}\`
- dependabot_covers_npm: \`${report.dependabotCoversNpm}\`
- dependabot_covers_github_actions: \`${report.dependabotCoversGitHubActions}\`
- dependency_review_workflow_present: \`${report.dependencyReviewWorkflowPresent}\`
- dependency_review_action_configured: \`${report.dependencyReviewActionConfigured}\`
- dependency_review_action_pinned: \`${report.dependencyReviewActionPinned}\`
- dependency_review_hosted_run_performed: \`${report.dependencyReviewHostedRunPerformed}\`
- dependency_review_required_status_claim_allowed: \`${report.dependencyReviewRequiredStatusClaimAllowed}\`
- frozen_dependency_install_present: \`${report.frozenDependencyInstallPresent}\`
- external_vulnerability_scan_performed: \`${report.externalVulnerabilityScanPerformed}\`
- npm_audit_performed: \`${report.npmAuditPerformed}\`
- github_api_calls_performed: \`${report.githubApiCallsPerformed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Direct Dependency Inventory

| Package | Scope | Manifest Version | Range Kind |
| --- | --- | --- | --- |
${dependencyRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'dependency-governance-quality-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })

  const packageJsonText = readText(packageJsonPath)
  const packageJson = JSON.parse(packageJsonText) as PackageJson
  const bunLockExists = existsSync(resolve(root, bunLockPath))
  const bunLockText = bunLockExists ? readText(bunLockPath) : ''
  const dependabotConfig = readText(dependabotConfigPath)
  const dependencyReviewWorkflow = readText(dependencyReviewWorkflowPath)
  const prWorkflow = readText(prWorkflowPath)
  const releaseWorkflow = readText(releaseWorkflowPath)
  const entries = dependencyEntries(packageJson)
  const missingFromLockfile = missingManifestDependenciesInLockfile(packageJson, bunLockText)
  const workflowVersions = workflowBunVersions(prWorkflow, releaseWorkflow)
  const packageManager = packageJson.packageManager ?? null
  const packageManagerBunVersion = packageManagerVersion(packageJson.packageManager)
  const packageManagerMatchesWorkflowBunVersion = packageManagerBunVersion !== null && workflowVersions.includes(packageManagerBunVersion)
  const exactVersionCount = entries.filter((entry) => entry.rangeKind === 'exact').length
  const semverRangeCount = entries.filter((entry) => entry.rangeKind === 'semver_range').length
  const otherVersionSpecifierCount = entries.filter((entry) => entry.rangeKind === 'other').length
  const overrideNames = Object.keys(packageJson.overrides ?? {}).sort((left, right) => left.localeCompare(right))
  const dependencyReviewWorkflowPresent = dependencyReviewWorkflow.trim().length > 0
  const dependencyReviewActionConfigured = /actions\/dependency-review-action@[a-f0-9]{40}/i.test(dependencyReviewWorkflow)
  const dependencyReviewActionPinned = actionReferencesArePinned(dependencyReviewWorkflow)
  const dependencyReviewWorkflowPullRequestOnly = /\bpull_request:\s*(?:\r?\n|$)/.test(dependencyReviewWorkflow) && !/\bpush:\s*(?:\r?\n|$)|\bworkflow_dispatch:\s*(?:\r?\n|$)/.test(dependencyReviewWorkflow)
  const dependencyReviewWorkflowPermissionsReadOnly = /permissions:\s*\r?\n\s+contents:\s+read/i.test(dependencyReviewWorkflow) && !/\b(write-all|contents:\s+write|packages:\s+write|id-token:\s+write)\b/i.test(dependencyReviewWorkflow)
  const dependabotCoversNpm = /package-ecosystem:\s*["']?npm["']?/i.test(dependabotConfig) && /directory:\s*["']?\/["']?/i.test(dependabotConfig)
  const dependabotCoversGitHubActions = /package-ecosystem:\s*["']?github-actions["']?/i.test(dependabotConfig)
  const dependabotSchedulesPresent = (dependabotConfig.match(/interval:\s*["']?weekly["']?/gi) ?? []).length >= 2
  const frozenDependencyInstallPresent = /bun install --frozen-lockfile/.test(prWorkflow) && /bun install --frozen-lockfile/.test(releaseWorkflow)

  const report: DependencyGovernanceQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_dependency_governance_quality',
    primarySourceInputs: [
      {
        sourceProject: 'GitHub Docs dependency review',
        sourceUrl: 'https://docs.github.com/en/code-security/concepts/supply-chain-security/about-dependency-review',
        observedPattern: 'Dependency review exposes dependency changes and vulnerability impact in pull requests, and the action can enforce review checks in GitHub Actions.',
        localAbsorption: 'OpenClaude adds a source-controlled dependency-review workflow while recording hosted execution and required-status evidence as unperformed locally.',
      },
      {
        sourceProject: 'actions/dependency-review-action',
        sourceUrl: 'https://github.com/actions/dependency-review-action',
        observedPattern: 'The action scans pull requests for dependency changes and can fail on introduced vulnerabilities or invalid licenses.',
        localAbsorption: 'OpenClaude pins the dependency-review action by full commit SHA and keeps the workflow PR-only with read-only contents permission.',
      },
      {
        sourceProject: 'Bun lockfile documentation',
        sourceUrl: 'https://bun.com/docs/install/lockfile',
        observedPattern: 'Bun creates a text lockfile called bun.lock and documents that it should be committed to source control.',
        localAbsorption: 'OpenClaude verifies bun.lock exists, is parseable, and covers every package.json direct dependency without running install.',
      },
      {
        sourceProject: 'GitHub Docs Dependabot options',
        sourceUrl: 'https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference',
        observedPattern: 'Dependabot update entries define package ecosystems, directories, and schedules for dependency maintenance.',
        localAbsorption: 'OpenClaude verifies source-controlled npm and GitHub Actions Dependabot coverage and weekly schedules.',
      },
      {
        sourceProject: 'OpenSSF Scorecard Pinned-Dependencies',
        sourceUrl: 'https://github.com/ossf/scorecard/blob/main/docs/checks.md',
        observedPattern: 'Build and release dependencies should be pinned to reduce compromised dependency risk, while external Scorecard execution remains a separate evidence boundary.',
        localAbsorption: 'OpenClaude keeps workflow actions SHA-pinned and records dependency-review/source-control evidence without claiming an external Scorecard result.',
      },
    ],
    packageJsonPath,
    packageJsonSha256: sha256(packageJsonText),
    packageManagerField: packageManager,
    packageManagerFieldPresent: packageManager !== null,
    workflowBunVersions: workflowVersions,
    packageManagerMatchesWorkflowBunVersion,
    bunLockPath,
    bunLockSha256: bunLockExists ? fileSha256(bunLockPath) : 'missing',
    bunLockSizeBytes: bunLockExists ? statSync(resolve(root, bunLockPath)).size : 0,
    bunLockTextStructureRecognized: lockfileVersion(bunLockText) !== null && hasRootWorkspace(bunLockText),
    bunLockfileVersion: lockfileVersion(bunLockText),
    bunLockRootWorkspacePresent: hasRootWorkspace(bunLockText),
    bunLockCoversPackageManifestDependencies: missingFromLockfile.length === 0,
    missingManifestDependenciesInLockfile: missingFromLockfile,
    dependencyEntries: entries,
    runtimeDependencyCount: entries.filter((entry) => entry.scope === 'runtime').length,
    developmentDependencyCount: entries.filter((entry) => entry.scope === 'development').length,
    exactVersionCount,
    semverRangeCount,
    otherVersionSpecifierCount,
    overridesPresent: overrideNames.length > 0,
    overrideNames,
    dependabotConfigPath,
    dependabotConfigSha256: fileSha256(dependabotConfigPath),
    dependabotCoversNpm,
    dependabotCoversGitHubActions,
    dependabotSchedulesPresent,
    dependencyReviewWorkflowPath,
    dependencyReviewWorkflowSha256: fileSha256(dependencyReviewWorkflowPath),
    dependencyReviewWorkflowPresent,
    dependencyReviewActionConfigured,
    dependencyReviewActionPinned,
    dependencyReviewWorkflowPullRequestOnly,
    dependencyReviewWorkflowPermissionsReadOnly,
    dependencyReviewHostedRunPerformed: false,
    dependencyReviewRequiredStatusClaimAllowed: false,
    prWorkflowPath,
    releaseWorkflowPath,
    frozenDependencyInstallPresent,
    externalVulnerabilityScanPerformed: false,
    npmAuditPerformed: false,
    githubApiCallsPerformed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    vulnerabilityFreeClaimAllowed: false,
    dependencyReviewPassClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    claimBoundary: 'Dependency governance quality is local source-controlled evidence only. It does not prove hosted dependency-review execution, vulnerability-free status, external Scorecard posture, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    governanceChecks: [],
  }

  report.governanceChecks = [
    check('packageManager field is explicit and aligned with workflow Bun version', report.packageManagerFieldPresent && report.packageManagerMatchesWorkflowBunVersion, `${report.packageManagerField ?? 'missing'} vs ${workflowVersions.join(',')}`),
    check('bun.lock exists and has recognized text structure', bunLockExists && report.bunLockTextStructureRecognized && report.bunLockfileVersion === 1, `${report.bunLockPath}/${report.bunLockSizeBytes} bytes`),
    check('bun.lock root workspace is present', report.bunLockRootWorkspacePresent, 'workspaces[""]'),
    check('bun.lock covers every direct package manifest dependency', report.bunLockCoversPackageManifestDependencies, report.missingManifestDependenciesInLockfile.join(',') || 'all present'),
    check('dependency range inventory is explicit', report.dependencyEntries.length > 0 && report.exactVersionCount + report.semverRangeCount + report.otherVersionSpecifierCount === report.dependencyEntries.length, `${report.dependencyEntries.length} direct entries`),
    check('runtime and development dependencies are both inventoried', report.runtimeDependencyCount > 0 && report.developmentDependencyCount > 0, `${report.runtimeDependencyCount}/${report.developmentDependencyCount}`),
    check('override policy is present for constrained dependency drift', report.overridesPresent, report.overrideNames.join(',') || 'none'),
    check('Dependabot covers npm and GitHub Actions with schedules', report.dependabotCoversNpm && report.dependabotCoversGitHubActions && report.dependabotSchedulesPresent, report.dependabotConfigPath),
    check('dependency-review workflow is source-controlled and PR-only', report.dependencyReviewWorkflowPresent && report.dependencyReviewWorkflowPullRequestOnly, report.dependencyReviewWorkflowPath),
    check('dependency-review action references are pinned by full SHA', report.dependencyReviewActionConfigured && report.dependencyReviewActionPinned, report.dependencyReviewWorkflowPath),
    check('dependency-review workflow permissions are read-only', report.dependencyReviewWorkflowPermissionsReadOnly, 'contents: read'),
    check('frozen dependency install is wired into PR and release workflows', report.frozenDependencyInstallPresent, `${report.prWorkflowPath}, ${report.releaseWorkflowPath}`),
    check('hosted dependency review and vulnerability scans remain unclaimed locally', report.dependencyReviewHostedRunPerformed === false && report.dependencyReviewRequiredStatusClaimAllowed === false && report.externalVulnerabilityScanPerformed === false && report.npmAuditPerformed === false && report.githubApiCallsPerformed === false, 'all hosted/external flags false'),
    check('provider live external calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero'),
    check('vulnerability and readiness claims remain blocked', report.vulnerabilityFreeClaimAllowed === false && report.dependencyReviewPassClaimAllowed === false && report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false, 'all false'),
  ]

  writeFileSync(resolve(docsDir, 'dependency-governance-quality-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.governanceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.governanceChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`package_manager_field=${report.packageManagerField}`)
  console.log(`workflow_bun_versions=${report.workflowBunVersions.join(',')}`)
  console.log(`bun_lock_covers_package_manifest_dependencies=${report.bunLockCoversPackageManifestDependencies}`)
  console.log(`direct_dependency_count=${report.dependencyEntries.length}`)
  console.log(`dependency_review_action_configured=${report.dependencyReviewActionConfigured}`)
  console.log(`dependency_review_hosted_run_performed=${report.dependencyReviewHostedRunPerformed}`)
  console.log(`external_vulnerability_scan_performed=${report.externalVulnerabilityScanPerformed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
}

main()
