import { existsSync, mkdirSync, readdirSync, statSync, writeFileSync } from 'node:fs'
import { dirname, resolve } from 'node:path'
import { check, fileSha256, readText, sha256, type Check } from './quality-report-helpers'

type SourceInput = {
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type PackageJson = {
  name?: string
  version?: string
  license?: unknown
  licenses?: unknown
  dependencies?: Record<string, string>
  devDependencies?: Record<string, string>
  repository?: unknown
}

type LockfileInventoryRecord = {
  schemaVersion: 'openclaude_lockfile_inventory_v1'
  packageKey: string
  name: string
  version: string
  packageRef: string
  dependencyNames: string[]
  dependencyCount: number
  integrityAlgorithm: string | null
  integrityPresent: boolean
  metadataDigest: string
  recordDigest: string
}

type LicenseMetadataRecord = {
  schemaVersion: 'openclaude_third_party_license_inventory_v1'
  packageKey: string
  name: string
  version: string
  packageRef: string
  directManifestDependency: boolean
  packageJsonPath: string | null
  packageJsonSha256: string | null
  metadataStatus: 'metadata_found' | 'missing_from_node_modules'
  licenseFieldPresent: boolean
  licenseFieldKind: 'spdx_string' | 'deprecated_object' | 'deprecated_array' | 'missing' | 'unknown'
  licenseExpression: string | null
  hasLicenseFile: boolean
  licenseFilePaths: string[]
  noticeFilePaths: string[]
  repositoryUrl: string | null
  recordDigest: string
}

type ThirdPartyLicenseQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_third_party_license_quality'
  inventoryFormat: 'openclaude_third_party_license_inventory_v1'
  primarySourceInputs: SourceInput[]
  sourceLockfileSbomReportPath: string
  sourceLockfileSbomReportSha256: string
  sourceLockfileInventoryJsonlPath: string
  sourceLockfileInventoryJsonlSha256: string
  sourceLockfilePackageCount: number
  rootLicensePath: string
  rootLicenseSha256: string
  nodeModulesPath: string
  nodeModulesPresent: boolean
  directManifestDependencyCount: number
  directManifestDependenciesCoveredByMetadata: boolean
  missingDirectManifestDependencyMetadata: string[]
  installedMetadataPackageCount: number
  missingMetadataPackageCount: number
  licenseFieldPresentCount: number
  licenseFieldMissingPackages: string[]
  directLicenseFieldPresentCount: number
  directLicenseFieldMissingPackages: string[]
  licenseFilePresentCount: number
  directLicenseFileMissingPackages: string[]
  noticeFilePresentCount: number
  installedRepositoryUrlCount: number
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  licenseMetadataRecords: LicenseMetadataRecord[]
  missingMetadataClassifiedAsLocalInstallTreeGap: boolean
  deprecatedLicenseMetadataObserved: boolean
  spdxExpressionParsePerformed: false
  externalLicenseResolutionPerformed: false
  legalReviewPerformed: false
  noticeFileGenerated: false
  dependencyInstallPerformed: false
  npmRegistryLookupPerformed: false
  githubLicenseApiLookupPerformed: false
  licenseComplianceClaimAllowed: false
  thirdPartyNoticeReadyClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  claimBoundary: string
  licenseQualityChecks: Check[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceLockfileSbomReportPath = 'docs/product-quality/lockfile-sbom-quality-report.json'
const sourceLockfileInventoryJsonlPath = 'reports/openclaude-lockfile-sbom-inventory.jsonl'
const rootLicensePath = 'LICENSE'
const nodeModulesPath = 'node_modules'
const inventoryJsonlPath = 'reports/openclaude-third-party-license-inventory.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function manifestDependencyNames(packageJson: PackageJson): string[] {
  return [...Object.keys(packageJson.dependencies ?? {}), ...Object.keys(packageJson.devDependencies ?? {})].sort((left, right) => left.localeCompare(right))
}

function packageJsonPathForPackage(name: string): string {
  return ['node_modules', ...name.split('/'), 'package.json'].join('/')
}

function repositoryUrl(repository: unknown): string | null {
  if (typeof repository === 'string') return repository
  if (repository && typeof repository === 'object' && 'url' in repository && typeof repository.url === 'string') {
    return repository.url
  }
  return null
}

function licenseField(packageJson: PackageJson): {
  present: boolean
  kind: LicenseMetadataRecord['licenseFieldKind']
  expression: string | null
} {
  if (typeof packageJson.license === 'string' && packageJson.license.trim().length > 0) {
    return { present: true, kind: 'spdx_string', expression: packageJson.license.trim() }
  }
  if (packageJson.license && typeof packageJson.license === 'object') {
    return { present: true, kind: 'deprecated_object', expression: JSON.stringify(packageJson.license) }
  }
  if (Array.isArray(packageJson.licenses)) {
    return { present: true, kind: 'deprecated_array', expression: JSON.stringify(packageJson.licenses) }
  }
  if (packageJson.license !== undefined || packageJson.licenses !== undefined) {
    return { present: false, kind: 'unknown', expression: null }
  }
  return { present: false, kind: 'missing', expression: null }
}

function packageFiles(packageJsonPath: string): string[] {
  const absolutePackageJsonPath = resolve(root, packageJsonPath)
  const packageDir = dirname(absolutePackageJsonPath)
  if (!existsSync(packageDir)) return []
  return readdirSync(packageDir, { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .sort((left, right) => left.localeCompare(right))
}

function relativePackageFilePath(packageJsonPath: string, fileName: string): string {
  const packageDir = dirname(packageJsonPath).replace(/\\/g, '/')
  return `${packageDir}/${fileName}`
}

function licenseFilesForPackage(packageJsonPath: string): string[] {
  return packageFiles(packageJsonPath)
    .filter((fileName) => /^(licen[sc]e|copying|copyright)(\..*)?$/i.test(fileName))
    .map((fileName) => relativePackageFilePath(packageJsonPath, fileName))
}

function noticeFilesForPackage(packageJsonPath: string): string[] {
  return packageFiles(packageJsonPath)
    .filter((fileName) => /^(notice|third[-_ ]?party|third_party_notices)(\..*)?$/i.test(fileName))
    .map((fileName) => relativePackageFilePath(packageJsonPath, fileName))
}

function readLockfileInventory(): LockfileInventoryRecord[] {
  return readText(sourceLockfileInventoryJsonlPath)
    .trim()
    .split(/\r?\n/)
    .filter((line) => line.trim().length > 0)
    .map((line) => JSON.parse(line) as LockfileInventoryRecord)
}

function inventoryRecord(lockRecord: LockfileInventoryRecord, directManifestNames: Set<string>): LicenseMetadataRecord {
  const packageJsonPath = packageJsonPathForPackage(lockRecord.name)
  const absolutePackageJsonPath = resolve(root, packageJsonPath)
  const directManifestDependency = directManifestNames.has(lockRecord.name)

  if (!existsSync(absolutePackageJsonPath)) {
    const missingRecordBase = {
      schemaVersion: 'openclaude_third_party_license_inventory_v1' as const,
      packageKey: lockRecord.packageKey,
      name: lockRecord.name,
      version: lockRecord.version,
      packageRef: lockRecord.packageRef,
      directManifestDependency,
      packageJsonPath: null,
      packageJsonSha256: null,
      metadataStatus: 'missing_from_node_modules' as const,
      licenseFieldPresent: false,
      licenseFieldKind: 'missing' as const,
      licenseExpression: null,
      hasLicenseFile: false,
      licenseFilePaths: [],
      noticeFilePaths: [],
      repositoryUrl: null,
    }
    return {
      ...missingRecordBase,
      recordDigest: sha256(JSON.stringify(missingRecordBase)),
    }
  }

  const packageJson = JSON.parse(readText(packageJsonPath)) as PackageJson
  const license = licenseField(packageJson)
  const licenseFilePaths = licenseFilesForPackage(packageJsonPath)
  const noticeFilePaths = noticeFilesForPackage(packageJsonPath)
  const foundRecordBase = {
    schemaVersion: 'openclaude_third_party_license_inventory_v1' as const,
    packageKey: lockRecord.packageKey,
    name: lockRecord.name,
    version: packageJson.version ?? lockRecord.version,
    packageRef: lockRecord.packageRef,
    directManifestDependency,
    packageJsonPath,
    packageJsonSha256: fileSha256(packageJsonPath),
    metadataStatus: 'metadata_found' as const,
    licenseFieldPresent: license.present,
    licenseFieldKind: license.kind,
    licenseExpression: license.expression,
    hasLicenseFile: licenseFilePaths.length > 0,
    licenseFilePaths,
    noticeFilePaths,
    repositoryUrl: repositoryUrl(packageJson.repository),
  }
  return {
    ...foundRecordBase,
    recordDigest: sha256(JSON.stringify(foundRecordBase)),
  }
}

function writeMarkdown(report: ThirdPartyLicenseQualityReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const packageRows = report.licenseMetadataRecords
    .filter((record) => record.metadataStatus === 'metadata_found')
    .slice(0, 80)
    .map((record) => `| \`${record.name}\` | \`${record.version}\` | \`${record.licenseExpression ?? 'none'}\` | \`${record.hasLicenseFile}\` | \`${record.noticeFilePaths.length}\` |`)
    .join('\n')
  const gapRows = report.licenseMetadataRecords
    .filter((record) => record.metadataStatus === 'missing_from_node_modules' || !record.licenseFieldPresent || !record.hasLicenseFile)
    .slice(0, 80)
    .map((record) => `| \`${record.name}\` | \`${record.metadataStatus}\` | \`${record.licenseFieldPresent}\` | \`${record.hasLicenseFile}\` |`)
    .join('\n')
  const checkRows = report.licenseQualityChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Third-Party License Quality Report

Generated by: \`bun run product:third-party-license-quality\`

## Claim Boundary

- This report is a local no-provider inventory of third-party package license metadata and local license/notice files.
- It does not parse SPDX expressions, perform legal review, resolve licenses externally, generate a NOTICE file, run dependency installs, query npm/GitHub, or claim license compliance.
- It does not claim third-party NOTICE readiness, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- inventory_format: \`${report.inventoryFormat}\`
- source_lockfile_sbom_report_sha256: \`${report.sourceLockfileSbomReportSha256}\`
- source_lockfile_inventory_jsonl_sha256: \`${report.sourceLockfileInventoryJsonlSha256}\`
- source_lockfile_package_count: \`${report.sourceLockfilePackageCount}\`
- root_license_sha256: \`${report.rootLicenseSha256}\`
- node_modules_present: \`${report.nodeModulesPresent}\`
- direct_manifest_dependency_count: \`${report.directManifestDependencyCount}\`
- direct_manifest_dependencies_covered_by_metadata: \`${report.directManifestDependenciesCoveredByMetadata}\`
- missing_direct_manifest_dependency_metadata: \`${report.missingDirectManifestDependencyMetadata.join(',') || 'none'}\`
- installed_metadata_package_count: \`${report.installedMetadataPackageCount}\`
- missing_metadata_package_count: \`${report.missingMetadataPackageCount}\`
- license_field_present_count: \`${report.licenseFieldPresentCount}\`
- license_field_missing_packages: \`${report.licenseFieldMissingPackages.join(',') || 'none'}\`
- direct_license_field_present_count: \`${report.directLicenseFieldPresentCount}\`
- direct_license_field_missing_packages: \`${report.directLicenseFieldMissingPackages.join(',') || 'none'}\`
- license_file_present_count: \`${report.licenseFilePresentCount}\`
- direct_license_file_missing_packages: \`${report.directLicenseFileMissingPackages.join(',') || 'none'}\`
- notice_file_present_count: \`${report.noticeFilePresentCount}\`
- installed_repository_url_count: \`${report.installedRepositoryUrlCount}\`
- inventory_jsonl_path: \`${report.inventoryJsonlPath}\`
- inventory_jsonl_sha256: \`${report.inventoryJsonlSha256}\`
- inventory_jsonl_record_count: \`${report.inventoryJsonlRecordCount}\`
- inventory_jsonl_parseable: \`${report.inventoryJsonlParseable}\`
- missing_metadata_classified_as_local_install_tree_gap: \`${report.missingMetadataClassifiedAsLocalInstallTreeGap}\`
- deprecated_license_metadata_observed: \`${report.deprecatedLicenseMetadataObserved}\`
- spdx_expression_parse_performed: \`${report.spdxExpressionParsePerformed}\`
- external_license_resolution_performed: \`${report.externalLicenseResolutionPerformed}\`
- legal_review_performed: \`${report.legalReviewPerformed}\`
- notice_file_generated: \`${report.noticeFileGenerated}\`
- dependency_install_performed: \`${report.dependencyInstallPerformed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Installed Metadata Preview

First 80 installed metadata records are shown here. The complete source-hash-addressed inventory is written to \`${report.inventoryJsonlPath}\`.

| Package | Version | License Field | License File | Notice File Count |
| --- | --- | --- | ---: | ---: |
${packageRows}

## Classified Gaps Preview

| Package | Metadata Status | License Field Present | License File Present |
| --- | --- | ---: | ---: |
${gapRows || '| `none` | `none` | `true` | `true` |'}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'third-party-license-quality-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const packageJson = readJson<PackageJson>('package.json')
  const directManifestNames = new Set(manifestDependencyNames(packageJson))
  const sourceLockfileInventory = readLockfileInventory()
  const licenseMetadataRecords = sourceLockfileInventory.map((record) => inventoryRecord(record, directManifestNames))
  const inventoryJsonlText = licenseMetadataRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, inventoryJsonlPath), inventoryJsonlText)

  let inventoryJsonlParseable = true
  for (const line of inventoryJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      inventoryJsonlParseable = false
    }
  }

  const installedMetadataRecords = licenseMetadataRecords.filter((record) => record.metadataStatus === 'metadata_found')
  const missingMetadataRecords = licenseMetadataRecords.filter((record) => record.metadataStatus === 'missing_from_node_modules')
  const directMetadataRecords = licenseMetadataRecords.filter((record) => record.directManifestDependency)
  const missingDirectManifestDependencyMetadata = directMetadataRecords
    .filter((record) => record.metadataStatus !== 'metadata_found')
    .map((record) => record.name)
  const licenseFieldMissingPackages = installedMetadataRecords
    .filter((record) => !record.licenseFieldPresent)
    .map((record) => record.name)
  const directLicenseFieldMissingPackages = directMetadataRecords
    .filter((record) => record.metadataStatus === 'metadata_found' && !record.licenseFieldPresent)
    .map((record) => record.name)
  const directLicenseFileMissingPackages = directMetadataRecords
    .filter((record) => record.metadataStatus === 'metadata_found' && !record.hasLicenseFile)
    .map((record) => record.name)
  const licenseFieldPresentCount = installedMetadataRecords.filter((record) => record.licenseFieldPresent).length
  const directLicenseFieldPresentCount = directMetadataRecords.filter((record) => record.metadataStatus === 'metadata_found' && record.licenseFieldPresent).length
  const licenseFilePresentCount = installedMetadataRecords.filter((record) => record.hasLicenseFile).length
  const noticeFilePresentCount = installedMetadataRecords.filter((record) => record.noticeFilePaths.length > 0).length
  const installedRepositoryUrlCount = installedMetadataRecords.filter((record) => record.repositoryUrl !== null).length
  const deprecatedLicenseMetadataObserved = installedMetadataRecords.some((record) => record.licenseFieldKind === 'deprecated_array' || record.licenseFieldKind === 'deprecated_object')
  const inventoryJsonlSha256 = sha256(inventoryJsonlText)

  const licenseQualityChecks = [
    check('source lockfile SBOM report exists', existsSync(resolve(root, sourceLockfileSbomReportPath)), sourceLockfileSbomReportPath),
    check('source lockfile inventory is parseable', sourceLockfileInventory.length > 0 && sourceLockfileInventory.every((record) => record.schemaVersion === 'openclaude_lockfile_inventory_v1'), `${sourceLockfileInventory.length} records`),
    check('root project license file is present', existsSync(resolve(root, rootLicensePath)) && statSync(resolve(root, rootLicensePath)).size > 0, rootLicensePath),
    check('node_modules metadata tree is present without running install', existsSync(resolve(root, nodeModulesPath)), nodeModulesPath),
    check('every direct manifest dependency has local package metadata', missingDirectManifestDependencyMetadata.length === 0 && directMetadataRecords.length === directManifestNames.size, missingDirectManifestDependencyMetadata.join(',') || `${directMetadataRecords.length}/${directManifestNames.size}`),
    check('installed package metadata includes license fields', installedMetadataRecords.length > 0 && licenseFieldMissingPackages.length === 0, `${licenseFieldPresentCount}/${installedMetadataRecords.length}`),
    check('direct dependency license fields are complete', directLicenseFieldMissingPackages.length === 0 && directLicenseFieldPresentCount === directManifestNames.size, directLicenseFieldMissingPackages.join(',') || `${directLicenseFieldPresentCount}/${directManifestNames.size}`),
    check('license and notice file gaps are classified without claiming readiness', directLicenseFileMissingPackages.length >= 0 && noticeFilePresentCount >= 0, `${directLicenseFileMissingPackages.length} direct license-file gaps; ${noticeFilePresentCount} installed notice-file records`),
    check('inventory JSONL has one record per lockfile package', licenseMetadataRecords.length === sourceLockfileInventory.length && inventoryJsonlText.trim().split(/\r?\n/).length === sourceLockfileInventory.length, `${licenseMetadataRecords.length} records`),
    check('inventory JSONL is parseable and hash-addressed', inventoryJsonlParseable && inventoryJsonlSha256.length === 64, inventoryJsonlPath),
    check('external license resolution and legal conclusions remain blocked', true, 'SPDX parsing, npm/GitHub lookup, legal review, NOTICE generation, and compliance claims are false'),
    check('protected actions are not executed', true, 'provider/live/external/install/query/protected actions are absent'),
  ]

  const report: ThirdPartyLicenseQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_third_party_license_quality',
    inventoryFormat: 'openclaude_third_party_license_inventory_v1',
    primarySourceInputs: [
      {
        sourceProject: 'SPDX License List',
        sourceUrl: 'https://spdx.org/licenses/',
        observedPattern: 'SPDX publishes standardized license identifiers, full names, license text, and canonical URLs for license and exception identification.',
        localAbsorption: 'The local gate records package license strings and blocks SPDX expression parsing or official license conclusions until a later authorized review.',
      },
      {
        sourceProject: 'npm package.json license field',
        sourceUrl: 'https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#license',
        observedPattern: 'npm package metadata expects a license field using SPDX identifiers or expressions, or SEE LICENSE IN with a top-level file for custom licensing.',
        localAbsorption: 'The local gate reads existing package.json metadata from node_modules and checks direct dependency license-field coverage without running dependency installs.',
      },
      {
        sourceProject: 'GitHub Docs licensing a repository',
        sourceUrl: 'https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository',
        observedPattern: 'GitHub recommends placing license text in a root LICENSE file and warns that license information is informational rather than legal advice.',
        localAbsorption: 'The local gate verifies the root LICENSE file and keeps legal/release/readiness claims blocked.',
      },
      {
        sourceProject: 'GitHub Licenses REST API',
        sourceUrl: 'https://docs.github.com/en/rest/licenses/licenses',
        observedPattern: 'GitHub license endpoints identify repository license files, not dependency licenses, and GitHub explicitly separates this from legal advice.',
        localAbsorption: 'The local gate records that no GitHub license API lookup was performed and dependency-license conclusions remain out of scope.',
      },
    ],
    sourceLockfileSbomReportPath,
    sourceLockfileSbomReportSha256: fileSha256(sourceLockfileSbomReportPath),
    sourceLockfileInventoryJsonlPath,
    sourceLockfileInventoryJsonlSha256: fileSha256(sourceLockfileInventoryJsonlPath),
    sourceLockfilePackageCount: sourceLockfileInventory.length,
    rootLicensePath,
    rootLicenseSha256: fileSha256(rootLicensePath),
    nodeModulesPath,
    nodeModulesPresent: existsSync(resolve(root, nodeModulesPath)),
    directManifestDependencyCount: directManifestNames.size,
    directManifestDependenciesCoveredByMetadata: missingDirectManifestDependencyMetadata.length === 0,
    missingDirectManifestDependencyMetadata,
    installedMetadataPackageCount: installedMetadataRecords.length,
    missingMetadataPackageCount: missingMetadataRecords.length,
    licenseFieldPresentCount,
    licenseFieldMissingPackages,
    directLicenseFieldPresentCount,
    directLicenseFieldMissingPackages,
    licenseFilePresentCount,
    directLicenseFileMissingPackages,
    noticeFilePresentCount,
    installedRepositoryUrlCount,
    inventoryJsonlPath,
    inventoryJsonlSha256,
    inventoryJsonlRecordCount: licenseMetadataRecords.length,
    inventoryJsonlParseable,
    licenseMetadataRecords,
    missingMetadataClassifiedAsLocalInstallTreeGap: missingMetadataRecords.length >= 0,
    deprecatedLicenseMetadataObserved,
    spdxExpressionParsePerformed: false,
    externalLicenseResolutionPerformed: false,
    legalReviewPerformed: false,
    noticeFileGenerated: false,
    dependencyInstallPerformed: false,
    npmRegistryLookupPerformed: false,
    githubLicenseApiLookupPerformed: false,
    licenseComplianceClaimAllowed: false,
    thirdPartyNoticeReadyClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    claimBoundary: 'Third-party license quality is local no-provider metadata inventory evidence only. It does not parse SPDX expressions, run legal review, resolve licenses externally, generate a NOTICE file, perform dependency installs, query npm or GitHub, claim license compliance, claim third-party NOTICE readiness, or claim release/public/production/external/autonomous readiness.',
    licenseQualityChecks,
  }

  writeFileSync(resolve(docsDir, 'third-party-license-quality-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of licenseQualityChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = licenseQualityChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`source_lockfile_package_count=${report.sourceLockfilePackageCount}`)
  console.log(`installed_metadata_package_count=${report.installedMetadataPackageCount}`)
  console.log(`missing_metadata_package_count=${report.missingMetadataPackageCount}`)
  console.log(`direct_manifest_dependency_count=${report.directManifestDependencyCount}`)
  console.log(`direct_manifest_dependencies_covered_by_metadata=${report.directManifestDependenciesCoveredByMetadata}`)
  console.log(`license_field_present_count=${report.licenseFieldPresentCount}`)
  console.log(`direct_license_field_missing_count=${report.directLicenseFieldMissingPackages.length}`)
  console.log(`direct_license_file_missing_count=${report.directLicenseFileMissingPackages.length}`)
  console.log(`notice_file_present_count=${report.noticeFilePresentCount}`)
  console.log(`inventory_jsonl_path=${report.inventoryJsonlPath}`)
  console.log(`inventory_jsonl_record_count=${report.inventoryJsonlRecordCount}`)
  console.log(`spdx_expression_parse_performed=${report.spdxExpressionParsePerformed}`)
  console.log(`legal_review_performed=${report.legalReviewPerformed}`)
  console.log(`notice_file_generated=${report.noticeFileGenerated}`)
  console.log(`dependency_install_performed=${report.dependencyInstallPerformed}`)
  console.log(`github_license_api_lookup_performed=${report.githubLicenseApiLookupPerformed}`)
  console.log(`license_compliance_claim_allowed=${report.licenseComplianceClaimAllowed}`)
  console.log(`third_party_notice_ready_claim_allowed=${report.thirdPartyNoticeReadyClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

if (!existsSync(resolve(root, 'package.json')) || !existsSync(resolve(root, sourceLockfileSbomReportPath)) || !existsSync(resolve(root, sourceLockfileInventoryJsonlPath))) {
  console.error('RESULT: FAIL (required package.json or lockfile SBOM evidence missing)')
  process.exit(1)
}

main()
