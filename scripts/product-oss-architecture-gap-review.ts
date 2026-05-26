import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type ArchitectureTargetRecord = {
  fullName: string
  sourceUrl: string
  targetStatus: 'prioritized_source_supported_target' | 'deferred_metadata_only_target'
  priority: 'high' | 'medium' | 'deferred'
  sourceSignals: string[]
  absorptionAxes: string[]
  protectedActionRequiredBeforeClaim: boolean
}

type ArchitectureTargetReport = {
  mode: string
  sourceReviewReportPath: string
  baselineSnapshotDate: string
  targetRecordCount: number
  prioritizedTargetCount: number
  deferredTargetCount: number
  newlyDiscoveredPrioritizedTargets: string[]
  coveredAbsorptionAxes: string[]
  targetChecks: Check[]
  targetRecords: ArchitectureTargetRecord[]
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
}

type GapRecord = {
  schemaVersion: 'openclaude_oss_architecture_gap_review_v1'
  fullName: string
  sourceUrl: string
  targetStatus: ArchitectureTargetRecord['targetStatus']
  priority: ArchitectureTargetRecord['priority']
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
  recordDigest: string
}

type GapReviewReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_architecture_gap_review'
  sourceTargetsReportPath: string
  sourceTargetsReportSha256: string
  sourceReviewReportPath: string
  baselineSnapshotDate: string
  targetRecordCount: number
  prioritizedTargetCount: number
  deferredTargetCount: number
  gapRecordCount: number
  axesReviewed: string[]
  safeInternalActionCount: number
  protectedBoundaryGapCount: number
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
  gapChecks: Check[]
  gapRecords: GapRecord[]
  claimBoundary: string
}

const root = process.cwd()
const sourceTargetsReportPath = 'docs/product-quality/oss-architecture-absorption-targets-report.json'
const reportJsonPath = 'docs/product-quality/oss-architecture-gap-review-report.json'
const reportMdPath = 'docs/product-quality/oss-architecture-gap-review-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-architecture-gap-review.jsonl'

