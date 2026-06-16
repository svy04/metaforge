import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { check, fileSha256, readText, sha256, type Check } from './quality-report-helpers'

type SourceInput = {
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type ThirdPartyLicenseQualityReport = {
  mode: string
  sourceLockfilePackageCount: number
  directManifestDependencyCount: number
  directManifestDependenciesCoveredByMetadata: boolean
  directLicenseFileMissingPackages: string[]
  noticeFilePresentCount: number
  spdxExpressionParsePerformed: boolean
  externalLicenseResolutionPerformed: boolean
  legalReviewPerformed: boolean
  noticeFileGenerated: boolean
  dependencyInstallPerformed: boolean
  npmRegistryLookupPerformed: boolean
  githubLicenseApiLookupPerformed: boolean
  licenseComplianceClaimAllowed: boolean
  thirdPartyNoticeReadyClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  licenseQualityChecks: Array<{ label: string; ok: boolean }>
}

type SourceLicenseMetadataQualityReport = {
  mode: string
  packageLicenseField: string | null
  rootLicenseContainsDerivedCodeBoundary: boolean
  rootLicenseContainsMitModificationBoundary: boolean
  reuseTomlPresent: boolean
  licensesDirectoryPresent: boolean
  reuseToolRunPerformed: boolean
  reuseComplianceClaimAllowed: boolean
  spdxDocumentGenerated: boolean
  legalReviewPerformed: boolean
  sourceLicenseComplianceClaimAllowed: boolean
  sourceMetadataReadyClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  scannedSourceFileCount: number
  sourceFilesWithSpdxLicenseIdentifierCount: number
  sourceFilesMissingFileLevelMetadataCount: number
  inventoryJsonlRecordCount: number
  sourceLicenseMetadataChecks: Array<{ label: string; ok: boolean }>
}

type AuthorizationItem = {
  schemaVersion: 'openclaude_license_boundary_authorization_item_v1'
  id: string
  category:
    | 'legal_review'
    | 'third_party_notice'
    | 'source_metadata'
    | 'reuse_spdx'
    | 'claim_boundary'
    | 'protected_execution'
  currentEvidence: string
  requiredDecision: string
  defaultAuthorized: false
  protectedAction: true
  forbiddenShortcut: string
  validationMethod: string
  status: 'blocked_pending_explicit_owner_or_legal_authorization'
  recordDigest: string
}

type LicenseBoundaryAuthorizationReport = {
  generatedAt: string
  mode: 'local_no_provider_license_boundary_authorization'
  primarySourceInputs: SourceInput[]
  sourceThirdPartyLicenseQualityReportPath: string
  sourceThirdPartyLicenseQualityReportSha256: string
  sourceSourceLicenseMetadataQualityReportPath: string
  sourceSourceLicenseMetadataQualityReportSha256: string
  requestMarkdownPath: string
  authorizationItemsJsonlPath: string
  authorizationItemsJsonlSha256: string
  authorizationItemsJsonlRecordCount: number
  authorizationItemsJsonlParseable: boolean
  licenseBoundaryStatus: 'owner_legal_authorization_required_before_release_or_license_compliance_claims'
  ownerLegalDecisionRequired: true
  protectedAuthorizationRequestCreated: true
  protectedAuthorizationRequestCount: number
  allProtectedAuthorizationsDefaultFalse: boolean
  thirdPartySourceLockfilePackageCount: number
  thirdPartyDirectManifestDependencyCount: number
  thirdPartyDirectDependenciesCoveredByMetadata: boolean
  thirdPartyDirectLicenseFileMissingPackages: string[]
  thirdPartyNoticeFilePresentCount: number
  sourceScannedFileCount: number
  sourceFilesWithSpdxLicenseIdentifierCount: number
  sourceFilesMissingFileLevelMetadataCount: number
  reuseTomlPresent: boolean
  licensesDirectoryPresent: boolean
  derivedCodeBoundaryRecognized: boolean
  mitModificationBoundaryRecognized: boolean
  spdxExpressionParsePerformed: false
  externalLicenseResolutionPerformed: false
  legalReviewPerformed: false
  noticeFileGenerated: false
  dependencyInstallPerformed: false
  npmRegistryLookupPerformed: false
  githubLicenseApiLookupPerformed: false
  reuseToolRunPerformed: false
  spdxDocumentGenerated: false
  reuseArtifactsCreated: false
  sourceFilesRewritten: false
  licenseComplianceClaimAllowed: false
  thirdPartyNoticeReadyClaimAllowed: false
  reuseComplianceClaimAllowed: false
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
  authorizationItems: AuthorizationItem[]
  licenseBoundaryAuthorizationChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const thirdPartyReportPath = 'docs/product-quality/third-party-license-quality-report.json'
const sourceLicenseReportPath = 'docs/product-quality/source-license-metadata-quality-report.json'
const reportJsonPath = 'docs/product-quality/license-boundary-authorization-report.json'
const reportMdPath = 'docs/product-quality/license-boundary-authorization-report.md'
const requestMarkdownPath = 'docs/product-quality/license-boundary-authorization-request.md'
const authorizationItemsJsonlPath = 'reports/openclaude-license-boundary-authorization-items.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function authorizationItem(input: Omit<AuthorizationItem, 'schemaVersion' | 'defaultAuthorized' | 'protectedAction' | 'status' | 'recordDigest'>): AuthorizationItem {
  const base = {
    schemaVersion: 'openclaude_license_boundary_authorization_item_v1' as const,
    ...input,
    defaultAuthorized: false as const,
    protectedAction: true as const,
    status: 'blocked_pending_explicit_owner_or_legal_authorization' as const,
  }
  return {
    ...base,
    recordDigest: sha256(JSON.stringify(base)),
  }
}

function authorizationItems(thirdParty: ThirdPartyLicenseQualityReport, sourceLicense: SourceLicenseMetadataQualityReport): AuthorizationItem[] {
  return [
    authorizationItem({
      id: 'authorize_legal_review_before_license_compliance_claim',
      category: 'legal_review',
      currentEvidence: 'Local license inventories exist, but no legal review was performed.',
      requiredDecision: 'Owner/legal must explicitly authorize legal review before any license-compliance conclusion is made.',
      forbiddenShortcut: 'Do not infer legal approval from package metadata, a root LICENSE file, or passing local scripts.',
      validationMethod: 'Require a separate owner/legal authorization artifact and rerun this boundary gate.',
    }),
    authorizationItem({
      id: 'authorize_third_party_notice_generation',
      category: 'third_party_notice',
      currentEvidence: `${thirdParty.directLicenseFileMissingPackages.length} direct dependency license-file gaps and ${thirdParty.noticeFilePresentCount} installed NOTICE-file records are classified.`,
      requiredDecision: 'Owner/legal must authorize NOTICE generation and review before any third-party NOTICE readiness claim.',
      forbiddenShortcut: 'Do not generate or publish a NOTICE file from unreviewed local metadata.',
      validationMethod: 'Require reviewed NOTICE inputs plus a separate NOTICE-generation gate.',
    }),
    authorizationItem({
      id: 'authorize_spdx_expression_parsing_and_external_license_resolution',
      category: 'reuse_spdx',
      currentEvidence: 'SPDX expression parsing and external license resolution were not performed.',
      requiredDecision: 'Owner/legal must authorize SPDX expression parsing and any external license resolution workflow.',
      forbiddenShortcut: 'Do not treat raw package license strings as final license conclusions.',
      validationMethod: 'Require a deterministic parser or reviewed external-resolution artifact before changing claim flags.',
    }),
    authorizationItem({
      id: 'authorize_reuse_toml_or_license_artifacts_for_derived_code_boundary',
      category: 'reuse_spdx',
      currentEvidence: `REUSE.toml present=${sourceLicense.reuseTomlPresent}; LICENSES directory present=${sourceLicense.licensesDirectoryPresent}; derived-code boundary recognized=${sourceLicense.rootLicenseContainsDerivedCodeBoundary}.`,
      requiredDecision: 'Owner/legal must decide how REUSE.toml, LICENSES files, or equivalent annotations should represent derived-code and modification-license boundaries.',
      forbiddenShortcut: 'Do not create REUSE.toml or LICENSES artifacts that simplify or overwrite the current derived-code boundary.',
      validationMethod: 'Require explicit owner/legal scope text for every covered file class before artifact creation.',
    }),
    authorizationItem({
      id: 'authorize_source_file_license_metadata_updates',
      category: 'source_metadata',
      currentEvidence: `${sourceLicense.sourceFilesMissingFileLevelMetadataCount} of ${sourceLicense.scannedSourceFileCount} scanned files lack file-level metadata.`,
      requiredDecision: 'Owner/legal must authorize source-file SPDX headers, adjacent .license files, or REUSE annotations before source metadata updates.',
      forbiddenShortcut: 'Do not mass-insert SPDX headers into derived-code files without a reviewed license mapping.',
      validationMethod: 'Require reviewed file-class mapping and rerun source-license metadata quality after any update.',
    }),
    authorizationItem({
      id: 'authorize_license_compliance_claim',
      category: 'claim_boundary',
      currentEvidence: 'Local inventories and gap classifications exist, but compliance flags remain false.',
      requiredDecision: 'Owner/legal must explicitly authorize any license-compliance claim.',
      forbiddenShortcut: 'Do not claim license compliance from local no-provider inventory coverage.',
      validationMethod: 'Require legal-review evidence and a gate that flips claim flags only after explicit authorization.',
    }),
    authorizationItem({
      id: 'authorize_source_metadata_readiness_claim',
      category: 'claim_boundary',
      currentEvidence: `Only ${sourceLicense.sourceFilesWithSpdxLicenseIdentifierCount} scanned file has an SPDX-License-Identifier and REUSE artifacts are absent.`,
      requiredDecision: 'Owner/legal must authorize any source-metadata readiness or REUSE compliance claim.',
      forbiddenShortcut: 'Do not convert gap classification into source-metadata readiness.',
      validationMethod: 'Require REUSE/SPDX evidence and legal approval before source-metadata readiness is allowed.',
    }),
    authorizationItem({
      id: 'authorize_release_public_or_production_readiness_claims',
      category: 'claim_boundary',
      currentEvidence: 'Release, public, production, external-validation, and autonomous-reliability claim flags remain false.',
      requiredDecision: 'Owner must explicitly authorize any stronger public, release, production, or external-validation claim.',
      forbiddenShortcut: 'Do not upgrade internal no-provider evidence into public readiness language.',
      validationMethod: 'Require separate owner authorization and the full product-quality gate to pass without protected blockers.',
    }),
    authorizationItem({
      id: 'authorize_dependency_install_or_external_lookup',
      category: 'protected_execution',
      currentEvidence: 'Dependency install, npm lookup, and GitHub license API lookup were not performed.',
      requiredDecision: 'Owner must explicitly authorize installs or external lookups if a later license workflow needs them.',
      forbiddenShortcut: 'Do not run package managers, npm registry calls, or GitHub API calls inside this local no-provider gate.',
      validationMethod: 'Require a protected-action authorization artifact before any external or install step.',
    }),
  ]
}

function writeRequest(report: LicenseBoundaryAuthorizationReport): void {
  const decisionRows = report.authorizationItems
    .map((item) => `| \`${item.id}\` | \`${item.defaultAuthorized}\` | ${item.requiredDecision} | ${item.validationMethod} |`)
    .join('\n')
  const markdown = `# License Boundary Authorization Request

Generated by: \`bun run product:license-boundary-authorization\`

## Request Boundary

This request asks for explicit owner/legal decisions before OpenClaude may perform or claim any license-compliance, source-metadata readiness, REUSE compliance, NOTICE readiness, public, release, production, external-validation, or autonomous-reliability status.

No authorization is granted by this file. Every protected authorization below defaults to \`false\`.

## Current Evidence

- third_party_source_lockfile_package_count: \`${report.thirdPartySourceLockfilePackageCount}\`
- third_party_direct_manifest_dependency_count: \`${report.thirdPartyDirectManifestDependencyCount}\`
- third_party_direct_dependencies_covered_by_metadata: \`${report.thirdPartyDirectDependenciesCoveredByMetadata}\`
- third_party_direct_license_file_missing_packages: \`${report.thirdPartyDirectLicenseFileMissingPackages.join(',') || 'none'}\`
- third_party_notice_file_present_count: \`${report.thirdPartyNoticeFilePresentCount}\`
- source_scanned_file_count: \`${report.sourceScannedFileCount}\`
- source_files_with_spdx_license_identifier_count: \`${report.sourceFilesWithSpdxLicenseIdentifierCount}\`
- source_files_missing_file_level_metadata_count: \`${report.sourceFilesMissingFileLevelMetadataCount}\`
- reuse_toml_present: \`${report.reuseTomlPresent}\`
- licenses_directory_present: \`${report.licensesDirectoryPresent}\`
- derived_code_boundary_recognized: \`${report.derivedCodeBoundaryRecognized}\`
- mit_modification_boundary_recognized: \`${report.mitModificationBoundaryRecognized}\`

## Explicit Decisions Required

| Decision | Default Authorized | Required Decision | Validation Method |
| --- | --- | --- | --- |
${decisionRows}

## Blocked Claims

- license compliance
- third-party NOTICE readiness
- REUSE compliance
- source license compliance
- source metadata readiness
- release readiness
- production readiness
- public readiness
- external validation
- autonomous reliability

## Blocked Actions

- legal review execution
- NOTICE generation
- dependency install
- npm registry lookup
- GitHub license API lookup
- external license resolution
- REUSE tool execution
- SPDX document generation
- REUSE.toml or LICENSES artifact creation
- source-file metadata rewrite
`

  writeFileSync(resolve(root, requestMarkdownPath), markdown)
}

function writeMarkdown(report: LicenseBoundaryAuthorizationReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const itemRows = report.authorizationItems
    .map((item) => `| \`${item.id}\` | \`${item.category}\` | \`${item.defaultAuthorized}\` | \`${item.status}\` |`)
    .join('\n')
  const checkRows = report.licenseBoundaryAuthorizationChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')
  const markdown = `# License Boundary Authorization Report

Generated by: \`bun run product:license-boundary-authorization\`

## Claim Boundary

- This report converts local license inventories into explicit owner/legal authorization requirements.
- It does not perform legal review, parse SPDX expressions, resolve licenses externally, generate NOTICE files, create REUSE artifacts, rewrite source-file license metadata, install dependencies, or call external services.
- It does not claim license compliance, third-party NOTICE readiness, REUSE compliance, source license compliance, source metadata readiness, release readiness, production readiness, public readiness, external validation, or autonomous reliability.

## Summary

- mode: \`${report.mode}\`
- license_boundary_status: \`${report.licenseBoundaryStatus}\`
- owner_legal_decision_required: \`${report.ownerLegalDecisionRequired}\`
- protected_authorization_request_created: \`${report.protectedAuthorizationRequestCreated}\`
- protected_authorization_request_count: \`${report.protectedAuthorizationRequestCount}\`
- all_protected_authorizations_default_false: \`${report.allProtectedAuthorizationsDefaultFalse}\`
- request_markdown_path: \`${report.requestMarkdownPath}\`
- authorization_items_jsonl_path: \`${report.authorizationItemsJsonlPath}\`
- authorization_items_jsonl_sha256: \`${report.authorizationItemsJsonlSha256}\`
- authorization_items_jsonl_record_count: \`${report.authorizationItemsJsonlRecordCount}\`
- authorization_items_jsonl_parseable: \`${report.authorizationItemsJsonlParseable}\`
- legal_review_performed: \`${report.legalReviewPerformed}\`
- notice_file_generated: \`${report.noticeFileGenerated}\`
- reuse_artifacts_created: \`${report.reuseArtifactsCreated}\`
- source_files_rewritten: \`${report.sourceFilesRewritten}\`
- license_compliance_claim_allowed: \`${report.licenseComplianceClaimAllowed}\`
- third_party_notice_ready_claim_allowed: \`${report.thirdPartyNoticeReadyClaimAllowed}\`
- reuse_compliance_claim_allowed: \`${report.reuseComplianceClaimAllowed}\`
- source_license_compliance_claim_allowed: \`${report.sourceLicenseComplianceClaimAllowed}\`
- source_metadata_ready_claim_allowed: \`${report.sourceMetadataReadyClaimAllowed}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Primary Sources

| Source | URL | Local Absorption |
| --- | --- | --- |
${sourceRows}

## Authorization Items

| Item | Category | Default Authorized | Status |
| --- | --- | --- | --- |
${itemRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const thirdParty = readJson<ThirdPartyLicenseQualityReport>(thirdPartyReportPath)
  const sourceLicense = readJson<SourceLicenseMetadataQualityReport>(sourceLicenseReportPath)
  const items = authorizationItems(thirdParty, sourceLicense)
  const itemsJsonlText = items.map((item) => JSON.stringify(item)).join('\n') + '\n'
  writeFileSync(resolve(root, authorizationItemsJsonlPath), itemsJsonlText)

  let authorizationItemsJsonlParseable = true
  for (const line of itemsJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      authorizationItemsJsonlParseable = false
    }
  }

  const allProtectedAuthorizationsDefaultFalse = items.every((item) => item.protectedAction === true && item.defaultAuthorized === false)
  const requiredItemIds = [
    'authorize_legal_review_before_license_compliance_claim',
    'authorize_third_party_notice_generation',
    'authorize_spdx_expression_parsing_and_external_license_resolution',
    'authorize_reuse_toml_or_license_artifacts_for_derived_code_boundary',
    'authorize_source_file_license_metadata_updates',
    'authorize_license_compliance_claim',
    'authorize_source_metadata_readiness_claim',
    'authorize_release_public_or_production_readiness_claims',
    'authorize_dependency_install_or_external_lookup',
  ]

  const licenseBoundaryAuthorizationChecks = [
    check('third-party license report is present and local no-provider', thirdParty.mode === 'local_no_provider_third_party_license_quality', thirdParty.mode),
    check('source license metadata report is present and local no-provider', sourceLicense.mode === 'local_no_provider_source_license_metadata_quality', sourceLicense.mode),
    check('source reports pass their own checks', thirdParty.licenseQualityChecks.every((item) => item.ok) && sourceLicense.sourceLicenseMetadataChecks.every((item) => item.ok), 'source license checks all ok'),
    check('source reports performed no provider/live/external calls', thirdParty.providerCallsPerformed.length === 0 && thirdParty.liveModelCallsPerformed.length === 0 && thirdParty.externalCallsPerformed.length === 0 && sourceLicense.providerCallsPerformed.length === 0 && sourceLicense.liveModelCallsPerformed.length === 0 && sourceLicense.externalCallsPerformed.length === 0, 'all source call arrays empty'),
    check('source reports executed no protected actions', thirdParty.protectedActionsExecuted.length === 0 && sourceLicense.protectedActionsExecuted.length === 0, 'protectedActionsExecuted=[]'),
    check('source reports preserve derived-code and modification-license boundaries', sourceLicense.packageLicenseField === 'SEE LICENSE FILE' && sourceLicense.rootLicenseContainsDerivedCodeBoundary && sourceLicense.rootLicenseContainsMitModificationBoundary, String(sourceLicense.packageLicenseField)),
    check('source reports keep license actions and claims blocked', thirdParty.spdxExpressionParsePerformed === false && thirdParty.externalLicenseResolutionPerformed === false && thirdParty.legalReviewPerformed === false && thirdParty.noticeFileGenerated === false && thirdParty.licenseComplianceClaimAllowed === false && thirdParty.thirdPartyNoticeReadyClaimAllowed === false && sourceLicense.reuseToolRunPerformed === false && sourceLicense.spdxDocumentGenerated === false && sourceLicense.legalReviewPerformed === false && sourceLicense.reuseComplianceClaimAllowed === false && sourceLicense.sourceLicenseComplianceClaimAllowed === false && sourceLicense.sourceMetadataReadyClaimAllowed === false, 'license and source metadata claims false'),
    check('source reports keep readiness claims blocked', thirdParty.releaseReadinessClaimAllowed === false && thirdParty.productionReadinessClaimAllowed === false && thirdParty.publicReadinessClaimAllowed === false && thirdParty.externalValidationClaimAllowed === false && thirdParty.autonomousReliabilityClaimAllowed === false && sourceLicense.releaseReadinessClaimAllowed === false && sourceLicense.productionReadinessClaimAllowed === false && sourceLicense.publicReadinessClaimAllowed === false && sourceLicense.externalValidationClaimAllowed === false && sourceLicense.autonomousReliabilityClaimAllowed === false, 'readiness claim flags false'),
    check('license boundary request includes all required decision items', requiredItemIds.every((id) => items.some((item) => item.id === id)) && items.length === requiredItemIds.length, `${items.length} items`),
    check('all protected authorization defaults are false', allProtectedAuthorizationsDefaultFalse, 'defaultAuthorized=false for every item'),
    check('authorization items JSONL is parseable and hash-addressed', authorizationItemsJsonlParseable && sha256(itemsJsonlText).length === 64, authorizationItemsJsonlPath),
  ]

  const report: LicenseBoundaryAuthorizationReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_license_boundary_authorization',
    primarySourceInputs: [
      {
        sourceProject: 'GitHub Docs licensing a repository',
        sourceUrl: 'https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository/',
        observedPattern: 'GitHub treats repository licensing as an explicit decision surface and separates license metadata from legal advice.',
        localAbsorption: 'OpenClaude records that license inventory evidence is not legal review and routes stronger license claims to explicit owner/legal authorization.',
      },
      {
        sourceProject: 'npm package.json license field',
        sourceUrl: 'https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#license',
        observedPattern: 'npm package metadata uses license fields, SPDX expressions, or SEE LICENSE references, but package metadata alone is not a full NOTICE or legal-review workflow.',
        localAbsorption: 'OpenClaude keeps package license fields as input evidence and blocks NOTICE/license-compliance claims until explicit review exists.',
      },
      {
        sourceProject: 'SPDX License List',
        sourceUrl: 'https://spdx.org/licenses/',
        observedPattern: 'SPDX identifiers support efficient and reliable identification in documents, source files, and other tooling.',
        localAbsorption: 'OpenClaude keeps SPDX expression parsing and final license conclusions behind owner/legal authorization.',
      },
      {
        sourceProject: 'SPDX File Tags',
        sourceUrl: 'https://spdx.github.io/spdx-spec/v2.3/file-tags/',
        observedPattern: 'SPDX file tags provide source-file-level license information through machine-readable tags.',
        localAbsorption: 'OpenClaude treats missing file-level tags as a measurable gap and blocks mass source rewrites until file-class licensing is authorized.',
      },
      {
        sourceProject: 'REUSE Specification 3.2',
        sourceUrl: 'https://reuse.software/spec-3.2/',
        observedPattern: 'REUSE requires licensing information for covered files and supports comment headers, adjacent .license files, and REUSE.toml annotations.',
        localAbsorption: 'OpenClaude records a decision request before creating REUSE artifacts because this repository has a derived-code/modification-license boundary.',
      },
    ],
    sourceThirdPartyLicenseQualityReportPath: thirdPartyReportPath,
    sourceThirdPartyLicenseQualityReportSha256: fileSha256(thirdPartyReportPath),
    sourceSourceLicenseMetadataQualityReportPath: sourceLicenseReportPath,
    sourceSourceLicenseMetadataQualityReportSha256: fileSha256(sourceLicenseReportPath),
    requestMarkdownPath,
    authorizationItemsJsonlPath,
    authorizationItemsJsonlSha256: sha256(itemsJsonlText),
    authorizationItemsJsonlRecordCount: items.length,
    authorizationItemsJsonlParseable,
    licenseBoundaryStatus: 'owner_legal_authorization_required_before_release_or_license_compliance_claims',
    ownerLegalDecisionRequired: true,
    protectedAuthorizationRequestCreated: true,
    protectedAuthorizationRequestCount: items.length,
    allProtectedAuthorizationsDefaultFalse,
    thirdPartySourceLockfilePackageCount: thirdParty.sourceLockfilePackageCount,
    thirdPartyDirectManifestDependencyCount: thirdParty.directManifestDependencyCount,
    thirdPartyDirectDependenciesCoveredByMetadata: thirdParty.directManifestDependenciesCoveredByMetadata,
    thirdPartyDirectLicenseFileMissingPackages: thirdParty.directLicenseFileMissingPackages,
    thirdPartyNoticeFilePresentCount: thirdParty.noticeFilePresentCount,
    sourceScannedFileCount: sourceLicense.scannedSourceFileCount,
    sourceFilesWithSpdxLicenseIdentifierCount: sourceLicense.sourceFilesWithSpdxLicenseIdentifierCount,
    sourceFilesMissingFileLevelMetadataCount: sourceLicense.sourceFilesMissingFileLevelMetadataCount,
    reuseTomlPresent: sourceLicense.reuseTomlPresent,
    licensesDirectoryPresent: sourceLicense.licensesDirectoryPresent,
    derivedCodeBoundaryRecognized: sourceLicense.rootLicenseContainsDerivedCodeBoundary,
    mitModificationBoundaryRecognized: sourceLicense.rootLicenseContainsMitModificationBoundary,
    spdxExpressionParsePerformed: false,
    externalLicenseResolutionPerformed: false,
    legalReviewPerformed: false,
    noticeFileGenerated: false,
    dependencyInstallPerformed: false,
    npmRegistryLookupPerformed: false,
    githubLicenseApiLookupPerformed: false,
    reuseToolRunPerformed: false,
    spdxDocumentGenerated: false,
    reuseArtifactsCreated: false,
    sourceFilesRewritten: false,
    licenseComplianceClaimAllowed: false,
    thirdPartyNoticeReadyClaimAllowed: false,
    reuseComplianceClaimAllowed: false,
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
    authorizationItems: items,
    licenseBoundaryAuthorizationChecks,
    claimBoundary: 'License boundary authorization is an internal no-provider owner/legal decision packet only. It does not authorize or perform legal review, dependency installs, external lookups, NOTICE generation, REUSE artifact creation, source-file rewrites, license-compliance claims, third-party NOTICE readiness claims, source-metadata readiness claims, release readiness, production readiness, public readiness, external validation, or autonomous reliability claims.',
  }

  writeRequest(report)
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of licenseBoundaryAuthorizationChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = licenseBoundaryAuthorizationChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`license_boundary_status=${report.licenseBoundaryStatus}`)
  console.log(`owner_legal_decision_required=${report.ownerLegalDecisionRequired}`)
  console.log(`protected_authorization_request_created=${report.protectedAuthorizationRequestCreated}`)
  console.log(`protected_authorization_request_count=${report.protectedAuthorizationRequestCount}`)
  console.log(`all_protected_authorizations_default_false=${report.allProtectedAuthorizationsDefaultFalse}`)
  console.log(`source_files_missing_file_level_metadata_count=${report.sourceFilesMissingFileLevelMetadataCount}`)
  console.log(`third_party_direct_license_file_missing_count=${report.thirdPartyDirectLicenseFileMissingPackages.length}`)
  console.log(`third_party_notice_file_present_count=${report.thirdPartyNoticeFilePresentCount}`)
  console.log(`license_compliance_claim_allowed=${report.licenseComplianceClaimAllowed}`)
  console.log(`third_party_notice_ready_claim_allowed=${report.thirdPartyNoticeReadyClaimAllowed}`)
  console.log(`source_metadata_ready_claim_allowed=${report.sourceMetadataReadyClaimAllowed}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

if (!existsSync(resolve(root, thirdPartyReportPath)) || !existsSync(resolve(root, sourceLicenseReportPath))) {
  console.error('RESULT: FAIL (required license source reports missing)')
  process.exit(1)
}

main()
