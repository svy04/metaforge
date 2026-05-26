import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
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

type EvidenceBinding = {
  path: string
  exists: boolean
  sha256: string | null
  sizeBytes: number
}

type TerminalWorkflowEvidenceItem = {
  evidenceItemId: string
  sourcePlanItemId: string
  sourceProject: string
  sourceUrl: string
  axis: 'terminal_workflow'
  backlogText: string
  transcriptCoverageClass: 'first_run_failure_recovery_doctor_handoff' | 'command_hash_no_provider_boundary'
  currentLocalEvidence: EvidenceBinding[]
  requiredCoverageBeforeClaim: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  implementationStatus: 'terminal_workflow_evidence_matrix_created_internal_no_provider'
  protectedActionRequiredForEvidenceMatrix: false
  protectedActionExecuted: false
  nonSyntheticUserSessionClaimAllowed: false
  externalBenchmarkSessionClaimAllowed: false
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
}

type TerminalWorkflowEvidenceReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_terminal_workflow_evidence'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: 'terminal_workflow'
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
  nonSyntheticUserSessionClaimAllowed: false
  externalBenchmarkSessionClaimAllowed: false
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
  evidenceItems: TerminalWorkflowEvidenceItem[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-terminal-workflow-evidence-report.json'
const reportMdPath = 'docs/product-quality/oss-terminal-workflow-evidence-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-terminal-workflow-evidence.jsonl'

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
  return {
    path,
    exists: true,
    sha256: sha256(content),
    sizeBytes: content.byteLength,
  }
}

function coverageClass(item: SafeBacklogPlanItem): TerminalWorkflowEvidenceItem['transcriptCoverageClass'] {
  return item.backlogText.toLowerCase().includes('hash')
    ? 'command_hash_no_provider_boundary'
    : 'first_run_failure_recovery_doctor_handoff'
}

function toEvidenceItem(item: SafeBacklogPlanItem): TerminalWorkflowEvidenceItem {
  return {
    evidenceItemId: `oss_terminal_workflow_${slug(item.sourceProject)}_${sha256(item.planItemId).slice(0, 10)}`,
    sourcePlanItemId: item.planItemId,
    sourceProject: item.sourceProject,
    sourceUrl: item.sourceUrl,
    axis: 'terminal_workflow',
    backlogText: item.backlogText,
    transcriptCoverageClass: coverageClass(item),
    currentLocalEvidence: item.currentLocalEvidence.map(bindEvidence),
    requiredCoverageBeforeClaim: [
      'local first-run transcript evidence with command and output hashes',
      'local failure-recovery transcript evidence with command and output hashes',
      'local doctor handoff transcript evidence with command and output hashes',
      'explicit no-provider and no-external-call boundary fields',
      'explicit owner authorization before non-synthetic session, external benchmark, public comparison, superiority, release, production, external-validation, or autonomous-reliability claims',
    ],
    unresolvedEvidenceGap: item.unresolvedEvidenceGap,
    protectedBoundary: item.protectedBoundary,
    forbiddenShortcuts: item.forbiddenShortcuts,
    implementationStatus: 'terminal_workflow_evidence_matrix_created_internal_no_provider',
    protectedActionRequiredForEvidenceMatrix: false,
    protectedActionExecuted: false,
    nonSyntheticUserSessionClaimAllowed: false,
    externalBenchmarkSessionClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
  }
}

function writeMarkdown(report: TerminalWorkflowEvidenceReport): void {
  const itemRows = report.evidenceItems
    .map((item) => {
      const evidence = item.currentLocalEvidence.map((entry) => `\`${entry.path}\``).join('<br>')
      return `| \`${item.evidenceItemId}\` | \`${item.sourceProject}\` | \`${item.transcriptCoverageClass}\` | ${evidence} | ${item.unresolvedEvidenceGap} |`
    })
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Terminal Workflow Evidence Report

Generated by: \`bun run product:oss-terminal-workflow-evidence\`

## Claim Boundary

- This report converts the \`terminal_workflow\` safe backlog items into a local no-provider terminal workflow evidence matrix.
- It does not capture non-synthetic user sessions, run external benchmarks, call providers, call live models, call external services, install dependencies, mutate production systems, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, public readiness, or autonomous reliability.
- Every evidence item remains bounded to local transcript/report hashes until a later explicit protected authorization supplies missing evidence.

## Summary

- Source safe backlog plan: \`${report.sourceSafeBacklogPlanReportPath}\`
- Source plan items: \`${report.sourcePlanItemCount}\`
- Evidence items: \`${report.evidenceItemCount}\`
- Source projects: ${report.sourceProjects.map((item) => `\`${item}\``).join(', ')}
- Provenance JSONL: \`${report.provenanceJsonlPath}\`

## Evidence Items

| Evidence item | Source project | Coverage class | Current local evidence | Unresolved gap |
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
  const sourcePlanItems = sourceReport.planItems.filter((item) => item.axis === 'terminal_workflow')
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
    check('selected terminal workflow axis has source items', sourcePlanItems.length === 6, `${sourcePlanItems.length}/6`),
    check('source next gate candidate exists', sourceReport.nextSafeInternalGateCandidates.some((candidate) => candidate.gateId === 'openclaude_internal_terminal_workflow_evidence_gate' && candidate.protectedActionRequiredForPlanning === false), 'openclaude_internal_terminal_workflow_evidence_gate'),
    check('every evidence item has hash-bound local evidence', allBindings.length > 0 && allBindings.every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${allBindings.length} bindings`),
    check('coverage includes transcript and command-hash classes', ['first_run_failure_recovery_doctor_handoff', 'command_hash_no_provider_boundary'].every((coverage) => evidenceItems.some((item) => item.transcriptCoverageClass === coverage)), [...new Set(evidenceItems.map((item) => item.transcriptCoverageClass))].join(',')),
    check('every evidence item rejects claim expansion', evidenceItems.every((item) => item.nonSyntheticUserSessionClaimAllowed === false && item.externalBenchmarkSessionClaimAllowed === false && item.publicComparisonClaimAllowed === false && item.superiorityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false), `${evidenceItems.length} items`),
    check('provenance JSONL is parseable', provenanceJsonlParseable && provenanceLines.length === evidenceItems.length, `${provenanceLines.length}/${evidenceItems.length}`),
  ]

  const report: TerminalWorkflowEvidenceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_terminal_workflow_evidence',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewReportPath: sourceReport.sourceAxisArchitectureReviewReportPath,
    selectedAxis: 'terminal_workflow',
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
    nonSyntheticUserSessionClaimAllowed: false,
    externalBenchmarkSessionClaimAllowed: false,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
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
        observedPattern: 'Terminal workflow quality should bind first-run, failure recovery, doctor handoff, command hashes, and no-provider boundaries before stronger claims are made.',
        localAbsorption: 'Convert terminal_workflow backlog items into a source-hash-addressed terminal workflow evidence matrix.',
      }
    }),
    evidenceItems,
    evidenceChecks,
    claimBoundary: 'Internal no-provider terminal workflow evidence only; not a non-synthetic user-session capture, external benchmark run, public comparison, superiority claim, release readiness claim, production readiness claim, external validation claim, public readiness claim, or autonomous reliability claim.',
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
