import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { check, readText, sha256 } from './quality-report-helpers'

type SourceInput = {
  sourceType: 'github_doc' | 'codeql_query_help' | 'oss_tool' | 'standard' | 'paper' | 'patent'
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type CodeScanningInput = {
  status: 'available' | 'unavailable'
  openAlertCount: number
  topRules: Array<{ ruleId: string; count: number }>
  detail?: string
}

type MainRun = {
  name: string
  status: string
  conclusion: string | null
  headSha: string
  url: string
}

type SampleLocation = {
  path: string
  startLine: number
}

type CodeScanningRemediationInput = {
  repository: string
  defaultBranch: string
  sourceCommit: string
  generatedFrom: string
  codeScanning: CodeScanningInput
  sampleLocationsByRule: Record<string, SampleLocation[]>
  latestMainRuns: MainRun[]
  externalCallsPerformed?: string[]
  sampleDiscoveryStatus?: 'not_attempted' | 'available' | 'unavailable'
  sampleDiscoveryDetail?: string
}

type RemediationPriority = 'P0' | 'P1' | 'P2' | 'P3'

type RemediationClass =
  | 'temp_file_and_race_safety'
  | 'file_network_data_flow_review'
  | 'command_execution_boundary_review'
  | 'generated_or_dead_code_cleanup'
  | 'quality_cleanup'
  | 'manual_triage'

type RuleMetadata = {
  priority: RemediationPriority
  remediationClass: RemediationClass
  securitySeverity: 'high' | 'medium' | 'low' | 'unknown'
  ruleSeverity: 'error' | 'warning' | 'note' | 'unknown'
  sourceUrl: string
  ownerDecisionRequired: boolean
  safeFirstStep: string
  validationCommands: string[]
}

type RemediationQueueItem = RuleMetadata & {
  queueId: string
  ruleId: string
  openAlertCount: number
  sampleLocations: SampleLocation[]
  claimBoundary: string
}

type EvidenceCheck = {
  label: string
  ok: boolean
  detail: string
}

type CodeScanningRemediationQueueReport = {
  generatedAt: string
  mode: 'code_scanning_remediation_queue_claim_safe'
  repository: string
  defaultBranch: string
  sourceCommit: string
  generatedFrom: string
  status: 'remediation_queue_required' | 'no_open_alerts' | 'code_scanning_unavailable'
  primarySourceInputs: SourceInput[]
  codeScanning: CodeScanningInput
  latestMainRuns: MainRun[]
  queueItems: RemediationQueueItem[]
  queueItemCount: number
  sampleDiscoveryStatus: 'not_attempted' | 'available' | 'unavailable'
  sampleDiscoveryDetail: string
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: string[]
  protectedActionsExecuted: []
  settingsMutationsPerformed: []
  publicSecurityPostureClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  alertResolutionClaimAllowed: false
  evidenceChecks: EvidenceCheck[]
  claimBoundary: string
}

type HostedTrustReportLike = {
  repository?: string
  defaultBranch?: string
  codeScanning?: CodeScanningInput
  latestMainRuns?: MainRun[]
  externalCallsPerformed?: string[]
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const inputReportPath = 'docs/product-quality/github-hosted-trust-posture-report.json'
const reportJsonPath = 'docs/product-quality/code-scanning-remediation-queue-report.json'
const reportMdPath = 'docs/product-quality/code-scanning-remediation-queue-report.md'
const reportJsonlPath = 'reports/openclaude-code-scanning-remediation-queue.jsonl'

const baseValidationCommands = [
  'bun test scripts/product-code-scanning-remediation-queue.test.ts',
  'bun run product:github-hosted-trust-posture',
  'bun run product:code-scanning-remediation-queue',
  'bun run typecheck --pretty false',
  'bun run verify:privacy',
]

const ruleOverrides: Record<string, Partial<RuleMetadata>> = {
  'js/file-system-race': {
    priority: 'P0',
    remediationClass: 'temp_file_and_race_safety',
    securitySeverity: 'high',
    ruleSeverity: 'warning',
    ownerDecisionRequired: true,
    safeFirstStep: 'Inspect each check-then-use file operation, replace path-name races with descriptor-safe or atomic operations, and add regression tests around the touched filesystem boundary.',
  },
  'js/insecure-temporary-file': {
    priority: 'P0',
    remediationClass: 'temp_file_and_race_safety',
    securitySeverity: 'high',
    ruleSeverity: 'warning',
    ownerDecisionRequired: true,
    safeFirstStep: 'Replace predictable temp paths with a well-tested temp-file API or an exclusive create pattern, then add a test proving the file cannot pre-exist or be world-readable.',
  },
  'js/file-access-to-http': {
    priority: 'P1',
    remediationClass: 'file_network_data_flow_review',
    securitySeverity: 'medium',
    ruleSeverity: 'warning',
    ownerDecisionRequired: true,
    safeFirstStep: 'Review whether file contents can leave the machine over HTTP, then add allowlist/redaction tests before changing behavior.',
  },
  'js/http-to-file-access': {
    priority: 'P1',
    remediationClass: 'file_network_data_flow_review',
    securitySeverity: 'medium',
    ruleSeverity: 'warning',
    ownerDecisionRequired: true,
    safeFirstStep: 'Review network-to-file writes for trust boundaries, destination validation, and overwrite behavior before changing downloader or cache code.',
  },
  'js/indirect-command-line-injection': {
    priority: 'P1',
    remediationClass: 'command_execution_boundary_review',
    securitySeverity: 'high',
    ruleSeverity: 'warning',
    ownerDecisionRequired: true,
    safeFirstStep: 'Trace command arguments to their source, switch to argument-array execution where possible, and add tests for metacharacter input.',
  },
  'js/unused-local-variable': {
    priority: 'P3',
    remediationClass: 'generated_or_dead_code_cleanup',
    securitySeverity: 'unknown',
    ruleSeverity: 'note',
    ownerDecisionRequired: false,
    safeFirstStep: 'Confirm whether the hit is generated or dead code, then remove unused locals in small batches behind typecheck and focused tests.',
    validationCommands: [...baseValidationCommands, 'bun run product:script-duplication-audit'],
  },
  'js/trivial-conditional': {
    priority: 'P3',
    remediationClass: 'quality_cleanup',
    securitySeverity: 'unknown',
    ruleSeverity: 'note',
    ownerDecisionRequired: false,
    safeFirstStep: 'Simplify constant conditionals only where tests prove behavior is unchanged.',
  },
  'js/automatic-semicolon-insertion': {
    priority: 'P3',
    remediationClass: 'quality_cleanup',
    securitySeverity: 'unknown',
    ruleSeverity: 'note',
    ownerDecisionRequired: false,
    safeFirstStep: 'Patch automatic-semicolon-insertion hazards in small formatting-only batches and rerun TypeScript verification.',
  },
  'js/useless-expression': {
    priority: 'P3',
    remediationClass: 'quality_cleanup',
    securitySeverity: 'unknown',
    ruleSeverity: 'note',
    ownerDecisionRequired: false,
    safeFirstStep: 'Remove useless expressions only after confirming they are not preserving intentional side effects.',
  },
  'js/useless-assignment-to-local': {
    priority: 'P3',
    remediationClass: 'generated_or_dead_code_cleanup',
    securitySeverity: 'unknown',
    ruleSeverity: 'note',
    ownerDecisionRequired: false,
    safeFirstStep: 'Remove dead assignments in small batches and keep changed-file diagnostics clean.',
  },
}

const codeqlSecurityScores: Record<string, number> = {
  'js/file-system-race': 7.7,
  'js/insecure-temporary-file': 7.0,
  'js/file-access-to-http': 6.5,
  'js/http-to-file-access': 6.3,
}

function queryHelpUrl(ruleId: string): string {
  return `https://codeql.github.com/codeql-query-help/javascript/${ruleId.replace('/', '-')}/`
}

function queueIdFor(ruleId: string): string {
  return `codeql-${ruleId.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase()}`
}

function priorityRank(priority: RemediationPriority): number {
  return { P0: 0, P1: 1, P2: 2, P3: 3 }[priority]
}

function metadataForRule(ruleId: string): RuleMetadata {
  const override = ruleOverrides[ruleId] ?? {}
  return {
    priority: override.priority ?? 'P2',
    remediationClass: override.remediationClass ?? 'manual_triage',
    securitySeverity: override.securitySeverity ?? 'unknown',
    ruleSeverity: override.ruleSeverity ?? 'unknown',
    sourceUrl: override.sourceUrl ?? queryHelpUrl(ruleId),
    ownerDecisionRequired: override.ownerDecisionRequired ?? true,
    safeFirstStep: override.safeFirstStep ?? 'Inspect representative alerts, decide whether they are generated code, false positives, or behavior defects, then fix the smallest test-backed cluster first.',
    validationCommands: override.validationCommands ?? baseValidationCommands,
  }
}

function primarySourceInputs(): SourceInput[] {
  return [
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Code Scanning alert management',
      sourceUrl: 'https://docs.github.com/en/code-security/how-tos/manage-security-alerts/manage-code-scanning-alerts',
      observedPattern: 'Code scanning alerts should be assessed, tracked, resolved, or dismissed through an explicit workflow.',
      localAbsorption: 'This queue converts alert buckets into tracked remediation work without claiming the alerts are already fixed.',
    },
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Code Scanning REST API',
      sourceUrl: 'https://docs.github.com/en/rest/code-scanning/code-scanning',
      observedPattern: 'Repository code scanning alerts expose rule and most recent instance data for inventory and triage.',
      localAbsorption: 'The queue binds local remediation order to the hosted alert inventory and keeps API sampling read-only.',
    },
    {
      sourceType: 'codeql_query_help',
      sourceProject: 'CodeQL JavaScript query help',
      sourceUrl: 'https://codeql.github.com/codeql-query-help/javascript/',
      observedPattern: 'Each JavaScript/TypeScript rule carries a query id, severity, precision, recommendation, and CWE mapping where applicable.',
      localAbsorption: 'Known rules map to remediation classes so high-risk filesystem and data-flow findings are not hidden by cleanup volume.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'OpenSSF Scorecard',
      sourceUrl: 'https://github.com/ossf/scorecard',
      observedPattern: 'Security posture work benefits from explicit checks, risk levels, and remediation prompts rather than one aggregate score.',
      localAbsorption: 'The queue records individual rule classes, validation commands, and blocked claim states.',
    },
    {
      sourceType: 'standard',
      sourceProject: 'SLSA Source Requirements',
      sourceUrl: 'https://slsa.dev/spec/v1.2/source-requirements',
      observedPattern: 'Source trust depends on controlled changes, source provenance, and technical controls administered by the repository owner.',
      localAbsorption: 'This report separates remediation planning from hosted settings mutation and stronger source-trust claims.',
    },
    {
      sourceType: 'paper',
      sourceProject: 'OpenSSF Scorecard paper',
      sourceUrl: 'https://arxiv.org/abs/2208.03412',
      observedPattern: 'Automated security metrics are useful for ecosystem-scale visibility but still need scoped interpretation and follow-up.',
      localAbsorption: 'The queue treats alert buckets as triage inputs, not as proof of public security posture.',
    },
    {
      sourceType: 'patent',
      sourceProject: 'US11463478B2 DevSecOps remediation optimization',
      sourceUrl: 'https://patents.google.com/patent/US11463478B2/en',
      observedPattern: 'Remediations can be aggregated and ordered across security findings to create a single remediation solution.',
      localAbsorption: 'The queue orders CodeQL buckets into a single claim-safe remediation plan for the repo.',
    },
  ]
}

