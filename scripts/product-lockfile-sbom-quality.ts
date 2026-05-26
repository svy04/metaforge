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

type PackageJson = {
  name?: string
  version?: string
  packageManager?: string
  dependencies?: Record<string, string>
  devDependencies?: Record<string, string>
}

type LockfilePackageRecord = {
  packageKey: string
  packageRef: string
  name: string
  version: string
  dependencyNames: string[]
  integrityAlgorithm: string | null
  integrityPresent: boolean
  metadataDigest: string
  recordDigest: string
}

type LockfileRelationshipRecord = {
  from: string
  to: string
  relationshipType: 'declares_dependency'
}

type InventoryJsonlRecord = {
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

type LockfileSbomQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_lockfile_sbom_quality'
  inventoryFormat: 'openclaude_lockfile_inventory_v1'
  primarySourceInputs: SourceInput[]
  packageJsonPath: string
  packageJsonSha256: string
  bunLockPath: string
  bunLockSha256: string
  bunLockSizeBytes: number
  bunLockTextStructureRecognized: boolean
  bunLockfileVersion: number | null
  rootWorkspaceDependencyCount: number
  rootWorkspaceDevDependencyCount: number
  directManifestDependencyCount: number
  lockfilePackageCount: number
  lockfilePackageCountExceedsDirectDependencies: boolean
  packagesWithIntegrityCount: number
  packagesMissingIntegrity: string[]
  packagesWithDependencyMetadataCount: number
  lockfileRelationshipCount: number
  directManifestDependenciesCovered: boolean
  missingDirectManifestDependencies: string[]
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  lockfilePackageRecords: LockfilePackageRecord[]
  lockfileRelationshipRecords: LockfileRelationshipRecord[]
  githubDependencyGraphExportPerformed: false
  externalSbomExportPerformed: false
  hostedSbomValidationPerformed: false
  vulnerabilityScanPerformed: false
  licenseConclusionPerformed: false
  officialCycloneDxComplianceClaimAllowed: false
  officialSpdxComplianceClaimAllowed: false
  githubDependencyGraphParityClaimAllowed: false
  vulnerabilityFreeClaimAllowed: false
  licenseComplianceClaimAllowed: false
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
  sbomQualityChecks: Check[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const packageJsonPath = 'package.json'
const bunLockPath = 'bun.lock'
const inventoryJsonlPath = 'reports/openclaude-lockfile-sbom-inventory.jsonl'

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function fileSha256(path: string): string {
  return sha256(readFileSync(resolve(root, path)))
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function lockfileVersion(lockText: string): number | null {
  const match = lockText.match(/"lockfileVersion":\s*(\d+)/)
  return match ? Number(match[1]) : null
}

function hasRootWorkspace(lockText: string): boolean {
  return /"workspaces":\s*\{\s*"":\s*\{/.test(lockText)
}

function rootWorkspaceSection(lockText: string): string {
  const workspaceMatch = lockText.match(/"workspaces":\s*\{\s*"":\s*\{([\s\S]*?)\n\s{4}\},\n\s{2}\},/)
  return workspaceMatch?.[1] ?? ''
}

function countRootWorkspaceDependencies(section: string, field: 'dependencies' | 'devDependencies'): number {
  const match = section.match(new RegExp(`"${field}":\\s*\\{([\\s\\S]*?)\\n\\s{6}\\}`, 'm'))
  if (!match) return 0
  return [...match[1].matchAll(/^\s{8}"(?:\\.|[^"\\])+":\s*"(?:\\.|[^"\\])*",?\s*$/gm)].length
}

function manifestDependencyNames(packageJson: PackageJson): string[] {
  return [...Object.keys(packageJson.dependencies ?? {}), ...Object.keys(packageJson.devDependencies ?? {})].sort((left, right) => left.localeCompare(right))
}

function decodeLockString(raw: string): string {
  return JSON.parse(`"${raw}"`) as string
}

function versionFromPackageRef(packageKey: string, packageRef: string): string {
  const expectedPrefix = `${packageKey}@`
  if (packageRef.startsWith(expectedPrefix)) {
    return packageRef.slice(expectedPrefix.length)
  }
  const splitIndex = packageRef.lastIndexOf('@')
  return splitIndex > 0 ? packageRef.slice(splitIndex + 1) : packageRef
}

function dependencyNamesFromMetadata(metadataText: string): string[] {
  const dependencyNames = new Set<string>()
  const blockPattern = /"(dependencies|optionalDependencies|peerDependencies)":\s*\{([^}]*)\}/g
  for (const blockMatch of metadataText.matchAll(blockPattern)) {
    const entries = blockMatch[2]
    for (const entryMatch of entries.matchAll(/"((?:\\.|[^"\\])+)":\s*"(?:\\.|[^"\\])*"/g)) {
      dependencyNames.add(decodeLockString(entryMatch[1]))
    }
  }
  return [...dependencyNames].sort((left, right) => left.localeCompare(right))
}

function integrityAlgorithm(integrity: string): string | null {
  const match = integrity.match(/^([a-z0-9]+)-/i)
  return match?.[1].toLowerCase() ?? null
}

function parseLockfilePackages(lockText: string): LockfilePackageRecord[] {
  const records: LockfilePackageRecord[] = []
  let inPackages = false

  for (const line of lockText.split(/\r?\n/)) {
    if (!inPackages && /^\s{2}"packages":\s*\{\s*$/.test(line)) {
      inPackages = true
      continue
    }
    if (inPackages && /^\s{2}\},?\s*$/.test(line)) {
      break
    }
    if (!inPackages || line.trim() === '') {
      continue
    }

    const match = line.match(/^\s{4}"((?:\\.|[^"\\])+)":\s*\["((?:\\.|[^"\\])*)",\s*"((?:\\.|[^"\\])*)",\s*(.*),\s*"((?:\\.|[^"\\])*)"\],?\s*$/)
    if (!match) {
      continue
    }

    const packageKey = decodeLockString(match[1])
    const packageRef = decodeLockString(match[2])
    const metadataText = match[4]
    const integrity = decodeLockString(match[5])
    const dependencyNames = dependencyNamesFromMetadata(metadataText)
    const recordBase = {
      packageKey,
      packageRef,
      name: packageKey,
      version: versionFromPackageRef(packageKey, packageRef),
      dependencyNames,
      integrityAlgorithm: integrityAlgorithm(integrity),
      integrityPresent: integrity.length > 0,
      metadataDigest: sha256(metadataText),
    }

    records.push({
      ...recordBase,
      recordDigest: sha256(JSON.stringify(recordBase)),
    })
  }

  return records.sort((left, right) => left.packageKey.localeCompare(right.packageKey))
}

function relationshipRecords(packages: LockfilePackageRecord[]): LockfileRelationshipRecord[] {
  const packageNames = new Set(packages.map((record) => record.name))
  const relationships: LockfileRelationshipRecord[] = []
  for (const record of packages) {
    for (const dependencyName of record.dependencyNames) {
      relationships.push({
        from: record.name,
        to: packageNames.has(dependencyName) ? dependencyName : `${dependencyName} (not materialized as package entry)`,
        relationshipType: 'declares_dependency',
      })
    }
  }
  return relationships.sort((left, right) => `${left.from}->${left.to}`.localeCompare(`${right.from}->${right.to}`))
}

function inventoryRecord(record: LockfilePackageRecord): InventoryJsonlRecord {
  return {
    schemaVersion: 'openclaude_lockfile_inventory_v1',
    packageKey: record.packageKey,
    name: record.name,
    version: record.version,
    packageRef: record.packageRef,
    dependencyNames: record.dependencyNames,
    dependencyCount: record.dependencyNames.length,
    integrityAlgorithm: record.integrityAlgorithm,
    integrityPresent: record.integrityPresent,
    metadataDigest: record.metadataDigest,
    recordDigest: record.recordDigest,
  }
}

function writeMarkdown(report: LockfileSbomQualityReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const packageRows = report.lockfilePackageRecords
    .slice(0, 80)
    .map((record) => `| \`${record.name}\` | \`${record.version}\` | \`${record.dependencyNames.length}\` | \`${record.integrityAlgorithm ?? 'none'}\` |`)
    .join('\n')
  const checkRows = report.sbomQualityChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Lockfile SBOM Quality Report

Generated by: \`bun run product:lockfile-sbom-quality\`

## Claim Boundary

- This report is a local no-provider lockfile inventory and SBOM-shaped evidence package.
- It does not claim official CycloneDX compliance, official SPDX compliance, GitHub Dependency Graph parity, vulnerability-free status, license compliance, release readiness, production readiness, public readiness, external validation, or autonomous reliability.
- It does not call GitHub APIs, export hosted SBOMs, run hosted validation, run installs, run audits, call providers, call live models, or call external services.

## Summary

- mode: \`${report.mode}\`
- inventory_format: \`${report.inventoryFormat}\`
- package_json_sha256: \`${report.packageJsonSha256}\`
- bun_lock_sha256: \`${report.bunLockSha256}\`
- bun_lock_size_bytes: \`${report.bunLockSizeBytes}\`
- bun_lock_text_structure_recognized: \`${report.bunLockTextStructureRecognized}\`
- bun_lockfile_version: \`${report.bunLockfileVersion ?? 'null'}\`
- root_workspace_dependency_count: \`${report.rootWorkspaceDependencyCount}\`
- root_workspace_dev_dependency_count: \`${report.rootWorkspaceDevDependencyCount}\`
- direct_manifest_dependency_count: \`${report.directManifestDependencyCount}\`
- lockfile_package_count: \`${report.lockfilePackageCount}\`
- packages_with_integrity_count: \`${report.packagesWithIntegrityCount}\`
- packages_missing_integrity: \`${report.packagesMissingIntegrity.join(',') || 'none'}\`
- packages_with_dependency_metadata_count: \`${report.packagesWithDependencyMetadataCount}\`
- lockfile_relationship_count: \`${report.lockfileRelationshipCount}\`
- direct_manifest_dependencies_covered: \`${report.directManifestDependenciesCovered}\`
- missing_direct_manifest_dependencies: \`${report.missingDirectManifestDependencies.join(',') || 'none'}\`
- inventory_jsonl_path: \`${report.inventoryJsonlPath}\`
- inventory_jsonl_sha256: \`${report.inventoryJsonlSha256}\`
- inventory_jsonl_record_count: \`${report.inventoryJsonlRecordCount}\`
- inventory_jsonl_parseable: \`${report.inventoryJsonlParseable}\`
- github_dependency_graph_export_performed: \`${report.githubDependencyGraphExportPerformed}\`
- external_sbom_export_performed: \`${report.externalSbomExportPerformed}\`
- hosted_sbom_validation_performed: \`${report.hostedSbomValidationPerformed}\`
- vulnerability_scan_performed: \`${report.vulnerabilityScanPerformed}\`
- license_conclusion_performed: \`${report.licenseConclusionPerformed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Lockfile Inventory Preview

First 80 package records are shown here. The complete source-hash-addressed inventory is written to \`${report.inventoryJsonlPath}\`.

| Package | Version | Dependency Count | Integrity Algorithm |
| --- | --- | ---: | --- |
${packageRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'lockfile-sbom-quality-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const packageJson = readJson<PackageJson>(packageJsonPath)
  const lockText = readText(bunLockPath)
  const workspaceSection = rootWorkspaceSection(lockText)
  const rootWorkspaceDependencyCount = countRootWorkspaceDependencies(workspaceSection, 'dependencies')
  const rootWorkspaceDevDependencyCount = countRootWorkspaceDependencies(workspaceSection, 'devDependencies')
  const directManifestNames = manifestDependencyNames(packageJson)
  const lockfilePackageRecords = parseLockfilePackages(lockText)
  const lockfilePackageNames = new Set(lockfilePackageRecords.map((record) => record.name))
  const missingDirectManifestDependencies = directManifestNames.filter((name) => !lockfilePackageNames.has(name))
  const lockfileRelationshipRecords = relationshipRecords(lockfilePackageRecords)
  const inventoryRecords = lockfilePackageRecords.map(inventoryRecord)
  const inventoryJsonlText = inventoryRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, inventoryJsonlPath), inventoryJsonlText)

  let inventoryJsonlParseable = true
  for (const line of inventoryJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      inventoryJsonlParseable = false
    }
  }

  const bunLockfileVersion = lockfileVersion(lockText)
  const packagesMissingIntegrity = lockfilePackageRecords.filter((record) => !record.integrityPresent).map((record) => record.name)
  const packagesWithIntegrityCount = lockfilePackageRecords.filter((record) => record.integrityPresent).length
  const packagesWithDependencyMetadataCount = lockfilePackageRecords.filter((record) => record.dependencyNames.length > 0).length
  const inventoryJsonlSha256 = sha256(inventoryJsonlText)
  const bunLockTextStructureRecognized = hasRootWorkspace(lockText) && bunLockfileVersion === 1 && lockfilePackageRecords.length > 0

  const sbomQualityChecks = [
    check('Bun text lockfile structure is recognized', bunLockTextStructureRecognized, `${lockfilePackageRecords.length} package entries`),
    check('lockfile version is current expected local format', bunLockfileVersion === 1, `${bunLockfileVersion ?? 'missing'}`),
    check('root workspace dependencies match package manifest count', rootWorkspaceDependencyCount + rootWorkspaceDevDependencyCount === directManifestNames.length, `${rootWorkspaceDependencyCount}+${rootWorkspaceDevDependencyCount}/${directManifestNames.length}`),
    check('lockfile inventory covers every direct manifest dependency', missingDirectManifestDependencies.length === 0, missingDirectManifestDependencies.join(',') || 'all direct dependencies covered'),
    check('lockfile inventory captures transitive package surface', lockfilePackageRecords.length > directManifestNames.length, `${lockfilePackageRecords.length} packages > ${directManifestNames.length} direct`),
    check('lockfile package records include version and integrity metadata', lockfilePackageRecords.every((record) => record.version.length > 0 && record.integrityPresent && record.integrityAlgorithm === 'sha512'), `${packagesWithIntegrityCount}/${lockfilePackageRecords.length} with integrity`),
    check('lockfile dependency relationships are extracted', lockfileRelationshipRecords.length > directManifestNames.length && packagesWithDependencyMetadataCount > 0, `${lockfileRelationshipRecords.length} relationships`),
    check('inventory JSONL has one record per lockfile package', inventoryRecords.length === lockfilePackageRecords.length && inventoryJsonlText.trim().split(/\r?\n/).length === lockfilePackageRecords.length, `${inventoryRecords.length} records`),
    check('inventory JSONL is parseable and hash-addressed', inventoryJsonlParseable && inventoryJsonlSha256.length === 64, inventoryJsonlPath),
    check('official SBOM and hosted validation claims remain blocked', true, 'CycloneDX/SPDX/GitHub Dependency Graph parity flags are false'),
    check('protected actions are not executed', true, 'provider/live/external/install/audit/export actions are absent'),
  ]

  const report: LockfileSbomQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_lockfile_sbom_quality',
    inventoryFormat: 'openclaude_lockfile_inventory_v1',
    primarySourceInputs: [
      {
        sourceProject: 'Bun lockfile documentation',
        sourceUrl: 'https://bun.com/docs/pm/lockfile',
        observedPattern: 'Bun creates the source-controlled text lockfile bun.lock, and its lockfile should be committed as local dependency resolution evidence.',
        localAbsorption: 'The local gate reads existing bun.lock only, recognizes the text lockfile structure, and avoids running bun install or dependency installers.',
      },
      {
        sourceProject: 'CycloneDX specification overview',
        sourceUrl: 'https://cyclonedx.org/specification/overview/',
        observedPattern: 'A bill of materials represents component inventory plus direct and transitive dependency relationships as machine-readable evidence.',
        localAbsorption: 'The local gate writes an SBOM-shaped lockfile package inventory and relationship list while blocking official CycloneDX compliance claims.',
      },
      {
        sourceProject: 'SPDX specifications',
        sourceUrl: 'https://spdx.dev/use/specifications/',
        observedPattern: 'SPDX is an open standard for SBOM-style software package exchange, with current and previous document formats published as specifications.',
        localAbsorption: 'The local gate preserves package/version/integrity fields but does not claim official SPDX document compliance or license conclusions.',
      },
      {
        sourceProject: 'GitHub Dependency Graph SBOM API',
        sourceUrl: 'https://docs.github.com/en/rest/dependency-graph',
        observedPattern: 'GitHub exposes dependency graph and repository SBOM endpoints as hosted repository supply-chain evidence.',
        localAbsorption: 'The local gate records that no GitHub API or hosted SBOM export was performed, leaving hosted parity as a protected future boundary.',
      },
    ],
    packageJsonPath,
    packageJsonSha256: fileSha256(packageJsonPath),
    bunLockPath,
    bunLockSha256: fileSha256(bunLockPath),
    bunLockSizeBytes: statSync(resolve(root, bunLockPath)).size,
    bunLockTextStructureRecognized,
    bunLockfileVersion,
    rootWorkspaceDependencyCount,
    rootWorkspaceDevDependencyCount,
    directManifestDependencyCount: directManifestNames.length,
    lockfilePackageCount: lockfilePackageRecords.length,
    lockfilePackageCountExceedsDirectDependencies: lockfilePackageRecords.length > directManifestNames.length,
    packagesWithIntegrityCount,
    packagesMissingIntegrity,
    packagesWithDependencyMetadataCount,
    lockfileRelationshipCount: lockfileRelationshipRecords.length,
    directManifestDependenciesCovered: missingDirectManifestDependencies.length === 0,
    missingDirectManifestDependencies,
    inventoryJsonlPath,
    inventoryJsonlSha256,
    inventoryJsonlRecordCount: inventoryRecords.length,
    inventoryJsonlParseable,
    lockfilePackageRecords,
    lockfileRelationshipRecords,
    githubDependencyGraphExportPerformed: false,
    externalSbomExportPerformed: false,
    hostedSbomValidationPerformed: false,
    vulnerabilityScanPerformed: false,
    licenseConclusionPerformed: false,
    officialCycloneDxComplianceClaimAllowed: false,
    officialSpdxComplianceClaimAllowed: false,
    githubDependencyGraphParityClaimAllowed: false,
    vulnerabilityFreeClaimAllowed: false,
    licenseComplianceClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    claimBoundary: 'Lockfile SBOM quality is local no-provider inventory evidence only. It does not claim official SPDX/CycloneDX compliance, hosted SBOM export, dependency graph parity, vulnerability-free status, license compliance, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
    sbomQualityChecks,
  }

  writeFileSync(resolve(docsDir, 'lockfile-sbom-quality-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of sbomQualityChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = sbomQualityChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`lockfile_package_count=${report.lockfilePackageCount}`)
  console.log(`direct_manifest_dependency_count=${report.directManifestDependencyCount}`)
  console.log(`lockfile_relationship_count=${report.lockfileRelationshipCount}`)
  console.log(`inventory_jsonl_path=${report.inventoryJsonlPath}`)
  console.log(`inventory_jsonl_record_count=${report.inventoryJsonlRecordCount}`)
  console.log(`github_dependency_graph_export_performed=${report.githubDependencyGraphExportPerformed}`)
  console.log(`external_sbom_export_performed=${report.externalSbomExportPerformed}`)
  console.log(`official_cyclonedx_compliance_claim_allowed=${report.officialCycloneDxComplianceClaimAllowed}`)
  console.log(`official_spdx_compliance_claim_allowed=${report.officialSpdxComplianceClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)
}

if (!existsSync(resolve(root, packageJsonPath)) || !existsSync(resolve(root, bunLockPath))) {
  console.error('RESULT: FAIL (package.json or bun.lock missing)')
  process.exit(1)
}

main()
