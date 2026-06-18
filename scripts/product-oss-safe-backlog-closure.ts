import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type Candidate = {
  gateId: string
  axis: string
  sourceBacklogItemCount: number
  protectedActionRequiredForPlanning: boolean
}

type ClosureRecord = {
  gateId: string
  axis: string
  sourceBacklogItemCount: number
  packageScript: string
  reportJsonPath: string
  reportMdPath: string
  provenanceJsonlPath: string
  reportJsonSha256: string | null
  reportMdSha256: string | null
  provenanceJsonlSha256: string | null
  implementedEvidenceExists: boolean
  packageScriptExists: boolean
  noProviderBoundaryPreserved: boolean
  protectedActionsExecuted: boolean
  claimsBlocked: boolean
  closureStatus: 'closed_by_existing_internal_evidence_gate' | 'open_missing_internal_evidence_gate'
}

type ClosureReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_safe_backlog_closure'
  sourceSafeBacklogPlanReportPath: string
  sourceSafeBacklogPlanReportSha256: string
  sourceCandidateCount: number
  closureRecordCount: number
  closedCandidateCount: number
  openCandidateCount: number
  closureJsonlPath: string
  closureJsonlSha256: string
  closureJsonlRecordCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  superiorityClaimAllowed: false
  closureRecords: ClosureRecord[]
  closureChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const sourceSafeBacklogPlanReportPath = 'docs/product-quality/oss-safe-backlog-plan-report.json'
const reportJsonPath = 'docs/product-quality/oss-safe-backlog-closure-report.json'
const reportMdPath = 'docs/product-quality/oss-safe-backlog-closure-report.md'
const closureJsonlPath = 'reports/openclaude-oss-safe-backlog-closure.jsonl'

const gateEvidenceMap: Record<string, {
  packageScript: string
  reportJsonPath: string
  reportMdPath: string
  provenanceJsonlPath: string
}> = {
  openclaude_internal_eval_and_quality_gates_evidence_gate: {
    packageScript: 'product:oss-eval-quality-gate-checklist',
    reportJsonPath: 'docs/product-quality/oss-eval-quality-gate-checklist-report.json',
    reportMdPath: 'docs/product-quality/oss-eval-quality-gate-checklist-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-eval-quality-gate-checklist.jsonl',
  },
  openclaude_internal_onboarding_docs_evidence_gate: {
    packageScript: 'product:oss-onboarding-docs-evidence',
    reportJsonPath: 'docs/product-quality/oss-onboarding-docs-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-onboarding-docs-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-onboarding-docs-evidence.jsonl',
  },
  openclaude_internal_provider_breadth_evidence_gate: {
    packageScript: 'product:oss-provider-breadth-evidence',
    reportJsonPath: 'docs/product-quality/oss-provider-breadth-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-provider-breadth-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-provider-breadth-evidence.jsonl',
  },
  openclaude_internal_privacy_and_no_phone_home_evidence_gate: {
    packageScript: 'product:oss-privacy-no-phone-home-evidence',
    reportJsonPath: 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-privacy-no-phone-home-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-privacy-no-phone-home-evidence.jsonl',
  },
  openclaude_internal_release_hygiene_evidence_gate: {
    packageScript: 'product:oss-release-hygiene-evidence',
    reportJsonPath: 'docs/product-quality/oss-release-hygiene-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-release-hygiene-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-release-hygiene-evidence.jsonl',
  },
  openclaude_internal_runtime_doctoring_evidence_gate: {
    packageScript: 'product:oss-runtime-doctoring-evidence',
    reportJsonPath: 'docs/product-quality/oss-runtime-doctoring-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-runtime-doctoring-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-runtime-doctoring-evidence.jsonl',
  },
  openclaude_internal_security_and_permissions_evidence_gate: {
    packageScript: 'product:oss-security-permissions-evidence',
    reportJsonPath: 'docs/product-quality/oss-security-permissions-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-security-permissions-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-security-permissions-evidence.jsonl',
  },
  openclaude_internal_terminal_workflow_evidence_gate: {
    packageScript: 'product:oss-terminal-workflow-evidence',
    reportJsonPath: 'docs/product-quality/oss-terminal-workflow-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-terminal-workflow-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-terminal-workflow-evidence.jsonl',
  },
  openclaude_internal_tool_loop_reliability_evidence_gate: {
    packageScript: 'product:oss-tool-loop-reliability-evidence',
    reportJsonPath: 'docs/product-quality/oss-tool-loop-reliability-evidence-report.json',
    reportMdPath: 'docs/product-quality/oss-tool-loop-reliability-evidence-report.md',
    provenanceJsonlPath: 'reports/openclaude-oss-tool-loop-reliability-evidence.jsonl',
  },
}

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function readJson<T>(path: string): T {
  return JSON.parse(readText(path)) as T
}

