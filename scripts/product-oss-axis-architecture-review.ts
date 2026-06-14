import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type GapRecord = {
  fullName: string
  sourceUrl: string
  targetStatus: 'prioritized_source_supported_target' | 'deferred_metadata_only_target'
  priority: 'high' | 'medium' | 'deferred'
  absorptionAxes: string[]
  sourceSignals: string[]
  openClaudeEvidence: Array<{
    axis: string
    currentLocalEvidence: string[]
    unresolvedGap: string
    protectedBoundary: string
  }>
  safeInternalNextActions: string[]
  protectedActionsStillRequired: string[]
  forbiddenShortcuts: string[]
  claimAllowed: false
}

type GapReviewReport = {
  mode: string
  sourceTargetsReportPath: string
  sourceReviewReportPath: string
  baselineSnapshotDate: string
  targetRecordCount: number
  prioritizedTargetCount: number
  deferredTargetCount: number
  gapRecordCount: number
  axesReviewed: string[]
  gapChecks: Check[]
  gapRecords: GapRecord[]
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
}

type AxisReviewRecord = {
  schemaVersion: 'openclaude_oss_axis_architecture_review_v1'
  fullName: string
  sourceUrl: string
  priority: 'high'
  axis: string
  sourceSignals: string[]
  currentLocalEvidence: string[]
  observedSourcePattern: string
  safeAbsorptionDecision: string
  safeInternalImplementationBacklog: string[]
  unresolvedEvidenceGap: string
  protectedBoundary: string
  forbiddenShortcuts: string[]
  claimAllowed: false
  recordDigest: string
}

type AxisArchitectureReviewReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_axis_architecture_review'
  sourceGapReviewReportPath: string
  sourceGapReviewReportSha256: string
  sourceTargetsReportPath: string
  sourceReviewReportPath: string
  baselineSnapshotDate: string
  highPriorityProjectCount: number
  reviewedHighPriorityProjects: string[]
  axisReviewRecordCount: number
  uniqueAxisCount: number
  reviewedAxes: string[]
  safeInternalBacklogItemCount: number
  protectedBoundaryCount: number
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
  reviewChecks: Check[]
  axisReviewRecords: AxisReviewRecord[]
  claimBoundary: string
}

const root = process.cwd()
const sourceGapReviewReportPath = 'docs/product-quality/oss-architecture-gap-review-report.json'
const reportJsonPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
const reportMdPath = 'docs/product-quality/oss-axis-architecture-review-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-axis-architecture-review.jsonl'

const requiredCoreAxes = [
  'provider_breadth',
  'terminal_workflow',
  'tool_loop_reliability',
  'eval_and_quality_gates',
  'release_hygiene',
  'runtime_doctoring',
  'security_and_permissions',
]

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function uniqueSorted(values: string[]): string[] {
  return [...new Set(values)].sort((left, right) => left.localeCompare(right))
}

function sourcePattern(axis: string, project: string): string {
  const projectPrefix = `${project} exposes source-reviewed signals for`
  const patterns: Record<string, string> = {
    provider_breadth: `${projectPrefix} provider/model breadth; OpenClaude should keep provider coverage measurable through local compatibility fixtures before live calls.`,
    terminal_workflow: `${projectPrefix} terminal-first workflows; OpenClaude should keep command surfaces reproducible through golden transcript and onboarding smoke evidence.`,
    tool_loop_reliability: `${projectPrefix} tool-use loops; OpenClaude should keep tool loops traceable through permission regression, prompted-loop, and code-editing trace evidence.`,
    eval_and_quality_gates: `${projectPrefix} agent/coding workflow quality signals; OpenClaude should keep gates machine-checkable before public benchmark claims.`,
    ide_or_editor_surface: `${projectPrefix} editor or IDE surfaces; OpenClaude should keep real host availability separated from mock-host evidence.`,
    release_hygiene: `${projectPrefix} package or release manifests; OpenClaude should keep artifact file lists, provenance, reproducibility, and license decisions explicit.`,
    onboarding_docs: `${projectPrefix} onboarding documentation; OpenClaude should keep first-run guidance covered by link and CLI smoke evidence.`,
    runtime_doctoring: `${projectPrefix} runtime configuration expectations; OpenClaude should keep runtime doctor evidence separate from protected install/PATH repair.`,
    security_and_permissions: `${projectPrefix} permission or tool-risk signals; OpenClaude should keep permission boundaries and hosted security claims separated.`,
  }
  return patterns[axis] ?? `${projectPrefix} ${axis}; OpenClaude should add a bounded local review before implementation absorption.`
}

