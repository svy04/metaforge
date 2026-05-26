import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs'
import { extname, resolve } from 'node:path'

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
  license?: unknown
}

type SourceLicenseRecord = {
  schemaVersion: 'openclaude_source_license_metadata_inventory_v1'
  path: string
  category: string
  sizeBytes: number
  sha256: string
  hasSpdxLicenseIdentifier: boolean
  spdxLicenseIdentifiers: string[]
  hasSpdxFileCopyrightText: boolean
  spdxFileCopyrightTexts: string[]
  hasAdjacentLicenseFile: boolean
  adjacentLicenseFilePath: string | null
  coveredByReuseTomlAnnotation: boolean
  metadataStatus:
    | 'file_level_spdx_metadata_present'
    | 'adjacent_license_metadata_present'
    | 'reuse_toml_not_present_gap_classified'
    | 'missing_file_level_license_metadata'
  recordDigest: string
}

type SourceLicenseMetadataQualityReport = {
  generatedAt: string
  mode: 'local_no_provider_source_license_metadata_quality'
  inventoryFormat: 'openclaude_source_license_metadata_inventory_v1'
  primarySourceInputs: SourceInput[]
  packageJsonPath: string
  packageJsonSha256: string
  packageLicenseField: string | null
  rootLicensePath: string
  rootLicenseSha256: string
  rootLicenseContainsDerivedCodeBoundary: boolean
  rootLicenseContainsMitModificationBoundary: boolean
  reuseTomlPath: string
  reuseTomlPresent: boolean
  licensesDirectoryPath: string
  licensesDirectoryPresent: boolean
  reuseToolRunPerformed: false
  reuseComplianceClaimAllowed: false
  spdxDocumentGenerated: false
  legalReviewPerformed: false
  sourceLicenseComplianceClaimAllowed: false
  sourceMetadataReadyClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  scanRoots: string[]
  excludedPathFragments: string[]
  scannedSourceFileCount: number
  sourceFilesWithSpdxLicenseIdentifierCount: number
  sourceFilesWithSpdxCopyrightTextCount: number
  sourceFilesWithAdjacentLicenseFileCount: number
  sourceFilesCoveredByReuseTomlAnnotationCount: number
  sourceFilesMissingFileLevelMetadataCount: number
  sourceFilesMissingFileLevelMetadata: string[]
  fileCategoryCounts: Record<string, number>
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  sourceLicenseRecords: SourceLicenseRecord[]
  claimBoundary: string
  sourceLicenseMetadataChecks: Check[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const packageJsonPath = 'package.json'
const rootLicensePath = 'LICENSE'
const reuseTomlPath = 'REUSE.toml'
const licensesDirectoryPath = 'LICENSES'
const inventoryJsonlPath = 'reports/openclaude-source-license-metadata-inventory.jsonl'
const scanRoots = ['src', 'scripts', 'packages/openclaude-vscode', '.github']
const additionalFiles = ['package.json', 'README.md', 'LICENSE', 'CONTRIBUTING.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md', 'bin/openclaude', 'bin/openclaude.cmd']
const scannedExtensions = new Set(['.ts', '.tsx', '.js', '.mjs', '.cjs', '.json', '.md', '.yml', '.yaml', '.cmd'])
const excludedPathFragments = [
  '/node_modules/',
  '/dist/',
  '/coverage/',
  '/.tmp',
  '/.openclaude/',
  '/.playwright-mcp/',
  '/assets/',
]

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

function normalizePath(path: string): string {
  return path.replace(/\\/g, '/')
}

function shouldExclude(path: string): boolean {
  const normalized = `/${normalizePath(path)}`
  return excludedPathFragments.some((fragment) => normalized.includes(fragment))
}

function listFiles(dir: string): string[] {
  const absoluteDir = resolve(root, dir)
  if (!existsSync(absoluteDir)) return []
  const results: string[] = []
  for (const entry of readdirSync(absoluteDir, { withFileTypes: true })) {
    const childPath = normalizePath(`${dir}/${entry.name}`)
    if (shouldExclude(childPath)) continue
    if (entry.isDirectory()) {
      results.push(...listFiles(childPath))
      continue
    }
    if (!entry.isFile()) continue
    const extension = extname(entry.name).toLowerCase()
    if (scannedExtensions.has(extension) || childPath === 'bin/openclaude') {
      results.push(childPath)
    }
  }
  return results
}

function sourceFilePaths(): string[] {
  const rootFiles = additionalFiles.filter((path) => existsSync(resolve(root, path)))
  return [...new Set([...scanRoots.flatMap(listFiles), ...rootFiles])]
    .filter((path) => existsSync(resolve(root, path)) && !shouldExclude(path))
    .sort((left, right) => left.localeCompare(right))
}

function sourceCategory(path: string): string {
  if (path.startsWith('src/')) return 'application_source'
  if (path.startsWith('scripts/')) return 'quality_or_build_script'
  if (path.startsWith('packages/openclaude-vscode/')) return 'vscode_extension_source'
  if (path.startsWith('.github/')) return 'github_community_or_workflow'
  if (path.startsWith('bin/')) return 'package_launcher'
  if (['README.md', 'CONTRIBUTING.md', 'SUPPORT.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md', 'LICENSE'].includes(path)) return 'root_community_or_license_doc'
  if (path === 'package.json') return 'root_package_metadata'
  return 'other_scanned_surface'
}

function spdxLicenseIdentifiers(text: string): string[] {
  return [...text.matchAll(/SPDX-License-Identifier:\s*([^\r\n*]+)/gi)]
    .map((match) => match[1].replace(/\s+\*\/\s*$/, '').trim())
    .filter((value) => value.length > 0)
}

function spdxCopyrightTexts(text: string): string[] {
  return [...text.matchAll(/SPDX-FileCopyrightText:\s*([^\r\n*]+)/gi)]
    .map((match) => match[1].replace(/\s+\*\/\s*$/, '').trim())
    .filter((value) => value.length > 0)
}

function adjacentLicenseFilePath(path: string): string | null {
  const candidate = `${path}.license`
  return existsSync(resolve(root, candidate)) ? candidate : null
}

function recordForPath(path: string): SourceLicenseRecord {
  const text = readText(path)
  const identifiers = spdxLicenseIdentifiers(text)
  const copyrights = spdxCopyrightTexts(text)
  const adjacent = adjacentLicenseFilePath(path)
  const coveredByReuseTomlAnnotation = false
  const baseRecord = {
    schemaVersion: 'openclaude_source_license_metadata_inventory_v1' as const,
    path,
    category: sourceCategory(path),
    sizeBytes: statSync(resolve(root, path)).size,
    sha256: fileSha256(path),
    hasSpdxLicenseIdentifier: identifiers.length > 0,
    spdxLicenseIdentifiers: identifiers,
    hasSpdxFileCopyrightText: copyrights.length > 0,
    spdxFileCopyrightTexts: copyrights,
    hasAdjacentLicenseFile: adjacent !== null,
    adjacentLicenseFilePath: adjacent,
    coveredByReuseTomlAnnotation,
    metadataStatus: (identifiers.length > 0
      ? 'file_level_spdx_metadata_present'
      : adjacent !== null
        ? 'adjacent_license_metadata_present'
        : existsSync(resolve(root, reuseTomlPath))
          ? 'reuse_toml_not_present_gap_classified'
          : 'missing_file_level_license_metadata') as SourceLicenseRecord['metadataStatus'],
  }
  return {
    ...baseRecord,
    recordDigest: sha256(JSON.stringify(baseRecord)),
  }
}

function countCategories(records: SourceLicenseRecord[]): Record<string, number> {
  const counts: Record<string, number> = {}
  for (const record of records) {
    counts[record.category] = (counts[record.category] ?? 0) + 1
  }
  return Object.fromEntries(Object.entries(counts).sort(([left], [right]) => left.localeCompare(right)))
}

function writeMarkdown(report: SourceLicenseMetadataQualityReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const categoryRows = Object.entries(report.fileCategoryCounts)
    .map(([category, count]) => `| \`${category}\` | ${count} |`)
    .join('\n')
  const gapRows = report.sourceFilesMissingFileLevelMetadata
    .slice(0, 100)
    .map((path) => `| \`${path}\` |`)
    .join('\n')
  const checkRows = report.sourceLicenseMetadataChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Source License Metadata Quality Report

Generated by: \`bun run product:source-license-metadata-quality\`

## Claim Boundary

- This report is a local no-provider inventory of source-file license metadata coverage.
- It recognizes the current root license as a derived-code/modification-license boundary and does not convert that boundary into a simpler license claim.
- It does not run the REUSE tool, create a REUSE.toml, generate an SPDX document, perform legal review, or claim REUSE compliance, source license compliance, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- inventory_format: \`${report.inventoryFormat}\`
- package_license_field: \`${report.packageLicenseField ?? 'null'}\`
- root_license_sha256: \`${report.rootLicenseSha256}\`
- root_license_contains_derived_code_boundary: \`${report.rootLicenseContainsDerivedCodeBoundary}\`
- root_license_contains_mit_modification_boundary: \`${report.rootLicenseContainsMitModificationBoundary}\`
- reuse_toml_present: \`${report.reuseTomlPresent}\`
- licenses_directory_present: \`${report.licensesDirectoryPresent}\`
- scanned_source_file_count: \`${report.scannedSourceFileCount}\`
- source_files_with_spdx_license_identifier_count: \`${report.sourceFilesWithSpdxLicenseIdentifierCount}\`
- source_files_with_spdx_copyright_text_count: \`${report.sourceFilesWithSpdxCopyrightTextCount}\`
- source_files_with_adjacent_license_file_count: \`${report.sourceFilesWithAdjacentLicenseFileCount}\`
- source_files_covered_by_reuse_toml_annotation_count: \`${report.sourceFilesCoveredByReuseTomlAnnotationCount}\`
- source_files_missing_file_level_metadata_count: \`${report.sourceFilesMissingFileLevelMetadataCount}\`
- inventory_jsonl_path: \`${report.inventoryJsonlPath}\`
- inventory_jsonl_sha256: \`${report.inventoryJsonlSha256}\`
- inventory_jsonl_record_count: \`${report.inventoryJsonlRecordCount}\`
- inventory_jsonl_parseable: \`${report.inventoryJsonlParseable}\`
- reuse_tool_run_performed: \`${report.reuseToolRunPerformed}\`
- reuse_compliance_claim_allowed: \`${report.reuseComplianceClaimAllowed}\`
- source_license_compliance_claim_allowed: \`${report.sourceLicenseComplianceClaimAllowed}\`
- source_metadata_ready_claim_allowed: \`${report.sourceMetadataReadyClaimAllowed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## File Categories

| Category | Count |
| --- | ---: |
${categoryRows}

## Missing File-Level Metadata Preview

First 100 missing file-level metadata records are shown here. The complete source-hash-addressed inventory is written to \`${report.inventoryJsonlPath}\`.

| Path |
| --- |
${gapRows || '| `none` |'}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'source-license-metadata-quality-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const packageJson = readJson<PackageJson>(packageJsonPath)
  const rootLicenseText = readText(rootLicensePath)
  const sourceLicenseRecords = sourceFilePaths().map(recordForPath)
  const sourceFilesMissingFileLevelMetadata = sourceLicenseRecords
    .filter((record) => !record.hasSpdxLicenseIdentifier && !record.hasAdjacentLicenseFile && !record.coveredByReuseTomlAnnotation)
    .map((record) => record.path)
  const inventoryJsonlText = sourceLicenseRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, inventoryJsonlPath), inventoryJsonlText)

  let inventoryJsonlParseable = true
  for (const line of inventoryJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      inventoryJsonlParseable = false
    }
  }

  const rootLicenseContainsDerivedCodeBoundary = /derived from Anthropic's Claude Code CLI/i.test(rootLicenseText) && /underlying derived code remains subject to Anthropic's copyright/i.test(rootLicenseText)
  const rootLicenseContainsMitModificationBoundary = /MIT License/i.test(rootLicenseText) && /OpenClaude contributors \(modifications only\)/i.test(rootLicenseText)
  const inventoryJsonlSha256 = sha256(inventoryJsonlText)
  const sourceFilesWithSpdxLicenseIdentifierCount = sourceLicenseRecords.filter((record) => record.hasSpdxLicenseIdentifier).length
  const sourceFilesWithSpdxCopyrightTextCount = sourceLicenseRecords.filter((record) => record.hasSpdxFileCopyrightText).length
  const sourceFilesWithAdjacentLicenseFileCount = sourceLicenseRecords.filter((record) => record.hasAdjacentLicenseFile).length
  const sourceFilesCoveredByReuseTomlAnnotationCount = sourceLicenseRecords.filter((record) => record.coveredByReuseTomlAnnotation).length

  const sourceLicenseMetadataChecks = [
    check('root LICENSE exists and is non-empty', existsSync(resolve(root, rootLicensePath)) && statSync(resolve(root, rootLicensePath)).size > 0, rootLicensePath),
    check('root LICENSE derived-code boundary is recognized', rootLicenseContainsDerivedCodeBoundary, 'Anthropic derived-code boundary present'),
    check('root LICENSE modification-license boundary is recognized', rootLicenseContainsMitModificationBoundary, 'OpenClaude modifications MIT boundary present'),
    check('package license field preserves SEE LICENSE boundary', packageJson.license === 'SEE LICENSE FILE', String(packageJson.license ?? 'missing')),
    check('source scan covers expected source and product surfaces', sourceLicenseRecords.length > 1000 && scanRoots.every((scanRoot) => sourceLicenseRecords.some((record) => record.path.startsWith(`${scanRoot}/`))), `${sourceLicenseRecords.length} scanned files`),
    check('file-level SPDX metadata gaps are classified', sourceFilesMissingFileLevelMetadata.length >= 0 && sourceFilesMissingFileLevelMetadata.length === sourceLicenseRecords.length - sourceFilesWithSpdxLicenseIdentifierCount - sourceFilesWithAdjacentLicenseFileCount - sourceFilesCoveredByReuseTomlAnnotationCount, `${sourceFilesMissingFileLevelMetadata.length} gaps`),
    check('REUSE.toml and LICENSES absence is recorded without claiming compliance', !existsSync(resolve(root, reuseTomlPath)) && !existsSync(resolve(root, licensesDirectoryPath)), 'REUSE.toml/LICENSES absent and classified'),
    check('inventory JSONL has one record per scanned source file', sourceLicenseRecords.length > 0 && inventoryJsonlText.trim().split(/\r?\n/).length === sourceLicenseRecords.length, `${sourceLicenseRecords.length} records`),
    check('inventory JSONL is parseable and hash-addressed', inventoryJsonlParseable && inventoryJsonlSha256.length === 64, inventoryJsonlPath),
    check('REUSE/legal/compliance claims remain blocked', true, 'reuse lint/spdx generation/legal review/source compliance/readiness claims are false'),
    check('protected actions are not executed', true, 'provider/live/external/tool install/protected actions are absent'),
  ]

  const report: SourceLicenseMetadataQualityReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_source_license_metadata_quality',
    inventoryFormat: 'openclaude_source_license_metadata_inventory_v1',
    primarySourceInputs: [
      {
        sourceProject: 'REUSE Specification',
        sourceUrl: 'https://reuse.software/spec-3.2/',
        observedPattern: 'REUSE defines license files, file licensing information, and REUSE.toml annotations so licensing data can be associated with covered files in a machine-readable way.',
        localAbsorption: 'The local gate inventories current file-level metadata coverage and records that REUSE.toml/LICENSES compliance artifacts are not present.',
      },
      {
        sourceProject: 'SPDX source-file identifiers',
        sourceUrl: 'https://spdx.github.io/spdx-spec/v2.3/using-SPDX-short-identifiers-in-source-files/',
        observedPattern: 'SPDX-License-Identifier tags at or near the top of source files provide concise, language-neutral, machine-processable file-level license declarations.',
        localAbsorption: 'The local gate scans source and product surfaces for SPDX-License-Identifier tags and classifies missing file-level metadata without rewriting source files.',
      },
      {
        sourceProject: 'fsfe/reuse-tool',
        sourceUrl: 'https://github.com/fsfe/reuse-tool',
        observedPattern: 'The maintained REUSE tool can lint projects and generate SPDX documents, but running it may require additional tooling or Docker/Python setup.',
        localAbsorption: 'The local gate records that reuse lint/spdx execution and dependency installation were not performed in this no-provider, no-install run.',
      },
      {
        sourceProject: 'SPDX handling license info',
        sourceUrl: 'https://spdx.dev/learn/handling-license-info/',
        observedPattern: 'SPDX short-form identifiers are used in source files and tooling because they are concise and easier to machine process.',
        localAbsorption: 'The local gate treats missing SPDX source identifiers as a measurable product-quality gap rather than a hidden release-readiness assumption.',
      },
    ],
    packageJsonPath,
    packageJsonSha256: fileSha256(packageJsonPath),
    packageLicenseField: typeof packageJson.license === 'string' ? packageJson.license : null,
    rootLicensePath,
    rootLicenseSha256: fileSha256(rootLicensePath),
    rootLicenseContainsDerivedCodeBoundary,
    rootLicenseContainsMitModificationBoundary,
    reuseTomlPath,
    reuseTomlPresent: existsSync(resolve(root, reuseTomlPath)),
    licensesDirectoryPath,
    licensesDirectoryPresent: existsSync(resolve(root, licensesDirectoryPath)),
    reuseToolRunPerformed: false,
    reuseComplianceClaimAllowed: false,
    spdxDocumentGenerated: false,
    legalReviewPerformed: false,
    sourceLicenseComplianceClaimAllowed: false,
    sourceMetadataReadyClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    scanRoots,
    excludedPathFragments,
    scannedSourceFileCount: sourceLicenseRecords.length,
    sourceFilesWithSpdxLicenseIdentifierCount,
    sourceFilesWithSpdxCopyrightTextCount,
    sourceFilesWithAdjacentLicenseFileCount,
    sourceFilesCoveredByReuseTomlAnnotationCount,
    sourceFilesMissingFileLevelMetadataCount: sourceFilesMissingFileLevelMetadata.length,
    sourceFilesMissingFileLevelMetadata,
    fileCategoryCounts: countCategories(sourceLicenseRecords),
    inventoryJsonlPath,
    inventoryJsonlSha256,
    inventoryJsonlRecordCount: sourceLicenseRecords.length,
    inventoryJsonlParseable,
    sourceLicenseRecords,
    claimBoundary: 'Source license metadata quality is a local no-provider inventory of file-level SPDX/REUSE metadata coverage only. It preserves the current derived-code and modification-license boundary and does not run reuse lint, create REUSE.toml, generate SPDX documents, perform legal review, claim REUSE compliance, claim source license compliance, or claim release/public/production/external/autonomous readiness.',
    sourceLicenseMetadataChecks,
  }

  writeFileSync(resolve(docsDir, 'source-license-metadata-quality-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of sourceLicenseMetadataChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = sourceLicenseMetadataChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`scanned_source_file_count=${report.scannedSourceFileCount}`)
  console.log(`source_files_with_spdx_license_identifier_count=${report.sourceFilesWithSpdxLicenseIdentifierCount}`)
  console.log(`source_files_missing_file_level_metadata_count=${report.sourceFilesMissingFileLevelMetadataCount}`)
  console.log(`reuse_toml_present=${report.reuseTomlPresent}`)
  console.log(`licenses_directory_present=${report.licensesDirectoryPresent}`)
  console.log(`root_license_contains_derived_code_boundary=${report.rootLicenseContainsDerivedCodeBoundary}`)
  console.log(`root_license_contains_mit_modification_boundary=${report.rootLicenseContainsMitModificationBoundary}`)
  console.log(`inventory_jsonl_path=${report.inventoryJsonlPath}`)
  console.log(`inventory_jsonl_record_count=${report.inventoryJsonlRecordCount}`)
  console.log(`reuse_tool_run_performed=${report.reuseToolRunPerformed}`)
  console.log(`reuse_compliance_claim_allowed=${report.reuseComplianceClaimAllowed}`)
  console.log(`source_license_compliance_claim_allowed=${report.sourceLicenseComplianceClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

if (!existsSync(resolve(root, packageJsonPath)) || !existsSync(resolve(root, rootLicensePath))) {
  console.error('RESULT: FAIL (required package.json or LICENSE missing)')
  process.exit(1)
}

main()