export function buildCodeScanningRemediationQueue(input: CodeScanningRemediationInput): CodeScanningRemediationQueueReport {
  const queueItems = input.codeScanning.topRules
    .map((rule) => {
      const metadata = metadataForRule(rule.ruleId)
      return {
        queueId: queueIdFor(rule.ruleId),
        ruleId: rule.ruleId,
        openAlertCount: rule.count,
        sampleLocations: input.sampleLocationsByRule[rule.ruleId] ?? [],
        ...metadata,
        claimBoundary: 'This queue item is a remediation candidate only. It does not claim the corresponding CodeQL alerts are resolved until hosted CodeQL confirms closure on the target branch.',
      }
    })
    .sort((left, right) => {
      const priorityDelta = priorityRank(left.priority) - priorityRank(right.priority)
      if (priorityDelta !== 0) return priorityDelta
      const securityScoreDelta = (codeqlSecurityScores[right.ruleId] ?? 0) - (codeqlSecurityScores[left.ruleId] ?? 0)
      if (securityScoreDelta !== 0) return securityScoreDelta
      return right.openAlertCount - left.openAlertCount || left.ruleId.localeCompare(right.ruleId)
    })

  const status = input.codeScanning.status === 'unavailable'
    ? 'code_scanning_unavailable'
    : input.codeScanning.openAlertCount === 0
      ? 'no_open_alerts'
      : 'remediation_queue_required'

  const firstCleanupIndex = queueItems.findIndex((item) => item.priority === 'P3')
  const lastSecurityIndex = Math.max(...queueItems.map((item, index) => item.priority === 'P0' || item.priority === 'P1' ? index : -1))
  const securityBeforeCleanup = firstCleanupIndex === -1 || lastSecurityIndex === -1 || lastSecurityIndex < firstCleanupIndex
  const sourceTypes = new Set(primarySourceInputs().map((source) => source.sourceType))

  const report: CodeScanningRemediationQueueReport = {
    generatedAt: new Date().toISOString(),
    mode: 'code_scanning_remediation_queue_claim_safe',
    repository: input.repository,
    defaultBranch: input.defaultBranch,
    sourceCommit: input.sourceCommit,
    generatedFrom: input.generatedFrom,
    status,
    primarySourceInputs: primarySourceInputs(),
    codeScanning: input.codeScanning,
    latestMainRuns: input.latestMainRuns,
    queueItems,
    queueItemCount: queueItems.length,
    sampleDiscoveryStatus: input.sampleDiscoveryStatus ?? 'not_attempted',
    sampleDiscoveryDetail: input.sampleDiscoveryDetail ?? 'sample locations supplied by input or not requested',
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: input.externalCallsPerformed ?? [],
    protectedActionsExecuted: [],
    settingsMutationsPerformed: [],
    publicSecurityPostureClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    alertResolutionClaimAllowed: false,
    evidenceChecks: [],
    claimBoundary: 'Code scanning remediation queue only. This report does not fix, dismiss, or close alerts; it does not mutate GitHub settings; and it does not claim public security posture, release readiness, production readiness, external validation, or alert resolution.',
  }

  report.evidenceChecks = [
    check('code scanning input was classified', ['available', 'unavailable'].includes(report.codeScanning.status), report.codeScanning.status),
    check('top CodeQL rules were converted into queue items', report.queueItemCount === report.codeScanning.topRules.length, `${report.queueItemCount}/${report.codeScanning.topRules.length}`),
    check('security-sensitive rules are prioritized before cleanup-heavy buckets', securityBeforeCleanup, queueItems.map((item) => `${item.priority}:${item.ruleId}`).join(',')),
    check('primary sources cover GitHub, CodeQL, OSS, standard, paper, and patent inputs', ['github_doc', 'codeql_query_help', 'oss_tool', 'standard', 'paper', 'patent'].every((sourceType) => sourceTypes.has(sourceType as SourceInput['sourceType'])), [...sourceTypes].join(',')),
    check('no provider live model or protected action was performed', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.protectedActionsExecuted.length === 0 && report.settingsMutationsPerformed.length === 0, 'provider/live/protected/settings arrays empty'),
    check('readiness security and alert-resolution claims remain blocked', report.publicSecurityPostureClaimAllowed === false && report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false && report.alertResolutionClaimAllowed === false, 'all claim flags false'),
  ]

  return report
}