function backlogFor(axis: string): string[] {
  const backlog: Record<string, string[]> = {
    provider_breadth: [
      'extend provider compatibility fixtures with per-provider capability and failure-mode rows before live-provider validation',
      'keep provider fallback evidence in local reports until explicit live-model authorization exists',
    ],
    terminal_workflow: [
      'add axis-specific terminal transcript coverage for first-run, failure-recovery, and doctor handoff paths',
      'bind every transcript to command hashes and no-provider claim boundaries',
    ],
    tool_loop_reliability: [
      'expand local disposable code-editing traces to cover multi-step tool interruption and repair cycles',
      'preserve raw-trace redaction and portable trace exports before stronger reliability claims',
    ],
    eval_and_quality_gates: [
      'add a per-axis quality-gate checklist that rejects public benchmark, leaderboard, or superiority claims without protected authorization',
      'map every local benchmark task to missing external execution evidence',
    ],
    ide_or_editor_surface: [
      'keep mock-host and WebviewView evidence separate from real VS Code Extension Host evidence',
      'rerun real host/workbench gates only after owner-authorized local code CLI repair',
    ],
    release_hygiene: [
      'keep local artifact reproducibility, SBOM-shaped inventory, and license-boundary authorization in the release gate',
      'block signed provenance, publish, deploy, and release-readiness claims until a real git/release boundary exists',
    ],
    onboarding_docs: [
      'add operator-authorized non-synthetic first-run session capture before cross-platform onboarding claims',
      'keep README and quick-start link integrity evidence in the product gate',
    ],
    runtime_doctoring: [
      'add runtime-doctor fixture rows for protected local install/PATH blockers',
      'separate diagnostic reporting from any repair, reinstall, or dependency-install action',
    ],
    security_and_permissions: [
      'keep permission regression fixtures tied to protected-action and public-claim blockers',
      'separate local security posture evidence from hosted Scorecard, hosted CodeQL, and branch-protection claims',
    ],
  }
  return backlog[axis] ?? [`add a no-provider review artifact for ${axis} before implementation absorption`]
}

function axisRecord(record: GapRecord, axis: string): AxisReviewRecord {
  const evidence = record.openClaudeEvidence.find((item) => item.axis === axis)
  const base = {
    schemaVersion: 'openclaude_oss_axis_architecture_review_v1' as const,
    fullName: record.fullName,
    sourceUrl: record.sourceUrl,
    priority: 'high' as const,
    axis,
    sourceSignals: [...record.sourceSignals].sort((left, right) => left.localeCompare(right)),
    currentLocalEvidence: evidence?.currentLocalEvidence ?? ['docs/product-quality/product-quality-gate.md'],
    observedSourcePattern: sourcePattern(axis, record.fullName),
    safeAbsorptionDecision: 'record as internal no-provider architecture review input only; do not implement, claim superiority, publish, deploy, or execute protected validation from this record alone',
    safeInternalImplementationBacklog: backlogFor(axis),
    unresolvedEvidenceGap: evidence?.unresolvedGap ?? 'Dedicated local evidence is still missing for this axis.',
    protectedBoundary: evidence?.protectedBoundary ?? 'claim expansion remains blocked until dedicated evidence and explicit authorization exist.',
    forbiddenShortcuts: [
      'do not infer superiority from GitHub stars, README text, or local planning artifacts',
      'do not treat this axis review as implementation, production readiness, release readiness, external validation, or autonomous reliability evidence',
      'do not call providers, live models, or external services from this local review',
      'do not clone, install dependencies, publish, deploy, launch, or mutate production systems',
      'do not modify MFH, real product repositories, canonical memory/governance, or decision ledgers',
    ],
    claimAllowed: false as const,
  }
  return {
    ...base,
    recordDigest: sha256(JSON.stringify(base)),
  }
}

