import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type SourceReviewRecord = {
  rank: number
  fullName: string
  sourceUrl: string
  stars: number
  rootManifestMarkers: string[]
  rootSourceMarkers: string[]
  readmeProductSignals: string[]
  sourceReviewStatus: 'source_supported_candidate' | 'metadata_only_needs_deeper_review'
  absorptionCandidate: boolean
}

type SourceReviewReport = {
  mode: string
  sourceBaselinePath: string
  baselineSnapshotDate: string
  reviewedProjectCount: number
  sourceSupportedCandidateCount: number
  metadataOnlyNeedsReviewCount: number
  newTop10SourceReviewed: string[]
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceReviewChecks: Check[]
  reviewRecords: SourceReviewRecord[]
}

type TargetRecord = {
  schemaVersion: 'openclaude_oss_architecture_absorption_target_v1'
  rank: number
  fullName: string
  sourceUrl: string
  stars: number
  targetStatus: 'prioritized_source_supported_target' | 'deferred_metadata_only_target'
  priority: 'high' | 'medium' | 'deferred'
  sourceSignals: string[]
  rootMarkers: string[]
  absorptionAxes: string[]
  safeLocalAction: string
  requiredNextEvidence: string[]
  forbiddenShortcuts: string[]
  protectedActionRequiredBeforeClaim: boolean
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  recordDigest: string
}

type ArchitectureTargetReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_architecture_absorption_targets'
  sourceReviewReportPath: string
  sourceReviewReportSha256: string
  sourceBaselinePath: string
  baselineSnapshotDate: string
  reviewedProjectCount: number
  targetRecordCount: number
  prioritizedTargetCount: number
  deferredTargetCount: number
  newlyDiscoveredPrioritizedTargets: string[]
  coveredAbsorptionAxes: string[]
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
  selfImprovementActions: string[]
  targetChecks: Check[]
  targetRecords: TargetRecord[]
  claimBoundary: string
}

const root = process.cwd()
const sourceReviewReportPath = 'docs/product-quality/oss-source-review-report.json'
const reportJsonPath = 'docs/product-quality/oss-architecture-absorption-targets-report.json'
const reportMdPath = 'docs/product-quality/oss-architecture-absorption-targets-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-architecture-absorption-targets.jsonl'

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

function axesFor(record: SourceReviewRecord): string[] {
  const axes: string[] = []
  const sourceSupported = record.sourceReviewStatus === 'source_supported_candidate' && record.absorptionCandidate
  if (record.readmeProductSignals.includes('provider-model')) axes.push('provider_breadth', 'runtime_doctoring')
  if (record.readmeProductSignals.includes('terminal-cli')) axes.push('terminal_workflow', 'onboarding_docs')
  if (record.readmeProductSignals.includes('tool-use')) axes.push('tool_loop_reliability', 'security_and_permissions')
  if (record.readmeProductSignals.includes('coding-agent') || record.readmeProductSignals.includes('codebase-workflow')) axes.push('eval_and_quality_gates', 'tool_loop_reliability')
  if (record.readmeProductSignals.includes('ide-extension')) axes.push('ide_or_editor_surface')
  if (sourceSupported && (record.readmeProductSignals.length > 0 || record.rootManifestMarkers.length > 0 || record.rootSourceMarkers.length > 0)) axes.push('privacy_and_no_phone_home')
  if (record.rootManifestMarkers.length > 0) axes.push('release_hygiene')
  if (record.rootSourceMarkers.length > 0) axes.push('eval_and_quality_gates')
  return uniqueSorted(axes)
}

function safeAction(record: SourceReviewRecord, priority: TargetRecord['priority']): string {
  if (priority === 'deferred') {
    return `Keep ${record.fullName} in deferred metadata-only status until a deeper source-level review proves root source/manifests or official package surfaces.`
  }
  if (priority === 'high') {
    return `Create the next axis-specific no-provider architecture review for ${record.fullName}, starting with terminal workflow, tool-loop evidence, release hygiene, and any IDE/provider surfaces visible in source-reviewed materials.`
  }
  return `Use ${record.fullName} as a source-supported architecture benchmark input for the next scoped no-provider product-quality gap review.`
}

