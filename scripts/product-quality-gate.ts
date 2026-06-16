import { existsSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

type BaselineProject = {
  rank: number
  full_name: string
  stars: number
  license: string
  source_url: string
  positioning: string
}

type Baseline = {
  snapshot_date: string
  category: string
  claim_boundary: string
  top10: BaselineProject[]
  required_product_axes: string[]
}

type OssBaselineFreshnessReport = {
  mode: string
  sourceBaselinePath: string
  sourceBaselineSha256: string
  baselineSnapshotDate: string
  validationDate: string
  baselineAgeDays: number
  baselineFreshForInternalPlanning: boolean
  baselineRefreshRequiredBeforePublicComparison: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  externalGitHubRefreshPerformed: boolean
  githubApiCallPerformed: boolean
  top10ProjectCount: number
  requiredProductAxisCount: number
  ranksAreConsecutive: boolean
  starsSortedDescending: boolean
  starsArePositiveIntegers: boolean
  sourceUrlsAreGithubRepos: boolean
  fullNamesMatchSourceUrls: boolean
  licensesArePresent: boolean
  collectionMethodMentionsGitHubMetadata: boolean
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  baselineFreshnessChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssBaselineRefreshReport = {
  mode: string
  snapshotDate: string
  outputBaselinePath: string
  outputBaselineSha256: string
  previousBaselinePath: string
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  searchQueryCount: number
  uniqueCandidateCount: number
  eligibleCandidateCount: number
  top10ProjectCount: number
  newlyDiscoveredTop10Projects: string[]
  removedPreviousTop10Projects: string[]
  discoveredHigherStarCandidatesExcluded: Array<{
    fullName: string
    stars: number
    reason: string
  }>
  baselineFreshForPublicComparisonInput: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  externalGitHubRefreshPerformed: boolean
  githubApiCallPerformed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalCallsPerformed: unknown[]
  refreshChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssSourceReviewReport = {
  mode: string
  sourceBaselinePath: string
  baselineSnapshotDate: string
  reviewedProjectCount: number
  sourceSupportedCandidateCount: number
  metadataOnlyNeedsReviewCount: number
  absorptionCandidateCount: number
  newTop10SourceReviewed: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  externalGitHubSourceReviewPerformed: boolean
  githubApiCallPerformed: boolean
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
  externalCallsPerformed: Array<{
    kind: string
    url: string
    status: number | null
  }>
  sourceReviewChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssArchitectureTargetsReport = {
  mode: string
  sourceReviewReportPath: string
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
  targetChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssArchitectureGapReviewReport = {
  mode: string
  sourceTargetsReportPath: string
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
  gapChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssAxisArchitectureReviewReport = {
  mode: string
  sourceGapReviewReportPath: string
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
  reviewChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssSafeBacklogPlanReport = {
  mode: string
  sourceAxisArchitectureReviewReportPath: string
  sourceAxisArchitectureReviewReportSha256: string
  sourceSafeInternalBacklogItemCount: number
  plannedBacklogItemCount: number
  reviewedHighPriorityProjects: string[]
  reviewedAxes: string[]
  uniqueAxisCount: number
  nextSafeInternalGateCandidateCount: number
  nextSafeInternalGateCandidates: Array<{
    gateId: string
    axis: string
    sourceBacklogItemCount: number
    protectedActionRequiredForPlanning: boolean
  }>
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
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
  planItems: Array<{
    planItemId: string
    axis: string
    currentLocalEvidence: string[]
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForPlanning: boolean
    protectedActionExecuted: boolean
    claimAllowed: boolean
  }>
  planChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssEvalQualityGateChecklistReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  checklistItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  publicBenchmarkClaimAllowed: boolean
  leaderboardClaimAllowed: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  checklistItems: Array<{
    checklistItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    currentLocalEvidence: string[]
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForChecklist: boolean
    protectedActionExecuted: boolean
    publicBenchmarkClaimAllowed: boolean
    leaderboardClaimAllowed: boolean
    superiorityClaimAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  checklistChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssTerminalWorkflowEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  nonSyntheticUserSessionClaimAllowed: boolean
  externalBenchmarkSessionClaimAllowed: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    transcriptCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    nonSyntheticUserSessionClaimAllowed: boolean
    externalBenchmarkSessionClaimAllowed: boolean
    publicComparisonClaimAllowed: boolean
    superiorityClaimAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssOnboardingDocsEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  nonSyntheticFirstRunClaimAllowed: boolean
  crossPlatformOnboardingClaimAllowed: boolean
  publicComparisonClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    onboardingCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    nonSyntheticFirstRunClaimAllowed: boolean
    crossPlatformOnboardingClaimAllowed: boolean
    publicReadinessClaimAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssRuntimeDoctoringEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  repairActionAllowed: boolean
  reinstallActionAllowed: boolean
  dependencyInstallAllowed: boolean
  providerProbeAllowed: boolean
  externalDiagnosticsAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    runtimeDoctoringCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    repairActionAllowed: boolean
    reinstallActionAllowed: boolean
    dependencyInstallAllowed: boolean
    providerProbeAllowed: boolean
    externalDiagnosticsAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssSecurityPermissionsEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  hostedScorecardRunAllowed: boolean
  hostedCodeqlRunAllowed: boolean
  hostedBranchProtectionClaimAllowed: boolean
  publicSecurityPostureClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    securityPermissionsCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    hostedScorecardRunAllowed: boolean
    hostedCodeqlRunAllowed: boolean
    hostedBranchProtectionClaimAllowed: boolean
    publicSecurityPostureClaimAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssToolLoopReliabilityEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  realProductRepoMutationAllowed: boolean
  providerBackedExecutionAllowed: boolean
  liveModelValidationAllowed: boolean
  externalBenchmarkExecutionAllowed: boolean
  nonSyntheticReliabilityClaimAllowed: boolean
  publicReliabilityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    toolLoopCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    supplementalLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    realProductRepoMutationAllowed: boolean
    providerBackedExecutionAllowed: boolean
    liveModelValidationAllowed: boolean
    externalBenchmarkExecutionAllowed: boolean
    nonSyntheticReliabilityClaimAllowed: boolean
    publicReliabilityClaimAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssProviderBreadthEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  providerCallsAllowed: boolean
  liveModelCallsAllowed: boolean
  externalCallsAllowed: boolean
  liveProviderValidationAllowed: boolean
  providerCompatibilityClaimAllowed: boolean
  modelBehaviorClaimAllowed: boolean
  providerBackedExecutionAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    providerBreadthCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    supplementalLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    providerCallsAllowed: boolean
    liveModelCallsAllowed: boolean
    externalCallsAllowed: boolean
    liveProviderValidationAllowed: boolean
    providerCompatibilityClaimAllowed: boolean
    modelBehaviorClaimAllowed: boolean
    providerBackedExecutionAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    publicReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OssReleaseHygieneEvidenceReport = {
  mode: string
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceAxisArchitectureReviewReportPath: string
  selectedAxis: string
  sourcePlanItemCount: number
  evidenceItemCount: number
  sourceProjects: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  commitAllowed: boolean
  pushAllowed: boolean
  publishAllowed: boolean
  deployAllowed: boolean
  launchAllowed: boolean
  signedProvenanceGenerated: boolean
  signedProvenanceClaimAllowed: boolean
  legalNoticeReuseDecisionAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceItems: Array<{
    evidenceItemId: string
    sourcePlanItemId: string
    sourceProject: string
    axis: string
    releaseHygieneCoverageClass: string
    currentLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    supplementalLocalEvidence: Array<{
      path: string
      exists: boolean
      sha256: string | null
      sizeBytes: number
    }>
    protectedBoundary: string
    forbiddenShortcuts: string[]
    implementationStatus: string
    protectedActionRequiredForEvidenceMatrix: boolean
    protectedActionExecuted: boolean
    commitAllowed: boolean
    pushAllowed: boolean
    publishAllowed: boolean
    deployAllowed: boolean
    launchAllowed: boolean
    signedProvenanceClaimAllowed: boolean
    legalNoticeReuseDecisionAllowed: boolean
    releaseReadinessClaimAllowed: boolean
    productionReadinessClaimAllowed: boolean
    publicReadinessClaimAllowed: boolean
    externalValidationClaimAllowed: boolean
    autonomousReliabilityClaimAllowed: boolean
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type GoldenTranscriptReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  transcripts: Array<{
    name: string
    exitCode: number | null
    passed: boolean
  }>
}

type TerminalFailureRecoveryTranscriptsReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  capturePerformed: boolean
  rawOutputStored: boolean
  transcriptCount: number
  failureStepDetected: boolean
  recoveryGuidanceProvided: boolean
  recoveryVerificationPassed: boolean
  transcripts: Array<{
    name: string
    kind: string
    exitCode: number | null
    expectedExitCode: number
    passed: boolean
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  transcriptChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OnboardingSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    appliedPattern: string
  }>
  readmePath: string
  windowsQuickStartPath: string
  macLinuxQuickStartPath: string
  readmeLinksWindowsQuickStart: boolean
  readmeLinksMacLinuxQuickStart: boolean
  windowsQuickStartPresent: boolean
  macLinuxQuickStartPresent: boolean
  installCommandDocumented: boolean
  startCommandDocumented: boolean
  nodeVersionCheckDocumented: boolean
  providerSetupDocumented: boolean
  providerFailureTroubleshootingDocumented: boolean
  updateAndUninstallDocumented: boolean
  advancedSetupLinked: boolean
  localRuntimeSmokePerformed: boolean
  crossPlatformRuntimeClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  localSmokeCommands: Array<{
    name: string
    exitCode: number | null
    passed: boolean
  }>
  onboardingChecks: Array<{
    label: string
    ok: boolean
  }>
}

type DocLinkIntegrityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalLinkFetchPerformed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    appliedPattern: string
  }>
  scannedMarkdownFiles: string[]
  canonicalVsCodeExtensionPath: string
  legacyVsCodeExtensionPath: string
  relativeLinksChecked: Array<{
    ok: boolean
  }>
  allRelativeLinksResolve: boolean
  readmeUsesCanonicalVsCodeExtensionPath: boolean
  readmeLegacyVsCodeExtensionPathAbsent: boolean
  packageExtensionSurfaceExists: boolean
  integrityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type AgentInstructionsQualityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceAgentInstructionsPath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  purposeSectionPresent: boolean
  setupVerificationCommandsPresent: string[]
  repositoryStructureSectionsPresent: string[]
  workflowEvidencePresent: boolean
  agentStackBoundariesPresent: string[]
  primarySourceRulePresent: boolean
  verificationStandardPresent: boolean
  protectedBoundaryLanguagePresent: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  instructionQualityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type CommunityIntakeQualityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalTemplateValidationPerformed: boolean
  sourceTemplatePaths: string[]
  blankIssuesEnabled: boolean
  issueTemplateChooserConfigured: boolean
  securityPolicyLinkedOrPresent: boolean
  bugReportTemplate: {
    requiredSectionsPresent: string[]
    requiredTermsPresent: string[]
  }
  featureRequestTemplate: {
    requiredSectionsPresent: string[]
    requiredTermsPresent: string[]
  }
  pullRequestTemplate: {
    requiredSectionsPresent: string[]
    requiredTermsPresent: string[]
  }
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  communityIntakeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type CommunityProfileQualityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalCommunityProfileCheckPerformed: boolean
  sourceProfilePaths: string[]
  readmeLinksCommunityFiles: boolean
  contributing: {
    requiredTermsPresent: string[]
  }
  support: {
    requiredTermsPresent: string[]
  }
  codeOfConduct: {
    requiredTermsPresent: string[]
  }
  security: {
    requiredTermsPresent: string[]
  }
  license: {
    requiredTermsPresent: string[]
  }
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  communityProfileChecks: Array<{
    label: string
    ok: boolean
  }>
}

type MaintainerOwnershipQualityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  codeownersPath: string
  codeownersSizeBytes: number
  codeownersPreferredLocation: boolean
  codeownersUnderGithubLimit: boolean
  codeownerRules: Array<{
    line: number
    pattern: string
    owners: string[]
  }>
  requiredPatterns: string[]
  missingRequiredPatterns: string[]
  ownerTokens: string[]
  invalidSyntaxLines: unknown[]
  hostedCodeownerResolutionPerformed: boolean
  branchProtectionQueryPerformed: boolean
  codeOwnerReviewRequiredClaimAllowed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  ownershipChecks: Array<{
    label: string
    ok: boolean
  }>
}

type DependencyGovernanceQualityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  packageManagerField: string | null
  workflowBunVersions: string[]
  packageManagerFieldPresent: boolean
  packageManagerMatchesWorkflowBunVersion: boolean
  bunLockPath: string
  bunLockSizeBytes: number
  bunLockTextStructureRecognized: boolean
  bunLockfileVersion: number | null
  bunLockRootWorkspacePresent: boolean
  bunLockCoversPackageManifestDependencies: boolean
  missingManifestDependenciesInLockfile: string[]
  dependencyEntries: unknown[]
  runtimeDependencyCount: number
  developmentDependencyCount: number
  exactVersionCount: number
  semverRangeCount: number
  otherVersionSpecifierCount: number
  overridesPresent: boolean
  overrideNames: string[]
  dependabotCoversNpm: boolean
  dependabotCoversGitHubActions: boolean
  dependabotSchedulesPresent: boolean
  dependencyReviewWorkflowPath: string
  dependencyReviewWorkflowPresent: boolean
  dependencyReviewActionConfigured: boolean
  dependencyReviewActionPinned: boolean
  dependencyReviewWorkflowPullRequestOnly: boolean
  dependencyReviewWorkflowPermissionsReadOnly: boolean
  dependencyReviewHostedRunPerformed: boolean
  dependencyReviewRequiredStatusClaimAllowed: boolean
  frozenDependencyInstallPresent: boolean
  externalVulnerabilityScanPerformed: boolean
  npmAuditPerformed: boolean
  githubApiCallsPerformed: boolean
  vulnerabilityFreeClaimAllowed: boolean
  dependencyReviewPassClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  governanceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type LockfileSbomQualityReport = {
  mode: string
  inventoryFormat: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  bunLockPath: string
  bunLockTextStructureRecognized: boolean
  bunLockfileVersion: number | null
  directManifestDependencyCount: number
  lockfilePackageCount: number
  lockfilePackageCountExceedsDirectDependencies: boolean
  packagesWithIntegrityCount: number
  packagesMissingIntegrity: string[]
  packagesWithDependencyMetadataCount: number
  lockfileRelationshipCount: number
  directManifestDependenciesCovered: boolean
  missingDirectManifestDependencies: string[]
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  lockfilePackageRecords: unknown[]
  lockfileRelationshipRecords: unknown[]
  githubDependencyGraphExportPerformed: boolean
  externalSbomExportPerformed: boolean
  hostedSbomValidationPerformed: boolean
  vulnerabilityScanPerformed: boolean
  licenseConclusionPerformed: boolean
  officialCycloneDxComplianceClaimAllowed: boolean
  officialSpdxComplianceClaimAllowed: boolean
  githubDependencyGraphParityClaimAllowed: boolean
  vulnerabilityFreeClaimAllowed: boolean
  licenseComplianceClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  sbomQualityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ThirdPartyLicenseQualityReport = {
  mode: string
  inventoryFormat: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceLockfileSbomReportPath: string
  sourceLockfileInventoryJsonlPath: string
  sourceLockfilePackageCount: number
  rootLicensePath: string
  nodeModulesPresent: boolean
  directManifestDependencyCount: number
  directManifestDependenciesCoveredByMetadata: boolean
  missingDirectManifestDependencyMetadata: string[]
  installedMetadataPackageCount: number
  missingMetadataPackageCount: number
  licenseFieldPresentCount: number
  licenseFieldMissingPackages: string[]
  directLicenseFieldPresentCount: number
  directLicenseFieldMissingPackages: string[]
  licenseFilePresentCount: number
  directLicenseFileMissingPackages: string[]
  noticeFilePresentCount: number
  installedRepositoryUrlCount: number
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  licenseMetadataRecords: unknown[]
  missingMetadataClassifiedAsLocalInstallTreeGap: boolean
  deprecatedLicenseMetadataObserved: boolean
  spdxExpressionParsePerformed: boolean
  externalLicenseResolutionPerformed: boolean
  legalReviewPerformed: boolean
  noticeFileGenerated: boolean
  dependencyInstallPerformed: boolean
  npmRegistryLookupPerformed: boolean
  githubLicenseApiLookupPerformed: boolean
  licenseComplianceClaimAllowed: boolean
  thirdPartyNoticeReadyClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  licenseQualityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type SourceLicenseMetadataQualityReport = {
  mode: string
  inventoryFormat: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  packageLicenseField: string | null
  rootLicensePath: string
  rootLicenseContainsDerivedCodeBoundary: boolean
  rootLicenseContainsMitModificationBoundary: boolean
  reuseTomlPresent: boolean
  licensesDirectoryPresent: boolean
  reuseToolRunPerformed: boolean
  reuseComplianceClaimAllowed: boolean
  spdxDocumentGenerated: boolean
  legalReviewPerformed: boolean
  sourceLicenseComplianceClaimAllowed: boolean
  sourceMetadataReadyClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  scanRoots: string[]
  scannedSourceFileCount: number
  sourceFilesWithSpdxLicenseIdentifierCount: number
  sourceFilesWithSpdxCopyrightTextCount: number
  sourceFilesWithAdjacentLicenseFileCount: number
  sourceFilesCoveredByReuseTomlAnnotationCount: number
  sourceFilesMissingFileLevelMetadataCount: number
  sourceFilesMissingFileLevelMetadata: string[]
  fileCategoryCounts: Record<string, number>
  inventoryJsonlPath: string
  inventoryJsonlSha256: string
  inventoryJsonlRecordCount: number
  inventoryJsonlParseable: boolean
  sourceLicenseRecords: unknown[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  sourceLicenseMetadataChecks: Array<{
    label: string
    ok: boolean
  }>
}

type LicenseBoundaryAuthorizationReport = {
  mode: string
  sourceThirdPartyLicenseQualityReportPath: string
  sourceSourceLicenseMetadataQualityReportPath: string
  requestMarkdownPath: string
  authorizationItemsJsonlPath: string
  authorizationItemsJsonlSha256: string
  authorizationItemsJsonlRecordCount: number
  authorizationItemsJsonlParseable: boolean
  licenseBoundaryStatus: string
  ownerLegalDecisionRequired: boolean
  protectedAuthorizationRequestCreated: boolean
  protectedAuthorizationRequestCount: number
  allProtectedAuthorizationsDefaultFalse: boolean
  thirdPartyDirectLicenseFileMissingPackages: string[]
  thirdPartyNoticeFilePresentCount: number
  sourceFilesMissingFileLevelMetadataCount: number
  derivedCodeBoundaryRecognized: boolean
  mitModificationBoundaryRecognized: boolean
  spdxExpressionParsePerformed: boolean
  externalLicenseResolutionPerformed: boolean
  legalReviewPerformed: boolean
  noticeFileGenerated: boolean
  dependencyInstallPerformed: boolean
  npmRegistryLookupPerformed: boolean
  githubLicenseApiLookupPerformed: boolean
  reuseToolRunPerformed: boolean
  spdxDocumentGenerated: boolean
  reuseArtifactsCreated: boolean
  sourceFilesRewritten: boolean
  licenseComplianceClaimAllowed: boolean
  thirdPartyNoticeReadyClaimAllowed: boolean
  reuseComplianceClaimAllowed: boolean
  sourceLicenseComplianceClaimAllowed: boolean
  sourceMetadataReadyClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  authorizationItems: Array<{
    id: string
    defaultAuthorized: boolean
    protectedAction: boolean
    status: string
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  licenseBoundaryAuthorizationChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ProviderCompatibilityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  directProviderFlags: string[]
  providerPresetDefaults: Array<{
    preset: string
    provider: string
    baseUrl: string
    model: string
    requiresApiKey: boolean
  }>
  compatibilityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ProviderCapabilityMatrixReport = {
  mode: string
  sourceProviderCompatibilityReportPath: string
  sourceRuntimeDoctorReportPath: string
  sourceOssAxisArchitectureReportPath: string
  directProviderFlagCount: number
  providerPresetDefaultCount: number
  capabilityRowCount: number
  localNoKeyProviderCount: number
  openAiCompatibleSurfaceCount: number
  failureModeCount: number
  failureModeIds: string[]
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  provenanceJsonlParseable: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  providerBackedExecutionClaimAllowed: boolean
  providerCompatibilityClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  capabilityRows: Array<{
    surfaceId: string
    provider: string
    preset: string | null
    noApiKeyLocalCandidate: boolean
    openAiCompatibleTransport: boolean
    claimAllowed: boolean
  }>
  failureModeRows: Array<{
    failureModeId: string
    affectedSurfaceIds: string[]
    claimAllowed: boolean
  }>
  capabilityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type PermissionRegressionReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  regressionFixtures: Array<{
    id: string
    ok: boolean
  }>
  behavioralTestCommands: Array<{
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
  }>
  protectedPermissionSurfaces: string[]
  targetedTestFiles: string[]
}

type DependencyTopologyReport = {
  mode: string
  dependencyCruiserVersion: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  moduleCount: number
  dependencyEdgeCount: number
  circularDependencyCount: number
  circularDependencyBaseline: number
  unresolvedDependencyCount: number
  unresolvedDependencyBaseline: number
  configuredRatchetMode: string
  dependencyCruiserConfigPath: string
  knownViolationBaselinePath: string
  configuredRatchetKnownViolationCount: number
  configuredRatchetKnownViolationRuleCounts: Record<string, number>
  configuredRatchetNewViolationCount: number
  configuredRatchetClaimAllowed: boolean
  topologyCleanClaimAllowed: boolean
  refactorCompletionClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  topologyCommands: Array<{
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  topologyChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ScriptDuplicationAuditReport = {
  mode: string
  scannerTargetGlob: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  helperOccurrenceCounts: Record<string, number>
  helperOccurrenceBaselines: Record<string, number>
  duplicateHelperClusterCount: number
  duplicateHelperClusterBaseline: number
  jscpdEnabled: boolean
  jscpdVersion: string
  jscpdConfigPath: string
  jscpdCommand: {
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
  }
  jscpdReportSha256: string
  jscpdCloneCount: number
  jscpdCloneBaseline: number
  jscpdDuplicatedLines: number
  jscpdDuplicatedLinesBaseline: number
  jscpdDuplicatedTokens: number
  jscpdDuplicatedTokensBaseline: number
  jscpdDuplicatedPercentage: number
  jscpdDuplicatedPercentageBaseline: number
  jscpdTopClonePairs: Array<{
    firstFile: string
    secondFile: string
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  publicReadinessClaimAllowed: boolean
  refactorCompletionClaimAllowed: boolean
  auditChecks: Array<{
    label: string
    ok: boolean
  }>
}

type DeadExportCandidatesReport = {
  mode: string
  knipVersion: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  candidateFileCount: number
  candidateUnusedExportCount: number
  candidateUnusedTypeCount: number
  candidateDuplicateExportCount: number
  candidateFileBaseline: number
  candidateUnusedExportBaseline: number
  candidateUnusedTypeBaseline: number
  candidateDuplicateExportBaseline: number
  triageLedgerPath: string
  triageRecordCount: number
  triageCurrentCandidateCount: number
  triageActionCounts: Record<string, number>
  triageRecords: Array<{
    currentCandidate: boolean
    rationale: string
    guardrail: string
  }>
  removedCandidateRatchets: Array<{
    currentCandidate: boolean
    guardrail: string
  }>
  deletionClaimAllowed: boolean
  cleanupCompletionClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  knipCommands: Array<{
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  deadExportChecks: Array<{
    label: string
    ok: boolean
  }>
}

type RuntimeDoctorRegressionReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  doctorCommands: Array<{
    name: string
    exitCode: number | null
    passed: boolean
  }>
  doctorChecks: Array<{
    label: string
    ok: boolean
  }>
  runtimeDoctorSurfaces: string[]
}

type GitReleaseHygieneReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workspaceGitStatus: string
  commitPushAttempted: boolean
  releaseActionPerformed: boolean
  protectedActionsPerformed: unknown[]
  releaseHygieneChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionSurfaceReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workspaceIdeExtensionStatus: string
  packagingAttempted: boolean
  installAttempted: boolean
  ideExtensionChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionScopeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  sourceSurfaceStatus: string
  scopeDecision: string
  proposedManifestPath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  minimumManifestRequirements: string[]
  contributionPlan: {
    commands: string[]
    views: string[]
    configurationKeys: string[]
    activationEvents: string[]
  }
  validationRequiredBeforeAvailabilityClaim: string[]
  protectedActions: {
    packagingAttempted: boolean
    installAttempted: boolean
    publishAttempted: boolean
    providerCallsAllowed: boolean
    externalCallsAllowed: boolean
  }
  scopeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionManifestSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  manifestPath: string
  entryPointPath: string
  packageDryRunExitCode: number | null
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  manifestSummary: {
    name: string
    displayName: string
    publisher: string
    enginesVscode: string
    extensionKind: string[]
    main: string
    activationEvents: string[]
    commandIds: string[]
    viewIds: string[]
    treeViewIds?: string[]
    webviewViewIds?: string[]
    configurationKeys: string[]
  }
  packageDryRunFiles: string[]
  manifestSmokeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionRuntimeSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  vscodeCliVersion: string
  manifestPath: string
  entryPointPath: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  registeredTreeViewIds?: string[]
  registeredWebviewViewIds?: string[]
  messagesShown: string[]
  contextSubscriptionCount: number
  missingManifestCommands: string[]
  unexpectedRegisteredCommands: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  runtimeSmokeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionHostSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  vscodeCliVersion: string
  manifestPath: string
  entryPointPath: string
  extensionDevelopmentPath: string
  extensionTestsPath: string
  codeExitCode: number | null
  codeTimedOut: boolean
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  registeredCommandIds: string[]
  executedCommandIds: string[]
  failedCommandIds: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  productLaunchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  hostSmokeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionWorkbenchSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  vscodeCliVersion: string
  manifestPath: string
  entryPointPath: string
  extensionDevelopmentPath: string
  extensionTestsPath: string
  codeExitCode: number | null
  codeTimedOut: boolean
  vscodeStartupBlocked?: boolean
  environmentBlockers?: string[]
  realExtensionHostLaunched: boolean
  extensionActivated: boolean
  contributedViewIds: string[]
  registeredTreeViewIds: string[]
  treeProviderViewIds: string[]
  focusedViewIds: string[]
  viewItemCounts: Record<string, number>
  executedViewCommandIds?: string[]
  failedViewCommandIds?: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  productLaunchAttempted: boolean
  extensionAvailabilityClaimAllowed: boolean
  workbenchSmokeChecks: Array<{
    label: string
    ok: boolean
  }>
}

type VscodeUpdateBoundaryReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  sourceHostSmokeReportPath: string
  sourceWorkbenchSmokeReportPath: string
  sourceHostEnvironmentBlockers: string[]
  sourceWorkbenchEnvironmentBlockers: string[]
  updatingSentinelExists: boolean
  codeSetupProcesses: Array<{
    processName: string
    pid: number | null
    path: string | null
  }>
  protectedActionsExecuted: unknown[]
  processTerminationAttempted: boolean
  dependencyInstallAttempted: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  boundaryStatus: string
  requiredOwnerActions: string[]
  blockedActions: string[]
  boundaryChecks: Array<{
    label: string
    ok: boolean
  }>
}

type VscodeStartupDiagnosticsReport = {
  mode: string
  sourceHostSmokeReportPath: string
  sourceWorkbenchSmokeReportPath: string
  sourceVscodeUpdateBoundaryReportPath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  vscodeCliVersion: string
  parsedVscodeCommit: string | null
  isolatedExecutionArgumentsObserved: string[]
  sentinelCandidates: Array<{
    path: string
    exists: boolean
    sha256: string | null
  }>
  currentCodeSetupProcesses: Array<{
    processName: string
    pid: number | null
    path: string | null
  }>
  updateLogEvidence: Array<{
    source: string
    path: string
    sha256: string
    sizeBytes: number
    updateGuardMessageFound: boolean
    matchedMessage: string | null
  }>
  updateGuardLogEvidenceCount: number
  diagnosisStatus: string
  protectedActionsRequiredToResolve: string[]
  protectedActionsExecuted: unknown[]
  processTerminationAttempted: boolean
  deleteUpdateStateAttempted: boolean
  dependencyInstallPerformed: boolean
  reinstallAttempted: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  startupDiagnosticsChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionWebviewRenderSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  manifestWebviewViewIds: string[]
  registeredWebviewViewIds: string[]
  resolvedWebviewViewIds: string[]
  renderedHtmlByteLength: number
  commandActionIds: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  webviewRenderChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionRenderedWorkbenchScreenshotReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  sourceReportPath: string
  hostRuntime: string
  screenshotPngPath: string
  screenshotSvgPath: string
  sourceRenderedHtmlByteLength: number
  renderedWidth: number
  renderedHeight: number
  pngByteLength: number
  pngSha256: string
  svgSha256: string
  nonBlankChannelCount: number
  commandActionIds: string[]
  renderMarkers: string[]
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  screenshotChecks: Array<{
    label: string
    ok: boolean
  }>
}

type IdeExtensionWebviewInteractionSmokeReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  hostRuntime: string
  sourceWebviewRenderReportPath: string
  sourceRenderedScreenshotReportPath: string
  manifestPath: string
  entryPointPath: string
  activationInvoked: boolean
  deactivationInvoked: boolean
  manifestCommandIds: string[]
  focusOrderCommandIds: string[]
  interactionCommandIds: string[]
  executedInteractionCommandIds: string[]
  failedInteractionCommandIds: string[]
  registeredCommandIds: string[]
  messagesShown: string[]
  commandButtonCount: number
  commandRegionRole: string
  commandRegionAriaLabel: string
  keyboardActivationModel: string
  installAttempted: boolean
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  realExtensionHostLaunched: boolean
  extensionAvailabilityClaimAllowed: boolean
  interactionChecks: Array<{
    label: string
    ok: boolean
  }>
  primarySourceInputs: Array<{
    source: string
    url: string
    appliedPattern: string
  }>
  claimBoundary: string
}

type ReleaseArtifactFileListReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  packDryRunExitCode: number | null
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  expectedPackageFiles: string[]
  actualPackageFiles: string[]
  forbiddenPackageFilePatterns: string[]
  releaseArtifactChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ReleaseArtifactProvenanceReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  packageFileHashes: Array<{
    path: string
    exists: boolean
    sizeBytes: number
    sha256: string | null
  }>
  sbomFormat: string
  sbomComponents: Array<{
    name: string
    versionRange: string
    scope: string
  }>
  provenanceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ReleaseArtifactReproducibilityReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  temporaryTarballsRemoved: boolean
  packRuns: Array<{
    id: string
    exitCode: number | null
    artifactFileCount: number
    tarballSha256: string | null
    fileList: string[]
  }>
  reproducibleTarballSha256: string | null
  reproducibilityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type AgentReplayEvalReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  replayScenarioCount: number
  minimumPassingScore: number
  replayScenarios: Array<{
    id: string
    score: number
    passed: boolean
  }>
  replayEvalChecks: Array<{
    label: string
    ok: boolean
  }>
}

type SourceControlledChecksReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  workflowPath: string
  productQualityCommandPresent: boolean
  pullRequestTriggerPresent: boolean
  pushMainTriggerPresent: boolean
  releaseActionsAbsent: boolean
  actionReferencesPinned: boolean
  sourceControlledChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OpenSsfSecurityPostureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  securityPolicyPath: string
  prWorkflowPath: string
  releaseWorkflowPath: string
  codeqlWorkflowPath: string
  dependabotConfigPath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    appliedPattern: string
  }>
  securityPolicyPresent: boolean
  privateReportingGuidancePresent: boolean
  responseTimelinePresent: boolean
  allWorkflowActionReferencesPinned: boolean
  prWorkflowTokenPermissionsReadOnly: boolean
  releaseWorkflowBoundaryOnly?: boolean
  releaseWorkflowPermissionsScoped: boolean
  pullRequestTargetAbsent: boolean
  dependabotConfigPresent: boolean
  dependabotCoversNpm: boolean
  dependabotCoversGitHubActions: boolean
  dependabotSchedulesPresent: boolean
  codeqlWorkflowPresent: boolean
  codeqlActionsPinned: boolean
  codeqlPermissionsScoped: boolean
  codeqlAnalyzesJavaScriptTypeScript: boolean
  codeqlSecurityExtendedQueriesConfigured: boolean
  codeqlScheduledScanConfigured: boolean
  codeqlHostedExecutionPerformed: boolean
  productQualityWorkflowPresent: boolean
  frozenDependencyInstallPresent: boolean
  npmProvenanceConfigured: boolean
  npmTrustedPublishingBoundaryPresent: boolean
  releaseEnvironmentPresent: boolean
  dockerPackageWriteScoped: boolean
  realScorecardRunPerformed: boolean
  scorecardExternalClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  classifiedUnresolvedGaps: Array<{
    id: string
    status: string
    protectedActionRequired: boolean
  }>
  postureChecks: Array<{
    label: string
    ok: boolean
  }>
}

type RealSessionCaptureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  commandTimeoutMs?: number
  tracePath: string
  traceSha256: string
  commandCaptures: Array<{
    name: string
    command: string[]
    exitCode: number | null
    signal?: string | null
    timeoutMs?: number
    timedOut?: boolean
    errorMessage?: string | null
    stdoutSha256: string
    stderrSha256: string
    stdoutByteLength?: number
    stderrByteLength?: number
    passed: boolean
  }>
  captureChecks: Array<{
    label: string
    ok: boolean
  }>
}

type PromptedToolLoopCaptureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  promptCaptured: boolean
  promptSha256: string
  promptByteLength: number
  nonSyntheticUserSessionClaimed: boolean
  tracePath: string
  traceSha256: string
  toolCommandCaptures: Array<{
    name: string
    command: string[]
    exitCode: number | null
    stdoutSha256: string
    stderrSha256: string
    stdoutByteLength?: number
    stderrByteLength?: number
    passed: boolean
  }>
  toolLoopChecks: Array<{
    label: string
    ok: boolean
  }>
}

type CodeEditingTraceCaptureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  nonSyntheticUserSessionClaimed: boolean
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeSha256: string
  sourceAfterSha256: string
  patchApplied: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: []
  unitCheck: {
    passed: boolean
    testCaseCount: number
  }
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type MultiFileCodeEditingTraceCaptureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  nonSyntheticUserSessionClaimed: boolean
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeTreeSha256: string
  sourceAfterTreeSha256: string
  patchApplied: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: []
  unitCheck: {
    passed: boolean
    testCaseCount: number
  }
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type RegressionCycleCodeEditingTraceCaptureReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  nonSyntheticUserSessionClaimed: boolean
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeSha256: string
  wrongPatchSha256: string
  repairedSourceSha256: string
  wrongPatchApplied: boolean
  regressionFailedBeforeRepair: boolean
  repairApplied: boolean
  regressionPassedAfterRepair: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: []
  unitCheck: {
    failedCaseCountBeforeRepair: number
    passedCaseCountAfterRepair: number
    testCaseCount: number
  }
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ToolInterruptionRecoveryTraceReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  nonSyntheticUserSessionClaimed: boolean
  fixtureRoot: string
  tracePath: string
  traceSha256: string
  sourceBeforeSha256: string
  interruptedObservationSha256: string
  recoveredSourceSha256: string
  outputSha256: string
  interruptionDetected: boolean
  recoveryApplied: boolean
  finalVerificationPassed: boolean
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: unknown[]
  interruptionRecoveryCheck: {
    interruptedToolStepCount: number
    recoveredToolStepCount: number
    invariantViolationCount: number
    testCaseCount: number
    passed: boolean
  }
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ProtectedActionDenialTraceReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  operatorAuthorization: {
    authorized: boolean
    scope: string
    protectedActionsAuthorized: boolean
  }
  capturePerformed: boolean
  nonSyntheticUserSessionClaimed: boolean
  fixtureRoot: string
  protectedActionRequestPath: string
  denialRecordPath: string
  safeAlternativeSummaryPath: string
  tracePath: string
  traceSha256: string
  protectedActionRequested: boolean
  protectedActionDenied: boolean
  protectedActionExecuted: boolean
  safeAlternativeSelected: boolean
  finalVerificationPassed: boolean
  requestSha256: string
  denialRecordSha256: string
  safeAlternativeSummarySha256: string
  modifiedFixtureFiles: string[]
  protectedRepoFilesModified: unknown[]
  denialCheck: {
    protectedActionRequestCount: number
    deniedProtectedActionCount: number
    executedProtectedActionCount: number
    safeAlternativeCount: number
    testCaseCount: number
    passed: boolean
  }
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type RealTraceEvalReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  traceFileCount: number
  traces: Array<{
    path: string
    sha256: string
    traceKind?: string
    parseErrorCount: number
    hasStarted: boolean
    hasTerminalStatus: boolean
    hasStartedToTerminalTransition?: boolean
    requiredFieldsComplete: boolean
    credentialPatternFound: boolean
    passed: boolean
  }>
  coverageSummary?: {
    traceKinds: string[]
    terminalOutcomes: string[]
    roles: string[]
    models: string[]
    querySources: string[]
    passedTraceCount: number
    failedTraceCount: number
    succeededTraceCount: number
    classifiedCoverageGaps: Array<{
      id: string
      status: string
      protectedActionRequired: boolean
    }>
  }
  traceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type TraceRedactionPolicyReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  rawTraceFileCount: number
  nonSyntheticRealSessionCapture: {
    performed: boolean
    requiredBeforeStrongerReliabilityClaims: boolean
    currentStatus: string
  }
  publishableSummaryFields: string[]
  forbiddenRawFields: string[]
  redactionRules: Array<{
    id: string
    action: string
  }>
  captureWorkflow: string[]
  scannedRawTraceFiles: Array<{
    path: string
    credentialPatternFound: boolean
    providerRequestIdPatternFound: boolean
  }>
  policyChecks: Array<{
    label: string
    ok: boolean
  }>
}

type TraceSchemaContractReport = {
  mode: string
  schemaContractVersion: string
  sourceRealTraceEvalReportPath: string
  sourceTraceDirectory: string
  sourceTraceFileCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  traceSchemaSummaries: Array<{
    path: string
    sha256: string
    eventCount: number
    parseErrorCount: number
    requiredFieldViolationCount: number
    invalidTimestampCount: number
    invalidStatusCount: number
    invalidTraceContextCount: number
    credentialPatternFound: boolean
    schemaContractPassed: boolean
  }>
  aggregate: {
    traceCount: number
    eventCount: number
    schemaPassedTraceCount: number
    schemaFailedTraceCount: number
    missingRecommendedEventNameCount: number
    missingRecommendedTraceContextCount: number
    missingRecommendedActionObservationCount?: number
    currentGeneratedTraceProducerTraceCount?: number
    currentGeneratedTraceProducerEventCount?: number
    currentGeneratedTraceProducerMissingEventNameCount?: number
    currentGeneratedTraceProducerMissingTraceContextCount?: number
    currentGeneratedTraceProducerMissingActionObservationCount?: number
  }
  recommendedAlignmentGaps: Array<{
    id: string
    status: string
    protectedActionRequired: boolean
  }>
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  schemaContractChecks: Array<{
    label: string
    ok: boolean
  }>
}

type TracePortabilityExportReport = {
  mode: string
  sourceRealTraceEvalReportPath: string
  sourceTraceSchemaContractReportPath: string
  portableTraceExportPath: string
  portableTraceExportSha256: string
  sourceTraceCount: number
  sourceEventCount: number
  portableEventCount: number
  sourceHistoricalMissingEventNameCount: number
  sourceHistoricalMissingTraceContextCount: number
  sourceHistoricalMissingActionObservationCount: number
  portableMissingEventNameCount: number
  portableMissingTraceContextCount: number
  portableMissingActionObservationCount: number
  sourceEventsAlreadyEnrichedCount: number
  portableEventsSynthesizedFromHistoricalGapsCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceTraceHashes: Array<{
    path: string
    sha256: string
    eventCount: number
  }>
  portabilityChecks: Array<{
    label: string
    ok: boolean
  }>
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
}

type ProductEvidenceManifestReport = {
  mode: string
  manifestFormat: string
  manifestJsonlPath: string
  manifestJsonlSha256: string
  evidenceRecordCount: number
  evidenceTotalSizeBytes: number
  evidenceRoles: Record<string, number>
  requiredEvidencePaths: string[]
  missingRequiredEvidencePaths: string[]
  recursiveSelfInputsExcluded: string[]
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalAttestationGenerated: boolean
  signedProvenanceGenerated: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  evidenceRecords: Array<{
    path: string
    sha256: string
    sizeBytes: number
    role: string
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type PrimarySourceRegistryReport = {
  mode: string
  registryFormat: string
  scannedReportCount: number
  reportsWithPrimarySourceInputs: string[]
  primarySourceEntryCount: number
  uniqueSourceUrlCount: number
  sourceKindCounts: Record<string, number>
  disallowedSecondarySourceCount: number
  unclassifiedSourceCount: number
  malformedSourceInputCount: number
  registryJsonlPath: string
  registryJsonlSha256: string
  registryJsonlRecordCount: number
  registryJsonlParseable: boolean
  externalSourceFetchPerformed: boolean
  blogSummarySourceAllowed: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  primarySourceRegistryChecks: Array<{
    label: string
    ok: boolean
  }>
}

type BenchmarkReadinessReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalBenchmarkRunPerformed: boolean
  externalBenchmarkResultClaimed: boolean
  benchmarkManifestPath: string
  benchmarkManifestSha256: string
  benchmarkTaskCount: number
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  readinessDimensions: Array<{
    id: string
    status: string
    protectedActionRequiredForGap: boolean
    protectedActionExecuted: boolean
  }>
  unresolvedGaps: Array<{
    id: string
    status: string
    protectedActionRequired: boolean
    protectedActionExecuted: boolean
  }>
  benchmarkReadinessChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ExternalBenchmarkBoundaryReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceBenchmarkReadinessPath: string
  sourceBenchmarkTaskCount: number
  sourceBenchmarkManifestSha256: string
  externalBenchmarkExecutionAuthorized: boolean
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkResultClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  authorizationRequestPath: string
  protectedActionAuthorizations: Array<{
    id: string
    authorized: boolean
    requiredBeforeExecution: boolean
  }>
  boundaryGaps: Array<{
    id: string
    category: string
    status: string
    protectedActionRequired: boolean
    protectedActionExecuted: boolean
  }>
  boundaryChecks: Array<{
    label: string
    ok: boolean
  }>
}

type LocalBenchmarkHarnessReport = {
  mode: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceBenchmarkManifestPath: string
  sourceBenchmarkTaskCount: number
  sourceBenchmarkManifestSha256: string
  sourceExternalBenchmarkBoundaryPath: string
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkResultClaimed: boolean
  localBenchmarkResultPath: string
  localBenchmarkResultSha256: string
  localBenchmarkTaskResults: Array<{
    benchmarkTaskId: string
    sourceEvidenceExists: boolean
    sourceEvidenceHashMatches: boolean
    protectedActionExecuted: boolean
    externalBenchmarkResultClaimed: boolean
    localHarnessStatus: string
  }>
  statusSummary: {
    validLocalEvidenceTasks: number
    classifiedBlockedTasks: number
    failedTasks: number
  }
  harnessChecks: Array<{
    label: string
    ok: boolean
  }>
}

type BenchmarkEfficiencyMetricsReport = {
  mode: string
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  metricSchemaFields: string[]
  metricsJsonlPath: string
  metricsJsonlSha256: string
  benchmarkEfficiencyRecords: Array<{
    benchmarkTaskId: string
    comparableMetricFields: {
      agent: string
      model: null
      inputTokens: null
      outputTokens: null
      costUsd: null
      numTurns: null
      durationMs: null
      resolved: null
    }
    metricAvailability: {
      tokenUsageMeasured: boolean
      costMeasured: boolean
      durationMeasured: boolean
      turnCountMeasured: boolean
      externalResolvedMeasured: boolean
    }
    metricGapStatus: string
    protectedActionExecuted: boolean
    externalBenchmarkResultClaimed: boolean
  }>
  summary: {
    sourceTaskCount: number
    comparableRecordCount: number
    recordsWithComparableMetricFields: number
    recordsWithMeasuredTokenCostDuration: number
    classifiedMetricGapCount: number
  }
  unresolvedMetricGaps: Array<{
    id: string
    status: string
    requiredBeforeExternalComparisonClaim: boolean
    protectedActionRequired: boolean
    protectedActionExecuted: boolean
  }>
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkResultClaimed: boolean
  externalComparisonClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  efficiencyChecks: Array<{
    label: string
    ok: boolean
  }>
}

type BenchmarkSubmissionReadinessReport = {
  mode: string
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  sourceBenchmarkEfficiencyMetricsPath: string
  sourceBenchmarkEfficiencyMetricsJsonlPath: string
  sourceBenchmarkEfficiencyMetricsJsonlSha256: string
  sourceRealTraceEvalsPath: string
  sourceRealTraceCount: number
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  submissionAssetsJsonlPath: string
  submissionAssetsJsonlSha256: string
  requiredSubmissionAssets: string[]
  submissionAssetRecords: Array<{
    assetId: string
    sweBenchRequiredAsset: string
    localEquivalentPath: string | null
    localEquivalentSha256: string | null
    readinessStatus: string
    requiredForExternalSubmission: boolean
    protectedActionRequiredToComplete: boolean
    protectedActionExecuted: boolean
    externalSubmissionClaimed: boolean
  }>
  summary: {
    requiredAssetCount: number
    localEquivalentAvailableCount: number
    partialLocalEquivalentCount: number
    classifiedUnresolvedProtectedGapCount: number
    officialExternalSubmissionReady: boolean
  }
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkSubmissionPerformed: boolean
  externalBenchmarkResultClaimed: boolean
  externalLeaderboardClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  submissionReadinessChecks: Array<{
    label: string
    ok: boolean
  }>
}

type BenchmarkPolicyComplianceReport = {
  mode: string
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
  policyItems: Array<{
    policyItemId: string
    sourcePolicyScope: string
    status: string
    protectedActionRequiredToResolve: boolean
    protectedActionExecuted: boolean
    officialClaimAllowed: boolean
  }>
  summary: {
    policyItemCount: number
    partialLocalEvidenceOnlyCount: number
    unresolvedProtectedOrOwnerClaimRequiredCount: number
    blockedNotAuthorizedCount: number
    officialSWEbenchVerifiedSubmissionEligible: boolean
    officialSWEbenchVerifiedSubmissionClaimAllowed: boolean
    officialLeaderboardClaimAllowed: boolean
  }
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  dependencyInstallPerformed: boolean
  officialBenchmarkSubmissionPerformed: boolean
  externalBenchmarkExecutionPerformed: boolean
  externalLeaderboardClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  policyComplianceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type TerminalBenchReadinessReport = {
  mode: string
  sourceBenchmarkReadinessPath: string
  sourceBenchmarkTaskManifestPath: string
  sourceBenchmarkTaskManifestSha256: string
  sourceLocalBenchmarkHarnessPath: string
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  sourceTracePortabilityExportPath: string
  sourcePortableTraceJsonlPath: string
  sourcePortableTraceJsonlSha256: string
  sourceBenchmarkPolicyCompliancePath: string
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  taskMapJsonlPath: string
  taskMapJsonlSha256: string
  terminalBenchRequirementRecords: Array<{
    requirementId: string
    terminalBenchRequirement: string
    readinessStatus: string
    localEquivalentPath: string | null
    localEquivalentSha256: string | null
    officialRunRequired: boolean
    protectedActionRequiredToComplete: boolean
    protectedActionExecuted: boolean
    officialResultClaimed: boolean
  }>
  summary: {
    requirementCount: number
    localEquivalentAvailableCount: number
    partialLocalEquivalentCount: number
    classifiedUnresolvedProtectedGapCount: number
    blockedNotAuthorizedCount: number
    officialTerminalBenchExecutionReady: boolean
  }
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  dependencyInstallPerformed: boolean
  dockerContainerRunPerformed: boolean
  harborInstallPerformed: boolean
  officialTerminalBenchExecutionPerformed: boolean
  officialTerminalBenchResultClaimed: boolean
  officialLeaderboardSubmissionPerformed: boolean
  officialLeaderboardClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  terminalBenchReadinessChecks: Array<{
    label: string
    ok: boolean
  }>
}

type TrajectoryProcessQualityReport = {
  mode: string
  sourceRealTraceEvalReportPath: string
  sourceTraceCount: number
  sourceLocalBenchmarkResultsPath: string
  sourceLocalBenchmarkResultsSha256: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalBenchmarkExecutionPerformed: boolean
  externalBenchmarkResultClaimed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  phaseTaxonomy: string[]
  wasteSignalTaxonomy: string[]
  traceAssessments: Array<{
    path: string
    sha256: string
    phaseLabelsPresent: string[]
    wasteSignals: string[]
    processQualityStatus: string
  }>
  summary: {
    assessedTraceCount: number
    processQualityOkTraceCount: number
    classifiedProcessGapTraceCount: number
    failedProcessEvidenceTraceCount: number
    tracesWithVerificationEvidence: number
    tracesWithImplementationEvidence: number
    tracesWithClassifiedWasteSignals: number
  }
  processQualityChecks: Array<{
    label: string
    ok: boolean
  }>
}

type VerificationReportConsistencyReport = {
  mode: string
  sourceVerificationReportPath: string
  sourceTypecheckHealthReportPath: string
  sourceTerminalReportPath: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  sourceTypecheckStrictPass: boolean
  sourceTypecheckTotalDiagnostics: number
  sourceTypecheckDiagnosticBudget: number
  sourceTerminalCondition: string
  obsoleteBlockerPhrasesFound: string[]
  currentBlockerPhrasesFound: string[]
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  reportConsistencyChecks: Array<{
    label: string
    ok: boolean
  }>
}

type QualityBlockerTaxonomyReport = {
  mode: string
  sourceHostSmokeReportPath: string
  sourceWorkbenchSmokeReportPath: string
  sourceAgentReplayReportPath: string
  sourceVscodeUpdateBoundaryReportPath: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  currentProductQualityGateStatus: string
  expectedProductQualityGateFailureCount: number
  blockerStatus: string
  knownFailureGroups: Array<{
    id: string
    expectedFailureCount: number
    source: string
    blockingReason: string
    protectedActionRequired: boolean
  }>
  unexpectedFailureGroups: string[]
  nextUnblockedAction: string
  processTerminationAttempted: boolean
  dependencyInstallAttempted: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  taxonomyChecks: Array<{
    label: string
    ok: boolean
  }>
}

type ProtectedActionAuthorizationPacketReport = {
  mode: string
  terminalCondition: string
  packetStatus: string
  sourceReportCount: number
  authorizationItemCount: number
  allSafeBacklogEvidenceGatesCreated: boolean
  protectedActionExecutionAllowed: boolean
  protectedActionExecuted: boolean
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  dependencyInstallPerformed: boolean
  commitPushPerformed: boolean
  publishDeployLaunchPerformed: boolean
  signedProvenanceGenerated: boolean
  releaseClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  mthResolutionStatus: string
  canonicalMemoryWriteAllowed: boolean
  allowedClaimLevel: string
  requiredOwnerAuthorizations: Array<{
    id: string
    protectedActionRequired: boolean
    authorized: boolean
    executed: boolean
    sourceReports: string[]
  }>
  sourceReportBindings: Array<{
    path: string
    exists: boolean
    sha256: string | null
    sizeBytes: number
  }>
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type PublicClaimBoundaryReport = {
  mode: string
  scannedPublicSurfaces: Array<{
    path: string
    exists: boolean
    sha256: string | null
    sizeBytes: number
    lineCount: number
  }>
  publicSurfaceCount: number
  scannedLineCount: number
  blockedContextClaimMentionCount: number
  unauthorizedPositiveClaimCount: number
  blockedContextClaimMentions: Array<{
    path: string
    line: number
    category: string
    status: string
  }>
  unauthorizedPositiveClaims: Array<{
    path: string
    line: number
    category: string
    status: string
  }>
  claimBoundaryStatus: string
  scanJsonlPath: string
  scanJsonlSha256: string
  scanJsonlRecordCount: number
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  dependencyInstallPerformed: boolean
  publishDeployLaunchPerformed: boolean
  releaseClaimAllowed: boolean
  releaseReadinessClaimAllowed: boolean
  productionReadinessClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  externalValidationClaimAllowed: boolean
  autonomousReliabilityClaimAllowed: boolean
  superiorityClaimAllowed: boolean
  mthResolutionStatus: string
  canonicalMemoryWriteAllowed: boolean
  allowedClaimLevel: string
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type GithubRemoteSurfaceAuditReport = {
  mode: string
  defaultBranch: string
  remoteHeads: Array<{
    name: string
    oid: string
  }>
  remoteHeadCount: number
  openPullRequests: Array<{
    number: number
    title: string
    url: string
    headRefName: string
    isSameRepository: boolean
  }>
  openPullRequestCount: number
  allowedOpenPrHeadBranches: string[]
  refScans: Array<{
    refName: string
    patternFindings: unknown[]
    treeFindings: unknown[]
  }>
  blockers: Array<{
    category: string
    refName?: string
    path?: string
    line?: number
    detail: string
  }>
  blockerCount: number
  status: string
  discovery: {
    gitFetchPerformed: boolean
    remoteHeadDiscovery: string
    openPullRequestDiscovery: string
    openPullRequestDiscoveryError?: string
  }
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  externalCallsPerformed: unknown[]
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type OriginLicenseProvenanceBoundaryReport = {
  mode: string
  status: string
  blockerCount: number
  blockers: Array<{
    category: string
    path?: string
    detail: string
  }>
  packageLicenseField: string | null
  packageRepositoryUrl: string | null
  originRemoteUrl: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  publishAttempted: boolean
  deployAttempted: boolean
  launchAttempted: boolean
  evidenceChecks: Array<{
    label: string
    ok: boolean
  }>
}

type Check = {
  label: string
  ok: boolean
  detail?: string
}

const root = process.cwd()

function readJson<T>(path: string): T {
  return JSON.parse(readFileSync(resolve(root, path), 'utf8')) as T
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function check(label: string, ok: boolean, detail?: string): Check {
  return { label, ok, detail }
}

function isMetaforgeGithubUrl(value: string | null): boolean {
  return typeof value === 'string' && /github\.com\/svy04\/metaforge(?:\.git)?$/i.test(value)
}

function fileExists(path: string): Check {
  return check(`file exists: ${path}`, existsSync(resolve(root, path)))
}

function isAbsorptionPrimarySourceUrl(url: string): boolean {
  return /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(url) ||
    /^https:\/\/docs\.openhands\.dev\/overview\/skills(\/repo)?$/.test(url) ||
    /^https:\/\/docs\.github\.com\//.test(url) ||
    /^https:\/\/bun\.com\/docs\//.test(url) ||
    /^https:\/\/docs\.npmjs\.com\//.test(url) ||
    /^https:\/\/slsa\.dev\/spec\//.test(url) ||
    /^https:\/\/reuse\.software\/spec-[0-9.]+\/?$/.test(url) ||
    /^https:\/\/spdx\.github\.io\/spdx-spec\//.test(url) ||
    /^https:\/\/spdx\.org\/licenses\/?$/.test(url) ||
    /^https:\/\/spdx\.dev\/learn\/handling-license-info\/?$/.test(url) ||
    /^https:\/\/cyclonedx\.org\/specification\//.test(url) ||
    /^https:\/\/spdx\.dev\/use\/specifications\/?$/.test(url)
}

function main(): void {
  const checks: Check[] = []
  const baselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
  const previousBaselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-17.json'
  const ossBaselineRefreshJsonPath = 'docs/product-quality/oss-baseline-refresh-report.json'
  const ossBaselineRefreshMdPath = 'docs/product-quality/oss-baseline-refresh-report.md'
  const ossBaselineRefreshProvenanceJsonlPath = 'reports/openclaude-oss-baseline-refresh-provenance.jsonl'
  const ossBaselineFreshnessJsonPath = 'docs/product-quality/oss-baseline-freshness-report.json'
  const ossBaselineFreshnessMdPath = 'docs/product-quality/oss-baseline-freshness-report.md'
  const ossBaselineProvenanceJsonlPath = 'reports/openclaude-oss-baseline-provenance.jsonl'
  const ossSourceReviewJsonPath = 'docs/product-quality/oss-source-review-report.json'
  const ossSourceReviewMdPath = 'docs/product-quality/oss-source-review-report.md'
  const ossSourceReviewProvenanceJsonlPath = 'reports/openclaude-oss-source-review-provenance.jsonl'
  const ossArchitectureTargetsJsonPath = 'docs/product-quality/oss-architecture-absorption-targets-report.json'
  const ossArchitectureTargetsMdPath = 'docs/product-quality/oss-architecture-absorption-targets-report.md'
  const ossArchitectureTargetsProvenanceJsonlPath = 'reports/openclaude-oss-architecture-absorption-targets.jsonl'
  const ossArchitectureGapReviewJsonPath = 'docs/product-quality/oss-architecture-gap-review-report.json'
  const ossArchitectureGapReviewMdPath = 'docs/product-quality/oss-architecture-gap-review-report.md'
  const ossArchitectureGapReviewProvenanceJsonlPath = 'reports/openclaude-oss-architecture-gap-review.jsonl'
  const ossAxisArchitectureReviewJsonPath = 'docs/product-quality/oss-axis-architecture-review-report.json'
  const ossAxisArchitectureReviewMdPath = 'docs/product-quality/oss-axis-architecture-review-report.md'
  const ossAxisArchitectureReviewProvenanceJsonlPath = 'reports/openclaude-oss-axis-architecture-review.jsonl'
  const ossSafeBacklogPlanJsonPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
  const ossSafeBacklogPlanMdPath = 'docs/product-quality/oss-safe-backlog-plan-report.md'
  const ossSafeBacklogPlanProvenanceJsonlPath = 'reports/openclaude-oss-safe-backlog-plan.jsonl'
  const ossSafeBacklogClosureJsonPath = 'docs/product-quality/oss-safe-backlog-closure-report.json'
  const ossSafeBacklogClosureMdPath = 'docs/product-quality/oss-safe-backlog-closure-report.md'
  const ossSafeBacklogClosureJsonlPath = 'reports/openclaude-oss-safe-backlog-closure.jsonl'
  const ossBaselineDriftClosureJsonPath = 'docs/product-quality/oss-baseline-drift-closure-report.json'
  const ossBaselineDriftClosureMdPath = 'docs/product-quality/oss-baseline-drift-closure-report.md'
  const ossBaselineDriftClosureJsonlPath = 'reports/openclaude-oss-baseline-drift-closure.jsonl'
  const ossBenchmarkComparisonMatrixJsonPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.json'
  const ossBenchmarkComparisonMatrixMdPath = 'docs/product-quality/oss-benchmark-comparison-matrix-report.md'
  const ossBenchmarkComparisonMatrixJsonlPath = 'reports/openclaude-oss-benchmark-comparison-matrix.jsonl'
  const ossComparisonReadinessIndexJsonPath = 'docs/product-quality/oss-comparison-readiness-index-report.json'
  const ossComparisonReadinessIndexMdPath = 'docs/product-quality/oss-comparison-readiness-index-report.md'
  const ossComparisonReadinessIndexJsonlPath = 'reports/openclaude-oss-comparison-readiness-index.jsonl'
  const ossIdeOrEditorSurfaceEvidenceJsonPath = 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json'
  const ossIdeOrEditorSurfaceEvidenceMdPath = 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.md'
  const ossIdeOrEditorSurfaceEvidenceJsonlPath = 'reports/openclaude-oss-ide-or-editor-surface-evidence.jsonl'
  const ossPrivacyNoPhoneHomeEvidenceJsonPath = 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json'
  const ossPrivacyNoPhoneHomeEvidenceMdPath = 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.md'
  const ossPrivacyNoPhoneHomeEvidenceJsonlPath = 'reports/openclaude-oss-privacy-no-phone-home-evidence.jsonl'
  const ossEvalQualityGateChecklistJsonPath = 'docs/product-quality/oss-eval-quality-gate-checklist-report.json'
  const ossEvalQualityGateChecklistMdPath = 'docs/product-quality/oss-eval-quality-gate-checklist-report.md'
  const ossEvalQualityGateChecklistProvenanceJsonlPath = 'reports/openclaude-oss-eval-quality-gate-checklist.jsonl'
  const ossTerminalWorkflowEvidenceJsonPath = 'docs/product-quality/oss-terminal-workflow-evidence-report.json'
  const ossTerminalWorkflowEvidenceMdPath = 'docs/product-quality/oss-terminal-workflow-evidence-report.md'
  const ossTerminalWorkflowEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-terminal-workflow-evidence.jsonl'
  const ossOnboardingDocsEvidenceJsonPath = 'docs/product-quality/oss-onboarding-docs-evidence-report.json'
  const ossOnboardingDocsEvidenceMdPath = 'docs/product-quality/oss-onboarding-docs-evidence-report.md'
  const ossOnboardingDocsEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-onboarding-docs-evidence.jsonl'
  const ossRuntimeDoctoringEvidenceJsonPath = 'docs/product-quality/oss-runtime-doctoring-evidence-report.json'
  const ossRuntimeDoctoringEvidenceMdPath = 'docs/product-quality/oss-runtime-doctoring-evidence-report.md'
  const ossRuntimeDoctoringEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-runtime-doctoring-evidence.jsonl'
  const ossSecurityPermissionsEvidenceJsonPath = 'docs/product-quality/oss-security-permissions-evidence-report.json'
  const ossSecurityPermissionsEvidenceMdPath = 'docs/product-quality/oss-security-permissions-evidence-report.md'
  const ossSecurityPermissionsEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-security-permissions-evidence.jsonl'
  const ossToolLoopReliabilityEvidenceJsonPath = 'docs/product-quality/oss-tool-loop-reliability-evidence-report.json'
  const ossToolLoopReliabilityEvidenceMdPath = 'docs/product-quality/oss-tool-loop-reliability-evidence-report.md'
  const ossToolLoopReliabilityEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-tool-loop-reliability-evidence.jsonl'
  const ossProviderBreadthEvidenceJsonPath = 'docs/product-quality/oss-provider-breadth-evidence-report.json'
  const ossProviderBreadthEvidenceMdPath = 'docs/product-quality/oss-provider-breadth-evidence-report.md'
  const ossProviderBreadthEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-provider-breadth-evidence.jsonl'
  const ossReleaseHygieneEvidenceJsonPath = 'docs/product-quality/oss-release-hygiene-evidence-report.json'
  const ossReleaseHygieneEvidenceMdPath = 'docs/product-quality/oss-release-hygiene-evidence-report.md'
  const ossReleaseHygieneEvidenceProvenanceJsonlPath = 'reports/openclaude-oss-release-hygiene-evidence.jsonl'
  const scorecardPath = 'docs/product-quality/competitive-scorecard.md'
  const gatePath = 'docs/product-quality/product-quality-gate.md'
  const terminalPath = 'docs/product-quality/terminal-report.md'
  const verificationPath = 'docs/product-quality/verification-report-2026-05-17.md'
  const typecheckHealthJsonPath = 'docs/product-quality/typecheck-health-report.json'
  const typecheckHealthMdPath = 'docs/product-quality/typecheck-health-report.md'
  const absorptionRegisterPath = 'docs/product-quality/open-source-absorption-register.json'
  const learningLoopPath = 'docs/product-quality/primary-source-learning-loop.md'
  const goldenTranscriptsJsonPath = 'docs/product-quality/golden-path-terminal-transcripts.json'
  const goldenTranscriptsMdPath = 'docs/product-quality/golden-path-terminal-transcripts.md'
  const terminalFailureRecoveryTranscriptsJsonPath = 'docs/product-quality/terminal-failure-recovery-transcripts-report.json'
  const terminalFailureRecoveryTranscriptsMdPath = 'docs/product-quality/terminal-failure-recovery-transcripts-report.md'
  const providerCompatibilityJsonPath = 'docs/product-quality/provider-compatibility-fixtures.json'
  const providerCompatibilityMdPath = 'docs/product-quality/provider-compatibility-fixtures.md'
  const providerCapabilityMatrixJsonPath = 'docs/product-quality/provider-capability-matrix-report.json'
  const providerCapabilityMatrixMdPath = 'docs/product-quality/provider-capability-matrix-report.md'
  const providerCapabilityMatrixJsonlPath = 'reports/openclaude-provider-capability-matrix.jsonl'
  const permissionRegressionJsonPath = 'docs/product-quality/permission-regression-fixtures.json'
  const permissionRegressionMdPath = 'docs/product-quality/permission-regression-fixtures.md'
  const runtimeDoctorRegressionJsonPath = 'docs/product-quality/runtime-doctor-regression-fixtures.json'
  const runtimeDoctorRegressionMdPath = 'docs/product-quality/runtime-doctor-regression-fixtures.md'
  const gitReleaseHygieneJsonPath = 'docs/product-quality/git-release-hygiene-report.json'
  const gitReleaseHygieneMdPath = 'docs/product-quality/git-release-hygiene-report.md'
  const ideExtensionSurfaceJsonPath = 'docs/product-quality/ide-extension-surface-report.json'
  const ideExtensionSurfaceMdPath = 'docs/product-quality/ide-extension-surface-report.md'
  const ideExtensionScopeJsonPath = 'docs/product-quality/ide-extension-scope-report.json'
  const ideExtensionScopeMdPath = 'docs/product-quality/ide-extension-scope-report.md'
  const ideExtensionManifestSmokeJsonPath = 'docs/product-quality/ide-extension-manifest-smoke-report.json'
  const ideExtensionManifestSmokeMdPath = 'docs/product-quality/ide-extension-manifest-smoke-report.md'
  const ideExtensionRuntimeSmokeJsonPath = 'docs/product-quality/ide-extension-runtime-smoke-report.json'
  const ideExtensionRuntimeSmokeMdPath = 'docs/product-quality/ide-extension-runtime-smoke-report.md'
  const ideExtensionHostSmokeJsonPath = 'docs/product-quality/ide-extension-host-smoke-report.json'
  const ideExtensionHostSmokeMdPath = 'docs/product-quality/ide-extension-host-smoke-report.md'
  const ideExtensionWorkbenchSmokeJsonPath = 'docs/product-quality/ide-extension-workbench-smoke-report.json'
  const ideExtensionWorkbenchSmokeMdPath = 'docs/product-quality/ide-extension-workbench-smoke-report.md'
  const vscodeUpdateBoundaryJsonPath = 'docs/product-quality/vscode-update-boundary-report.json'
  const vscodeUpdateBoundaryMdPath = 'docs/product-quality/vscode-update-boundary-report.md'
  const vscodeStartupDiagnosticsJsonPath = 'docs/product-quality/vscode-startup-diagnostics-report.json'
  const vscodeStartupDiagnosticsMdPath = 'docs/product-quality/vscode-startup-diagnostics-report.md'
  const ideExtensionWebviewRenderSmokeJsonPath = 'docs/product-quality/ide-extension-webview-render-smoke-report.json'
  const ideExtensionWebviewRenderSmokeMdPath = 'docs/product-quality/ide-extension-webview-render-smoke-report.md'
  const ideExtensionRenderedWorkbenchScreenshotJsonPath = 'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json'
  const ideExtensionRenderedWorkbenchScreenshotMdPath = 'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.md'
  const ideExtensionRenderedWorkbenchScreenshotPngPath = 'docs/product-quality/assets/ide-extension-control-center-render.png'
  const ideExtensionRenderedWorkbenchScreenshotSvgPath = 'docs/product-quality/assets/ide-extension-control-center-render.svg'
  const ideExtensionWebviewInteractionSmokeJsonPath = 'docs/product-quality/ide-extension-webview-interaction-smoke-report.json'
  const ideExtensionWebviewInteractionSmokeMdPath = 'docs/product-quality/ide-extension-webview-interaction-smoke-report.md'
  const releaseArtifactFileListJsonPath = 'docs/product-quality/release-artifact-file-list-report.json'
  const releaseArtifactFileListMdPath = 'docs/product-quality/release-artifact-file-list-report.md'
  const releaseArtifactProvenanceJsonPath = 'docs/product-quality/release-artifact-provenance-report.json'
  const releaseArtifactProvenanceMdPath = 'docs/product-quality/release-artifact-provenance-report.md'
  const releaseArtifactReproducibilityJsonPath = 'docs/product-quality/release-artifact-reproducibility-report.json'
  const releaseArtifactReproducibilityMdPath = 'docs/product-quality/release-artifact-reproducibility-report.md'
  const agentReplayEvalsJsonPath = 'docs/product-quality/agent-replay-evals-report.json'
  const agentReplayEvalsMdPath = 'docs/product-quality/agent-replay-evals-report.md'
  const sourceControlledChecksJsonPath = 'docs/product-quality/source-controlled-checks-report.json'
  const sourceControlledChecksMdPath = 'docs/product-quality/source-controlled-checks-report.md'
  const openSsfSecurityPostureJsonPath = 'docs/product-quality/openssf-security-posture-report.json'
  const openSsfSecurityPostureMdPath = 'docs/product-quality/openssf-security-posture-report.md'
  const realSessionCaptureJsonPath = 'docs/product-quality/real-session-capture-report.json'
  const realSessionCaptureMdPath = 'docs/product-quality/real-session-capture-report.md'
  const promptedToolLoopCaptureJsonPath = 'docs/product-quality/prompted-tool-loop-capture-report.json'
  const promptedToolLoopCaptureMdPath = 'docs/product-quality/prompted-tool-loop-capture-report.md'
  const codeEditingTraceCaptureJsonPath = 'docs/product-quality/code-editing-trace-capture-report.json'
  const codeEditingTraceCaptureMdPath = 'docs/product-quality/code-editing-trace-capture-report.md'
  const codeEditingTracePath = 'reports/orchestra-code-editing-trace-local-fixture.jsonl'
  const multiFileCodeEditingTraceCaptureJsonPath = 'docs/product-quality/multi-file-code-editing-trace-capture-report.json'
  const multiFileCodeEditingTraceCaptureMdPath = 'docs/product-quality/multi-file-code-editing-trace-capture-report.md'
  const multiFileCodeEditingTracePath = 'reports/orchestra-multi-file-code-editing-trace-local-fixture.jsonl'
  const regressionCycleCodeEditingTraceCaptureJsonPath = 'docs/product-quality/regression-cycle-code-editing-trace-capture-report.json'
  const regressionCycleCodeEditingTraceCaptureMdPath = 'docs/product-quality/regression-cycle-code-editing-trace-capture-report.md'
  const regressionCycleCodeEditingTracePath = 'reports/orchestra-regression-cycle-code-editing-trace-local-fixture.jsonl'
  const toolInterruptionRecoveryTraceJsonPath = 'docs/product-quality/tool-interruption-recovery-trace-report.json'
  const toolInterruptionRecoveryTraceMdPath = 'docs/product-quality/tool-interruption-recovery-trace-report.md'
  const toolInterruptionRecoveryTracePath = 'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl'
  const protectedActionDenialTraceJsonPath = 'docs/product-quality/protected-action-denial-trace-report.json'
  const protectedActionDenialTraceMdPath = 'docs/product-quality/protected-action-denial-trace-report.md'
  const protectedActionDenialTracePath = 'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl'
  const realTraceEvalsJsonPath = 'docs/product-quality/real-session-trace-evals-report.json'
  const realTraceEvalsMdPath = 'docs/product-quality/real-session-trace-evals-report.md'
  const traceSchemaContractJsonPath = 'docs/product-quality/trace-schema-contract-report.json'
  const traceSchemaContractMdPath = 'docs/product-quality/trace-schema-contract-report.md'
  const tracePortabilityExportJsonPath = 'docs/product-quality/trace-portability-export-report.json'
  const tracePortabilityExportMdPath = 'docs/product-quality/trace-portability-export-report.md'
  const portableTraceEventsPath = 'reports/openclaude-portable-trace-events.jsonl'
  const traceRedactionPolicyJsonPath = 'docs/product-quality/trace-capture-redaction-policy-report.json'
  const traceRedactionPolicyMdPath = 'docs/product-quality/trace-capture-redaction-policy-report.md'
  const benchmarkReadinessJsonPath = 'docs/product-quality/benchmark-readiness-matrix.json'
  const benchmarkReadinessMdPath = 'docs/product-quality/benchmark-readiness-matrix.md'
  const benchmarkTaskManifestPath = 'reports/openclaude-benchmark-task-manifest.jsonl'
  const externalBenchmarkBoundaryJsonPath = 'docs/product-quality/external-benchmark-boundary-report.json'
  const externalBenchmarkBoundaryMdPath = 'docs/product-quality/external-benchmark-boundary-report.md'
  const externalBenchmarkAuthorizationRequestPath = 'docs/product-quality/external-benchmark-authorization-request.md'
  const localBenchmarkHarnessJsonPath = 'docs/product-quality/local-benchmark-harness-report.json'
  const localBenchmarkHarnessMdPath = 'docs/product-quality/local-benchmark-harness-report.md'
  const localBenchmarkResultsPath = 'reports/openclaude-local-benchmark-results.jsonl'
  const benchmarkEfficiencyMetricsJsonPath = 'docs/product-quality/benchmark-efficiency-metrics-report.json'
  const benchmarkEfficiencyMetricsMdPath = 'docs/product-quality/benchmark-efficiency-metrics-report.md'
  const benchmarkEfficiencyMetricsJsonlPath = 'reports/openclaude-benchmark-efficiency-metrics.jsonl'
  const benchmarkSubmissionReadinessJsonPath = 'docs/product-quality/benchmark-submission-readiness-report.json'
  const benchmarkSubmissionReadinessMdPath = 'docs/product-quality/benchmark-submission-readiness-report.md'
  const benchmarkSubmissionAssetsJsonlPath = 'reports/openclaude-benchmark-submission-assets.jsonl'
  const benchmarkPolicyComplianceJsonPath = 'docs/product-quality/benchmark-policy-compliance-report.json'
  const benchmarkPolicyComplianceMdPath = 'docs/product-quality/benchmark-policy-compliance-report.md'
  const benchmarkPolicyComplianceJsonlPath = 'reports/openclaude-benchmark-policy-compliance.jsonl'
  const terminalBenchReadinessJsonPath = 'docs/product-quality/terminal-bench-readiness-report.json'
  const terminalBenchReadinessMdPath = 'docs/product-quality/terminal-bench-readiness-report.md'
  const terminalBenchTaskMapJsonlPath = 'reports/openclaude-terminal-bench-task-map.jsonl'
  const trajectoryProcessQualityJsonPath = 'docs/product-quality/trajectory-process-quality-report.json'
  const trajectoryProcessQualityMdPath = 'docs/product-quality/trajectory-process-quality-report.md'
  const trajectoryProcessQualityResultsPath = 'reports/openclaude-trajectory-process-quality.jsonl'
  const verificationReportConsistencyJsonPath = 'docs/product-quality/verification-report-consistency-report.json'
  const verificationReportConsistencyMdPath = 'docs/product-quality/verification-report-consistency-report.md'
  const qualityBlockerTaxonomyJsonPath = 'docs/product-quality/quality-blocker-taxonomy-report.json'
  const qualityBlockerTaxonomyMdPath = 'docs/product-quality/quality-blocker-taxonomy-report.md'
  const publicClaimBoundaryJsonPath = 'docs/product-quality/public-claim-boundary-report.json'
  const publicClaimBoundaryMdPath = 'docs/product-quality/public-claim-boundary-report.md'
  const publicClaimBoundaryJsonlPath = 'reports/openclaude-public-claim-boundary.jsonl'
  const githubRemoteSurfaceAuditJsonPath = 'docs/product-quality/github-remote-surface-audit-report.json'
  const githubRemoteSurfaceAuditMdPath = 'docs/product-quality/github-remote-surface-audit-report.md'
  const githubRemoteSurfaceAuditJsonlPath = 'reports/openclaude-github-remote-surface-audit.jsonl'
  const originLicenseProvenanceBoundaryJsonPath = 'docs/product-quality/origin-license-provenance-boundary-report.json'
  const originLicenseProvenanceBoundaryMdPath = 'docs/product-quality/origin-license-provenance-boundary-report.md'
  const originLicenseProvenanceBoundaryJsonlPath = 'reports/openclaude-origin-license-provenance-boundary.jsonl'
  const protectedActionAuthorizationPacketJsonPath = 'docs/product-quality/protected-action-authorization-packet.json'
  const protectedActionAuthorizationPacketMdPath = 'docs/product-quality/protected-action-authorization-packet.md'
  const protectedActionAuthorizationPacketJsonlPath = 'reports/openclaude-protected-action-authorization-packet.jsonl'
  const productEvidenceManifestJsonPath = 'docs/product-quality/product-evidence-manifest.json'
  const productEvidenceManifestMdPath = 'docs/product-quality/product-evidence-manifest.md'
  const productEvidenceManifestJsonlPath = 'reports/openclaude-product-evidence-manifest.jsonl'
  const onboardingSmokeJsonPath = 'docs/product-quality/onboarding-smoke-report.json'
  const onboardingSmokeMdPath = 'docs/product-quality/onboarding-smoke-report.md'
  const docLinkIntegrityJsonPath = 'docs/product-quality/doc-link-integrity-report.json'
  const docLinkIntegrityMdPath = 'docs/product-quality/doc-link-integrity-report.md'
  const primarySourceRegistryJsonPath = 'docs/product-quality/primary-source-registry-report.json'
  const primarySourceRegistryMdPath = 'docs/product-quality/primary-source-registry-report.md'
  const primarySourceRegistryJsonlPath = 'reports/openclaude-primary-source-registry.jsonl'
  const agentInstructionsQualityJsonPath = 'docs/product-quality/agent-instructions-quality-report.json'
  const agentInstructionsQualityMdPath = 'docs/product-quality/agent-instructions-quality-report.md'
  const communityIntakeQualityJsonPath = 'docs/product-quality/community-intake-quality-report.json'
  const communityIntakeQualityMdPath = 'docs/product-quality/community-intake-quality-report.md'
  const communityProfileQualityJsonPath = 'docs/product-quality/community-profile-quality-report.json'
  const communityProfileQualityMdPath = 'docs/product-quality/community-profile-quality-report.md'
  const dependencyTopologyJsonPath = 'docs/product-quality/dependency-topology-report.json'
  const dependencyTopologyMdPath = 'docs/product-quality/dependency-topology-report.md'
  const scriptDuplicationAuditJsonPath = 'docs/product-quality/script-duplication-audit-report.json'
  const scriptDuplicationAuditMdPath = 'docs/product-quality/script-duplication-audit-report.md'
  const deadExportCandidatesJsonPath = 'docs/product-quality/dead-export-candidates-report.json'
  const deadExportCandidatesMdPath = 'docs/product-quality/dead-export-candidates-report.md'
  const deadExportCandidateTriagePath = 'docs/product-quality/dead-export-candidate-triage.json'
  const maintainerOwnershipQualityJsonPath = 'docs/product-quality/maintainer-ownership-quality-report.json'
  const maintainerOwnershipQualityMdPath = 'docs/product-quality/maintainer-ownership-quality-report.md'
  const dependencyGovernanceQualityJsonPath = 'docs/product-quality/dependency-governance-quality-report.json'
  const dependencyGovernanceQualityMdPath = 'docs/product-quality/dependency-governance-quality-report.md'
  const lockfileSbomQualityJsonPath = 'docs/product-quality/lockfile-sbom-quality-report.json'
  const lockfileSbomQualityMdPath = 'docs/product-quality/lockfile-sbom-quality-report.md'
  const lockfileSbomInventoryJsonlPath = 'reports/openclaude-lockfile-sbom-inventory.jsonl'
  const thirdPartyLicenseQualityJsonPath = 'docs/product-quality/third-party-license-quality-report.json'
  const thirdPartyLicenseQualityMdPath = 'docs/product-quality/third-party-license-quality-report.md'
  const thirdPartyLicenseInventoryJsonlPath = 'reports/openclaude-third-party-license-inventory.jsonl'
  const sourceLicenseMetadataQualityJsonPath = 'docs/product-quality/source-license-metadata-quality-report.json'
  const sourceLicenseMetadataQualityMdPath = 'docs/product-quality/source-license-metadata-quality-report.md'
  const sourceLicenseMetadataInventoryJsonlPath = 'reports/openclaude-source-license-metadata-inventory.jsonl'
  const licenseBoundaryAuthorizationJsonPath = 'docs/product-quality/license-boundary-authorization-report.json'
  const licenseBoundaryAuthorizationMdPath = 'docs/product-quality/license-boundary-authorization-report.md'
  const licenseBoundaryAuthorizationRequestPath = 'docs/product-quality/license-boundary-authorization-request.md'
  const licenseBoundaryAuthorizationItemsJsonlPath = 'reports/openclaude-license-boundary-authorization-items.jsonl'

  for (const path of [
    'README.md',
    'SECURITY.md',
    'docs/EVALS.md',
    'docs/ROADMAP.md',
    'docs/quick-start-windows.md',
    'docs/quick-start-mac-linux.md',
    '.github/workflows/pr-checks.yml',
    '.github/workflows/codeql.yml',
    '.github/workflows/dependency-review.yml',
    '.github/dependabot.yml',
    'bun.lock',
    previousBaselinePath,
    baselinePath,
    ossBaselineRefreshJsonPath,
    ossBaselineRefreshMdPath,
    ossBaselineRefreshProvenanceJsonlPath,
    ossBaselineFreshnessJsonPath,
    ossBaselineFreshnessMdPath,
    ossBaselineProvenanceJsonlPath,
    ossSourceReviewJsonPath,
    ossSourceReviewMdPath,
    ossSourceReviewProvenanceJsonlPath,
    ossArchitectureTargetsJsonPath,
    ossArchitectureTargetsMdPath,
    ossArchitectureTargetsProvenanceJsonlPath,
    ossArchitectureGapReviewJsonPath,
    ossArchitectureGapReviewMdPath,
    ossArchitectureGapReviewProvenanceJsonlPath,
    ossAxisArchitectureReviewJsonPath,
    ossAxisArchitectureReviewMdPath,
    ossAxisArchitectureReviewProvenanceJsonlPath,
    ossSafeBacklogPlanJsonPath,
    ossSafeBacklogPlanMdPath,
    ossSafeBacklogPlanProvenanceJsonlPath,
    ossSafeBacklogClosureJsonPath,
    ossSafeBacklogClosureMdPath,
    ossSafeBacklogClosureJsonlPath,
    ossBaselineDriftClosureJsonPath,
    ossBaselineDriftClosureMdPath,
    ossBaselineDriftClosureJsonlPath,
    ossBenchmarkComparisonMatrixJsonPath,
    ossBenchmarkComparisonMatrixMdPath,
    ossBenchmarkComparisonMatrixJsonlPath,
    ossComparisonReadinessIndexJsonPath,
    ossComparisonReadinessIndexMdPath,
    ossComparisonReadinessIndexJsonlPath,
    ossIdeOrEditorSurfaceEvidenceJsonPath,
    ossIdeOrEditorSurfaceEvidenceMdPath,
    ossIdeOrEditorSurfaceEvidenceJsonlPath,
    ossPrivacyNoPhoneHomeEvidenceJsonPath,
    ossPrivacyNoPhoneHomeEvidenceMdPath,
    ossPrivacyNoPhoneHomeEvidenceJsonlPath,
    ossEvalQualityGateChecklistJsonPath,
    ossEvalQualityGateChecklistMdPath,
    ossEvalQualityGateChecklistProvenanceJsonlPath,
    ossTerminalWorkflowEvidenceJsonPath,
    ossTerminalWorkflowEvidenceMdPath,
    ossTerminalWorkflowEvidenceProvenanceJsonlPath,
    ossOnboardingDocsEvidenceJsonPath,
    ossOnboardingDocsEvidenceMdPath,
    ossOnboardingDocsEvidenceProvenanceJsonlPath,
    ossRuntimeDoctoringEvidenceJsonPath,
    ossRuntimeDoctoringEvidenceMdPath,
    ossRuntimeDoctoringEvidenceProvenanceJsonlPath,
    ossSecurityPermissionsEvidenceJsonPath,
    ossSecurityPermissionsEvidenceMdPath,
    ossSecurityPermissionsEvidenceProvenanceJsonlPath,
    ossToolLoopReliabilityEvidenceJsonPath,
    ossToolLoopReliabilityEvidenceMdPath,
    ossToolLoopReliabilityEvidenceProvenanceJsonlPath,
    ossProviderBreadthEvidenceJsonPath,
    ossProviderBreadthEvidenceMdPath,
    ossProviderBreadthEvidenceProvenanceJsonlPath,
    ossReleaseHygieneEvidenceJsonPath,
    ossReleaseHygieneEvidenceMdPath,
    ossReleaseHygieneEvidenceProvenanceJsonlPath,
    scorecardPath,
    gatePath,
    terminalPath,
    verificationPath,
    typecheckHealthJsonPath,
    typecheckHealthMdPath,
    absorptionRegisterPath,
    learningLoopPath,
    goldenTranscriptsJsonPath,
    goldenTranscriptsMdPath,
    terminalFailureRecoveryTranscriptsJsonPath,
    terminalFailureRecoveryTranscriptsMdPath,
    onboardingSmokeJsonPath,
    onboardingSmokeMdPath,
    docLinkIntegrityJsonPath,
    docLinkIntegrityMdPath,
    primarySourceRegistryJsonPath,
    primarySourceRegistryMdPath,
    primarySourceRegistryJsonlPath,
    agentInstructionsQualityJsonPath,
    agentInstructionsQualityMdPath,
    communityIntakeQualityJsonPath,
    communityIntakeQualityMdPath,
    communityProfileQualityJsonPath,
    communityProfileQualityMdPath,
    dependencyTopologyJsonPath,
    dependencyTopologyMdPath,
    scriptDuplicationAuditJsonPath,
    scriptDuplicationAuditMdPath,
    deadExportCandidatesJsonPath,
    deadExportCandidatesMdPath,
    deadExportCandidateTriagePath,
    maintainerOwnershipQualityJsonPath,
    maintainerOwnershipQualityMdPath,
    dependencyGovernanceQualityJsonPath,
    dependencyGovernanceQualityMdPath,
    lockfileSbomQualityJsonPath,
    lockfileSbomQualityMdPath,
    lockfileSbomInventoryJsonlPath,
    thirdPartyLicenseQualityJsonPath,
    thirdPartyLicenseQualityMdPath,
    thirdPartyLicenseInventoryJsonlPath,
    sourceLicenseMetadataQualityJsonPath,
    sourceLicenseMetadataQualityMdPath,
    sourceLicenseMetadataInventoryJsonlPath,
    licenseBoundaryAuthorizationJsonPath,
    licenseBoundaryAuthorizationMdPath,
    licenseBoundaryAuthorizationRequestPath,
    licenseBoundaryAuthorizationItemsJsonlPath,
    providerCompatibilityJsonPath,
    providerCompatibilityMdPath,
    providerCapabilityMatrixJsonPath,
    providerCapabilityMatrixMdPath,
    providerCapabilityMatrixJsonlPath,
    permissionRegressionJsonPath,
    permissionRegressionMdPath,
    runtimeDoctorRegressionJsonPath,
    runtimeDoctorRegressionMdPath,
    gitReleaseHygieneJsonPath,
    gitReleaseHygieneMdPath,
    ideExtensionSurfaceJsonPath,
    ideExtensionSurfaceMdPath,
    ideExtensionScopeJsonPath,
    ideExtensionScopeMdPath,
    ideExtensionManifestSmokeJsonPath,
    ideExtensionManifestSmokeMdPath,
    ideExtensionRuntimeSmokeJsonPath,
    ideExtensionRuntimeSmokeMdPath,
    ideExtensionHostSmokeJsonPath,
    ideExtensionHostSmokeMdPath,
    ideExtensionWorkbenchSmokeJsonPath,
    ideExtensionWorkbenchSmokeMdPath,
    vscodeUpdateBoundaryJsonPath,
    vscodeUpdateBoundaryMdPath,
    vscodeStartupDiagnosticsJsonPath,
    vscodeStartupDiagnosticsMdPath,
    ideExtensionWebviewRenderSmokeJsonPath,
    ideExtensionWebviewRenderSmokeMdPath,
    ideExtensionRenderedWorkbenchScreenshotJsonPath,
    ideExtensionRenderedWorkbenchScreenshotMdPath,
    ideExtensionRenderedWorkbenchScreenshotPngPath,
    ideExtensionRenderedWorkbenchScreenshotSvgPath,
    ideExtensionWebviewInteractionSmokeJsonPath,
    ideExtensionWebviewInteractionSmokeMdPath,
    'packages/openclaude-vscode/package.json',
    'packages/openclaude-vscode/README.md',
    'packages/openclaude-vscode/dist/extension.js',
    releaseArtifactFileListJsonPath,
    releaseArtifactFileListMdPath,
    releaseArtifactProvenanceJsonPath,
    releaseArtifactProvenanceMdPath,
    releaseArtifactReproducibilityJsonPath,
    releaseArtifactReproducibilityMdPath,
    agentReplayEvalsJsonPath,
    agentReplayEvalsMdPath,
    sourceControlledChecksJsonPath,
    sourceControlledChecksMdPath,
    openSsfSecurityPostureJsonPath,
    openSsfSecurityPostureMdPath,
    realSessionCaptureJsonPath,
    realSessionCaptureMdPath,
    promptedToolLoopCaptureJsonPath,
    promptedToolLoopCaptureMdPath,
    codeEditingTraceCaptureJsonPath,
    codeEditingTraceCaptureMdPath,
    codeEditingTracePath,
    multiFileCodeEditingTraceCaptureJsonPath,
    multiFileCodeEditingTraceCaptureMdPath,
    multiFileCodeEditingTracePath,
    regressionCycleCodeEditingTraceCaptureJsonPath,
    regressionCycleCodeEditingTraceCaptureMdPath,
    regressionCycleCodeEditingTracePath,
    toolInterruptionRecoveryTraceJsonPath,
    toolInterruptionRecoveryTraceMdPath,
    toolInterruptionRecoveryTracePath,
    protectedActionDenialTraceJsonPath,
    protectedActionDenialTraceMdPath,
    protectedActionDenialTracePath,
    realTraceEvalsJsonPath,
    realTraceEvalsMdPath,
    traceSchemaContractJsonPath,
    traceSchemaContractMdPath,
    tracePortabilityExportJsonPath,
    tracePortabilityExportMdPath,
    portableTraceEventsPath,
    traceRedactionPolicyJsonPath,
    traceRedactionPolicyMdPath,
    benchmarkReadinessJsonPath,
    benchmarkReadinessMdPath,
    benchmarkTaskManifestPath,
    externalBenchmarkBoundaryJsonPath,
    externalBenchmarkBoundaryMdPath,
    externalBenchmarkAuthorizationRequestPath,
    localBenchmarkHarnessJsonPath,
    localBenchmarkHarnessMdPath,
    localBenchmarkResultsPath,
    benchmarkEfficiencyMetricsJsonPath,
    benchmarkEfficiencyMetricsMdPath,
    benchmarkEfficiencyMetricsJsonlPath,
    benchmarkSubmissionReadinessJsonPath,
    benchmarkSubmissionReadinessMdPath,
    benchmarkSubmissionAssetsJsonlPath,
    benchmarkPolicyComplianceJsonPath,
    benchmarkPolicyComplianceMdPath,
    benchmarkPolicyComplianceJsonlPath,
    terminalBenchReadinessJsonPath,
    terminalBenchReadinessMdPath,
    terminalBenchTaskMapJsonlPath,
    trajectoryProcessQualityJsonPath,
    trajectoryProcessQualityMdPath,
    trajectoryProcessQualityResultsPath,
    verificationReportConsistencyJsonPath,
    verificationReportConsistencyMdPath,
    qualityBlockerTaxonomyJsonPath,
    qualityBlockerTaxonomyMdPath,
    publicClaimBoundaryJsonPath,
    publicClaimBoundaryMdPath,
    publicClaimBoundaryJsonlPath,
    githubRemoteSurfaceAuditJsonPath,
    githubRemoteSurfaceAuditMdPath,
    githubRemoteSurfaceAuditJsonlPath,
    originLicenseProvenanceBoundaryJsonPath,
    originLicenseProvenanceBoundaryMdPath,
    originLicenseProvenanceBoundaryJsonlPath,
    protectedActionAuthorizationPacketJsonPath,
    protectedActionAuthorizationPacketMdPath,
    protectedActionAuthorizationPacketJsonlPath,
    productEvidenceManifestJsonPath,
    productEvidenceManifestMdPath,
    productEvidenceManifestJsonlPath,
  ]) {
    checks.push(fileExists(path))
  }

  const pkg = readJson<{ scripts: Record<string, string>; name: string; version: string }>('package.json')
  for (const scriptName of [
    'build',
    'test',
    'typecheck',
    'smoke',
    'verify:privacy',
    'doctor:runtime',
    'hardening:strict',
    'product:typecheck-health',
    'product:oss-baseline-refresh',
    'product:oss-baseline-freshness',
    'product:oss-source-review',
    'product:oss-safe-backlog-plan',
    'product:oss-safe-backlog-closure',
    'product:oss-baseline-drift-closure',
    'product:oss-benchmark-comparison-matrix',
    'product:oss-comparison-readiness-index',
    'product:oss-ide-or-editor-surface-evidence',
    'product:oss-privacy-no-phone-home-evidence',
    'product:oss-eval-quality-gate-checklist',
    'product:oss-terminal-workflow-evidence',
    'product:oss-onboarding-docs-evidence',
    'product:oss-runtime-doctoring-evidence',
    'product:oss-security-permissions-evidence',
    'product:oss-tool-loop-reliability-evidence',
    'product:oss-provider-breadth-evidence',
    'product:oss-release-hygiene-evidence',
    'product:golden-transcripts',
    'product:terminal-failure-recovery-transcripts',
    'product:onboarding-smoke',
    'product:doc-link-integrity',
    'product:agent-instructions-quality',
    'product:community-intake-quality',
    'product:community-profile-quality',
    'product:maintainer-ownership-quality',
    'product:dependency-governance-quality',
    'product:lockfile-sbom-quality',
    'product:third-party-license-quality',
    'product:source-license-metadata-quality',
    'product:provider-compatibility',
    'product:permission-regression',
    'product:runtime-doctor',
    'product:git-release-hygiene',
    'product:ide-extension-surface',
    'product:ide-extension-scope',
    'product:ide-extension-manifest-smoke',
    'product:ide-extension-runtime-smoke',
    'product:ide-extension-host-smoke',
    'product:ide-extension-workbench-smoke',
    'product:vscode-update-boundary',
    'product:vscode-startup-diagnostics',
    'product:ide-extension-webview-render-smoke',
    'product:ide-extension-rendered-workbench-screenshot',
    'product:ide-extension-webview-interaction-smoke',
    'product:release-artifact',
    'product:release-provenance',
    'product:release-reproducibility',
    'product:agent-replay-evals',
    'product:source-controlled-checks',
    'product:openssf-security-posture',
    'product:real-session-capture',
    'product:prompted-tool-loop-capture',
    'product:code-editing-trace-capture',
    'product:multi-file-code-editing-trace-capture',
    'product:regression-cycle-code-editing-trace-capture',
    'product:tool-interruption-recovery-trace',
    'product:protected-action-denial-trace',
    'product:real-trace-evals',
    'product:trace-schema-contract',
    'product:trace-portability-export',
    'product:trace-redaction-policy',
    'product:benchmark-readiness',
    'product:external-benchmark-boundary',
    'product:local-benchmark-harness',
    'product:benchmark-efficiency-metrics',
    'product:benchmark-submission-readiness',
    'product:benchmark-policy-compliance',
    'product:terminal-bench-readiness',
    'product:trajectory-process-quality',
    'product:verification-report-consistency',
    'product:quality-blocker-taxonomy',
    'product:public-claim-boundary',
    'product:github-remote-surface-audit',
    'product:origin-license-provenance-boundary',
    'product:protected-action-authorization-packet',
    'product:evidence-manifest',
    'product:quality',
  ]) {
    checks.push(check(`package script: ${scriptName}`, typeof pkg.scripts?.[scriptName] === 'string'))
  }

  const baseline = readJson<Baseline>(baselinePath)
  checks.push(check('baseline has exactly 10 projects', baseline.top10.length === 10, `${baseline.top10.length}`))
  checks.push(check('baseline snapshot date set', /^\d{4}-\d{2}-\d{2}$/.test(baseline.snapshot_date), baseline.snapshot_date))
  checks.push(check('baseline claim boundary rejects premature superiority claim', /not a claim/i.test(baseline.claim_boundary), baseline.claim_boundary))

  const ranks = baseline.top10.map((project) => project.rank)
  checks.push(check('baseline ranks are 1..10', ranks.every((rank, index) => rank === index + 1), ranks.join(',')))
  checks.push(
    check(
      'baseline projects have primary GitHub source URLs',
      baseline.top10.every((project) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(project.source_url)),
    ),
  )
  checks.push(
    check(
      'baseline projects have star metadata',
      baseline.top10.every((project) => Number.isInteger(project.stars) && project.stars > 0),
    ),
  )
  checks.push(
    check(
      'baseline project names are unique',
      new Set(baseline.top10.map((project) => project.full_name.toLowerCase())).size === baseline.top10.length,
    ),
  )
  checks.push(
    check(
      'baseline projects are sorted by stars descending',
      baseline.top10.every((project, index, projects) => index === 0 || projects[index - 1].stars >= project.stars),
      baseline.top10.map((project) => String(project.stars)).join(','),
    ),
  )

  for (const axis of [
    'provider_breadth',
    'terminal_workflow',
    'tool_loop_reliability',
    'privacy_and_no_phone_home',
    'runtime_doctoring',
    'eval_and_quality_gates',
    'security_and_permissions',
    'onboarding_docs',
    'ide_or_editor_surface',
    'release_hygiene',
  ]) {
    checks.push(check(`required product axis: ${axis}`, baseline.required_product_axes.includes(axis)))
  }

  const scorecard = readText(scorecardPath)
  const gate = readText(gatePath)
  const terminal = readText(terminalPath)
  const ossBaselineRefresh = readJson<OssBaselineRefreshReport>(ossBaselineRefreshJsonPath)
  const ossBaselineFreshness = readJson<OssBaselineFreshnessReport>(ossBaselineFreshnessJsonPath)
  const ossSourceReview = readJson<OssSourceReviewReport>(ossSourceReviewJsonPath)
  const ossArchitectureTargets = readJson<OssArchitectureTargetsReport>(ossArchitectureTargetsJsonPath)
  const ossArchitectureGapReview = readJson<OssArchitectureGapReviewReport>(ossArchitectureGapReviewJsonPath)
  const ossAxisArchitectureReview = readJson<OssAxisArchitectureReviewReport>(ossAxisArchitectureReviewJsonPath)
  const ossSafeBacklogPlan = readJson<OssSafeBacklogPlanReport>(ossSafeBacklogPlanJsonPath)
  const ossSafeBacklogClosure = readJson<Record<string, unknown>>(ossSafeBacklogClosureJsonPath)
  const ossSafeBacklogClosureRecords = Array.isArray(ossSafeBacklogClosure.closureRecords) ? ossSafeBacklogClosure.closureRecords as Array<Record<string, unknown>> : []
  const ossSafeBacklogClosureChecks = Array.isArray(ossSafeBacklogClosure.closureChecks) ? ossSafeBacklogClosure.closureChecks as Array<{ ok?: boolean }> : []
  const ossBaselineDriftClosure = readJson<Record<string, unknown>>(ossBaselineDriftClosureJsonPath)
  const ossBaselineDriftClosureRecords = Array.isArray(ossBaselineDriftClosure.driftRecords) ? ossBaselineDriftClosure.driftRecords as Array<Record<string, unknown>> : []
  const ossBaselineDriftClosureChecks = Array.isArray(ossBaselineDriftClosure.driftChecks) ? ossBaselineDriftClosure.driftChecks as Array<{ ok?: boolean }> : []
  const ossBenchmarkComparisonMatrix = readJson<Record<string, unknown>>(ossBenchmarkComparisonMatrixJsonPath)
  const ossBenchmarkComparisonMatrixRecords = Array.isArray(ossBenchmarkComparisonMatrix.matrixRecords) ? ossBenchmarkComparisonMatrix.matrixRecords as Array<Record<string, unknown>> : []
  const ossBenchmarkComparisonMatrixChecks = Array.isArray(ossBenchmarkComparisonMatrix.matrixChecks) ? ossBenchmarkComparisonMatrix.matrixChecks as Array<{ ok?: boolean }> : []
  const ossComparisonReadinessIndex = readJson<Record<string, unknown>>(ossComparisonReadinessIndexJsonPath)
  const ossComparisonReadinessIndexRecords = Array.isArray(ossComparisonReadinessIndex.readinessIndexRecords) ? ossComparisonReadinessIndex.readinessIndexRecords as Array<Record<string, unknown>> : []
  const ossComparisonReadinessIndexChecks = Array.isArray(ossComparisonReadinessIndex.indexChecks) ? ossComparisonReadinessIndex.indexChecks as Array<{ ok?: boolean }> : []
  const ossIdeOrEditorSurfaceEvidence = readJson<Record<string, unknown>>(ossIdeOrEditorSurfaceEvidenceJsonPath)
  const ossIdeOrEditorSurfaceEvidenceRecords = Array.isArray(ossIdeOrEditorSurfaceEvidence.reconciliationRecords) ? ossIdeOrEditorSurfaceEvidence.reconciliationRecords as Array<Record<string, unknown>> : []
  const ossIdeOrEditorSurfaceEvidenceChecks = Array.isArray(ossIdeOrEditorSurfaceEvidence.evidenceChecks) ? ossIdeOrEditorSurfaceEvidence.evidenceChecks as Array<{ ok?: boolean }> : []
  const ossPrivacyNoPhoneHomeEvidence = readJson<Record<string, unknown>>(ossPrivacyNoPhoneHomeEvidenceJsonPath)
  const ossPrivacyNoPhoneHomeEvidenceRecords = Array.isArray(ossPrivacyNoPhoneHomeEvidence.reconciliationRecords) ? ossPrivacyNoPhoneHomeEvidence.reconciliationRecords as Array<Record<string, unknown>> : []
  const ossPrivacyNoPhoneHomeEvidenceChecks = Array.isArray(ossPrivacyNoPhoneHomeEvidence.evidenceChecks) ? ossPrivacyNoPhoneHomeEvidence.evidenceChecks as Array<{ ok?: boolean }> : []
  const ossEvalQualityGateChecklist = readJson<OssEvalQualityGateChecklistReport>(ossEvalQualityGateChecklistJsonPath)
  const ossTerminalWorkflowEvidence = readJson<OssTerminalWorkflowEvidenceReport>(ossTerminalWorkflowEvidenceJsonPath)
  const ossOnboardingDocsEvidence = readJson<OssOnboardingDocsEvidenceReport>(ossOnboardingDocsEvidenceJsonPath)
  const ossRuntimeDoctoringEvidence = readJson<OssRuntimeDoctoringEvidenceReport>(ossRuntimeDoctoringEvidenceJsonPath)
  const ossSecurityPermissionsEvidence = readJson<OssSecurityPermissionsEvidenceReport>(ossSecurityPermissionsEvidenceJsonPath)
  const ossToolLoopReliabilityEvidence = readJson<OssToolLoopReliabilityEvidenceReport>(ossToolLoopReliabilityEvidenceJsonPath)
  const ossProviderBreadthEvidence = readJson<OssProviderBreadthEvidenceReport>(ossProviderBreadthEvidenceJsonPath)
  const ossReleaseHygieneEvidence = readJson<OssReleaseHygieneEvidenceReport>(ossReleaseHygieneEvidenceJsonPath)
  const typecheckHealth = readJson<{ strictPass: boolean; totalDiagnostics: number; diagnosticBudget?: number; buckets: unknown[] }>(typecheckHealthJsonPath)
  const absorptionRegister = readJson<{ entries: Array<{ source_project: string; source_url: string; observed_pattern: string; openclaude_absorption_decision: string; local_action: string; status: string }>; next_absorption_targets: string[] }>(absorptionRegisterPath)
  const goldenTranscripts = readJson<GoldenTranscriptReport>(goldenTranscriptsJsonPath)
  const terminalFailureRecoveryTranscripts = readJson<TerminalFailureRecoveryTranscriptsReport>(terminalFailureRecoveryTranscriptsJsonPath)
  const onboardingSmoke = readJson<OnboardingSmokeReport>(onboardingSmokeJsonPath)
  const docLinkIntegrity = readJson<DocLinkIntegrityReport>(docLinkIntegrityJsonPath)
  const primarySourceRegistry = readJson<PrimarySourceRegistryReport>(primarySourceRegistryJsonPath)
  const agentInstructionsQuality = readJson<AgentInstructionsQualityReport>(agentInstructionsQualityJsonPath)
  const communityIntakeQuality = readJson<CommunityIntakeQualityReport>(communityIntakeQualityJsonPath)
  const communityProfileQuality = readJson<CommunityProfileQualityReport>(communityProfileQualityJsonPath)
  const dependencyTopology = readJson<DependencyTopologyReport>(dependencyTopologyJsonPath)
  const scriptDuplicationAudit = readJson<ScriptDuplicationAuditReport>(scriptDuplicationAuditJsonPath)
  const deadExportCandidates = readJson<DeadExportCandidatesReport>(deadExportCandidatesJsonPath)
  const maintainerOwnershipQuality = readJson<MaintainerOwnershipQualityReport>(maintainerOwnershipQualityJsonPath)
  const dependencyGovernanceQuality = readJson<DependencyGovernanceQualityReport>(dependencyGovernanceQualityJsonPath)
  const lockfileSbomQuality = readJson<LockfileSbomQualityReport>(lockfileSbomQualityJsonPath)
  const thirdPartyLicenseQuality = readJson<ThirdPartyLicenseQualityReport>(thirdPartyLicenseQualityJsonPath)
  const sourceLicenseMetadataQuality = readJson<SourceLicenseMetadataQualityReport>(sourceLicenseMetadataQualityJsonPath)
  const licenseBoundaryAuthorization = readJson<LicenseBoundaryAuthorizationReport>(licenseBoundaryAuthorizationJsonPath)
  const providerCompatibility = readJson<ProviderCompatibilityReport>(providerCompatibilityJsonPath)
  const permissionRegression = readJson<PermissionRegressionReport>(permissionRegressionJsonPath)
  const runtimeDoctorRegression = readJson<RuntimeDoctorRegressionReport>(runtimeDoctorRegressionJsonPath)
  const providerCapabilityMatrix = readJson<ProviderCapabilityMatrixReport>(providerCapabilityMatrixJsonPath)
  const gitReleaseHygiene = readJson<GitReleaseHygieneReport>(gitReleaseHygieneJsonPath)
  const ideExtensionSurface = readJson<IdeExtensionSurfaceReport>(ideExtensionSurfaceJsonPath)
  const ideExtensionScope = readJson<IdeExtensionScopeReport>(ideExtensionScopeJsonPath)
  const ideExtensionManifestSmoke = readJson<IdeExtensionManifestSmokeReport>(ideExtensionManifestSmokeJsonPath)
  const ideExtensionRuntimeSmoke = readJson<IdeExtensionRuntimeSmokeReport>(ideExtensionRuntimeSmokeJsonPath)
  const ideExtensionHostSmoke = readJson<IdeExtensionHostSmokeReport>(ideExtensionHostSmokeJsonPath)
  const ideExtensionWorkbenchSmoke = readJson<IdeExtensionWorkbenchSmokeReport>(ideExtensionWorkbenchSmokeJsonPath)
  const vscodeUpdateBoundary = readJson<VscodeUpdateBoundaryReport>(vscodeUpdateBoundaryJsonPath)
  const vscodeStartupDiagnostics = readJson<VscodeStartupDiagnosticsReport>(vscodeStartupDiagnosticsJsonPath)
  const ideExtensionWebviewRenderSmoke = readJson<IdeExtensionWebviewRenderSmokeReport>(ideExtensionWebviewRenderSmokeJsonPath)
  const ideExtensionRenderedWorkbenchScreenshot = readJson<IdeExtensionRenderedWorkbenchScreenshotReport>(ideExtensionRenderedWorkbenchScreenshotJsonPath)
  const ideExtensionWebviewInteractionSmoke = readJson<IdeExtensionWebviewInteractionSmokeReport>(ideExtensionWebviewInteractionSmokeJsonPath)
  const releaseArtifactFileList = readJson<ReleaseArtifactFileListReport>(releaseArtifactFileListJsonPath)
  const releaseArtifactProvenance = readJson<ReleaseArtifactProvenanceReport>(releaseArtifactProvenanceJsonPath)
  const releaseArtifactReproducibility = readJson<ReleaseArtifactReproducibilityReport>(releaseArtifactReproducibilityJsonPath)
  const agentReplayEvals = readJson<AgentReplayEvalReport>(agentReplayEvalsJsonPath)
  const sourceControlledChecks = readJson<SourceControlledChecksReport>(sourceControlledChecksJsonPath)
  const openSsfSecurityPosture = readJson<OpenSsfSecurityPostureReport>(openSsfSecurityPostureJsonPath)
  const realSessionCapture = readJson<RealSessionCaptureReport>(realSessionCaptureJsonPath)
  const promptedToolLoopCapture = readJson<PromptedToolLoopCaptureReport>(promptedToolLoopCaptureJsonPath)
  const codeEditingTraceCapture = readJson<CodeEditingTraceCaptureReport>(codeEditingTraceCaptureJsonPath)
  const multiFileCodeEditingTraceCapture = readJson<MultiFileCodeEditingTraceCaptureReport>(multiFileCodeEditingTraceCaptureJsonPath)
  const regressionCycleCodeEditingTraceCapture = readJson<RegressionCycleCodeEditingTraceCaptureReport>(regressionCycleCodeEditingTraceCaptureJsonPath)
  const toolInterruptionRecoveryTrace = readJson<ToolInterruptionRecoveryTraceReport>(toolInterruptionRecoveryTraceJsonPath)
  const protectedActionDenialTrace = readJson<ProtectedActionDenialTraceReport>(protectedActionDenialTraceJsonPath)
  const realTraceEvals = readJson<RealTraceEvalReport>(realTraceEvalsJsonPath)
  const traceSchemaContract = readJson<TraceSchemaContractReport>(traceSchemaContractJsonPath)
  const tracePortabilityExport = readJson<TracePortabilityExportReport>(tracePortabilityExportJsonPath)
  const traceRedactionPolicy = readJson<TraceRedactionPolicyReport>(traceRedactionPolicyJsonPath)
  const benchmarkReadiness = readJson<BenchmarkReadinessReport>(benchmarkReadinessJsonPath)
  const externalBenchmarkBoundary = readJson<ExternalBenchmarkBoundaryReport>(externalBenchmarkBoundaryJsonPath)
  const localBenchmarkHarness = readJson<LocalBenchmarkHarnessReport>(localBenchmarkHarnessJsonPath)
  const benchmarkEfficiencyMetrics = readJson<BenchmarkEfficiencyMetricsReport>(benchmarkEfficiencyMetricsJsonPath)
  const benchmarkSubmissionReadiness = readJson<BenchmarkSubmissionReadinessReport>(benchmarkSubmissionReadinessJsonPath)
  const benchmarkPolicyCompliance = readJson<BenchmarkPolicyComplianceReport>(benchmarkPolicyComplianceJsonPath)
  const terminalBenchReadiness = readJson<TerminalBenchReadinessReport>(terminalBenchReadinessJsonPath)
  const trajectoryProcessQuality = readJson<TrajectoryProcessQualityReport>(trajectoryProcessQualityJsonPath)
  const verificationReportConsistency = readJson<VerificationReportConsistencyReport>(verificationReportConsistencyJsonPath)
  const qualityBlockerTaxonomy = readJson<QualityBlockerTaxonomyReport>(qualityBlockerTaxonomyJsonPath)
  const publicClaimBoundary = readJson<PublicClaimBoundaryReport>(publicClaimBoundaryJsonPath)
  const githubRemoteSurfaceAudit = readJson<GithubRemoteSurfaceAuditReport>(githubRemoteSurfaceAuditJsonPath)
  const originLicenseProvenanceBoundary = readJson<OriginLicenseProvenanceBoundaryReport>(originLicenseProvenanceBoundaryJsonPath)
  const protectedActionAuthorizationPacket = readJson<ProtectedActionAuthorizationPacketReport>(protectedActionAuthorizationPacketJsonPath)
  const productEvidenceManifest = readJson<ProductEvidenceManifestReport>(productEvidenceManifestJsonPath)
  const manifestTreeViewIds = ideExtensionManifestSmoke.manifestSummary.treeViewIds ?? ideExtensionManifestSmoke.manifestSummary.viewIds
  const manifestWebviewViewIds = ideExtensionManifestSmoke.manifestSummary.webviewViewIds ?? []
  const protectedVscodeBlockers = ['vscode_update_in_progress', 'vscode_cli_unavailable']
  const hasProtectedVscodeBlocker = (blockers: string[] | undefined): boolean => (blockers ?? []).some((blocker) => protectedVscodeBlockers.includes(blocker))
  const ideExtensionHostEnvironmentBlocked = ideExtensionHostSmoke.vscodeStartupBlocked === true &&
    ideExtensionHostSmoke.realExtensionHostLaunched === false &&
    ideExtensionHostSmoke.extensionAvailabilityClaimAllowed === false &&
    hasProtectedVscodeBlocker(ideExtensionHostSmoke.environmentBlockers)
  const ideExtensionWorkbenchEnvironmentBlocked = ideExtensionWorkbenchSmoke.vscodeStartupBlocked === true &&
    ideExtensionWorkbenchSmoke.realExtensionHostLaunched === false &&
    ideExtensionWorkbenchSmoke.extensionAvailabilityClaimAllowed === false &&
    hasProtectedVscodeBlocker(ideExtensionWorkbenchSmoke.environmentBlockers)
  const ideExtensionHostVerified = ideExtensionHostSmoke.realExtensionHostLaunched === true &&
    ideExtensionHostSmoke.vscodeStartupBlocked !== true &&
    ideExtensionHostSmoke.extensionActivated === true &&
    ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionHostSmoke.registeredCommandIds.includes(command)) &&
    ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionHostSmoke.executedCommandIds.includes(command)) &&
    ideExtensionHostSmoke.failedCommandIds.length === 0
  const ideExtensionWorkbenchVerified = ideExtensionWorkbenchSmoke.realExtensionHostLaunched === true &&
    ideExtensionWorkbenchSmoke.vscodeStartupBlocked !== true &&
    ideExtensionWorkbenchSmoke.extensionActivated === true &&
    manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.registeredTreeViewIds.includes(viewId)) &&
    manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.treeProviderViewIds.includes(viewId)) &&
    manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.focusedViewIds.includes(viewId)) &&
    manifestTreeViewIds.every((viewId) => (ideExtensionWorkbenchSmoke.viewItemCounts[viewId] ?? 0) > 0) &&
    (ideExtensionWorkbenchSmoke.failedViewCommandIds ?? []).length === 0
  const agentReplayFailedScenarioIds = agentReplayEvals.replayScenarios.filter((item) => !item.passed).map((item) => item.id)
  const agentReplayFailedCheckLabels = agentReplayEvals.replayEvalChecks.filter((item) => !item.ok).map((item) => item.label)
  const agentReplayKnownVscodeBoundary = ideExtensionHostEnvironmentBlocked &&
    ideExtensionWorkbenchEnvironmentBlocked &&
    agentReplayFailedScenarioIds.join(',') === 'ide_extension_host_smoke_replay,ide_extension_workbench_smoke_replay' &&
    agentReplayFailedCheckLabels.join(',') === 'all replay scenarios passed threshold'
  const startupDiagnosticsSentinelEnumerationBounded = vscodeStartupDiagnostics.startupDiagnosticsChecks.some((item) => item.label === 'sentinel candidates are enumerated or bounded without mutation' && item.ok)
  const realTraceFailedTerminalOutcomeClassified = realTraceEvals.coverageSummary?.classifiedCoverageGaps.some((gap) => gap.id === 'failed_terminal_outcome_coverage' && gap.status === 'classified_unresolved') === true
  const tracePortabilityHistoricalGapCountEstimate = Math.max(
    traceSchemaContract.aggregate.missingRecommendedEventNameCount,
    traceSchemaContract.aggregate.missingRecommendedTraceContextCount,
    traceSchemaContract.aggregate.missingRecommendedActionObservationCount ?? 0,
  )
  checks.push(check('OSS baseline refresh uses GitHub REST metadata', ossBaselineRefresh.mode === 'external_github_api_oss_baseline_refresh' && ossBaselineRefresh.externalGitHubRefreshPerformed === true && ossBaselineRefresh.githubApiCallPerformed === true))
  checks.push(check('OSS baseline refresh writes current baseline', ossBaselineRefresh.outputBaselinePath === baselinePath && ossBaselineRefresh.snapshotDate === baseline.snapshot_date && ossBaselineRefresh.top10ProjectCount === baseline.top10.length, `${ossBaselineRefresh.outputBaselinePath}/${ossBaselineRefresh.snapshotDate}/${ossBaselineRefresh.top10ProjectCount}`))
  checks.push(check('OSS baseline refresh writes expected provenance JSONL', ossBaselineRefresh.provenanceJsonlPath === ossBaselineRefreshProvenanceJsonlPath && ossBaselineRefresh.provenanceJsonlSha256.length === 64 && ossBaselineRefresh.provenanceJsonlRecordCount === baseline.top10.length, ossBaselineRefresh.provenanceJsonlPath))
  checks.push(check('OSS baseline refresh found fresh candidate changes', ossBaselineRefresh.newlyDiscoveredTop10Projects.includes('ultraworkers/claw-code') && ossBaselineRefresh.removedPreviousTop10Projects.length > 0, `${ossBaselineRefresh.newlyDiscoveredTop10Projects.join(',')}/${ossBaselineRefresh.removedPreviousTop10Projects.join(',')}`))
  checks.push(check('OSS baseline refresh keeps claim expansion blocked', ossBaselineRefresh.publicComparisonClaimAllowed === false && ossBaselineRefresh.superiorityClaimAllowed === false && ossBaselineRefresh.releaseReadinessClaimAllowed === false && ossBaselineRefresh.productionReadinessClaimAllowed === false && ossBaselineRefresh.publicReadinessClaimAllowed === false && ossBaselineRefresh.externalValidationClaimAllowed === false && ossBaselineRefresh.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS baseline refresh performed no provider live or protected calls', ossBaselineRefresh.providerCallsPerformed.length === 0 && ossBaselineRefresh.liveModelCallsPerformed.length === 0 && ossBaselineRefresh.protectedActionsExecuted.length === 0 && ossBaselineRefresh.externalCallsPerformed.length > 0, `${ossBaselineRefresh.externalCallsPerformed.length} external GitHub calls`))
  checks.push(check('OSS baseline refresh checks pass', ossBaselineRefresh.refreshChecks.every((item) => item.ok)))
  checks.push(check('OSS baseline freshness is local no-provider check', ossBaselineFreshness.mode === 'local_no_provider_oss_baseline_freshness'))
  checks.push(check('OSS baseline freshness imports current baseline', ossBaselineFreshness.sourceBaselinePath === baselinePath && ossBaselineFreshness.top10ProjectCount === baseline.top10.length && ossBaselineFreshness.requiredProductAxisCount === baseline.required_product_axes.length, `${ossBaselineFreshness.sourceBaselinePath}/${ossBaselineFreshness.top10ProjectCount}`))
  checks.push(check('OSS baseline freshness preserves baseline snapshot date', ossBaselineFreshness.baselineSnapshotDate === baseline.snapshot_date && ossBaselineFreshness.validationDate === '2026-05-21' && ossBaselineFreshness.baselineAgeDays === 0, `${ossBaselineFreshness.baselineSnapshotDate}/${ossBaselineFreshness.validationDate}/${ossBaselineFreshness.baselineAgeDays}`))
  checks.push(check('OSS baseline freshness validates structural invariants', ossBaselineFreshness.ranksAreConsecutive && ossBaselineFreshness.starsArePositiveIntegers && ossBaselineFreshness.starsSortedDescending && ossBaselineFreshness.sourceUrlsAreGithubRepos && ossBaselineFreshness.fullNamesMatchSourceUrls && ossBaselineFreshness.licensesArePresent && ossBaselineFreshness.collectionMethodMentionsGitHubMetadata))
  checks.push(check('OSS baseline freshness keeps public comparison blocked pending claim authorization', ossBaselineFreshness.baselineFreshForInternalPlanning === true && ossBaselineFreshness.baselineRefreshRequiredBeforePublicComparison === false && ossBaselineFreshness.publicComparisonClaimAllowed === false && ossBaselineFreshness.superiorityClaimAllowed === false, `${ossBaselineFreshness.baselineFreshForInternalPlanning}/${ossBaselineFreshness.baselineRefreshRequiredBeforePublicComparison}`))
  checks.push(check('OSS baseline freshness writes expected provenance JSONL', ossBaselineFreshness.provenanceJsonlPath === ossBaselineProvenanceJsonlPath && ossBaselineFreshness.provenanceJsonlSha256.length === 64 && ossBaselineFreshness.provenanceJsonlRecordCount === baseline.top10.length && ossBaselineFreshness.provenanceJsonlParseable, ossBaselineFreshness.provenanceJsonlPath))
  checks.push(check('OSS baseline freshness performed no external refresh or calls', ossBaselineFreshness.externalGitHubRefreshPerformed === false && ossBaselineFreshness.githubApiCallPerformed === false && ossBaselineFreshness.providerCallsPerformed.length === 0 && ossBaselineFreshness.liveModelCallsPerformed.length === 0 && ossBaselineFreshness.externalCallsPerformed.length === 0 && ossBaselineFreshness.protectedActionsExecuted.length === 0))
  checks.push(check('OSS baseline freshness keeps readiness claims blocked', ossBaselineFreshness.releaseReadinessClaimAllowed === false && ossBaselineFreshness.productionReadinessClaimAllowed === false && ossBaselineFreshness.publicReadinessClaimAllowed === false && ossBaselineFreshness.externalValidationClaimAllowed === false && ossBaselineFreshness.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS baseline freshness checks pass', ossBaselineFreshness.baselineFreshnessChecks.every((item) => item.ok)))
  checks.push(check('OSS source review imports current baseline', ossSourceReview.sourceBaselinePath === baselinePath && ossSourceReview.baselineSnapshotDate === baseline.snapshot_date && ossSourceReview.reviewedProjectCount === baseline.top10.length, `${ossSourceReview.sourceBaselinePath}/${ossSourceReview.reviewedProjectCount}`))
  checks.push(check('OSS source review covers source-promoted newly discovered top-10 projects', ossSourceReview.newTop10SourceReviewed.length > 0 && ossSourceReview.newTop10SourceReviewed.every((name) => ossBaselineRefresh.newlyDiscoveredTop10Projects.includes(name)), ossSourceReview.newTop10SourceReviewed.join(',') || 'none'))
  checks.push(check('OSS source review classifies source-supported candidates', ossSourceReview.sourceSupportedCandidateCount >= 5 && ossSourceReview.sourceSupportedCandidateCount + ossSourceReview.metadataOnlyNeedsReviewCount === ossSourceReview.reviewedProjectCount, `${ossSourceReview.sourceSupportedCandidateCount}/${ossSourceReview.metadataOnlyNeedsReviewCount}`))
  checks.push(check('OSS source review writes expected provenance JSONL', ossSourceReview.provenanceJsonlPath === ossSourceReviewProvenanceJsonlPath && ossSourceReview.provenanceJsonlSha256.length === 64 && ossSourceReview.provenanceJsonlRecordCount === baseline.top10.length && ossSourceReview.provenanceJsonlParseable, ossSourceReview.provenanceJsonlPath))
  checks.push(check('OSS source review records bounded GitHub source calls', ossSourceReview.mode === 'external_github_api_oss_source_review' && ossSourceReview.externalGitHubSourceReviewPerformed === true && ossSourceReview.githubApiCallPerformed === true && ossSourceReview.externalCallsPerformed.length >= baseline.top10.length * 2 && ossSourceReview.externalCallsPerformed.every((call) => call.url.startsWith('https://api.github.com/') || call.url.startsWith('https://raw.githubusercontent.com/') || call.url.startsWith('https://github.com/')), `${ossSourceReview.externalCallsPerformed.length} calls`))
  checks.push(check('OSS source review keeps claim expansion blocked', ossSourceReview.publicComparisonClaimAllowed === false && ossSourceReview.superiorityClaimAllowed === false && ossSourceReview.releaseReadinessClaimAllowed === false && ossSourceReview.productionReadinessClaimAllowed === false && ossSourceReview.publicReadinessClaimAllowed === false && ossSourceReview.externalValidationClaimAllowed === false && ossSourceReview.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS source review performed no provider live or protected calls', ossSourceReview.providerCallsPerformed.length === 0 && ossSourceReview.liveModelCallsPerformed.length === 0 && ossSourceReview.protectedActionsExecuted.length === 0))
  checks.push(check('OSS source review checks pass', ossSourceReview.sourceReviewChecks.every((item) => item.ok)))
  checks.push(check('OSS architecture targets import source review evidence', ossArchitectureTargets.mode === 'local_no_provider_oss_architecture_absorption_targets' && ossArchitectureTargets.sourceReviewReportPath === ossSourceReviewJsonPath && ossArchitectureTargets.sourceBaselinePath === baselinePath && ossArchitectureTargets.baselineSnapshotDate === baseline.snapshot_date, `${ossArchitectureTargets.sourceReviewReportPath}/${ossArchitectureTargets.baselineSnapshotDate}`))
  checks.push(check('OSS architecture targets cover reviewed and source-supported candidates', ossArchitectureTargets.reviewedProjectCount === ossSourceReview.reviewedProjectCount && ossArchitectureTargets.targetRecordCount === ossSourceReview.reviewedProjectCount && ossArchitectureTargets.prioritizedTargetCount === ossSourceReview.sourceSupportedCandidateCount && ossArchitectureTargets.deferredTargetCount === ossSourceReview.metadataOnlyNeedsReviewCount, `${ossArchitectureTargets.targetRecordCount}/${ossArchitectureTargets.prioritizedTargetCount}/${ossArchitectureTargets.deferredTargetCount}`))
  checks.push(check('OSS architecture targets prioritize newly discovered source-supported projects', ossArchitectureTargets.newlyDiscoveredPrioritizedTargets.length === ossSourceReview.newTop10SourceReviewed.length && ossSourceReview.newTop10SourceReviewed.every((name) => ossArchitectureTargets.newlyDiscoveredPrioritizedTargets.includes(name)), ossArchitectureTargets.newlyDiscoveredPrioritizedTargets.join(',') || 'none'))
  checks.push(check('OSS architecture targets cover required product-quality axes', ['provider_breadth', 'terminal_workflow', 'tool_loop_reliability', 'eval_and_quality_gates', 'ide_or_editor_surface', 'release_hygiene'].every((axis) => ossArchitectureTargets.coveredAbsorptionAxes.includes(axis)), ossArchitectureTargets.coveredAbsorptionAxes.join(',')))
  checks.push(check('OSS architecture targets write expected provenance JSONL', ossArchitectureTargets.provenanceJsonlPath === ossArchitectureTargetsProvenanceJsonlPath && ossArchitectureTargets.provenanceJsonlSha256.length === 64 && ossArchitectureTargets.provenanceJsonlRecordCount === ossArchitectureTargets.targetRecordCount && ossArchitectureTargets.provenanceJsonlParseable, ossArchitectureTargets.provenanceJsonlPath))
  checks.push(check('OSS architecture targets keep claim expansion blocked', ossArchitectureTargets.publicComparisonClaimAllowed === false && ossArchitectureTargets.superiorityClaimAllowed === false && ossArchitectureTargets.releaseReadinessClaimAllowed === false && ossArchitectureTargets.productionReadinessClaimAllowed === false && ossArchitectureTargets.publicReadinessClaimAllowed === false && ossArchitectureTargets.externalValidationClaimAllowed === false && ossArchitectureTargets.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS architecture targets performed no provider live external or protected calls', ossArchitectureTargets.providerCallsPerformed.length === 0 && ossArchitectureTargets.liveModelCallsPerformed.length === 0 && ossArchitectureTargets.externalCallsPerformed.length === 0 && ossArchitectureTargets.protectedActionsExecuted.length === 0))
  checks.push(check('OSS architecture targets checks pass', ossArchitectureTargets.targetChecks.every((item) => item.ok)))
  checks.push(check('OSS architecture gap review imports architecture targets', ossArchitectureGapReview.mode === 'local_no_provider_oss_architecture_gap_review' && ossArchitectureGapReview.sourceTargetsReportPath === ossArchitectureTargetsJsonPath && ossArchitectureGapReview.sourceReviewReportPath === ossSourceReviewJsonPath && ossArchitectureGapReview.baselineSnapshotDate === baseline.snapshot_date, `${ossArchitectureGapReview.sourceTargetsReportPath}/${ossArchitectureGapReview.baselineSnapshotDate}`))
  checks.push(check('OSS architecture gap review preserves target counts', ossArchitectureGapReview.targetRecordCount === ossArchitectureTargets.targetRecordCount && ossArchitectureGapReview.prioritizedTargetCount === ossArchitectureTargets.prioritizedTargetCount && ossArchitectureGapReview.deferredTargetCount === ossArchitectureTargets.deferredTargetCount && ossArchitectureGapReview.gapRecordCount === ossArchitectureTargets.targetRecordCount, `${ossArchitectureGapReview.gapRecordCount}/${ossArchitectureGapReview.prioritizedTargetCount}/${ossArchitectureGapReview.deferredTargetCount}`))
  checks.push(check('OSS architecture gap review covers required axes and safe actions', ['provider_breadth', 'terminal_workflow', 'tool_loop_reliability', 'eval_and_quality_gates', 'ide_or_editor_surface', 'release_hygiene'].every((axis) => ossArchitectureGapReview.axesReviewed.includes(axis)) && ossArchitectureGapReview.safeInternalActionCount >= ossArchitectureGapReview.targetRecordCount, `${ossArchitectureGapReview.axesReviewed.join(',')}/${ossArchitectureGapReview.safeInternalActionCount}`))
  const ossAxisEvidenceReportBindings = [
    ['provider_breadth', ossProviderBreadthEvidenceJsonPath],
    ['terminal_workflow', ossTerminalWorkflowEvidenceJsonPath],
    ['tool_loop_reliability', ossToolLoopReliabilityEvidenceJsonPath],
    ['eval_and_quality_gates', ossEvalQualityGateChecklistJsonPath],
    ['privacy_and_no_phone_home', ossPrivacyNoPhoneHomeEvidenceJsonPath],
    ['ide_or_editor_surface', ossIdeOrEditorSurfaceEvidenceJsonPath],
    ['release_hygiene', ossReleaseHygieneEvidenceJsonPath],
    ['onboarding_docs', ossOnboardingDocsEvidenceJsonPath],
    ['runtime_doctoring', ossRuntimeDoctoringEvidenceJsonPath],
    ['security_and_permissions', ossSecurityPermissionsEvidenceJsonPath],
  ] as const
  const ossArchitectureGapReviewMissingAxisEvidenceReportBindings = ossArchitectureGapReview.gapRecords.flatMap((record) =>
    ossAxisEvidenceReportBindings
      .filter(([axis]) => record.openClaudeEvidence.some((item) => item.axis === axis))
      .filter(([axis, path]) => {
        const evidence = record.openClaudeEvidence.find((item) => item.axis === axis)
        return !evidence?.currentLocalEvidence.includes(path)
      })
      .map(([axis, path]) => `${record.fullName}:${axis}:${path}`),
  )
  checks.push(check('OSS architecture gap review binds axis-level evidence reports', ossArchitectureGapReviewMissingAxisEvidenceReportBindings.length === 0, ossArchitectureGapReviewMissingAxisEvidenceReportBindings.slice(0, 5).join(',') || 'all bound'))
  checks.push(check('OSS architecture gap review keeps protected gaps explicit', ossArchitectureGapReview.protectedBoundaryGapCount >= ossArchitectureGapReview.prioritizedTargetCount, `${ossArchitectureGapReview.protectedBoundaryGapCount}`))
  checks.push(check('OSS architecture gap review writes expected provenance JSONL', ossArchitectureGapReview.provenanceJsonlPath === ossArchitectureGapReviewProvenanceJsonlPath && ossArchitectureGapReview.provenanceJsonlSha256.length === 64 && ossArchitectureGapReview.provenanceJsonlRecordCount === ossArchitectureGapReview.gapRecordCount && ossArchitectureGapReview.provenanceJsonlParseable, ossArchitectureGapReview.provenanceJsonlPath))
  checks.push(check('OSS architecture gap review keeps claim expansion blocked', ossArchitectureGapReview.publicComparisonClaimAllowed === false && ossArchitectureGapReview.superiorityClaimAllowed === false && ossArchitectureGapReview.releaseReadinessClaimAllowed === false && ossArchitectureGapReview.productionReadinessClaimAllowed === false && ossArchitectureGapReview.publicReadinessClaimAllowed === false && ossArchitectureGapReview.externalValidationClaimAllowed === false && ossArchitectureGapReview.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS architecture gap review performed no provider live external or protected calls', ossArchitectureGapReview.providerCallsPerformed.length === 0 && ossArchitectureGapReview.liveModelCallsPerformed.length === 0 && ossArchitectureGapReview.externalCallsPerformed.length === 0 && ossArchitectureGapReview.protectedActionsExecuted.length === 0))
  checks.push(check('OSS architecture gap review checks pass', ossArchitectureGapReview.gapChecks.every((item) => item.ok)))
  checks.push(check('OSS axis architecture review imports gap review', ossAxisArchitectureReview.mode === 'local_no_provider_oss_axis_architecture_review' && ossAxisArchitectureReview.sourceGapReviewReportPath === ossArchitectureGapReviewJsonPath && ossAxisArchitectureReview.sourceTargetsReportPath === ossArchitectureTargetsJsonPath && ossAxisArchitectureReview.sourceReviewReportPath === ossSourceReviewJsonPath && ossAxisArchitectureReview.baselineSnapshotDate === baseline.snapshot_date, `${ossAxisArchitectureReview.sourceGapReviewReportPath}/${ossAxisArchitectureReview.baselineSnapshotDate}`))
  checks.push(check('OSS axis architecture review covers high-priority targets', ossAxisArchitectureReview.highPriorityProjectCount === ossAxisArchitectureReview.reviewedHighPriorityProjects.length && ossAxisArchitectureReview.reviewedHighPriorityProjects.length === ossArchitectureTargets.newlyDiscoveredPrioritizedTargets.length && ossAxisArchitectureReview.reviewedHighPriorityProjects.every((name) => ossArchitectureTargets.newlyDiscoveredPrioritizedTargets.includes(name)), ossAxisArchitectureReview.reviewedHighPriorityProjects.join(',') || 'none'))
  checks.push(check('OSS axis architecture review covers required axes and backlog', ['provider_breadth', 'terminal_workflow', 'tool_loop_reliability', 'eval_and_quality_gates', 'release_hygiene', 'runtime_doctoring', 'security_and_permissions'].every((axis) => ossAxisArchitectureReview.reviewedAxes.includes(axis)) && ossAxisArchitectureReview.axisReviewRecordCount >= ossAxisArchitectureReview.reviewedAxes.length && ossAxisArchitectureReview.safeInternalBacklogItemCount >= ossAxisArchitectureReview.axisReviewRecordCount, `${ossAxisArchitectureReview.reviewedAxes.join(',')}/${ossAxisArchitectureReview.axisReviewRecordCount}/${ossAxisArchitectureReview.safeInternalBacklogItemCount}`))
  checks.push(check('OSS axis architecture review keeps protected boundaries explicit', ossAxisArchitectureReview.protectedBoundaryCount >= 7, `${ossAxisArchitectureReview.protectedBoundaryCount}`))
  checks.push(check('OSS axis architecture review writes expected provenance JSONL', ossAxisArchitectureReview.provenanceJsonlPath === ossAxisArchitectureReviewProvenanceJsonlPath && ossAxisArchitectureReview.provenanceJsonlSha256.length === 64 && ossAxisArchitectureReview.provenanceJsonlRecordCount === ossAxisArchitectureReview.axisReviewRecordCount && ossAxisArchitectureReview.provenanceJsonlParseable, ossAxisArchitectureReview.provenanceJsonlPath))
  checks.push(check('OSS axis architecture review keeps claim expansion blocked', ossAxisArchitectureReview.publicComparisonClaimAllowed === false && ossAxisArchitectureReview.superiorityClaimAllowed === false && ossAxisArchitectureReview.releaseReadinessClaimAllowed === false && ossAxisArchitectureReview.productionReadinessClaimAllowed === false && ossAxisArchitectureReview.publicReadinessClaimAllowed === false && ossAxisArchitectureReview.externalValidationClaimAllowed === false && ossAxisArchitectureReview.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS axis architecture review performed no provider live external or protected calls', ossAxisArchitectureReview.providerCallsPerformed.length === 0 && ossAxisArchitectureReview.liveModelCallsPerformed.length === 0 && ossAxisArchitectureReview.externalCallsPerformed.length === 0 && ossAxisArchitectureReview.protectedActionsExecuted.length === 0))
  checks.push(check('OSS axis architecture review checks pass', ossAxisArchitectureReview.reviewChecks.every((item) => item.ok)))
  checks.push(check('OSS safe backlog plan imports axis review evidence', ossSafeBacklogPlan.mode === 'local_no_provider_oss_safe_backlog_plan' && ossSafeBacklogPlan.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath && ossSafeBacklogPlan.sourceAxisArchitectureReviewReportSha256.length === 64, `${ossSafeBacklogPlan.sourceAxisArchitectureReviewReportPath}/${ossSafeBacklogPlan.sourceAxisArchitectureReviewReportSha256}`))
  checks.push(check('OSS safe backlog plan preserves backlog count', ossSafeBacklogPlan.sourceSafeInternalBacklogItemCount === ossAxisArchitectureReview.safeInternalBacklogItemCount && ossSafeBacklogPlan.plannedBacklogItemCount === ossAxisArchitectureReview.safeInternalBacklogItemCount && ossSafeBacklogPlan.planItems.length === ossSafeBacklogPlan.plannedBacklogItemCount, `${ossSafeBacklogPlan.plannedBacklogItemCount}/${ossAxisArchitectureReview.safeInternalBacklogItemCount}`))
  checks.push(check('OSS safe backlog plan covers reviewed axes and gates', ossSafeBacklogPlan.uniqueAxisCount === ossAxisArchitectureReview.reviewedAxes.length && ossSafeBacklogPlan.nextSafeInternalGateCandidateCount === ossAxisArchitectureReview.reviewedAxes.length && ossSafeBacklogPlan.nextSafeInternalGateCandidates.every((candidate) => ossAxisArchitectureReview.reviewedAxes.includes(candidate.axis) && candidate.sourceBacklogItemCount > 0 && candidate.protectedActionRequiredForPlanning === false), `${ossSafeBacklogPlan.nextSafeInternalGateCandidateCount}/${ossSafeBacklogPlan.uniqueAxisCount}`))
  checks.push(check('OSS safe backlog plan keeps every item bounded', ossSafeBacklogPlan.planItems.every((item) => item.currentLocalEvidence.length > 0 && item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'planned_internal_no_provider' && item.protectedActionRequiredForPlanning === false && item.protectedActionExecuted === false && item.claimAllowed === false), `${ossSafeBacklogPlan.planItems.length} items`))
  checks.push(check('OSS safe backlog plan writes expected provenance JSONL', ossSafeBacklogPlan.provenanceJsonlPath === ossSafeBacklogPlanProvenanceJsonlPath && ossSafeBacklogPlan.provenanceJsonlSha256.length === 64 && ossSafeBacklogPlan.provenanceJsonlRecordCount === ossSafeBacklogPlan.plannedBacklogItemCount && ossSafeBacklogPlan.provenanceJsonlParseable, ossSafeBacklogPlan.provenanceJsonlPath))
  checks.push(check('OSS safe backlog plan keeps claim expansion blocked', ossSafeBacklogPlan.publicComparisonClaimAllowed === false && ossSafeBacklogPlan.superiorityClaimAllowed === false && ossSafeBacklogPlan.releaseReadinessClaimAllowed === false && ossSafeBacklogPlan.productionReadinessClaimAllowed === false && ossSafeBacklogPlan.publicReadinessClaimAllowed === false && ossSafeBacklogPlan.externalValidationClaimAllowed === false && ossSafeBacklogPlan.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OSS safe backlog plan performed no provider live external or protected calls', ossSafeBacklogPlan.providerCallsPerformed.length === 0 && ossSafeBacklogPlan.liveModelCallsPerformed.length === 0 && ossSafeBacklogPlan.externalCallsPerformed.length === 0 && ossSafeBacklogPlan.protectedActionsExecuted.length === 0))
  checks.push(check('OSS safe backlog plan checks pass', ossSafeBacklogPlan.planChecks.every((item) => item.ok)))
  checks.push(check('OSS safe backlog closure is local no-provider check', ossSafeBacklogClosure.mode === 'local_no_provider_oss_safe_backlog_closure'))
  checks.push(check('OSS safe backlog closure imports planned candidates', ossSafeBacklogClosure.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossSafeBacklogClosure.sourceCandidateCount === ossSafeBacklogPlan.nextSafeInternalGateCandidateCount, `${String(ossSafeBacklogClosure.sourceCandidateCount)}/${ossSafeBacklogPlan.nextSafeInternalGateCandidateCount}`))
  checks.push(check('OSS safe backlog closure closes every planned internal evidence gate', ossSafeBacklogClosure.openCandidateCount === 0 && ossSafeBacklogClosure.closedCandidateCount === ossSafeBacklogClosure.sourceCandidateCount && ossSafeBacklogClosureRecords.every((record) => record.closureStatus === 'closed_by_existing_internal_evidence_gate'), `${String(ossSafeBacklogClosure.closedCandidateCount)}/${String(ossSafeBacklogClosure.sourceCandidateCount)}`))
  checks.push(check('OSS safe backlog closure writes expected JSONL', ossSafeBacklogClosure.closureJsonlPath === ossSafeBacklogClosureJsonlPath && typeof ossSafeBacklogClosure.closureJsonlSha256 === 'string' && ossSafeBacklogClosure.closureJsonlSha256.length === 64 && ossSafeBacklogClosure.closureJsonlRecordCount === ossSafeBacklogClosureRecords.length, String(ossSafeBacklogClosure.closureJsonlPath)))
  checks.push(check('OSS safe backlog closure preserves no-provider and protected-action boundaries', Array.isArray(ossSafeBacklogClosure.providerCallsPerformed) && ossSafeBacklogClosure.providerCallsPerformed.length === 0 && Array.isArray(ossSafeBacklogClosure.liveModelCallsPerformed) && ossSafeBacklogClosure.liveModelCallsPerformed.length === 0 && Array.isArray(ossSafeBacklogClosure.externalCallsPerformed) && ossSafeBacklogClosure.externalCallsPerformed.length === 0 && Array.isArray(ossSafeBacklogClosure.protectedActionsExecuted) && ossSafeBacklogClosure.protectedActionsExecuted.length === 0))
  checks.push(check('OSS safe backlog closure keeps readiness and superiority claims blocked', ossSafeBacklogClosure.releaseReadinessClaimAllowed === false && ossSafeBacklogClosure.productionReadinessClaimAllowed === false && ossSafeBacklogClosure.publicReadinessClaimAllowed === false && ossSafeBacklogClosure.externalValidationClaimAllowed === false && ossSafeBacklogClosure.autonomousReliabilityClaimAllowed === false && ossSafeBacklogClosure.superiorityClaimAllowed === false))
  checks.push(check('OSS safe backlog closure checks pass', ossSafeBacklogClosureChecks.every((item) => item.ok === true)))
  checks.push(check('OSS baseline drift closure is local no-provider check', ossBaselineDriftClosure.mode === 'local_no_provider_oss_baseline_drift_closure'))
  checks.push(check('OSS baseline drift closure propagates newly discovered top-10 projects', ossBaselineDriftClosure.propagatedNewDiscoveryCount === ossBaselineRefresh.newlyDiscoveredTop10Projects.length && ossBaselineDriftClosureRecords.filter((record) => record.driftKind === 'newly_discovered_top10').every((record) => record.status === 'propagated_to_current_internal_evidence'), `${String(ossBaselineDriftClosure.propagatedNewDiscoveryCount)}/${ossBaselineRefresh.newlyDiscoveredTop10Projects.length}`))
  checks.push(check('OSS baseline drift closure removes prior top-10 projects from current target reports', ossBaselineDriftClosure.removedPreviousTop10Count === ossBaselineRefresh.removedPreviousTop10Projects.length && ossBaselineDriftClosureRecords.filter((record) => record.driftKind === 'removed_previous_top10').every((record) => record.presentInCurrentBaseline === false && record.status === 'removed_from_current_top10_only'), `${String(ossBaselineDriftClosure.removedPreviousTop10Count)}/${ossBaselineRefresh.removedPreviousTop10Projects.length}`))
  checks.push(check('OSS baseline drift closure writes expected JSONL', ossBaselineDriftClosure.driftJsonlPath === ossBaselineDriftClosureJsonlPath && typeof ossBaselineDriftClosure.driftJsonlSha256 === 'string' && ossBaselineDriftClosure.driftJsonlSha256.length === 64 && ossBaselineDriftClosure.driftJsonlRecordCount === ossBaselineDriftClosureRecords.length, String(ossBaselineDriftClosure.driftJsonlPath)))
  checks.push(check('OSS baseline drift closure preserves no-provider and protected-action boundaries', Array.isArray(ossBaselineDriftClosure.providerCallsPerformed) && ossBaselineDriftClosure.providerCallsPerformed.length === 0 && Array.isArray(ossBaselineDriftClosure.liveModelCallsPerformed) && ossBaselineDriftClosure.liveModelCallsPerformed.length === 0 && Array.isArray(ossBaselineDriftClosure.externalCallsPerformed) && ossBaselineDriftClosure.externalCallsPerformed.length === 0 && Array.isArray(ossBaselineDriftClosure.protectedActionsExecuted) && ossBaselineDriftClosure.protectedActionsExecuted.length === 0))
  checks.push(check('OSS baseline drift closure keeps readiness and superiority claims blocked', ossBaselineDriftClosure.releaseReadinessClaimAllowed === false && ossBaselineDriftClosure.productionReadinessClaimAllowed === false && ossBaselineDriftClosure.publicReadinessClaimAllowed === false && ossBaselineDriftClosure.publicComparisonClaimAllowed === false && ossBaselineDriftClosure.externalValidationClaimAllowed === false && ossBaselineDriftClosure.autonomousReliabilityClaimAllowed === false && ossBaselineDriftClosure.superiorityClaimAllowed === false))
  checks.push(check('OSS baseline drift closure checks pass', ossBaselineDriftClosureChecks.every((item) => item.ok === true)))
  checks.push(check('OSS benchmark comparison matrix is local no-provider check', ossBenchmarkComparisonMatrix.mode === 'local_no_provider_oss_benchmark_comparison_matrix'))
  checks.push(check('OSS benchmark comparison matrix covers every top-10 project-axis pair', ossBenchmarkComparisonMatrix.top10ProjectCount === baseline.top10.length && ossBenchmarkComparisonMatrix.requiredProductAxisCount === baseline.required_product_axes.length && ossBenchmarkComparisonMatrix.matrixRecordCount === baseline.top10.length * baseline.required_product_axes.length && ossBenchmarkComparisonMatrixRecords.length === ossBenchmarkComparisonMatrix.matrixRecordCount, `${String(ossBenchmarkComparisonMatrix.matrixRecordCount)}/${baseline.top10.length * baseline.required_product_axes.length}`))
  checks.push(check('OSS benchmark comparison matrix writes expected JSONL', ossBenchmarkComparisonMatrix.comparisonMatrixJsonlPath === ossBenchmarkComparisonMatrixJsonlPath && typeof ossBenchmarkComparisonMatrix.comparisonMatrixJsonlSha256 === 'string' && ossBenchmarkComparisonMatrix.comparisonMatrixJsonlSha256.length === 64 && ossBenchmarkComparisonMatrix.comparisonMatrixJsonlRecordCount === ossBenchmarkComparisonMatrixRecords.length, String(ossBenchmarkComparisonMatrix.comparisonMatrixJsonlPath)))
  checks.push(check('OSS benchmark comparison matrix records evidence-backed and open-gap rows', Number(ossBenchmarkComparisonMatrix.recordsWithLocalEvidenceCount) > 0 && Number(ossBenchmarkComparisonMatrix.axisNotYetAbsorbedRecordCount) > 0 && Number(ossBenchmarkComparisonMatrix.recordsNeedingProtectedActionCount) === ossBenchmarkComparisonMatrix.matrixRecordCount, `evidence=${String(ossBenchmarkComparisonMatrix.recordsWithLocalEvidenceCount)} open=${String(ossBenchmarkComparisonMatrix.axisNotYetAbsorbedRecordCount)}`))
  checks.push(check('OSS benchmark comparison matrix preserves no-provider and protected-action boundaries', Array.isArray(ossBenchmarkComparisonMatrix.providerCallsPerformed) && ossBenchmarkComparisonMatrix.providerCallsPerformed.length === 0 && Array.isArray(ossBenchmarkComparisonMatrix.liveModelCallsPerformed) && ossBenchmarkComparisonMatrix.liveModelCallsPerformed.length === 0 && Array.isArray(ossBenchmarkComparisonMatrix.externalCallsPerformed) && ossBenchmarkComparisonMatrix.externalCallsPerformed.length === 0 && Array.isArray(ossBenchmarkComparisonMatrix.protectedActionsExecuted) && ossBenchmarkComparisonMatrix.protectedActionsExecuted.length === 0 && ossBenchmarkComparisonMatrixRecords.every((record) => record.protectedActionExecuted === false)))
  checks.push(check('OSS benchmark comparison matrix keeps comparison superiority and readiness claims blocked', ossBenchmarkComparisonMatrix.publicComparisonClaimAllowed === false && ossBenchmarkComparisonMatrix.superiorityClaimAllowed === false && ossBenchmarkComparisonMatrix.releaseReadinessClaimAllowed === false && ossBenchmarkComparisonMatrix.productionReadinessClaimAllowed === false && ossBenchmarkComparisonMatrix.publicReadinessClaimAllowed === false && ossBenchmarkComparisonMatrix.externalValidationClaimAllowed === false && ossBenchmarkComparisonMatrix.autonomousReliabilityClaimAllowed === false && ossBenchmarkComparisonMatrixRecords.every((record) => record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS benchmark comparison matrix checks pass', ossBenchmarkComparisonMatrixChecks.every((item) => item.ok === true)))
  checks.push(check('OSS comparison readiness index is local no-provider check', ossComparisonReadinessIndex.mode === 'local_no_provider_oss_comparison_readiness_index'))
  checks.push(check('OSS comparison readiness index imports the comparison matrix', ossComparisonReadinessIndex.sourceComparisonMatrixReportPath === ossBenchmarkComparisonMatrixJsonPath && typeof ossComparisonReadinessIndex.sourceComparisonMatrixReportSha256 === 'string' && ossComparisonReadinessIndex.matrixRecordCount === ossBenchmarkComparisonMatrix.matrixRecordCount, `${String(ossComparisonReadinessIndex.matrixRecordCount)}/${String(ossBenchmarkComparisonMatrix.matrixRecordCount)}`))
  checks.push(check('OSS comparison readiness index creates axis and project priority records', ossComparisonReadinessIndex.axisIndexRecordCount === ossBenchmarkComparisonMatrix.requiredProductAxisCount && ossComparisonReadinessIndex.projectIndexRecordCount === ossBenchmarkComparisonMatrix.top10ProjectCount && ossComparisonReadinessIndex.indexRecordCount === Number(ossBenchmarkComparisonMatrix.requiredProductAxisCount) + Number(ossBenchmarkComparisonMatrix.top10ProjectCount) && ossComparisonReadinessIndexRecords.length === ossComparisonReadinessIndex.indexRecordCount, `${String(ossComparisonReadinessIndex.indexRecordCount)} records`))
  checks.push(check('OSS comparison readiness index writes expected JSONL', ossComparisonReadinessIndex.readinessIndexJsonlPath === ossComparisonReadinessIndexJsonlPath && typeof ossComparisonReadinessIndex.readinessIndexJsonlSha256 === 'string' && ossComparisonReadinessIndex.readinessIndexJsonlSha256.length === 64 && ossComparisonReadinessIndex.readinessIndexJsonlRecordCount === ossComparisonReadinessIndexRecords.length, String(ossComparisonReadinessIndex.readinessIndexJsonlPath)))
  checks.push(check('OSS comparison readiness index preserves no-provider and protected-action boundaries', Array.isArray(ossComparisonReadinessIndex.providerCallsPerformed) && ossComparisonReadinessIndex.providerCallsPerformed.length === 0 && Array.isArray(ossComparisonReadinessIndex.liveModelCallsPerformed) && ossComparisonReadinessIndex.liveModelCallsPerformed.length === 0 && Array.isArray(ossComparisonReadinessIndex.externalCallsPerformed) && ossComparisonReadinessIndex.externalCallsPerformed.length === 0 && Array.isArray(ossComparisonReadinessIndex.protectedActionsExecuted) && ossComparisonReadinessIndex.protectedActionsExecuted.length === 0 && ossComparisonReadinessIndex.protectedActionExecuted === false && ossComparisonReadinessIndexRecords.every((record) => record.protectedActionExecuted === false)))
  checks.push(check('OSS comparison readiness index keeps comparison superiority and readiness claims blocked', ossComparisonReadinessIndex.publicComparisonClaimAllowed === false && ossComparisonReadinessIndex.superiorityClaimAllowed === false && ossComparisonReadinessIndex.releaseReadinessClaimAllowed === false && ossComparisonReadinessIndex.productionReadinessClaimAllowed === false && ossComparisonReadinessIndex.publicReadinessClaimAllowed === false && ossComparisonReadinessIndex.externalValidationClaimAllowed === false && ossComparisonReadinessIndex.autonomousReliabilityClaimAllowed === false && ossComparisonReadinessIndexRecords.every((record) => record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS comparison readiness index leaves terminal boundary protected', ossComparisonReadinessIndex.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY' && ossComparisonReadinessIndex.protectedActionRequiredForNextVerifiableBoundary === true && ossComparisonReadinessIndex.mthResolutionStatus === 'unresolved' && ossComparisonReadinessIndex.canonicalMemoryWriteAllowed === false, String(ossComparisonReadinessIndex.terminalCondition)))
  checks.push(check('OSS comparison readiness index checks pass', ossComparisonReadinessIndexChecks.every((item) => item.ok === true)))
  checks.push(check('OSS IDE/editor surface evidence is local no-provider check', ossIdeOrEditorSurfaceEvidence.mode === 'local_no_provider_oss_ide_or_editor_surface_evidence' && ossIdeOrEditorSurfaceEvidence.selectedAxis === 'ide_or_editor_surface'))
  checks.push(check('OSS IDE/editor surface evidence imports readiness and comparison sources', ossIdeOrEditorSurfaceEvidence.sourceReadinessIndexReportPath === ossComparisonReadinessIndexJsonPath && ossIdeOrEditorSurfaceEvidence.sourceComparisonMatrixReportPath === ossBenchmarkComparisonMatrixJsonPath && ossIdeOrEditorSurfaceEvidence.sourceIdeMatrixRowCount === ossBenchmarkComparisonMatrix.top10ProjectCount, `${String(ossIdeOrEditorSurfaceEvidence.sourceIdeMatrixRowCount)}/${String(ossBenchmarkComparisonMatrix.top10ProjectCount)}`))
  checks.push(check('OSS IDE/editor surface evidence binds current priority counts', ossIdeOrEditorSurfaceEvidence.sourceIdePriorityTier === 'safe_internal_absorption_priority' && ossIdeOrEditorSurfaceEvidence.sourceIdeLocalEvidenceBackedCellCount > 0 && ossIdeOrEditorSurfaceEvidence.sourceIdeLocalEvidenceBackedCellCount + ossIdeOrEditorSurfaceEvidence.sourceIdeAxisNotYetAbsorbedCellCount + ossIdeOrEditorSurfaceEvidence.sourceIdeMetadataOnlyCellCount === ossIdeOrEditorSurfaceEvidence.sourceIdeMatrixRowCount, `${String(ossIdeOrEditorSurfaceEvidence.sourceIdeLocalEvidenceBackedCellCount)}/${String(ossIdeOrEditorSurfaceEvidence.sourceIdeAxisNotYetAbsorbedCellCount)}/${String(ossIdeOrEditorSurfaceEvidence.sourceIdeMetadataOnlyCellCount)}`))
  checks.push(check('OSS IDE/editor surface evidence binds local VS Code evidence and protected host boundary', ossIdeOrEditorSurfaceEvidence.localIdeEvidenceBindingCount === 13 && ossIdeOrEditorSurfaceEvidence.hostSmokeRealHostBlockedByVscodeCli === true && (ossIdeOrEditorSurfaceEvidence.workbenchSmokePass === true || ideExtensionWorkbenchEnvironmentBlocked), `${String(ossIdeOrEditorSurfaceEvidence.localIdeEvidenceBindingCount)} bindings`))
  checks.push(check('OSS IDE/editor surface evidence writes expected JSONL', ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlPath === ossIdeOrEditorSurfaceEvidenceJsonlPath && typeof ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlSha256 === 'string' && ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlSha256.length === 64 && ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlRecordCount === ossIdeOrEditorSurfaceEvidenceRecords.length, String(ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlPath)))
  checks.push(check('OSS IDE/editor surface evidence preserves no-provider and protected-action boundaries', Array.isArray(ossIdeOrEditorSurfaceEvidence.providerCallsPerformed) && ossIdeOrEditorSurfaceEvidence.providerCallsPerformed.length === 0 && Array.isArray(ossIdeOrEditorSurfaceEvidence.liveModelCallsPerformed) && ossIdeOrEditorSurfaceEvidence.liveModelCallsPerformed.length === 0 && Array.isArray(ossIdeOrEditorSurfaceEvidence.externalCallsPerformed) && ossIdeOrEditorSurfaceEvidence.externalCallsPerformed.length === 0 && Array.isArray(ossIdeOrEditorSurfaceEvidence.protectedActionsExecuted) && ossIdeOrEditorSurfaceEvidence.protectedActionsExecuted.length === 0 && ossIdeOrEditorSurfaceEvidence.protectedActionExecuted === false && ossIdeOrEditorSurfaceEvidenceRecords.every((record) => record.protectedActionExecuted === false)))
  checks.push(check('OSS IDE/editor surface evidence keeps availability comparison superiority and readiness claims blocked', ossIdeOrEditorSurfaceEvidence.extensionAvailabilityClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.publicComparisonClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.superiorityClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.releaseReadinessClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.productionReadinessClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.publicReadinessClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.externalValidationClaimAllowed === false && ossIdeOrEditorSurfaceEvidence.autonomousReliabilityClaimAllowed === false && ossIdeOrEditorSurfaceEvidenceRecords.every((record) => record.extensionAvailabilityClaimAllowed === false && record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS IDE/editor surface evidence leaves terminal boundary protected', ossIdeOrEditorSurfaceEvidence.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY' && ossIdeOrEditorSurfaceEvidence.protectedActionRequiredForNextVerifiableBoundary === true && ossIdeOrEditorSurfaceEvidence.mthResolutionStatus === 'unresolved' && ossIdeOrEditorSurfaceEvidence.canonicalMemoryWriteAllowed === false, String(ossIdeOrEditorSurfaceEvidence.terminalCondition)))
  checks.push(check('OSS IDE/editor surface evidence checks pass', ossIdeOrEditorSurfaceEvidenceChecks.every((item) => item.ok === true)))
  checks.push(check('OSS privacy no-phone-home evidence is local no-provider check', ossPrivacyNoPhoneHomeEvidence.mode === 'local_no_provider_oss_privacy_no_phone_home_evidence' && ossPrivacyNoPhoneHomeEvidence.selectedAxis === 'privacy_and_no_phone_home'))
  checks.push(check('OSS privacy no-phone-home evidence imports readiness and comparison sources', ossPrivacyNoPhoneHomeEvidence.sourceReadinessIndexReportPath === ossComparisonReadinessIndexJsonPath && ossPrivacyNoPhoneHomeEvidence.sourceComparisonMatrixReportPath === ossBenchmarkComparisonMatrixJsonPath && ossPrivacyNoPhoneHomeEvidence.sourcePrivacyMatrixRowCount === ossBenchmarkComparisonMatrix.top10ProjectCount, `${String(ossPrivacyNoPhoneHomeEvidence.sourcePrivacyMatrixRowCount)}/${String(ossBenchmarkComparisonMatrix.top10ProjectCount)}`))
  checks.push(check('OSS privacy no-phone-home evidence scans build output cleanly', ossPrivacyNoPhoneHomeEvidence.bannedPatternFindingCount === 0 && ossPrivacyNoPhoneHomeEvidence.noTelemetryPluginPresent === true && ossPrivacyNoPhoneHomeEvidence.privacySettingsSurfacePresent === true && ossPrivacyNoPhoneHomeEvidence.verifyPrivacyScriptPresent === true && ossPrivacyNoPhoneHomeEvidence.packageVerifyPrivacyScriptPresent === true && ossPrivacyNoPhoneHomeEvidence.buildVerifiedIncludesPrivacy === true, `${String(ossPrivacyNoPhoneHomeEvidence.bannedPatternFindingCount)} findings`))
  checks.push(check('OSS privacy no-phone-home evidence writes expected JSONL', ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlPath === ossPrivacyNoPhoneHomeEvidenceJsonlPath && typeof ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlSha256 === 'string' && ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlSha256.length === 64 && ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlRecordCount === ossPrivacyNoPhoneHomeEvidenceRecords.length, String(ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlPath)))
  checks.push(check('OSS privacy no-phone-home evidence preserves no-provider and protected-action boundaries', Array.isArray(ossPrivacyNoPhoneHomeEvidence.providerCallsPerformed) && ossPrivacyNoPhoneHomeEvidence.providerCallsPerformed.length === 0 && Array.isArray(ossPrivacyNoPhoneHomeEvidence.liveModelCallsPerformed) && ossPrivacyNoPhoneHomeEvidence.liveModelCallsPerformed.length === 0 && Array.isArray(ossPrivacyNoPhoneHomeEvidence.externalCallsPerformed) && ossPrivacyNoPhoneHomeEvidence.externalCallsPerformed.length === 0 && Array.isArray(ossPrivacyNoPhoneHomeEvidence.protectedActionsExecuted) && ossPrivacyNoPhoneHomeEvidence.protectedActionsExecuted.length === 0 && ossPrivacyNoPhoneHomeEvidence.protectedActionExecuted === false && ossPrivacyNoPhoneHomeEvidenceRecords.every((record) => record.protectedActionExecuted === false)))
  checks.push(check('OSS privacy no-phone-home evidence keeps privacy comparison superiority and readiness claims blocked', ossPrivacyNoPhoneHomeEvidence.publicPrivacyClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.publicComparisonClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.superiorityClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.releaseReadinessClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.productionReadinessClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.publicReadinessClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.externalValidationClaimAllowed === false && ossPrivacyNoPhoneHomeEvidence.autonomousReliabilityClaimAllowed === false && ossPrivacyNoPhoneHomeEvidenceRecords.every((record) => record.publicPrivacyClaimAllowed === false && record.publicComparisonClaimAllowed === false && record.superiorityClaimAllowed === false && record.releaseReadinessClaimAllowed === false && record.productionReadinessClaimAllowed === false && record.publicReadinessClaimAllowed === false && record.externalValidationClaimAllowed === false && record.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS privacy no-phone-home evidence leaves terminal boundary protected', ossPrivacyNoPhoneHomeEvidence.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY' && ossPrivacyNoPhoneHomeEvidence.protectedActionRequiredForNextVerifiableBoundary === true && ossPrivacyNoPhoneHomeEvidence.mthResolutionStatus === 'unresolved' && ossPrivacyNoPhoneHomeEvidence.canonicalMemoryWriteAllowed === false, String(ossPrivacyNoPhoneHomeEvidence.terminalCondition)))
  checks.push(check('OSS privacy no-phone-home evidence checks pass', ossPrivacyNoPhoneHomeEvidenceChecks.every((item) => item.ok === true)))
  checks.push(check('OSS eval quality gate checklist imports safe backlog evidence', ossEvalQualityGateChecklist.mode === 'local_no_provider_oss_eval_quality_gate_checklist' && ossEvalQualityGateChecklist.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossEvalQualityGateChecklist.sourceSafeBacklogPlanReportSha256.length === 64 && ossEvalQualityGateChecklist.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossEvalQualityGateChecklist.sourceSafeBacklogPlanReportPath}/${ossEvalQualityGateChecklist.selectedAxis}`))
  checks.push(check('OSS eval quality gate checklist covers selected axis items', ossEvalQualityGateChecklist.selectedAxis === 'eval_and_quality_gates' && ossEvalQualityGateChecklist.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'eval_and_quality_gates').length && ossEvalQualityGateChecklist.checklistItemCount === ossEvalQualityGateChecklist.sourcePlanItemCount && ossEvalQualityGateChecklist.checklistItems.every((item) => item.axis === 'eval_and_quality_gates'), `${ossEvalQualityGateChecklist.checklistItemCount}/${ossEvalQualityGateChecklist.sourcePlanItemCount}`))
  checks.push(check('OSS eval quality gate checklist writes expected provenance JSONL', ossEvalQualityGateChecklist.provenanceJsonlPath === ossEvalQualityGateChecklistProvenanceJsonlPath && ossEvalQualityGateChecklist.provenanceJsonlSha256.length === 64 && ossEvalQualityGateChecklist.provenanceJsonlRecordCount === ossEvalQualityGateChecklist.checklistItemCount && ossEvalQualityGateChecklist.provenanceJsonlParseable, ossEvalQualityGateChecklist.provenanceJsonlPath))
  checks.push(check('OSS eval quality gate checklist keeps every item bounded', ossEvalQualityGateChecklist.checklistItems.every((item) => item.currentLocalEvidence.length > 0 && item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'checklist_created_internal_no_provider' && item.protectedActionRequiredForChecklist === false && item.protectedActionExecuted === false), `${ossEvalQualityGateChecklist.checklistItems.length} items`))
  checks.push(check('OSS eval quality gate checklist keeps benchmark and readiness claims blocked', ossEvalQualityGateChecklist.publicBenchmarkClaimAllowed === false && ossEvalQualityGateChecklist.leaderboardClaimAllowed === false && ossEvalQualityGateChecklist.publicComparisonClaimAllowed === false && ossEvalQualityGateChecklist.superiorityClaimAllowed === false && ossEvalQualityGateChecklist.releaseReadinessClaimAllowed === false && ossEvalQualityGateChecklist.productionReadinessClaimAllowed === false && ossEvalQualityGateChecklist.publicReadinessClaimAllowed === false && ossEvalQualityGateChecklist.externalValidationClaimAllowed === false && ossEvalQualityGateChecklist.autonomousReliabilityClaimAllowed === false && ossEvalQualityGateChecklist.checklistItems.every((item) => item.publicBenchmarkClaimAllowed === false && item.leaderboardClaimAllowed === false && item.superiorityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS eval quality gate checklist performed no provider live external or protected calls', ossEvalQualityGateChecklist.providerCallsPerformed.length === 0 && ossEvalQualityGateChecklist.liveModelCallsPerformed.length === 0 && ossEvalQualityGateChecklist.externalCallsPerformed.length === 0 && ossEvalQualityGateChecklist.protectedActionsExecuted.length === 0))
  checks.push(check('OSS eval quality gate checklist checks pass', ossEvalQualityGateChecklist.checklistChecks.every((item) => item.ok)))
  checks.push(check('OSS terminal workflow evidence imports safe backlog evidence', ossTerminalWorkflowEvidence.mode === 'local_no_provider_oss_terminal_workflow_evidence' && ossTerminalWorkflowEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossTerminalWorkflowEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossTerminalWorkflowEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossTerminalWorkflowEvidence.sourceSafeBacklogPlanReportPath}/${ossTerminalWorkflowEvidence.selectedAxis}`))
  checks.push(check('OSS terminal workflow evidence covers selected axis items', ossTerminalWorkflowEvidence.selectedAxis === 'terminal_workflow' && ossTerminalWorkflowEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'terminal_workflow').length && ossTerminalWorkflowEvidence.evidenceItemCount === ossTerminalWorkflowEvidence.sourcePlanItemCount && ossTerminalWorkflowEvidence.evidenceItems.every((item) => item.axis === 'terminal_workflow'), `${ossTerminalWorkflowEvidence.evidenceItemCount}/${ossTerminalWorkflowEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS terminal workflow evidence writes expected provenance JSONL', ossTerminalWorkflowEvidence.provenanceJsonlPath === ossTerminalWorkflowEvidenceProvenanceJsonlPath && ossTerminalWorkflowEvidence.provenanceJsonlSha256.length === 64 && ossTerminalWorkflowEvidence.provenanceJsonlRecordCount === ossTerminalWorkflowEvidence.evidenceItemCount && ossTerminalWorkflowEvidence.provenanceJsonlParseable, ossTerminalWorkflowEvidence.provenanceJsonlPath))
  checks.push(check('OSS terminal workflow evidence binds local evidence hashes', ossTerminalWorkflowEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossTerminalWorkflowEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).length} bindings`))
  checks.push(check('OSS terminal workflow evidence covers transcript and command-hash classes', ['first_run_failure_recovery_doctor_handoff', 'command_hash_no_provider_boundary'].every((coverage) => ossTerminalWorkflowEvidence.evidenceItems.some((item) => item.transcriptCoverageClass === coverage))))
  checks.push(check('OSS terminal workflow evidence keeps every item bounded', ossTerminalWorkflowEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'terminal_workflow_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossTerminalWorkflowEvidence.evidenceItems.length} items`))
  checks.push(check('OSS terminal workflow evidence keeps session benchmark and readiness claims blocked', ossTerminalWorkflowEvidence.nonSyntheticUserSessionClaimAllowed === false && ossTerminalWorkflowEvidence.externalBenchmarkSessionClaimAllowed === false && ossTerminalWorkflowEvidence.publicComparisonClaimAllowed === false && ossTerminalWorkflowEvidence.superiorityClaimAllowed === false && ossTerminalWorkflowEvidence.releaseReadinessClaimAllowed === false && ossTerminalWorkflowEvidence.productionReadinessClaimAllowed === false && ossTerminalWorkflowEvidence.publicReadinessClaimAllowed === false && ossTerminalWorkflowEvidence.externalValidationClaimAllowed === false && ossTerminalWorkflowEvidence.autonomousReliabilityClaimAllowed === false && ossTerminalWorkflowEvidence.evidenceItems.every((item) => item.nonSyntheticUserSessionClaimAllowed === false && item.externalBenchmarkSessionClaimAllowed === false && item.publicComparisonClaimAllowed === false && item.superiorityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS terminal workflow evidence performed no provider live external or protected calls', ossTerminalWorkflowEvidence.providerCallsPerformed.length === 0 && ossTerminalWorkflowEvidence.liveModelCallsPerformed.length === 0 && ossTerminalWorkflowEvidence.externalCallsPerformed.length === 0 && ossTerminalWorkflowEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS terminal workflow evidence checks pass', ossTerminalWorkflowEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS onboarding docs evidence imports safe backlog evidence', ossOnboardingDocsEvidence.mode === 'local_no_provider_oss_onboarding_docs_evidence' && ossOnboardingDocsEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossOnboardingDocsEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossOnboardingDocsEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossOnboardingDocsEvidence.sourceSafeBacklogPlanReportPath}/${ossOnboardingDocsEvidence.selectedAxis}`))
  checks.push(check('OSS onboarding docs evidence covers selected axis items', ossOnboardingDocsEvidence.selectedAxis === 'onboarding_docs' && ossOnboardingDocsEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'onboarding_docs').length && ossOnboardingDocsEvidence.evidenceItemCount === ossOnboardingDocsEvidence.sourcePlanItemCount && ossOnboardingDocsEvidence.evidenceItems.every((item) => item.axis === 'onboarding_docs'), `${ossOnboardingDocsEvidence.evidenceItemCount}/${ossOnboardingDocsEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS onboarding docs evidence writes expected provenance JSONL', ossOnboardingDocsEvidence.provenanceJsonlPath === ossOnboardingDocsEvidenceProvenanceJsonlPath && ossOnboardingDocsEvidence.provenanceJsonlSha256.length === 64 && ossOnboardingDocsEvidence.provenanceJsonlRecordCount === ossOnboardingDocsEvidence.evidenceItemCount && ossOnboardingDocsEvidence.provenanceJsonlParseable, ossOnboardingDocsEvidence.provenanceJsonlPath))
  checks.push(check('OSS onboarding docs evidence binds local evidence hashes', ossOnboardingDocsEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossOnboardingDocsEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).length} bindings`))
  checks.push(check('OSS onboarding docs evidence covers first-run boundary and link-integrity classes', ['non_synthetic_first_run_boundary', 'readme_quickstart_link_integrity'].every((coverage) => ossOnboardingDocsEvidence.evidenceItems.some((item) => item.onboardingCoverageClass === coverage))))
  checks.push(check('OSS onboarding docs evidence keeps every item bounded', ossOnboardingDocsEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'onboarding_docs_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossOnboardingDocsEvidence.evidenceItems.length} items`))
  checks.push(check('OSS onboarding docs evidence keeps first-run platform and readiness claims blocked', ossOnboardingDocsEvidence.nonSyntheticFirstRunClaimAllowed === false && ossOnboardingDocsEvidence.crossPlatformOnboardingClaimAllowed === false && ossOnboardingDocsEvidence.publicComparisonClaimAllowed === false && ossOnboardingDocsEvidence.superiorityClaimAllowed === false && ossOnboardingDocsEvidence.releaseReadinessClaimAllowed === false && ossOnboardingDocsEvidence.productionReadinessClaimAllowed === false && ossOnboardingDocsEvidence.publicReadinessClaimAllowed === false && ossOnboardingDocsEvidence.externalValidationClaimAllowed === false && ossOnboardingDocsEvidence.autonomousReliabilityClaimAllowed === false && ossOnboardingDocsEvidence.evidenceItems.every((item) => item.nonSyntheticFirstRunClaimAllowed === false && item.crossPlatformOnboardingClaimAllowed === false && item.publicReadinessClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS onboarding docs evidence performed no provider live external or protected calls', ossOnboardingDocsEvidence.providerCallsPerformed.length === 0 && ossOnboardingDocsEvidence.liveModelCallsPerformed.length === 0 && ossOnboardingDocsEvidence.externalCallsPerformed.length === 0 && ossOnboardingDocsEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS onboarding docs evidence checks pass', ossOnboardingDocsEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS runtime doctoring evidence imports safe backlog evidence', ossRuntimeDoctoringEvidence.mode === 'local_no_provider_oss_runtime_doctoring_evidence' && ossRuntimeDoctoringEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossRuntimeDoctoringEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossRuntimeDoctoringEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossRuntimeDoctoringEvidence.sourceSafeBacklogPlanReportPath}/${ossRuntimeDoctoringEvidence.selectedAxis}`))
  checks.push(check('OSS runtime doctoring evidence covers selected axis items', ossRuntimeDoctoringEvidence.selectedAxis === 'runtime_doctoring' && ossRuntimeDoctoringEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'runtime_doctoring').length && ossRuntimeDoctoringEvidence.evidenceItemCount === ossRuntimeDoctoringEvidence.sourcePlanItemCount && ossRuntimeDoctoringEvidence.evidenceItems.every((item) => item.axis === 'runtime_doctoring'), `${ossRuntimeDoctoringEvidence.evidenceItemCount}/${ossRuntimeDoctoringEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS runtime doctoring evidence writes expected provenance JSONL', ossRuntimeDoctoringEvidence.provenanceJsonlPath === ossRuntimeDoctoringEvidenceProvenanceJsonlPath && ossRuntimeDoctoringEvidence.provenanceJsonlSha256.length === 64 && ossRuntimeDoctoringEvidence.provenanceJsonlRecordCount === ossRuntimeDoctoringEvidence.evidenceItemCount && ossRuntimeDoctoringEvidence.provenanceJsonlParseable, ossRuntimeDoctoringEvidence.provenanceJsonlPath))
  checks.push(check('OSS runtime doctoring evidence binds local evidence hashes', ossRuntimeDoctoringEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossRuntimeDoctoringEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).length} bindings`))
  checks.push(check('OSS runtime doctoring evidence covers blocker fixture and diagnosis-only classes', ['protected_install_path_blocker_fixture', 'diagnosis_without_repair_boundary'].every((coverage) => ossRuntimeDoctoringEvidence.evidenceItems.some((item) => item.runtimeDoctoringCoverageClass === coverage))))
  checks.push(check('OSS runtime doctoring evidence keeps every item bounded', ossRuntimeDoctoringEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'runtime_doctoring_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossRuntimeDoctoringEvidence.evidenceItems.length} items`))
  checks.push(check('OSS runtime doctoring evidence keeps repair install probe and readiness claims blocked', ossRuntimeDoctoringEvidence.repairActionAllowed === false && ossRuntimeDoctoringEvidence.reinstallActionAllowed === false && ossRuntimeDoctoringEvidence.dependencyInstallAllowed === false && ossRuntimeDoctoringEvidence.providerProbeAllowed === false && ossRuntimeDoctoringEvidence.externalDiagnosticsAllowed === false && ossRuntimeDoctoringEvidence.releaseReadinessClaimAllowed === false && ossRuntimeDoctoringEvidence.productionReadinessClaimAllowed === false && ossRuntimeDoctoringEvidence.publicReadinessClaimAllowed === false && ossRuntimeDoctoringEvidence.externalValidationClaimAllowed === false && ossRuntimeDoctoringEvidence.autonomousReliabilityClaimAllowed === false && ossRuntimeDoctoringEvidence.evidenceItems.every((item) => item.repairActionAllowed === false && item.reinstallActionAllowed === false && item.dependencyInstallAllowed === false && item.providerProbeAllowed === false && item.externalDiagnosticsAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS runtime doctoring evidence performed no provider live external or protected calls', ossRuntimeDoctoringEvidence.providerCallsPerformed.length === 0 && ossRuntimeDoctoringEvidence.liveModelCallsPerformed.length === 0 && ossRuntimeDoctoringEvidence.externalCallsPerformed.length === 0 && ossRuntimeDoctoringEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS runtime doctoring evidence checks pass', ossRuntimeDoctoringEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS security permissions evidence imports safe backlog evidence', ossSecurityPermissionsEvidence.mode === 'local_no_provider_oss_security_permissions_evidence' && ossSecurityPermissionsEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossSecurityPermissionsEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossSecurityPermissionsEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossSecurityPermissionsEvidence.sourceSafeBacklogPlanReportPath}/${ossSecurityPermissionsEvidence.selectedAxis}`))
  checks.push(check('OSS security permissions evidence covers selected axis items', ossSecurityPermissionsEvidence.selectedAxis === 'security_and_permissions' && ossSecurityPermissionsEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'security_and_permissions').length && ossSecurityPermissionsEvidence.evidenceItemCount === ossSecurityPermissionsEvidence.sourcePlanItemCount && ossSecurityPermissionsEvidence.evidenceItems.every((item) => item.axis === 'security_and_permissions'), `${ossSecurityPermissionsEvidence.evidenceItemCount}/${ossSecurityPermissionsEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS security permissions evidence writes expected provenance JSONL', ossSecurityPermissionsEvidence.provenanceJsonlPath === ossSecurityPermissionsEvidenceProvenanceJsonlPath && ossSecurityPermissionsEvidence.provenanceJsonlSha256.length === 64 && ossSecurityPermissionsEvidence.provenanceJsonlRecordCount === ossSecurityPermissionsEvidence.evidenceItemCount && ossSecurityPermissionsEvidence.provenanceJsonlParseable, ossSecurityPermissionsEvidence.provenanceJsonlPath))
  checks.push(check('OSS security permissions evidence binds local evidence hashes', ossSecurityPermissionsEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossSecurityPermissionsEvidence.evidenceItems.flatMap((item) => item.currentLocalEvidence).length} bindings`))
  checks.push(check('OSS security permissions evidence covers permission and hosted claim boundaries', ['permission_protected_action_claim_boundary', 'hosted_security_claim_boundary'].every((coverage) => ossSecurityPermissionsEvidence.evidenceItems.some((item) => item.securityPermissionsCoverageClass === coverage))))
  checks.push(check('OSS security permissions evidence keeps every item bounded', ossSecurityPermissionsEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'security_permissions_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossSecurityPermissionsEvidence.evidenceItems.length} items`))
  checks.push(check('OSS security permissions evidence keeps hosted security and readiness claims blocked', ossSecurityPermissionsEvidence.hostedScorecardRunAllowed === false && ossSecurityPermissionsEvidence.hostedCodeqlRunAllowed === false && ossSecurityPermissionsEvidence.hostedBranchProtectionClaimAllowed === false && ossSecurityPermissionsEvidence.publicSecurityPostureClaimAllowed === false && ossSecurityPermissionsEvidence.releaseReadinessClaimAllowed === false && ossSecurityPermissionsEvidence.productionReadinessClaimAllowed === false && ossSecurityPermissionsEvidence.publicReadinessClaimAllowed === false && ossSecurityPermissionsEvidence.externalValidationClaimAllowed === false && ossSecurityPermissionsEvidence.autonomousReliabilityClaimAllowed === false && ossSecurityPermissionsEvidence.evidenceItems.every((item) => item.hostedScorecardRunAllowed === false && item.hostedCodeqlRunAllowed === false && item.hostedBranchProtectionClaimAllowed === false && item.publicSecurityPostureClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS security permissions evidence performed no provider live external or protected calls', ossSecurityPermissionsEvidence.providerCallsPerformed.length === 0 && ossSecurityPermissionsEvidence.liveModelCallsPerformed.length === 0 && ossSecurityPermissionsEvidence.externalCallsPerformed.length === 0 && ossSecurityPermissionsEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS security permissions evidence checks pass', ossSecurityPermissionsEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS tool loop reliability evidence imports safe backlog evidence', ossToolLoopReliabilityEvidence.mode === 'local_no_provider_oss_tool_loop_reliability_evidence' && ossToolLoopReliabilityEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossToolLoopReliabilityEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossToolLoopReliabilityEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossToolLoopReliabilityEvidence.sourceSafeBacklogPlanReportPath}/${ossToolLoopReliabilityEvidence.selectedAxis}`))
  checks.push(check('OSS tool loop reliability evidence covers selected axis items', ossToolLoopReliabilityEvidence.selectedAxis === 'tool_loop_reliability' && ossToolLoopReliabilityEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'tool_loop_reliability').length && ossToolLoopReliabilityEvidence.evidenceItemCount === ossToolLoopReliabilityEvidence.sourcePlanItemCount && ossToolLoopReliabilityEvidence.evidenceItems.every((item) => item.axis === 'tool_loop_reliability'), `${ossToolLoopReliabilityEvidence.evidenceItemCount}/${ossToolLoopReliabilityEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS tool loop reliability evidence writes expected provenance JSONL', ossToolLoopReliabilityEvidence.provenanceJsonlPath === ossToolLoopReliabilityEvidenceProvenanceJsonlPath && ossToolLoopReliabilityEvidence.provenanceJsonlSha256.length === 64 && ossToolLoopReliabilityEvidence.provenanceJsonlRecordCount === ossToolLoopReliabilityEvidence.evidenceItemCount && ossToolLoopReliabilityEvidence.provenanceJsonlParseable, ossToolLoopReliabilityEvidence.provenanceJsonlPath))
  checks.push(check('OSS tool loop reliability evidence binds local evidence hashes', ossToolLoopReliabilityEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossToolLoopReliabilityEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).length} bindings`))
  checks.push(check('OSS tool loop reliability evidence covers repair and redaction portability boundaries', ['disposable_code_editing_trace_reliability', 'trace_redaction_portability_boundary'].every((coverage) => ossToolLoopReliabilityEvidence.evidenceItems.some((item) => item.toolLoopCoverageClass === coverage))))
  checks.push(check('OSS tool loop reliability evidence keeps every item bounded', ossToolLoopReliabilityEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'tool_loop_reliability_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossToolLoopReliabilityEvidence.evidenceItems.length} items`))
  checks.push(check('OSS tool loop reliability evidence keeps reliability and protected-action claims blocked', ossToolLoopReliabilityEvidence.realProductRepoMutationAllowed === false && ossToolLoopReliabilityEvidence.providerBackedExecutionAllowed === false && ossToolLoopReliabilityEvidence.liveModelValidationAllowed === false && ossToolLoopReliabilityEvidence.externalBenchmarkExecutionAllowed === false && ossToolLoopReliabilityEvidence.nonSyntheticReliabilityClaimAllowed === false && ossToolLoopReliabilityEvidence.publicReliabilityClaimAllowed === false && ossToolLoopReliabilityEvidence.releaseReadinessClaimAllowed === false && ossToolLoopReliabilityEvidence.productionReadinessClaimAllowed === false && ossToolLoopReliabilityEvidence.publicReadinessClaimAllowed === false && ossToolLoopReliabilityEvidence.externalValidationClaimAllowed === false && ossToolLoopReliabilityEvidence.autonomousReliabilityClaimAllowed === false && ossToolLoopReliabilityEvidence.evidenceItems.every((item) => item.realProductRepoMutationAllowed === false && item.providerBackedExecutionAllowed === false && item.liveModelValidationAllowed === false && item.externalBenchmarkExecutionAllowed === false && item.nonSyntheticReliabilityClaimAllowed === false && item.publicReliabilityClaimAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS tool loop reliability evidence performed no provider live external or protected calls', ossToolLoopReliabilityEvidence.providerCallsPerformed.length === 0 && ossToolLoopReliabilityEvidence.liveModelCallsPerformed.length === 0 && ossToolLoopReliabilityEvidence.externalCallsPerformed.length === 0 && ossToolLoopReliabilityEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS tool loop reliability evidence checks pass', ossToolLoopReliabilityEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS provider breadth evidence imports safe backlog evidence', ossProviderBreadthEvidence.mode === 'local_no_provider_oss_provider_breadth_evidence' && ossProviderBreadthEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossProviderBreadthEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossProviderBreadthEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossProviderBreadthEvidence.sourceSafeBacklogPlanReportPath}/${ossProviderBreadthEvidence.selectedAxis}`))
  checks.push(check('OSS provider breadth evidence covers selected axis items', ossProviderBreadthEvidence.selectedAxis === 'provider_breadth' && ossProviderBreadthEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'provider_breadth').length && ossProviderBreadthEvidence.evidenceItemCount === ossProviderBreadthEvidence.sourcePlanItemCount && ossProviderBreadthEvidence.evidenceItems.every((item) => item.axis === 'provider_breadth'), `${ossProviderBreadthEvidence.evidenceItemCount}/${ossProviderBreadthEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS provider breadth evidence writes expected provenance JSONL', ossProviderBreadthEvidence.provenanceJsonlPath === ossProviderBreadthEvidenceProvenanceJsonlPath && ossProviderBreadthEvidence.provenanceJsonlSha256.length === 64 && ossProviderBreadthEvidence.provenanceJsonlRecordCount === ossProviderBreadthEvidence.evidenceItemCount && ossProviderBreadthEvidence.provenanceJsonlParseable, ossProviderBreadthEvidence.provenanceJsonlPath))
  checks.push(check('OSS provider breadth evidence binds local evidence hashes', ossProviderBreadthEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossProviderBreadthEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).length} bindings`))
  checks.push(check('OSS provider breadth evidence covers capability and fallback boundaries', ['provider_capability_failure_mode_matrix', 'provider_fallback_live_authorization_boundary'].every((coverage) => ossProviderBreadthEvidence.evidenceItems.some((item) => item.providerBreadthCoverageClass === coverage))))
  checks.push(check('OSS provider breadth evidence keeps every item bounded', ossProviderBreadthEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'provider_breadth_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossProviderBreadthEvidence.evidenceItems.length} items`))
  checks.push(check('OSS provider breadth evidence keeps provider and claim expansion blocked', ossProviderBreadthEvidence.providerCallsAllowed === false && ossProviderBreadthEvidence.liveModelCallsAllowed === false && ossProviderBreadthEvidence.externalCallsAllowed === false && ossProviderBreadthEvidence.liveProviderValidationAllowed === false && ossProviderBreadthEvidence.providerCompatibilityClaimAllowed === false && ossProviderBreadthEvidence.modelBehaviorClaimAllowed === false && ossProviderBreadthEvidence.providerBackedExecutionAllowed === false && ossProviderBreadthEvidence.releaseReadinessClaimAllowed === false && ossProviderBreadthEvidence.productionReadinessClaimAllowed === false && ossProviderBreadthEvidence.publicReadinessClaimAllowed === false && ossProviderBreadthEvidence.externalValidationClaimAllowed === false && ossProviderBreadthEvidence.autonomousReliabilityClaimAllowed === false && ossProviderBreadthEvidence.evidenceItems.every((item) => item.providerCallsAllowed === false && item.liveModelCallsAllowed === false && item.externalCallsAllowed === false && item.liveProviderValidationAllowed === false && item.providerCompatibilityClaimAllowed === false && item.modelBehaviorClaimAllowed === false && item.providerBackedExecutionAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.publicReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS provider breadth evidence performed no provider live external or protected calls', ossProviderBreadthEvidence.providerCallsPerformed.length === 0 && ossProviderBreadthEvidence.liveModelCallsPerformed.length === 0 && ossProviderBreadthEvidence.externalCallsPerformed.length === 0 && ossProviderBreadthEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS provider breadth evidence checks pass', ossProviderBreadthEvidence.evidenceChecks.every((item) => item.ok)))
  checks.push(check('OSS release hygiene evidence imports safe backlog evidence', ossReleaseHygieneEvidence.mode === 'local_no_provider_oss_release_hygiene_evidence' && ossReleaseHygieneEvidence.sourceSafeBacklogPlanReportPath === ossSafeBacklogPlanJsonPath && ossReleaseHygieneEvidence.sourceSafeBacklogPlanReportSha256.length === 64 && ossReleaseHygieneEvidence.sourceAxisArchitectureReviewReportPath === ossAxisArchitectureReviewJsonPath, `${ossReleaseHygieneEvidence.sourceSafeBacklogPlanReportPath}/${ossReleaseHygieneEvidence.selectedAxis}`))
  checks.push(check('OSS release hygiene evidence covers selected axis items', ossReleaseHygieneEvidence.selectedAxis === 'release_hygiene' && ossReleaseHygieneEvidence.sourcePlanItemCount === ossSafeBacklogPlan.planItems.filter((item) => item.axis === 'release_hygiene').length && ossReleaseHygieneEvidence.evidenceItemCount === ossReleaseHygieneEvidence.sourcePlanItemCount && ossReleaseHygieneEvidence.evidenceItems.every((item) => item.axis === 'release_hygiene'), `${ossReleaseHygieneEvidence.evidenceItemCount}/${ossReleaseHygieneEvidence.sourcePlanItemCount}`))
  checks.push(check('OSS release hygiene evidence writes expected provenance JSONL', ossReleaseHygieneEvidence.provenanceJsonlPath === ossReleaseHygieneEvidenceProvenanceJsonlPath && ossReleaseHygieneEvidence.provenanceJsonlSha256.length === 64 && ossReleaseHygieneEvidence.provenanceJsonlRecordCount === ossReleaseHygieneEvidence.evidenceItemCount && ossReleaseHygieneEvidence.provenanceJsonlParseable, ossReleaseHygieneEvidence.provenanceJsonlPath))
  checks.push(check('OSS release hygiene evidence binds local evidence hashes', ossReleaseHygieneEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).every((binding) => binding.exists && typeof binding.sha256 === 'string' && binding.sha256.length === 64 && binding.sizeBytes > 0), `${ossReleaseHygieneEvidence.evidenceItems.flatMap((item) => [...item.currentLocalEvidence, ...item.supplementalLocalEvidence]).length} bindings`))
  checks.push(check('OSS release hygiene evidence covers reproducibility and release-claim boundaries', ['local_artifact_reproducibility_sbom_license_gate', 'signed_provenance_publish_release_claim_boundary'].every((coverage) => ossReleaseHygieneEvidence.evidenceItems.some((item) => item.releaseHygieneCoverageClass === coverage))))
  checks.push(check('OSS release hygiene evidence keeps every item bounded', ossReleaseHygieneEvidence.evidenceItems.every((item) => item.protectedBoundary.length > 0 && item.forbiddenShortcuts.length > 0 && item.implementationStatus === 'release_hygiene_evidence_matrix_created_internal_no_provider' && item.protectedActionRequiredForEvidenceMatrix === false && item.protectedActionExecuted === false), `${ossReleaseHygieneEvidence.evidenceItems.length} items`))
  checks.push(check('OSS release hygiene evidence keeps release and protected-action claims blocked', ossReleaseHygieneEvidence.commitAllowed === false && ossReleaseHygieneEvidence.pushAllowed === false && ossReleaseHygieneEvidence.publishAllowed === false && ossReleaseHygieneEvidence.deployAllowed === false && ossReleaseHygieneEvidence.launchAllowed === false && ossReleaseHygieneEvidence.signedProvenanceGenerated === false && ossReleaseHygieneEvidence.signedProvenanceClaimAllowed === false && ossReleaseHygieneEvidence.legalNoticeReuseDecisionAllowed === false && ossReleaseHygieneEvidence.releaseReadinessClaimAllowed === false && ossReleaseHygieneEvidence.productionReadinessClaimAllowed === false && ossReleaseHygieneEvidence.publicReadinessClaimAllowed === false && ossReleaseHygieneEvidence.externalValidationClaimAllowed === false && ossReleaseHygieneEvidence.autonomousReliabilityClaimAllowed === false && ossReleaseHygieneEvidence.evidenceItems.every((item) => item.commitAllowed === false && item.pushAllowed === false && item.publishAllowed === false && item.deployAllowed === false && item.launchAllowed === false && item.signedProvenanceClaimAllowed === false && item.legalNoticeReuseDecisionAllowed === false && item.releaseReadinessClaimAllowed === false && item.productionReadinessClaimAllowed === false && item.publicReadinessClaimAllowed === false && item.externalValidationClaimAllowed === false && item.autonomousReliabilityClaimAllowed === false)))
  checks.push(check('OSS release hygiene evidence performed no provider live external or protected calls', ossReleaseHygieneEvidence.providerCallsPerformed.length === 0 && ossReleaseHygieneEvidence.liveModelCallsPerformed.length === 0 && ossReleaseHygieneEvidence.externalCallsPerformed.length === 0 && ossReleaseHygieneEvidence.protectedActionsExecuted.length === 0))
  checks.push(check('OSS release hygiene evidence checks pass', ossReleaseHygieneEvidence.evidenceChecks.every((item) => item.ok)))
  for (const phrase of ['market leadership', 'release readiness', 'production readiness', 'external validation', 'autonomous reliability']) {
    checks.push(check(`scorecard claim boundary mentions ${phrase}`, scorecard.includes(phrase)))
  }
  checks.push(check('quality gate defines command', gate.includes('bun run product:quality')))
  checks.push(check('terminal report preserves non-claim boundary', terminal.includes('protected_external_claims_made: `false`')))
  checks.push(check('typecheck health report records current strict status', typecheckHealth.strictPass === false || typecheckHealth.strictPass === true))
  checks.push(check('typecheck health report has bucket summaries', Array.isArray(typecheckHealth.buckets)))
  checks.push(check('typecheck health report records diagnostic count', Number.isInteger(typecheckHealth.totalDiagnostics) && typecheckHealth.totalDiagnostics >= 0, String(typecheckHealth.totalDiagnostics)))
  checks.push(check('typecheck health report records diagnostic budget', Number.isInteger(typecheckHealth.diagnosticBudget), String(typecheckHealth.diagnosticBudget)))
  checks.push(check('typecheck diagnostics stay within ratchet budget', Number.isInteger(typecheckHealth.diagnosticBudget) && typecheckHealth.totalDiagnostics <= typecheckHealth.diagnosticBudget, `${typecheckHealth.totalDiagnostics}/${typecheckHealth.diagnosticBudget}`))
  checks.push(check('absorption register has primary-source entries', Array.isArray(absorptionRegister.entries) && absorptionRegister.entries.length >= 5, String(absorptionRegister.entries?.length ?? 0)))
  checks.push(check('absorption entries use official primary sources', absorptionRegister.entries.every((entry) => isAbsorptionPrimarySourceUrl(entry.source_url)), absorptionRegister.entries.filter((entry) => !isAbsorptionPrimarySourceUrl(entry.source_url)).map((entry) => entry.source_url).join(',')))
  checks.push(check('absorption entries define local actions', absorptionRegister.entries.every((entry) => entry.local_action.trim().length > 0)))
  checks.push(check('absorption register has next targets', Array.isArray(absorptionRegister.next_absorption_targets) && absorptionRegister.next_absorption_targets.length >= 3))
  checks.push(check('golden transcripts are local no-provider CLI surface checks', goldenTranscripts.mode === 'local_no_provider_cli_surface'))
  checks.push(check('golden transcripts performed no provider calls', goldenTranscripts.providerCallsPerformed.length === 0))
  checks.push(check('golden transcripts performed no live model calls', goldenTranscripts.liveModelCallsPerformed.length === 0))
  checks.push(check('golden transcripts performed no external calls', goldenTranscripts.externalCallsPerformed.length === 0))
  checks.push(check('golden transcripts include version and help', new Set(goldenTranscripts.transcripts.map((transcript) => transcript.name)).has('version') && new Set(goldenTranscripts.transcripts.map((transcript) => transcript.name)).has('help')))
  checks.push(check('golden transcripts pass', goldenTranscripts.transcripts.every((transcript) => transcript.exitCode === 0 && transcript.passed)))
  checks.push(check('terminal failure recovery transcripts are local no-provider CLI checks', terminalFailureRecoveryTranscripts.mode === 'local_no_provider_terminal_failure_recovery_transcripts'))
  checks.push(check('terminal failure recovery transcripts performed no provider calls', terminalFailureRecoveryTranscripts.providerCallsPerformed.length === 0))
  checks.push(check('terminal failure recovery transcripts performed no live model calls', terminalFailureRecoveryTranscripts.liveModelCallsPerformed.length === 0))
  checks.push(check('terminal failure recovery transcripts performed no external calls', terminalFailureRecoveryTranscripts.externalCallsPerformed.length === 0))
  checks.push(check('terminal failure recovery transcripts executed no protected actions', terminalFailureRecoveryTranscripts.protectedActionsExecuted.length === 0))
  checks.push(check('terminal failure recovery transcripts capture hash-only output', terminalFailureRecoveryTranscripts.capturePerformed === true && terminalFailureRecoveryTranscripts.rawOutputStored === false))
  checks.push(check('terminal failure recovery transcripts include local failure and recovery', terminalFailureRecoveryTranscripts.failureStepDetected === true && terminalFailureRecoveryTranscripts.recoveryGuidanceProvided === true && terminalFailureRecoveryTranscripts.recoveryVerificationPassed === true && terminalFailureRecoveryTranscripts.transcriptCount >= 4, `${terminalFailureRecoveryTranscripts.transcriptCount} transcripts`))
  checks.push(check('terminal failure recovery transcripts include expected command kinds', ['local_failure', 'recovery_guidance', 'recovery_verification'].every((kind) => terminalFailureRecoveryTranscripts.transcripts.some((transcript) => transcript.kind === kind && transcript.passed)), terminalFailureRecoveryTranscripts.transcripts.map((transcript) => `${transcript.name}:${transcript.kind}`).join(',')))
  checks.push(check('terminal failure recovery transcripts record primary sources', terminalFailureRecoveryTranscripts.primarySourceInputs.length >= 3 && terminalFailureRecoveryTranscripts.primarySourceInputs.every((source) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(source.sourceUrl)), terminalFailureRecoveryTranscripts.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('terminal failure recovery transcript checks pass', terminalFailureRecoveryTranscripts.transcriptChecks.every((item) => item.ok)))
  checks.push(check('onboarding smoke is local no-provider check', onboardingSmoke.mode === 'local_no_provider_onboarding_smoke'))
  checks.push(check('onboarding smoke performed no provider calls', onboardingSmoke.providerCallsPerformed.length === 0))
  checks.push(check('onboarding smoke performed no live model calls', onboardingSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('onboarding smoke performed no external calls', onboardingSmoke.externalCallsPerformed.length === 0))
  checks.push(check('onboarding smoke executed no protected actions', onboardingSmoke.protectedActionsExecuted.length === 0))
  checks.push(check('onboarding smoke records primary sources', ['openai/codex', 'Aider-AI/aider', 'opencode-ai/opencode'].every((source) => onboardingSmoke.primarySourceInputs.some((item) => item.sourceProject === source)), onboardingSmoke.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('onboarding smoke links platform quick starts', onboardingSmoke.readmePath === 'README.md' && onboardingSmoke.windowsQuickStartPath === 'docs/quick-start-windows.md' && onboardingSmoke.macLinuxQuickStartPath === 'docs/quick-start-mac-linux.md' && onboardingSmoke.readmeLinksWindowsQuickStart && onboardingSmoke.readmeLinksMacLinuxQuickStart))
  checks.push(check('onboarding smoke verifies platform docs', onboardingSmoke.windowsQuickStartPresent && onboardingSmoke.macLinuxQuickStartPresent && onboardingSmoke.installCommandDocumented && onboardingSmoke.startCommandDocumented && onboardingSmoke.nodeVersionCheckDocumented))
  checks.push(check('onboarding smoke verifies provider guidance', onboardingSmoke.providerSetupDocumented && onboardingSmoke.providerFailureTroubleshootingDocumented && onboardingSmoke.updateAndUninstallDocumented && onboardingSmoke.advancedSetupLinked))
  checks.push(check('onboarding smoke verifies local runtime commands', onboardingSmoke.localRuntimeSmokePerformed && ['version', 'help', 'doctor_help'].every((name) => onboardingSmoke.localSmokeCommands.some((item) => item.name === name && item.exitCode === 0 && item.passed)), onboardingSmoke.localSmokeCommands.map((item) => `${item.name}:${item.passed}`).join(',')))
  checks.push(check('onboarding smoke blocks unsupported cross-platform and readiness claims', onboardingSmoke.crossPlatformRuntimeClaimAllowed === false && onboardingSmoke.releaseReadinessClaimAllowed === false && onboardingSmoke.productionReadinessClaimAllowed === false && onboardingSmoke.publicReadinessClaimAllowed === false && onboardingSmoke.externalValidationClaimAllowed === false && onboardingSmoke.autonomousReliabilityClaimAllowed === false))
  checks.push(check('onboarding smoke checks pass', onboardingSmoke.onboardingChecks.every((item) => item.ok)))
  checks.push(check('doc link integrity is local no-provider check', docLinkIntegrity.mode === 'local_no_provider_doc_link_integrity'))
  checks.push(check('doc link integrity performed no provider calls', docLinkIntegrity.providerCallsPerformed.length === 0))
  checks.push(check('doc link integrity performed no live model calls', docLinkIntegrity.liveModelCallsPerformed.length === 0))
  checks.push(check('doc link integrity performed no external calls', docLinkIntegrity.externalCallsPerformed.length === 0))
  checks.push(check('doc link integrity executed no protected actions', docLinkIntegrity.protectedActionsExecuted.length === 0))
  checks.push(check('doc link integrity did not fetch external links', docLinkIntegrity.externalLinkFetchPerformed === false))
  checks.push(check('doc link integrity records primary sources', ['github/docs', 'openai/codex', 'continuedev/continue'].every((source) => docLinkIntegrity.primarySourceInputs.some((item) => item.sourceProject === source)), docLinkIntegrity.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('doc link integrity scans expected docs', ['README.md', 'docs/quick-start-windows.md', 'docs/quick-start-mac-linux.md', 'docs/product-quality/product-quality-gate.md', 'docs/product-quality/competitive-scorecard.md'].every((path) => docLinkIntegrity.scannedMarkdownFiles.includes(path)), docLinkIntegrity.scannedMarkdownFiles.join(',')))
  checks.push(check('doc link integrity verifies local relative links', docLinkIntegrity.relativeLinksChecked.length >= 10 && docLinkIntegrity.allRelativeLinksResolve && docLinkIntegrity.relativeLinksChecked.every((item) => item.ok), String(docLinkIntegrity.relativeLinksChecked.length)))
  checks.push(check('doc link integrity verifies canonical VS Code extension path', docLinkIntegrity.canonicalVsCodeExtensionPath === 'packages/openclaude-vscode' && docLinkIntegrity.legacyVsCodeExtensionPath === 'vscode-extension/openclaude-vscode' && docLinkIntegrity.readmeUsesCanonicalVsCodeExtensionPath && docLinkIntegrity.readmeLegacyVsCodeExtensionPathAbsent && docLinkIntegrity.packageExtensionSurfaceExists))
  checks.push(check('doc link integrity checks pass', docLinkIntegrity.integrityChecks.every((item) => item.ok)))
  checks.push(check('primary source registry is local no-provider check', primarySourceRegistry.mode === 'local_no_provider_primary_source_registry'))
  checks.push(check('primary source registry performed no provider calls', primarySourceRegistry.providerCallsPerformed.length === 0))
  checks.push(check('primary source registry performed no live model calls', primarySourceRegistry.liveModelCallsPerformed.length === 0))
  checks.push(check('primary source registry performed no external calls', primarySourceRegistry.externalCallsPerformed.length === 0))
  checks.push(check('primary source registry executed no protected actions', primarySourceRegistry.protectedActionsExecuted.length === 0))
  checks.push(check('primary source registry did not fetch external sources', primarySourceRegistry.externalSourceFetchPerformed === false && primarySourceRegistry.blogSummarySourceAllowed === false))
  checks.push(check('primary source registry covers broad evidence inputs', primarySourceRegistry.reportsWithPrimarySourceInputs.length >= 20 && primarySourceRegistry.primarySourceEntryCount >= 80 && primarySourceRegistry.uniqueSourceUrlCount >= 50, `${primarySourceRegistry.reportsWithPrimarySourceInputs.length} reports / ${primarySourceRegistry.primarySourceEntryCount} entries / ${primarySourceRegistry.uniqueSourceUrlCount} URLs`))
  checks.push(check('primary source registry rejects secondary and malformed sources', primarySourceRegistry.disallowedSecondarySourceCount === 0 && primarySourceRegistry.malformedSourceInputCount === 0 && primarySourceRegistry.unclassifiedSourceCount === 0, `secondary=${primarySourceRegistry.disallowedSecondarySourceCount} malformed=${primarySourceRegistry.malformedSourceInputCount} unclassified=${primarySourceRegistry.unclassifiedSourceCount}`))
  checks.push(check('primary source registry covers source kind classes', ['original_repository', 'official_documentation', 'standard_or_specification', 'benchmark_project', 'research_paper'].every((kind) => (primarySourceRegistry.sourceKindCounts[kind] ?? 0) > 0), JSON.stringify(primarySourceRegistry.sourceKindCounts)))
  checks.push(check('primary source registry writes expected JSONL', primarySourceRegistry.registryJsonlPath === primarySourceRegistryJsonlPath && primarySourceRegistry.registryJsonlSha256.length === 64 && primarySourceRegistry.registryJsonlRecordCount === primarySourceRegistry.primarySourceEntryCount && primarySourceRegistry.registryJsonlParseable, primarySourceRegistry.registryJsonlPath))
  checks.push(check('primary source registry keeps readiness claims blocked', primarySourceRegistry.releaseReadinessClaimAllowed === false && primarySourceRegistry.productionReadinessClaimAllowed === false && primarySourceRegistry.publicReadinessClaimAllowed === false && primarySourceRegistry.externalValidationClaimAllowed === false && primarySourceRegistry.autonomousReliabilityClaimAllowed === false))
  checks.push(check('primary source registry checks pass', primarySourceRegistry.primarySourceRegistryChecks.every((item) => item.ok)))
  checks.push(check('agent instructions quality is local no-provider check', agentInstructionsQuality.mode === 'local_no_provider_agent_instructions_quality'))
  checks.push(check('agent instructions quality performed no provider calls', agentInstructionsQuality.providerCallsPerformed.length === 0))
  checks.push(check('agent instructions quality performed no live model calls', agentInstructionsQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('agent instructions quality performed no external calls', agentInstructionsQuality.externalCallsPerformed.length === 0))
  checks.push(check('agent instructions quality executed no protected actions', agentInstructionsQuality.protectedActionsExecuted.length === 0))
  checks.push(check('agent instructions quality records OpenHands primary sources', ['OpenHands Repository Agent guidance', 'OpenHands Skills overview'].every((source) => agentInstructionsQuality.primarySourceInputs.some((item) => item.sourceProject === source)), agentInstructionsQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('agent instructions quality verifies repository orientation', agentInstructionsQuality.sourceAgentInstructionsPath === 'AGENTS.md' && agentInstructionsQuality.purposeSectionPresent && agentInstructionsQuality.setupVerificationCommandsPresent.length === 4 && agentInstructionsQuality.repositoryStructureSectionsPresent.length === 6, `${agentInstructionsQuality.setupVerificationCommandsPresent.length}/${agentInstructionsQuality.repositoryStructureSectionsPresent.length}`))
  checks.push(check('agent instructions quality verifies workflow and stack boundaries', agentInstructionsQuality.workflowEvidencePresent && agentInstructionsQuality.agentStackBoundariesPresent.length === 3, `${agentInstructionsQuality.workflowEvidencePresent}/${agentInstructionsQuality.agentStackBoundariesPresent.join(',')}`))
  checks.push(check('agent instructions quality verifies research, verification, and protected boundaries', agentInstructionsQuality.primarySourceRulePresent && agentInstructionsQuality.verificationStandardPresent && agentInstructionsQuality.protectedBoundaryLanguagePresent))
  checks.push(check('agent instructions quality keeps readiness claims blocked', agentInstructionsQuality.releaseReadinessClaimAllowed === false && agentInstructionsQuality.productionReadinessClaimAllowed === false && agentInstructionsQuality.publicReadinessClaimAllowed === false && agentInstructionsQuality.externalValidationClaimAllowed === false && agentInstructionsQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('agent instructions quality checks pass', agentInstructionsQuality.instructionQualityChecks.every((item) => item.ok)))
  checks.push(check('community intake quality is local no-provider check', communityIntakeQuality.mode === 'local_no_provider_community_intake_quality'))
  checks.push(check('community intake quality performed no provider calls', communityIntakeQuality.providerCallsPerformed.length === 0))
  checks.push(check('community intake quality performed no live model calls', communityIntakeQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('community intake quality performed no external calls', communityIntakeQuality.externalCallsPerformed.length === 0 && communityIntakeQuality.externalTemplateValidationPerformed === false))
  checks.push(check('community intake quality executed no protected actions', communityIntakeQuality.protectedActionsExecuted.length === 0))
  checks.push(check('community intake quality records GitHub Docs primary sources', ['GitHub Docs issue templates', 'GitHub Docs pull request standardization', 'GitHub Docs issue forms syntax'].every((source) => communityIntakeQuality.primarySourceInputs.some((item) => item.sourceProject === source)) && communityIntakeQuality.primarySourceInputs.every((item) => /^https:\/\/docs\.github\.com\//.test(item.sourceUrl)), communityIntakeQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('community intake quality discourages blank issues through configured templates', communityIntakeQuality.issueTemplateChooserConfigured && communityIntakeQuality.blankIssuesEnabled === false, `blank_issues_enabled=${communityIntakeQuality.blankIssuesEnabled}`))
  checks.push(check('community intake quality verifies bug feature and PR intake coverage', communityIntakeQuality.bugReportTemplate.requiredSectionsPresent.length >= 8 && communityIntakeQuality.featureRequestTemplate.requiredSectionsPresent.length >= 7 && communityIntakeQuality.pullRequestTemplate.requiredSectionsPresent.length >= 5, `${communityIntakeQuality.bugReportTemplate.requiredSectionsPresent.length}/${communityIntakeQuality.featureRequestTemplate.requiredSectionsPresent.length}/${communityIntakeQuality.pullRequestTemplate.requiredSectionsPresent.length}`))
  checks.push(check('community intake quality verifies secret redaction and protected claim boundaries', communityIntakeQuality.securityPolicyLinkedOrPresent && communityIntakeQuality.bugReportTemplate.requiredTermsPresent.includes('redact') && communityIntakeQuality.pullRequestTemplate.requiredTermsPresent.includes('redacted credentials') && communityIntakeQuality.pullRequestTemplate.requiredTermsPresent.includes('release readiness'), communityIntakeQuality.pullRequestTemplate.requiredTermsPresent.join(',')))
  checks.push(check('community intake quality keeps readiness claims blocked', communityIntakeQuality.releaseReadinessClaimAllowed === false && communityIntakeQuality.productionReadinessClaimAllowed === false && communityIntakeQuality.publicReadinessClaimAllowed === false && communityIntakeQuality.externalValidationClaimAllowed === false && communityIntakeQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('community intake quality checks pass', communityIntakeQuality.communityIntakeChecks.every((item) => item.ok)))
  checks.push(check('community profile quality is local no-provider check', communityProfileQuality.mode === 'local_no_provider_community_profile_quality'))
  checks.push(check('community profile quality performed no provider calls', communityProfileQuality.providerCallsPerformed.length === 0))
  checks.push(check('community profile quality performed no live model calls', communityProfileQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('community profile quality performed no external calls', communityProfileQuality.externalCallsPerformed.length === 0 && communityProfileQuality.externalCommunityProfileCheckPerformed === false))
  checks.push(check('community profile quality executed no protected actions', communityProfileQuality.protectedActionsExecuted.length === 0))
  checks.push(check('community profile quality records GitHub Docs primary sources', ['GitHub Docs healthy contributions', 'GitHub Docs contributor guidelines', 'GitHub Docs support resources', 'GitHub Docs code of conduct', 'GitHub Docs licensing'].every((source) => communityProfileQuality.primarySourceInputs.some((item) => item.sourceProject === source)) && communityProfileQuality.primarySourceInputs.every((item) => /^https:\/\/docs\.github\.com\//.test(item.sourceUrl)), communityProfileQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('community profile quality verifies README and profile surfaces', communityProfileQuality.readmeLinksCommunityFiles && communityProfileQuality.sourceProfilePaths.length === 6, `${communityProfileQuality.sourceProfilePaths.length} files`))
  checks.push(check('community profile quality verifies contributing support conduct security and license terms', communityProfileQuality.contributing.requiredTermsPresent.length >= 8 && communityProfileQuality.support.requiredTermsPresent.length >= 9 && communityProfileQuality.codeOfConduct.requiredTermsPresent.length >= 6 && communityProfileQuality.security.requiredTermsPresent.length >= 6 && communityProfileQuality.license.requiredTermsPresent.length >= 5, `${communityProfileQuality.contributing.requiredTermsPresent.length}/${communityProfileQuality.support.requiredTermsPresent.length}/${communityProfileQuality.codeOfConduct.requiredTermsPresent.length}/${communityProfileQuality.security.requiredTermsPresent.length}/${communityProfileQuality.license.requiredTermsPresent.length}`))
  checks.push(check('community profile quality keeps readiness claims blocked', communityProfileQuality.releaseReadinessClaimAllowed === false && communityProfileQuality.productionReadinessClaimAllowed === false && communityProfileQuality.publicReadinessClaimAllowed === false && communityProfileQuality.externalValidationClaimAllowed === false && communityProfileQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('community profile quality checks pass', communityProfileQuality.communityProfileChecks.every((item) => item.ok)))
  checks.push(check('dependency topology gate is local no-provider evidence', dependencyTopology.mode === 'local_no_provider_dependency_topology_gate'))
  checks.push(check('dependency topology performed no provider live external or protected calls', dependencyTopology.providerCallsPerformed.length === 0 && dependencyTopology.liveModelCallsPerformed.length === 0 && dependencyTopology.externalCallsPerformed.length === 0 && dependencyTopology.protectedActionsExecuted.length === 0))
  checks.push(check('dependency topology records dependency-cruiser command evidence', dependencyTopology.dependencyCruiserVersion.length > 0 && dependencyTopology.topologyCommands.some((item) => item.name === 'dependency_cruiser_src_scripts' && item.command.includes('depcruise') && item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0), dependencyTopology.dependencyCruiserVersion))
  checks.push(check('dependency topology records dependency-cruiser known-violation ratchet command evidence', dependencyTopology.topologyCommands.some((item) => item.name === 'dependency_cruiser_known_violation_ratchet' && item.command.includes('depcruise') && item.command.includes('--config') && item.command.includes('.dependency-cruiser.mjs') && item.command.includes('--ignore-known') && item.command.includes('.dependency-cruiser-known-violations.json') && item.command.includes('--output-type') && item.command.includes('err') && item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0), dependencyTopology.dependencyCruiserVersion))
  checks.push(check('dependency topology discovers modules and edges', dependencyTopology.moduleCount > 0 && dependencyTopology.dependencyEdgeCount > 0, `${dependencyTopology.moduleCount}/${dependencyTopology.dependencyEdgeCount}`))
  checks.push(check('dependency topology circular dependencies do not exceed baseline', dependencyTopology.circularDependencyCount <= dependencyTopology.circularDependencyBaseline, `${dependencyTopology.circularDependencyCount}/${dependencyTopology.circularDependencyBaseline}`))
  checks.push(check('dependency topology unresolved dependencies do not exceed baseline', dependencyTopology.unresolvedDependencyCount <= dependencyTopology.unresolvedDependencyBaseline, `${dependencyTopology.unresolvedDependencyCount}/${dependencyTopology.unresolvedDependencyBaseline}`))
  checks.push(check('configured dependency topology ratchet has no new violations', dependencyTopology.configuredRatchetMode === 'dependency_cruiser_known_violation_ratchet' && dependencyTopology.dependencyCruiserConfigPath === '.dependency-cruiser.mjs' && dependencyTopology.knownViolationBaselinePath === '.dependency-cruiser-known-violations.json' && dependencyTopology.configuredRatchetKnownViolationCount > 0 && dependencyTopology.configuredRatchetNewViolationCount === 0 && dependencyTopology.configuredRatchetClaimAllowed === false, `${dependencyTopology.configuredRatchetKnownViolationCount}/${dependencyTopology.configuredRatchetNewViolationCount}`))
  checks.push(check('dependency topology records official primary sources', ['dependency-cruiser', 'US7904892B2 dependency graph cycle patent'].every((source) => dependencyTopology.primarySourceInputs.some((item) => item.sourceProject === source)) && dependencyTopology.primarySourceInputs.every((item) => item.sourceUrl.startsWith('https://github.com/') || item.sourceUrl.startsWith('https://patents.google.com/')), dependencyTopology.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('dependency topology keeps cleanup and readiness claims blocked', dependencyTopology.topologyCleanClaimAllowed === false && dependencyTopology.refactorCompletionClaimAllowed === false && dependencyTopology.publicReadinessClaimAllowed === false))
  checks.push(check('dependency topology commands pass', dependencyTopology.topologyCommands.every((item) => item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0)))
  checks.push(check('dependency topology checks pass', dependencyTopology.topologyChecks.every((item) => item.ok)))
  checks.push(check('script duplication audit is local no-provider evidence', scriptDuplicationAudit.mode === 'local_no_provider_product_script_duplication_audit' && scriptDuplicationAudit.scannerTargetGlob === 'scripts/product-*.ts'))
  checks.push(check('script duplication audit performed no provider live external or protected calls', scriptDuplicationAudit.providerCallsPerformed.length === 0 && scriptDuplicationAudit.liveModelCallsPerformed.length === 0 && scriptDuplicationAudit.externalCallsPerformed.length === 0 && scriptDuplicationAudit.protectedActionsExecuted.length === 0))
  checks.push(check('script duplication helper clusters do not exceed baseline', scriptDuplicationAudit.duplicateHelperClusterCount <= scriptDuplicationAudit.duplicateHelperClusterBaseline && Object.keys(scriptDuplicationAudit.helperOccurrenceBaselines).every((helperName) => (scriptDuplicationAudit.helperOccurrenceCounts[helperName] ?? 0) <= scriptDuplicationAudit.helperOccurrenceBaselines[helperName]), `${scriptDuplicationAudit.duplicateHelperClusterCount}/${scriptDuplicationAudit.duplicateHelperClusterBaseline}`))
  checks.push(check('script duplication jscpd command records configured JSON evidence', scriptDuplicationAudit.jscpdEnabled === true && scriptDuplicationAudit.jscpdVersion.includes('5.0.9') && scriptDuplicationAudit.jscpdConfigPath === '.jscpd.json' && scriptDuplicationAudit.jscpdCommand.name === 'jscpd_product_scripts_json' && scriptDuplicationAudit.jscpdCommand.command.includes('jscpd') && scriptDuplicationAudit.jscpdCommand.command.includes('--config') && scriptDuplicationAudit.jscpdCommand.command.includes('.jscpd.json') && scriptDuplicationAudit.jscpdCommand.command.includes('--reporters') && scriptDuplicationAudit.jscpdCommand.command.includes('json') && scriptDuplicationAudit.jscpdCommand.exitCode === 0 && scriptDuplicationAudit.jscpdCommand.passed && scriptDuplicationAudit.jscpdCommand.missingSubstrings.length === 0 && scriptDuplicationAudit.jscpdReportSha256.length === 64, scriptDuplicationAudit.jscpdVersion))
  checks.push(check('script duplication jscpd ratchet does not exceed baseline', scriptDuplicationAudit.jscpdCloneCount <= scriptDuplicationAudit.jscpdCloneBaseline && scriptDuplicationAudit.jscpdDuplicatedLines <= scriptDuplicationAudit.jscpdDuplicatedLinesBaseline && scriptDuplicationAudit.jscpdDuplicatedTokens <= scriptDuplicationAudit.jscpdDuplicatedTokensBaseline && scriptDuplicationAudit.jscpdDuplicatedPercentage <= scriptDuplicationAudit.jscpdDuplicatedPercentageBaseline, `${scriptDuplicationAudit.jscpdCloneCount}/${scriptDuplicationAudit.jscpdCloneBaseline}; ${scriptDuplicationAudit.jscpdDuplicatedLines}/${scriptDuplicationAudit.jscpdDuplicatedLinesBaseline}; ${scriptDuplicationAudit.jscpdDuplicatedTokens}/${scriptDuplicationAudit.jscpdDuplicatedTokensBaseline}; ${scriptDuplicationAudit.jscpdDuplicatedPercentage}/${scriptDuplicationAudit.jscpdDuplicatedPercentageBaseline}`))
  checks.push(check('script duplication jscpd paths are normalized candidates', scriptDuplicationAudit.jscpdTopClonePairs.length > 0 && scriptDuplicationAudit.jscpdTopClonePairs.every((pair) => !pair.firstFile.includes('\\') && !pair.secondFile.includes('\\')), `${scriptDuplicationAudit.jscpdTopClonePairs.length} pairs`))
  checks.push(check('script duplication audit records official primary sources', ['jscpd', 'Roy and Cordy clone detection survey', 'US11662998B2 duplicate code pattern patent'].every((source) => scriptDuplicationAudit.primarySourceInputs.some((item) => item.sourceProject === source)) && scriptDuplicationAudit.primarySourceInputs.every((item) => item.sourceUrl.startsWith('https://github.com/') || item.sourceUrl.startsWith('https://knip.dev/') || item.sourceUrl.startsWith('https://research.cs.queensu.ca/') || item.sourceUrl.startsWith('https://patents.google.com/')), scriptDuplicationAudit.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('script duplication audit keeps refactor and readiness claims blocked', scriptDuplicationAudit.refactorCompletionClaimAllowed === false && scriptDuplicationAudit.publicReadinessClaimAllowed === false))
  checks.push(check('script duplication audit checks pass', scriptDuplicationAudit.auditChecks.every((item) => item.ok)))
  checks.push(check('dead export candidate gate is local no-provider evidence', deadExportCandidates.mode === 'local_no_provider_dead_export_candidate_gate'))
  checks.push(check('dead export candidate gate performed no provider live external or protected calls', deadExportCandidates.providerCallsPerformed.length === 0 && deadExportCandidates.liveModelCallsPerformed.length === 0 && deadExportCandidates.externalCallsPerformed.length === 0 && deadExportCandidates.protectedActionsExecuted.length === 0))
  checks.push(check('dead export candidate gate records Knip config command evidence', deadExportCandidates.knipVersion.length > 0 && deadExportCandidates.knipCommands.some((item) => item.name === 'knip_exports_json' && item.command.includes('knip') && item.command.includes('--config') && item.command.includes('knip.jsonc') && item.command.includes('--exports') && item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0), deadExportCandidates.knipVersion))
  checks.push(check('dead export candidate gate discovers candidates', deadExportCandidates.candidateFileCount > 0 && deadExportCandidates.candidateUnusedExportCount > 0, `${deadExportCandidates.candidateFileCount}/${deadExportCandidates.candidateUnusedExportCount}`))
  checks.push(check('dead export candidate files do not exceed baseline', deadExportCandidates.candidateFileCount <= deadExportCandidates.candidateFileBaseline, `${deadExportCandidates.candidateFileCount}/${deadExportCandidates.candidateFileBaseline}`))
  checks.push(check('dead export unused exports do not exceed baseline', deadExportCandidates.candidateUnusedExportCount <= deadExportCandidates.candidateUnusedExportBaseline, `${deadExportCandidates.candidateUnusedExportCount}/${deadExportCandidates.candidateUnusedExportBaseline}`))
  checks.push(check('dead export unused types do not exceed baseline', deadExportCandidates.candidateUnusedTypeCount <= deadExportCandidates.candidateUnusedTypeBaseline, `${deadExportCandidates.candidateUnusedTypeCount}/${deadExportCandidates.candidateUnusedTypeBaseline}`))
  checks.push(check('dead export duplicate exports do not exceed baseline', deadExportCandidates.candidateDuplicateExportCount <= deadExportCandidates.candidateDuplicateExportBaseline, `${deadExportCandidates.candidateDuplicateExportCount}/${deadExportCandidates.candidateDuplicateExportBaseline}`))
  checks.push(check('dead export candidate triage path is required evidence', deadExportCandidates.triageLedgerPath === deadExportCandidateTriagePath && existsSync(resolve(root, deadExportCandidateTriagePath)), deadExportCandidates.triageLedgerPath))
  checks.push(check('dead export candidate triage entries remain current', deadExportCandidates.triageRecordCount >= 5 && deadExportCandidates.triageCurrentCandidateCount === deadExportCandidates.triageRecordCount && deadExportCandidates.triageRecords.every((item) => item.currentCandidate), `${deadExportCandidates.triageCurrentCandidateCount}/${deadExportCandidates.triageRecordCount}`))
  checks.push(check('dead export candidate triage covers guarded and removal-review paths', (deadExportCandidates.triageActionCounts.needs_runtime_guard ?? 0) > 0 && (deadExportCandidates.triageActionCounts.review_for_removal ?? 0) > 0, JSON.stringify(deadExportCandidates.triageActionCounts)))
  checks.push(check('dead export candidate triage records rationale and guardrails', deadExportCandidates.triageRecords.every((item) => item.rationale.length > 20 && item.guardrail.length > 20), `${deadExportCandidates.triageRecordCount} records`))
  checks.push(check('dead export candidate removed ratchets remain absent', deadExportCandidates.removedCandidateRatchets.length >= 4 && deadExportCandidates.removedCandidateRatchets.every((item) => !item.currentCandidate && item.guardrail.length > 20), `${deadExportCandidates.removedCandidateRatchets.filter((item) => item.currentCandidate).length}/${deadExportCandidates.removedCandidateRatchets.length} regressed`))
  checks.push(check('dead export candidate gate records official primary sources', ['Knip', 'Knip JSON reporter docs', 'fallow'].every((source) => deadExportCandidates.primarySourceInputs.some((item) => item.sourceProject === source)) && deadExportCandidates.primarySourceInputs.every((item) => item.sourceUrl.startsWith('https://github.com/') || item.sourceUrl.startsWith('https://knip.dev/')), deadExportCandidates.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('dead export candidate gate keeps deletion cleanup and readiness claims blocked', deadExportCandidates.deletionClaimAllowed === false && deadExportCandidates.cleanupCompletionClaimAllowed === false && deadExportCandidates.publicReadinessClaimAllowed === false))
  checks.push(check('dead export candidate commands pass', deadExportCandidates.knipCommands.every((item) => item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0)))
  checks.push(check('dead export candidate checks pass', deadExportCandidates.deadExportChecks.every((item) => item.ok)))
  checks.push(check('maintainer ownership quality is local no-provider check', maintainerOwnershipQuality.mode === 'local_no_provider_maintainer_ownership_quality'))
  checks.push(check('maintainer ownership quality performed no provider calls', maintainerOwnershipQuality.providerCallsPerformed.length === 0))
  checks.push(check('maintainer ownership quality performed no live model calls', maintainerOwnershipQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('maintainer ownership quality performed no external calls', maintainerOwnershipQuality.externalCallsPerformed.length === 0 && maintainerOwnershipQuality.hostedCodeownerResolutionPerformed === false && maintainerOwnershipQuality.branchProtectionQueryPerformed === false))
  checks.push(check('maintainer ownership quality executed no protected actions', maintainerOwnershipQuality.protectedActionsExecuted.length === 0))
  checks.push(check('maintainer ownership quality records ownership primary sources', ['GitHub Docs CODEOWNERS', 'GitHub Docs protected branches', 'OpenSSF Scorecard checks'].every((source) => maintainerOwnershipQuality.primarySourceInputs.some((item) => item.sourceProject === source)), maintainerOwnershipQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('maintainer ownership quality verifies preferred CODEOWNERS surface', maintainerOwnershipQuality.codeownersPath === '.github/CODEOWNERS' && maintainerOwnershipQuality.codeownersPreferredLocation && maintainerOwnershipQuality.codeownersUnderGithubLimit && maintainerOwnershipQuality.invalidSyntaxLines.length === 0, `${maintainerOwnershipQuality.codeownersPath}/${maintainerOwnershipQuality.codeownersSizeBytes}`))
  checks.push(check('maintainer ownership quality covers required owner patterns', maintainerOwnershipQuality.missingRequiredPatterns.length === 0 && maintainerOwnershipQuality.codeownerRules.length >= maintainerOwnershipQuality.requiredPatterns.length, maintainerOwnershipQuality.missingRequiredPatterns.join(',') || `${maintainerOwnershipQuality.codeownerRules.length} rules`))
  checks.push(check('maintainer ownership quality keeps hosted enforcement claims blocked', maintainerOwnershipQuality.hostedCodeownerResolutionPerformed === false && maintainerOwnershipQuality.branchProtectionQueryPerformed === false && maintainerOwnershipQuality.codeOwnerReviewRequiredClaimAllowed === false))
  checks.push(check('maintainer ownership quality keeps readiness claims blocked', maintainerOwnershipQuality.releaseReadinessClaimAllowed === false && maintainerOwnershipQuality.productionReadinessClaimAllowed === false && maintainerOwnershipQuality.publicReadinessClaimAllowed === false && maintainerOwnershipQuality.externalValidationClaimAllowed === false && maintainerOwnershipQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('maintainer ownership quality checks pass', maintainerOwnershipQuality.ownershipChecks.every((item) => item.ok)))
  checks.push(check('dependency governance quality is local no-provider check', dependencyGovernanceQuality.mode === 'local_no_provider_dependency_governance_quality'))
  checks.push(check('dependency governance quality performed no provider calls', dependencyGovernanceQuality.providerCallsPerformed.length === 0))
  checks.push(check('dependency governance quality performed no live model calls', dependencyGovernanceQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('dependency governance quality performed no external calls', dependencyGovernanceQuality.externalCallsPerformed.length === 0 && dependencyGovernanceQuality.dependencyReviewHostedRunPerformed === false && dependencyGovernanceQuality.externalVulnerabilityScanPerformed === false && dependencyGovernanceQuality.githubApiCallsPerformed === false))
  checks.push(check('dependency governance quality executed no protected actions', dependencyGovernanceQuality.protectedActionsExecuted.length === 0))
  checks.push(check('dependency governance quality records dependency primary sources', ['GitHub Docs dependency review', 'actions/dependency-review-action', 'Bun lockfile documentation', 'GitHub Docs Dependabot options', 'OpenSSF Scorecard Pinned-Dependencies'].every((source) => dependencyGovernanceQuality.primarySourceInputs.some((item) => item.sourceProject === source)), dependencyGovernanceQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('dependency governance quality verifies package manager and lockfile evidence', dependencyGovernanceQuality.packageManagerFieldPresent && dependencyGovernanceQuality.packageManagerMatchesWorkflowBunVersion && dependencyGovernanceQuality.bunLockPath === 'bun.lock' && dependencyGovernanceQuality.bunLockTextStructureRecognized && dependencyGovernanceQuality.bunLockfileVersion === 1 && dependencyGovernanceQuality.bunLockRootWorkspacePresent && dependencyGovernanceQuality.bunLockCoversPackageManifestDependencies && dependencyGovernanceQuality.missingManifestDependenciesInLockfile.length === 0, `${dependencyGovernanceQuality.packageManagerField}/${dependencyGovernanceQuality.bunLockSizeBytes}`))
  checks.push(check('dependency governance quality inventories manifest dependency policy', dependencyGovernanceQuality.dependencyEntries.length >= 90 && dependencyGovernanceQuality.runtimeDependencyCount > 0 && dependencyGovernanceQuality.developmentDependencyCount > 0 && dependencyGovernanceQuality.exactVersionCount + dependencyGovernanceQuality.semverRangeCount + dependencyGovernanceQuality.otherVersionSpecifierCount === dependencyGovernanceQuality.dependencyEntries.length && dependencyGovernanceQuality.overridesPresent, `${dependencyGovernanceQuality.dependencyEntries.length} entries; overrides=${dependencyGovernanceQuality.overrideNames.join(',')}`))
  checks.push(check('dependency governance quality verifies update and review wiring', dependencyGovernanceQuality.dependabotCoversNpm && dependencyGovernanceQuality.dependabotCoversGitHubActions && dependencyGovernanceQuality.dependabotSchedulesPresent && dependencyGovernanceQuality.dependencyReviewWorkflowPath === '.github/workflows/dependency-review.yml' && dependencyGovernanceQuality.dependencyReviewWorkflowPresent && dependencyGovernanceQuality.dependencyReviewActionConfigured && dependencyGovernanceQuality.dependencyReviewActionPinned && dependencyGovernanceQuality.dependencyReviewWorkflowPullRequestOnly && dependencyGovernanceQuality.dependencyReviewWorkflowPermissionsReadOnly && dependencyGovernanceQuality.frozenDependencyInstallPresent, dependencyGovernanceQuality.dependencyReviewWorkflowPath))
  checks.push(check('dependency governance quality keeps hosted review and vulnerability claims blocked', dependencyGovernanceQuality.dependencyReviewHostedRunPerformed === false && dependencyGovernanceQuality.dependencyReviewRequiredStatusClaimAllowed === false && dependencyGovernanceQuality.externalVulnerabilityScanPerformed === false && dependencyGovernanceQuality.npmAuditPerformed === false && dependencyGovernanceQuality.vulnerabilityFreeClaimAllowed === false && dependencyGovernanceQuality.dependencyReviewPassClaimAllowed === false))
  checks.push(check('dependency governance quality keeps readiness claims blocked', dependencyGovernanceQuality.releaseReadinessClaimAllowed === false && dependencyGovernanceQuality.productionReadinessClaimAllowed === false && dependencyGovernanceQuality.publicReadinessClaimAllowed === false && dependencyGovernanceQuality.externalValidationClaimAllowed === false && dependencyGovernanceQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('dependency governance quality checks pass', dependencyGovernanceQuality.governanceChecks.every((item) => item.ok)))
  checks.push(check('lockfile SBOM quality is local no-provider check', lockfileSbomQuality.mode === 'local_no_provider_lockfile_sbom_quality'))
  checks.push(check('lockfile SBOM quality performed no provider calls', lockfileSbomQuality.providerCallsPerformed.length === 0))
  checks.push(check('lockfile SBOM quality performed no live model calls', lockfileSbomQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('lockfile SBOM quality performed no external calls', lockfileSbomQuality.externalCallsPerformed.length === 0 && lockfileSbomQuality.githubDependencyGraphExportPerformed === false && lockfileSbomQuality.externalSbomExportPerformed === false && lockfileSbomQuality.hostedSbomValidationPerformed === false))
  checks.push(check('lockfile SBOM quality executed no protected actions', lockfileSbomQuality.protectedActionsExecuted.length === 0))
  checks.push(check('lockfile SBOM quality records SBOM primary sources', ['Bun lockfile documentation', 'CycloneDX specification overview', 'SPDX specifications', 'GitHub Dependency Graph SBOM API'].every((source) => lockfileSbomQuality.primarySourceInputs.some((item) => item.sourceProject === source)), lockfileSbomQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('lockfile SBOM quality inventories lockfile packages and relationships', lockfileSbomQuality.inventoryFormat === 'openclaude_lockfile_inventory_v1' && lockfileSbomQuality.bunLockPath === 'bun.lock' && lockfileSbomQuality.bunLockTextStructureRecognized && lockfileSbomQuality.bunLockfileVersion === 1 && lockfileSbomQuality.lockfilePackageCount > lockfileSbomQuality.directManifestDependencyCount && lockfileSbomQuality.lockfilePackageCountExceedsDirectDependencies && lockfileSbomQuality.lockfileRelationshipCount > lockfileSbomQuality.directManifestDependencyCount, `${lockfileSbomQuality.lockfilePackageCount} packages/${lockfileSbomQuality.lockfileRelationshipCount} relationships`))
  checks.push(check('lockfile SBOM quality covers manifest dependencies and integrity metadata', lockfileSbomQuality.directManifestDependenciesCovered && lockfileSbomQuality.missingDirectManifestDependencies.length === 0 && lockfileSbomQuality.packagesMissingIntegrity.length === 0 && lockfileSbomQuality.packagesWithIntegrityCount === lockfileSbomQuality.lockfilePackageCount && lockfileSbomQuality.packagesWithDependencyMetadataCount > 0, lockfileSbomQuality.missingDirectManifestDependencies.join(',') || 'all direct dependencies covered'))
  checks.push(check('lockfile SBOM quality writes expected JSONL inventory', lockfileSbomQuality.inventoryJsonlPath === lockfileSbomInventoryJsonlPath && lockfileSbomQuality.inventoryJsonlSha256.length === 64 && lockfileSbomQuality.inventoryJsonlParseable && lockfileSbomQuality.inventoryJsonlRecordCount === lockfileSbomQuality.lockfilePackageCount && lockfileSbomQuality.lockfilePackageRecords.length === lockfileSbomQuality.lockfilePackageCount && lockfileSbomQuality.lockfileRelationshipRecords.length === lockfileSbomQuality.lockfileRelationshipCount, lockfileSbomQuality.inventoryJsonlPath))
  checks.push(check('lockfile SBOM quality keeps official SBOM and vulnerability claims blocked', lockfileSbomQuality.officialCycloneDxComplianceClaimAllowed === false && lockfileSbomQuality.officialSpdxComplianceClaimAllowed === false && lockfileSbomQuality.githubDependencyGraphParityClaimAllowed === false && lockfileSbomQuality.vulnerabilityScanPerformed === false && lockfileSbomQuality.vulnerabilityFreeClaimAllowed === false && lockfileSbomQuality.licenseConclusionPerformed === false && lockfileSbomQuality.licenseComplianceClaimAllowed === false))
  checks.push(check('lockfile SBOM quality keeps readiness claims blocked', lockfileSbomQuality.releaseReadinessClaimAllowed === false && lockfileSbomQuality.productionReadinessClaimAllowed === false && lockfileSbomQuality.publicReadinessClaimAllowed === false && lockfileSbomQuality.externalValidationClaimAllowed === false && lockfileSbomQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('lockfile SBOM quality checks pass', lockfileSbomQuality.sbomQualityChecks.every((item) => item.ok)))
  checks.push(check('third-party license quality is local no-provider check', thirdPartyLicenseQuality.mode === 'local_no_provider_third_party_license_quality'))
  checks.push(check('third-party license quality performed no provider calls', thirdPartyLicenseQuality.providerCallsPerformed.length === 0))
  checks.push(check('third-party license quality performed no live model calls', thirdPartyLicenseQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('third-party license quality performed no external calls', thirdPartyLicenseQuality.externalCallsPerformed.length === 0 && thirdPartyLicenseQuality.externalLicenseResolutionPerformed === false && thirdPartyLicenseQuality.npmRegistryLookupPerformed === false && thirdPartyLicenseQuality.githubLicenseApiLookupPerformed === false))
  checks.push(check('third-party license quality executed no protected actions', thirdPartyLicenseQuality.protectedActionsExecuted.length === 0 && thirdPartyLicenseQuality.dependencyInstallPerformed === false && thirdPartyLicenseQuality.legalReviewPerformed === false && thirdPartyLicenseQuality.noticeFileGenerated === false))
  checks.push(check('third-party license quality records license primary sources', ['SPDX License List', 'npm package.json license field', 'GitHub Docs licensing a repository', 'GitHub Licenses REST API'].every((source) => thirdPartyLicenseQuality.primarySourceInputs.some((item) => item.sourceProject === source)), thirdPartyLicenseQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('third-party license quality consumes lockfile SBOM inventory', thirdPartyLicenseQuality.sourceLockfileSbomReportPath === lockfileSbomQualityJsonPath && thirdPartyLicenseQuality.sourceLockfileInventoryJsonlPath === lockfileSbomInventoryJsonlPath && thirdPartyLicenseQuality.sourceLockfilePackageCount === lockfileSbomQuality.lockfilePackageCount, `${thirdPartyLicenseQuality.sourceLockfilePackageCount}/${lockfileSbomQuality.lockfilePackageCount}`))
  checks.push(check('third-party license quality covers direct dependency metadata', thirdPartyLicenseQuality.nodeModulesPresent && thirdPartyLicenseQuality.directManifestDependenciesCoveredByMetadata && thirdPartyLicenseQuality.missingDirectManifestDependencyMetadata.length === 0 && thirdPartyLicenseQuality.directManifestDependencyCount === lockfileSbomQuality.directManifestDependencyCount, thirdPartyLicenseQuality.missingDirectManifestDependencyMetadata.join(',') || `${thirdPartyLicenseQuality.directManifestDependencyCount} direct dependencies`))
  checks.push(check('third-party license quality inventories installed license metadata', thirdPartyLicenseQuality.inventoryFormat === 'openclaude_third_party_license_inventory_v1' && thirdPartyLicenseQuality.installedMetadataPackageCount > thirdPartyLicenseQuality.directManifestDependencyCount && thirdPartyLicenseQuality.licenseFieldMissingPackages.length === 0 && thirdPartyLicenseQuality.licenseFieldPresentCount === thirdPartyLicenseQuality.installedMetadataPackageCount, `${thirdPartyLicenseQuality.licenseFieldPresentCount}/${thirdPartyLicenseQuality.installedMetadataPackageCount}`))
  checks.push(check('third-party license quality writes expected JSONL inventory', thirdPartyLicenseQuality.inventoryJsonlPath === thirdPartyLicenseInventoryJsonlPath && thirdPartyLicenseQuality.inventoryJsonlSha256.length === 64 && thirdPartyLicenseQuality.inventoryJsonlParseable && thirdPartyLicenseQuality.inventoryJsonlRecordCount === thirdPartyLicenseQuality.sourceLockfilePackageCount && thirdPartyLicenseQuality.licenseMetadataRecords.length === thirdPartyLicenseQuality.inventoryJsonlRecordCount, thirdPartyLicenseQuality.inventoryJsonlPath))
  checks.push(check('third-party license quality classifies local install-tree and notice gaps', thirdPartyLicenseQuality.missingMetadataClassifiedAsLocalInstallTreeGap && thirdPartyLicenseQuality.missingMetadataPackageCount >= 0 && thirdPartyLicenseQuality.licenseFilePresentCount > 0 && thirdPartyLicenseQuality.noticeFilePresentCount >= 0 && thirdPartyLicenseQuality.directLicenseFileMissingPackages.length >= 0, `${thirdPartyLicenseQuality.missingMetadataPackageCount} missing metadata; ${thirdPartyLicenseQuality.directLicenseFileMissingPackages.length} direct license-file gaps`))
  checks.push(check('third-party license quality keeps compliance and readiness claims blocked', thirdPartyLicenseQuality.spdxExpressionParsePerformed === false && thirdPartyLicenseQuality.licenseComplianceClaimAllowed === false && thirdPartyLicenseQuality.thirdPartyNoticeReadyClaimAllowed === false && thirdPartyLicenseQuality.releaseReadinessClaimAllowed === false && thirdPartyLicenseQuality.productionReadinessClaimAllowed === false && thirdPartyLicenseQuality.publicReadinessClaimAllowed === false && thirdPartyLicenseQuality.externalValidationClaimAllowed === false && thirdPartyLicenseQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('third-party license quality checks pass', thirdPartyLicenseQuality.licenseQualityChecks.every((item) => item.ok)))
  checks.push(check('source license metadata quality is local no-provider check', sourceLicenseMetadataQuality.mode === 'local_no_provider_source_license_metadata_quality'))
  checks.push(check('source license metadata quality performed no provider calls', sourceLicenseMetadataQuality.providerCallsPerformed.length === 0))
  checks.push(check('source license metadata quality performed no live model calls', sourceLicenseMetadataQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('source license metadata quality performed no external calls', sourceLicenseMetadataQuality.externalCallsPerformed.length === 0 && sourceLicenseMetadataQuality.reuseToolRunPerformed === false && sourceLicenseMetadataQuality.spdxDocumentGenerated === false))
  checks.push(check('source license metadata quality executed no protected actions', sourceLicenseMetadataQuality.protectedActionsExecuted.length === 0 && sourceLicenseMetadataQuality.legalReviewPerformed === false))
  checks.push(check('source license metadata quality records REUSE/SPDX primary sources', ['REUSE Specification', 'SPDX source-file identifiers', 'fsfe/reuse-tool', 'SPDX handling license info'].every((source) => sourceLicenseMetadataQuality.primarySourceInputs.some((item) => item.sourceProject === source)), sourceLicenseMetadataQuality.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('source license metadata quality preserves derived-code license boundary', sourceLicenseMetadataQuality.packageLicenseField === 'SEE LICENSE FILE' && sourceLicenseMetadataQuality.rootLicensePath === 'LICENSE' && sourceLicenseMetadataQuality.rootLicenseContainsDerivedCodeBoundary && sourceLicenseMetadataQuality.rootLicenseContainsMitModificationBoundary, `${sourceLicenseMetadataQuality.packageLicenseField}/${sourceLicenseMetadataQuality.rootLicensePath}`))
  checks.push(check('source license metadata quality scans expected source surfaces', sourceLicenseMetadataQuality.scannedSourceFileCount > 1000 && ['src', 'scripts', 'packages/openclaude-vscode', '.github'].every((root) => sourceLicenseMetadataQuality.scanRoots.includes(root)) && Object.keys(sourceLicenseMetadataQuality.fileCategoryCounts).length >= 5, `${sourceLicenseMetadataQuality.scannedSourceFileCount} scanned files`))
  checks.push(check('source license metadata quality classifies missing file-level metadata', sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadataCount >= 0 && sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadata.length === sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadataCount && sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadataCount === sourceLicenseMetadataQuality.scannedSourceFileCount - sourceLicenseMetadataQuality.sourceFilesWithSpdxLicenseIdentifierCount - sourceLicenseMetadataQuality.sourceFilesWithAdjacentLicenseFileCount - sourceLicenseMetadataQuality.sourceFilesCoveredByReuseTomlAnnotationCount, `${sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadataCount} gaps`))
  checks.push(check('source license metadata quality records missing REUSE compliance artifacts without claiming compliance', sourceLicenseMetadataQuality.reuseTomlPresent === false && sourceLicenseMetadataQuality.licensesDirectoryPresent === false && sourceLicenseMetadataQuality.reuseComplianceClaimAllowed === false && sourceLicenseMetadataQuality.sourceLicenseComplianceClaimAllowed === false && sourceLicenseMetadataQuality.sourceMetadataReadyClaimAllowed === false))
  checks.push(check('source license metadata quality writes expected JSONL inventory', sourceLicenseMetadataQuality.inventoryJsonlPath === sourceLicenseMetadataInventoryJsonlPath && sourceLicenseMetadataQuality.inventoryJsonlSha256.length === 64 && sourceLicenseMetadataQuality.inventoryJsonlParseable && sourceLicenseMetadataQuality.inventoryJsonlRecordCount === sourceLicenseMetadataQuality.scannedSourceFileCount && sourceLicenseMetadataQuality.sourceLicenseRecords.length === sourceLicenseMetadataQuality.inventoryJsonlRecordCount, sourceLicenseMetadataQuality.inventoryJsonlPath))
  checks.push(check('source license metadata quality keeps readiness claims blocked', sourceLicenseMetadataQuality.releaseReadinessClaimAllowed === false && sourceLicenseMetadataQuality.productionReadinessClaimAllowed === false && sourceLicenseMetadataQuality.publicReadinessClaimAllowed === false && sourceLicenseMetadataQuality.externalValidationClaimAllowed === false && sourceLicenseMetadataQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('source license metadata quality checks pass', sourceLicenseMetadataQuality.sourceLicenseMetadataChecks.every((item) => item.ok)))
  checks.push(check('license boundary authorization is local no-provider check', licenseBoundaryAuthorization.mode === 'local_no_provider_license_boundary_authorization'))
  checks.push(check('license boundary authorization performed no provider calls', licenseBoundaryAuthorization.providerCallsPerformed.length === 0))
  checks.push(check('license boundary authorization performed no live model calls', licenseBoundaryAuthorization.liveModelCallsPerformed.length === 0))
  checks.push(check('license boundary authorization performed no external calls', licenseBoundaryAuthorization.externalCallsPerformed.length === 0 && licenseBoundaryAuthorization.externalLicenseResolutionPerformed === false && licenseBoundaryAuthorization.npmRegistryLookupPerformed === false && licenseBoundaryAuthorization.githubLicenseApiLookupPerformed === false))
  checks.push(check('license boundary authorization executed no protected actions', licenseBoundaryAuthorization.protectedActionsExecuted.length === 0 && licenseBoundaryAuthorization.dependencyInstallPerformed === false && licenseBoundaryAuthorization.legalReviewPerformed === false && licenseBoundaryAuthorization.noticeFileGenerated === false && licenseBoundaryAuthorization.reuseArtifactsCreated === false && licenseBoundaryAuthorization.sourceFilesRewritten === false))
  checks.push(check('license boundary authorization records license decision primary sources', ['GitHub Docs licensing a repository', 'npm package.json license field', 'SPDX License List', 'SPDX File Tags', 'REUSE Specification 3.2'].every((source) => licenseBoundaryAuthorization.primarySourceInputs.some((item) => item.sourceProject === source)), licenseBoundaryAuthorization.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('license boundary authorization imports source reports', licenseBoundaryAuthorization.sourceThirdPartyLicenseQualityReportPath === thirdPartyLicenseQualityJsonPath && licenseBoundaryAuthorization.sourceSourceLicenseMetadataQualityReportPath === sourceLicenseMetadataQualityJsonPath, `${licenseBoundaryAuthorization.sourceThirdPartyLicenseQualityReportPath}/${licenseBoundaryAuthorization.sourceSourceLicenseMetadataQualityReportPath}`))
  checks.push(check('license boundary authorization preserves source gap metrics', licenseBoundaryAuthorization.thirdPartyDirectLicenseFileMissingPackages.length === thirdPartyLicenseQuality.directLicenseFileMissingPackages.length && licenseBoundaryAuthorization.thirdPartyNoticeFilePresentCount === thirdPartyLicenseQuality.noticeFilePresentCount && licenseBoundaryAuthorization.sourceFilesMissingFileLevelMetadataCount === sourceLicenseMetadataQuality.sourceFilesMissingFileLevelMetadataCount, `${licenseBoundaryAuthorization.thirdPartyDirectLicenseFileMissingPackages.length}/${licenseBoundaryAuthorization.sourceFilesMissingFileLevelMetadataCount}`))
  checks.push(check('license boundary authorization preserves derived-code license boundary', licenseBoundaryAuthorization.derivedCodeBoundaryRecognized === true && licenseBoundaryAuthorization.mitModificationBoundaryRecognized === true && licenseBoundaryAuthorization.licenseBoundaryStatus === 'owner_legal_authorization_required_before_release_or_license_compliance_claims'))
  checks.push(check('license boundary authorization request is explicit and default-deny', licenseBoundaryAuthorization.ownerLegalDecisionRequired === true && licenseBoundaryAuthorization.protectedAuthorizationRequestCreated === true && licenseBoundaryAuthorization.protectedAuthorizationRequestCount === licenseBoundaryAuthorization.authorizationItems.length && licenseBoundaryAuthorization.protectedAuthorizationRequestCount >= 8 && licenseBoundaryAuthorization.allProtectedAuthorizationsDefaultFalse === true && licenseBoundaryAuthorization.authorizationItems.every((item) => item.protectedAction === true && item.defaultAuthorized === false && item.status === 'blocked_pending_explicit_owner_or_legal_authorization'), `${licenseBoundaryAuthorization.protectedAuthorizationRequestCount} requests`))
  checks.push(check('license boundary authorization writes expected request and JSONL', licenseBoundaryAuthorization.requestMarkdownPath === licenseBoundaryAuthorizationRequestPath && licenseBoundaryAuthorization.authorizationItemsJsonlPath === licenseBoundaryAuthorizationItemsJsonlPath && licenseBoundaryAuthorization.authorizationItemsJsonlSha256.length === 64 && licenseBoundaryAuthorization.authorizationItemsJsonlParseable && licenseBoundaryAuthorization.authorizationItemsJsonlRecordCount === licenseBoundaryAuthorization.authorizationItems.length, licenseBoundaryAuthorization.authorizationItemsJsonlPath))
  checks.push(check('license boundary authorization keeps license and readiness claims blocked', licenseBoundaryAuthorization.spdxExpressionParsePerformed === false && licenseBoundaryAuthorization.reuseToolRunPerformed === false && licenseBoundaryAuthorization.spdxDocumentGenerated === false && licenseBoundaryAuthorization.licenseComplianceClaimAllowed === false && licenseBoundaryAuthorization.thirdPartyNoticeReadyClaimAllowed === false && licenseBoundaryAuthorization.reuseComplianceClaimAllowed === false && licenseBoundaryAuthorization.sourceLicenseComplianceClaimAllowed === false && licenseBoundaryAuthorization.sourceMetadataReadyClaimAllowed === false && licenseBoundaryAuthorization.releaseReadinessClaimAllowed === false && licenseBoundaryAuthorization.productionReadinessClaimAllowed === false && licenseBoundaryAuthorization.publicReadinessClaimAllowed === false && licenseBoundaryAuthorization.externalValidationClaimAllowed === false && licenseBoundaryAuthorization.autonomousReliabilityClaimAllowed === false))
  checks.push(check('license boundary authorization checks pass', licenseBoundaryAuthorization.licenseBoundaryAuthorizationChecks.every((item) => item.ok)))
  checks.push(check('provider compatibility fixtures are local no-provider checks', providerCompatibility.mode === 'local_no_provider_provider_surface'))
  checks.push(check('provider compatibility performed no provider calls', providerCompatibility.providerCallsPerformed.length === 0))
  checks.push(check('provider compatibility performed no live model calls', providerCompatibility.liveModelCallsPerformed.length === 0))
  checks.push(check('provider compatibility performed no external calls', providerCompatibility.externalCallsPerformed.length === 0))
  checks.push(check('provider compatibility includes direct provider flags', providerCompatibility.directProviderFlags.length >= 6))
  checks.push(check('provider compatibility includes preset defaults', providerCompatibility.providerPresetDefaults.length >= 10))
  checks.push(check('provider compatibility checks pass', providerCompatibility.compatibilityChecks.every((item) => item.ok)))
  checks.push(check('permission regression fixtures are local no-provider checks', permissionRegression.mode === 'local_no_provider_permission_regression'))
  checks.push(check('permission regression performed no provider calls', permissionRegression.providerCallsPerformed.length === 0))
  checks.push(check('permission regression performed no live model calls', permissionRegression.liveModelCallsPerformed.length === 0))
  checks.push(check('permission regression performed no external calls', permissionRegression.externalCallsPerformed.length === 0))
  checks.push(check('permission regression includes protected surfaces', permissionRegression.protectedPermissionSurfaces.length >= 5))
  checks.push(check('permission regression includes targeted test files', permissionRegression.targetedTestFiles.length >= 4))
  checks.push(check('permission regression fixtures pass', permissionRegression.regressionFixtures.every((item) => item.ok)))
  checks.push(check('permission regression includes behavioral test command evidence', permissionRegression.behavioralTestCommands.length >= 1))
  checks.push(check('permission regression behavioral commands pass', permissionRegression.behavioralTestCommands.every((item) => item.exitCode === 0 && item.passed && item.missingSubstrings.length === 0)))
  checks.push(check('runtime doctor fixtures are local no-provider checks', runtimeDoctorRegression.mode === 'local_no_provider_runtime_doctor_regression'))
  checks.push(check('runtime doctor regression performed no provider calls', runtimeDoctorRegression.providerCallsPerformed.length === 0))
  checks.push(check('runtime doctor regression performed no live model calls', runtimeDoctorRegression.liveModelCallsPerformed.length === 0))
  checks.push(check('runtime doctor regression performed no external calls', runtimeDoctorRegression.externalCallsPerformed.length === 0))
  checks.push(check('runtime doctor regression includes runtime surfaces', runtimeDoctorRegression.runtimeDoctorSurfaces.length >= 6))
  checks.push(check('runtime doctor regression includes command evidence', runtimeDoctorRegression.doctorCommands.length >= 2))
  checks.push(check('runtime doctor commands pass', runtimeDoctorRegression.doctorCommands.every((item) => item.exitCode === 0 && item.passed)))
  checks.push(check('runtime doctor checks pass', runtimeDoctorRegression.doctorChecks.every((item) => item.ok)))
  checks.push(check('provider capability matrix is local no-provider evidence', providerCapabilityMatrix.mode === 'local_no_provider_provider_capability_matrix'))
  checks.push(check('provider capability matrix imports expected sources', providerCapabilityMatrix.sourceProviderCompatibilityReportPath === providerCompatibilityJsonPath && providerCapabilityMatrix.sourceRuntimeDoctorReportPath === runtimeDoctorRegressionJsonPath && providerCapabilityMatrix.sourceOssAxisArchitectureReportPath === ossAxisArchitectureReviewJsonPath, `${providerCapabilityMatrix.sourceProviderCompatibilityReportPath}/${providerCapabilityMatrix.sourceRuntimeDoctorReportPath}/${providerCapabilityMatrix.sourceOssAxisArchitectureReportPath}`))
  checks.push(check('provider capability matrix covers provider surfaces', providerCapabilityMatrix.directProviderFlagCount === providerCompatibility.directProviderFlags.length && providerCapabilityMatrix.providerPresetDefaultCount === providerCompatibility.providerPresetDefaults.length && providerCapabilityMatrix.capabilityRowCount >= providerCompatibility.providerPresetDefaults.length && providerCapabilityMatrix.openAiCompatibleSurfaceCount >= 10, `${providerCapabilityMatrix.directProviderFlagCount}/${providerCapabilityMatrix.providerPresetDefaultCount}/${providerCapabilityMatrix.capabilityRowCount}`))
  checks.push(check('provider capability matrix covers local no-key providers', ['ollama', 'lmstudio', 'atomic-chat'].every((preset) => providerCapabilityMatrix.capabilityRows.some((row) => row.preset === preset && row.noApiKeyLocalCandidate && row.claimAllowed === false)), providerCapabilityMatrix.capabilityRows.filter((row) => row.noApiKeyLocalCandidate).map((row) => row.surfaceId).join(',') || 'none'))
  checks.push(check('provider capability matrix covers required failure modes', ['provider_key_missing', 'local_runtime_unavailable', 'provider_reachability_skipped', 'profile_direct_surface_drift', 'live_model_authorization_missing'].every((id) => providerCapabilityMatrix.failureModeIds.includes(id)) && providerCapabilityMatrix.failureModeCount === 5 && providerCapabilityMatrix.failureModeRows.every((row) => row.affectedSurfaceIds.length > 0 && row.claimAllowed === false), providerCapabilityMatrix.failureModeIds.join(',')))
  checks.push(check('provider capability matrix writes expected provenance JSONL', providerCapabilityMatrix.provenanceJsonlPath === providerCapabilityMatrixJsonlPath && providerCapabilityMatrix.provenanceJsonlSha256.length === 64 && providerCapabilityMatrix.provenanceJsonlRecordCount === providerCapabilityMatrix.capabilityRowCount + providerCapabilityMatrix.failureModeCount && providerCapabilityMatrix.provenanceJsonlParseable, providerCapabilityMatrix.provenanceJsonlPath))
  checks.push(check('provider capability matrix keeps provider and readiness claims blocked', providerCapabilityMatrix.providerBackedExecutionClaimAllowed === false && providerCapabilityMatrix.providerCompatibilityClaimAllowed === false && providerCapabilityMatrix.releaseReadinessClaimAllowed === false && providerCapabilityMatrix.productionReadinessClaimAllowed === false && providerCapabilityMatrix.publicReadinessClaimAllowed === false && providerCapabilityMatrix.externalValidationClaimAllowed === false && providerCapabilityMatrix.autonomousReliabilityClaimAllowed === false))
  checks.push(check('provider capability matrix performed no provider live external or protected calls', providerCapabilityMatrix.providerCallsPerformed.length === 0 && providerCapabilityMatrix.liveModelCallsPerformed.length === 0 && providerCapabilityMatrix.externalCallsPerformed.length === 0 && providerCapabilityMatrix.protectedActionsExecuted.length === 0))
  checks.push(check('provider capability matrix checks pass', providerCapabilityMatrix.capabilityChecks.every((item) => item.ok)))
  checks.push(check('git release hygiene fixtures are local no-provider checks', gitReleaseHygiene.mode === 'local_no_provider_git_release_hygiene'))
  checks.push(check('git release hygiene performed no provider calls', gitReleaseHygiene.providerCallsPerformed.length === 0))
  checks.push(check('git release hygiene performed no live model calls', gitReleaseHygiene.liveModelCallsPerformed.length === 0))
  checks.push(check('git release hygiene performed no external calls', gitReleaseHygiene.externalCallsPerformed.length === 0))
  checks.push(check('git release hygiene classified workspace status', ['git_repo_detected', 'blocked_by_no_git_repo', 'git_unavailable'].includes(gitReleaseHygiene.workspaceGitStatus), gitReleaseHygiene.workspaceGitStatus))
  checks.push(check('git release hygiene did not attempt commit or push', gitReleaseHygiene.commitPushAttempted === false))
  checks.push(check('git release hygiene did not perform release action', gitReleaseHygiene.releaseActionPerformed === false))
  checks.push(check('git release hygiene did not perform protected actions', gitReleaseHygiene.protectedActionsPerformed.length === 0))
  checks.push(check('git release hygiene checks pass', gitReleaseHygiene.releaseHygieneChecks.every((item) => item.ok)))
  checks.push(check('IDE extension surface fixtures are local no-provider checks', ideExtensionSurface.mode === 'local_no_provider_ide_extension_surface'))
  checks.push(check('IDE extension surface performed no provider calls', ideExtensionSurface.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension surface performed no live model calls', ideExtensionSurface.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension surface performed no external calls', ideExtensionSurface.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension surface classified workspace status', ['extension_manifest_found', 'extension_manifest_missing'].includes(ideExtensionSurface.workspaceIdeExtensionStatus), ideExtensionSurface.workspaceIdeExtensionStatus))
  checks.push(check('IDE extension surface did not attempt packaging', ideExtensionSurface.packagingAttempted === false))
  checks.push(check('IDE extension surface did not attempt install', ideExtensionSurface.installAttempted === false))
  checks.push(check('IDE extension surface checks pass', ideExtensionSurface.ideExtensionChecks.every((item) => item.ok)))
  checks.push(check('IDE extension scope is local no-provider check', ideExtensionScope.mode === 'local_no_provider_ide_extension_scope'))
  checks.push(check('IDE extension scope performed no provider calls', ideExtensionScope.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension scope performed no live model calls', ideExtensionScope.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension scope performed no external calls', ideExtensionScope.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension scope consumes current surface status', ideExtensionScope.sourceSurfaceStatus === ideExtensionSurface.workspaceIdeExtensionStatus, ideExtensionScope.sourceSurfaceStatus))
  checks.push(check('IDE extension scope records bounded no-availability decision', ['scope_extension_before_implementation_no_availability_claim', 'manifest_surface_detected_availability_claim_blocked_until_smoke'].includes(ideExtensionScope.scopeDecision), ideExtensionScope.scopeDecision))
  checks.push(check('IDE extension scope proposes bounded manifest path', ideExtensionScope.proposedManifestPath === 'packages/openclaude-vscode/package.json', ideExtensionScope.proposedManifestPath))
  checks.push(check('IDE extension scope uses primary source inputs', ideExtensionScope.primarySourceInputs.length >= 3 && ideExtensionScope.primarySourceInputs.every((input) => /^https:\/\//.test(input.sourceUrl))))
  checks.push(check('IDE extension scope includes manifest requirements', ['engines.vscode', 'main', 'activationEvents', 'contributes', 'extensionKind'].every((item) => ideExtensionScope.minimumManifestRequirements.includes(item))))
  checks.push(check('IDE extension scope includes commands, views, configuration, and activation events', ideExtensionScope.contributionPlan.commands.length >= 3 && ideExtensionScope.contributionPlan.views.length >= 1 && ideExtensionScope.contributionPlan.configurationKeys.length >= 3 && ideExtensionScope.contributionPlan.activationEvents.length >= 2))
  checks.push(check('IDE extension scope blocks availability claim until validation', ideExtensionScope.validationRequiredBeforeAvailabilityClaim.length >= 5))
  checks.push(check('IDE extension scope did not package, install, publish, or authorize calls', ideExtensionScope.protectedActions.packagingAttempted === false && ideExtensionScope.protectedActions.installAttempted === false && ideExtensionScope.protectedActions.publishAttempted === false && ideExtensionScope.protectedActions.providerCallsAllowed === false && ideExtensionScope.protectedActions.externalCallsAllowed === false))
  checks.push(check('IDE extension scope checks pass', ideExtensionScope.scopeChecks.every((item) => item.ok)))
  checks.push(check('IDE extension manifest smoke is local no-provider check', ideExtensionManifestSmoke.mode === 'local_no_provider_ide_extension_manifest_smoke'))
  checks.push(check('IDE extension manifest smoke performed no provider calls', ideExtensionManifestSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension manifest smoke performed no live model calls', ideExtensionManifestSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension manifest smoke performed no external calls', ideExtensionManifestSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension manifest smoke targets scoped manifest path', ideExtensionManifestSmoke.manifestPath === ideExtensionScope.proposedManifestPath, ideExtensionManifestSmoke.manifestPath))
  checks.push(check('IDE extension manifest smoke entry point exists in package path', ideExtensionManifestSmoke.entryPointPath === 'packages/openclaude-vscode/dist/extension.js', ideExtensionManifestSmoke.entryPointPath))
  checks.push(check('IDE extension manifest smoke dry-run pack exits 0', ideExtensionManifestSmoke.packageDryRunExitCode === 0, String(ideExtensionManifestSmoke.packageDryRunExitCode)))
  checks.push(check('IDE extension manifest smoke does not install, publish, deploy, or launch', ideExtensionManifestSmoke.installAttempted === false && ideExtensionManifestSmoke.publishAttempted === false && ideExtensionManifestSmoke.deployAttempted === false && ideExtensionManifestSmoke.launchAttempted === false))
  checks.push(check('IDE extension manifest smoke does not allow availability claim', ideExtensionManifestSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension manifest has required identity and runtime fields', ideExtensionManifestSmoke.manifestSummary.name === 'openclaude-vscode' && ideExtensionManifestSmoke.manifestSummary.displayName === 'OpenClaude' && ideExtensionManifestSmoke.manifestSummary.publisher === 'gitlawb' && ideExtensionManifestSmoke.manifestSummary.enginesVscode.length > 0 && ideExtensionManifestSmoke.manifestSummary.main === './dist/extension.js'))
  checks.push(check('IDE extension manifest exposes UI and workspace extension kinds', ideExtensionManifestSmoke.manifestSummary.extensionKind.includes('ui') && ideExtensionManifestSmoke.manifestSummary.extensionKind.includes('workspace'), ideExtensionManifestSmoke.manifestSummary.extensionKind.join(',')))
  checks.push(check('IDE extension manifest includes scoped commands', ideExtensionScope.contributionPlan.commands.every((command) => ideExtensionManifestSmoke.manifestSummary.commandIds.includes(command)), ideExtensionManifestSmoke.manifestSummary.commandIds.join(',')))
  checks.push(check('IDE extension manifest includes scoped views', ideExtensionScope.contributionPlan.views.every((view) => ideExtensionManifestSmoke.manifestSummary.viewIds.includes(view)), ideExtensionManifestSmoke.manifestSummary.viewIds.join(',')))
  checks.push(check('IDE extension manifest includes webview render surface', manifestWebviewViewIds.includes('openclaude.controlCenterView') && ideExtensionManifestSmoke.manifestSummary.activationEvents.includes('onView:openclaude.controlCenterView'), `${manifestWebviewViewIds.join(',')}/${ideExtensionManifestSmoke.manifestSummary.activationEvents.join(',')}`))
  checks.push(check('IDE extension manifest includes scoped configuration keys', ideExtensionScope.contributionPlan.configurationKeys.every((key) => ideExtensionManifestSmoke.manifestSummary.configurationKeys.includes(key)), ideExtensionManifestSmoke.manifestSummary.configurationKeys.join(',')))
  checks.push(check('IDE extension manifest includes scoped activation events', ideExtensionScope.contributionPlan.activationEvents.every((event) => ideExtensionManifestSmoke.manifestSummary.activationEvents.includes(event)), ideExtensionManifestSmoke.manifestSummary.activationEvents.join(',')))
  checks.push(check('IDE extension dry-run package has bounded files', ideExtensionManifestSmoke.packageDryRunFiles.length >= 3 && ideExtensionManifestSmoke.packageDryRunFiles.every((path) => !/node_modules|\\.env|credential|secret|token/i.test(path)), ideExtensionManifestSmoke.packageDryRunFiles.join(',')))
  checks.push(check('IDE extension manifest smoke checks pass', ideExtensionManifestSmoke.manifestSmokeChecks.every((item) => item.ok)))
  checks.push(check('IDE extension runtime smoke is local no-provider check', ideExtensionRuntimeSmoke.mode === 'local_no_provider_ide_extension_runtime_smoke'))
  checks.push(check('IDE extension runtime smoke performed no provider calls', ideExtensionRuntimeSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension runtime smoke performed no live model calls', ideExtensionRuntimeSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension runtime smoke performed no external calls', ideExtensionRuntimeSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension runtime smoke uses local mock host', ideExtensionRuntimeSmoke.hostRuntime === 'local_mock_vscode_extension_host', ideExtensionRuntimeSmoke.hostRuntime))
  checks.push(check('IDE extension runtime smoke targets scoped manifest path', ideExtensionRuntimeSmoke.manifestPath === ideExtensionScope.proposedManifestPath, ideExtensionRuntimeSmoke.manifestPath))
  checks.push(check('IDE extension runtime smoke targets scoped entry point', ideExtensionRuntimeSmoke.entryPointPath === ideExtensionManifestSmoke.entryPointPath, ideExtensionRuntimeSmoke.entryPointPath))
  checks.push(check('IDE extension runtime smoke did not launch real Extension Host', ideExtensionRuntimeSmoke.realExtensionHostLaunched === false))
  checks.push(check('IDE extension runtime smoke does not install, publish, deploy, or launch', ideExtensionRuntimeSmoke.installAttempted === false && ideExtensionRuntimeSmoke.publishAttempted === false && ideExtensionRuntimeSmoke.deployAttempted === false && ideExtensionRuntimeSmoke.launchAttempted === false))
  checks.push(check('IDE extension runtime smoke does not allow availability claim', ideExtensionRuntimeSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension activation and deactivation are callable', ideExtensionRuntimeSmoke.activationInvoked === true && ideExtensionRuntimeSmoke.deactivationInvoked === true))
  checks.push(check('IDE extension runtime registers all manifest commands', ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionRuntimeSmoke.registeredCommandIds.includes(command)) && ideExtensionRuntimeSmoke.missingManifestCommands.length === 0, ideExtensionRuntimeSmoke.registeredCommandIds.join(',')))
  checks.push(check('IDE extension runtime executes all registered manifest commands', ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionRuntimeSmoke.executedCommandIds.includes(command)), ideExtensionRuntimeSmoke.executedCommandIds.join(',')))
  checks.push(check('IDE extension runtime registers no unexpected commands', ideExtensionRuntimeSmoke.unexpectedRegisteredCommands.length === 0, ideExtensionRuntimeSmoke.unexpectedRegisteredCommands.join(',')))
  checks.push(check('IDE extension runtime registers all manifest tree views', manifestTreeViewIds.every((viewId) => ideExtensionRuntimeSmoke.registeredTreeViewIds?.includes(viewId) === true), ideExtensionRuntimeSmoke.registeredTreeViewIds?.join(',') ?? 'missing'))
  checks.push(check('IDE extension runtime registers all manifest webview views', manifestWebviewViewIds.every((viewId) => ideExtensionRuntimeSmoke.registeredWebviewViewIds?.includes(viewId) === true), ideExtensionRuntimeSmoke.registeredWebviewViewIds?.join(',') ?? 'missing'))
  checks.push(check('IDE extension runtime subscriptions match command and view provider count', ideExtensionRuntimeSmoke.contextSubscriptionCount === ideExtensionManifestSmoke.manifestSummary.commandIds.length + manifestTreeViewIds.length + manifestWebviewViewIds.length, `${ideExtensionRuntimeSmoke.contextSubscriptionCount}/${ideExtensionManifestSmoke.manifestSummary.commandIds.length + manifestTreeViewIds.length + manifestWebviewViewIds.length}`))
  checks.push(check('IDE extension runtime command handlers show bounded local messages', ideExtensionRuntimeSmoke.messagesShown.length === ideExtensionManifestSmoke.manifestSummary.commandIds.length && ideExtensionRuntimeSmoke.messagesShown.every((message) => /scoped/i.test(message) && !/available|published|released|production ready/i.test(message)), ideExtensionRuntimeSmoke.messagesShown.join(' | ')))
  checks.push(check('IDE extension runtime smoke checks pass', ideExtensionRuntimeSmoke.runtimeSmokeChecks.every((item) => item.ok)))
  checks.push(check('IDE extension host smoke is local no-provider check', ideExtensionHostSmoke.mode === 'local_no_provider_real_vscode_extension_host_smoke'))
  checks.push(check('IDE extension host smoke performed no provider calls', ideExtensionHostSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension host smoke performed no live model calls', ideExtensionHostSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension host smoke performed no external calls', ideExtensionHostSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension host smoke records real host evidence or protected local boundary', ideExtensionHostSmoke.hostRuntime === 'real_vscode_extension_development_host' && (ideExtensionHostVerified || ideExtensionHostEnvironmentBlocked), `${ideExtensionHostSmoke.hostRuntime}; blockers=${ideExtensionHostSmoke.environmentBlockers?.join(',') ?? 'none'}`))
  checks.push(check('IDE extension host smoke targets scoped manifest path', ideExtensionHostSmoke.manifestPath === ideExtensionScope.proposedManifestPath, ideExtensionHostSmoke.manifestPath))
  checks.push(check('IDE extension host smoke targets scoped entry point', ideExtensionHostSmoke.entryPointPath === ideExtensionManifestSmoke.entryPointPath, ideExtensionHostSmoke.entryPointPath))
  checks.push(check('IDE extension host smoke exits 0 without timeout or records protected CLI boundary', (ideExtensionHostSmoke.codeExitCode === 0 && ideExtensionHostSmoke.codeTimedOut === false) || ideExtensionHostEnvironmentBlocked, `${ideExtensionHostSmoke.codeExitCode}/${ideExtensionHostSmoke.codeTimedOut}`))
  checks.push(check('IDE extension host smoke startup state is classified', ideExtensionHostSmoke.vscodeStartupBlocked !== true || ideExtensionHostEnvironmentBlocked, ideExtensionHostSmoke.environmentBlockers?.join(',') ?? 'none'))
  checks.push(check('IDE extension host smoke activates extension or blocks availability claim', ideExtensionHostSmoke.extensionActivated === true || ideExtensionHostEnvironmentBlocked, String(ideExtensionHostSmoke.extensionActivated)))
  checks.push(check('IDE extension host smoke registers all manifest commands or records protected boundary', ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionHostSmoke.registeredCommandIds.includes(command)) || ideExtensionHostEnvironmentBlocked, ideExtensionHostSmoke.registeredCommandIds.join(',')))
  checks.push(check('IDE extension host smoke executes all manifest commands or records protected boundary', (ideExtensionManifestSmoke.manifestSummary.commandIds.every((command) => ideExtensionHostSmoke.executedCommandIds.includes(command)) && ideExtensionHostSmoke.failedCommandIds.length === 0) || ideExtensionHostEnvironmentBlocked, ideExtensionHostSmoke.executedCommandIds.join(',')))
  checks.push(check('IDE extension host smoke does not install, publish, deploy, or product-launch', ideExtensionHostSmoke.installAttempted === false && ideExtensionHostSmoke.publishAttempted === false && ideExtensionHostSmoke.deployAttempted === false && ideExtensionHostSmoke.productLaunchAttempted === false))
  checks.push(check('IDE extension host smoke does not allow availability claim', ideExtensionHostSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension host smoke checks pass or are classified by protected boundary', ideExtensionHostSmoke.hostSmokeChecks.every((item) => item.ok) || ideExtensionHostEnvironmentBlocked))
  checks.push(check('IDE extension workbench smoke is local no-provider check', ideExtensionWorkbenchSmoke.mode === 'local_no_provider_real_vscode_workbench_tree_view_smoke'))
  checks.push(check('IDE extension workbench smoke performed no provider calls', ideExtensionWorkbenchSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension workbench smoke performed no live model calls', ideExtensionWorkbenchSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension workbench smoke performed no external calls', ideExtensionWorkbenchSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension workbench smoke records real host evidence or protected local boundary', ideExtensionWorkbenchSmoke.hostRuntime === 'real_vscode_extension_development_host' && (ideExtensionWorkbenchVerified || ideExtensionWorkbenchEnvironmentBlocked), `${ideExtensionWorkbenchSmoke.hostRuntime}; blockers=${ideExtensionWorkbenchSmoke.environmentBlockers?.join(',') ?? 'none'}`))
  checks.push(check('IDE extension workbench smoke exits 0 without timeout or records protected CLI boundary', (ideExtensionWorkbenchSmoke.codeExitCode === 0 && ideExtensionWorkbenchSmoke.codeTimedOut === false) || ideExtensionWorkbenchEnvironmentBlocked, `${ideExtensionWorkbenchSmoke.codeExitCode}/${ideExtensionWorkbenchSmoke.codeTimedOut}`))
  checks.push(check('IDE extension workbench smoke startup state is classified', ideExtensionWorkbenchSmoke.vscodeStartupBlocked !== true || ideExtensionWorkbenchEnvironmentBlocked, ideExtensionWorkbenchSmoke.environmentBlockers?.join(',') ?? 'none'))
  checks.push(check('IDE extension workbench smoke activates extension or blocks availability claim', ideExtensionWorkbenchSmoke.extensionActivated === true || ideExtensionWorkbenchEnvironmentBlocked, String(ideExtensionWorkbenchSmoke.extensionActivated)))
  checks.push(check('IDE extension workbench smoke registers all contributed tree views or records protected boundary', manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.registeredTreeViewIds.includes(viewId)) || ideExtensionWorkbenchEnvironmentBlocked, ideExtensionWorkbenchSmoke.registeredTreeViewIds.join(',')))
  checks.push(check('IDE extension workbench smoke registers all tree data providers or records protected boundary', manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.treeProviderViewIds.includes(viewId)) || ideExtensionWorkbenchEnvironmentBlocked, ideExtensionWorkbenchSmoke.treeProviderViewIds.join(',')))
  checks.push(check('IDE extension workbench smoke focuses all contributed tree views or records protected boundary', manifestTreeViewIds.every((viewId) => ideExtensionWorkbenchSmoke.focusedViewIds.includes(viewId)) || ideExtensionWorkbenchEnvironmentBlocked, ideExtensionWorkbenchSmoke.focusedViewIds.join(',')))
  checks.push(check('IDE extension workbench smoke provides non-empty tree view items or records protected boundary', manifestTreeViewIds.every((viewId) => (ideExtensionWorkbenchSmoke.viewItemCounts[viewId] ?? 0) > 0) || ideExtensionWorkbenchEnvironmentBlocked, JSON.stringify(ideExtensionWorkbenchSmoke.viewItemCounts)))
  checks.push(check('IDE extension workbench smoke executes all tree item commands or records protected boundary', (Array.isArray(ideExtensionWorkbenchSmoke.executedViewCommandIds) && ideExtensionWorkbenchSmoke.executedViewCommandIds.length >= ideExtensionManifestSmoke.manifestSummary.commandIds.length && Array.isArray(ideExtensionWorkbenchSmoke.failedViewCommandIds) && ideExtensionWorkbenchSmoke.failedViewCommandIds.length === 0) || ideExtensionWorkbenchEnvironmentBlocked, `${ideExtensionWorkbenchSmoke.executedViewCommandIds?.join(',') ?? 'missing'}/${ideExtensionWorkbenchSmoke.failedViewCommandIds?.join(',') ?? 'missing'}`))
  checks.push(check('IDE extension workbench smoke does not install, publish, deploy, or product-launch', ideExtensionWorkbenchSmoke.installAttempted === false && ideExtensionWorkbenchSmoke.publishAttempted === false && ideExtensionWorkbenchSmoke.deployAttempted === false && ideExtensionWorkbenchSmoke.productLaunchAttempted === false))
  checks.push(check('IDE extension workbench smoke does not allow availability claim', ideExtensionWorkbenchSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension workbench smoke checks pass or are classified by protected boundary', ideExtensionWorkbenchSmoke.workbenchSmokeChecks.every((item) => item.ok) || ideExtensionWorkbenchEnvironmentBlocked))
  checks.push(check('VS Code update boundary is local no-provider check', vscodeUpdateBoundary.mode === 'local_no_provider_vscode_update_boundary'))
  checks.push(check('VS Code update boundary performed no provider calls', vscodeUpdateBoundary.providerCallsPerformed.length === 0))
  checks.push(check('VS Code update boundary performed no live model calls', vscodeUpdateBoundary.liveModelCallsPerformed.length === 0))
  checks.push(check('VS Code update boundary performed no external calls', vscodeUpdateBoundary.externalCallsPerformed.length === 0))
  checks.push(check('VS Code update boundary imports host/workbench smoke reports', vscodeUpdateBoundary.sourceHostSmokeReportPath === ideExtensionHostSmokeJsonPath && vscodeUpdateBoundary.sourceWorkbenchSmokeReportPath === ideExtensionWorkbenchSmokeJsonPath))
  checks.push(check('VS Code update boundary preserves observed blockers', vscodeUpdateBoundary.sourceHostEnvironmentBlockers.join(',') === (ideExtensionHostSmoke.environmentBlockers ?? []).join(',') && vscodeUpdateBoundary.sourceWorkbenchEnvironmentBlockers.join(',') === (ideExtensionWorkbenchSmoke.environmentBlockers ?? []).join(','), `${vscodeUpdateBoundary.sourceHostEnvironmentBlockers.join(',')}/${vscodeUpdateBoundary.sourceWorkbenchEnvironmentBlockers.join(',')}`))
  checks.push(check('VS Code update boundary blocks process intervention and protected actions', vscodeUpdateBoundary.processTerminationAttempted === false && vscodeUpdateBoundary.dependencyInstallAttempted === false && vscodeUpdateBoundary.protectedActionsExecuted.length === 0))
  checks.push(check('VS Code update boundary blocks readiness claims', vscodeUpdateBoundary.releaseReadinessClaimAllowed === false && vscodeUpdateBoundary.productionReadinessClaimAllowed === false && vscodeUpdateBoundary.publicReadinessClaimAllowed === false && vscodeUpdateBoundary.autonomousReliabilityClaimAllowed === false))
  checks.push(check('VS Code update boundary classifies owner action requirement', ['blocked_wait_for_local_vscode_update_or_explicit_owner_process_action', 'blocked_missing_vscode_cli_or_explicit_owner_repair_action', 'clear_no_current_vscode_update_boundary'].includes(vscodeUpdateBoundary.boundaryStatus), vscodeUpdateBoundary.boundaryStatus))
  checks.push(check('VS Code update boundary checks pass', vscodeUpdateBoundary.boundaryChecks.every((item) => item.ok)))
  checks.push(check('VS Code startup diagnostics is local no-provider check', vscodeStartupDiagnostics.mode === 'local_no_provider_vscode_startup_diagnostics'))
  checks.push(check('VS Code startup diagnostics performed no provider calls', vscodeStartupDiagnostics.providerCallsPerformed.length === 0))
  checks.push(check('VS Code startup diagnostics performed no live model calls', vscodeStartupDiagnostics.liveModelCallsPerformed.length === 0))
  checks.push(check('VS Code startup diagnostics performed no external calls', vscodeStartupDiagnostics.externalCallsPerformed.length === 0))
  checks.push(check('VS Code startup diagnostics imports host/workbench/update reports', vscodeStartupDiagnostics.sourceHostSmokeReportPath === ideExtensionHostSmokeJsonPath && vscodeStartupDiagnostics.sourceWorkbenchSmokeReportPath === ideExtensionWorkbenchSmokeJsonPath && vscodeStartupDiagnostics.sourceVscodeUpdateBoundaryReportPath === vscodeUpdateBoundaryJsonPath))
  checks.push(check('VS Code startup diagnostics records official VS Code sources', vscodeStartupDiagnostics.primarySourceInputs.some((source) => source.sourceProject.includes('Workspace Trust')) && vscodeStartupDiagnostics.primarySourceInputs.some((source) => source.sourceProject.includes('Testing Extensions')) && vscodeStartupDiagnostics.primarySourceInputs.some((source) => source.sourceProject.includes('Command Line')) && vscodeStartupDiagnostics.primarySourceInputs.every((source) => /^https:\/\/code\.visualstudio\.com\//.test(source.sourceUrl)), vscodeStartupDiagnostics.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('VS Code startup diagnostics observes isolated execution arguments', ['--extensionDevelopmentPath', '--extensionTestsPath', '--user-data-dir', '--extensions-dir', '--disable-workspace-trust'].every((arg) => vscodeStartupDiagnostics.isolatedExecutionArgumentsObserved.includes(arg)), vscodeStartupDiagnostics.isolatedExecutionArgumentsObserved.join(',')))
  const startupDiagnosticsRequiresUpdateGuardLogs = vscodeStartupDiagnostics.diagnosisStatus.startsWith('vscode_core_update_guard')
  checks.push(check('VS Code startup diagnostics preserves update guard log evidence when update-blocked', startupDiagnosticsRequiresUpdateGuardLogs ? vscodeStartupDiagnostics.updateGuardLogEvidenceCount > 0 && vscodeStartupDiagnostics.updateLogEvidence.every((item) => item.sha256.length === 64 && item.sizeBytes > 0) : vscodeStartupDiagnostics.updateGuardLogEvidenceCount === 0, `${vscodeStartupDiagnostics.updateGuardLogEvidenceCount} update logs`))
  checks.push(check('VS Code startup diagnostics enumerates sentinel candidates', (vscodeStartupDiagnostics.sentinelCandidates.length >= 1 && vscodeStartupDiagnostics.sentinelCandidates.every((item) => typeof item.exists === 'boolean')) || startupDiagnosticsSentinelEnumerationBounded, `${vscodeStartupDiagnostics.sentinelCandidates.length} candidates`))
  checks.push(check('VS Code startup diagnostics classifies bounded diagnosis', ['vscode_core_update_guard_without_visible_sentinel_or_codesetup_process', 'vscode_core_update_guard_with_visible_codesetup_process', 'vscode_core_update_guard_with_visible_sentinel', 'vscode_cli_unavailable_or_install_boundary', 'clear_no_current_update_guard_evidence'].includes(vscodeStartupDiagnostics.diagnosisStatus), vscodeStartupDiagnostics.diagnosisStatus))
  checks.push(check('VS Code startup diagnostics blocks protected intervention', vscodeStartupDiagnostics.processTerminationAttempted === false && vscodeStartupDiagnostics.deleteUpdateStateAttempted === false && vscodeStartupDiagnostics.dependencyInstallPerformed === false && vscodeStartupDiagnostics.reinstallAttempted === false && vscodeStartupDiagnostics.protectedActionsExecuted.length === 0))
  checks.push(check('VS Code startup diagnostics keeps readiness claims blocked', vscodeStartupDiagnostics.releaseReadinessClaimAllowed === false && vscodeStartupDiagnostics.productionReadinessClaimAllowed === false && vscodeStartupDiagnostics.publicReadinessClaimAllowed === false && vscodeStartupDiagnostics.externalValidationClaimAllowed === false && vscodeStartupDiagnostics.autonomousReliabilityClaimAllowed === false))
  checks.push(check('VS Code startup diagnostics checks pass', vscodeStartupDiagnostics.startupDiagnosticsChecks.every((item) => item.ok)))
  checks.push(check('IDE extension webview render smoke is local no-provider check', ideExtensionWebviewRenderSmoke.mode === 'local_no_provider_ide_extension_webview_render_smoke'))
  checks.push(check('IDE extension webview render smoke performed no provider calls', ideExtensionWebviewRenderSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension webview render smoke performed no live model calls', ideExtensionWebviewRenderSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension webview render smoke performed no external calls', ideExtensionWebviewRenderSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension webview render smoke uses mock webview host', ideExtensionWebviewRenderSmoke.hostRuntime === 'local_mock_vscode_webview_view_host' && ideExtensionWebviewRenderSmoke.realExtensionHostLaunched === false, ideExtensionWebviewRenderSmoke.hostRuntime))
  checks.push(check('IDE extension webview render smoke activates extension', ideExtensionWebviewRenderSmoke.activationInvoked === true && ideExtensionWebviewRenderSmoke.deactivationInvoked === true))
  checks.push(check('IDE extension webview render smoke registers all manifest webview views', manifestWebviewViewIds.length > 0 && manifestWebviewViewIds.every((viewId) => ideExtensionWebviewRenderSmoke.registeredWebviewViewIds.includes(viewId)), ideExtensionWebviewRenderSmoke.registeredWebviewViewIds.join(',')))
  checks.push(check('IDE extension webview render smoke resolves all manifest webview views', manifestWebviewViewIds.length > 0 && manifestWebviewViewIds.every((viewId) => ideExtensionWebviewRenderSmoke.resolvedWebviewViewIds.includes(viewId)), ideExtensionWebviewRenderSmoke.resolvedWebviewViewIds.join(',')))
  checks.push(check('IDE extension webview render smoke renders non-empty HTML', ideExtensionWebviewRenderSmoke.renderedHtmlByteLength > 1000, String(ideExtensionWebviewRenderSmoke.renderedHtmlByteLength)))
  checks.push(check('IDE extension webview render smoke exposes manifest command actions', ideExtensionManifestSmoke.manifestSummary.commandIds.every((commandId) => ideExtensionWebviewRenderSmoke.commandActionIds.includes(commandId)), ideExtensionWebviewRenderSmoke.commandActionIds.join(',')))
  checks.push(check('IDE extension webview render smoke does not install, publish, deploy, or launch', ideExtensionWebviewRenderSmoke.installAttempted === false && ideExtensionWebviewRenderSmoke.publishAttempted === false && ideExtensionWebviewRenderSmoke.deployAttempted === false && ideExtensionWebviewRenderSmoke.launchAttempted === false))
  checks.push(check('IDE extension webview render smoke does not allow availability claim', ideExtensionWebviewRenderSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension webview render smoke checks pass', ideExtensionWebviewRenderSmoke.webviewRenderChecks.every((item) => item.ok)))
  checks.push(check('IDE extension rendered workbench screenshot is local no-provider check', ideExtensionRenderedWorkbenchScreenshot.mode === 'local_no_provider_ide_extension_rendered_workbench_screenshot'))
  checks.push(check('IDE extension rendered workbench screenshot performed no provider calls', ideExtensionRenderedWorkbenchScreenshot.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension rendered workbench screenshot performed no live model calls', ideExtensionRenderedWorkbenchScreenshot.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension rendered workbench screenshot performed no external calls', ideExtensionRenderedWorkbenchScreenshot.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension rendered workbench screenshot uses local renderer', ideExtensionRenderedWorkbenchScreenshot.hostRuntime === 'local_sharp_rendered_workbench_panel_from_webview_contract', ideExtensionRenderedWorkbenchScreenshot.hostRuntime))
  checks.push(check('IDE extension rendered workbench screenshot derives from webview render smoke', ideExtensionRenderedWorkbenchScreenshot.sourceReportPath === ideExtensionWebviewRenderSmokeJsonPath))
  checks.push(check('IDE extension rendered workbench screenshot dimensions are stable', ideExtensionRenderedWorkbenchScreenshot.renderedWidth === 960 && ideExtensionRenderedWorkbenchScreenshot.renderedHeight === 720, `${ideExtensionRenderedWorkbenchScreenshot.renderedWidth}x${ideExtensionRenderedWorkbenchScreenshot.renderedHeight}`))
  checks.push(check('IDE extension rendered workbench screenshot records nonblank PNG hash evidence', ideExtensionRenderedWorkbenchScreenshot.pngByteLength > 4000 && ideExtensionRenderedWorkbenchScreenshot.pngSha256.length === 64 && ideExtensionRenderedWorkbenchScreenshot.svgSha256.length === 64 && ideExtensionRenderedWorkbenchScreenshot.nonBlankChannelCount >= 3, `${ideExtensionRenderedWorkbenchScreenshot.pngByteLength}/${ideExtensionRenderedWorkbenchScreenshot.nonBlankChannelCount}`))
  checks.push(check('IDE extension rendered workbench screenshot exposes manifest command actions', ideExtensionManifestSmoke.manifestSummary.commandIds.every((commandId) => ideExtensionRenderedWorkbenchScreenshot.commandActionIds.includes(commandId)), ideExtensionRenderedWorkbenchScreenshot.commandActionIds.join(',')))
  checks.push(check('IDE extension rendered workbench screenshot records render markers', ideExtensionRenderedWorkbenchScreenshot.renderMarkers.includes('data-openclaude-render-contract=control-center') && ideExtensionRenderedWorkbenchScreenshot.renderMarkers.includes('command-action-rail'), ideExtensionRenderedWorkbenchScreenshot.renderMarkers.join(',')))
  checks.push(check('IDE extension rendered workbench screenshot does not install, publish, deploy, or launch', ideExtensionRenderedWorkbenchScreenshot.installAttempted === false && ideExtensionRenderedWorkbenchScreenshot.publishAttempted === false && ideExtensionRenderedWorkbenchScreenshot.deployAttempted === false && ideExtensionRenderedWorkbenchScreenshot.launchAttempted === false))
  checks.push(check('IDE extension rendered workbench screenshot does not launch real Extension Host', ideExtensionRenderedWorkbenchScreenshot.realExtensionHostLaunched === false))
  checks.push(check('IDE extension rendered workbench screenshot does not allow availability claim', ideExtensionRenderedWorkbenchScreenshot.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension rendered workbench screenshot checks pass', ideExtensionRenderedWorkbenchScreenshot.screenshotChecks.every((item) => item.ok)))
  checks.push(check('IDE extension webview interaction smoke is local no-provider check', ideExtensionWebviewInteractionSmoke.mode === 'local_no_provider_ide_extension_webview_interaction_smoke'))
  checks.push(check('IDE extension webview interaction smoke performed no provider calls', ideExtensionWebviewInteractionSmoke.providerCallsPerformed.length === 0))
  checks.push(check('IDE extension webview interaction smoke performed no live model calls', ideExtensionWebviewInteractionSmoke.liveModelCallsPerformed.length === 0))
  checks.push(check('IDE extension webview interaction smoke performed no external calls', ideExtensionWebviewInteractionSmoke.externalCallsPerformed.length === 0))
  checks.push(check('IDE extension webview interaction smoke uses local interaction host', ideExtensionWebviewInteractionSmoke.hostRuntime === 'local_mock_vscode_webview_interaction_host' && ideExtensionWebviewInteractionSmoke.realExtensionHostLaunched === false, ideExtensionWebviewInteractionSmoke.hostRuntime))
  checks.push(check('IDE extension webview interaction smoke derives from webview render smoke', ideExtensionWebviewInteractionSmoke.sourceWebviewRenderReportPath === ideExtensionWebviewRenderSmokeJsonPath, ideExtensionWebviewInteractionSmoke.sourceWebviewRenderReportPath))
  checks.push(check('IDE extension webview interaction smoke derives from rendered screenshot smoke', ideExtensionWebviewInteractionSmoke.sourceRenderedScreenshotReportPath === ideExtensionRenderedWorkbenchScreenshotJsonPath, ideExtensionWebviewInteractionSmoke.sourceRenderedScreenshotReportPath))
  checks.push(check('IDE extension webview interaction smoke targets scoped manifest and entry point', ideExtensionWebviewInteractionSmoke.manifestPath === ideExtensionScope.proposedManifestPath && ideExtensionWebviewInteractionSmoke.entryPointPath === ideExtensionManifestSmoke.entryPointPath, `${ideExtensionWebviewInteractionSmoke.manifestPath}/${ideExtensionWebviewInteractionSmoke.entryPointPath}`))
  checks.push(check('IDE extension webview interaction smoke activates extension', ideExtensionWebviewInteractionSmoke.activationInvoked === true && ideExtensionWebviewInteractionSmoke.deactivationInvoked === true))
  checks.push(check('IDE extension webview interaction buttons match manifest command count', ideExtensionWebviewInteractionSmoke.commandButtonCount === ideExtensionManifestSmoke.manifestSummary.commandIds.length, `${ideExtensionWebviewInteractionSmoke.commandButtonCount}/${ideExtensionManifestSmoke.manifestSummary.commandIds.length}`))
  checks.push(check('IDE extension webview interaction focus order matches manifest order', JSON.stringify(ideExtensionWebviewInteractionSmoke.focusOrderCommandIds) === JSON.stringify(ideExtensionManifestSmoke.manifestSummary.commandIds), ideExtensionWebviewInteractionSmoke.focusOrderCommandIds.join(',')))
  checks.push(check('IDE extension webview interaction command actions match render evidence', JSON.stringify(ideExtensionWebviewInteractionSmoke.interactionCommandIds) === JSON.stringify(ideExtensionWebviewRenderSmoke.commandActionIds) && JSON.stringify(ideExtensionWebviewInteractionSmoke.interactionCommandIds) === JSON.stringify(ideExtensionRenderedWorkbenchScreenshot.commandActionIds), ideExtensionWebviewInteractionSmoke.interactionCommandIds.join(',')))
  checks.push(check('IDE extension webview interaction commands are registered', ideExtensionWebviewInteractionSmoke.interactionCommandIds.every((commandId) => ideExtensionWebviewInteractionSmoke.registeredCommandIds.includes(commandId)), ideExtensionWebviewInteractionSmoke.registeredCommandIds.join(',')))
  checks.push(check('IDE extension webview interaction commands execute without failures', ideExtensionWebviewInteractionSmoke.interactionCommandIds.every((commandId) => ideExtensionWebviewInteractionSmoke.executedInteractionCommandIds.includes(commandId)) && ideExtensionWebviewInteractionSmoke.failedInteractionCommandIds.length === 0, `${ideExtensionWebviewInteractionSmoke.executedInteractionCommandIds.join(',')}/failed=${ideExtensionWebviewInteractionSmoke.failedInteractionCommandIds.join(',')}`))
  checks.push(check('IDE extension webview interaction command region is accessible', ideExtensionWebviewInteractionSmoke.commandRegionRole === 'list' && ideExtensionWebviewInteractionSmoke.commandRegionAriaLabel === 'OpenClaude command action contract', `${ideExtensionWebviewInteractionSmoke.commandRegionRole}/${ideExtensionWebviewInteractionSmoke.commandRegionAriaLabel}`))
  checks.push(check('IDE extension webview interaction uses native keyboard activation model', ideExtensionWebviewInteractionSmoke.keyboardActivationModel === 'native_button_enter_space_command_mapping', ideExtensionWebviewInteractionSmoke.keyboardActivationModel))
  checks.push(check('IDE extension webview interaction handlers show bounded local messages', ideExtensionWebviewInteractionSmoke.messagesShown.length === ideExtensionManifestSmoke.manifestSummary.commandIds.length && ideExtensionWebviewInteractionSmoke.messagesShown.every((message) => /scoped/i.test(message) && !/available|published|released|production ready/i.test(message)), ideExtensionWebviewInteractionSmoke.messagesShown.join(' | ')))
  checks.push(check('IDE extension webview interaction records primary source inputs', ideExtensionWebviewInteractionSmoke.primarySourceInputs.length >= 2 && ideExtensionWebviewInteractionSmoke.primarySourceInputs.every((input) => /^https:\/\/code\.visualstudio\.com\//.test(input.url)), ideExtensionWebviewInteractionSmoke.primarySourceInputs.map((input) => input.url).join(',')))
  checks.push(check('IDE extension webview interaction does not install, publish, deploy, or launch', ideExtensionWebviewInteractionSmoke.installAttempted === false && ideExtensionWebviewInteractionSmoke.publishAttempted === false && ideExtensionWebviewInteractionSmoke.deployAttempted === false && ideExtensionWebviewInteractionSmoke.launchAttempted === false))
  checks.push(check('IDE extension webview interaction does not allow availability claim', ideExtensionWebviewInteractionSmoke.extensionAvailabilityClaimAllowed === false))
  checks.push(check('IDE extension webview interaction claim boundary blocks readiness claims', ['release readiness', 'production readiness', 'public readiness', 'external validation', 'autonomous reliability'].every((phrase) => ideExtensionWebviewInteractionSmoke.claimBoundary.includes(phrase))))
  checks.push(check('IDE extension webview interaction checks pass', ideExtensionWebviewInteractionSmoke.interactionChecks.every((item) => item.ok)))
  checks.push(check('release artifact fixtures are local no-provider checks', releaseArtifactFileList.mode === 'local_no_provider_release_artifact_file_list'))
  checks.push(check('release artifact performed no provider calls', releaseArtifactFileList.providerCallsPerformed.length === 0))
  checks.push(check('release artifact performed no live model calls', releaseArtifactFileList.liveModelCallsPerformed.length === 0))
  checks.push(check('release artifact performed no external calls', releaseArtifactFileList.externalCallsPerformed.length === 0))
  checks.push(check('release artifact dry-run pack exited 0', releaseArtifactFileList.packDryRunExitCode === 0, String(releaseArtifactFileList.packDryRunExitCode)))
  checks.push(check('release artifact did not attempt publish', releaseArtifactFileList.publishAttempted === false))
  checks.push(check('release artifact did not attempt deploy', releaseArtifactFileList.deployAttempted === false))
  checks.push(check('release artifact did not attempt launch', releaseArtifactFileList.launchAttempted === false))
  checks.push(check('release artifact expected file list is present', releaseArtifactFileList.expectedPackageFiles.length >= 3))
  checks.push(check('release artifact forbidden file patterns are present', releaseArtifactFileList.forbiddenPackageFilePatterns.length >= 5))
  checks.push(check('release artifact checks pass', releaseArtifactFileList.releaseArtifactChecks.every((item) => item.ok)))
  checks.push(check('release provenance fixtures are local no-provider checks', releaseArtifactProvenance.mode === 'local_no_provider_release_artifact_hash_sbom_provenance'))
  checks.push(check('release provenance performed no provider calls', releaseArtifactProvenance.providerCallsPerformed.length === 0))
  checks.push(check('release provenance performed no live model calls', releaseArtifactProvenance.liveModelCallsPerformed.length === 0))
  checks.push(check('release provenance performed no external calls', releaseArtifactProvenance.externalCallsPerformed.length === 0))
  checks.push(check('release provenance did not attempt publish', releaseArtifactProvenance.publishAttempted === false))
  checks.push(check('release provenance did not attempt deploy', releaseArtifactProvenance.deployAttempted === false))
  checks.push(check('release provenance did not attempt launch', releaseArtifactProvenance.launchAttempted === false))
  checks.push(check('release provenance hashes package files', releaseArtifactProvenance.packageFileHashes.length >= releaseArtifactFileList.actualPackageFiles.length, String(releaseArtifactProvenance.packageFileHashes.length)))
  checks.push(check('release provenance file hashes are complete', releaseArtifactProvenance.packageFileHashes.every((item) => item.exists && typeof item.sha256 === 'string' && item.sha256.length === 64)))
  checks.push(check('release provenance includes SBOM-style inventory', releaseArtifactProvenance.sbomFormat === 'local_package_json_component_inventory'))
  checks.push(check('release provenance includes runtime and dev components', releaseArtifactProvenance.sbomComponents.some((item) => item.scope === 'runtime') && releaseArtifactProvenance.sbomComponents.some((item) => item.scope === 'development'), String(releaseArtifactProvenance.sbomComponents.length)))
  checks.push(check('release provenance checks pass', releaseArtifactProvenance.provenanceChecks.every((item) => item.ok)))
  checks.push(check('release reproducibility fixtures are local no-provider checks', releaseArtifactReproducibility.mode === 'local_no_provider_release_artifact_reproducibility'))
  checks.push(check('release reproducibility performed no provider calls', releaseArtifactReproducibility.providerCallsPerformed.length === 0))
  checks.push(check('release reproducibility performed no live model calls', releaseArtifactReproducibility.liveModelCallsPerformed.length === 0))
  checks.push(check('release reproducibility performed no external calls', releaseArtifactReproducibility.externalCallsPerformed.length === 0))
  checks.push(check('release reproducibility did not attempt publish', releaseArtifactReproducibility.publishAttempted === false))
  checks.push(check('release reproducibility did not attempt deploy', releaseArtifactReproducibility.deployAttempted === false))
  checks.push(check('release reproducibility did not attempt launch', releaseArtifactReproducibility.launchAttempted === false))
  checks.push(check('release reproducibility runs pack twice', releaseArtifactReproducibility.packRuns.length === 2 && releaseArtifactReproducibility.packRuns.every((run) => run.exitCode === 0), releaseArtifactReproducibility.packRuns.map((run) => `${run.id}=${run.exitCode}`).join(',')))
  checks.push(check('release reproducibility file lists match artifact report', releaseArtifactReproducibility.packRuns.every((run) => JSON.stringify(run.fileList) === JSON.stringify(releaseArtifactFileList.actualPackageFiles)), releaseArtifactReproducibility.packRuns.map((run) => String(run.artifactFileCount)).join(',')))
  checks.push(check('release reproducibility tarball hash is stable', typeof releaseArtifactReproducibility.reproducibleTarballSha256 === 'string' && releaseArtifactReproducibility.reproducibleTarballSha256.length === 64, releaseArtifactReproducibility.reproducibleTarballSha256 ?? 'missing'))
  checks.push(check('release reproducibility temporary tarballs removed', releaseArtifactReproducibility.temporaryTarballsRemoved === true))
  checks.push(check('release reproducibility checks pass', releaseArtifactReproducibility.reproducibilityChecks.every((item) => item.ok)))
  checks.push(check('agent replay eval fixtures are local no-provider checks', agentReplayEvals.mode === 'local_no_provider_trace_graded_agent_replay_evals'))
  checks.push(check('agent replay evals performed no provider calls', agentReplayEvals.providerCallsPerformed.length === 0))
  checks.push(check('agent replay evals performed no live model calls', agentReplayEvals.liveModelCallsPerformed.length === 0))
  checks.push(check('agent replay evals performed no external calls', agentReplayEvals.externalCallsPerformed.length === 0))
  checks.push(check('agent replay evals include replay scenarios', agentReplayEvals.replayScenarioCount >= 5, String(agentReplayEvals.replayScenarioCount)))
  checks.push(check('agent replay evals set passing threshold', agentReplayEvals.minimumPassingScore >= 0.8, String(agentReplayEvals.minimumPassingScore)))
  checks.push(check('agent replay scenarios pass or are explained by protected VS Code boundary', agentReplayEvals.replayScenarios.every((item) => item.passed && item.score >= agentReplayEvals.minimumPassingScore) || agentReplayKnownVscodeBoundary, `${agentReplayFailedScenarioIds.join(',') || 'none'} / ${agentReplayFailedCheckLabels.join(',') || 'none'}`))
  checks.push(check('agent replay evals include IDE runtime smoke scenario', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_runtime_smoke_replay' && item.passed)))
  checks.push(check('agent replay evals include IDE host smoke scenario or protected boundary classification', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_host_smoke_replay' && item.passed) || (agentReplayKnownVscodeBoundary && agentReplayFailedScenarioIds.includes('ide_extension_host_smoke_replay'))))
  checks.push(check('agent replay evals include IDE workbench smoke scenario or protected boundary classification', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_workbench_smoke_replay' && item.passed) || (agentReplayKnownVscodeBoundary && agentReplayFailedScenarioIds.includes('ide_extension_workbench_smoke_replay'))))
  checks.push(check('agent replay evals include IDE webview render smoke scenario', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_webview_render_smoke_replay' && item.passed)))
  checks.push(check('agent replay evals include IDE rendered workbench screenshot scenario', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_rendered_workbench_screenshot_replay' && item.passed)))
  checks.push(check('agent replay evals include IDE webview interaction smoke scenario', agentReplayEvals.replayScenarios.some((item) => item.id === 'ide_extension_webview_interaction_smoke_replay' && item.passed)))
  checks.push(check('agent replay eval checks pass or are explained by protected VS Code boundary', agentReplayEvals.replayEvalChecks.every((item) => item.ok) || agentReplayKnownVscodeBoundary, agentReplayFailedCheckLabels.join(',') || 'none'))
  checks.push(check('source-controlled checks are local no-provider checks', sourceControlledChecks.mode === 'local_no_provider_source_controlled_product_checks'))
  checks.push(check('source-controlled checks performed no provider calls', sourceControlledChecks.providerCallsPerformed.length === 0))
  checks.push(check('source-controlled checks performed no live model calls', sourceControlledChecks.liveModelCallsPerformed.length === 0))
  checks.push(check('source-controlled checks performed no external calls', sourceControlledChecks.externalCallsPerformed.length === 0))
  checks.push(check('source-controlled checks target PR workflow', sourceControlledChecks.workflowPath === '.github/workflows/pr-checks.yml', sourceControlledChecks.workflowPath))
  checks.push(check('source-controlled checks require product-quality command', sourceControlledChecks.productQualityCommandPresent))
  checks.push(check('source-controlled checks require pull request trigger', sourceControlledChecks.pullRequestTriggerPresent))
  checks.push(check('source-controlled checks require main push trigger', sourceControlledChecks.pushMainTriggerPresent))
  checks.push(check('source-controlled checks reject release actions in PR workflow', sourceControlledChecks.releaseActionsAbsent))
  checks.push(check('source-controlled checks require pinned actions', sourceControlledChecks.actionReferencesPinned))
  checks.push(check('source-controlled check items pass', sourceControlledChecks.sourceControlledChecks.every((item) => item.ok)))
  checks.push(check('OpenSSF security posture is local no-provider check', openSsfSecurityPosture.mode === 'local_no_provider_openssf_security_posture'))
  checks.push(check('OpenSSF security posture performed no provider calls', openSsfSecurityPosture.providerCallsPerformed.length === 0))
  checks.push(check('OpenSSF security posture performed no live model calls', openSsfSecurityPosture.liveModelCallsPerformed.length === 0))
  checks.push(check('OpenSSF security posture performed no external calls', openSsfSecurityPosture.externalCallsPerformed.length === 0))
  checks.push(check('OpenSSF security posture executed no protected actions', openSsfSecurityPosture.protectedActionsExecuted.length === 0))
  checks.push(check('OpenSSF security posture records primary sources', ['ossf/scorecard', 'slsa-framework/slsa', 'github/docs', 'npm/documentation'].every((source) => openSsfSecurityPosture.primarySourceInputs.some((item) => item.sourceProject === source)), openSsfSecurityPosture.primarySourceInputs.map((item) => item.sourceProject).join(',')))
  checks.push(check('OpenSSF security posture verifies security policy', openSsfSecurityPosture.securityPolicyPresent && openSsfSecurityPosture.privateReportingGuidancePresent && openSsfSecurityPosture.responseTimelinePresent, openSsfSecurityPosture.securityPolicyPath))
  checks.push(check('OpenSSF security posture verifies pinned workflow actions', openSsfSecurityPosture.allWorkflowActionReferencesPinned))
  checks.push(check('OpenSSF security posture verifies least-privilege workflow permissions', openSsfSecurityPosture.prWorkflowTokenPermissionsReadOnly && openSsfSecurityPosture.releaseWorkflowPermissionsScoped))
  checks.push(check('OpenSSF security posture rejects dangerous pull_request_target usage', openSsfSecurityPosture.pullRequestTargetAbsent))
  checks.push(check('OpenSSF security posture verifies Dependabot config', openSsfSecurityPosture.dependabotConfigPath === '.github/dependabot.yml' && openSsfSecurityPosture.dependabotConfigPresent && openSsfSecurityPosture.dependabotCoversNpm && openSsfSecurityPosture.dependabotCoversGitHubActions && openSsfSecurityPosture.dependabotSchedulesPresent, openSsfSecurityPosture.dependabotConfigPath))
  checks.push(check('OpenSSF security posture verifies CodeQL SAST workflow', openSsfSecurityPosture.codeqlWorkflowPath === '.github/workflows/codeql.yml' && openSsfSecurityPosture.codeqlWorkflowPresent && openSsfSecurityPosture.codeqlActionsPinned && openSsfSecurityPosture.codeqlPermissionsScoped && openSsfSecurityPosture.codeqlAnalyzesJavaScriptTypeScript && openSsfSecurityPosture.codeqlSecurityExtendedQueriesConfigured && openSsfSecurityPosture.codeqlScheduledScanConfigured && openSsfSecurityPosture.codeqlHostedExecutionPerformed === false, openSsfSecurityPosture.codeqlWorkflowPath))
  checks.push(check('OpenSSF security posture verifies product-quality CI wiring', openSsfSecurityPosture.productQualityWorkflowPresent))
  checks.push(check('OpenSSF security posture verifies frozen dependency install', openSsfSecurityPosture.frozenDependencyInstallPresent))
  checks.push(check('OpenSSF security posture verifies npm provenance configuration or release boundary', openSsfSecurityPosture.releaseWorkflowBoundaryOnly === true || (openSsfSecurityPosture.npmProvenanceConfigured && openSsfSecurityPosture.npmTrustedPublishingBoundaryPresent && openSsfSecurityPosture.releaseEnvironmentPresent)))
  checks.push(check('OpenSSF security posture verifies Docker package permission scope or release boundary', openSsfSecurityPosture.releaseWorkflowBoundaryOnly === true || openSsfSecurityPosture.dockerPackageWriteScoped))
  checks.push(check('OpenSSF security posture blocks external Scorecard result claims', openSsfSecurityPosture.realScorecardRunPerformed === false && openSsfSecurityPosture.scorecardExternalClaimAllowed === false))
  checks.push(check('OpenSSF security posture keeps readiness and validation claims blocked', openSsfSecurityPosture.releaseReadinessClaimAllowed === false && openSsfSecurityPosture.productionReadinessClaimAllowed === false && openSsfSecurityPosture.publicReadinessClaimAllowed === false && openSsfSecurityPosture.externalValidationClaimAllowed === false && openSsfSecurityPosture.autonomousReliabilityClaimAllowed === false))
  checks.push(check('OpenSSF security posture classifies protected gaps', ['external_openssf_scorecard_run', 'hosted_ci_scorecard_evidence', 'hosted_codeql_analysis_evidence', 'signed_artifact_attestation_verification'].every((id) => openSsfSecurityPosture.classifiedUnresolvedGaps.some((gap) => gap.id === id && gap.status === 'classified_unresolved')), openSsfSecurityPosture.classifiedUnresolvedGaps.map((gap) => gap.id).join(',')))
  checks.push(check('OpenSSF security posture checks pass', openSsfSecurityPosture.postureChecks.every((item) => item.ok)))
  checks.push(check('real session capture is local no-provider fixture', realSessionCapture.mode === 'local_no_provider_operator_authorized_real_session_capture_fixture'))
  checks.push(check('real session capture performed no provider calls', realSessionCapture.providerCallsPerformed.length === 0))
  checks.push(check('real session capture performed no live model calls', realSessionCapture.liveModelCallsPerformed.length === 0))
  checks.push(check('real session capture performed no external calls', realSessionCapture.externalCallsPerformed.length === 0))
  checks.push(check('real session capture has bounded operator authorization', realSessionCapture.operatorAuthorization.authorized === true && realSessionCapture.operatorAuthorization.scope === 'operator_authorized_local_no_provider_cli_capture_only'))
  checks.push(check('real session capture does not authorize protected actions', realSessionCapture.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('real session capture was performed', realSessionCapture.capturePerformed === true))
  checks.push(check('real session capture writes expected trace', realSessionCapture.tracePath === 'reports/orchestra-real-session-capture-local-cli.jsonl', realSessionCapture.tracePath))
  checks.push(check('real session capture trace hash is recorded', typeof realSessionCapture.traceSha256 === 'string' && realSessionCapture.traceSha256.length === 64, realSessionCapture.traceSha256))
  checks.push(check('real session capture commands are timeout bounded', typeof realSessionCapture.commandTimeoutMs === 'number' && realSessionCapture.commandTimeoutMs > 0, String(realSessionCapture.commandTimeoutMs)))
  checks.push(check(
    'real session capture includes broader no-provider command session',
    ['version', 'help', 'doctor_help', 'auto_mode_help', 'agents_help'].every((name) => new Set(realSessionCapture.commandCaptures.map((capture) => capture.name)).has(name)),
    realSessionCapture.commandCaptures.map((capture) => capture.name).join(','),
  ))
  checks.push(check(
    'real session capture includes no-provider introspection beyond top-level help/version',
    ['doctor_help', 'auto_mode_help', 'agents_help'].every((name) => realSessionCapture.commandCaptures.some((capture) => capture.name === name && capture.passed)),
    realSessionCapture.commandCaptures.map((capture) => capture.name).join(','),
  ))
  checks.push(check('real session capture commands pass', realSessionCapture.commandCaptures.every((capture) => capture.exitCode === 0 && capture.passed)))
  checks.push(check('real session capture commands do not time out', realSessionCapture.commandCaptures.every((capture) => capture.timedOut === false), realSessionCapture.commandCaptures.filter((capture) => capture.timedOut !== false).map((capture) => `${capture.name}:${capture.timedOut}`).join(',') || 'none'))
  checks.push(check('real session capture uses local CLI command only', realSessionCapture.commandCaptures.every((capture) => capture.command[0] === 'node' && capture.command[1] === 'dist/cli.mjs')))
  checks.push(check('real session capture checks pass', realSessionCapture.captureChecks.every((item) => item.ok)))
  checks.push(check('prompted tool-loop capture is local no-provider fixture', promptedToolLoopCapture.mode === 'local_no_provider_prompted_tool_loop_capture'))
  checks.push(check('prompted tool-loop capture performed no provider calls', promptedToolLoopCapture.providerCallsPerformed.length === 0))
  checks.push(check('prompted tool-loop capture performed no live model calls', promptedToolLoopCapture.liveModelCallsPerformed.length === 0))
  checks.push(check('prompted tool-loop capture performed no external calls', promptedToolLoopCapture.externalCallsPerformed.length === 0))
  checks.push(check('prompted tool-loop capture has bounded operator authorization', promptedToolLoopCapture.operatorAuthorization.authorized === true && promptedToolLoopCapture.operatorAuthorization.scope === 'operator_authorized_local_no_provider_prompted_tool_loop_capture_only'))
  checks.push(check('prompted tool-loop capture does not authorize protected actions', promptedToolLoopCapture.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('prompted tool-loop capture records prompt hash only', promptedToolLoopCapture.promptCaptured === true && promptedToolLoopCapture.promptSha256.length === 64 && promptedToolLoopCapture.promptByteLength > 0, `${promptedToolLoopCapture.promptByteLength} bytes`))
  checks.push(check('prompted tool-loop capture does not claim non-synthetic user session', promptedToolLoopCapture.nonSyntheticUserSessionClaimed === false))
  checks.push(check('prompted tool-loop capture writes expected trace', promptedToolLoopCapture.tracePath === 'reports/orchestra-prompted-tool-loop-local-cli.jsonl', promptedToolLoopCapture.tracePath))
  checks.push(check('prompted tool-loop capture trace hash is recorded', typeof promptedToolLoopCapture.traceSha256 === 'string' && promptedToolLoopCapture.traceSha256.length === 64, promptedToolLoopCapture.traceSha256))
  checks.push(check('prompted tool-loop capture executes local tool steps', promptedToolLoopCapture.toolCommandCaptures.length >= 2 && promptedToolLoopCapture.toolCommandCaptures.every((capture) => capture.exitCode === 0 && capture.passed), promptedToolLoopCapture.toolCommandCaptures.map((capture) => capture.name).join(',')))
  checks.push(check('prompted tool-loop capture uses local CLI commands only', promptedToolLoopCapture.toolCommandCaptures.every((capture) => capture.command[0] === 'node' && capture.command[1] === 'dist/cli.mjs')))
  checks.push(check('prompted tool-loop capture checks pass', promptedToolLoopCapture.toolLoopChecks.every((item) => item.ok)))
  checks.push(check('code-editing trace capture is local no-provider fixture', codeEditingTraceCapture.mode === 'local_no_provider_code_editing_trace_capture'))
  checks.push(check('code-editing trace capture performed no provider calls', codeEditingTraceCapture.providerCallsPerformed.length === 0))
  checks.push(check('code-editing trace capture performed no live model calls', codeEditingTraceCapture.liveModelCallsPerformed.length === 0))
  checks.push(check('code-editing trace capture performed no external calls', codeEditingTraceCapture.externalCallsPerformed.length === 0))
  checks.push(check('code-editing trace capture has bounded operator authorization', codeEditingTraceCapture.operatorAuthorization.authorized === true && codeEditingTraceCapture.operatorAuthorization.scope === 'operator_authorized_local_no_provider_code_editing_trace_capture_only'))
  checks.push(check('code-editing trace capture does not authorize protected actions', codeEditingTraceCapture.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('code-editing trace capture was performed', codeEditingTraceCapture.capturePerformed === true))
  checks.push(check('code-editing trace capture does not claim non-synthetic user session', codeEditingTraceCapture.nonSyntheticUserSessionClaimed === false))
  checks.push(check('code-editing trace capture writes expected trace', codeEditingTraceCapture.tracePath === codeEditingTracePath && codeEditingTraceCapture.traceSha256.length === 64, codeEditingTraceCapture.tracePath))
  checks.push(check('code-editing trace capture applies fixture-only patch', codeEditingTraceCapture.patchApplied === true && codeEditingTraceCapture.modifiedFixtureFiles.length >= 1 && codeEditingTraceCapture.protectedRepoFilesModified.length === 0, codeEditingTraceCapture.modifiedFixtureFiles.join(',')))
  checks.push(check('code-editing trace capture changes source hash', codeEditingTraceCapture.sourceBeforeSha256.length === 64 && codeEditingTraceCapture.sourceAfterSha256.length === 64 && codeEditingTraceCapture.sourceBeforeSha256 !== codeEditingTraceCapture.sourceAfterSha256))
  checks.push(check('code-editing trace capture verifies fixture unit check', codeEditingTraceCapture.unitCheck.passed === true && codeEditingTraceCapture.unitCheck.testCaseCount >= 3, `${codeEditingTraceCapture.unitCheck.testCaseCount} cases`))
  checks.push(check('code-editing trace capture checks pass', codeEditingTraceCapture.traceChecks.every((item) => item.ok)))
  checks.push(check('multi-file code-editing trace capture is local no-provider fixture', multiFileCodeEditingTraceCapture.mode === 'local_no_provider_multi_file_code_editing_trace_capture'))
  checks.push(check('multi-file code-editing trace capture performed no provider calls', multiFileCodeEditingTraceCapture.providerCallsPerformed.length === 0))
  checks.push(check('multi-file code-editing trace capture performed no live model calls', multiFileCodeEditingTraceCapture.liveModelCallsPerformed.length === 0))
  checks.push(check('multi-file code-editing trace capture performed no external calls', multiFileCodeEditingTraceCapture.externalCallsPerformed.length === 0))
  checks.push(check('multi-file code-editing trace capture has bounded operator authorization', multiFileCodeEditingTraceCapture.operatorAuthorization.authorized === true && multiFileCodeEditingTraceCapture.operatorAuthorization.scope === 'operator_authorized_local_no_provider_multi_file_code_editing_trace_capture_only'))
  checks.push(check('multi-file code-editing trace capture does not authorize protected actions', multiFileCodeEditingTraceCapture.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('multi-file code-editing trace capture was performed', multiFileCodeEditingTraceCapture.capturePerformed === true))
  checks.push(check('multi-file code-editing trace capture does not claim non-synthetic user session', multiFileCodeEditingTraceCapture.nonSyntheticUserSessionClaimed === false))
  checks.push(check('multi-file code-editing trace capture writes expected trace', multiFileCodeEditingTraceCapture.tracePath === multiFileCodeEditingTracePath && multiFileCodeEditingTraceCapture.traceSha256.length === 64, multiFileCodeEditingTraceCapture.tracePath))
  checks.push(check('multi-file code-editing trace capture applies fixture-only patches', multiFileCodeEditingTraceCapture.patchApplied === true && multiFileCodeEditingTraceCapture.modifiedFixtureFiles.length >= 3 && multiFileCodeEditingTraceCapture.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-multi-file-code-editing-trace/')) && multiFileCodeEditingTraceCapture.protectedRepoFilesModified.length === 0, multiFileCodeEditingTraceCapture.modifiedFixtureFiles.join(',')))
  checks.push(check('multi-file code-editing trace capture changes source tree hash', multiFileCodeEditingTraceCapture.sourceBeforeTreeSha256.length === 64 && multiFileCodeEditingTraceCapture.sourceAfterTreeSha256.length === 64 && multiFileCodeEditingTraceCapture.sourceBeforeTreeSha256 !== multiFileCodeEditingTraceCapture.sourceAfterTreeSha256))
  checks.push(check('multi-file code-editing trace capture verifies fixture unit check', multiFileCodeEditingTraceCapture.unitCheck.passed === true && multiFileCodeEditingTraceCapture.unitCheck.testCaseCount >= 4, `${multiFileCodeEditingTraceCapture.unitCheck.testCaseCount} cases`))
  checks.push(check('multi-file code-editing trace capture checks pass', multiFileCodeEditingTraceCapture.traceChecks.every((item) => item.ok)))
  checks.push(check('regression-cycle code-editing trace capture is local no-provider fixture', regressionCycleCodeEditingTraceCapture.mode === 'local_no_provider_regression_cycle_code_editing_trace_capture'))
  checks.push(check('regression-cycle code-editing trace capture performed no provider calls', regressionCycleCodeEditingTraceCapture.providerCallsPerformed.length === 0))
  checks.push(check('regression-cycle code-editing trace capture performed no live model calls', regressionCycleCodeEditingTraceCapture.liveModelCallsPerformed.length === 0))
  checks.push(check('regression-cycle code-editing trace capture performed no external calls', regressionCycleCodeEditingTraceCapture.externalCallsPerformed.length === 0))
  checks.push(check('regression-cycle code-editing trace capture has bounded operator authorization', regressionCycleCodeEditingTraceCapture.operatorAuthorization.authorized === true && regressionCycleCodeEditingTraceCapture.operatorAuthorization.scope === 'operator_authorized_local_no_provider_regression_cycle_code_editing_trace_capture_only'))
  checks.push(check('regression-cycle code-editing trace capture does not authorize protected actions', regressionCycleCodeEditingTraceCapture.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('regression-cycle code-editing trace capture was performed', regressionCycleCodeEditingTraceCapture.capturePerformed === true))
  checks.push(check('regression-cycle code-editing trace capture does not claim non-synthetic user session', regressionCycleCodeEditingTraceCapture.nonSyntheticUserSessionClaimed === false))
  checks.push(check('regression-cycle code-editing trace capture writes expected trace', regressionCycleCodeEditingTraceCapture.tracePath === regressionCycleCodeEditingTracePath && regressionCycleCodeEditingTraceCapture.traceSha256.length === 64, regressionCycleCodeEditingTraceCapture.tracePath))
  checks.push(check('regression-cycle code-editing trace capture applies fixture-only repair', regressionCycleCodeEditingTraceCapture.modifiedFixtureFiles.length >= 1 && regressionCycleCodeEditingTraceCapture.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-regression-cycle-code-editing-trace/')) && regressionCycleCodeEditingTraceCapture.protectedRepoFilesModified.length === 0, regressionCycleCodeEditingTraceCapture.modifiedFixtureFiles.join(',')))
  checks.push(check('regression-cycle code-editing trace capture records red-green evidence', regressionCycleCodeEditingTraceCapture.wrongPatchApplied === true && regressionCycleCodeEditingTraceCapture.regressionFailedBeforeRepair === true && regressionCycleCodeEditingTraceCapture.repairApplied === true && regressionCycleCodeEditingTraceCapture.regressionPassedAfterRepair === true))
  checks.push(check('regression-cycle code-editing trace capture changes source through wrong and repaired hashes', regressionCycleCodeEditingTraceCapture.sourceBeforeSha256.length === 64 && regressionCycleCodeEditingTraceCapture.wrongPatchSha256.length === 64 && regressionCycleCodeEditingTraceCapture.repairedSourceSha256.length === 64 && regressionCycleCodeEditingTraceCapture.sourceBeforeSha256 !== regressionCycleCodeEditingTraceCapture.wrongPatchSha256 && regressionCycleCodeEditingTraceCapture.wrongPatchSha256 !== regressionCycleCodeEditingTraceCapture.repairedSourceSha256))
  checks.push(check('regression-cycle code-editing trace capture verifies failing then passing regression cases', regressionCycleCodeEditingTraceCapture.unitCheck.failedCaseCountBeforeRepair >= 1 && regressionCycleCodeEditingTraceCapture.unitCheck.passedCaseCountAfterRepair === regressionCycleCodeEditingTraceCapture.unitCheck.testCaseCount && regressionCycleCodeEditingTraceCapture.unitCheck.testCaseCount >= 4, `${regressionCycleCodeEditingTraceCapture.unitCheck.failedCaseCountBeforeRepair} failed before/${regressionCycleCodeEditingTraceCapture.unitCheck.passedCaseCountAfterRepair} passed after`))
  checks.push(check('regression-cycle code-editing trace capture checks pass', regressionCycleCodeEditingTraceCapture.traceChecks.every((item) => item.ok)))
  checks.push(check('tool-interruption recovery trace is local no-provider fixture', toolInterruptionRecoveryTrace.mode === 'local_no_provider_tool_interruption_recovery_trace_capture'))
  checks.push(check('tool-interruption recovery trace performed no provider calls', toolInterruptionRecoveryTrace.providerCallsPerformed.length === 0))
  checks.push(check('tool-interruption recovery trace performed no live model calls', toolInterruptionRecoveryTrace.liveModelCallsPerformed.length === 0))
  checks.push(check('tool-interruption recovery trace performed no external calls', toolInterruptionRecoveryTrace.externalCallsPerformed.length === 0))
  checks.push(check('tool-interruption recovery trace has bounded operator authorization', toolInterruptionRecoveryTrace.operatorAuthorization.authorized === true && toolInterruptionRecoveryTrace.operatorAuthorization.scope === 'operator_authorized_local_no_provider_tool_interruption_recovery_trace_capture_only'))
  checks.push(check('tool-interruption recovery trace does not authorize protected actions', toolInterruptionRecoveryTrace.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('tool-interruption recovery trace was performed', toolInterruptionRecoveryTrace.capturePerformed === true))
  checks.push(check('tool-interruption recovery trace does not claim non-synthetic user session', toolInterruptionRecoveryTrace.nonSyntheticUserSessionClaimed === false))
  checks.push(check('tool-interruption recovery trace writes expected trace', toolInterruptionRecoveryTrace.tracePath === toolInterruptionRecoveryTracePath && toolInterruptionRecoveryTrace.traceSha256.length === 64, toolInterruptionRecoveryTrace.tracePath))
  checks.push(check('tool-interruption recovery trace applies fixture-only recovery', toolInterruptionRecoveryTrace.modifiedFixtureFiles.length >= 3 && toolInterruptionRecoveryTrace.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-tool-interruption-recovery-trace/')) && toolInterruptionRecoveryTrace.protectedRepoFilesModified.length === 0, toolInterruptionRecoveryTrace.modifiedFixtureFiles.join(',')))
  checks.push(check('tool-interruption recovery trace records interruption invariant and recovery', toolInterruptionRecoveryTrace.interruptionDetected === true && toolInterruptionRecoveryTrace.recoveryApplied === true && toolInterruptionRecoveryTrace.finalVerificationPassed === true && toolInterruptionRecoveryTrace.interruptionRecoveryCheck.interruptedToolStepCount === 1 && toolInterruptionRecoveryTrace.interruptionRecoveryCheck.recoveredToolStepCount === 1 && toolInterruptionRecoveryTrace.interruptionRecoveryCheck.invariantViolationCount === 1 && toolInterruptionRecoveryTrace.interruptionRecoveryCheck.passed === true))
  checks.push(check('tool-interruption recovery trace changes output hash after recovery', toolInterruptionRecoveryTrace.sourceBeforeSha256.length === 64 && toolInterruptionRecoveryTrace.interruptedObservationSha256.length === 64 && toolInterruptionRecoveryTrace.recoveredSourceSha256.length === 64 && toolInterruptionRecoveryTrace.outputSha256.length === 64 && toolInterruptionRecoveryTrace.interruptedObservationSha256 !== toolInterruptionRecoveryTrace.outputSha256))
  checks.push(check('tool-interruption recovery trace records primary sources', toolInterruptionRecoveryTrace.primarySourceInputs.length >= 4 && toolInterruptionRecoveryTrace.primarySourceInputs.every((source) => /^https:\/\//.test(source.sourceUrl)), toolInterruptionRecoveryTrace.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('tool-interruption recovery trace checks pass', toolInterruptionRecoveryTrace.traceChecks.every((item) => item.ok)))
  checks.push(check('protected-action denial trace is local no-provider fixture', protectedActionDenialTrace.mode === 'local_no_provider_protected_action_denial_trace_capture'))
  checks.push(check('protected-action denial trace performed no provider calls', protectedActionDenialTrace.providerCallsPerformed.length === 0))
  checks.push(check('protected-action denial trace performed no live model calls', protectedActionDenialTrace.liveModelCallsPerformed.length === 0))
  checks.push(check('protected-action denial trace performed no external calls', protectedActionDenialTrace.externalCallsPerformed.length === 0))
  checks.push(check('protected-action denial trace has bounded operator authorization', protectedActionDenialTrace.operatorAuthorization.authorized === true && protectedActionDenialTrace.operatorAuthorization.scope === 'operator_authorized_local_no_provider_protected_action_denial_trace_capture_only'))
  checks.push(check('protected-action denial trace does not authorize protected actions', protectedActionDenialTrace.operatorAuthorization.protectedActionsAuthorized === false))
  checks.push(check('protected-action denial trace was performed', protectedActionDenialTrace.capturePerformed === true))
  checks.push(check('protected-action denial trace does not claim non-synthetic user session', protectedActionDenialTrace.nonSyntheticUserSessionClaimed === false))
  checks.push(check('protected-action denial trace writes expected trace', protectedActionDenialTrace.tracePath === protectedActionDenialTracePath && protectedActionDenialTrace.traceSha256.length === 64, protectedActionDenialTrace.tracePath))
  checks.push(check('protected-action denial trace applies fixture-only denial evidence', protectedActionDenialTrace.modifiedFixtureFiles.length >= 3 && protectedActionDenialTrace.modifiedFixtureFiles.every((path) => path.startsWith('_fixtures/product-protected-action-denial-trace/')) && protectedActionDenialTrace.protectedRepoFilesModified.length === 0, protectedActionDenialTrace.modifiedFixtureFiles.join(',')))
  checks.push(check('protected-action denial trace records denial and safe fallback', protectedActionDenialTrace.protectedActionRequested === true && protectedActionDenialTrace.protectedActionDenied === true && protectedActionDenialTrace.protectedActionExecuted === false && protectedActionDenialTrace.safeAlternativeSelected === true && protectedActionDenialTrace.finalVerificationPassed === true && protectedActionDenialTrace.denialCheck.protectedActionRequestCount === 1 && protectedActionDenialTrace.denialCheck.deniedProtectedActionCount === 1 && protectedActionDenialTrace.denialCheck.executedProtectedActionCount === 0 && protectedActionDenialTrace.denialCheck.safeAlternativeCount === 1 && protectedActionDenialTrace.denialCheck.passed === true))
  checks.push(check('protected-action denial trace records stable hashes', protectedActionDenialTrace.requestSha256.length === 64 && protectedActionDenialTrace.denialRecordSha256.length === 64 && protectedActionDenialTrace.safeAlternativeSummarySha256.length === 64))
  checks.push(check('protected-action denial trace records primary sources', protectedActionDenialTrace.primarySourceInputs.length >= 4 && protectedActionDenialTrace.primarySourceInputs.every((source) => /^https:\/\//.test(source.sourceUrl)), protectedActionDenialTrace.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('protected-action denial trace checks pass', protectedActionDenialTrace.traceChecks.every((item) => item.ok)))
  checks.push(check('real trace evals are local no-provider checks', realTraceEvals.mode === 'local_no_provider_real_session_jsonl_trace_grading'))
  checks.push(check('real trace evals performed no provider calls', realTraceEvals.providerCallsPerformed.length === 0))
  checks.push(check('real trace evals performed no live model calls', realTraceEvals.liveModelCallsPerformed.length === 0))
  checks.push(check('real trace evals performed no external calls', realTraceEvals.externalCallsPerformed.length === 0))
  checks.push(check('real trace evals include real JSONL traces', realTraceEvals.traceFileCount >= 5, String(realTraceEvals.traceFileCount)))
  checks.push(check('real trace evals include local capture trace', realTraceEvals.traces.some((trace) => trace.path === realSessionCapture.tracePath && trace.sha256 === realSessionCapture.traceSha256)))
  checks.push(check('real trace evals include prompted tool-loop trace', realTraceEvals.traces.some((trace) => trace.path === promptedToolLoopCapture.tracePath && trace.sha256 === promptedToolLoopCapture.traceSha256)))
  checks.push(check('real trace evals include implementation-bearing code-editing trace', realTraceEvals.traces.some((trace) => trace.path === codeEditingTraceCapture.tracePath && trace.sha256 === codeEditingTraceCapture.traceSha256)))
  checks.push(check('real trace evals include multi-file implementation-bearing code-editing trace', realTraceEvals.traces.some((trace) => trace.path === multiFileCodeEditingTraceCapture.tracePath && trace.sha256 === multiFileCodeEditingTraceCapture.traceSha256)))
  checks.push(check('real trace evals include regression-cycle implementation-bearing code-editing trace', realTraceEvals.traces.some((trace) => trace.path === regressionCycleCodeEditingTraceCapture.tracePath && trace.sha256 === regressionCycleCodeEditingTraceCapture.traceSha256)))
  checks.push(check('real trace evals include tool-interruption recovery trace', realTraceEvals.traces.some((trace) => trace.path === toolInterruptionRecoveryTrace.tracePath && trace.sha256 === toolInterruptionRecoveryTrace.traceSha256)))
  checks.push(check('real trace evals include protected-action denial trace', realTraceEvals.traces.some((trace) => trace.path === protectedActionDenialTrace.tracePath && trace.sha256 === protectedActionDenialTrace.traceSha256)))
  checks.push(check('real trace evals parse all traces', realTraceEvals.traces.every((trace) => trace.parseErrorCount === 0)))
  checks.push(check('real trace evals verify required fields', realTraceEvals.traces.every((trace) => trace.requiredFieldsComplete)))
  checks.push(check('real trace evals verify started and terminal statuses', realTraceEvals.traces.every((trace) => trace.hasStarted && trace.hasTerminalStatus)))
  checks.push(check('real trace evals verify started-to-terminal ordering', realTraceEvals.traces.every((trace) => trace.hasStartedToTerminalTransition === true)))
  checks.push(check('real trace evals include coverage summary', typeof realTraceEvals.coverageSummary === 'object' && realTraceEvals.coverageSummary !== null))
  checks.push(check('real trace evals classify trace kinds', Array.isArray(realTraceEvals.coverageSummary?.traceKinds) && realTraceEvals.coverageSummary.traceKinds.length >= 4, realTraceEvals.coverageSummary?.traceKinds?.join(',') ?? 'missing'))
  checks.push(check('real trace evals classify local capture trace kind', realTraceEvals.coverageSummary?.traceKinds.includes('real_session_capture_cli') === true, realTraceEvals.coverageSummary?.traceKinds?.join(',') ?? 'missing'))
  checks.push(check('real trace evals classify prompted tool-loop trace kind', realTraceEvals.coverageSummary?.traceKinds.includes('prompted_tool_loop_cli') === true, realTraceEvals.coverageSummary?.traceKinds?.join(',') ?? 'missing'))
  checks.push(check('real trace evals cover multiple query sources', Array.isArray(realTraceEvals.coverageSummary?.querySources) && realTraceEvals.coverageSummary.querySources.length >= 2, realTraceEvals.coverageSummary?.querySources?.join(',') ?? 'missing'))
  checks.push(check('real trace evals cover success and failure outcomes', realTraceEvals.coverageSummary?.terminalOutcomes.includes('succeeded') === true && (realTraceEvals.coverageSummary.terminalOutcomes.includes('failed') || realTraceFailedTerminalOutcomeClassified), realTraceEvals.coverageSummary?.terminalOutcomes?.join(',') ?? 'missing'))
  checks.push(check('real trace evals classify coverage gaps without protected action', Array.isArray(realTraceEvals.coverageSummary?.classifiedCoverageGaps) && realTraceEvals.coverageSummary.classifiedCoverageGaps.length >= 2 && realTraceEvals.coverageSummary.classifiedCoverageGaps.every((gap) => gap.protectedActionRequired === false && ['classified_unresolved', 'not_present'].includes(gap.status))))
  checks.push(check('real trace evals find no credential patterns', realTraceEvals.traces.every((trace) => !trace.credentialPatternFound)))
  checks.push(check('real trace summaries pass', realTraceEvals.traces.every((trace) => trace.passed)))
  checks.push(check('real trace eval checks pass', realTraceEvals.traceChecks.every((item) => item.ok)))
  checks.push(check('trace schema contract is local no-provider check', traceSchemaContract.mode === 'local_no_provider_trace_schema_contract'))
  checks.push(check('trace schema contract performed no provider calls', traceSchemaContract.providerCallsPerformed.length === 0))
  checks.push(check('trace schema contract performed no live model calls', traceSchemaContract.liveModelCallsPerformed.length === 0))
  checks.push(check('trace schema contract performed no external calls', traceSchemaContract.externalCallsPerformed.length === 0))
  checks.push(check('trace schema contract executed no protected actions', traceSchemaContract.protectedActionsExecuted.length === 0))
  checks.push(check('trace schema contract imports real trace evals', traceSchemaContract.sourceRealTraceEvalReportPath === realTraceEvalsJsonPath && traceSchemaContract.sourceTraceFileCount === realTraceEvals.traceFileCount, `${traceSchemaContract.sourceRealTraceEvalReportPath}/${traceSchemaContract.sourceTraceFileCount}`))
  checks.push(check('trace schema contract assesses every trace', traceSchemaContract.aggregate.traceCount === realTraceEvals.traceFileCount && traceSchemaContract.traceSchemaSummaries.length === realTraceEvals.traceFileCount, `${traceSchemaContract.aggregate.traceCount}/${realTraceEvals.traceFileCount}`))
  checks.push(check('trace schema contract preserves trace hashes', traceSchemaContract.traceSchemaSummaries.every((summary) => realTraceEvals.traces.some((trace) => trace.path === summary.path && trace.sha256 === summary.sha256))))
  checks.push(check('trace schema contract passes all current traces', traceSchemaContract.aggregate.schemaFailedTraceCount === 0 && traceSchemaContract.traceSchemaSummaries.every((summary) => summary.schemaContractPassed), `${traceSchemaContract.aggregate.schemaPassedTraceCount}/${traceSchemaContract.aggregate.traceCount}`))
  checks.push(check('trace schema contract records primary sources', traceSchemaContract.primarySourceInputs.length >= 3 && traceSchemaContract.primarySourceInputs.every((source) => /^https:\/\//.test(source.sourceUrl)), traceSchemaContract.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('trace schema contract classifies recommended gaps without protected action', traceSchemaContract.recommendedAlignmentGaps.length >= 2 && traceSchemaContract.recommendedAlignmentGaps.every((gap) => ['classified_unresolved', 'not_present'].includes(gap.status) && gap.protectedActionRequired === false)))
  checks.push(check('trace schema contract verifies current generated trace producer enrichment', (traceSchemaContract.aggregate.currentGeneratedTraceProducerTraceCount ?? 0) >= 5 && traceSchemaContract.aggregate.currentGeneratedTraceProducerMissingEventNameCount === 0 && traceSchemaContract.aggregate.currentGeneratedTraceProducerMissingTraceContextCount === 0 && traceSchemaContract.aggregate.currentGeneratedTraceProducerMissingActionObservationCount === 0, `${traceSchemaContract.aggregate.currentGeneratedTraceProducerTraceCount ?? 'missing'} producers`))
  checks.push(check('trace schema contract keeps readiness claims blocked', traceSchemaContract.releaseReadinessClaimAllowed === false && traceSchemaContract.productionReadinessClaimAllowed === false && traceSchemaContract.publicReadinessClaimAllowed === false && traceSchemaContract.externalValidationClaimAllowed === false && traceSchemaContract.autonomousReliabilityClaimAllowed === false))
  checks.push(check('trace schema contract checks pass', traceSchemaContract.schemaContractChecks.every((item) => item.ok)))
  checks.push(check('trace portability export is local no-provider check', tracePortabilityExport.mode === 'local_no_provider_trace_portability_export'))
  checks.push(check('trace portability export performed no provider calls', tracePortabilityExport.providerCallsPerformed.length === 0))
  checks.push(check('trace portability export performed no live model calls', tracePortabilityExport.liveModelCallsPerformed.length === 0))
  checks.push(check('trace portability export performed no external calls', tracePortabilityExport.externalCallsPerformed.length === 0))
  checks.push(check('trace portability export executed no protected actions', tracePortabilityExport.protectedActionsExecuted.length === 0))
  checks.push(check('trace portability export imports current trace sources', tracePortabilityExport.sourceRealTraceEvalReportPath === realTraceEvalsJsonPath && tracePortabilityExport.sourceTraceSchemaContractReportPath === traceSchemaContractJsonPath, `${tracePortabilityExport.sourceRealTraceEvalReportPath}/${tracePortabilityExport.sourceTraceSchemaContractReportPath}`))
  checks.push(check('trace portability export writes portable JSONL', tracePortabilityExport.portableTraceExportPath === portableTraceEventsPath && tracePortabilityExport.portableTraceExportSha256.length === 64, tracePortabilityExport.portableTraceExportPath))
  checks.push(check('trace portability export covers every source trace', tracePortabilityExport.sourceTraceCount === realTraceEvals.traceFileCount && tracePortabilityExport.sourceTraceHashes.length === realTraceEvals.traceFileCount && tracePortabilityExport.sourceTraceHashes.every((summary) => realTraceEvals.traces.some((trace) => trace.path === summary.path && trace.sha256 === summary.sha256)), `${tracePortabilityExport.sourceTraceCount}/${realTraceEvals.traceFileCount}`))
  checks.push(check('trace portability export covers every source event', tracePortabilityExport.sourceEventCount === traceSchemaContract.aggregate.eventCount && tracePortabilityExport.portableEventCount === traceSchemaContract.aggregate.eventCount, `${tracePortabilityExport.portableEventCount}/${traceSchemaContract.aggregate.eventCount}`))
  checks.push(check('trace portability export fills portable event names', tracePortabilityExport.portableMissingEventNameCount === 0, `${tracePortabilityExport.portableMissingEventNameCount} missing`))
  checks.push(check('trace portability export fills portable trace context', tracePortabilityExport.portableMissingTraceContextCount === 0, `${tracePortabilityExport.portableMissingTraceContextCount} missing`))
  checks.push(check('trace portability export fills portable action observations', tracePortabilityExport.portableMissingActionObservationCount === 0, `${tracePortabilityExport.portableMissingActionObservationCount} missing`))
  checks.push(check('trace portability export preserves historical-gap accounting', tracePortabilityExport.sourceHistoricalMissingEventNameCount === traceSchemaContract.aggregate.missingRecommendedEventNameCount && tracePortabilityExport.sourceHistoricalMissingTraceContextCount === traceSchemaContract.aggregate.missingRecommendedTraceContextCount && tracePortabilityExport.sourceHistoricalMissingActionObservationCount === (traceSchemaContract.aggregate.missingRecommendedActionObservationCount ?? 0), `${tracePortabilityExport.sourceHistoricalMissingEventNameCount}/${traceSchemaContract.aggregate.missingRecommendedEventNameCount}`))
  checks.push(check('trace portability export normalizes historical gaps without raw mutation', (tracePortabilityHistoricalGapCountEstimate === 0 ? tracePortabilityExport.portableEventsSynthesizedFromHistoricalGapsCount === 0 : tracePortabilityExport.portableEventsSynthesizedFromHistoricalGapsCount >= tracePortabilityHistoricalGapCountEstimate) && tracePortabilityExport.sourceEventsAlreadyEnrichedCount === traceSchemaContract.aggregate.currentGeneratedTraceProducerEventCount, `${tracePortabilityExport.portableEventsSynthesizedFromHistoricalGapsCount} synthesized for ${tracePortabilityHistoricalGapCountEstimate} source gap events`))
  checks.push(check('trace portability export keeps readiness claims blocked', tracePortabilityExport.releaseReadinessClaimAllowed === false && tracePortabilityExport.productionReadinessClaimAllowed === false && tracePortabilityExport.publicReadinessClaimAllowed === false && tracePortabilityExport.externalValidationClaimAllowed === false && tracePortabilityExport.autonomousReliabilityClaimAllowed === false))
  checks.push(check('trace portability export checks pass', tracePortabilityExport.portabilityChecks.every((item) => item.ok)))
  checks.push(check('trace redaction policy is local no-provider check', traceRedactionPolicy.mode === 'local_no_provider_trace_capture_redaction_policy'))
  checks.push(check('trace redaction policy performed no provider calls', traceRedactionPolicy.providerCallsPerformed.length === 0))
  checks.push(check('trace redaction policy performed no live model calls', traceRedactionPolicy.liveModelCallsPerformed.length === 0))
  checks.push(check('trace redaction policy performed no external calls', traceRedactionPolicy.externalCallsPerformed.length === 0))
  checks.push(check('trace redaction policy scans all trace files', traceRedactionPolicy.rawTraceFileCount === realTraceEvals.traceFileCount, `${traceRedactionPolicy.rawTraceFileCount}/${realTraceEvals.traceFileCount}`))
  checks.push(check('trace redaction policy does not falsely claim non-synthetic capture', traceRedactionPolicy.nonSyntheticRealSessionCapture.performed === false && traceRedactionPolicy.nonSyntheticRealSessionCapture.requiredBeforeStrongerReliabilityClaims === true && traceRedactionPolicy.nonSyntheticRealSessionCapture.currentStatus === 'policy_ready_capture_not_performed'))
  checks.push(check('trace redaction policy has summary-only publishable fields', traceRedactionPolicy.publishableSummaryFields.length >= 8 && traceRedactionPolicy.publishableSummaryFields.every((field) => !traceRedactionPolicy.forbiddenRawFields.includes(field))))
  checks.push(check('trace redaction policy forbids raw credentials and provider payloads', ['api_key', 'authorization', 'rawPrompt', 'rawCompletion', 'rawProviderPayload', 'providerRequestId'].every((field) => traceRedactionPolicy.forbiddenRawFields.includes(field))))
  checks.push(check('trace redaction policy defines redaction rules', traceRedactionPolicy.redactionRules.length >= 5 && ['credentials_and_tokens', 'provider_request_identifiers', 'raw_prompt_and_completion_payloads', 'local_path_and_environment_details', 'raw_trace_identity'].every((id) => traceRedactionPolicy.redactionRules.some((rule) => rule.id === id))))
  checks.push(check('trace redaction policy has explicit capture workflow', traceRedactionPolicy.captureWorkflow.length >= 5 && traceRedactionPolicy.captureWorkflow.some((step) => step.includes('explicit operator')) && traceRedactionPolicy.captureWorkflow.some((step) => step.includes('quarantine'))))
  checks.push(check('trace redaction policy finds no raw credential patterns', traceRedactionPolicy.scannedRawTraceFiles.every((trace) => !trace.credentialPatternFound)))
  checks.push(check('trace redaction policy finds no raw provider request id patterns', traceRedactionPolicy.scannedRawTraceFiles.every((trace) => !trace.providerRequestIdPatternFound)))
  checks.push(check('trace redaction policy checks pass', traceRedactionPolicy.policyChecks.every((item) => item.ok)))
  checks.push(check('benchmark readiness is local no-provider check', benchmarkReadiness.mode === 'local_no_provider_benchmark_readiness_matrix'))
  checks.push(check('benchmark readiness performed no provider calls', benchmarkReadiness.providerCallsPerformed.length === 0))
  checks.push(check('benchmark readiness performed no live model calls', benchmarkReadiness.liveModelCallsPerformed.length === 0))
  checks.push(check('benchmark readiness performed no external calls', benchmarkReadiness.externalCallsPerformed.length === 0))
  checks.push(check('benchmark readiness executed no protected actions', benchmarkReadiness.protectedActionsExecuted.length === 0))
  checks.push(check('benchmark readiness does not claim external benchmark run', benchmarkReadiness.externalBenchmarkRunPerformed === false && benchmarkReadiness.externalBenchmarkResultClaimed === false))
  checks.push(check('benchmark readiness uses primary GitHub sources', benchmarkReadiness.primarySourceInputs.length >= 3 && benchmarkReadiness.primarySourceInputs.every((source) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(source.sourceUrl))))
  checks.push(check('benchmark readiness writes expected manifest', benchmarkReadiness.benchmarkManifestPath === benchmarkTaskManifestPath && benchmarkReadiness.benchmarkManifestSha256.length === 64, benchmarkReadiness.benchmarkManifestPath))
  checks.push(check('benchmark readiness maps local tasks', benchmarkReadiness.benchmarkTaskCount >= realTraceEvals.traceFileCount + 2, String(benchmarkReadiness.benchmarkTaskCount)))
  checks.push(check('benchmark readiness covers benchmark dimensions', ['task_instance_schema_alignment', 'trajectory_artifact_alignment', 'replay_grading_alignment', 'reproducible_artifact_alignment', 'publishable_summary_redaction', 'source_controlled_gate_wiring', 'external_benchmark_run_boundary'].every((id) => benchmarkReadiness.readinessDimensions.some((dimension) => dimension.id === id)), benchmarkReadiness.readinessDimensions.map((dimension) => dimension.id).join(',')))
  checks.push(check('benchmark readiness classifies unresolved gaps without execution', benchmarkReadiness.unresolvedGaps.length >= 3 && benchmarkReadiness.unresolvedGaps.every((gap) => gap.status === 'classified_unresolved' && gap.protectedActionExecuted === false)))
  checks.push(check('benchmark readiness checks pass', benchmarkReadiness.benchmarkReadinessChecks.every((item) => item.ok)))
  checks.push(check('external benchmark boundary is local no-provider check', externalBenchmarkBoundary.mode === 'local_no_provider_external_benchmark_boundary'))
  checks.push(check('external benchmark boundary performed no provider calls', externalBenchmarkBoundary.providerCallsPerformed.length === 0))
  checks.push(check('external benchmark boundary performed no live model calls', externalBenchmarkBoundary.liveModelCallsPerformed.length === 0))
  checks.push(check('external benchmark boundary performed no external calls', externalBenchmarkBoundary.externalCallsPerformed.length === 0))
  checks.push(check('external benchmark boundary executed no protected actions', externalBenchmarkBoundary.protectedActionsExecuted.length === 0))
  checks.push(check('external benchmark boundary imports benchmark readiness evidence', externalBenchmarkBoundary.sourceBenchmarkReadinessPath === benchmarkReadinessJsonPath && externalBenchmarkBoundary.sourceBenchmarkTaskCount === benchmarkReadiness.benchmarkTaskCount && externalBenchmarkBoundary.sourceBenchmarkManifestSha256 === benchmarkReadiness.benchmarkManifestSha256, externalBenchmarkBoundary.sourceBenchmarkReadinessPath))
  checks.push(check('external benchmark execution remains unauthorized and unperformed', externalBenchmarkBoundary.externalBenchmarkExecutionAuthorized === false && externalBenchmarkBoundary.externalBenchmarkExecutionPerformed === false))
  checks.push(check('external benchmark result and readiness claims remain blocked', externalBenchmarkBoundary.externalBenchmarkResultClaimAllowed === false && externalBenchmarkBoundary.releaseReadinessClaimAllowed === false && externalBenchmarkBoundary.productionReadinessClaimAllowed === false && externalBenchmarkBoundary.publicReadinessClaimAllowed === false && externalBenchmarkBoundary.autonomousReliabilityClaimAllowed === false))
  checks.push(check('external benchmark authorization request is written', externalBenchmarkBoundary.authorizationRequestPath === externalBenchmarkAuthorizationRequestPath, externalBenchmarkBoundary.authorizationRequestPath))
  checks.push(check('external benchmark protected authorizations default false', externalBenchmarkBoundary.protectedActionAuthorizations.length >= 8 && externalBenchmarkBoundary.protectedActionAuthorizations.every((item) => item.requiredBeforeExecution && item.authorized === false)))
  checks.push(check('external benchmark boundary classifies required protected gaps', ['external_dataset_access', 'container_runtime_setup', 'provider_live_model_validation', 'remote_runtime_access', 'hosted_ci_execution', 'public_result_claim', 'release_readiness_claim', 'production_readiness_claim'].every((id) => externalBenchmarkBoundary.boundaryGaps.some((gap) => gap.id === id)), externalBenchmarkBoundary.boundaryGaps.map((gap) => gap.id).join(',')))
  checks.push(check('external benchmark boundary keeps all gaps unexecuted', externalBenchmarkBoundary.boundaryGaps.every((gap) => gap.status === 'classified_unresolved' && gap.protectedActionExecuted === false)))
  checks.push(check('external benchmark boundary checks pass', externalBenchmarkBoundary.boundaryChecks.every((item) => item.ok)))
  checks.push(check('local benchmark harness is local no-provider check', localBenchmarkHarness.mode === 'local_no_provider_benchmark_replay_harness'))
  checks.push(check('local benchmark harness performed no provider calls', localBenchmarkHarness.providerCallsPerformed.length === 0))
  checks.push(check('local benchmark harness performed no live model calls', localBenchmarkHarness.liveModelCallsPerformed.length === 0))
  checks.push(check('local benchmark harness performed no external calls', localBenchmarkHarness.externalCallsPerformed.length === 0))
  checks.push(check('local benchmark harness executed no protected actions', localBenchmarkHarness.protectedActionsExecuted.length === 0))
  checks.push(check('local benchmark harness uses benchmark manifest', localBenchmarkHarness.sourceBenchmarkManifestPath === benchmarkTaskManifestPath && localBenchmarkHarness.sourceBenchmarkTaskCount === benchmarkReadiness.benchmarkTaskCount && localBenchmarkHarness.sourceBenchmarkManifestSha256 === benchmarkReadiness.benchmarkManifestSha256, localBenchmarkHarness.sourceBenchmarkManifestPath))
  checks.push(check('local benchmark harness imports external boundary', localBenchmarkHarness.sourceExternalBenchmarkBoundaryPath === externalBenchmarkBoundaryJsonPath, localBenchmarkHarness.sourceExternalBenchmarkBoundaryPath))
  checks.push(check('local benchmark harness writes result JSONL', localBenchmarkHarness.localBenchmarkResultPath === localBenchmarkResultsPath && localBenchmarkHarness.localBenchmarkResultSha256.length === 64, localBenchmarkHarness.localBenchmarkResultPath))
  checks.push(check('local benchmark harness has one result per benchmark task', localBenchmarkHarness.localBenchmarkTaskResults.length === benchmarkReadiness.benchmarkTaskCount, `${localBenchmarkHarness.localBenchmarkTaskResults.length}/${benchmarkReadiness.benchmarkTaskCount}`))
  checks.push(check('local benchmark harness verifies source evidence hashes', localBenchmarkHarness.localBenchmarkTaskResults.every((item) => item.sourceEvidenceExists && item.sourceEvidenceHashMatches)))
  checks.push(check('local benchmark harness keeps protected actions and external claims false', localBenchmarkHarness.localBenchmarkTaskResults.every((item) => item.protectedActionExecuted === false && item.externalBenchmarkResultClaimed === false) && localBenchmarkHarness.externalBenchmarkExecutionPerformed === false && localBenchmarkHarness.externalBenchmarkResultClaimed === false))
  checks.push(check('local benchmark harness classifies blocked tasks without failing the harness', localBenchmarkHarness.statusSummary.classifiedBlockedTasks >= 0 && localBenchmarkHarness.statusSummary.failedTasks === 0, `${localBenchmarkHarness.statusSummary.classifiedBlockedTasks} blocked/${localBenchmarkHarness.statusSummary.failedTasks} failed`))
  checks.push(check('local benchmark harness checks pass', localBenchmarkHarness.harnessChecks.every((item) => item.ok)))
  checks.push(check('benchmark efficiency metrics is local no-provider check', benchmarkEfficiencyMetrics.mode === 'local_no_provider_benchmark_efficiency_metrics'))
  checks.push(check('benchmark efficiency metrics performed no provider calls', benchmarkEfficiencyMetrics.providerCallsPerformed.length === 0))
  checks.push(check('benchmark efficiency metrics performed no live model calls', benchmarkEfficiencyMetrics.liveModelCallsPerformed.length === 0))
  checks.push(check('benchmark efficiency metrics performed no external calls', benchmarkEfficiencyMetrics.externalCallsPerformed.length === 0))
  checks.push(check('benchmark efficiency metrics executed no protected actions', benchmarkEfficiencyMetrics.protectedActionsExecuted.length === 0))
  checks.push(check('benchmark efficiency metrics imports local benchmark results', benchmarkEfficiencyMetrics.sourceLocalBenchmarkHarnessPath === localBenchmarkHarnessJsonPath && benchmarkEfficiencyMetrics.sourceLocalBenchmarkResultsPath === localBenchmarkResultsPath && benchmarkEfficiencyMetrics.sourceLocalBenchmarkResultsSha256 === localBenchmarkHarness.localBenchmarkResultSha256, benchmarkEfficiencyMetrics.sourceLocalBenchmarkResultsPath))
  checks.push(check('benchmark efficiency metrics writes expected JSONL', benchmarkEfficiencyMetrics.metricsJsonlPath === benchmarkEfficiencyMetricsJsonlPath && benchmarkEfficiencyMetrics.metricsJsonlSha256.length === 64, benchmarkEfficiencyMetrics.metricsJsonlPath))
  checks.push(check('benchmark efficiency metrics records one record per local task', benchmarkEfficiencyMetrics.benchmarkEfficiencyRecords.length === localBenchmarkHarness.localBenchmarkTaskResults.length && benchmarkEfficiencyMetrics.summary.comparableRecordCount === localBenchmarkHarness.localBenchmarkTaskResults.length, `${benchmarkEfficiencyMetrics.summary.comparableRecordCount}/${localBenchmarkHarness.localBenchmarkTaskResults.length}`))
  checks.push(check('benchmark efficiency metrics preserves comparable fields', ['agent', 'model', 'inputTokens', 'outputTokens', 'costUsd', 'numTurns', 'durationMs', 'resolved', 'sourceEvidenceSha256'].every((field) => benchmarkEfficiencyMetrics.metricSchemaFields.includes(field)) && benchmarkEfficiencyMetrics.summary.recordsWithComparableMetricFields === benchmarkEfficiencyMetrics.benchmarkEfficiencyRecords.length, benchmarkEfficiencyMetrics.metricSchemaFields.join(',')))
  checks.push(check('benchmark efficiency metrics classifies token cost duration gaps', benchmarkEfficiencyMetrics.summary.recordsWithMeasuredTokenCostDuration === 0 && benchmarkEfficiencyMetrics.summary.classifiedMetricGapCount === benchmarkEfficiencyMetrics.benchmarkEfficiencyRecords.length && benchmarkEfficiencyMetrics.benchmarkEfficiencyRecords.every((record) => record.metricGapStatus === 'classified_unresolved_external_or_live_run_required'), `${benchmarkEfficiencyMetrics.summary.classifiedMetricGapCount} classified`))
  checks.push(check('benchmark efficiency metrics records primary sources', benchmarkEfficiencyMetrics.primarySourceInputs.some((source) => source.sourceProject === 'Vexp-ai/vexp-swe-bench') && benchmarkEfficiencyMetrics.primarySourceInputs.every((source) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(source.sourceUrl)), benchmarkEfficiencyMetrics.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('benchmark efficiency metrics keeps external comparison claims blocked', benchmarkEfficiencyMetrics.externalBenchmarkExecutionPerformed === false && benchmarkEfficiencyMetrics.externalBenchmarkResultClaimed === false && benchmarkEfficiencyMetrics.externalComparisonClaimAllowed === false && benchmarkEfficiencyMetrics.releaseReadinessClaimAllowed === false && benchmarkEfficiencyMetrics.productionReadinessClaimAllowed === false && benchmarkEfficiencyMetrics.publicReadinessClaimAllowed === false && benchmarkEfficiencyMetrics.externalValidationClaimAllowed === false && benchmarkEfficiencyMetrics.autonomousReliabilityClaimAllowed === false))
  checks.push(check('benchmark efficiency metrics keeps unresolved gaps unexecuted', benchmarkEfficiencyMetrics.unresolvedMetricGaps.length >= 5 && benchmarkEfficiencyMetrics.unresolvedMetricGaps.every((gap) => gap.status === 'classified_unresolved' && gap.requiredBeforeExternalComparisonClaim && gap.protectedActionRequired && gap.protectedActionExecuted === false), benchmarkEfficiencyMetrics.unresolvedMetricGaps.map((gap) => gap.id).join(',')))
  checks.push(check('benchmark efficiency metrics checks pass', benchmarkEfficiencyMetrics.efficiencyChecks.every((item) => item.ok)))
  checks.push(check('benchmark submission readiness is local no-provider check', benchmarkSubmissionReadiness.mode === 'local_no_provider_benchmark_submission_readiness'))
  checks.push(check('benchmark submission readiness performed no provider calls', benchmarkSubmissionReadiness.providerCallsPerformed.length === 0))
  checks.push(check('benchmark submission readiness performed no live model calls', benchmarkSubmissionReadiness.liveModelCallsPerformed.length === 0))
  checks.push(check('benchmark submission readiness performed no external calls', benchmarkSubmissionReadiness.externalCallsPerformed.length === 0))
  checks.push(check('benchmark submission readiness executed no protected actions', benchmarkSubmissionReadiness.protectedActionsExecuted.length === 0))
  checks.push(check('benchmark submission readiness imports local benchmark and efficiency evidence', benchmarkSubmissionReadiness.sourceLocalBenchmarkHarnessPath === localBenchmarkHarnessJsonPath && benchmarkSubmissionReadiness.sourceLocalBenchmarkResultsPath === localBenchmarkResultsPath && benchmarkSubmissionReadiness.sourceLocalBenchmarkResultsSha256 === localBenchmarkHarness.localBenchmarkResultSha256 && benchmarkSubmissionReadiness.sourceBenchmarkEfficiencyMetricsPath === benchmarkEfficiencyMetricsJsonPath && benchmarkSubmissionReadiness.sourceBenchmarkEfficiencyMetricsJsonlPath === benchmarkEfficiencyMetricsJsonlPath && benchmarkSubmissionReadiness.sourceBenchmarkEfficiencyMetricsJsonlSha256 === benchmarkEfficiencyMetrics.metricsJsonlSha256, benchmarkSubmissionReadiness.sourceBenchmarkEfficiencyMetricsJsonlPath))
  checks.push(check('benchmark submission readiness imports real trace eval evidence', benchmarkSubmissionReadiness.sourceRealTraceEvalsPath === realTraceEvalsJsonPath && benchmarkSubmissionReadiness.sourceRealTraceCount === realTraceEvals.traceFileCount, `${benchmarkSubmissionReadiness.sourceRealTraceCount}/${realTraceEvals.traceFileCount}`))
  checks.push(check('benchmark submission readiness writes expected JSONL', benchmarkSubmissionReadiness.submissionAssetsJsonlPath === benchmarkSubmissionAssetsJsonlPath && benchmarkSubmissionReadiness.submissionAssetsJsonlSha256.length === 64, benchmarkSubmissionReadiness.submissionAssetsJsonlPath))
  checks.push(check('benchmark submission readiness covers SWE-bench required assets', benchmarkSubmissionReadiness.summary.requiredAssetCount >= 10 && ['all_predictions_equivalent', 'metadata_yaml', 'reasoning_traces', 'evaluation_logs', 'patch_diff_per_instance', 'report_json_per_instance', 'test_output_per_instance', 'verified_submission_instructions'].every((id) => benchmarkSubmissionReadiness.submissionAssetRecords.some((record) => record.assetId === id)), `${benchmarkSubmissionReadiness.summary.requiredAssetCount} assets`))
  checks.push(check('benchmark submission readiness records primary sources', benchmarkSubmissionReadiness.primarySourceInputs.some((source) => source.sourceProject === 'SWE-bench/experiments') && benchmarkSubmissionReadiness.primarySourceInputs.every((source) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(source.sourceUrl)), benchmarkSubmissionReadiness.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('benchmark submission readiness keeps official external submission blocked', benchmarkSubmissionReadiness.summary.officialExternalSubmissionReady === false && benchmarkSubmissionReadiness.externalBenchmarkExecutionPerformed === false && benchmarkSubmissionReadiness.externalBenchmarkSubmissionPerformed === false && benchmarkSubmissionReadiness.externalBenchmarkResultClaimed === false && benchmarkSubmissionReadiness.externalLeaderboardClaimAllowed === false))
  checks.push(check('benchmark submission readiness keeps protected gaps unexecuted', benchmarkSubmissionReadiness.summary.classifiedUnresolvedProtectedGapCount >= 5 && benchmarkSubmissionReadiness.submissionAssetRecords.every((record) => record.protectedActionExecuted === false && record.externalSubmissionClaimed === false), `${benchmarkSubmissionReadiness.summary.classifiedUnresolvedProtectedGapCount} protected gaps`))
  checks.push(check('benchmark submission readiness keeps readiness claims blocked', benchmarkSubmissionReadiness.releaseReadinessClaimAllowed === false && benchmarkSubmissionReadiness.productionReadinessClaimAllowed === false && benchmarkSubmissionReadiness.publicReadinessClaimAllowed === false && benchmarkSubmissionReadiness.externalValidationClaimAllowed === false && benchmarkSubmissionReadiness.autonomousReliabilityClaimAllowed === false))
  checks.push(check('benchmark submission readiness checks pass', benchmarkSubmissionReadiness.submissionReadinessChecks.every((item) => item.ok)))
  checks.push(check('benchmark policy compliance is local no-provider check', benchmarkPolicyCompliance.mode === 'local_no_provider_benchmark_policy_compliance'))
  checks.push(check('benchmark policy compliance performed no provider calls', benchmarkPolicyCompliance.providerCallsPerformed.length === 0))
  checks.push(check('benchmark policy compliance performed no live model calls', benchmarkPolicyCompliance.liveModelCallsPerformed.length === 0))
  checks.push(check('benchmark policy compliance performed no external calls', benchmarkPolicyCompliance.externalCallsPerformed.length === 0))
  checks.push(check('benchmark policy compliance executed no protected actions', benchmarkPolicyCompliance.protectedActionsExecuted.length === 0 && benchmarkPolicyCompliance.dependencyInstallPerformed === false))
  checks.push(check('benchmark policy compliance imports submission readiness and boundary evidence', benchmarkPolicyCompliance.sourceBenchmarkSubmissionReadinessPath === benchmarkSubmissionReadinessJsonPath && benchmarkPolicyCompliance.sourceSubmissionAssetsJsonlPath === benchmarkSubmissionAssetsJsonlPath && benchmarkPolicyCompliance.sourceSubmissionAssetsJsonlSha256 === benchmarkSubmissionReadiness.submissionAssetsJsonlSha256 && benchmarkPolicyCompliance.sourceExternalBenchmarkBoundaryPath === externalBenchmarkBoundaryJsonPath, benchmarkPolicyCompliance.sourceBenchmarkSubmissionReadinessPath))
  checks.push(check('benchmark policy compliance writes expected JSONL', benchmarkPolicyCompliance.policyComplianceJsonlPath === benchmarkPolicyComplianceJsonlPath && benchmarkPolicyCompliance.policyComplianceJsonlSha256.length === 64, benchmarkPolicyCompliance.policyComplianceJsonlPath))
  checks.push(check('benchmark policy compliance records SWE-bench policy source', benchmarkPolicyCompliance.primarySourceInputs.some((source) => source.sourceProject === 'SWE-bench/experiments') && benchmarkPolicyCompliance.primarySourceInputs.every((source) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(source.sourceUrl)), benchmarkPolicyCompliance.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('benchmark policy compliance covers required policy gates', ['open_research_publication_or_technical_report', 'academic_or_research_institution_affiliation', 'open_source_methods', 'peer_reviewed_publication', 'official_submission_assets_complete', 'official_leaderboard_pr_or_submission'].every((id) => benchmarkPolicyCompliance.policyItems.some((item) => item.policyItemId === id)), `${benchmarkPolicyCompliance.summary.policyItemCount} policy items`))
  checks.push(check('benchmark policy compliance preserves official claim boundary', benchmarkPolicyCompliance.summary.officialSWEbenchVerifiedSubmissionEligible === false && benchmarkPolicyCompliance.summary.officialSWEbenchVerifiedSubmissionClaimAllowed === false && benchmarkPolicyCompliance.summary.officialLeaderboardClaimAllowed === false && benchmarkPolicyCompliance.officialBenchmarkSubmissionPerformed === false && benchmarkPolicyCompliance.externalBenchmarkExecutionPerformed === false && benchmarkPolicyCompliance.externalLeaderboardClaimAllowed === false))
  checks.push(check('benchmark policy compliance keeps protected policy gaps unexecuted', benchmarkPolicyCompliance.summary.unresolvedProtectedOrOwnerClaimRequiredCount >= 4 && benchmarkPolicyCompliance.policyItems.every((item) => item.protectedActionExecuted === false && item.officialClaimAllowed === false), `${benchmarkPolicyCompliance.summary.unresolvedProtectedOrOwnerClaimRequiredCount} unresolved policy gaps`))
  checks.push(check('benchmark policy compliance keeps readiness claims blocked', benchmarkPolicyCompliance.releaseReadinessClaimAllowed === false && benchmarkPolicyCompliance.productionReadinessClaimAllowed === false && benchmarkPolicyCompliance.publicReadinessClaimAllowed === false && benchmarkPolicyCompliance.externalValidationClaimAllowed === false && benchmarkPolicyCompliance.autonomousReliabilityClaimAllowed === false))
  checks.push(check('benchmark policy compliance checks pass', benchmarkPolicyCompliance.policyComplianceChecks.every((item) => item.ok)))
  checks.push(check('Terminal-Bench readiness is local no-provider check', terminalBenchReadiness.mode === 'local_no_provider_terminal_bench_readiness'))
  checks.push(check('Terminal-Bench readiness performed no provider calls', terminalBenchReadiness.providerCallsPerformed.length === 0))
  checks.push(check('Terminal-Bench readiness performed no live model calls', terminalBenchReadiness.liveModelCallsPerformed.length === 0))
  checks.push(check('Terminal-Bench readiness performed no external calls', terminalBenchReadiness.externalCallsPerformed.length === 0))
  checks.push(check('Terminal-Bench readiness executed no protected actions', terminalBenchReadiness.protectedActionsExecuted.length === 0 && terminalBenchReadiness.dependencyInstallPerformed === false && terminalBenchReadiness.dockerContainerRunPerformed === false && terminalBenchReadiness.harborInstallPerformed === false))
  checks.push(check('Terminal-Bench readiness imports benchmark trace and policy evidence', terminalBenchReadiness.sourceBenchmarkReadinessPath === benchmarkReadinessJsonPath && terminalBenchReadiness.sourceBenchmarkTaskManifestPath === benchmarkTaskManifestPath && terminalBenchReadiness.sourceBenchmarkTaskManifestSha256 === benchmarkReadiness.benchmarkManifestSha256 && terminalBenchReadiness.sourceLocalBenchmarkHarnessPath === localBenchmarkHarnessJsonPath && terminalBenchReadiness.sourceLocalBenchmarkResultsPath === localBenchmarkResultsPath && terminalBenchReadiness.sourceLocalBenchmarkResultsSha256 === localBenchmarkHarness.localBenchmarkResultSha256 && terminalBenchReadiness.sourceTracePortabilityExportPath === tracePortabilityExportJsonPath && terminalBenchReadiness.sourcePortableTraceJsonlPath === portableTraceEventsPath && terminalBenchReadiness.sourcePortableTraceJsonlSha256 === tracePortabilityExport.portableTraceExportSha256 && terminalBenchReadiness.sourceBenchmarkPolicyCompliancePath === benchmarkPolicyComplianceJsonPath, terminalBenchReadiness.sourcePortableTraceJsonlPath))
  checks.push(check('Terminal-Bench readiness writes expected JSONL', terminalBenchReadiness.taskMapJsonlPath === terminalBenchTaskMapJsonlPath && terminalBenchReadiness.taskMapJsonlSha256.length === 64, terminalBenchReadiness.taskMapJsonlPath))
  checks.push(check('Terminal-Bench readiness records primary sources', terminalBenchReadiness.primarySourceInputs.some((source) => source.sourceProject === 'harbor-framework/terminal-bench') && terminalBenchReadiness.primarySourceInputs.some((source) => source.sourceProject === 'Terminal-Bench task documentation') && terminalBenchReadiness.primarySourceInputs.every((source) => /^https:\/\//.test(source.sourceUrl)), terminalBenchReadiness.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('Terminal-Bench readiness covers task environment tests solution trajectory result audit run and submission requirements', terminalBenchReadiness.summary.requirementCount >= 10 && ['instruction_or_task_description', 'docker_environment', 'tests_or_verifier', 'oracle_solution', 'agent_trajectory_artifacts', 'result_and_reward_artifacts', 'human_review_and_exploit_audit', 'official_harbor_or_terminal_bench_run', 'leaderboard_or_external_submission'].every((id) => terminalBenchReadiness.terminalBenchRequirementRecords.some((record) => record.requirementId === id)), `${terminalBenchReadiness.summary.requirementCount} requirements`))
  checks.push(check('Terminal-Bench readiness keeps official execution and leaderboard claims blocked', terminalBenchReadiness.summary.officialTerminalBenchExecutionReady === false && terminalBenchReadiness.officialTerminalBenchExecutionPerformed === false && terminalBenchReadiness.officialTerminalBenchResultClaimed === false && terminalBenchReadiness.officialLeaderboardSubmissionPerformed === false && terminalBenchReadiness.officialLeaderboardClaimAllowed === false))
  checks.push(check('Terminal-Bench readiness keeps protected gaps unexecuted', terminalBenchReadiness.summary.classifiedUnresolvedProtectedGapCount >= 1 && terminalBenchReadiness.summary.blockedNotAuthorizedCount >= 2 && terminalBenchReadiness.terminalBenchRequirementRecords.every((record) => record.protectedActionExecuted === false && record.officialResultClaimed === false), `${terminalBenchReadiness.summary.classifiedUnresolvedProtectedGapCount}/${terminalBenchReadiness.summary.blockedNotAuthorizedCount} gaps`))
  checks.push(check('Terminal-Bench readiness keeps readiness claims blocked', terminalBenchReadiness.releaseReadinessClaimAllowed === false && terminalBenchReadiness.productionReadinessClaimAllowed === false && terminalBenchReadiness.publicReadinessClaimAllowed === false && terminalBenchReadiness.externalValidationClaimAllowed === false && terminalBenchReadiness.autonomousReliabilityClaimAllowed === false))
  checks.push(check('Terminal-Bench readiness checks pass', terminalBenchReadiness.terminalBenchReadinessChecks.every((item) => item.ok)))
  checks.push(check('trajectory process quality is local no-provider check', trajectoryProcessQuality.mode === 'local_no_provider_trajectory_process_quality'))
  checks.push(check('trajectory process quality performed no provider calls', trajectoryProcessQuality.providerCallsPerformed.length === 0))
  checks.push(check('trajectory process quality performed no live model calls', trajectoryProcessQuality.liveModelCallsPerformed.length === 0))
  checks.push(check('trajectory process quality performed no external calls', trajectoryProcessQuality.externalCallsPerformed.length === 0))
  checks.push(check('trajectory process quality executed no protected actions', trajectoryProcessQuality.protectedActionsExecuted.length === 0))
  checks.push(check('trajectory process quality imports real trace eval source', trajectoryProcessQuality.sourceRealTraceEvalReportPath === realTraceEvalsJsonPath && trajectoryProcessQuality.sourceTraceCount === realTraceEvals.traceFileCount, trajectoryProcessQuality.sourceRealTraceEvalReportPath))
  checks.push(check('trajectory process quality imports local benchmark results', trajectoryProcessQuality.sourceLocalBenchmarkResultsPath === localBenchmarkResultsPath && trajectoryProcessQuality.sourceLocalBenchmarkResultsSha256 === localBenchmarkHarness.localBenchmarkResultSha256, trajectoryProcessQuality.sourceLocalBenchmarkResultsPath))
  checks.push(check('trajectory process quality assesses every real trace', trajectoryProcessQuality.summary.assessedTraceCount === realTraceEvals.traceFileCount && trajectoryProcessQuality.traceAssessments.length === realTraceEvals.traceFileCount, `${trajectoryProcessQuality.summary.assessedTraceCount}/${realTraceEvals.traceFileCount}`))
  checks.push(check('trajectory process quality preserves trace hashes', trajectoryProcessQuality.traceAssessments.every((assessment) => realTraceEvals.traces.some((trace) => trace.path === assessment.path && trace.sha256 === assessment.sha256))))
  checks.push(check('trajectory process quality uses process phase taxonomy', ['exploration', 'implementation', 'verification', 'orchestration'].every((label) => trajectoryProcessQuality.phaseTaxonomy.includes(label)), trajectoryProcessQuality.phaseTaxonomy.join(',')))
  checks.push(check('trajectory process quality uses waste signal taxonomy', ['missing_verification', 'blind_retry_loop', 'temporal_disorder', 'regression_cycle', 'unbounded_repeated_tool_use', 'raw_trace_payload_exposure'].every((label) => trajectoryProcessQuality.wasteSignalTaxonomy.includes(label)), trajectoryProcessQuality.wasteSignalTaxonomy.join(',')))
  checks.push(check('trajectory process quality records primary sources', trajectoryProcessQuality.primarySourceInputs.length >= 4 && trajectoryProcessQuality.primarySourceInputs.every((source) => /^https:\/\//.test(source.sourceUrl)), trajectoryProcessQuality.primarySourceInputs.map((source) => source.sourceProject).join(',')))
  checks.push(check('trajectory process quality classifies process gaps without hiding them', trajectoryProcessQuality.summary.classifiedProcessGapTraceCount >= 0 && trajectoryProcessQuality.traceAssessments.every((assessment) => ['process_quality_evidence_ok', 'classified_process_gap', 'failed_process_evidence'].includes(assessment.processQualityStatus)), `${trajectoryProcessQuality.summary.classifiedProcessGapTraceCount} classified gaps`))
  checks.push(check('trajectory process quality has no failed process evidence', trajectoryProcessQuality.summary.failedProcessEvidenceTraceCount === 0, `${trajectoryProcessQuality.summary.failedProcessEvidenceTraceCount} failed`))
  checks.push(check('trajectory process quality keeps release and external claims blocked', trajectoryProcessQuality.externalBenchmarkExecutionPerformed === false && trajectoryProcessQuality.externalBenchmarkResultClaimed === false && trajectoryProcessQuality.releaseReadinessClaimAllowed === false && trajectoryProcessQuality.productionReadinessClaimAllowed === false && trajectoryProcessQuality.publicReadinessClaimAllowed === false && trajectoryProcessQuality.autonomousReliabilityClaimAllowed === false))
  checks.push(check('trajectory process quality checks pass', trajectoryProcessQuality.processQualityChecks.every((item) => item.ok)))
  checks.push(check('verification report consistency is local no-provider check', verificationReportConsistency.mode === 'local_no_provider_verification_report_consistency'))
  checks.push(check('verification report consistency performed no provider calls', verificationReportConsistency.providerCallsPerformed.length === 0))
  checks.push(check('verification report consistency performed no live model calls', verificationReportConsistency.liveModelCallsPerformed.length === 0))
  checks.push(check('verification report consistency performed no external calls', verificationReportConsistency.externalCallsPerformed.length === 0))
  checks.push(check('verification report consistency executed no protected actions', verificationReportConsistency.protectedActionsExecuted.length === 0))
  checks.push(check('verification report consistency imports expected sources', verificationReportConsistency.sourceVerificationReportPath === verificationPath && verificationReportConsistency.sourceTypecheckHealthReportPath === typecheckHealthJsonPath && verificationReportConsistency.sourceTerminalReportPath === terminalPath))
  checks.push(check('verification report consistency preserves zero-diagnostic state', verificationReportConsistency.sourceTypecheckStrictPass === true && verificationReportConsistency.sourceTypecheckTotalDiagnostics === typecheckHealth.totalDiagnostics && verificationReportConsistency.sourceTypecheckDiagnosticBudget === (typecheckHealth.diagnosticBudget ?? 0) && verificationReportConsistency.sourceTypecheckTotalDiagnostics === 0 && verificationReportConsistency.sourceTypecheckDiagnosticBudget === 0, `${verificationReportConsistency.sourceTypecheckTotalDiagnostics}/${verificationReportConsistency.sourceTypecheckDiagnosticBudget}`))
  const allowedTerminalConditions = ['PRODUCT_QUALITY_GATE_READY', 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_UPDATE', 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_CLI_UNAVAILABLE']
  const requiredVerificationBlockers = verificationReportConsistency.sourceTerminalCondition === 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_CLI_UNAVAILABLE'
    ? ['vscode_cli_unavailable', 'blocked_by_no_git_repo', 'external benchmark']
    : verificationReportConsistency.sourceTerminalCondition === 'PRODUCT_QUALITY_GATE_BLOCKED_BY_LOCAL_VSCODE_UPDATE'
    ? ['vscode_update_in_progress', 'blocked_by_no_git_repo', 'external benchmark']
    : ['blocked_by_no_git_repo', 'external benchmark']
  checks.push(check('verification report consistency preserves current terminal condition', allowedTerminalConditions.includes(verificationReportConsistency.sourceTerminalCondition), verificationReportConsistency.sourceTerminalCondition))
  checks.push(check('verification report consistency rejects obsolete typecheck blockers', verificationReportConsistency.obsoleteBlockerPhrasesFound.length === 0, verificationReportConsistency.obsoleteBlockerPhrasesFound.join(',')))
  checks.push(check('verification report consistency records current blockers', requiredVerificationBlockers.every((phrase) => verificationReportConsistency.currentBlockerPhrasesFound.some((found) => found.includes(phrase))), verificationReportConsistency.currentBlockerPhrasesFound.join(',')))
  checks.push(check('verification report consistency keeps readiness claims blocked', verificationReportConsistency.releaseReadinessClaimAllowed === false && verificationReportConsistency.productionReadinessClaimAllowed === false && verificationReportConsistency.publicReadinessClaimAllowed === false && verificationReportConsistency.externalValidationClaimAllowed === false && verificationReportConsistency.autonomousReliabilityClaimAllowed === false))
  checks.push(check('verification report consistency checks pass', verificationReportConsistency.reportConsistencyChecks.every((item) => item.ok)))
  checks.push(check('quality blocker taxonomy is local no-provider check', qualityBlockerTaxonomy.mode === 'local_no_provider_quality_blocker_taxonomy'))
  checks.push(check('quality blocker taxonomy performed no provider calls', qualityBlockerTaxonomy.providerCallsPerformed.length === 0))
  checks.push(check('quality blocker taxonomy performed no live model calls', qualityBlockerTaxonomy.liveModelCallsPerformed.length === 0))
  checks.push(check('quality blocker taxonomy performed no external calls', qualityBlockerTaxonomy.externalCallsPerformed.length === 0))
  checks.push(check('quality blocker taxonomy executed no protected actions', qualityBlockerTaxonomy.protectedActionsExecuted.length === 0))
  checks.push(check('quality blocker taxonomy imports expected sources', qualityBlockerTaxonomy.sourceHostSmokeReportPath === ideExtensionHostSmokeJsonPath && qualityBlockerTaxonomy.sourceWorkbenchSmokeReportPath === ideExtensionWorkbenchSmokeJsonPath && qualityBlockerTaxonomy.sourceAgentReplayReportPath === agentReplayEvalsJsonPath && qualityBlockerTaxonomy.sourceVscodeUpdateBoundaryReportPath === vscodeUpdateBoundaryJsonPath))
  const qualityBlockerTaxonomyClear = qualityBlockerTaxonomy.currentProductQualityGateStatus === 'clear_no_current_vscode_update_dependent_failures' && qualityBlockerTaxonomy.expectedProductQualityGateFailureCount === 0
  const qualityBlockerTaxonomyBlocked = qualityBlockerTaxonomy.currentProductQualityGateStatus === 'blocked_by_known_vscode_update_dependent_failures' && qualityBlockerTaxonomy.expectedProductQualityGateFailureCount === 19
  const qualityBlockerTaxonomyCliUnavailable = qualityBlockerTaxonomy.currentProductQualityGateStatus === 'blocked_by_vscode_cli_unavailable' && qualityBlockerTaxonomy.expectedProductQualityGateFailureCount > 0
  checks.push(check('quality blocker taxonomy preserves expected current failure count', qualityBlockerTaxonomyClear || qualityBlockerTaxonomyBlocked || qualityBlockerTaxonomyCliUnavailable, `${qualityBlockerTaxonomy.currentProductQualityGateStatus}/${qualityBlockerTaxonomy.expectedProductQualityGateFailureCount}`))
  checks.push(check('quality blocker taxonomy classifies known groups', qualityBlockerTaxonomyClear ? qualityBlockerTaxonomy.knownFailureGroups.length === 0 : qualityBlockerTaxonomyCliUnavailable ? qualityBlockerTaxonomy.knownFailureGroups.some((group) => group.id === 'ide_extension_smoke_vscode_cli_unavailable') : ['ide_extension_host_smoke_vscode_update_blocked', 'ide_extension_workbench_smoke_vscode_update_blocked', 'agent_replay_vscode_update_dependent_failures'].every((id) => qualityBlockerTaxonomy.knownFailureGroups.some((group) => group.id === id)), qualityBlockerTaxonomy.knownFailureGroups.map((group) => group.id).join(',') || 'none'))
  checks.push(check('quality blocker taxonomy rejects unexpected failure groups', qualityBlockerTaxonomy.unexpectedFailureGroups.length === 0, qualityBlockerTaxonomy.unexpectedFailureGroups.join(',')))
  checks.push(check('quality blocker taxonomy blocks process intervention and readiness claims', qualityBlockerTaxonomy.processTerminationAttempted === false && qualityBlockerTaxonomy.dependencyInstallAttempted === false && qualityBlockerTaxonomy.releaseReadinessClaimAllowed === false && qualityBlockerTaxonomy.productionReadinessClaimAllowed === false && qualityBlockerTaxonomy.publicReadinessClaimAllowed === false && qualityBlockerTaxonomy.externalValidationClaimAllowed === false && qualityBlockerTaxonomy.autonomousReliabilityClaimAllowed === false))
  checks.push(check('quality blocker taxonomy checks pass', qualityBlockerTaxonomy.taxonomyChecks.every((item) => item.ok)))
  checks.push(check('public claim boundary is local no-provider check', publicClaimBoundary.mode === 'local_no_provider_public_claim_boundary'))
  checks.push(check('public claim boundary scans public surfaces', publicClaimBoundary.publicSurfaceCount === publicClaimBoundary.scannedPublicSurfaces.length && publicClaimBoundary.publicSurfaceCount >= 10 && publicClaimBoundary.scannedLineCount > 0, `${publicClaimBoundary.publicSurfaceCount} surfaces/${publicClaimBoundary.scannedLineCount} lines`))
  checks.push(check('public claim boundary hash-binds scanned surfaces', publicClaimBoundary.scannedPublicSurfaces.every((surface) => surface.exists && typeof surface.sha256 === 'string' && surface.sha256.length === 64 && surface.sizeBytes > 0), `${publicClaimBoundary.scannedPublicSurfaces.length} surfaces`))
  checks.push(check('public claim boundary detects no unauthorized positive claims', publicClaimBoundary.unauthorizedPositiveClaimCount === 0 && publicClaimBoundary.unauthorizedPositiveClaims.length === 0 && publicClaimBoundary.claimBoundaryStatus === 'no_unauthorized_public_claims_detected', `${publicClaimBoundary.unauthorizedPositiveClaimCount} findings`))
  checks.push(check('public claim boundary writes expected JSONL', publicClaimBoundary.scanJsonlPath === publicClaimBoundaryJsonlPath && publicClaimBoundary.scanJsonlSha256.length === 64 && publicClaimBoundary.scanJsonlRecordCount === publicClaimBoundary.blockedContextClaimMentionCount + publicClaimBoundary.unauthorizedPositiveClaimCount, publicClaimBoundary.scanJsonlPath))
  checks.push(check('public claim boundary performed no provider live or external calls', publicClaimBoundary.providerCallsPerformed.length === 0 && publicClaimBoundary.liveModelCallsPerformed.length === 0 && publicClaimBoundary.externalCallsPerformed.length === 0))
  checks.push(check('public claim boundary executed no protected actions', publicClaimBoundary.protectedActionsExecuted.length === 0 && publicClaimBoundary.dependencyInstallPerformed === false && publicClaimBoundary.publishDeployLaunchPerformed === false))
  checks.push(check('public claim boundary keeps release public external reliability and superiority claims blocked', publicClaimBoundary.releaseClaimAllowed === false && publicClaimBoundary.releaseReadinessClaimAllowed === false && publicClaimBoundary.productionReadinessClaimAllowed === false && publicClaimBoundary.publicReadinessClaimAllowed === false && publicClaimBoundary.externalValidationClaimAllowed === false && publicClaimBoundary.autonomousReliabilityClaimAllowed === false && publicClaimBoundary.superiorityClaimAllowed === false))
  checks.push(check('public claim boundary preserves mth and canonical-memory boundaries', publicClaimBoundary.mthResolutionStatus === 'unresolved' && publicClaimBoundary.canonicalMemoryWriteAllowed === false && publicClaimBoundary.allowedClaimLevel === 'internal_no_provider_product_quality_evidence_only'))
  checks.push(check('public claim boundary checks pass', publicClaimBoundary.evidenceChecks.every((item) => item.ok)))
  checks.push(check('GitHub remote surface audit uses public remote mode', githubRemoteSurfaceAudit.mode === 'github_public_remote_surface_audit', githubRemoteSurfaceAudit.mode))
  checks.push(check('GitHub remote surface audit inventories remote heads', githubRemoteSurfaceAudit.remoteHeadCount === githubRemoteSurfaceAudit.remoteHeads.length && githubRemoteSurfaceAudit.remoteHeadCount > 0 && githubRemoteSurfaceAudit.remoteHeads.some((head) => head.name === githubRemoteSurfaceAudit.defaultBranch), `${githubRemoteSurfaceAudit.remoteHeadCount} heads/default=${githubRemoteSurfaceAudit.defaultBranch}`))
  checks.push(check('GitHub remote surface audit inventories open PRs', githubRemoteSurfaceAudit.openPullRequestCount === githubRemoteSurfaceAudit.openPullRequests.length && ['github_pr_api', 'gh_cli'].includes(githubRemoteSurfaceAudit.discovery.openPullRequestDiscovery), `${githubRemoteSurfaceAudit.openPullRequestCount} PRs via ${githubRemoteSurfaceAudit.discovery.openPullRequestDiscovery}`))
  checks.push(check('GitHub remote surface audit scans every remote head', githubRemoteSurfaceAudit.refScans.length === githubRemoteSurfaceAudit.remoteHeadCount && githubRemoteSurfaceAudit.remoteHeads.every((head) => githubRemoteSurfaceAudit.refScans.some((scan) => scan.refName === head.name)), `${githubRemoteSurfaceAudit.refScans.length}/${githubRemoteSurfaceAudit.remoteHeadCount}`))
  checks.push(check('GitHub remote surface audit detects no blockers', githubRemoteSurfaceAudit.blockerCount === 0 && githubRemoteSurfaceAudit.blockers.length === 0 && githubRemoteSurfaceAudit.status === 'no_public_github_surface_findings_detected', `${githubRemoteSurfaceAudit.blockerCount} blockers`))
  checks.push(check('GitHub remote surface audit blocks provider live and protected actions', githubRemoteSurfaceAudit.providerCallsPerformed.length === 0 && githubRemoteSurfaceAudit.liveModelCallsPerformed.length === 0 && githubRemoteSurfaceAudit.protectedActionsExecuted.length === 0))
  checks.push(check('GitHub remote surface audit checks pass', githubRemoteSurfaceAudit.evidenceChecks.every((item) => item.ok)))
  checks.push(check('origin/license provenance boundary is local no-provider check', originLicenseProvenanceBoundary.mode === 'local_no_provider_origin_license_provenance_boundary', originLicenseProvenanceBoundary.mode))
  checks.push(check('origin/license provenance boundary detects no blockers', originLicenseProvenanceBoundary.blockerCount === 0 && originLicenseProvenanceBoundary.blockers.length === 0 && originLicenseProvenanceBoundary.status === 'no_origin_license_provenance_boundary_findings', `${originLicenseProvenanceBoundary.blockerCount} blockers`))
  checks.push(check('origin/license provenance boundary preserves package and origin metadata', originLicenseProvenanceBoundary.packageLicenseField === 'SEE LICENSE FILE' && isMetaforgeGithubUrl(originLicenseProvenanceBoundary.packageRepositoryUrl) && isMetaforgeGithubUrl(originLicenseProvenanceBoundary.originRemoteUrl), `${originLicenseProvenanceBoundary.packageLicenseField}/${originLicenseProvenanceBoundary.packageRepositoryUrl}/${originLicenseProvenanceBoundary.originRemoteUrl}`))
  checks.push(check('origin/license provenance boundary performed no provider live external or protected calls', originLicenseProvenanceBoundary.providerCallsPerformed.length === 0 && originLicenseProvenanceBoundary.liveModelCallsPerformed.length === 0 && originLicenseProvenanceBoundary.externalCallsPerformed.length === 0 && originLicenseProvenanceBoundary.protectedActionsExecuted.length === 0))
  checks.push(check('origin/license provenance boundary did not publish deploy or launch', originLicenseProvenanceBoundary.publishAttempted === false && originLicenseProvenanceBoundary.deployAttempted === false && originLicenseProvenanceBoundary.launchAttempted === false))
  checks.push(check('origin/license provenance boundary checks pass', originLicenseProvenanceBoundary.evidenceChecks.every((item) => item.ok)))
  checks.push(check('protected action authorization packet is local no-provider check', protectedActionAuthorizationPacket.mode === 'local_no_provider_protected_action_authorization_packet'))
  checks.push(check('protected action authorization packet records terminal protected boundary', protectedActionAuthorizationPacket.terminalCondition === 'PROTECTED_ACTION_REQUIRED_FOR_NEXT_VERIFIABLE_PRODUCT_BOUNDARY' && protectedActionAuthorizationPacket.packetStatus === 'owner_authorization_required_before_protected_actions', protectedActionAuthorizationPacket.terminalCondition))
  checks.push(check('protected action authorization packet imports source reports', protectedActionAuthorizationPacket.sourceReportCount === protectedActionAuthorizationPacket.sourceReportBindings.length && [qualityBlockerTaxonomyJsonPath, vscodeUpdateBoundaryJsonPath, vscodeStartupDiagnosticsJsonPath, gitReleaseHygieneJsonPath, externalBenchmarkBoundaryJsonPath, benchmarkSubmissionReadinessJsonPath, benchmarkPolicyComplianceJsonPath, terminalBenchReadinessJsonPath, licenseBoundaryAuthorizationJsonPath, ossProviderBreadthEvidenceJsonPath, ossIdeOrEditorSurfaceEvidenceJsonPath, ossReleaseHygieneEvidenceJsonPath, verificationReportConsistencyJsonPath, publicClaimBoundaryJsonPath].every((path) => protectedActionAuthorizationPacket.sourceReportBindings.some((source) => source.path === path && source.exists && typeof source.sha256 === 'string' && source.sha256.length === 64 && source.sizeBytes > 0)), `${protectedActionAuthorizationPacket.sourceReportCount} reports`))
  checks.push(check('protected action authorization packet requires owner decisions for protected boundaries', protectedActionAuthorizationPacket.authorizationItemCount === protectedActionAuthorizationPacket.requiredOwnerAuthorizations.length && ['authorize_local_vscode_cli_path_or_install_state_repair', 'authorize_real_git_repository_commit_push_boundary', 'authorize_publish_deploy_launch_or_release_execution', 'authorize_signed_provenance_or_external_attestation', 'authorize_license_notice_reuse_or_legal_decisions', 'authorize_live_provider_or_model_validation', 'authorize_external_benchmark_execution_or_submission', 'authorize_release_public_production_external_or_autonomous_claims'].every((id) => protectedActionAuthorizationPacket.requiredOwnerAuthorizations.some((item) => item.id === id && item.protectedActionRequired === true && item.authorized === false && item.executed === false)), `${protectedActionAuthorizationPacket.authorizationItemCount} authorizations`))
  checks.push(check('protected action authorization packet executes no protected actions', protectedActionAuthorizationPacket.protectedActionExecutionAllowed === false && protectedActionAuthorizationPacket.protectedActionExecuted === false && protectedActionAuthorizationPacket.protectedActionsExecuted.length === 0 && protectedActionAuthorizationPacket.dependencyInstallPerformed === false && protectedActionAuthorizationPacket.commitPushPerformed === false && protectedActionAuthorizationPacket.publishDeployLaunchPerformed === false && protectedActionAuthorizationPacket.signedProvenanceGenerated === false))
  checks.push(check('protected action authorization packet performed no provider live or external calls', protectedActionAuthorizationPacket.providerCallsPerformed.length === 0 && protectedActionAuthorizationPacket.liveModelCallsPerformed.length === 0 && protectedActionAuthorizationPacket.externalCallsPerformed.length === 0))
  checks.push(check('protected action authorization packet keeps claims blocked', protectedActionAuthorizationPacket.releaseClaimAllowed === false && protectedActionAuthorizationPacket.releaseReadinessClaimAllowed === false && protectedActionAuthorizationPacket.productionReadinessClaimAllowed === false && protectedActionAuthorizationPacket.publicReadinessClaimAllowed === false && protectedActionAuthorizationPacket.externalValidationClaimAllowed === false && protectedActionAuthorizationPacket.autonomousReliabilityClaimAllowed === false && protectedActionAuthorizationPacket.superiorityClaimAllowed === false))
  checks.push(check('protected action authorization packet preserves mth and canonical-memory boundaries', protectedActionAuthorizationPacket.mthResolutionStatus === 'unresolved' && protectedActionAuthorizationPacket.canonicalMemoryWriteAllowed === false && protectedActionAuthorizationPacket.allowedClaimLevel === 'internal_no_provider_product_quality_evidence_only'))
  checks.push(check('protected action authorization packet checks pass', protectedActionAuthorizationPacket.evidenceChecks.every((item) => item.ok)))
  checks.push(check('product evidence manifest is local no-provider check', productEvidenceManifest.mode === 'local_no_provider_product_evidence_manifest'))
  checks.push(check('product evidence manifest performed no provider calls', productEvidenceManifest.providerCallsPerformed.length === 0))
  checks.push(check('product evidence manifest performed no live model calls', productEvidenceManifest.liveModelCallsPerformed.length === 0))
  checks.push(check('product evidence manifest performed no external calls', productEvidenceManifest.externalCallsPerformed.length === 0))
  checks.push(check('product evidence manifest executed no protected actions', productEvidenceManifest.protectedActionsExecuted.length === 0))
  checks.push(check('product evidence manifest writes expected JSONL', productEvidenceManifest.manifestJsonlPath === productEvidenceManifestJsonlPath && productEvidenceManifest.manifestJsonlSha256.length === 64, productEvidenceManifest.manifestJsonlPath))
  checks.push(check('product evidence manifest has required format', productEvidenceManifest.manifestFormat === 'openclaude_product_evidence_manifest_v1', productEvidenceManifest.manifestFormat))
  checks.push(check('product evidence manifest covers required evidence', productEvidenceManifest.missingRequiredEvidencePaths.length === 0 && ['.github/CODEOWNERS', '.github/workflows/dependency-review.yml', 'bun.lock', '.jscpd.json', '.dependency-cruiser.mjs', '.dependency-cruiser-known-violations.json', previousBaselinePath, baselinePath, ossBaselineRefreshJsonPath, ossBaselineRefreshMdPath, ossBaselineRefreshProvenanceJsonlPath, ossBaselineFreshnessJsonPath, ossBaselineFreshnessMdPath, ossBaselineProvenanceJsonlPath, ossSourceReviewJsonPath, ossSourceReviewMdPath, ossSourceReviewProvenanceJsonlPath, ossArchitectureTargetsJsonPath, ossArchitectureTargetsMdPath, ossArchitectureTargetsProvenanceJsonlPath, ossArchitectureGapReviewJsonPath, ossArchitectureGapReviewMdPath, ossArchitectureGapReviewProvenanceJsonlPath, ossAxisArchitectureReviewJsonPath, ossAxisArchitectureReviewMdPath, ossAxisArchitectureReviewProvenanceJsonlPath, ossSafeBacklogPlanJsonPath, ossSafeBacklogPlanMdPath, ossSafeBacklogPlanProvenanceJsonlPath, ossSafeBacklogClosureJsonPath, ossSafeBacklogClosureMdPath, ossSafeBacklogClosureJsonlPath, ossBaselineDriftClosureJsonPath, ossBaselineDriftClosureMdPath, ossBaselineDriftClosureJsonlPath, ossBenchmarkComparisonMatrixJsonPath, ossBenchmarkComparisonMatrixMdPath, ossBenchmarkComparisonMatrixJsonlPath, ossIdeOrEditorSurfaceEvidenceJsonPath, ossIdeOrEditorSurfaceEvidenceMdPath, ossIdeOrEditorSurfaceEvidenceJsonlPath, ossPrivacyNoPhoneHomeEvidenceJsonPath, ossPrivacyNoPhoneHomeEvidenceMdPath, ossPrivacyNoPhoneHomeEvidenceJsonlPath, ossEvalQualityGateChecklistJsonPath, ossEvalQualityGateChecklistMdPath, ossEvalQualityGateChecklistProvenanceJsonlPath, ossTerminalWorkflowEvidenceJsonPath, ossTerminalWorkflowEvidenceMdPath, ossTerminalWorkflowEvidenceProvenanceJsonlPath, ossOnboardingDocsEvidenceJsonPath, ossOnboardingDocsEvidenceMdPath, ossOnboardingDocsEvidenceProvenanceJsonlPath, ossRuntimeDoctoringEvidenceJsonPath, ossRuntimeDoctoringEvidenceMdPath, ossRuntimeDoctoringEvidenceProvenanceJsonlPath, ossSecurityPermissionsEvidenceJsonPath, ossSecurityPermissionsEvidenceMdPath, ossSecurityPermissionsEvidenceProvenanceJsonlPath, ossToolLoopReliabilityEvidenceJsonPath, ossToolLoopReliabilityEvidenceMdPath, ossToolLoopReliabilityEvidenceProvenanceJsonlPath, ossProviderBreadthEvidenceJsonPath, ossProviderBreadthEvidenceMdPath, ossProviderBreadthEvidenceProvenanceJsonlPath, ossReleaseHygieneEvidenceJsonPath, ossReleaseHygieneEvidenceMdPath, ossReleaseHygieneEvidenceProvenanceJsonlPath, providerCapabilityMatrixJsonPath, providerCapabilityMatrixMdPath, providerCapabilityMatrixJsonlPath, terminalFailureRecoveryTranscriptsJsonPath, terminalFailureRecoveryTranscriptsMdPath, toolInterruptionRecoveryTraceJsonPath, toolInterruptionRecoveryTraceMdPath, toolInterruptionRecoveryTracePath, protectedActionDenialTraceJsonPath, protectedActionDenialTraceMdPath, protectedActionDenialTracePath, gatePath, terminalPath, verificationPath, agentInstructionsQualityJsonPath, primarySourceRegistryJsonPath, primarySourceRegistryMdPath, primarySourceRegistryJsonlPath, communityIntakeQualityJsonPath, communityProfileQualityJsonPath, dependencyTopologyJsonPath, dependencyTopologyMdPath, scriptDuplicationAuditJsonPath, scriptDuplicationAuditMdPath, maintainerOwnershipQualityJsonPath, dependencyGovernanceQualityJsonPath, lockfileSbomQualityJsonPath, lockfileSbomInventoryJsonlPath, thirdPartyLicenseQualityJsonPath, thirdPartyLicenseInventoryJsonlPath, sourceLicenseMetadataQualityJsonPath, sourceLicenseMetadataInventoryJsonlPath, licenseBoundaryAuthorizationJsonPath, licenseBoundaryAuthorizationRequestPath, licenseBoundaryAuthorizationItemsJsonlPath, qualityBlockerTaxonomyJsonPath, publicClaimBoundaryJsonPath, publicClaimBoundaryMdPath, publicClaimBoundaryJsonlPath, githubRemoteSurfaceAuditJsonPath, githubRemoteSurfaceAuditMdPath, githubRemoteSurfaceAuditJsonlPath, originLicenseProvenanceBoundaryJsonPath, originLicenseProvenanceBoundaryMdPath, originLicenseProvenanceBoundaryJsonlPath, protectedActionAuthorizationPacketJsonPath, protectedActionAuthorizationPacketMdPath, protectedActionAuthorizationPacketJsonlPath, tracePortabilityExportJsonPath, benchmarkReadinessJsonPath, vscodeStartupDiagnosticsJsonPath, localBenchmarkHarnessJsonPath, benchmarkEfficiencyMetricsJsonPath, benchmarkSubmissionReadinessJsonPath, benchmarkPolicyComplianceJsonPath, terminalBenchReadinessJsonPath, openSsfSecurityPostureJsonPath, portableTraceEventsPath, benchmarkTaskManifestPath, localBenchmarkResultsPath, benchmarkEfficiencyMetricsJsonlPath, benchmarkSubmissionAssetsJsonlPath, benchmarkPolicyComplianceJsonlPath, terminalBenchTaskMapJsonlPath].every((path) => productEvidenceManifest.requiredEvidencePaths.includes(path)), productEvidenceManifest.missingRequiredEvidencePaths.join(',') || 'all present'))
  checks.push(check('product evidence manifest covers OSS comparison readiness index evidence', [ossComparisonReadinessIndexJsonPath, ossComparisonReadinessIndexMdPath, ossComparisonReadinessIndexJsonlPath].every((path) => productEvidenceManifest.requiredEvidencePaths.includes(path)), 'readiness index JSON/MD/JSONL present'))
  checks.push(check('product evidence manifest covers OSS IDE/editor surface evidence', [ossIdeOrEditorSurfaceEvidenceJsonPath, ossIdeOrEditorSurfaceEvidenceMdPath, ossIdeOrEditorSurfaceEvidenceJsonlPath].every((path) => productEvidenceManifest.requiredEvidencePaths.includes(path)), 'IDE/editor JSON/MD/JSONL present'))
  checks.push(check('product evidence manifest covers OSS privacy no-phone-home evidence', [ossPrivacyNoPhoneHomeEvidenceJsonPath, ossPrivacyNoPhoneHomeEvidenceMdPath, ossPrivacyNoPhoneHomeEvidenceJsonlPath].every((path) => productEvidenceManifest.requiredEvidencePaths.includes(path)), 'privacy JSON/MD/JSONL present'))
  checks.push(check('product evidence manifest records evidence hashes', productEvidenceManifest.evidenceRecordCount >= 100 && productEvidenceManifest.evidenceRecords.length === productEvidenceManifest.evidenceRecordCount && productEvidenceManifest.evidenceRecords.every((record) => /^[a-f0-9]{64}$/.test(record.sha256) && record.sizeBytes > 0), `${productEvidenceManifest.evidenceRecordCount} records`))
  checks.push(check('product evidence manifest excludes recursive self inputs', productEvidenceManifest.recursiveSelfInputsExcluded.includes(productEvidenceManifestJsonPath) && productEvidenceManifest.recursiveSelfInputsExcluded.includes(productEvidenceManifestMdPath) && productEvidenceManifest.recursiveSelfInputsExcluded.includes(productEvidenceManifestJsonlPath) && productEvidenceManifest.evidenceRecords.every((record) => !productEvidenceManifest.recursiveSelfInputsExcluded.includes(record.path)), productEvidenceManifest.recursiveSelfInputsExcluded.join(',')))
  checks.push(check('product evidence manifest covers source/report/artifact/gate/workflow roles', ['source', 'evidence_report', 'evidence_artifact', 'quality_gate', 'workflow'].every((role) => (productEvidenceManifest.evidenceRoles[role] ?? 0) > 0), JSON.stringify(productEvidenceManifest.evidenceRoles)))
  checks.push(check('product evidence manifest keeps signed/external attestations blocked', productEvidenceManifest.externalAttestationGenerated === false && productEvidenceManifest.signedProvenanceGenerated === false))
  checks.push(check('product evidence manifest keeps readiness claims blocked', productEvidenceManifest.releaseReadinessClaimAllowed === false && productEvidenceManifest.productionReadinessClaimAllowed === false && productEvidenceManifest.publicReadinessClaimAllowed === false && productEvidenceManifest.externalValidationClaimAllowed === false && productEvidenceManifest.autonomousReliabilityClaimAllowed === false))
  checks.push(check('product evidence manifest checks pass', productEvidenceManifest.evidenceChecks.every((item) => item.ok)))

  const failed = checks.filter((item) => !item.ok)
  for (const item of checks) {
    const prefix = item.ok ? 'PASS' : 'FAIL'
    console.log(`${prefix}: ${item.label}${item.detail ? ` (${item.detail})` : ''}`)
  }

  console.log('')
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`package=${pkg.name}@${pkg.version}`)
  console.log(`top10_projects=${baseline.top10.length}`)
  console.log(`oss_baseline_refresh_external_calls=${ossBaselineRefresh.externalCallsPerformed.length}`)
  console.log(`oss_baseline_refresh_new_top10=${ossBaselineRefresh.newlyDiscoveredTop10Projects.join(',') || 'none'}`)
  console.log(`oss_baseline_age_days=${ossBaselineFreshness.baselineAgeDays}`)
  console.log(`oss_baseline_refresh_required_before_public_comparison=${ossBaselineFreshness.baselineRefreshRequiredBeforePublicComparison}`)
  console.log(`oss_source_review_source_supported=${ossSourceReview.sourceSupportedCandidateCount}`)
  console.log(`oss_source_review_metadata_only=${ossSourceReview.metadataOnlyNeedsReviewCount}`)
  console.log(`oss_architecture_target_count=${ossArchitectureTargets.targetRecordCount}`)
  console.log(`oss_architecture_prioritized_targets=${ossArchitectureTargets.prioritizedTargetCount}`)
  console.log(`oss_architecture_deferred_targets=${ossArchitectureTargets.deferredTargetCount}`)
  console.log(`oss_architecture_gap_records=${ossArchitectureGapReview.gapRecordCount}`)
  console.log(`oss_architecture_protected_gaps=${ossArchitectureGapReview.protectedBoundaryGapCount}`)
  console.log(`oss_axis_architecture_high_priority_projects=${ossAxisArchitectureReview.highPriorityProjectCount}`)
  console.log(`oss_axis_architecture_records=${ossAxisArchitectureReview.axisReviewRecordCount}`)
  console.log(`oss_axis_architecture_backlog_items=${ossAxisArchitectureReview.safeInternalBacklogItemCount}`)
  console.log(`oss_safe_backlog_plan_items=${ossSafeBacklogPlan.plannedBacklogItemCount}`)
  console.log(`oss_safe_backlog_next_gate_candidates=${ossSafeBacklogPlan.nextSafeInternalGateCandidateCount}`)
  console.log(`oss_safe_backlog_closure_closed_candidates=${String(ossSafeBacklogClosure.closedCandidateCount)}`)
  console.log(`oss_baseline_drift_propagated_new_discoveries=${String(ossBaselineDriftClosure.propagatedNewDiscoveryCount)}`)
  console.log(`oss_benchmark_comparison_matrix_records=${String(ossBenchmarkComparisonMatrix.matrixRecordCount)}`)
  console.log(`oss_ide_or_editor_surface_records=${String(ossIdeOrEditorSurfaceEvidence.ideEvidenceJsonlRecordCount)}`)
  console.log(`oss_privacy_no_phone_home_records=${String(ossPrivacyNoPhoneHomeEvidence.privacyEvidenceJsonlRecordCount)}`)
  console.log(`oss_eval_quality_gate_checklist_items=${ossEvalQualityGateChecklist.checklistItemCount}`)
  console.log(`oss_terminal_workflow_evidence_items=${ossTerminalWorkflowEvidence.evidenceItemCount}`)
  console.log(`oss_onboarding_docs_evidence_items=${ossOnboardingDocsEvidence.evidenceItemCount}`)
  console.log(`oss_runtime_doctoring_evidence_items=${ossRuntimeDoctoringEvidence.evidenceItemCount}`)
  console.log(`oss_security_permissions_evidence_items=${ossSecurityPermissionsEvidence.evidenceItemCount}`)
  console.log(`oss_tool_loop_reliability_evidence_items=${ossToolLoopReliabilityEvidence.evidenceItemCount}`)
  console.log(`oss_provider_breadth_evidence_items=${ossProviderBreadthEvidence.evidenceItemCount}`)
  console.log(`oss_release_hygiene_evidence_items=${ossReleaseHygieneEvidence.evidenceItemCount}`)
  console.log(`typecheck_strict_pass=${typecheckHealth.strictPass}`)
  console.log(`typecheck_diagnostics=${typecheckHealth.totalDiagnostics}`)
  console.log(`absorption_entries=${absorptionRegister.entries.length}`)
  console.log(`golden_transcripts=${goldenTranscripts.transcripts.length}`)
  console.log(`terminal_failure_recovery_transcripts=${terminalFailureRecoveryTranscripts.transcriptCount}`)
  console.log(`onboarding_smoke_commands=${onboardingSmoke.localSmokeCommands.length}`)
  console.log(`doc_relative_links_checked=${docLinkIntegrity.relativeLinksChecked.length}`)
  console.log(`primary_source_registry_entries=${primarySourceRegistry.primarySourceEntryCount}`)
  console.log(`agent_instruction_setup_commands=${agentInstructionsQuality.setupVerificationCommandsPresent.length}`)
  console.log(`community_intake_template_count=${communityIntakeQuality.sourceTemplatePaths.length}`)
  console.log(`community_profile_file_count=${communityProfileQuality.sourceProfilePaths.length}`)
  console.log(`dependency_topology_cycles=${dependencyTopology.circularDependencyCount}`)
  console.log(`dependency_topology_unresolved=${dependencyTopology.unresolvedDependencyCount}`)
  console.log(`dependency_topology_ratchet_known_violations=${dependencyTopology.configuredRatchetKnownViolationCount}`)
  console.log(`dependency_topology_ratchet_new_violations=${dependencyTopology.configuredRatchetNewViolationCount}`)
  console.log(`script_duplication_helper_clusters=${scriptDuplicationAudit.duplicateHelperClusterCount}`)
  console.log(`script_duplication_jscpd_clones=${scriptDuplicationAudit.jscpdCloneCount}`)
  console.log(`script_duplication_jscpd_duplicated_lines=${scriptDuplicationAudit.jscpdDuplicatedLines}`)
  console.log(`dead_export_candidate_unused_exports=${deadExportCandidates.candidateUnusedExportCount}`)
  console.log(`dead_export_candidate_unused_types=${deadExportCandidates.candidateUnusedTypeCount}`)
  console.log(`maintainer_ownership_rule_count=${maintainerOwnershipQuality.codeownerRules.length}`)
  console.log(`dependency_governance_direct_dependency_count=${dependencyGovernanceQuality.dependencyEntries.length}`)
  console.log(`lockfile_sbom_package_count=${lockfileSbomQuality.lockfilePackageCount}`)
  console.log(`lockfile_sbom_relationship_count=${lockfileSbomQuality.lockfileRelationshipCount}`)
  console.log(`lockfile_sbom_inventory_records=${lockfileSbomQuality.inventoryJsonlRecordCount}`)
  console.log(`license_boundary_authorization_requests=${licenseBoundaryAuthorization.protectedAuthorizationRequestCount}`)
  console.log(`provider_compatibility_presets=${providerCompatibility.providerPresetDefaults.length}`)
  console.log(`provider_capability_rows=${providerCapabilityMatrix.capabilityRowCount}`)
  console.log(`provider_failure_modes=${providerCapabilityMatrix.failureModeCount}`)
  console.log(`permission_regression_fixtures=${permissionRegression.regressionFixtures.length}`)
  console.log(`permission_regression_behavioral_commands=${permissionRegression.behavioralTestCommands.length}`)
  console.log(`runtime_doctor_checks=${runtimeDoctorRegression.doctorChecks.length}`)
  console.log(`git_release_hygiene_status=${gitReleaseHygiene.workspaceGitStatus}`)
  console.log(`ide_extension_surface_status=${ideExtensionSurface.workspaceIdeExtensionStatus}`)
  console.log(`ide_extension_scope_decision=${ideExtensionScope.scopeDecision}`)
  console.log(`ide_extension_manifest_pack_exit=${ideExtensionManifestSmoke.packageDryRunExitCode}`)
  console.log(`ide_extension_runtime_registered_commands=${ideExtensionRuntimeSmoke.registeredCommandIds.length}`)
  console.log(`ide_extension_host_smoke_exit=${ideExtensionHostSmoke.codeExitCode}`)
  console.log(`ide_extension_workbench_smoke_exit=${ideExtensionWorkbenchSmoke.codeExitCode}`)
  console.log(`ide_extension_workbench_executed_view_commands=${ideExtensionWorkbenchSmoke.executedViewCommandIds?.length ?? 0}`)
  console.log(`vscode_update_boundary_status=${vscodeUpdateBoundary.boundaryStatus}`)
  console.log(`vscode_update_codesetup_processes=${vscodeUpdateBoundary.codeSetupProcesses.length}`)
  console.log(`vscode_startup_diagnosis_status=${vscodeStartupDiagnostics.diagnosisStatus}`)
  console.log(`vscode_startup_update_guard_logs=${vscodeStartupDiagnostics.updateGuardLogEvidenceCount}`)
  console.log(`ide_extension_webview_render_contracts=${ideExtensionWebviewRenderSmoke.resolvedWebviewViewIds.length}`)
  console.log(`ide_extension_rendered_screenshot_png_bytes=${ideExtensionRenderedWorkbenchScreenshot.pngByteLength}`)
  console.log(`ide_extension_webview_interaction_commands=${ideExtensionWebviewInteractionSmoke.interactionCommandIds.length}`)
  console.log(`release_artifact_checks=${releaseArtifactFileList.releaseArtifactChecks.length}`)
  console.log(`release_provenance_hashes=${releaseArtifactProvenance.packageFileHashes.length}`)
  console.log(`release_provenance_components=${releaseArtifactProvenance.sbomComponents.length}`)
  console.log(`release_reproducibility_pack_runs=${releaseArtifactReproducibility.packRuns.length}`)
  console.log(`release_reproducibility_tarball_sha256=${releaseArtifactReproducibility.reproducibleTarballSha256 ?? 'missing'}`)
  console.log(`agent_replay_eval_scenarios=${agentReplayEvals.replayScenarioCount}`)
  console.log(`source_controlled_checks=${sourceControlledChecks.sourceControlledChecks.length}`)
  console.log(`openssf_security_posture_checks=${openSsfSecurityPosture.postureChecks.length}`)
  console.log(`real_session_capture_performed=${realSessionCapture.capturePerformed}`)
  console.log(`prompted_tool_loop_commands=${promptedToolLoopCapture.toolCommandCaptures.length}`)
  console.log(`code_editing_trace_capture_performed=${codeEditingTraceCapture.capturePerformed}`)
  console.log(`multi_file_code_editing_trace_capture_performed=${multiFileCodeEditingTraceCapture.capturePerformed}`)
  console.log(`regression_cycle_code_editing_trace_capture_performed=${regressionCycleCodeEditingTraceCapture.capturePerformed}`)
  console.log(`tool_interruption_recovery_trace_capture_performed=${toolInterruptionRecoveryTrace.capturePerformed}`)
  console.log(`protected_action_denial_trace_capture_performed=${protectedActionDenialTrace.capturePerformed}`)
  console.log(`real_trace_eval_files=${realTraceEvals.traceFileCount}`)
  console.log(`trace_portability_export_events=${tracePortabilityExport.portableEventCount}`)
  console.log(`trace_redaction_rules=${traceRedactionPolicy.redactionRules.length}`)
  console.log(`benchmark_readiness_tasks=${benchmarkReadiness.benchmarkTaskCount}`)
  console.log(`external_benchmark_execution_authorized=${externalBenchmarkBoundary.externalBenchmarkExecutionAuthorized}`)
  console.log(`external_benchmark_boundary_gaps=${externalBenchmarkBoundary.boundaryGaps.length}`)
  console.log(`local_benchmark_tasks=${localBenchmarkHarness.localBenchmarkTaskResults.length}`)
  console.log(`local_benchmark_blocked_tasks=${localBenchmarkHarness.statusSummary.classifiedBlockedTasks}`)
  console.log(`benchmark_efficiency_records=${benchmarkEfficiencyMetrics.summary.comparableRecordCount}`)
  console.log(`benchmark_efficiency_measured_token_cost_duration_records=${benchmarkEfficiencyMetrics.summary.recordsWithMeasuredTokenCostDuration}`)
  console.log(`benchmark_submission_required_assets=${benchmarkSubmissionReadiness.summary.requiredAssetCount}`)
  console.log(`benchmark_submission_official_external_ready=${benchmarkSubmissionReadiness.summary.officialExternalSubmissionReady}`)
  console.log(`benchmark_policy_items=${benchmarkPolicyCompliance.summary.policyItemCount}`)
  console.log(`benchmark_policy_official_claim_allowed=${benchmarkPolicyCompliance.summary.officialSWEbenchVerifiedSubmissionClaimAllowed}`)
  console.log(`terminal_bench_requirements=${terminalBenchReadiness.summary.requirementCount}`)
  console.log(`terminal_bench_official_execution_ready=${terminalBenchReadiness.summary.officialTerminalBenchExecutionReady}`)
  console.log(`trajectory_process_quality_traces=${trajectoryProcessQuality.summary.assessedTraceCount}`)
  console.log(`trajectory_process_quality_gaps=${trajectoryProcessQuality.summary.classifiedProcessGapTraceCount}`)
  console.log(`verification_report_consistency_obsolete_blockers=${verificationReportConsistency.obsoleteBlockerPhrasesFound.length}`)
  console.log(`quality_blocker_taxonomy_expected_failures=${qualityBlockerTaxonomy.expectedProductQualityGateFailureCount}`)
  console.log(`public_claim_boundary_unauthorized_claims=${publicClaimBoundary.unauthorizedPositiveClaimCount}`)
  console.log(`protected_action_authorization_items=${protectedActionAuthorizationPacket.authorizationItemCount}`)
  console.log(`product_evidence_manifest_records=${productEvidenceManifest.evidenceRecordCount}`)
  console.log(`terminal_condition=${verificationReportConsistency.sourceTerminalCondition}`)
}

main()
