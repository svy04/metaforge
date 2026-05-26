import { createHash } from 'node:crypto'
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type AxisReviewRecord = {
  fullName: string
  sourceUrl: string
  axis: string
  currentLocalEvidence: string[]
  safeInternalImplementationBacklog: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  claimAllowed: false
  recordDigest: string
}

type AxisArchitectureReviewReport = {
  mode: 'local_no_provider_oss_axis_architecture_review'
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  reviewedHighPriorityProjects: string[]
  reviewedAxes: string[]
  safeInternalBacklogItemCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  axisReviewRecords: AxisReviewRecord[]
}

type BacklogPlanItem = {
  planItemId: string
  sourceProject: string
  sourceUrl: string
  axis: string
  backlogText: string
  category: string
  sourceRecordDigest: string
  currentLocalEvidence: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  recommendedNextGateId: string
  implementationStatus: 'planned_internal_no_provider'
  protectedActionRequiredForPlanning: false
  protectedActionExecuted: false
  claimAllowed: false
}

type NextSafeInternalGateCandidate = {
  gateId: string
  axis: string
  sourceBacklogItemCount: number
  purpose: string
  protectedActionRequiredForPlanning: false
  selectedNow: false
}

type OssSafeBacklogPlanReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_safe_backlog_plan'
  sourceAxisArchitectureReviewReportPath: string
  sourceAxisArchitectureReviewReportSha256: string
  sourceAxisArchitectureReviewProvenanceJsonlPath: string
  sourceAxisArchitectureReviewProvenanceJsonlSha256: string
  sourceSafeInternalBacklogItemCount: number
  plannedBacklogItemCount: number
  reviewedHighPriorityProjects: string[]
  reviewedAxes: string[]
  uniqueAxisCount: number
  categoryCounts: Record<string, number>
  nextSafeInternalGateCandidateCount: number
  nextSafeInternalGateCandidates: NextSafeInternalGateCandidate[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
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
  planItems: BacklogPlanItem[]
  planChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceAxisArchitectureReviewReportPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
const reportJsonPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportMdPath = 'docs/product-quality/oss-safe-backlog-plan-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-safe-backlog-plan.jsonl'

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

function categoryFor(axis: string, backlogText: string): string {
  const text = backlogText.toLowerCase()
  if (text.includes('benchmark') || text.includes('leaderboard') || text.includes('quality-gate')) return 'benchmark_claim_boundary'
  if (text.includes('provider') || text.includes('model')) return 'provider_surface'
  if (text.includes('terminal') || text.includes('transcript') || text.includes('doctor')) return 'terminal_runtime_surface'
  if (text.includes('trace') || text.includes('tool')) return 'tool_loop_traceability'
  if (text.includes('mock-host') || text.includes('webview') || text.includes('extension host') || text.includes('vs code')) return 'ide_surface_boundary'
  if (text.includes('release') || text.includes('artifact') || text.includes('sbom') || text.includes('license')) return 'release_hygiene'
  if (text.includes('onboarding') || text.includes('readme') || text.includes('quick-start')) return 'onboarding_evidence'
  if (text.includes('runtime') || text.includes('path') || text.includes('install')) return 'runtime_doctoring'
  if (text.includes('permission') || text.includes('security') || text.includes('scorecard') || text.includes('codeql')) return 'security_permission_boundary'
  return slug(axis)
}

function planItem(record: AxisReviewRecord, backlogText: string, index: number): BacklogPlanItem {
  const idSeed = `${record.fullName}:${record.axis}:${index}:${backlogText}`
  return {
    planItemId: `oss_backlog_${slug(record.fullName)}_${slug(record.axis)}_${index + 1}_${sha256(idSeed).slice(0, 10)}`,
    sourceProject: record.fullName,
    sourceUrl: record.sourceUrl,
    axis: record.axis,
    backlogText,
    category: categoryFor(record.axis, backlogText),
    sourceRecordDigest: record.recordDigest,
    currentLocalEvidence: record.currentLocalEvidence,
    unresolvedEvidenceGap: record.unresolvedEvidenceGap,
    protectedBoundary: record.protectedBoundary,
    forbiddenShortcuts: record.forbiddenShortcuts,
    recommendedNextGateId: `openclaude_internal_${slug(record.axis)}_evidence_gate`,
    implementationStatus: 'planned_internal_no_provider',
    protectedActionRequiredForPlanning: false,
    protectedActionExecuted: false,
    claimAllowed: false,
  }
}

function countCategories(items: BacklogPlanItem[]): Record<string, number> {
  return items.reduce<Record<string, number>>((counts, item) => {
    counts[item.category] = (counts[item.category] ?? 0) + 1
    return counts
  }, {})
}

function nextGateCandidates(items: BacklogPlanItem[], axes: string[]): NextSafeInternalGateCandidate[] {
  return axes.map((axis) => {
    const axisItems = items.filter((item) => item.axis === axis)
    return {
      gateId: `openclaude_internal_${slug(axis)}_evidence_gate`,
      axis,
      sourceBacklogItemCount: axisItems.length,
      purpose: `Create the next bounded no-provider evidence gate for ${axis} backlog items without executing protected actions or expanding claims.`,
      protectedActionRequiredForPlanning: false,
      selectedNow: false,
    }
  })
}

function writeMarkdown(report: OssSafeBacklogPlanReport): void {
  const categoryRows = Object.entries(report.categoryCounts)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([category, count]) => `| \`${category}\` | ${count} |`)
    .join('\n')
  const gateRows = report.nextSafeInternalGateCandidates
    .map((candidate) => `| \`${candidate.gateId}\` | \`${candidate.axis}\` | ${candidate.sourceBacklogItemCount} | \`${candidate.protectedActionRequiredForPlanning}\` |`)
    .join('\n')
  const itemRows = report.planItems
    .map((item) => `| \`${item.planItemId}\` | \`${item.sourceProject}\` | \`${item.axis}\` | \`${item.category}\` | ${item.backlogText} |`)
    .join('\n')
  const checkRows = report.planChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Safe Backlog Plan Report

Generated by: \`bun run product:oss-safe-backlog-plan\`

## Claim Boundary

- This report converts the high-priority OSS axis architecture review backlog into internal no-provider evidence-gate planning records.
- It does not clone repositories, install dependencies, call providers, call live models, call external services, mutate production OpenClaude, mutate real product repositories, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Every backlog item remains candidate planning evidence until a later bounded gate implements and verifies it.

## Summary

- mode: \`${report.mode}\`
- source_axis_architecture_review_report_path: \`${report.sourceAxisArchitectureReviewReportPath}\`
- source_safe_internal_backlog_item_count: \`${report.sourceSafeInternalBacklogItemCount}\`
- planned_backlog_item_count: \`${report.plannedBacklogItemCount}\`
- unique_axis_count: \`${report.uniqueAxisCount}\`
- next_safe_internal_gate_candidate_count: \`${report.nextSafeInternalGateCandidateCount}\`
- provider_calls_performed: \`${report.providerCallsPerformed.length}\`
- live_model_calls_performed: \`${report.liveModelCallsPerformed.length}\`
- external_calls_performed: \`${report.externalCallsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`

## Categories

| Category | Count |
| --- | ---: |
${categoryRows}

## Next Safe Internal Gate Candidates

| Gate | Axis | Backlog Items | Protected Action Required For Planning |
| --- | --- | ---: | --- |
${gateRows}

## Backlog Plan Items

| Item | Source | Axis | Category | Backlog |
| --- | --- | --- | --- | --- |
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

  const sourceText = readText(sourceAxisArchitectureReviewReportPath)
  const source = JSON.parse(sourceText) as AxisArchitectureReviewReport
  const planItems = source.axisReviewRecords.flatMap((record) =>
    record.safeInternalImplementationBacklog.map((item, index) => planItem(record, item, index)),
  )
  const provenanceText = `${planItems.map((item) => JSON.stringify(item)).join('\n')}\n`
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceText)

  const sourceProvenanceText = readText(source.provenanceJsonlPath)
  const gateCandidates = nextGateCandidates(planItems, source.reviewedAxes)
  const categoryCounts = countCategories(planItems)
  const provenanceParseable = provenanceText.trim().split(/\r?\n/).every((line) => {
    try {
      JSON.parse(line)
      return true
    } catch {
      return false
    }
  })

  const checks = [
    check('source axis review is local no-provider', source.mode === 'local_no_provider_oss_axis_architecture_review', source.mode),
    check('source axis review performed no provider/live/external/protected calls', source.providerCallsPerformed.length === 0 && source.liveModelCallsPerformed.length === 0 && source.externalCallsPerformed.length === 0 && source.protectedActionsExecuted.length === 0, 'all source call/action arrays empty'),
    check('planned backlog count matches source count', planItems.length === source.safeInternalBacklogItemCount, `${planItems.length}/${source.safeInternalBacklogItemCount}`),
    check('every plan item preserves source evidence and boundary', planItems.every((item) => item.currentLocalEvidence.length > 0 && item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0), `${planItems.length} items`),
    check('every plan item remains internal no-provider planning', planItems.every((item) => item.implementationStatus === 'planned_internal_no_provider' && !item.protectedActionRequiredForPlanning && !item.protectedActionExecuted && !item.claimAllowed), 'all false for protected execution and claims'),
    check('next gate candidates cover reviewed axes', gateCandidates.length === source.reviewedAxes.length && gateCandidates.every((candidate) => candidate.sourceBacklogItemCount > 0), `${gateCandidates.length}/${source.reviewedAxes.length}`),
    check('category classification covers multiple product-quality surfaces', Object.keys(categoryCounts).length >= 6, Object.keys(categoryCounts).sort().join(',')),
    check('claim expansion remains blocked', source.publicComparisonClaimAllowed === false && source.superiorityClaimAllowed === false && source.releaseReadinessClaimAllowed === false && source.productionReadinessClaimAllowed === false && source.publicReadinessClaimAllowed === false && source.externalValidationClaimAllowed === false && source.autonomousReliabilityClaimAllowed === false, 'source claim flags false'),
    check('provenance JSONL is parseable', provenanceParseable, provenanceJsonlPath),
  ]

  const report: OssSafeBacklogPlanReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_safe_backlog_plan',
    sourceAxisArchitectureReviewReportPath,
    sourceAxisArchitectureReviewReportSha256: sha256(sourceText),
    sourceAxisArchitectureReviewProvenanceJsonlPath: source.provenanceJsonlPath,
    sourceAxisArchitectureReviewProvenanceJsonlSha256: sha256(sourceProvenanceText),
    sourceSafeInternalBacklogItemCount: source.safeInternalBacklogItemCount,
    plannedBacklogItemCount: planItems.length,
    reviewedHighPriorityProjects: source.reviewedHighPriorityProjects,
    reviewedAxes: source.reviewedAxes,
    uniqueAxisCount: source.reviewedAxes.length,
    categoryCounts,
    nextSafeInternalGateCandidateCount: gateCandidates.length,
    nextSafeInternalGateCandidates: gateCandidates,
    provenanceJsonlPath,
    provenanceJsonlSha256: sha256(provenanceText),
    provenanceJsonlRecordCount: planItems.length,
    provenanceJsonlParseable: provenanceParseable,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: [
      {
        sourceProject: 'ultraworkers/claw-code',
        sourceUrl: 'https://github.com/ultraworkers/claw-code',
        observedPattern: 'Claw Code exposes doctor, usage, parity, and Windows-first verification surfaces as first-class product evidence.',
        localAbsorption: 'OpenClaude preserves high-priority backlog items as bounded evidence-gate candidates before implementation claims.',
      },
      {
        sourceProject: 'warpdotdev/warp',
        sourceUrl: 'https://github.com/warpdotdev/warp',
        observedPattern: 'Warp positions terminal workflows as an agentic development surface that needs auditable local evidence.',
        localAbsorption: 'OpenClaude categorizes terminal and recovery backlog items into local no-provider evidence gates.',
      },
      {
        sourceProject: 'ruvnet/ruflo',
        sourceUrl: 'https://github.com/ruvnet/ruflo',
        observedPattern: 'Ruflo positions agent orchestration as a coordinated workflow surface, requiring explicit boundaries around multi-agent claims.',
        localAbsorption: 'OpenClaude maps orchestration and reliability backlog items to future internal gates without expanding autonomous reliability claims.',
      },
    ],
    planItems,
    planChecks: checks,
    claimBoundary: 'OSS safe backlog planning is internal local no-provider planning evidence only. It does not execute backlog items, protected actions, external validation, public comparison, release readiness, production readiness, or autonomous reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  const failed = checks.filter((item) => !item.ok)
  console.log('')
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log(`planned_backlog_item_count=${report.plannedBacklogItemCount}`)
  console.log(`next_safe_internal_gate_candidate_count=${report.nextSafeInternalGateCandidateCount}`)
  console.log(`provenance_jsonl_path=${report.provenanceJsonlPath}`)
  console.log('provider_calls_performed=0')
  console.log('live_model_calls_performed=0')
  console.log('external_calls_performed=0')
  console.log('protected_actions_executed=0')
}

main()