function targetFor(record: SourceReviewRecord, newTop10: Set<string>): TargetRecord {
  const sourceSupported = record.sourceReviewStatus === 'source_supported_candidate' && record.absorptionCandidate
  const priority: TargetRecord['priority'] = sourceSupported ? (newTop10.has(record.fullName) ? 'high' : 'medium') : 'deferred'
  const recordBase = {
    schemaVersion: 'openclaude_oss_architecture_absorption_target_v1' as const,
    rank: record.rank,
    fullName: record.fullName,
    sourceUrl: record.sourceUrl,
    stars: record.stars,
    targetStatus: sourceSupported ? 'prioritized_source_supported_target' as const : 'deferred_metadata_only_target' as const,
    priority,
    sourceSignals: [...record.readmeProductSignals].sort((left, right) => left.localeCompare(right)),
    rootMarkers: uniqueSorted([...record.rootManifestMarkers, ...record.rootSourceMarkers]),
    absorptionAxes: axesFor(record),
    safeLocalAction: safeAction(record, priority),
    requiredNextEvidence: sourceSupported
      ? [
          'axis-specific source/doc inspection without cloning or installing dependencies',
          'local OpenClaude gap mapping for each observed pattern',
          'no-provider fixture or report before any production implementation',
          'explicit protected-action request before external benchmark, provider call, install, publish, deploy, or public claim',
        ]
      : [
          'deeper source-surface evidence before implementation-pattern absorption',
          'root manifest or source tree evidence before source-supported classification',
          'claim boundary review before any public comparison language',
        ],
    forbiddenShortcuts: [
      'do not infer superiority from stars',
      'do not treat README-only evidence as external validation',
      'do not clone, install, publish, deploy, or run external services in this gate',
      'do not call providers or live models',
      'do not claim release, production, public, external-validation, or autonomous-reliability readiness',
    ],
    protectedActionRequiredBeforeClaim: true,
    publicComparisonClaimAllowed: false as const,
    superiorityClaimAllowed: false as const,
    releaseReadinessClaimAllowed: false as const,
    productionReadinessClaimAllowed: false as const,
    externalValidationClaimAllowed: false as const,
    autonomousReliabilityClaimAllowed: false as const,
  }
  return {
    ...recordBase,
    recordDigest: sha256(JSON.stringify(recordBase)),
  }
}

function writeMarkdown(report: ArchitectureTargetReport): void {
  const rows = report.targetRecords
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | \`${record.priority}\` | \`${record.targetStatus}\` | ${record.absorptionAxes.join(', ') || 'none'} | ${record.safeLocalAction} |`)
    .join('\n')
  const checkRows = report.targetChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Architecture Absorption Targets Report

