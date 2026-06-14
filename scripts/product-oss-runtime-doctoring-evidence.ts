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
  category: string
  currentLocalEvidence: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  recommendedNextGateId: string
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

type RuntimeDoctoringEvidenceItem = {
  evidenceItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'runtime_doctoring'
  backlogText: string
  runtimeDoctoringCoverageClass: 'protected_install_path_blocker_fixture' | 'diagnosis_without_repair_boundary'
  currentLocalEvidence: EvidenceBinding[]
  requiredEvidenceBeforeRepairClaim: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  implementationStatus: 'runtime_doctoring_evidence_matrix_created_internal_no_provider'
  protectedActionRequiredForEvidenceMatrix: false
  protectedActionExecuted: false
  repairActionAllowed: false
  reinstallActionAllowed: false
  dependencyInstallAllowed: false
  providerProbeAllowed: false
  externalDiagnosticsAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type RuntimeDoctoringEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_runtime_doctoring_evidence'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'runtime_doctoring'
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
  repairActionAllowed: false
  reinstallActionAllowed: false
  dependencyInstallAllowed: false
  providerProbeAllowed: false
  externalDiagnosticsAllowed: false
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
  evidenceItems: RuntimeDoctoringEvidenceItem[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-runtime-doctoring-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-runtime-doctoring-evidence-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-runtime-doctoring-evidence.jsonl'

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
  if (!existsSync(absolutePath)) return { path, exists: false, sha256: null, sizeBytes: 0 }
  const content = readFileSync(absolutePath)
  return { path, exists: true, sha256: sha256(content), sizeBytes: content.byteLength }
}

function coverageClass(item: SafeBacklogPlanItem): RuntimeDoctoringEvidenceItem['runtimeDoctoringCoverageClass'] {
  return item.backlogText.toLowerCase().includes('repair')
    ? 'diagnosis_without_repair_boundary'
    : 'protected_install_path_blocker_fixture'
}

function toEvidenceItem(item: SafeBacklogPlanItem): RuntimeDoctoringEvidenceItem {
  return {
    evidenceItemId: `oss_runtime_doctoring_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'runtime_doctoring',
    backlogText: item.backlogText,
    runtimeDoctoringCoverageClass: coverageClass(item),
    currentLocalEvidence: item.currentLocalEvidence.map(bindEvidence),
    requiredEvidenceBeforeRepairClaim: [
      'runtime doctor regression fixture evidence',
      'VS Code startup diagnostics evidence for local install/PATH blockers',
      'explicit owner authorization before repair, reinstall, dependency install, provider probe, or external diagnostic action',
      'post-repair smoke evidence before any availability, release, production, external-validation, or autonomous-reliability claim',
    ],
    unresolvedEvidenceGap: item.unresolvedEvidenceGap,
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    implementationStatus: 'runtime_doctoring_evidence_matrix_created_internal_no_provider',
    protectedActionRequiredForEvidenceMatrix: false,
    protectedActionExecuted: false,
    repairActionAllowed: false,
    reinstallActionAllowed: false,
    dependencyInstallAllowed: false,
    providerProbeAllowed: false,
    externalDiagnosticsAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: RuntimeDoctoringEvidenceReport): void {
  const itemRows = report.evidenceItems
    .map((item) => {
      const evidence = item.currentLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      return `| \`${item.evidenceItemId}\` | \`${item.sourceProject}\` | \`${item.runtimeDoctoringCoverageClass}\` | ${evidence} | ${item.protectedBoundary} |`
    })
    .join('\n')
  const checkRows = report.evidenceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`).join('\n')

  const markdown = `# OSS Runtime Doctoring Evidence Report

Generated by: \`bun run product:oss-runtime-doctoring-evidence\`

## Claim Boundary

- This report converts the \`runtime_doctoring\` safe backlog items into a local no-provider runtime diagnosis evidence matrix.
- It does not repair local install/PATH state, reinstall VS Code, install dependencies, call providers, call live models, call external diagnostics, mutate production systems, publish, deploy, launch, or claim release readiness, production readiness, external validation, public readiness, or autonomous reliability.
- Every evidence item remains bounded to local diagnostic/report hashes until a later explicit protected authorization supplies missing evidence.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Evidence items: \`${report.evidenceItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`

## Evidence Items

| Evidence item | Source project | Coverage class | Current local evidence | Protected boundary |
| --- | --- | --- | --- | --- |
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
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'runtime_doctoring')
  const sourceGateCandidate = sourceReport.nextSafeInternalGateCandidates.find((candidate) => candidate.gateId === 'openclaude_internal_runtime_doctoring_evidence_gate')
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

  const allBindings = evidenceItems.flatMap((item) => item.currentLocalEvidence)
  const evidenceChecks = [
    check('source safe backlog plan is local no-provider', sourceReport.mode === 'local_no_provider_oss_safe_backlog_plan', sourceReport.mode),
    check('source safe backlog plan performed no provider/live/external/protected calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0 && sourceReport.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('selected runtime doctoring axis has source items', sourcePlanItems.length > 0 && sourcePlanItems.length === expectedSourcePlanItemCount, `${sourcePlanItems.length}/${expectedSourcePlanItemCount}`),
    check('source next gate candidate exists', sourceGateCandidate?.protectedActionRequiredForPlanning === false, 'openclaude_internal_runtime_doctoring_evidence_gate'),
    check('every evidence item has hash-bound local evidence', allBindings.length > 0 && allBindings.every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${allBindings.length} bindings`),
    check('coverage includes blocker fixture and diagnosis-only classes', ['protected_install_path_blocker_fixture', 'diagnosis_without_repair_boundary'].every((coverage) => evidenceItems.some((item) => item.runtimeDoctoringCoverageClass === coverage)), [...new Set(evidenceItems.map((item) => item.runtimeDoctoringCoverageClass))].join(',')),
    check('every evidence item rejects repair and claim expansion', evidenceItems.every((item) => item.repairActionAllowed === false && item.reinstallActionAllowed === false && item.dependencyInstallAllowed === false && item.providerProbeAllowed === false && item.externalDiagnosticsAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${evidenceItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === evidenceItems.length, `${provenanceLines.length}/${evidenceItems.length}`),
  ]

  const report: RuntimeDoctoringEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_runtime_doctoring_evidence',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'runtime_doctoring',
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
    repairActionAllowed: false,
    reinstallActionAllowed: false,
    dependencyInstallAllowed: false,
    providerProbeAllowed: false,
    externalDiagnosticsAllowed: false,
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
        observedPattern: 'Runtime doctoring should separate diagnostic evidence from protected repair, reinstall, dependency install, provider probe, and external diagnostic actions.',
        localAbsorption: 'Convert runtime_doctoring backlog items into a source-hash-addressed runtime doctor evidence matrix.',
      }
    }),
    evidenceItems,
    evidenceChecks,
    claimBoundary: 'Internal no-provider runtime doctoring evidence only; not local repair, reinstall, dependency install, provider probe, external diagnostics, release readiness, production readiness, external validation, or autonomous reliability evidence.',
  }

  writeFileSync(resolve(root, reportJsonPath), JSON.stringify(report, null, 2) + '\n')
  writeMarkdown(report)

  for (const item of evidenceChecks) console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
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

  if (failed.length > 0) process.exit(1)
}

main()
