import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { argv, exit } from 'node:process'
import { spawnSync } from 'node:child_process'

import { check, readText, type Check } from './quality-report-helpers'

type PackageJson = {
  name?: string
  license?: unknown
  repository?: string | {
    type?: string
    url?: string
  }
}

type Blocker = {
  category:
    | 'stale_repository_origin'
    | 'package_license_boundary_missing'
    | 'blanket_mit_license_claim'
    | 'missing_derived_runtime_boundary'
    | 'missing_metaforge_os_boundary'
    | 'fully_original_cli_claim'
    | 'ambiguous_external_npm_install_claim'
    | 'source_license_claim_overreach'
    | 'third_party_license_claim_overreach'
    | 'legal_review_claim_present'
    | 'license_boundary_claim_overreach'
    | 'public_remote_surface_blocked'
    | 'protected_release_action_attempted'
    | 'provider_or_live_call_claim_present'
    | 'required_source_report_missing'
  path?: string
  detail: string
}

type OriginLicenseProvenanceInput = {
  packageJson: PackageJson
  originRemoteUrl: string
  readmeText: string
  koreanReadmeText: string
  licenseText: string
  sourceLicenseMetadataReport: Record<string, unknown>
  thirdPartyLicenseReport: Record<string, unknown>
  licenseBoundaryAuthorizationReport: Record<string, unknown>
  githubRemoteSurfaceAuditReport: Record<string, unknown>
  releaseArtifactProvenanceReport: Record<string, unknown>
  sourceReportHashes?: Record<string, string>
}