Generated by: \`bun run product:oss-architecture-targets\`

## Claim Boundary

- This report converts the existing OSS source-review evidence into internal architecture absorption targets.
- It does not fetch new sources, clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Source-supported targets are next-review inputs only. Metadata-only targets remain deferred until stronger source evidence exists.

## Summary

- mode: \`${report.mode}\`
- source_review_report_path: \`${report.sourceReviewReportPath}\`
- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- reviewed_project_count: \`${report.reviewedProjectCount}\`
- target_record_count: \`${report.targetRecordCount}\`
- prioritized_target_count: \`${report.prioritizedTargetCount}\`
- deferred_target_count: \`${report.deferredTargetCount}\`
- newly_discovered_prioritized_targets: \`${report.newlyDiscoveredPrioritizedTargets.join(',') || 'none'}\`
- covered_absorption_axes: \`${report.coveredAbsorptionAxes.join(',')}\`

## Target Records

| Rank | Project | Priority | Status | Axes | Safe local action |
| ---: | --- | --- | --- | --- | --- |
${rows}

## Self-Improvement Actions

${report.selfImprovementActions.map((item) => `- ${item}`).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  if (!existsSync(resolve(root, sourceReviewReportPath))) {
    console.error(`RESULT: FAIL (${sourceReviewReportPath} missing)`)
    process.exit(1)
  }

  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const sourceReviewText = readText(sourceReviewReportPath)
  const sourceReview = JSON.parse(sourceReviewText) as SourceReviewReport
  const sourceReviewReportSha256 = sha256(sourceReviewText)
  const newTop10 = new Set(sourceReview.newTop10SourceReviewed)
  const targetRecords = sourceReview.reviewRecords.map((record) => targetFor(record, newTop10))
  const prioritizedTargets = targetRecords.filter((record) => record.targetStatus === 'prioritized_source_supported_target')
  const deferredTargets = targetRecords.filter((record) => record.targetStatus === 'deferred_metadata_only_target')
  const newlyDiscoveredPrioritizedTargets = prioritizedTargets
    .filter((record) => newTop10.has(record.fullName))
    .map((record) => record.fullName)
  const coveredAbsorptionAxes = uniqueSorted(targetRecords.flatMap((record) => record.absorptionAxes))

  const provenanceText = `${targetRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
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
  const targetChecks = [
    check('source review report is current and passed', sourceReview.mode === 'external_github_api_oss_source_review' && sourceReview.baselineSnapshotDate === '2026-05-21' && sourceReview.sourceReviewChecks.every((item) => item.ok), `${sourceReview.mode}/${sourceReview.baselineSnapshotDate}`),
    check('target records cover every reviewed project', targetRecords.length === sourceReview.reviewedProjectCount && targetRecords.length === sourceReview.reviewRecords.length, `${targetRecords.length}/${sourceReview.reviewedProjectCount}`),
    check('prioritized targets match source-supported candidates', prioritizedTargets.length === sourceReview.sourceSupportedCandidateCount, `${prioritizedTargets.length}/${sourceReview.sourceSupportedCandidateCount}`),
    check('deferred targets match metadata-only candidates', deferredTargets.length === sourceReview.metadataOnlyNeedsReviewCount, `${deferredTargets.length}/${sourceReview.metadataOnlyNeedsReviewCount}`),
    check('newly discovered source-supported projects are high priority', ['ultraworkers/claw-code', 'warpdotdev/warp', 'ruvnet/ruflo'].every((name) => newlyDiscoveredPrioritizedTargets.includes(name)), newlyDiscoveredPrioritizedTargets.join(',') || 'none'),
    check('absorption axes cover core product-quality dimensions', ['provider_breadth', 'terminal_workflow', 'tool_loop_reliability', 'privacy_and_no_phone_home', 'eval_and_quality_gates', 'ide_or_editor_surface', 'release_hygiene'].every((axis) => coveredAbsorptionAxes.includes(axis)), coveredAbsorptionAxes.join(',')),
    check('every target keeps protected claims blocked', targetRecords.every((record) => record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false && record.protectedActionRequiredBeforeClaim === true), 'all target claim flags false'),
    check('provenance JSONL is parseable and hash-addressed', provenanceJsonlParseable && provenanceJsonlSha256.length === 64 && targetRecords.every((record) => record.recordDigest.length === 64), provenanceJsonlPath),
    check('no provider live external or protected actions occurred', providerCallsPerformed.length === 0 && liveModelCallsPerformed.length === 0 && externalCallsPerformed.length === 0 && protectedActionsExecuted.length === 0, 'all call arrays empty'),
  ]

  const report: ArchitectureTargetReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_architecture_absorption_targets',
    sourceReviewReportPath,
    sourceReviewReportSha256,
    sourceBaselinePath: sourceReview.sourceBaselinePath,
    baselineSnapshotDate: sourceReview.baselineSnapshotDate,
    reviewedProjectCount: sourceReview.reviewedProjectCount,
    targetRecordCount: targetRecords.length,
    prioritizedTargetCount: prioritizedTargets.length,
    deferredTargetCount: deferredTargets.length,
    newlyDiscoveredPrioritizedTargets,
    coveredAbsorptionAxes,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: targetRecords.length,
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
        observedPattern: 'Source-supported benchmark candidates are more actionable when converted into axis-specific absorption targets with forbidden shortcuts and claim boundaries.',
        localAbsorption: 'OpenClaude creates a no-provider target queue before implementing or claiming any architecture absorption from high-star OSS candidates.',
      },
      {
        sourceProject: 'GitHub REST repository README endpoint',
        sourceUrl: 'https://docs.github.com/en/rest/repos/contents#get-a-repository-readme',
        observedPattern: 'README content is a primary project source for positioning and usage signals.',
        localAbsorption: 'OpenClaude uses README-derived signals only as internal target-selection evidence, not as public validation.',
      },
      {
        sourceProject: 'GitHub REST repository contents endpoint',
        sourceUrl: 'https://docs.github.com/en/rest/repos/contents#get-repository-content',
        observedPattern: 'Repository contents help classify source/manifests before implementation-pattern absorption.',
        localAbsorption: 'OpenClaude requires root source or manifest evidence before prioritizing architecture absorption targets.',
      },
    ],
    selfImprovementActions: [
      'Prioritize newly discovered source-supported projects for scoped architecture reviews.',
      'Defer metadata-only candidates until source/manifests are proven by stronger evidence.',
      'Map every absorption target to product-quality axes before any implementation work.',
      'Keep protected actions and public/readiness/superiority claims blocked until explicit authorization and stronger evidence exist.',
    ],
    targetChecks,
    targetRecords,
    claimBoundary: 'Architecture absorption targets are local no-provider planning evidence only. They do not clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or authorize public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of targetChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = targetChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`target_record_count=${report.targetRecordCount}`)
  console.log(`prioritized_target_count=${report.prioritizedTargetCount}`)
  console.log(`deferred_target_count=${report.deferredTargetCount}`)
  console.log(`newly_discovered_prioritized_targets=${report.newlyDiscoveredPrioritizedTargets.join(',') || 'none'}`)
  console.log(`covered_absorption_axes=${report.coveredAbsorptionAxes.join(',')}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report.superiorityClaimAllowed}`)
}

main()