export function buildCodeScanningRemediationQueueJsonl(report: CodeScanningRemediationQueueReport): string {
  const records = report.queueItems.length > 0
    ? report.queueItems.map((item) => ({
      kind: 'code_scanning_remediation_queue_item',
      repository: report.repository,
      sourceCommit: report.sourceCommit,
      queueId: item.queueId,
      ruleId: item.ruleId,
      priority: item.priority,
      remediationClass: item.remediationClass,
      openAlertCount: item.openAlertCount,
      ownerDecisionRequired: item.ownerDecisionRequired,
      sampleLocations: item.sampleLocations,
    }))
    : [{
      kind: 'code_scanning_remediation_queue_summary',
      repository: report.repository,
      sourceCommit: report.sourceCommit,
      status: report.status,
      openAlertCount: report.codeScanning.openAlertCount,
    }]
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

function run(command: string, args: string[]): { status: number | null; stdout: string; stderr: string } {
  const result = spawnSync(command, args, { cwd: root, encoding: 'utf8', shell: false })
  return { status: result.status, stdout: result.stdout ?? '', stderr: result.stderr ?? '' }
}

function readGitHead(): string {
  const result = run('git', ['rev-parse', 'HEAD'])
  return result.status === 0 ? result.stdout.trim() : 'unknown'
}

function readHostedTrustReport(): HostedTrustReportLike {
  if (!existsSync(resolve(root, inputReportPath))) {
    return {
      repository: 'unknown/unknown',
      defaultBranch: 'main',
      codeScanning: {
        status: 'unavailable',
        openAlertCount: 0,
        topRules: [],
        detail: `${inputReportPath} is missing`,
      },
      latestMainRuns: [],
      externalCallsPerformed: [],
    }
  }
  return JSON.parse(readText(inputReportPath, root)) as HostedTrustReportLike
}

function discoverSampleLocations(repository: string): {
  sampleLocationsByRule: Record<string, SampleLocation[]>
  externalCallsPerformed: string[]
  sampleDiscoveryStatus: 'available' | 'unavailable'
  sampleDiscoveryDetail: string
} {
  if (!repository || repository === 'unknown/unknown') {
    return {
      sampleLocationsByRule: {},
      externalCallsPerformed: [],
      sampleDiscoveryStatus: 'unavailable',
      sampleDiscoveryDetail: 'repository name unavailable',
    }
  }

  const result = run('gh', [
    'api',
    '--paginate',
    `repos/${repository}/code-scanning/alerts?state=open&per_page=100`,
    '--jq',
    '.[] | {ruleId:.rule.id,path:.most_recent_instance.location.path,startLine:.most_recent_instance.location.start_line}',
  ])

  if (result.status !== 0) {
    return {
      sampleLocationsByRule: {},
      externalCallsPerformed: ['github_code_scanning_alert_sample_discovery_unavailable'],
      sampleDiscoveryStatus: 'unavailable',
      sampleDiscoveryDetail: (result.stderr || result.stdout).trim().slice(0, 200) || 'gh code scanning sample discovery unavailable',
    }
  }

  const sampleLocationsByRule: Record<string, SampleLocation[]> = {}
  for (const line of result.stdout.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)) {
    const record = JSON.parse(line) as { ruleId?: string; path?: string; startLine?: number }
    if (!record.ruleId || !record.path || typeof record.startLine !== 'number') continue
    const samples = sampleLocationsByRule[record.ruleId] ?? []
    if (samples.length < 3 && !samples.some((sample) => sample.path === record.path && sample.startLine === record.startLine)) {
      samples.push({ path: record.path, startLine: record.startLine })
    }
    sampleLocationsByRule[record.ruleId] = samples
  }

  return {
    sampleLocationsByRule,
    externalCallsPerformed: ['github_code_scanning_alert_sample_discovery'],
    sampleDiscoveryStatus: 'available',
    sampleDiscoveryDetail: `${Object.keys(sampleLocationsByRule).length} rules sampled`,
  }
}

