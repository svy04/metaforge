import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { sha256 as sha256Text } from './quality-report-helpers'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type BenchmarkSubmissionReadinessReport = {
  mode: 'local_no_provider_benchmark_submission_readiness'
  submissionAssetsJsonlPath: string
  submissionAssetsJsonlSha256: string
  summary: {
    requiredAssetCount: number
    localEquivalentAvailableCount: number
    partialLocalEquivalentCount: number
    classifiedUnresolvedProtectedGapCount: number
    officialExternalSubmissionReady: false
  }
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkSubmissionPerformed: false
  externalLeaderboardClaimAllowed: false
}

type ExternalBenchmarkBoundaryReport = {
  mode: 'local_no_provider_external_benchmark_boundary'
  externalBenchmarkExecutionAuthorized: false
  externalBenchmarkExecutionPerformed: false
  externalBenchmarkResultClaimAllowed: false
  externalValidationClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  protectedActionAuthorizations: Array<{
    id: string
    authorized: boolean
  }>
}

type PolicyItemStatus =
  | 'partial_local_evidence_only'
  | 'classified_unresolved_protected_or_owner_claim_required'
  | 'blocked_not_authorized'

type BenchmarkPolicyItem = {
  policyItemId: string
  sourcePolicyScope: string
  status: PolicyItemStatus
  currentLocalEvidence: string
  requiredBeforeOfficialClaim: string
  protectedActionRequiredToResolve: boolean
  protectedActionExecuted: false
  officialClaimAllowed: false
}

type BenchmarkPolicyComplianceReport = {
  generatedAt: string
  mode: 'local_no_provider_benchmark_policy_compliance'
  sourceBenchmarkSubmissionReadinessPath: string
  sourceBenchmarkSubmissionReadinessSha256: string
  sourceExternalBenchmarkBoundaryPath: string
  sourceExternalBenchmarkBoundarySha256: string
  sourceSubmissionAssetsJsonlPath: string
  sourceSubmissionAssetsJsonlSha256: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPolicy: string
  }>
  policyComplianceJsonlPath: string
  policyComplianceJsonlSha256: string
  policyItems: BenchmarkPolicyItem[]
  summary: {
    policyItemCount: number
    partialLocalEvidenceOnlyCount: number
    unresolvedProtectedOrOwnerClaimRequiredCount: number
    blockedNotAuthorizedCount: number
    officialSWEbenchVerifiedSubmissionEligible: false
    officialSWEbenchVerifiedSubmissionClaimAllowed: false
    officialLeaderboardClaimAllowed: false
  }
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  dependencyInstallPerformed: false
  officialBenchmarkSubmissionPerformed: false
  externalBenchmarkExecutionPerformed: false
  externalLeaderboardClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  policyComplianceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSubmissionReadinessPath = 'docs/product-quality/benchmark-submission-readiness-report.json'