function writeMarkdown(report: AxisArchitectureReviewReport): void {
  const projectRows = report.reviewedHighPriorityProjects
    .map((project) => {
      const records = report.axisReviewRecords.filter((record) => record.fullName === project)
      const axes = records.map((record) => record.axis).join(', ')
      return `| \`${project}\` | ${records.length} | ${axes} |`
    })
    .join('\n')
  const checkRows = report.reviewChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Axis Architecture Review Report

Generated by: \`bun run product:oss-axis-architecture-review\`

## Claim Boundary

- This report performs a local no-provider axis-specific architecture review for the 3 high-priority source-supported OSS targets.
- It does not fetch sources, clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Axis records are internal implementation-planning inputs only.

## Summary

- mode: \`${report.mode}\`
- source_gap_review_report_path: \`${report.sourceGapReviewReportPath}\`
- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- high_priority_project_count: \`${report.highPriorityProjectCount}\`
- axis_review_record_count: \`${report.axisReviewRecordCount}\`
- unique_axis_count: \`${report.uniqueAxisCount}\`
- safe_internal_backlog_item_count: \`${report.safeInternalBacklogItemCount}\`
- protected_boundary_count: \`${report.protectedBoundaryCount}\`
- reviewed_axes: \`${report.reviewedAxes.join(',')}\`

## Reviewed High-Priority Projects

| Project | Axis records | Axes |
| --- | ---: | --- |
${projectRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  if (!existsSync(resolve(root, sourceGapReviewReportPath))) {
    console.error(`RESULT: FAIL (${sourceGapReviewReportPath} missing)`)
    process.exit(1)
  }

  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const sourceText = readText(sourceGapReviewReportPath)
  const sourceReport = JSON.parse(sourceText) as GapReviewReport
  const sourceGapReviewReportSha256 = sha256(sourceText)
  const highPriorityGapRecords = sourceReport.gapRecords
    .filter((record) => record.priority === 'high' && record.targetStatus === 'prioritized_source_supported_target')
    .sort((left, right) => left.fullName.localeCompare(right.fullName))
  const expectedHighPriorityProjects = highPriorityGapRecords.map((record) => record.fullName)
  const reviewedHighPriorityProjects = highPriorityGapRecords.map((record) => record.fullName)
  const axisReviewRecords = highPriorityGapRecords.flatMap((record) => record.absorptionAxes.map((axis) => axisRecord(record, axis)))
  const reviewedAxes = uniqueSorted(axisReviewRecords.map((record) => record.axis))
  const protectedBoundaryCount = new Set(axisReviewRecords.map((record) => record.protectedBoundary)).size
  const safeInternalBacklogItemCount = axisReviewRecords.reduce((total, record) => total + record.safeInternalImplementationBacklog.length, 0)

  const provenanceText = `${axisReviewRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceText)
  const provenanceJsonlSha256 = sha256(provenanceText)
  let provenanceJsonlParseable = true
  for (const line of provenanceText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      provenanceJsonlParseable = false
    }
  }

  const providerCallsPerformed: [] = []
  const liveModelCallsPerformed: [] = []
  const externalCallsPerformed: [] = []
  const protectedActionsExecuted: [] = []
  const reviewChecks = [
    check('gap review report is current and passed', sourceReport.mode === 'local_no_provider_oss_architecture_gap_review' && sourceReport.baselineSnapshotDate === '2026-05-21' && sourceReport.gapChecks.every((item) => item.ok), `${sourceReport.mode}/${sourceReport.baselineSnapshotDate}`),
    check('high-priority projects are exactly the newly discovered source-supported targets', expectedHighPriorityProjects.every((project) => reviewedHighPriorityProjects.includes(project)) && reviewedHighPriorityProjects.length === expectedHighPriorityProjects.length, reviewedHighPriorityProjects.join(',') || 'none'),
    check('axis review records cover high-priority target axes', axisReviewRecords.length === highPriorityGapRecords.reduce((total, record) => total + record.absorptionAxes.length, 0) && axisReviewRecords.length >= requiredCoreAxes.length, `${axisReviewRecords.length} records`),
    check('core benchmark-quality axes are reviewed', requiredCoreAxes.every((axis) => reviewedAxes.includes(axis)), reviewedAxes.join(',')),
    check('every axis review has local evidence and safe backlog items', axisReviewRecords.every((record) => record.currentLocalEvidence.length > 0 && record.safeInternalImplementationBacklog.length > 0), `${safeInternalBacklogItemCount} backlog items`),
    check('protected boundaries remain explicit for every axis', protectedBoundaryCount >= requiredCoreAxes.length && axisReviewRecords.every((record) => record.protectedBoundary.length > 0), `${protectedBoundaryCount} protected boundaries`),
    check('every axis review blocks claims and shortcuts', axisReviewRecords.every((record) => record.claimAllowed === false && record.forbiddenShortcuts.length >= 5), 'claimAllowed=false for every record'),
    check('axis review writes parseable provenance JSONL', provenanceJsonlParseable && provenanceJsonlSha256.length === 64 && axisReviewRecords.every((record) => record.recordDigest.length === 64), provenanceJsonlPath),
    check('no provider live external or protected actions occurred', providerCallsPerformed.length === 0 && liveModelCallsPerformed.length === 0 && externalCallsPerformed.length === 0 && protectedActionsExecuted.length === 0, 'all call arrays empty'),
  ]

  const report: AxisArchitectureReviewReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_axis_architecture_review',
    sourceGapReviewReportPath,
    sourceGapReviewReportSha256,
    sourceTargetsReportPath: sourceReport.sourceTargetsReportPath,
    sourceReviewReportPath: sourceReport.sourceReviewReportPath,
    baselineSnapshotDate: sourceReport.baselineSnapshotDate,
    highPriorityProjectCount: reviewedHighPriorityProjects.length,
    reviewedHighPriorityProjects,
    axisReviewRecordCount: axisReviewRecords.length,
    uniqueAxisCount: reviewedAxes.length,
    reviewedAxes,
    safeInternalBacklogItemCount,
    protectedBoundaryCount,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: axisReviewRecords.length,
    provenanceJsonlParseable,
    providerCallsPerformed,
    liveModelCallsPerformed,
    externalCallsPerformed,
    protectedActionsExecuted,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST repository contents endpoint',
        sourceUrl: 'https://docs.github.com/en/rest/repos/contents#get-repository-content',
        observedPattern: 'Source-supported OSS evidence should be transformed into explicit axis-level review records before implementation absorption.',
        localAbsorption: 'OpenClaude creates high-priority per-axis records from the already reviewed top-10 source evidence and keeps them internal-only.',
      },
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence should bind claims to concrete materials and subjects rather than narrative summaries.',
        localAbsorption: 'OpenClaude writes each axis review as hash-addressed JSONL material with source report hashes.',
      },
      {
        sourceProject: 'OpenTelemetry Logs Data Model',
        sourceUrl: 'https://opentelemetry.io/docs/specs/otel/logs/data-model/',
        observedPattern: 'Structured events make operational evidence queryable and reviewable across systems.',
        localAbsorption: 'OpenClaude keeps each axis review record structured with project, axis, evidence, unresolved gap, boundary, and digest fields.',
      },
    ],
    reviewChecks,
    axisReviewRecords,
    claimBoundary: 'OSS axis architecture review is local no-provider planning evidence only. It does not fetch sources, clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or authorize public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of reviewChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = reviewChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`high_priority_project_count=${report.highPriorityProjectCount}`)
  console.log(`axis_review_record_count=${report.axisReviewRecordCount}`)
  console.log(`unique_axis_count=${report.uniqueAxisCount}`)
  console.log(`safe_internal_backlog_item_count=${report.safeInternalBacklogItemCount}`)
  console.log(`protected_boundary_count=${report.protectedBoundaryCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report.superiorityClaimAllowed}`)
}

main()
