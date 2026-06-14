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

type ToolLoopCoverageClass =
  | 'disposable_code_editing_trace_reliability'
  | 'trace_redaction_portability_boundary'

type ToolLoopReliabilityEvidenceItem = {
  evidenceItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'tool_loop_reliability'
  backlogText: string
  toolLoopCoverageClass: ToolLoopCoverageClass
  currentLocalEvidence: EvidenceBinding[]
  supplementalLocalEvidence: EvidenceBinding[]
  requiredEvidenceBeforeReliabilityClaim: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  implementationStatus: 'tool_loop_reliability_evidence_matrix_created_internal_no_provider'
  protectedActionRequiredForEvidenceMatrix: false
  protectedActionExecuted: false
  realProductRepoMutationAllowed: false
  providerBackedExecutionAllowed: false
  liveModelValidationAllowed: false
  externalBenchmarkExecutionAllowed: false
  nonSyntheticReliabilityClaimAllowed: false
  publicReliabilityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type ToolLoopReliabilityEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_tool_loop_reliability_evidence'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'tool_loop_reliability'
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
  realProductRepoMutationAllowed: false
  providerBackedExecutionAllowed: false
  liveModelValidationAllowed: false
  externalBenchmarkExecutionAllowed: false
  nonSyntheticReliabilityClaimAllowed: false
  publicReliabilityClaimAllowed: false
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
  evidenceItems: ToolLoopReliabilityEvidenceItem[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-tool-loop-reliability-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-tool-loop-reliability-evidence-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-tool-loop-reliability-evidence.jsonl'

const interruptionAndRepairEvidence = [
  'docs/product-quality/tool-interruption-recovery-trace-report.json',
  'docs/product-quality/protected-action-denial-trace-report.json',
  'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
  'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
]

const redactionAndPortabilityEvidence = [
  'docs/product-quality/real-session-trace-evals-report.json',
  'docs/product-quality/trace-schema-contract-report.json',
  'docs/product-quality/trace-portability-export-report.json',
  'docs/product-quality/trace-capture-redaction-policy-report.json',
  'reports/openclaude-portable-trace-events.jsonl',
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

function coverageClass(item: SafeBacklogPlanItem): ToolLoopCoverageClass {
  return item.backlogText.toLowerCase().includes('redaction') || item.backlogText.toLowerCase().includes('portable')
    ? 'trace_redaction_portability_boundary'
    : 'disposable_code_editing_trace_reliability'
}

function supplementalEvidencePaths(item: SafeBacklogPlanItem): string[] {
  return coverageClass(item) === 'trace_redaction_portability_boundary'
    ? redactionAndPortabilityEvidence
    : interruptionAndRepairEvidence
}

function toEvidenceItem(item: SafeBacklogPlanItem): ToolLoopReliabilityEvidenceItem {
  return {
    evidenceItemId: `oss_tool_loop_reliability_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'tool_loop_reliability',
    backlogText: item.backlogText,
    toolLoopCoverageClass: coverageClass(item),
    currentLocalEvidence: item.currentLocalEvidence.map(bindEvidence),
    supplementalLocalEvidence: supplementalEvidencePaths(item).map(bindEvidence),
    requiredEvidenceBeforeReliabilityClaim: [
      'fixture-bounded prompted tool-loop and code-editing trace evidence',
      'fixture-bounded multi-file, regression-cycle, interrupted-tool, and protected-action denial trace evidence',
      'trace eval, schema contract, portability export, and redaction policy evidence',
      'explicit owner authorization before real product repo mutation, provider-backed execution, live model validation, external benchmark execution, or reliability/readiness claims',
    ],
    unresolvedEvidenceGap: item.unresolvedEvidenceGap,
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    implementationStatus: 'tool_loop_reliability_evidence_matrix_created_internal_no_provider',
    protectedActionRequiredForEvidenceMatrix: false,
    protectedActionExecuted: false,
    realProductRepoMutationAllowed: false,
    providerBackedExecutionAllowed: false,
    liveModelValidationAllowed: false,
    externalBenchmarkExecutionAllowed: false,
    nonSyntheticReliabilityClaimAllowed: false,
    publicReliabilityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: ToolLoopReliabilityEvidenceReport): void {
  const itemRows = report.evidenceItems
    .map((item) => {
      const currentEvidence = item.currentLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      const supplementalEvidence = item.supplementalLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      return `| \`${item.evidenceItemId}\` | \`${item.sourceProject}\` | \`${item.toolLoopCoverageClass}\` | ${currentEvidence} | ${supplementalEvidence} | ${item.protectedBoundary} |`
    })
    .join('\n')
  const checkRows = report.evidenceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`).join('\n')

  const markdown = `# OSS Tool Loop Reliability Evidence Report

Generated by: \`bun run product:oss-tool-loop-reliability-evidence\`

## Claim Boundary

- This report converts the \`tool_loop_reliability\` safe backlog items into a local no-provider trace and tool-loop evidence matrix.
- It does not mutate real product repositories, call providers, call live models, execute external benchmarks, claim non-synthetic reliability, publish, deploy, launch, or claim release readiness, production readiness, public readiness, external validation, or autonomous reliability.
- Every evidence item remains bounded to local fixture/report hashes until a later explicit protected authorization supplies real-repo, provider-backed, or external benchmark evidence.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Evidence items: \`${report.evidenceItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`

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
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'tool_loop_reliability')
  const sourceGateCandidate = sourceReport.nextSafeInternalGateCandidates.find((candidate) => candidate.gateId === 'openclaude_internal_tool_loop_reliability_evidence_gate')
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
  const evidenceChecks = [
    check('source safe backlog plan is local no-provider', sourceReport.mode === 'local_no_provider_oss_safe_backlog_plan', sourceReport.mode),
    check('source safe backlog plan performed no provider/live/external/protected calls', sourceReport.providerCallsPerformed.length === 0 && sourceReport.liveModelCallsPerformed.length === 0 && sourceReport.externalCallsPerformed.length === 0 && sourceReport.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('selected tool loop reliability axis has source items', sourcePlanItems.length > 0 && sourcePlanItems.length === expectedSourcePlanItemCount, `${sourcePlanItems.length}/${expectedSourcePlanItemCount}`),
    check('source next gate candidate exists', sourceGateCandidate?.protectedActionRequiredForPlanning === false, 'openclaude_internal_tool_loop_reliability_evidence_gate'),
    check('every evidence item has hash-bound local evidence', allBindings.length > 0 && allBindings.every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${allBindings.length} bindings`),
    check('coverage includes tool repair and redaction portability classes', ['disposable_code_editing_trace_reliability', 'trace_redaction_portability_boundary'].every((coverage) => evidenceItems.some((item) => item.toolLoopCoverageClass === coverage)), [...new Set(evidenceItems.map((item) => item.toolLoopCoverageClass))].join(',')),
    check('every evidence item rejects reliability and protected-action expansion', evidenceItems.every((item) => item.realProductRepoMutationAllowed === false && item.providerBackedExecutionAllowed === false && item.liveModelValidationAllowed === false && item.externalBenchmarkExecutionAllowed === false && item.nonSyntheticReliabilityClaimAllowed === false && item.publicReliabilityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${evidenceItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === evidenceItems.length, `${provenanceLines.length}/${evidenceItems.length}`),
  ]

  const report: ToolLoopReliabilityEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_tool_loop_reliability_evidence',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'tool_loop_reliability',
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
    realProductRepoMutationAllowed: false,
    providerBackedExecutionAllowed: false,
    liveModelValidationAllowed: false,
    externalBenchmarkExecutionAllowed: false,
    nonSyntheticReliabilityClaimAllowed: false,
    publicReliabilityClaimAllowed: false,
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
        observedPattern: 'Tool-loop reliability evidence should preserve fixture-bounded repair traces, interrupted-tool recovery, redaction, and portable trace exports before stronger reliability claims.',
        localAbsorption: 'Convert tool_loop_reliability backlog items into a source-hash-addressed local trace and tool-loop evidence matrix.',
      }
    }),
    evidenceItems,
    evidenceChecks,
    claimBoundary: 'Internal no-provider tool-loop reliability evidence only; not real product repo repair, provider-backed execution, live model validation, external benchmark execution, public reliability, release readiness, production readiness, external validation, or autonomous reliability evidence.',
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

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
