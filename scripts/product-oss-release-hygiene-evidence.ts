import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = { label: string; ok: boolean; detail: string }

type SafeBacklogPlanItem = {
  planItemId: string
  sourceProject: string
  sourceUrl: string
  axis: string
  backlogText: string
  currentLocalEvidence: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
}

type SafeBacklogPlanReport = {
  mode: string
  sourceAxisArchitectureReviewReportPath: string
  nextSafeInternalGateCandidates: Array<{
    gateId: string
    axis: string
    protectedActionRequiredForPlanning: boolean
  }>
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  planItems: SafeBacklogPlanItem[]
}

type EvidenceBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type ReleaseHygieneCoverageClass =
  | 'local_artifact_reproducibility_sbom_license_gate'
  | 'signed_provenance_publish_release_claim_boundary'

type ReleaseHygieneEvidenceItem = {
  evidenceItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'release_hygiene'
  backlogText: string
  releaseHygieneCoverageClass: ReleaseHygieneCoverageClass
  currentLocalEvidence: EvidenceBinding[]
  supplementalLocalEvidence: EvidenceBinding[]
  requiredEvidenceBeforeReleaseClaim: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  implementationStatus: 'release_hygiene_evidence_matrix_created_internal_no_provider'
  protectedActionRequiredForEvidenceMatrix: false
  protectedActionExecuted: false
  commitAllowed: false
  pushAllowed: false
  publishAllowed: false
  deployAllowed: false
  launchAllowed: false
  signedProvenanceClaimAllowed: false
  legalNoticeReuseDecisionAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type ReleaseHygieneEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_release_hygiene_evidence'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'release_hygiene'
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  commitAllowed: false
  pushAllowed: false
  publishAllowed: false
  deployAllowed: false
  launchAllowed: false
  signedProvenanceGenerated: false
  signedProvenanceClaimAllowed: false
  legalNoticeReuseDecisionAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  evidenceItems: ReleaseHygieneEvidenceItem[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-release-hygiene-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-release-hygiene-evidence-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-release-hygiene-evidence.jsonl'

const reproducibilitySupplementalEvidence = [
  'docs/product-quality/release-artifact-file-list-report.md',
  'docs/product-quality/release-artifact-provenance-report.md',
  'docs/product-quality/release-artifact-reproducibility-report.md',
  'docs/product-quality/lockfile-sbom-quality-report.json',
  'reports/openclaude-lockfile-sbom-inventory.jsonl',
  'docs/product-quality/third-party-license-quality-report.json',
  'reports/openclaude-third-party-license-inventory.jsonl',
  'docs/product-quality/source-license-metadata-quality-report.json',
  'reports/openclaude-source-license-metadata-inventory.jsonl',
]

const releaseClaimBoundarySupplementalEvidence = [
  'docs/product-quality/git-release-hygiene-report.md',
  'docs/product-quality/license-boundary-authorization-report.md',
  'docs/product-quality/license-boundary-authorization-request.md',
  'reports/openclaude-license-boundary-authorization-items.jsonl',
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function slug(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '')
}

function bindEvidence(path: string): EvidenceBinding {
  const absolutePath = resolve(root, path)
  if (!existsSync(absolutePath)) {
    return { path, exists: false, sha256: null, sizeBytes: 0 }
  }
  const content = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(content), sizeBytes: content.byteLength }
}

function coverageClass(item: SafeBacklogPlanItem): ReleaseHygieneCoverageClass {
  const text = item.backlogText.toLowerCase()
  return text.includes('signed provenance') || text.includes('publish') || text.includes('deploy')
    ? 'signed_provenance_publish_release_claim_boundary'
    : 'local_artifact_reproducibility_sbom_license_gate'
}

function supplementalEvidencePaths(item: SafeBacklogPlanItem): string[] {
  return coverageClass(item) === 'signed_provenance_publish_release_claim_boundary'
    ? releaseClaimBoundarySupplementalEvidence
    : reproducibilitySupplementalEvidence
}

function toEvidenceItem(item: SafeBacklogPlanItem): ReleaseHygieneEvidenceItem {
  return {
    evidenceItemId: `oss_release_hygiene_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'release_hygiene',
    backlogText: item.backlogText,
    releaseHygieneCoverageClass: coverageClass(item),
    currentLocalEvidence: item.currentLocalEvidence.map(bindEvidence),
    supplementalLocalEvidence: supplementalEvidencePaths(item).map(bindEvidence),
    requiredEvidenceBeforeReleaseClaim: [
      'real git repository and release boundary evidence',
      'artifact reproducibility, file-list, SBOM-shaped inventory, and license-boundary evidence',
      'explicit owner authorization before commit, push, publish, deploy, launch, signed provenance, legal/NOTICE/REUSE decisions, or readiness claims',
      'separate external validation before any external, public, production, release, or autonomous reliability claim',
    ],
    unresolvedEvidenceGap: item.unresolvedEvidenceGap,
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    implementationStatus: 'release_hygiene_evidence_matrix_created_internal_no_provider',
    protectedActionRequiredForEvidenceMatrix: false,
    protectedActionExecuted: false,
    commitAllowed: false,
    pushAllowed: false,
    publishAllowed: false,
    deployAllowed: false,
    launchAllowed: false,
    signedProvenanceClaimAllowed: false,
    legalNoticeReuseDecisionAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: ReleaseHygieneEvidenceReport): void {
  const itemRows = report.evidenceItems
    .map((item) => {
      const currentEvidence = item.currentLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      const supplementalEvidence = item.supplementalLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      return `| \`${item.evidenceItemId}\` | \`${item.sourceProject}\` | \`${item.releaseHygieneCoverageClass}\` | ${currentEvidence} | ${supplementalEvidence} | ${item.protectedBoundary} |`
    })
    .join('\n')
  const checkRows = report.evidenceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`).join('\n')

  const markdown = `# OSS Release Hygiene Evidence Report

Generated by: \`bun run product:oss-release-hygiene-evidence\`

## Claim Boundary

- This report converts the \`release_hygiene\` safe backlog items into a local no-provider artifact, SBOM-shaped inventory, license-boundary, and release-claim boundary evidence matrix.
- It does not commit, push, publish, deploy, launch, sign provenance, make legal/NOTICE/REUSE decisions, call providers, call live models, call external services, or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.
- Every evidence item remains bounded to local fixture/report hashes until a later explicit protected authorization supplies a real git/release boundary and owner-approved release actions.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Evidence items: \`${report.evidenceItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`
- signed_provenance_generated: \`${report.signedProvenanceGenerated}\`
- release_readiness_claim_allowed: \`${report.releaseReadinessClaimAllowed}\`

## Evidence Items

| Evidence item | Source project | Coverage class | Source local evidence | Supplemental local evidence | Protected boundary |
| --- | --- | --- | --- | --- | --- |
${itemRows}

## Validation Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`
  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const sourceText = readText(sourceSafeBacklogPlanReportPath)
  const sourceReport = JSON.parse(sourceText) as SafeBacklogPlanReport
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'release_hygiene')
  const sourceGateCandidate = sourceReport.nextSafeInternalGateCandidates.find((candidate) => candidate.gateId === 'openclaude_internal_release_hygiene_evidence_gate')
  const expectedSourcePlanItemCount = sourceGateCandidate?.sourceBacklogItemCount ?? sourcePlanItems.length
  const evidenceItems = sourcePlanItems.map(toEvidenceItem)
  const sourceProjects = [...new Set(evidenceItems.map((item) => item.sourceProject))].sort()

  const jsonl = evidenceItems.map((item) => JSON.stringify(item)).join('\n') + '\n'
  writeFileSync(resolve(root, provenanceJsonlPath), jsonl)
  const provenanceText = readText(provenanceJsonlPath)
  const provenanceLines = provenanceText.trim().length === 0 ? [] : provenanceText.trim().split(/\r?\n/)
  const provenanceJsonlParseable = provenanceLines.every((line) => {
    try {
      JSON.parse(line)
      return true
    } catch {
      return false
    }
  })

  const allBindings = evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence])
  const coverageClasses = [...new Set(evidenceItems.map((item) => item.releaseHygieneCoverageClass))]
  const evidenceChecks = [
    check('source safe backlog plan is local no-provider', sourceReport.mode === 'local_no_provider_oss_safe_backlog_plan', sourceReport.mode),
    check('source safe backlog plan performed no provider/live/external/protected calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0 && sourceReport.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('selected release hygiene axis has source items', sourcePlanItems.length > 0 && sourcePlanItems.length === expectedSourcePlanItemCount, `${sourcePlanItems.length}/${expectedSourcePlanItemCount}`),
    check('source next gate candidate exists', sourceGateCandidate?.protectedActionRequiredForPlanning === false, 'openclaude_internal_release_hygiene_evidence_gate'),
    check('every evidence item has hash-bound local evidence', allBindings.length > 0 && allBindings.every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${allBindings.length} bindings`),
    check('coverage includes artifact reproducibility and release-claim boundaries', ['local_artifact_reproducibility_sbom_license_gate', 'signed_provenance_publish_release_claim_boundary'].every((coverage) => coverageClasses.includes(coverage as ReleaseHygieneCoverageClass)), coverageClasses.join(',')),
    check('every evidence item rejects release and protected-action expansion', evidenceItems.every((item) => item.commitAllowed === false && item.pushAllowed === false && item.publishAllowed === false && item.deployAllowed === false && item.launchAllowed === false && item.signedProvenanceClaimAllowed === false && item.legalNoticeReuseDecisionAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.publicReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${evidenceItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === evidenceItems.length, `${provenanceLines.length}/${evidenceItems.length}`),
  ]

  const report: ReleaseHygieneEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_release_hygiene_evidence',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'release_hygiene',
    sourcePlanItemCount: sourcePlanItems.length,
    evidenceItemCount: evidenceItems.length,
    sourceProjects,
    provenanceJsonlPath,
    provenanceJsonlSha256: sha256(provenanceText),
    provenanceJsonlRecordCount: provenanceLines.length,
    provenanceJsonlParseable,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    commitAllowed: false,
    pushAllowed: false,
    publishAllowed: false,
    deployAllowed: false,
    launchAllowed: false,
    signedProvenanceGenerated: false,
    signedProvenanceClaimAllowed: false,
    legalNoticeReuseDecisionAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: sourceProjects.map((sourceProject) => {
      const sourceUrl = evidenceItems.find((item) => item.sourceProject === sourceProject)?.sourceUrl ?? ''
      return {
        sourceProject,
        sourceUrl,
        observedPattern: 'Release hygiene evidence should bind reproducible local artifacts, SBOM-shaped inventory, license-boundary authorization, and signed/publish/deploy claim blockers before release claims.',
        localAbsorption: 'Convert release_hygiene backlog items into a source-hash-addressed local artifact and release-claim boundary evidence matrix.',
      }
    }),
    evidenceItems,
    evidenceChecks,
    claimBoundary: 'Internal no-provider release hygiene evidence only; not a commit, push, publish, deploy, launch, signed provenance, legal/NOTICE/REUSE decision, release readiness, production readiness, public readiness, external validation, or autonomous reliability claim.',
  }

  writeFileSync(resolve(root, reportJsonPath), JSON.stringify(report, null, 2) + '\n')
  writeMarkdown(report)

  for (const item of evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  const failed = evidenceChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`source_plan_item_count=${report.sourcePlanItemCount}`)
  console.log(`evidence_item_count=${report.evidenceItemCount}`)
  console.log(`evidence_binding_count=${allBindings.length}`)
  console.log(`provenance_jsonl_path=${report.provenanceJsonlPath}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`release_readiness_claim_allowed=${report.releaseReadinessClaimAllowed}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