type OriginLicenseProvenanceBoundaryReport = {
  generatedAt: string
  mode: 'local_no_provider_origin_license_provenance_boundary'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  packageName: string | null
  packageLicenseField: string | null
  packageRepositoryUrl: string | null
  originRemoteUrl: string
  sourceReportHashes: Record<string, string>
  blockers: Blocker[]
  blockerCount: number
  status:
    | 'no_origin_license_provenance_boundary_findings'
    | 'blocked_origin_license_provenance_boundary'
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  publishAttempted: false
  deployAttempted: false
  launchAttempted: false
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/origin-license-provenance-boundary-report.json'
const reportMdPath = 'docs/product-quality/origin-license-provenance-boundary-report.md'
const reportJsonlPath = 'reports/openclaude-origin-license-provenance-boundary.jsonl'
const expectedRepositorySlug = 'svy04/metaforge'

export function originLicenseProvenanceMode(args = argv): 'check' | 'write' {
  return args.includes('--check') ? 'check' : 'write'
}

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function packageRepositoryUrl(pkg: PackageJson): string | null {
  if (typeof pkg.repository === 'string') return pkg.repository
  if (typeof pkg.repository?.url === 'string') return pkg.repository.url
  return null
}

function includesExpectedRepository(url: string | null): boolean {
  return typeof url === 'string' && url.toLowerCase().includes(expectedRepositorySlug)
}

function trueFlag(report: Record<string, unknown>, keys: string[]): string | null {
  return keys.find((key) => report[key] === true) ?? null
}

function arrayLength(report: Record<string, unknown>, key: string): number {
  const value = report[key]
  return Array.isArray(value) ? value.length : 0
}

function containsDerivedBoundary(text: string): boolean {
  return /derived from Anthropic'?s Claude Code CLI/i.test(text)
    || /Anthropic Claude Code CLI.*\bderived\b/i.test(text)
    || /Anthropic Claude Code CLI.*파생/i.test(text)
}

function containsMetaforgeBoundary(text: string): boolean {
  return /Meta\s*(?:\+|\/)\s*MFH\s*(?:\+|\/)\s*Orchestra\s*OS/i.test(text)
}

function containsBlanketMitClaim(text: string): boolean {
  return /license-MIT/i.test(text)
    || /fully original MIT-licensed/i.test(text)
    || /MIT-licensed CLI/i.test(text)
    || /blanket MIT license/i.test(text) && !/not a blanket MIT license/i.test(text)
}

function containsFullyOriginalClaim(text: string): boolean {
  return /fully original/i.test(text)
    || /built from scratch/i.test(text)
    || /from scratch/i.test(text)
}

function containsAmbiguousExternalNpmInstall(text: string): boolean {
  if (!/npm install -g @gitlawb\/openclaude/i.test(text)) return false
  return !/external OpenClaude npm package/i.test(text)
    || !/not a Metaforge release artifact/i.test(text)
}

function addBlocker(blockers: Blocker[], category: Blocker['category'], detail: string, path?: string): void {
  blockers.push(path ? { category, path, detail } : { category, detail })
}

export function analyzeOriginLicenseProvenanceBoundary(
  input: OriginLicenseProvenanceInput,
): OriginLicenseProvenanceBoundaryReport {
  const blockers: Blocker[] = []
  const repositoryUrl = packageRepositoryUrl(input.packageJson)
  const packageLicenseField = typeof input.packageJson.license === 'string'
    ? input.packageJson.license
    : null
  const readmePair = `${input.readmeText}\n${input.koreanReadmeText}`
  const allPublicText = `${readmePair}\n${input.licenseText}`

  if (!includesExpectedRepository(repositoryUrl) || !includesExpectedRepository(input.originRemoteUrl)) {
    addBlocker(
      blockers,
      'stale_repository_origin',
      `package repository and git origin must point at ${expectedRepositorySlug}`,
      'package.json',
    )
  }

  if (packageLicenseField !== 'SEE LICENSE FILE') {
    addBlocker(
      blockers,
      'package_license_boundary_missing',
      `package license must preserve SEE LICENSE FILE boundary; found ${String(packageLicenseField)}`,
      'package.json',
    )
  }

  if (packageLicenseField === 'MIT' || containsBlanketMitClaim(allPublicText)) {
    addBlocker(
      blockers,
      'blanket_mit_license_claim',
      'public package/readme/license surfaces must not imply blanket MIT licensing over the derived runtime',
    )
  }

  if (!containsDerivedBoundary(input.readmeText) || !containsDerivedBoundary(input.koreanReadmeText) || !containsDerivedBoundary(input.licenseText)) {
    addBlocker(
      blockers,
      'missing_derived_runtime_boundary',
      'English README, Korean README, and LICENSE must all state the Anthropic Claude Code derived runtime boundary',
    )
  }

  if (!containsMetaforgeBoundary(readmePair)) {
    addBlocker(
      blockers,
      'missing_metaforge_os_boundary',
      'public README surfaces must keep Metaforge framed as Meta + MFH + Orchestra OS',
    )
  }

  if (containsFullyOriginalClaim(readmePair)) {
    addBlocker(
      blockers,
      'fully_original_cli_claim',
      'public README surfaces must not imply a fully original CLI when fork/adaptation ancestry is material',
    )
  }

  if (containsAmbiguousExternalNpmInstall(readmePair)) {
    addBlocker(
      blockers,
      'ambiguous_external_npm_install_claim',
      'npm install -g @gitlawb/openclaude must be labeled as the external OpenClaude npm package and not a Metaforge release artifact',
    )
  }

  const sourceLicenseOverreach = trueFlag(input.sourceLicenseMetadataReport, [
    'reuseComplianceClaimAllowed',
    'sourceLicenseComplianceClaimAllowed',
    'sourceMetadataReadyClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
  ])
  if (sourceLicenseOverreach !== null) {
    addBlocker(
      blockers,
      'source_license_claim_overreach',
      `${sourceLicenseOverreach} is true in source license metadata report`,
    )
  }

  const thirdPartyLicenseOverreach = trueFlag(input.thirdPartyLicenseReport, [
    'licenseComplianceClaimAllowed',
    'thirdPartyNoticeReadyClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
  ])
  if (thirdPartyLicenseOverreach !== null) {
    addBlocker(
      blockers,
      'third_party_license_claim_overreach',
      `${thirdPartyLicenseOverreach} is true in third-party license report`,
    )
  }

  if (input.licenseBoundaryAuthorizationReport.legalReviewPerformed === true) {
    addBlocker(
      blockers,
      'legal_review_claim_present',
      'legalReviewPerformed must stay false until an actual legal review is recorded',
    )
  }

  const authorizationOverreach = trueFlag(input.licenseBoundaryAuthorizationReport, [
    'licenseBoundaryAuthorizationClaimAllowed',
    'licenseComplianceClaimAllowed',
    'thirdPartyNoticeReadyClaimAllowed',
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
  ])
  if (authorizationOverreach !== null) {
    addBlocker(
      blockers,
      'license_boundary_claim_overreach',
      `${authorizationOverreach} is true in license boundary authorization report`,
    )
  }

  if (
    input.githubRemoteSurfaceAuditReport.status !== 'no_public_github_surface_findings_detected'
    || Number(input.githubRemoteSurfaceAuditReport.blockerCount ?? 0) !== 0
  ) {
    addBlocker(
      blockers,
      'public_remote_surface_blocked',
      'GitHub remote surface audit must be clean before origin/license provenance is claimable',
    )
  }

  if (
    input.releaseArtifactProvenanceReport.publishAttempted === true
    || input.releaseArtifactProvenanceReport.deployAttempted === true
    || input.releaseArtifactProvenanceReport.launchAttempted === true
  ) {
    addBlocker(
      blockers,
      'protected_release_action_attempted',
      'release provenance inputs must not publish, deploy, or launch',
    )
  }

  const providerOrLiveCalls =
    arrayLength(input.sourceLicenseMetadataReport, 'providerCallsPerformed')
    + arrayLength(input.sourceLicenseMetadataReport, 'liveModelCallsPerformed')
    + arrayLength(input.thirdPartyLicenseReport, 'providerCallsPerformed')
    + arrayLength(input.thirdPartyLicenseReport, 'liveModelCallsPerformed')
    + arrayLength(input.licenseBoundaryAuthorizationReport, 'providerCallsPerformed')
    + arrayLength(input.licenseBoundaryAuthorizationReport, 'liveModelCallsPerformed')
    + arrayLength(input.githubRemoteSurfaceAuditReport, 'providerCallsPerformed')
    + arrayLength(input.githubRemoteSurfaceAuditReport, 'liveModelCallsPerformed')
    + arrayLength(input.releaseArtifactProvenanceReport, 'providerCallsPerformed')
    + arrayLength(input.releaseArtifactProvenanceReport, 'liveModelCallsPerformed')

  if (providerOrLiveCalls > 0) {
    addBlocker(
      blockers,
      'provider_or_live_call_claim_present',
      `${providerOrLiveCalls} provider/live model calls are present in upstream evidence reports`,
    )
  }

  const evidenceChecks = [
    check('package repository matches current public origin', includesExpectedRepository(repositoryUrl) && includesExpectedRepository(input.originRemoteUrl), String(repositoryUrl ?? 'missing')),
    check('package license preserves SEE LICENSE FILE boundary', packageLicenseField === 'SEE LICENSE FILE', String(packageLicenseField ?? 'missing')),
    check('public surfaces state derived runtime boundary', containsDerivedBoundary(input.readmeText) && containsDerivedBoundary(input.koreanReadmeText) && containsDerivedBoundary(input.licenseText), 'README.md, README.ko.md, LICENSE'),
    check('public surfaces keep Metaforge as Meta + MFH + Orchestra OS', containsMetaforgeBoundary(readmePair), 'README.md and README.ko.md'),
    check('blanket MIT and fully-original CLI claims are absent', !blockers.some((blocker) => blocker.category === 'blanket_mit_license_claim' || blocker.category === 'fully_original_cli_claim'), 'public text scan'),
    check('external npm install command is provenance-bounded when present', !blockers.some((blocker) => blocker.category === 'ambiguous_external_npm_install_claim'), '@gitlawb/openclaude install copy'),
    check('source and third-party license reports keep compliance/readiness claims blocked', sourceLicenseOverreach === null && thirdPartyLicenseOverreach === null, 'claim flags false'),
    check('license boundary authorization report does not claim legal review', input.licenseBoundaryAuthorizationReport.legalReviewPerformed !== true && authorizationOverreach === null, 'legal and authorization flags false'),
    check('GitHub remote surface audit has no blockers', !blockers.some((blocker) => blocker.category === 'public_remote_surface_blocked'), String(input.githubRemoteSurfaceAuditReport.status ?? 'missing')),
    check('release provenance report did not publish, deploy, or launch', !blockers.some((blocker) => blocker.category === 'protected_release_action_attempted'), 'protected release action flags false'),
    check('provider and live model calls remain absent in source evidence', providerOrLiveCalls === 0, `${providerOrLiveCalls} calls`),
  ]

  return {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_origin_license_provenance_boundary',
    primarySourceInputs: [
      {
        sourceProject: 'GitHub Docs licensing a repository',
        sourceUrl: 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository',
        observedPattern: 'GitHub treats repository licensing as an explicit public surface and separates repository license metadata from legal advice.',
        localAbsorption: 'The local gate checks that public package/readme/license surfaces preserve the actual origin and license boundary instead of overclaiming open-source readiness.',
      },
      {
        sourceProject: 'REUSE Specification 3.3',
        sourceUrl: 'https://reuse.software/spec-3.3/',
        observedPattern: 'REUSE defines comprehensive, unambiguous, human- and machine-readable licensing information for each file.',
        localAbsorption: 'The local gate consumes the existing source-license metadata report as evidence and keeps REUSE/source-compliance claims blocked until stronger file-level metadata exists.',
      },
      {
        sourceProject: 'SPDX License List',
        sourceUrl: 'https://spdx.org/licenses/',
        observedPattern: 'SPDX publishes standardized license identifiers, names, texts, and canonical URLs for license identification.',
        localAbsorption: 'The local gate requires SEE LICENSE FILE for this derived-runtime package boundary instead of collapsing the project into a blanket SPDX MIT claim.',
      },
      {
        sourceProject: 'OpenSSF Scorecard checks',
        sourceUrl: 'https://github.com/ossf/scorecard/blob/main/docs/checks.md',
        observedPattern: 'OpenSSF Scorecard treats branch protection, CI tests, dependency update tooling, and security policy as separate quality signals.',
        localAbsorption: 'The local gate composes existing remote-surface, release-provenance, and license evidence without converting them into external validation or production readiness.',
      },
    ],
    packageName: input.packageJson.name ?? null,
    packageLicenseField,
    packageRepositoryUrl: repositoryUrl,
    originRemoteUrl: input.originRemoteUrl,
    sourceReportHashes: input.sourceReportHashes ?? {},
    blockers,
    blockerCount: blockers.length,
    status: blockers.length === 0
      ? 'no_origin_license_provenance_boundary_findings'
      : 'blocked_origin_license_provenance_boundary',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    publishAttempted: false,
    deployAttempted: false,
    launchAttempted: false,
    evidenceChecks,
    claimBoundary: 'Origin/license provenance boundary evidence is a local no-provider consistency gate across package metadata, README/LICENSE copy, source-license reports, GitHub remote-surface evidence, and release-provenance reports. It does not perform legal review, claim license compliance, claim open-source readiness, claim release/public/production readiness, publish, deploy, launch, or call providers/live models.',
  }
}

export function buildOriginLicenseProvenanceJsonl(report: OriginLicenseProvenanceBoundaryReport): string {
  const records = report.blockers.length > 0
    ? report.blockers.map((blocker) => ({
      kind: 'origin_license_provenance_boundary_blocker',
      ...blocker,
    }))
    : [{
      kind: 'origin_license_provenance_boundary_summary',
      status: report.status,
      blockerCount: report.blockerCount,
      packageName: report.packageName,
      packageLicenseField: report.packageLicenseField,
      packageRepositoryUrl: report.packageRepositoryUrl,
    }]
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

function writeMarkdown(report: OriginLicenseProvenanceBoundaryReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const blockerRows = report.blockers
    .map((blocker) => `| \`${blocker.category}\` | ${blocker.path ? `\`${blocker.path}\`` : ''} | ${blocker.detail} |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Origin License Provenance Boundary Report

Generated by: \`bun run product:origin-license-provenance-boundary\`

## Claim Boundary

- This report is a local no-provider consistency gate across public origin, package license metadata, README/LICENSE copy, and existing product-quality reports.
- It does not perform legal review, claim license compliance, claim open-source readiness, claim release/public/production readiness, publish, deploy, launch, call providers, or call live models.

## Summary

- mode: \`${report.mode}\`
- status: \`${report.status}\`
- blocker_count: \`${report.blockerCount}\`
- package_name: \`${report.packageName ?? 'null'}\`
- package_license_field: \`${report.packageLicenseField ?? 'null'}\`
- package_repository_url: \`${report.packageRepositoryUrl ?? 'null'}\`
- origin_remote_url: \`${report.originRemoteUrl}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- publish_attempted: \`${report.publishAttempted}\`
- deploy_attempted: \`${report.deployAttempted}\`
- launch_attempted: \`${report.launchAttempted}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Blockers

| Category | Path | Detail |
| --- | --- | --- |
${blockerRows || '| `none` |  |  |'}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function currentOriginRemoteUrl(): string {
  const result = spawnSync('git', ['remote', 'get-url', 'origin'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })
  if (result.status !== 0) {
    throw new Error(`git remote get-url origin failed: ${result.stderr || result.stdout}`)
  }
  return result.stdout.trim()
}

function main(): void {
  const mode = originLicenseProvenanceMode()

  if (mode === 'write') {
    mkdirSync(docsDir, { recursive: true })
    mkdirSync(reportsDir, { recursive: true })
  }

  const requiredReportPaths = {
    sourceLicenseMetadataReport: 'docs/product-quality/source-license-metadata-quality-report.json',
    thirdPartyLicenseReport: 'docs/product-quality/third-party-license-quality-report.json',
    licenseBoundaryAuthorizationReport: 'docs/product-quality/license-boundary-authorization-report.json',
    githubRemoteSurfaceAuditReport: 'docs/product-quality/github-remote-surface-audit-report.json',
    releaseArtifactProvenanceReport: 'docs/product-quality/release-artifact-provenance-report.json',
  }

  const missingReports = Object.values(requiredReportPaths).filter((path) => !existsSync(resolve(root, path)))
  if (missingReports.length > 0) {
    const report = analyzeOriginLicenseProvenanceBoundary({
      packageJson: existsSync(resolve(root, 'package.json')) ? readJson<PackageJson>('package.json') : {},
      originRemoteUrl: currentOriginRemoteUrl(),
      readmeText: existsSync(resolve(root, 'README.md')) ? readText('README.md') : '',
      koreanReadmeText: existsSync(resolve(root, 'README.ko.md')) ? readText('README.ko.md') : '',
      licenseText: existsSync(resolve(root, 'LICENSE')) ? readText('LICENSE') : '',
      sourceLicenseMetadataReport: {},
      thirdPartyLicenseReport: {},
      licenseBoundaryAuthorizationReport: {},
      githubRemoteSurfaceAuditReport: {},
      releaseArtifactProvenanceReport: {},
      sourceReportHashes: {},
    })
    for (const path of missingReports) {
      addBlocker(report.blockers, 'required_source_report_missing', `required source report missing: ${path}`, path)
    }
    report.blockerCount = report.blockers.length
    report.status = 'blocked_origin_license_provenance_boundary'
    if (mode === 'write') {
      writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
      writeMarkdown(report)
      writeFileSync(resolve(root, reportJsonlPath), buildOriginLicenseProvenanceJsonl(report))
    }
    console.error(`RESULT: FAIL (${missingReports.length} required reports missing)`)
    console.error(`mode=${mode}`)
    exit(1)
  }

  const sourceReportHashes = Object.fromEntries(
    Object.entries(requiredReportPaths).map(([key, path]) => [key, fileSha256(path)]),
  )

  const report = analyzeOriginLicenseProvenanceBoundary({
    packageJson: readJson<PackageJson>('package.json'),
    originRemoteUrl: currentOriginRemoteUrl(),
    readmeText: readText('README.md'),
    koreanReadmeText: readText('README.ko.md'),
    licenseText: readText('LICENSE'),
    sourceLicenseMetadataReport: readJson<Record<string, unknown>>(requiredReportPaths.sourceLicenseMetadataReport),
    thirdPartyLicenseReport: readJson<Record<string, unknown>>(requiredReportPaths.thirdPartyLicenseReport),
    licenseBoundaryAuthorizationReport: readJson<Record<string, unknown>>(requiredReportPaths.licenseBoundaryAuthorizationReport),
    githubRemoteSurfaceAuditReport: readJson<Record<string, unknown>>(requiredReportPaths.githubRemoteSurfaceAuditReport),
    releaseArtifactProvenanceReport: readJson<Record<string, unknown>>(requiredReportPaths.releaseArtifactProvenanceReport),
    sourceReportHashes,
  })

  if (mode === 'write') {
    writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
    writeMarkdown(report)
    writeFileSync(resolve(root, reportJsonlPath), buildOriginLicenseProvenanceJsonl(report))
  }

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  console.log('')
  console.log(`RESULT: ${report.blockerCount === 0 && report.evidenceChecks.every((item) => item.ok) ? 'PASS' : 'FAIL'}`)
  console.log(`mode=${mode}`)
  console.log(`status=${report.status}`)
  console.log(`blocker_count=${report.blockerCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`publish_attempted=${report.publishAttempted}`)
  console.log(`deploy_attempted=${report.deployAttempted}`)
  console.log(`launch_attempted=${report.launchAttempted}`)

  if (report.blockerCount > 0 || !report.evidenceChecks.every((item) => item.ok)) {
    exit(1)
  }
}

if (import.meta.main) {
  try {
    main()
  } catch (error) {
    console.error(error instanceof Error ? error.message : String(error))
    exit(1)
  }
}