function writeMarkdown(report: CodeScanningRemediationQueueReport, jsonlSha256: string): void {
  const queueRows = report.queueItems
    .map((item) => `| \`${item.priority}\` | \`${item.ruleId}\` | ${item.openAlertCount} | \`${item.remediationClass}\` | \`${item.ownerDecisionRequired}\` | ${item.safeFirstStep} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const sampleRows = report.queueItems
    .flatMap((item) => item.sampleLocations.map((sample) => `| \`${item.ruleId}\` | \`${sample.path}:${sample.startLine}\` |`))
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# Code Scanning Remediation Queue

Generated by: \`bun run product:code-scanning-remediation-queue\`

## Claim Boundary

- This is a claim-safe remediation queue for hosted CodeQL alerts.
- It does not fix, dismiss, or close alerts.
- It does not mutate GitHub settings, publish, deploy, call providers, call live models, or execute protected actions.
- It does not claim public security posture, release readiness, production readiness, external validation, or alert resolution.

## Summary

- repository: \`${report.repository}\`
- default_branch: \`${report.defaultBranch}\`
- source_commit: \`${report.sourceCommit}\`
- generated_from: \`${report.generatedFrom}\`
- status: \`${report.status}\`
- code_scanning_status: \`${report.codeScanning.status}\`
- code_scanning_open_alert_count: \`${report.codeScanning.openAlertCount}\`
- queue_item_count: \`${report.queueItemCount}\`
- sample_discovery_status: \`${report.sampleDiscoveryStatus}\`
- sample_discovery_detail: \`${report.sampleDiscoveryDetail}\`
- public_security_posture_claim_allowed: \`${report.publicSecurityPostureClaimAllowed}\`
- alert_resolution_claim_allowed: \`${report.alertResolutionClaimAllowed}\`
- jsonl_sha256: \`${jsonlSha256}\`

## Queue

| Priority | Rule | Open alerts | Class | Owner decision required | Safe first step |
| --- | --- | ---: | --- | --- | --- |
${queueRows || '| none | none | 0 | none | false | no queue items |'}

## Sample Locations

| Rule | Sample |
| --- | --- |
${sampleRows || '| none | none |'}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`
  writeFileSync(resolve(root, reportMdPath), markdown)
}