function fileSha256(path: string): string | null {
  const absolutePath = resolve(root, path)
  return existsSync(absolutePath) ? sha256(readFileSync(absolutePath)) : null
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function arrayLength(report: Record<string, unknown>, key: string): number | null {
  const value = report[key]
  return Array.isArray(value) ? value.length : null
}

function bool(report: Record<string, unknown>, key: string): boolean | null {
  const value = report[key]
  return typeof value === 'boolean' ? value : null
}

function noProviderBoundaryPreserved(report: Record<string, unknown>): boolean {
  return (arrayLength(report, 'providerCallsPerformed') ?? 0) === 0 &&
    (arrayLength(report, 'liveModelCallsPerformed') ?? 0) === 0 &&
    (arrayLength(report, 'externalCallsPerformed') ?? 0) === 0
}

function protectedActionsExecuted(report: Record<string, unknown>): boolean {
  const protectedActions = arrayLength(report, 'protectedActionsExecuted')
  const protectedActionsPerformed = arrayLength(report, 'protectedActionsPerformed')
  return (protectedActions !== null && protectedActions > 0) ||
    (protectedActionsPerformed !== null && protectedActionsPerformed > 0)
}

function claimsBlocked(report: Record<string, unknown>): boolean {
  const claimKeys = [
    'releaseReadinessClaimAllowed',
    'productionReadinessClaimAllowed',
    'publicReadinessClaimAllowed',
    'externalValidationClaimAllowed',
    'autonomousReliabilityClaimAllowed',
    'superiorityClaimAllowed',
    'publicComparisonClaimAllowed',
  ]
  return claimKeys.every((key) => bool(report, key) !== true)
}

function closureRecord(candidate: Candidate, packageScripts: Record<string, string>): ClosureRecord {
  const mapped = gateEvidenceMap[candidate.gateId]
  if (!mapped) {
    return {
      gateId: candidate.gateId,
      axis: candidate.axis,
      sourceBacklogItemCount: candidate.sourceBacklogItemCount,
      packageScript: 'missing',
      reportJsonPath: 'missing',
      reportMdPath: 'missing',
      provenanceJsonlPath: 'missing',
      reportJsonSha256: null,
      reportMdSha256: null,
      provenanceJsonlSha256: null,
      implementedEvidenceExists: false,
      packageScriptExists: false,
      noProviderBoundaryPreserved: false,
      protectedActionsExecuted: false,
      claimsBlocked: false,
      closureStatus: 'open_missing_internal_evidence_gate',
    }
  }

  const reportExists = existsSync(resolve(root, mapped.reportJsonPath))
  const report = reportExists ? readJson<Record<string, unknown>>(mapped.reportJsonPath) : {}
  const implementedEvidenceExists = reportExists &&
    existsSync(resolve(root, mapped.reportMdPath)) &&
    existsSync(resolve(root, mapped.provenanceJsonlPath))
  const packageScriptExists = typeof packageScripts[mapped.packageScript] === 'string'
  const noProvider = reportExists && noProviderBoundaryPreserved(report)
  const protectedExecuted = reportExists && protectedActionsExecuted(report)
  const blockedClaims = reportExists && claimsBlocked(report)
  const closed = implementedEvidenceExists && packageScriptExists && noProvider && !protectedExecuted && blockedClaims

  return {
    gateId: candidate.gateId,
    axis: candidate.axis,
    sourceBacklogItemCount: candidate.sourceBacklogItemCount,
    packageScript: mapped.packageScript,
    reportJsonPath: mapped.reportJsonPath,
    reportMdPath: mapped.reportMdPath,
    provenanceJsonlPath: mapped.provenanceJsonlPath,
    reportJsonSha256: fileSha256(mapped.reportJsonPath),
    reportMdSha256: fileSha256(mapped.reportMdPath),
    provenanceJsonlSha256: fileSha256(mapped.provenanceJsonlPath),
    implementedEvidenceExists,
    packageScriptExists,
    noProviderBoundaryPreserved: noProvider,
    protectedActionsExecuted: protectedExecuted,
    claimsBlocked: blockedClaims,
    closureStatus: closed ? 'closed_by_existing_internal_evidence_gate' : 'open_missing_internal_evidence_gate',
  }
}

function writeMarkdown(report: ClosureReport): void {
  const recordRows = report.closureRecords
    .map((record) => `| \`${record.gateId}\` | \`${record.axis}\` | \`${record.packageScript}\` | \`${record.closureStatus}\` | \`${record.noProviderBoundaryPreserved}\` | \`${record.claimsBlocked}\` |`)
    .join('\n')
  const checkRows = report.closureChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Safe Backlog Closure Report

Generated by: \`bun run product:oss-safe-backlog-closure\`

## Claim Boundary

- This report reconciles planned safe internal OSS backlog candidates with already-created local no-provider evidence gates.
- It does not execute providers, live models, external services, dependency installs, protected actions, release actions, or public claims.
- It does not claim the underlying protected gaps are resolved; it only closes stale internal planning status where local evidence gates already exist.

## Summary

- source_candidate_count: \`${report.sourceCandidateCount}\`
- closure_record_count: \`${report.closureRecordCount}\`
- closed_candidate_count: \`${report.closedCandidateCount}\`
- open_candidate_count: \`${report.openCandidateCount}\`
- closure_jsonl_path: \`${report.closureJsonlPath}\`
- closure_jsonl_sha256: \`${report.closureJsonlSha256}\`

## Closure Records

| Gate | Axis | Package Script | Closure Status | No-Provider Boundary | Claims Blocked |
| --- | --- | --- | --- | --- | --- |
${recordRows}

## Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })

  const sourceSafeBacklogPlan = readJson<{ nextSafeInternalGateCandidates: Candidate[] }>(sourceSafeBacklogPlanReportPath)
  const packageJson = readJson<{ scripts: Record<string, string> }>('package.json')
  const closureRecords = sourceSafeBacklogPlan.nextSafeInternalGateCandidates.map((candidate) => closureRecord(candidate, packageJson.scripts))
  const closureJsonlText = closureRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, closureJsonlPath), closureJsonlText)
  const closureJsonlSha256 = sha256(closureJsonlText)
  const closedCandidateCount = closureRecords.filter((record) => record.closureStatus === 'closed_by_existing_internal_evidence_gate').length
  const openCandidateCount = closureRecords.length - closedCandidateCount

  const report: ClosureReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_safe_backlog_closure',
    sourceSafeBacklogPlanReportPath,
    sourceSafeBacklogPlanReportSha256: sha256(readFileSync(resolve(root, sourceSafeBacklogPlanReportPath))),
    sourceCandidateCount: sourceSafeBacklogPlan.nextSafeInternalGateCandidates.length,
    closureRecordCount: closureRecords.length,
    closedCandidateCount,
    openCandidateCount,
    closureJsonlPath,
    closureJsonlSha256,
    closureJsonlRecordCount: closureRecords.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    superiorityClaimAllowed: false,
    closureRecords,
    closureChecks: [],
    claimBoundary: 'OSS safe backlog closure is local no-provider reconciliation only. It closes stale internal planning status where evidence gates already exist and does not execute or authorize protected actions.',
  }

  report.closureChecks = [
    check('safe backlog plan candidates imported', report.sourceCandidateCount === closureRecords.length, `${report.sourceCandidateCount}/${closureRecords.length} candidates`),
    check('every candidate has a mapped evidence gate', closureRecords.every((record) => record.reportJsonPath !== 'missing'), `${closureRecords.length} records`),
    check('every mapped package script exists', closureRecords.every((record) => record.packageScriptExists), closureRecords.filter((record) => !record.packageScriptExists).map((record) => record.packageScript).join(',') || 'all present'),
    check('every mapped evidence gate has JSON MD and JSONL artifacts', closureRecords.every((record) => record.implementedEvidenceExists), closureRecords.filter((record) => !record.implementedEvidenceExists).map((record) => record.gateId).join(',') || 'all present'),
    check('every mapped evidence gate preserves no-provider boundary', closureRecords.every((record) => record.noProviderBoundaryPreserved), closureRecords.filter((record) => !record.noProviderBoundaryPreserved).map((record) => record.gateId).join(',') || 'all preserved'),
    check('no mapped evidence gate executed protected actions', closureRecords.every((record) => !record.protectedActionsExecuted), closureRecords.filter((record) => record.protectedActionsExecuted).map((record) => record.gateId).join(',') || 'none'),
    check('claims remain blocked across mapped evidence gates', closureRecords.every((record) => record.claimsBlocked), closureRecords.filter((record) => !record.claimsBlocked).map((record) => record.gateId).join(',') || 'all blocked'),
    check('all planned safe internal candidates are closed by evidence gates', openCandidateCount === 0 && closedCandidateCount === closureRecords.length, `${closedCandidateCount}/${closureRecords.length} closed`),
    check('closure JSONL has one record per candidate', report.closureJsonlRecordCount === closureRecords.length, `${report.closureJsonlRecordCount}/${closureRecords.length}`),
    check('provider live external and protected action arrays remain empty', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.externalCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0, 'all arrays empty'),
    check('readiness and superiority claims remain blocked', report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.publicReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.autonomousReliabilityClaimAllowed === false && report.superiorityClaimAllowed === false, 'all false'),
  ]

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of report.closureChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = report.closureChecks.filter((item) => !item.ok)
  console.log('')
  console.log(`RESULT: ${failed.length === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`source_candidate_count=${report.sourceCandidateCount}`)
  console.log(`closed_candidate_count=${report.closedCandidateCount}`)
  console.log(`open_candidate_count=${report.openCandidateCount}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (failed.length > 0) {
    process.exit(1)
  }
}

main()
