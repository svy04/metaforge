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

type ProviderBreadthCoverageClass =
  | 'provider_capability_failure_mode_matrix'
  | 'provider_fallback_live_authorization_boundary'

type ProviderBreadthEvidenceItem = {
  evidenceItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'provider_breadth'
  backlogText: string
  providerBreadthCoverageClass: ProviderBreadthCoverageClass
  currentLocalEvidence: EvidenceBinding[]
  supplementalLocalEvidence: EvidenceBinding[]
  requiredEvidenceBeforeProviderClaim: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  implementationStatus: 'provider_breadth_evidence_matrix_created_internal_no_provider'
  protectedActionRequiredForEvidenceMatrix: false
  protectedActionExecuted: false
  providerCallsAllowed: false
  liveModelCallsAllowed: false
  externalCallsAllowed: false
  liveProviderValidationAllowed: false
  providerCompatibilityClaimAllowed: false
  modelBehaviorClaimAllowed: false
  providerBackedExecutionAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type ProviderBreadthEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_provider_breadth_evidence'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'provider_breadth'
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
  providerCallsAllowed: false
  liveModelCallsAllowed: false
  externalCallsAllowed: false
  liveProviderValidationAllowed: false
  providerCompatibilityClaimAllowed: false
  modelBehaviorClaimAllowed: false
  providerBackedExecutionAllowed: false
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
  evidenceItems: ProviderBreadthEvidenceItem[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-provider-breadth-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-provider-breadth-evidence-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-provider-breadth-evidence.jsonl'

const capabilityMatrixEvidence = [
  'docs/product-quality/provider-capability-matrix-report.json',
  'docs/product-quality/provider-capability-matrix-report.md',
  'docs/product-quality/provider-compatibility-fixtures.md',
]

const fallbackBoundaryEvidence = [
  'docs/product-quality/runtime-doctor-regression-fixtures.md',
  'docs/product-quality/oss-runtime-doctoring-evidence-report.json',
  'docs/product-quality/oss-runtime-doctoring-evidence-report.md',
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

function coverageClass(item: SafeBacklogPlanItem): ProviderBreadthCoverageClass {
  return item.backlogText.toLowerCase().includes('fallback')
    ? 'provider_fallback_live_authorization_boundary'
    : 'provider_capability_failure_mode_matrix'
}

function supplementalEvidencePaths(item: SafeBacklogPlanItem): string[] {
  return coverageClass(item) === 'provider_fallback_live_authorization_boundary'
    ? fallbackBoundaryEvidence
    : capabilityMatrixEvidence
}

function toEvidenceItem(item: SafeBacklogPlanItem): ProviderBreadthEvidenceItem {
  return {
    evidenceItemId: `oss_provider_breadth_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'provider_breadth',
    backlogText: item.backlogText,
    providerBreadthCoverageClass: coverageClass(item),
    currentLocalEvidence: item.currentLocalEvidence.map(bindEvidence),
    supplementalLocalEvidence: supplementalEvidencePaths(item).map(bindEvidence),
    requiredEvidenceBeforeProviderClaim: [
      'per-provider local capability and failure-mode rows',
      'runtime doctor and provider compatibility fixture evidence',
      'explicit owner authorization before provider calls, live model calls, external services, or live provider validation',
      'separate measured live-provider evidence before provider compatibility, model behavior, external validation, release, production, or autonomous reliability claims',
    ],
    unresolvedEvidenceGap: item.unresolvedEvidenceGap,
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    implementationStatus: 'provider_breadth_evidence_matrix_created_internal_no_provider',
    protectedActionRequiredForEvidenceMatrix: false,
    protectedActionExecuted: false,
    providerCallsAllowed: false,
    liveModelCallsAllowed: false,
    externalCallsAllowed: false,
    liveProviderValidationAllowed: false,
    providerCompatibilityClaimAllowed: false,
    modelBehaviorClaimAllowed: false,
    providerBackedExecutionAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: ProviderBreadthEvidenceReport): void {
  const itemRows = report.evidenceItems
    .map((item) => {
      const currentEvidence = item.currentLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      const supplementalEvidence = item.supplementalLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      return `| \`${item.evidenceItemId}\` | \`${item.sourceProject}\` | \`${item.providerBreadthCoverageClass}\` | ${currentEvidence} | ${supplementalEvidence} | ${item.protectedBoundary} |`
    })
    .join('\n')
  const checkRows = report.evidenceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`).join('\n')

  const markdown = `# OSS Provider Breadth Evidence Report

Generated by: \`bun run product:oss-provider-breadth-evidence\`

## Claim Boundary

- This report converts the \`provider_breadth\` safe backlog items into a local no-provider provider capability, failure-mode, runtime-doctor, and live-authorization boundary evidence matrix.
- It does not call providers, call live models, call external services, run live provider validation, or claim provider compatibility, model behavior, release readiness, production readiness, public readiness, external validation, or autonomous reliability.
- Every evidence item remains bounded to local fixture/report hashes until a later explicit protected authorization supplies measured live-provider evidence.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Evidence items: \`${report.evidenceItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`
- provider_calls_allowed: \`${report.providerCallsAllowed}\`
- live_model_calls_allowed: \`${report.liveModelCallsAllowed}\`
- provider_compatibility_claim_allowed: \`${report.providerCompatibilityClaimAllowed}\`

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
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'provider_breadth')
  const sourceGateCandidate = sourceReport.nextSafeInternalGateCandidates.find((candidate) => candidate.gateId === 'openclaude_internal_provider_breadth_evidence_gate' && candidate.axis === 'provider_breadth')
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
  const coverageClasses = [...new Set(evidenceItems.map((item) => item.providerBreadthCoverageClass))]
  const evidenceChecks = [
    check('source safe backlog plan is local no-provider', sourceReport.mode === 'local_no_provider_oss_safe_backlog_plan', sourceReport.mode),
    check('source safe backlog plan performed no provider/live/external/protected calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0 && sourceReport.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('selected provider breadth axis has source items', sourcePlanItems.length > 0 && sourcePlanItems.length === expectedSourcePlanItemCount, `${sourcePlanItems.length}/${expectedSourcePlanItemCount}`),
    check('source next gate candidate exists', sourceGateCandidate?.protectedActionRequiredForPlanning === false, 'openclaude_internal_provider_breadth_evidence_gate'),
    check('every evidence item has hash-bound local evidence', allBindings.length > 0 && allBindings.every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${allBindings.length} bindings`),
    check('coverage includes capability matrix and fallback authorization boundaries', ['provider_capability_failure_mode_matrix', 'provider_fallback_live_authorization_boundary'].every((coverage) => coverageClasses.includes(coverage as ProviderBreadthCoverageClass)), coverageClasses.join(',')),
    check('every evidence item rejects provider and claim expansion', evidenceItems.every((item) => item.providerCallsAllowed === false && item.liveModelCallsAllowed === false && item.externalCallsAllowed === false && item.liveProviderValidationAllowed === false && item.providerCompatibilityClaimAllowed === false && item.modelBehaviorClaimAllowed === false && item.providerBackedExecutionAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.publicReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${evidenceItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === evidenceItems.length, `${provenanceLines.length}/${evidenceItems.length}`),
  ]

  const report: ProviderBreadthEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_provider_breadth_evidence',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'provider_breadth',
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
    providerCallsAllowed: false,
    liveModelCallsAllowed: false,
    externalCallsAllowed: false,
    liveProviderValidationAllowed: false,
    providerCompatibilityClaimAllowed: false,
    modelBehaviorClaimAllowed: false,
    providerBackedExecutionAllowed: false,
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
        observedPattern: 'Provider breadth evidence should preserve per-provider capability/failure-mode rows and provider fallback boundaries before any live-provider validation or compatibility claim.',
        localAbsorption: 'Convert provider_breadth backlog items into a source-hash-addressed local capability and live-authorization boundary evidence matrix.',
      }
    }),
    evidenceItems,
    evidenceChecks,
    claimBoundary: 'Internal no-provider provider breadth evidence only; not provider calls, live model calls, live provider validation, provider compatibility evidence, model behavior evidence, release readiness, production readiness, public readiness, external validation, or autonomous reliability evidence.',
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
  console.log(`provider_compatibility_claim_allowed=${report.providerCompatibilityClaimAllowed}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
