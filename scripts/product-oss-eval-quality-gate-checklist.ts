import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

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
  implementationStatus: string
  protectedActionRequiredForPlanning: boolean
  protectedActionExecuted: boolean
  claimAllowed: boolean
}

type SafeBacklogPlanReport = {
  mode: string
  sourceAxisArchitectureReviewReportPath: string
  plannedBacklogItemCount: number
  nextSafeInternalGateCandidates: Array<{
    gateId: string
    axis: string
    sourceBacklogItemCount: number
    protectedActionRequiredForPlanning: boolean
  }>
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  planItems: SafeBacklogPlanItem[]
}

type QualityGateChecklistItem = {
  checklistItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'eval_and_quality_gates'
  backlogText: string
  requiredGateRule: string
  rejectionCondition: string
  requiredEvidenceBeforeClaim: string[]
  protectedBoundary: string
  forbiddenShortcuts: string[]
  currentLocalEvidence: string[]
  implementationStatus: 'checklist_created_internal_no_provider'
  protectedActionRequiredForChecklist: false
  protectedActionExecuted: false
  publicBenchmarkClaimAllowed: false
  leaderboardClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type EvalQualityGateChecklistReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_eval_quality_gate_checklist'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'eval_and_quality_gates'
  sourcePlanItemCount: number
  checklistItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  publicBenchmarkClaimAllowed: false
  leaderboardClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
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
  checklistItems: QualityGateChecklistItem[]
  checklistChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-eval-quality-gate-checklist-report.json'
const reportMdPath = 'docs/product-quality/oss-eval-quality-gate-checklist-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-eval-quality-gate-checklist.jsonl'

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

function requiredGateRule(backlogText: string): string {
  const text = backlogText.toLowerCase()
  if (text.includes('leaderboard') || text.includes('superiority')) {
    return 'Reject leaderboard, superiority, or public comparison claims unless protected external benchmark authorization and result evidence are present.'
  }
  if (text.includes('quality-gate')) {
    return 'Require each product-quality gate to preserve local no-provider evidence status and explicit protected-action blockers.'
  }
  return 'Reject public benchmark claims unless external benchmark execution, submission, and claim authorization are separately approved.'
}

function rejectionCondition(backlogText: string): string {
  const text = backlogText.toLowerCase()
  if (text.includes('leaderboard')) return 'Fail if local planning evidence is converted into a leaderboard or public benchmark result claim.'
  if (text.includes('superiority')) return 'Fail if local source review or backlog evidence is converted into a superiority claim.'
  if (text.includes('quality-gate')) return 'Fail if a gate passes while provider/live/external calls, protected actions, or readiness claims are unblocked.'
  return 'Fail if benchmark readiness is claimed from local artifacts without external execution authorization.'
}

function toChecklistItem(item: SafeBacklogPlanItem): QualityGateChecklistItem {
  return {
    checklistItemId: `oss_eval_quality_gate_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'eval_and_quality_gates',
    backlogText: item.backlogText,
    requiredGateRule: requiredGateRule(item.backlogText),
    rejectionCondition: rejectionCondition(item.backlogText),
    requiredEvidenceBeforeClaim: [
      'accepted local product-quality gate evidence',
      'source-hash-addressed benchmark or quality evidence',
      'explicit protected-action authorization for any external benchmark/provider/live-model step',
      'explicit owner authorization before public comparison, leaderboard, superiority, release, production, external-validation, or autonomous-reliability claims',
    ],
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    currentLocalEvidence: item.currentLocalEvidence,
    implementationStatus: 'checklist_created_internal_no_provider',
    protectedActionRequiredForChecklist: false,
    protectedActionExecuted: false,
    publicBenchmarkClaimAllowed: false,
    leaderboardClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: EvalQualityGateChecklistReport): void {
  const itemRows = report.checklistItems
    .map((item) => `| \`${item.checklistItemId}\` | \`${item.sourceProject}\` | ${item.requiredGateRule} | ${item.rejectionCondition} |`)
    .join('\n')
  const checkRows = report.checklistChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Eval And Quality Gate Checklist Report

Generated by: \`bun run product:oss-eval-quality-gate-checklist\`

## Claim Boundary

- This report converts the \`eval_and_quality_gates\` safe backlog items into local no-provider checklist rules.
- It does not run external benchmarks, submit leaderboard results, call providers, call live models, call external services, install dependencies, mutate production systems, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, public readiness, or autonomous reliability.
- Every checklist item rejects claim expansion until a later explicitly authorized protected action supplies the missing evidence.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Checklist items: \`${report.checklistItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`

## Checklist Items

| Checklist item | Source project | Required gate rule | Rejection condition |
| --- | --- | --- | --- |
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
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'eval_and_quality_gates')
  const sourceGateCandidate = sourceReport.nextSafeInternalGateCandidates.find((candidate) => candidate.gateId === 'openclaude_internal_eval_and_quality_gates_evidence_gate')
  const expectedSourcePlanItemCount = sourceGateCandidate?.sourceBacklogItemCount ?? sourcePlanItems.length
  const checklistItems = sourcePlanItems.map(toChecklistItem)
  const sourceProjects = [...new Set(checklistItems.map((item) => item.sourceProject))].sort()

  const jsonl = checklistItems.map((item) => JSON.stringify(item)).join('\n') + '\n'
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

  const checklistChecks = [
    check('source safe backlog plan is local no-provider', sourceReport.mode === 'local_no_provider_oss_safe_backlog_plan', sourceReport.mode),
    check('source safe backlog plan performed no provider/live/external/protected calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0 && sourceReport.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('selected eval quality axis has source items', sourcePlanItems.length > 0 && sourcePlanItems.length === expectedSourcePlanItemCount, `${sourcePlanItems.length}/${expectedSourcePlanItemCount}`),
    check('source next gate candidate exists', sourceGateCandidate?.protectedActionRequiredForPlanning === false, 'openclaude_internal_eval_and_quality_gates_evidence_gate'),
    check('every checklist item rejects claim expansion', checklistItems.every((item) => item.publicBenchmarkClaimAllowed === false && item.leaderboardClaimAllowed === false && item.superiorityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${checklistItems.length} items`),
    check('every checklist item preserves current local evidence and protected boundary', checklistItems.every((item) => item.currentLocalEvidence.length > 0 && item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0), `${checklistItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === checklistItems.length, `${provenanceLines.length}/${checklistItems.length}`),
  ]

  const report: EvalQualityGateChecklistReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_eval_quality_gate_checklist',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'eval_and_quality_gates',
    sourcePlanItemCount: sourcePlanItems.length,
    checklistItemCount: checklistItems.length,
    sourceProjects,
    provenanceJsonlPath,
    provenanceJsonlSha256: sha256(provenanceText),
    provenanceJsonlRecordCount: provenanceLines.length,
    provenanceJsonlParseable,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    publicBenchmarkClaimAllowed: false,
    leaderboardClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: sourceProjects.map((sourceProject) => {
      const sourceUrl = checklistItems.find((item) => item.sourceProject === sourceProject)?.sourceUrl ?? ''
      return {
        sourceProject,
        sourceUrl,
        observedPattern: 'OSS benchmark and quality-gate evidence must separate internal planning evidence from public benchmark, leaderboard, superiority, and readiness claims.',
        localAbsorption: 'Convert eval_and_quality_gates backlog items into checklist rejection rules enforced by the local product-quality gate.',
      }
    }),
    checklistItems,
    checklistChecks,
    claimBoundary: 'Internal no-provider checklist evidence only; not an external benchmark run, leaderboard submission, superiority claim, release readiness claim, production readiness claim, external validation claim, public readiness claim, or autonomous reliability claim.',
  }

  writeFileSync(resolve(root, reportJsonPath), JSON.stringify(report, null, 2) + '\n')
  writeMarkdown(report)

  for (const item of checklistChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  const failed = checklistChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`source_plan_item_count=${report.sourcePlanItemCount}`)
  console.log(`checklist_item_count=${report.checklistItemCount}`)
  console.log(`provenance_jsonl_path=${report.provenanceJsonlPath}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