const sourceExternalBoundaryPath = 'docs/product-quality/external-benchmark-boundary-report.json'
const policyComplianceJsonlPath = 'reports/openclaude-benchmark-policy-compliance.jsonl'

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function fileSha256(path: string): string {
  return createHash('sha256').update(readFileSync(resolve(root, path))).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function policyItem(
  policyItemId: string,
  sourcePolicyScope: string,
  status: PolicyItemStatus,
  currentLocalEvidence: string,
  requiredBeforeOfficialClaim: string,
  protectedActionRequiredToResolve = true,
): BenchmarkPolicyItem {
  return {
    policyItemId,
    sourcePolicyScope,
    status,
    currentLocalEvidence,
    requiredBeforeOfficialClaim,
    protectedActionRequiredToResolve,
    protectedActionExecuted: false,
    officialClaimAllowed: false,
  }
}

function buildPolicyItems(submission: BenchmarkSubmissionReadinessReport): BenchmarkPolicyItem[] {
  return [
    policyItem(
      'open_research_publication_or_technical_report',
      'SWE-bench Verified and Multilingual submission policy dated 2025-11-18',
      'classified_unresolved_protected_or_owner_claim_required',
      'No arXiv preprint, technical report, or peer-reviewed publication artifact is present in local no-provider product-quality evidence.',
      'Publication evidence and explicit permission to cite it before any official SWE-bench Verified or Multilingual submission eligibility claim.',
    ),
    policyItem(
      'academic_or_research_institution_affiliation',
      'SWE-bench Verified and Multilingual submission policy dated 2025-11-18',
      'classified_unresolved_protected_or_owner_claim_required',
      'No academic institution or established research-lab affiliation evidence is present in local product-quality artifacts.',
      'Explicit affiliation evidence before any official SWE-bench Verified or Multilingual eligibility claim.',
    ),
    policyItem(
      'open_source_methods',
      'SWE-bench Verified and Multilingual submission policy dated 2025-11-18',
      'partial_local_evidence_only',
      'Local repo files, product-quality scripts, and evidence reports are present, but no official benchmark submission method disclosure package exists.',
      'A complete authorized method disclosure package bound to an official benchmark submission, without adding release or public-readiness claims.',
      false,
    ),
    policyItem(
      'peer_reviewed_publication',
      'SWE-bench Verified and Multilingual submission policy dated 2025-11-18',
      'classified_unresolved_protected_or_owner_claim_required',
      'No peer-reviewed publication evidence is present in this local no-provider gate.',
      'Peer-review or accepted publication evidence before any official eligibility claim that depends on it.',
    ),
    policyItem(
      'official_submission_assets_complete',
      'SWE-bench experiments required submission assets',
      submission.summary.officialExternalSubmissionReady === false
        ? 'classified_unresolved_protected_or_owner_claim_required'
        : 'partial_local_evidence_only',
      `${submission.summary.requiredAssetCount} submission assets are mapped locally, with ${submission.summary.classifiedUnresolvedProtectedGapCount} unresolved protected gaps.`,
      'Official external submission assets such as metadata, per-instance patch/test output, and verification instructions must be produced only after explicit authorization.',
    ),
    policyItem(
      'official_leaderboard_pr_or_submission',
      'SWE-bench experiments leaderboard participation flow',
      'blocked_not_authorized',
      'No fork, official submission folder, external benchmark PR, or leaderboard request was created by this local gate.',
      'Explicit owner authorization for external repository interaction and public result claims.',
    ),
    policyItem(
      'multimodal_scope_not_inferred',
      'SWE-bench experiments policy note distinguishes Multimodal from Verified and Multilingual restrictions',
      'blocked_not_authorized',
      'This gate does not infer eligibility for any SWE-bench split, including Multimodal, from local readiness evidence.',
      'Explicit owner decision on benchmark split, external dataset/runtime authorization, and claim boundary before any split-specific submission claim.',
    ),
  ]
}

function writeMarkdown(report: BenchmarkPolicyComplianceReport): void {
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPolicy} |`)
    .join('\n')
  const itemRows = report.policyItems
    .map((item) => `| \`${item.policyItemId}\` | \`${item.status}\` | ${item.currentLocalEvidence} | \`${item.protectedActionRequiredToResolve}\` | \`${item.officialClaimAllowed}\` |`)
    .join('\n')
  const checkRows = report.policyComplianceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Benchmark Policy Compliance Report