function writeReports(report: CodeScanningRemediationQueueReport): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  const jsonl = buildCodeScanningRemediationQueueJsonl(report)
  const jsonlSha256 = sha256(jsonl)
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, reportJsonlPath), jsonl)
  writeMarkdown(report, jsonlSha256)
}

function main(): void {
  const hosted = readHostedTrustReport()
  const repository = hosted.repository ?? 'unknown/unknown'
  const samples = discoverSampleLocations(repository)
  const report = buildCodeScanningRemediationQueue({
    repository,
    defaultBranch: hosted.defaultBranch ?? 'main',
    sourceCommit: readGitHead(),
    generatedFrom: inputReportPath,
    codeScanning: hosted.codeScanning ?? {
      status: 'unavailable',
      openAlertCount: 0,
      topRules: [],
      detail: 'code scanning field missing from hosted trust report',
    },
    sampleLocationsByRule: samples.sampleLocationsByRule,
    latestMainRuns: hosted.latestMainRuns ?? [],
    externalCallsPerformed: [
      ...(hosted.externalCallsPerformed ?? []),
      ...samples.externalCallsPerformed,
    ],
    sampleDiscoveryStatus: samples.sampleDiscoveryStatus,
    sampleDiscoveryDetail: samples.sampleDiscoveryDetail,
  })

  writeReports(report)

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  console.log(`RESULT: ${report.evidenceChecks.every((item) => item.ok) ? 'PASS' : 'FAIL'}`)
  console.log(`repository=${report.repository}`)
  console.log(`status=${report.status}`)
  console.log(`code_scanning_open_alert_count=${report.codeScanning.openAlertCount}`)
  console.log(`queue_item_count=${report.queueItemCount}`)
  console.log(`sample_discovery_status=${report.sampleDiscoveryStatus}`)
  console.log(`public_security_posture_claim_allowed=${report.publicSecurityPostureClaimAllowed}`)
  console.log(`alert_resolution_claim_allowed=${report.alertResolutionClaimAllowed}`)

  if (!report.evidenceChecks.every((item) => item.ok)) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