const requiredAxes = [
  'provider_breadth',
  'terminal_workflow',
  'tool_loop_reliability',
  'privacy_and_no_phone_home',
  'eval_and_quality_gates',
  'ide_or_editor_surface',
  'release_hygiene',
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

function evidenceForAxis(axis: string): GapRecord['openClaudeEvidence'][number] {
  const map: Record<string, GapRecord['openClaudeEvidence'][number]> = {
    provider_breadth: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-provider-breadth-evidence-report.json',
        'docs/product-quality/provider-capability-matrix-report.json',
        'docs/product-quality/provider-compatibility-fixtures.json',
        'docs/product-quality/runtime-doctor-regression-fixtures.json',
      ],
      unresolvedGap: 'Provider breadth is locally fixture-verified; live provider compatibility and model behavior remain unmeasured.',
      protectedBoundary: 'provider/live model calls require explicit authorization before any external validation or compatibility claim.',
    },
    terminal_workflow: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-terminal-workflow-evidence-report.json',
        'docs/product-quality/golden-path-terminal-transcripts.json',
        'docs/product-quality/terminal-failure-recovery-transcripts-report.json',
        'docs/product-quality/onboarding-smoke-report.json',
        'docs/product-quality/real-session-capture-report.json',
      ],
      unresolvedGap: 'Terminal workflow has local no-provider command evidence; non-synthetic user workflows and external benchmark sessions remain absent.',
      protectedBoundary: 'external benchmark, public comparison, and non-synthetic capture claims require explicit operator/owner authorization.',
    },
    tool_loop_reliability: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-tool-loop-reliability-evidence-report.json',
        'docs/product-quality/permission-regression-fixtures.json',
        'docs/product-quality/prompted-tool-loop-capture-report.json',
        'docs/product-quality/code-editing-trace-capture-report.json',
        'docs/product-quality/multi-file-code-editing-trace-capture-report.json',
        'docs/product-quality/regression-cycle-code-editing-trace-capture-report.json',
        'docs/product-quality/tool-interruption-recovery-trace-report.json',
        'docs/product-quality/protected-action-denial-trace-report.json',
      ],
      unresolvedGap: 'Tool-loop evidence is local and fixture-bounded; broader non-synthetic repository repair tasks remain unproven.',
      protectedBoundary: 'real product repo mutation, provider/live model execution, and autonomous reliability claims remain blocked.',
    },
    eval_and_quality_gates: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-eval-quality-gate-checklist-report.json',
        'docs/product-quality/product-quality-gate.md',
        'docs/product-quality/benchmark-readiness-matrix.json',
        'docs/product-quality/local-benchmark-harness-report.json',
        'docs/product-quality/benchmark-submission-readiness-report.json',
        'docs/product-quality/terminal-bench-readiness-report.json',
        'docs/product-quality/verification-report-consistency-report.json',
        'docs/product-quality/quality-blocker-taxonomy-report.json',
      ],
      unresolvedGap: 'Local benchmark readiness and replay evidence exists; official external benchmark execution remains unperformed.',
      protectedBoundary: 'external datasets, Docker/remote runtimes, hosted CI, provider calls, and leaderboard/public result claims require explicit authorization.',
    },
    privacy_and_no_phone_home: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json',
        'docs/product-quality/public-claim-boundary-report.json',
        'scripts/verify-no-phone-home.ts',
      ],
      unresolvedGap: 'Local no-phone-home evidence exists for OpenClaude build output and privacy surfaces; external comparative telemetry review and public privacy claims remain unproven.',
      protectedBoundary: 'external telemetry comparison, provider/live validation, public privacy claims, production mutation, and release/public/production readiness claims require explicit authorization.',
    },
    ide_or_editor_surface: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json',
        'docs/product-quality/ide-extension-surface-report.json',
        'docs/product-quality/ide-extension-scope-report.json',
        'docs/product-quality/ide-extension-manifest-smoke-report.json',
        'docs/product-quality/ide-extension-runtime-smoke-report.json',
        'docs/product-quality/ide-extension-host-smoke-report.json',
        'docs/product-quality/ide-extension-workbench-smoke-report.json',
        'docs/product-quality/vscode-startup-diagnostics-report.json',
        'docs/product-quality/ide-extension-webview-render-smoke-report.json',
        'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json',
        'docs/product-quality/ide-extension-webview-interaction-smoke-report.json',
      ],
      unresolvedGap: 'IDE surface, manifest, mock-host runtime, workbench, webview, screenshot, interaction, and startup-boundary evidence exists, but current real host command smoke remains blocked by unavailable code CLI.',
      protectedBoundary: 'VS Code repair, reinstall, PATH/install-state mutation, extension availability claims, publish, deploy, and public comparison require explicit owner action.',
    },
    release_hygiene: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-release-hygiene-evidence-report.json',
        'docs/product-quality/release-artifact-file-list-report.json',
        'docs/product-quality/release-artifact-provenance-report.json',
        'docs/product-quality/release-artifact-reproducibility-report.json',
        'docs/product-quality/git-release-hygiene-report.json',
        'docs/product-quality/license-boundary-authorization-report.json',
      ],
      unresolvedGap: 'Local packaging and provenance evidence exists; this workspace is not a git repository and license/legal decisions remain default-false.',
      protectedBoundary: 'commit, push, publish, deploy, signed provenance, legal/NOTICE/REUSE decisions, and release readiness claims remain blocked.',
    },
    onboarding_docs: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-onboarding-docs-evidence-report.json',
        'docs/product-quality/onboarding-smoke-report.json',
        'docs/product-quality/doc-link-integrity-report.json',
        'docs/product-quality/community-profile-quality-report.json',
      ],
      unresolvedGap: 'Documentation structure is locally checked; cross-platform non-synthetic first-run sessions remain absent.',
      protectedBoundary: 'cross-platform runtime claims and public readiness claims require separate evidence and authorization.',
    },
    runtime_doctoring: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-runtime-doctoring-evidence-report.json',
        'docs/product-quality/runtime-doctor-regression-fixtures.json',
        'docs/product-quality/vscode-startup-diagnostics-report.json',
      ],
      unresolvedGap: 'Runtime diagnostics are locally checked; protected local install/PATH repair is still outside this gate.',
      protectedBoundary: 'dependency install, VS Code repair, provider probes, and external diagnostics remain blocked.',
    },
    security_and_permissions: {
      axis,
      currentLocalEvidence: [
        'docs/product-quality/oss-security-permissions-evidence-report.json',
        'docs/product-quality/permission-regression-fixtures.json',
        'docs/product-quality/openssf-security-posture-report.json',
        'docs/product-quality/dependency-governance-quality-report.json',
        'docs/product-quality/source-controlled-checks-report.json',
      ],
      unresolvedGap: 'Security posture is local file evidence; hosted Scorecard, hosted CodeQL, and branch protection enforcement remain unverified.',
      protectedBoundary: 'hosted CI/security service calls and public security posture claims require explicit authorization.',
    },
  }
  return map[axis] ?? {
    axis,
    currentLocalEvidence: ['docs/product-quality/product-quality-gate.md'],
    unresolvedGap: 'Axis is recognized by OSS target evidence but needs a dedicated no-provider local review before implementation.',
    protectedBoundary: 'claim expansion remains blocked until dedicated evidence and authorization exist.',
  }
}