Generated by: \`bun run product:benchmark-policy-compliance\`

## Claim Boundary

- This is a local no-provider benchmark policy compliance and claim-boundary report.
- It records that local benchmark submission readiness is not official SWE-bench Verified, Multilingual, Multimodal, or leaderboard eligibility.
- It does not create a benchmark submission, fork, pull request, publication, affiliation claim, peer-review claim, provider run, live model run, external service call, dependency install, deploy, publish, launch, public claim, external validation claim, release readiness claim, production readiness claim, or autonomous reliability claim.

## Summary

- mode: \`${report.mode}\`
- source_submission_readiness_path: \`${report.sourceBenchmarkSubmissionReadinessPath}\`
- source_submission_assets_jsonl_path: \`${report.sourceSubmissionAssetsJsonlPath}\`
- policy_compliance_jsonl_path: \`${report.policyComplianceJsonlPath}\`
- policy_compliance_jsonl_sha256: \`${report.policyComplianceJsonlSha256}\`
- policy_item_count: \`${report.summary.policyItemCount}\`
- partial_local_evidence_only_count: \`${report.summary.partialLocalEvidenceOnlyCount}\`
- unresolved_protected_or_owner_claim_required_count: \`${report.summary.unresolvedProtectedOrOwnerClaimRequiredCount}\`
- blocked_not_authorized_count: \`${report.summary.blockedNotAuthorizedCount}\`
- official_swebench_verified_submission_eligible: \`${report.summary.officialSWEbenchVerifiedSubmissionEligible}\`
- official_swebench_verified_submission_claim_allowed: \`${report.summary.officialSWEbenchVerifiedSubmissionClaimAllowed}\`
- official_leaderboard_claim_allowed: \`${report.summary.officialLeaderboardClaimAllowed}\`

## Primary Source Inputs

| Source | URL | Policy Absorbed |
| --- | --- | --- |
${sourceRows}

## Policy Items

| Policy Item | Status | Current Local Evidence | Protected Action Required | Official Claim Allowed |
| --- | --- | --- | --- | --- |
${itemRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(docsDir, 'benchmark-policy-compliance-report.md'), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const submission = readJson<BenchmarkSubmissionReadinessReport>(sourceSubmissionReadinessPath)
  const externalBoundary = readJson<ExternalBenchmarkBoundaryReport>(sourceExternalBoundaryPath)
  const policyItems = buildPolicyItems(submission)
  const jsonl = `${policyItems.map((item) => JSON.stringify(item)).join('\n')}\n`
  writeFileSync(resolve(root, policyComplianceJsonlPath), jsonl)
  const policyComplianceJsonlSha256 = sha256Text(jsonl)

  const summary = {
    policyItemCount: policyItems.length,
    partialLocalEvidenceOnlyCount: policyItems.filter((item) => item.status === 'partial_local_evidence_only').length,
    unresolvedProtectedOrOwnerClaimRequiredCount: policyItems.filter((item) => item.status === 'classified_unresolved_protected_or_owner_claim_required').length,
    blockedNotAuthorizedCount: policyItems.filter((item) => item.status === 'blocked_not_authorized').length,
    officialSWEbenchVerifiedSubmissionEligible: false as const,
    officialSWEbenchVerifiedSubmissionClaimAllowed: false as const,
    officialLeaderboardClaimAllowed: false as const,
  }

  const checks = [
    check('benchmark submission readiness is imported', submission.mode === 'local_no_provider_benchmark_submission_readiness', submission.mode),
    check('external benchmark boundary is imported', externalBoundary.mode === 'local_no_provider_external_benchmark_boundary', externalBoundary.mode),
    check('submission readiness remains unofficial', submission.summary.officialExternalSubmissionReady === false && submission.externalBenchmarkSubmissionPerformed === false && submission.externalLeaderboardClaimAllowed === false, 'officialExternalSubmissionReady=false'),
    check('external benchmark execution remains unauthorized', externalBoundary.externalBenchmarkExecutionAuthorized === false && externalBoundary.externalBenchmarkExecutionPerformed === false, 'externalBenchmarkExecutionAuthorized=false'),
    check('policy items cover publication affiliation methods peer review assets and PR boundary', ['open_research_publication_or_technical_report', 'academic_or_research_institution_affiliation', 'open_source_methods', 'peer_reviewed_publication', 'official_submission_assets_complete', 'official_leaderboard_pr_or_submission'].every((id) => policyItems.some((item) => item.policyItemId === id)), `${policyItems.length} policy items`),
    check('policy source date is preserved', policyItems.some((item) => item.sourcePolicyScope.includes('2025-11-18')), '2025-11-18'),
    check('official eligibility and leaderboard claims remain blocked', summary.officialSWEbenchVerifiedSubmissionEligible === false && summary.officialSWEbenchVerifiedSubmissionClaimAllowed === false && summary.officialLeaderboardClaimAllowed === false, 'all official claims false'),
    check('protected policy gaps are not executed', policyItems.some((item) => item.protectedActionRequiredToResolve) && policyItems.every((item) => item.protectedActionExecuted === false && item.officialClaimAllowed === false), `${summary.unresolvedProtectedOrOwnerClaimRequiredCount} unresolved policy gaps`),
    check('policy JSONL hash is recorded', policyComplianceJsonlSha256.length === 64 && existsSync(resolve(root, policyComplianceJsonlPath)), policyComplianceJsonlPath),
    check('no provider live external or protected actions occurred', submission.providerCallsPerformed.length === 0 && submission.liveModelCallsPerformed.length === 0 && submission.externalCallsPerformed.length === 0 && submission.protectedActionsExecuted.length === 0 && externalBoundary.providerCallsPerformed.length === 0 && externalBoundary.liveModelCallsPerformed.length === 0 && externalBoundary.externalCallsPerformed.length === 0 && externalBoundary.protectedActionsExecuted.length === 0, 'all call/action arrays empty'),
  ]

  const report: BenchmarkPolicyComplianceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_benchmark_policy_compliance',
    sourceBenchmarkSubmissionReadinessPath: sourceSubmissionReadinessPath,
    sourceBenchmarkSubmissionReadinessSha256: fileSha256(sourceSubmissionReadinessPath),
    sourceExternalBenchmarkBoundaryPath: sourceExternalBoundaryPath,
    sourceExternalBenchmarkBoundarySha256: fileSha256(sourceExternalBoundaryPath),
    sourceSubmissionAssetsJsonlPath: submission.submissionAssetsJsonlPath,
    sourceSubmissionAssetsJsonlSha256: submission.submissionAssetsJsonlSha256,
    primarySourceInputs: [
      {
        sourceProject: 'SWE-bench/experiments',
        sourceUrl: 'https://github.com/swe-bench/experiments',
        observedPolicy: 'SWE-bench Verified and Multilingual submissions are now constrained by open research publication, research affiliation, open-source methods, and peer-review expectations; leaderboard artifacts must remain reproducible and transparent.',
      },
      {
        sourceProject: 'SWE-bench/SWE-bench',
        sourceUrl: 'https://github.com/swe-bench/SWE-bench',
        observedPolicy: 'Benchmark execution and submission claims must remain separate from local readiness evidence until the external evaluation path is explicitly authorized.',
      },
    ],
    policyComplianceJsonlPath,
    policyComplianceJsonlSha256,
    policyItems,
    summary,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    dependencyInstallPerformed: false,
    officialBenchmarkSubmissionPerformed: false,
    externalBenchmarkExecutionPerformed: false,
    externalLeaderboardClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    policyComplianceChecks: checks,
    claimBoundary: 'Benchmark policy compliance is local no-provider claim-boundary evidence only. It does not create or claim official SWE-bench eligibility, external benchmark submission, leaderboard standing, release readiness, production readiness, public readiness, external validation, or autonomous reliability.',
  }

  writeFileSync(resolve(docsDir, 'benchmark-policy-compliance-report.json'), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  if (!checks.every((item) => item.ok)) {
    console.error(`RESULT: FAIL (${checks.filter((item) => !item.ok).length} failed checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log(`policy_compliance_jsonl_path=${policyComplianceJsonlPath}`)
  console.log(`policy_item_count=${summary.policyItemCount}`)
  console.log(`unresolved_policy_gap_count=${summary.unresolvedProtectedOrOwnerClaimRequiredCount}`)
  console.log(`blocked_not_authorized_count=${summary.blockedNotAuthorizedCount}`)
  console.log(`official_swebench_verified_submission_eligible=${summary.officialSWEbenchVerifiedSubmissionEligible}`)
  console.log(`official_leaderboard_claim_allowed=${summary.officialLeaderboardClaimAllowed}`)
}

main()