function safeActionsFor(record: ArchitectureTargetRecord): string[] {
  if (record.targetStatus === 'deferred_metadata_only_target') {
    return [
      `Keep ${record.fullName} deferred until source-level evidence becomes sufficient.`,
      'Do not absorb implementation patterns from deferred metadata-only candidates.',
    ]
  }
  return [
    `Use ${record.fullName} as an input to the next axis-specific no-provider review.`,
    'Compare its observed axes against current local evidence before any implementation change.',
    'Create protected-action authorization requests for any live provider, external benchmark, install, publish, deploy, or public claim step.',
  ]
}

function protectedActionsFor(record: ArchitectureTargetRecord): string[] {
  const boundaries = new Set<string>()
  for (const axis of record.absorptionAxes) {
    boundaries.add(evidenceForAxis(axis).protectedBoundary)
  }
  if (record.targetStatus === 'deferred_metadata_only_target') {
    boundaries.add('deeper external source inspection remains a separate explicit source-review action and cannot be converted into a claim.')
  }
  return [...boundaries]
}

function gapRecordFor(record: ArchitectureTargetRecord): GapRecord {
  const evidence = record.absorptionAxes.map((axis) => evidenceForAxis(axis))
  const base = {
    schemaVersion: 'openclaude_oss_architecture_gap_review_v1' as const,
    fullName: record.fullName,
    sourceUrl: record.sourceUrl,
    targetStatus: record.targetStatus,
    priority: record.priority,
    absorptionAxes: [...record.absorptionAxes],
    sourceSignals: [...record.sourceSignals],
    openClaudeEvidence: evidence,
    safeInternalNextActions: safeActionsFor(record),
    protectedActionsStillRequired: protectedActionsFor(record),
    forbiddenShortcuts: [
      'do not treat GitHub stars as superiority evidence',
      'do not treat local no-provider evidence as external validation',
      'do not modify production OpenClaude, MFH, or real product repositories in this gate',
      'do not call providers, live models, or external services',
      'do not install dependencies, publish, deploy, launch, or make release/public/production/autonomous reliability claims',
    ],
    claimAllowed: false as const,
  }
  return {
    ...base,
    recordDigest: sha256(JSON.stringify(base)),
  }
}

function writeMarkdown(report: GapReviewReport): void {
  const rows = report.gapRecords
    .map((record) => `| \`${record.fullName}\` | \`${record.priority}\` | ${record.absorptionAxes.join(', ') || 'none'} | ${record.safeInternalNextActions[0]} | ${record.protectedActionsStillRequired.length} |`)
    .join('\n')
  const checkRows = report.gapChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Architecture Gap Review Report

Generated by: \`bun run product:oss-architecture-gap-review\`

## Claim Boundary

- This report maps the OSS architecture target queue to current OpenClaude local evidence and unresolved gaps.
- It does not fetch sources, clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Protected gaps stay blocked until explicit owner/operator authorization exists.

## Summary

- mode: \`${report.mode}\`
- source_targets_report_path: \`${report.sourceTargetsReportPath}\`
- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- target_record_count: \`${report.targetRecordCount}\`
- prioritized_target_count: \`${report.prioritizedTargetCount}\`
- deferred_target_count: \`${report.deferredTargetCount}\`
- safe_internal_action_count: \`${report.safeInternalActionCount}\`
- protected_boundary_gap_count: \`${report.protectedBoundaryGapCount}\`
- axes_reviewed: \`${report.axesReviewed.join(',')}\`

## Gap Records

| Project | Priority | Axes | Next safe internal action | Protected gap count |
| --- | --- | --- | --- | ---: |
${rows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  if (!existsSync(resolve(root, sourceTargetsReportPath))) {
    console.error(`RESULT: FAIL (${sourceTargetsReportPath} missing)`)
    process.exit(1)
  }

  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const sourceText = readText(sourceTargetsReportPath)
  const sourceReport = JSON.parse(sourceText) as ArchitectureTargetReport
  const sourceTargetsReportSha256 = sha256(sourceText)
  const gapRecords = sourceReport.targetRecords.map((record) => gapRecordFor(record))
  const axesReviewed = uniqueSorted(gapRecords.flatMap((record) => record.absorptionAxes))
  const provenanceText = `${gapRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
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
  const protectedBoundaryGapCount = gapRecords.reduce((total, record) => total + record.protectedActionsStillRequired.length, 0)
  const safeInternalActionCount = gapRecords.reduce((total, record) => total + record.safeInternalNextActions.length, 0)
  const gapChecks = [
    check('architecture targets report is current and passed', sourceReport.mode === 'local_no_provider_oss_architecture_absorption_targets' && sourceReport.baselineSnapshotDate === '2026-05-21' && sourceReport.targetChecks.every((item) => item.ok), `${sourceReport.mode}/${sourceReport.baselineSnapshotDate}`),
    check('gap records cover every architecture target', gapRecords.length === sourceReport.targetRecordCount && gapRecords.length === sourceReport.targetRecords.length, `${gapRecords.length}/${sourceReport.targetRecordCount}`),
    check('gap review preserves prioritized and deferred counts', sourceReport.prioritizedTargetCount === gapRecords.filter((record) => record.targetStatus === 'prioritized_source_supported_target').length && sourceReport.deferredTargetCount === gapRecords.filter((record) => record.targetStatus === 'deferred_metadata_only_target').length, `${sourceReport.prioritizedTargetCount}/${sourceReport.deferredTargetCount}`),
    check('gap review covers required product-quality axes', requiredAxes.every((axis) => axesReviewed.includes(axis)), axesReviewed.join(',')),
    check('every gap record has safe internal next actions', gapRecords.every((record) => record.safeInternalNextActions.length > 0), `${safeInternalActionCount} actions`),
    check('protected boundary gaps remain explicit', protectedBoundaryGapCount >= sourceReport.prioritizedTargetCount && gapRecords.every((record) => record.protectedActionsStillRequired.length > 0), `${protectedBoundaryGapCount} protected gaps`),
    check('every gap record blocks claims and shortcuts', gapRecords.every((record) => record.claimAllowed === false && record.forbiddenShortcuts.length >= 5), 'claimAllowed=false for every record'),
    check('gap review writes parseable provenance JSONL', provenanceJsonlParseable && provenanceJsonlSha256.length === 64 && gapRecords.every((record) => record.recordDigest.length === 64), provenanceJsonlPath),
    check('no provider live external or protected actions occurred', providerCallsPerformed.length === 0 && liveModelCallsPerformed.length === 0 && externalCallsPerformed.length === 0 && protectedActionsExecuted.length === 0, 'all call arrays empty'),
  ]

  const report: GapReviewReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_architecture_gap_review',
    sourceTargetsReportPath,
    sourceTargetsReportSha256,
    sourceReviewReportPath: sourceReport.sourceReviewReportPath,
    baselineSnapshotDate: sourceReport.baselineSnapshotDate,
    targetRecordCount: sourceReport.targetRecordCount,
    prioritizedTargetCount: sourceReport.prioritizedTargetCount,
    deferredTargetCount: sourceReport.deferredTargetCount,
    gapRecordCount: gapRecords.length,
    axesReviewed,
    safeInternalActionCount,
    protectedBoundaryGapCount,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: gapRecords.length,
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
        observedPattern: 'Source-level repository evidence should be separated from metadata-only candidates before implementation-pattern absorption.',
        localAbsorption: 'OpenClaude maps every source-supported target to local evidence and protected gaps before implementation.',
      },
      {
        sourceProject: 'SLSA Build Provenance',
        sourceUrl: 'https://slsa.dev/spec/v1.2/build-provenance',
        observedPattern: 'Evidence packages should bind claims to concrete subjects and materials instead of relying on prose.',
        localAbsorption: 'OpenClaude records each OSS gap review record as a hash-addressed JSONL material.',
      },
    ],
    gapChecks,
    gapRecords,
    claimBoundary: 'OSS architecture gap review is local no-provider planning evidence only. It does not fetch external sources, clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, publish, deploy, launch, or authorize public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of gapChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = gapChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`gap_record_count=${report.gapRecordCount}`)
  console.log(`prioritized_target_count=${report.prioritizedTargetCount}`)
  console.log(`deferred_target_count=${report.deferredTargetCount}`)
  console.log(`safe_internal_action_count=${report.safeInternalActionCount}`)
  console.log(`protected_boundary_gap_count=${report.protectedBoundaryGapCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report.superiorityClaimAllowed}`)
}

main()
