import { createHash } from 'node:crypto'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { spawnSync } from 'node:child_process'
import { check } from './quality-report-helpers'

type SourceInput = {
  sourceType: 'github_doc' | 'oss_tool' | 'standard' | 'paper' | 'patent'
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type HostedStatus = 'enabled' | 'disabled' | 'unavailable'

type BranchProtectionStatus = {
  status: 'enabled' | 'disabled' | 'unavailable'
  detail: string
}

type RulesetStatus = {
  status: 'present' | 'absent' | 'unavailable'
  count: number
  detail: string
}

type SecurityAndAnalysisStatus = {
  secretScanning: HostedStatus
  pushProtection: HostedStatus
  dependabotSecurityUpdates: HostedStatus
}

type VulnerabilityAlertStatus = {
  status: 'enabled' | 'disabled_or_unavailable' | 'unavailable'
  detail: string
}

type CodeScanningStatus = {
  status: 'available' | 'unavailable'
  openAlertCount: number
  byRuleSeverity: Record<string, number>
  bySecuritySeverity: Record<string, number>
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

type Discovery = {
  repositoryDiscovery: 'gh_repo_view' | 'git_remote' | 'unavailable'
  branchProtectionDiscovery: 'github_branch_protection_api' | 'unavailable'
  rulesetDiscovery: 'github_rulesets_api' | 'unavailable'
  securityAndAnalysisDiscovery: 'github_repository_api' | 'unavailable'
  vulnerabilityAlertDiscovery: 'github_vulnerability_alerts_api' | 'unavailable'
  codeScanningDiscovery: 'github_code_scanning_api' | 'unavailable'
  workflowRunDiscovery: 'gh_run_list' | 'unavailable'
}

type HostedTrustInput = {
  repository: string
  defaultBranch: string
  branchProtection: BranchProtectionStatus
  rulesets: RulesetStatus
  securityAndAnalysis: SecurityAndAnalysisStatus
  vulnerabilityAlerts: VulnerabilityAlertStatus
  codeScanning: CodeScanningStatus
  latestMainRuns: MainRun[]
  discovery: Discovery
}

type RiskCategory =
  | 'branch_protection_disabled'
  | 'branch_protection_unavailable'
  | 'rulesets_absent'
  | 'rulesets_unavailable'
  | 'secret_scanning_disabled'
  | 'secret_scanning_unavailable'
  | 'push_protection_disabled'
  | 'push_protection_unavailable'
  | 'dependabot_security_updates_disabled'
  | 'vulnerability_alerts_disabled_or_unavailable'
  | 'code_scanning_alert_backlog'
  | 'code_scanning_unavailable'
  | 'main_workflow_not_green'

type HostedTrustRisk = {
  category: RiskCategory
  severity: 'info' | 'medium' | 'high'
  detail: string
}

type EvidenceCheck = {
  label: string
  ok: boolean
  detail: string
}

type HostedTrustPostureReport = {
  generatedAt: string
  mode: 'github_hosted_trust_posture_readonly'
  repository: string
  defaultBranch: string
  status: 'hosted_trust_no_risks_detected' | 'hosted_trust_risks_detected'
  primarySourceInputs: SourceInput[]
  branchProtection: BranchProtectionStatus
  rulesets: RulesetStatus
  securityAndAnalysis: SecurityAndAnalysisStatus
  vulnerabilityAlerts: VulnerabilityAlertStatus
  codeScanning: CodeScanningStatus
  latestMainRuns: MainRun[]
  risks: HostedTrustRisk[]
  riskCount: number
  discovery: Discovery
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: string[]
  protectedActionsExecuted: []
  settingsMutationsPerformed: []
  publicSecurityPostureClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  evidenceChecks: EvidenceCheck[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/github-hosted-trust-posture-report.json'
const reportMdPath = 'docs/product-quality/github-hosted-trust-posture-report.md'
const reportJsonlPath = 'reports/openclaude-github-hosted-trust-posture.jsonl'

export function hostedTrustPostureMode(args = process.argv): 'check' | 'write' {
  return args.includes('--check') ? 'check' : 'write'
}

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function countBy(items: string[]): Record<string, number> {
  const counts: Record<string, number> = {}
  for (const item of items.filter(Boolean)) {
    counts[item] = (counts[item] ?? 0) + 1
  }
  return counts
}

function topCounts(counts: Record<string, number>, limit = 10): Array<{ ruleId: string; count: number }> {
  return Object.entries(counts)
    .map(([ruleId, count]) => ({ ruleId, count }))
    .sort((a, b) => b.count - a.count || a.ruleId.localeCompare(b.ruleId))
    .slice(0, limit)
}

function addRisk(risks: HostedTrustRisk[], category: RiskCategory, severity: HostedTrustRisk['severity'], detail: string): void {
  risks.push({ category, severity, detail })
}

function latestRunsByName(runs: MainRun[]): Map<string, MainRun> {
  const byName = new Map<string, MainRun>()
  for (const run of runs) {
    if (!byName.has(run.name)) byName.set(run.name, run)
  }
  return byName
}

const requiredMainWorkflowNames = ['PR Checks', 'Release Boundary', 'CodeQL', 'OpenSSF Scorecard'] as const

export function analyzeHostedTrustPosture(input: HostedTrustInput): HostedTrustPostureReport {
  const risks: HostedTrustRisk[] = []

  if (input.branchProtection.status === 'disabled') {
    addRisk(risks, 'branch_protection_disabled', 'high', input.branchProtection.detail)
  }
  if (input.branchProtection.status === 'unavailable') {
    addRisk(risks, 'branch_protection_unavailable', 'medium', input.branchProtection.detail)
  }
  if (input.rulesets.status === 'absent') {
    addRisk(risks, 'rulesets_absent', 'medium', input.rulesets.detail)
  }
  if (input.rulesets.status === 'unavailable') {
    addRisk(risks, 'rulesets_unavailable', 'medium', input.rulesets.detail)
  }
  if (input.securityAndAnalysis.secretScanning === 'disabled') {
    addRisk(risks, 'secret_scanning_disabled', 'high', 'GitHub secret scanning is disabled.')
  }
  if (input.securityAndAnalysis.secretScanning === 'unavailable') {
    addRisk(risks, 'secret_scanning_unavailable', 'medium', 'GitHub secret scanning status is unavailable.')
  }
  if (input.securityAndAnalysis.pushProtection === 'disabled') {
    addRisk(risks, 'push_protection_disabled', 'high', 'GitHub secret scanning push protection is disabled.')
  }
  if (input.securityAndAnalysis.pushProtection === 'unavailable') {
    addRisk(risks, 'push_protection_unavailable', 'medium', 'GitHub push protection status is unavailable.')
  }
  if (input.securityAndAnalysis.dependabotSecurityUpdates === 'disabled') {
    addRisk(risks, 'dependabot_security_updates_disabled', 'medium', 'Dependabot security updates are disabled.')
  }
  if (input.vulnerabilityAlerts.status !== 'enabled') {
    addRisk(risks, 'vulnerability_alerts_disabled_or_unavailable', 'high', input.vulnerabilityAlerts.detail)
  }
  if (input.codeScanning.status === 'unavailable') {
    addRisk(risks, 'code_scanning_unavailable', 'medium', input.codeScanning.detail ?? 'Code scanning alert inventory is unavailable.')
  }
  if (input.codeScanning.openAlertCount > 0) {
    addRisk(risks, 'code_scanning_alert_backlog', 'high', `${input.codeScanning.openAlertCount} open code scanning alerts.`)
  }

  const byRunName = latestRunsByName(input.latestMainRuns)
  for (const requiredName of requiredMainWorkflowNames) {
    const run = byRunName.get(requiredName)
    if (!run) {
      addRisk(risks, 'main_workflow_not_green', 'medium', `${requiredName} run was not found on ${input.defaultBranch}.`)
      continue
    }
    if (run.status !== 'completed' || run.conclusion !== 'success') {
      addRisk(risks, 'main_workflow_not_green', 'medium', `${requiredName} is ${run.status}/${run.conclusion ?? 'null'}: ${run.url}`)
    }
  }

  const primarySourceInputs: SourceInput[] = [
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Code Scanning REST API',
      sourceUrl: 'https://docs.github.com/rest/code-scanning',
      observedPattern: 'Hosted code scanning alerts are first-class repository security evidence and can be inventoried through the GitHub API.',
      localAbsorption: 'This report records open alert backlog counts without claiming the alerts are resolved.',
    },
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Secret Scanning REST API',
      sourceUrl: 'https://docs.github.com/en/rest/secret-scanning/secret-scanning',
      observedPattern: 'Secret scanning alert status is hosted evidence with repository permission boundaries.',
      localAbsorption: 'This report separates current-tree hygiene scans from hosted secret scanning and push-protection configuration.',
    },
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Push Protection',
      sourceUrl: 'https://docs.github.com/en/code-security/concepts/secret-security/push-protection',
      observedPattern: 'Push protection blocks supported hardcoded credentials before they reach the repository.',
      localAbsorption: 'Disabled push protection is recorded as a trust risk, not silently hidden behind local grep scans.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'OpenSSF Scorecard',
      sourceUrl: 'https://github.com/ossf/scorecard',
      observedPattern: 'Open-source security posture is stronger when branch protection, token permissions, SAST, dependency updates, and security policy are explicit checks.',
      localAbsorption: 'Hosted posture is split from local OpenSSF file evidence and tracked as a separate read-only report.',
    },
    {
      sourceType: 'standard',
      sourceProject: 'SLSA Source Requirements',
      sourceUrl: 'https://slsa.dev/spec/v1.2/source-requirements',
      observedPattern: 'Protected source branches and source provenance are separate requirements from local source files.',
      localAbsorption: 'Branch protection gaps block stronger supply-chain claims until hosted settings are verified.',
    },
    {
      sourceType: 'paper',
      sourceProject: 'OpenSSF Scorecard paper',
      sourceUrl: 'https://arxiv.org/pdf/2208.03412',
      observedPattern: 'Security-policy, code-review, maintained status, and token-permission checks are useful ecosystem-scale posture signals with limitations.',
      localAbsorption: 'This report records signals and limitations instead of reducing posture to a single score.',
    },
    {
      sourceType: 'patent',
      sourceProject: 'US11463478B2 DevSecOps remediation optimization',
      sourceUrl: 'https://patents.google.com/patent/US11463478B2/en',
      observedPattern: 'DevSecOps systems prioritize remediation across security findings rather than treating scan output as a finished state.',
      localAbsorption: 'Code scanning backlog is a remediation input and not a public security-readiness claim.',
    },
  ]

  const report: HostedTrustPostureReport = {
    generatedAt: new Date().toISOString(),
    mode: 'github_hosted_trust_posture_readonly',
    repository: input.repository,
    defaultBranch: input.defaultBranch,
    status: risks.length === 0 ? 'hosted_trust_no_risks_detected' : 'hosted_trust_risks_detected',
    primarySourceInputs,
    branchProtection: input.branchProtection,
    rulesets: input.rulesets,
    securityAndAnalysis: input.securityAndAnalysis,
    vulnerabilityAlerts: input.vulnerabilityAlerts,
    codeScanning: input.codeScanning,
    latestMainRuns: input.latestMainRuns,
    risks,
    riskCount: risks.length,
    discovery: input.discovery,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: Object.values(input.discovery),
    protectedActionsExecuted: [],
    settingsMutationsPerformed: [],
    publicSecurityPostureClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    evidenceChecks: [],
    claimBoundary: 'This hosted GitHub trust posture report is read-only evidence. It does not enable repository settings, resolve alerts, claim public security posture, release readiness, production readiness, external validation, or autonomous reliability.',
  }

  report.evidenceChecks = [
    check('hosted settings were read only', report.settingsMutationsPerformed.length === 0 && report.protectedActionsExecuted.length === 0, 'no settings mutation or protected action recorded'),
    check('primary sources include GitHub docs, OSS, standard, paper, and patent inputs', ['github_doc', 'oss_tool', 'standard', 'paper', 'patent'].every((sourceType) => report.primarySourceInputs.some((source) => source.sourceType === sourceType)), [...new Set(report.primarySourceInputs.map((source) => source.sourceType))].join(',')),
    check('code scanning alert inventory was classified', report.codeScanning.status === 'available' || report.codeScanning.status === 'unavailable', report.codeScanning.status),
    check('branch protection status was classified', report.branchProtection.status.length > 0, report.branchProtection.status),
    check('secret scanning status was classified', report.securityAndAnalysis.secretScanning.length > 0, report.securityAndAnalysis.secretScanning),
    check('OpenSSF Scorecard hosted workflow was included in main-run classification', byRunName.has('OpenSSF Scorecard'), byRunName.get('OpenSSF Scorecard')?.url ?? 'missing'),
    check('hosted trust risks do not unlock readiness claims', !report.publicSecurityPostureClaimAllowed && !report.releaseReadinessClaimAllowed && !report.productionReadinessClaimAllowed && !report.externalValidationClaimAllowed, 'all claim booleans false'),
  ]

  return report
}

export function buildHostedTrustPostureJsonl(report: HostedTrustPostureReport): string {
  const records = report.risks.length > 0
    ? report.risks.map((risk) => ({
      kind: 'github_hosted_trust_risk',
      repository: report.repository,
      ...risk,
    }))
    : [{
      kind: 'github_hosted_trust_posture_summary',
      repository: report.repository,
      status: report.status,
      riskCount: report.riskCount,
    }]
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

function run(command: string, args: string[]): { status: number | null; stdout: string; stderr: string } {
  const result = spawnSync(command, args, { cwd: root, encoding: 'utf8', shell: false })
  return { status: result.status, stdout: result.stdout ?? '', stderr: result.stderr ?? '' }
}

function runJson(command: string, args: string[]): unknown | null {
  const result = run(command, args)
  if (result.status !== 0 || !result.stdout.trim()) return null
  return JSON.parse(result.stdout)
}

function discoverRepository(): { repository: string; defaultBranch: string; discovery: Discovery['repositoryDiscovery'] } {
  const repo = runJson('gh', ['repo', 'view', '--json', 'nameWithOwner,defaultBranchRef']) as {
    nameWithOwner?: string
    defaultBranchRef?: { name?: string }
  } | null
  if (repo?.nameWithOwner) {
    return {
      repository: repo.nameWithOwner,
      defaultBranch: repo.defaultBranchRef?.name ?? 'main',
      discovery: 'gh_repo_view',
    }
  }

  const remote = run('git', ['remote', 'get-url', 'origin']).stdout.trim()
  const match = remote.match(/github\.com[:/]([^/]+)\/(.+?)(?:\.git)?$/i)
  if (match) {
    return {
      repository: `${match[1]}/${match[2].replace(/\.git$/i, '')}`,
      defaultBranch: 'main',
      discovery: 'git_remote',
    }
  }

  return { repository: 'unknown/unknown', defaultBranch: 'main', discovery: 'unavailable' }
}

function readRepositorySecurity(repository: string): {
  securityAndAnalysis: SecurityAndAnalysisStatus
  discovery: Discovery['securityAndAnalysisDiscovery']
} {
  const data = runJson('gh', ['api', `repos/${repository}`]) as {
    security_and_analysis?: Record<string, { status?: string }>
  } | null
  const security = data?.security_and_analysis
  if (!security) {
    return {
      securityAndAnalysis: {
        secretScanning: 'unavailable',
        pushProtection: 'unavailable',
        dependabotSecurityUpdates: 'unavailable',
      },
      discovery: 'unavailable',
    }
  }
  const statusOf = (key: string): HostedStatus => {
    const status = security[key]?.status
    if (status === 'enabled') return 'enabled'
    if (status === 'disabled') return 'disabled'
    return 'unavailable'
  }
  return {
    securityAndAnalysis: {
      secretScanning: statusOf('secret_scanning'),
      pushProtection: statusOf('secret_scanning_push_protection'),
      dependabotSecurityUpdates: statusOf('dependabot_security_updates'),
    },
    discovery: 'github_repository_api',
  }
}

function readBranchProtection(repository: string, defaultBranch: string): {
  branchProtection: BranchProtectionStatus
  discovery: Discovery['branchProtectionDiscovery']
} {
  const result = run('gh', ['api', `repos/${repository}/branches/${defaultBranch}/protection`])
  if (result.status === 0) {
    return { branchProtection: { status: 'enabled', detail: 'branch protection endpoint returned 200' }, discovery: 'github_branch_protection_api' }
  }
  const output = `${result.stderr}\n${result.stdout}`
  if (/404|Branch not protected|Not Found/i.test(output)) {
    return { branchProtection: { status: 'disabled', detail: 'branch protection endpoint returned not found' }, discovery: 'github_branch_protection_api' }
  }
  return { branchProtection: { status: 'unavailable', detail: output.trim().slice(0, 200) || 'branch protection endpoint unavailable' }, discovery: 'unavailable' }
}

function readRulesets(repository: string): {
  rulesets: RulesetStatus
  discovery: Discovery['rulesetDiscovery']
} {
  const data = runJson('gh', ['api', `repos/${repository}/rulesets`]) as unknown[] | null
  if (!Array.isArray(data)) {
    return { rulesets: { status: 'unavailable', count: 0, detail: 'rulesets endpoint unavailable' }, discovery: 'unavailable' }
  }
  return {
    rulesets: {
      status: data.length > 0 ? 'present' : 'absent',
      count: data.length,
      detail: `${data.length} repository rulesets returned`,
    },
    discovery: 'github_rulesets_api',
  }
}

function readVulnerabilityAlerts(repository: string): {
  vulnerabilityAlerts: VulnerabilityAlertStatus
  discovery: Discovery['vulnerabilityAlertDiscovery']
} {
  const result = run('gh', ['api', `repos/${repository}/vulnerability-alerts`])
  if (result.status === 0) {
    return { vulnerabilityAlerts: { status: 'enabled', detail: 'vulnerability alerts endpoint returned success' }, discovery: 'github_vulnerability_alerts_api' }
  }
  const output = `${result.stderr}\n${result.stdout}`.trim()
  if (/404|Not Found|disabled/i.test(output)) {
    return { vulnerabilityAlerts: { status: 'disabled_or_unavailable', detail: 'vulnerability alerts endpoint returned not found or disabled' }, discovery: 'github_vulnerability_alerts_api' }
  }
  return { vulnerabilityAlerts: { status: 'unavailable', detail: output.slice(0, 200) || 'vulnerability alerts endpoint unavailable' }, discovery: 'unavailable' }
}

function readCodeScanning(repository: string): {
  codeScanning: CodeScanningStatus
  discovery: Discovery['codeScanningDiscovery']
} {
  const result = run('gh', [
    'api',
    '--paginate',
    `repos/${repository}/code-scanning/alerts?state=open&per_page=100`,
    '--jq',
    '.[] | {ruleId:.rule.id, ruleSeverity:.rule.severity, securitySeverity:.rule.security_severity_level}',
  ])
  if (result.status !== 0) {
    return {
      codeScanning: {
        status: 'unavailable',
        openAlertCount: 0,
        byRuleSeverity: {},
        bySecuritySeverity: {},
        topRules: [],
        detail: (result.stderr || result.stdout).trim().slice(0, 200) || 'code scanning endpoint unavailable',
      },
      discovery: 'unavailable',
    }
  }
  const alerts = result.stdout
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line) as { ruleId?: string; ruleSeverity?: string; securitySeverity?: string })
  const byRule = countBy(alerts.map((alert) => alert.ruleId ?? 'unknown'))
  return {
    codeScanning: {
      status: 'available',
      openAlertCount: alerts.length,
      byRuleSeverity: countBy(alerts.map((alert) => alert.ruleSeverity ?? 'unknown')),
      bySecuritySeverity: countBy(alerts.map((alert) => alert.securitySeverity ?? 'unknown')),
      topRules: topCounts(byRule),
    },
    discovery: 'github_code_scanning_api',
  }
}

function readLatestMainRuns(repository: string, defaultBranch: string): {
  latestMainRuns: MainRun[]
  discovery: Discovery['workflowRunDiscovery']
} {
  const data = runJson('gh', [
    'run',
    'list',
    '--repo',
    repository,
    '--branch',
    defaultBranch,
    '--limit',
    '10',
    '--json',
    'name,status,conclusion,headSha,url',
  ]) as MainRun[] | null
  if (!Array.isArray(data)) {
    return { latestMainRuns: [], discovery: 'unavailable' }
  }
  return { latestMainRuns: data, discovery: 'gh_run_list' }
}

export function buildHostedTrustPostureMarkdown(report: HostedTrustPostureReport, jsonlSha256: string): string {
  const riskRows = report.risks
    .map((risk) => `| ${risk.category} | ${risk.severity} | ${risk.detail} |`)
    .join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')
  const runRows = report.latestMainRuns
    .slice(0, 10)
    .map((run) => `| ${run.name} | ${run.status} | ${run.conclusion ?? 'null'} | ${run.headSha} | ${run.url} |`)
    .join('\n')
  const topRuleRows = report.codeScanning.topRules
    .map((rule) => `| ${rule.ruleId} | ${rule.count} |`)
    .join('\n')
  const markdown = `# GitHub Hosted Trust Posture Report

Generated by: \`bun run product:github-hosted-trust-posture\`

## Claim Boundary

- This is a read-only hosted GitHub posture inventory.
- It does not enable repository settings, resolve alerts, publish, deploy, call providers, call live models, or perform protected actions.
- It does not claim public security posture, release readiness, production readiness, external validation, or autonomous reliability.

## Summary

- generated_at: \`${report.generatedAt}\`
- freshness_boundary: \`current at generated_at only\`
- repository: \`${report.repository}\`
- default_branch: \`${report.defaultBranch}\`
- status: \`${report.status}\`
- risk_count: \`${report.riskCount}\`
- branch_protection: \`${report.branchProtection.status}\`
- rulesets: \`${report.rulesets.status}\` / \`${report.rulesets.count}\`
- secret_scanning: \`${report.securityAndAnalysis.secretScanning}\`
- push_protection: \`${report.securityAndAnalysis.pushProtection}\`
- dependabot_security_updates: \`${report.securityAndAnalysis.dependabotSecurityUpdates}\`
- vulnerability_alerts: \`${report.vulnerabilityAlerts.status}\`
- code_scanning_open_alert_count: \`${report.codeScanning.openAlertCount}\`
- settings_mutations_performed: \`${report.settingsMutationsPerformed.length}\`
- protected_actions_executed: \`${report.protectedActionsExecuted.length}\`
- public_security_posture_claim_allowed: \`${report.publicSecurityPostureClaimAllowed}\`
- jsonl_sha256: \`${jsonlSha256}\`

## Risks

| Category | Severity | Detail |
| --- | --- | --- |
${riskRows || '| none | info | no hosted trust risks detected |'}

## Code Scanning Top Rules

| Rule | Open alerts |
| --- | ---: |
${topRuleRows || '| none | 0 |'}

## Latest Main Workflow Runs

| Workflow | Status | Conclusion | SHA | URL |
| --- | --- | --- | --- | --- |
${runRows || '| none | none | none | none | none |'}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`
  return markdown
}

function writeMarkdown(report: HostedTrustPostureReport, jsonlSha256: string): void {
  const markdown = buildHostedTrustPostureMarkdown(report, jsonlSha256)
  writeFileSync(resolve(root, reportMdPath), markdown)
}

function writeReports(report: HostedTrustPostureReport): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  const jsonl = buildHostedTrustPostureJsonl(report)
  const jsonlSha256 = sha256(jsonl)
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, reportJsonlPath), jsonl)
  writeMarkdown(report, jsonlSha256)
}

function main(): void {
  const mode = hostedTrustPostureMode()
  const repo = discoverRepository()
  const security = readRepositorySecurity(repo.repository)
  const branch = readBranchProtection(repo.repository, repo.defaultBranch)
  const rulesets = readRulesets(repo.repository)
  const vulnerabilityAlerts = readVulnerabilityAlerts(repo.repository)
  const codeScanning = readCodeScanning(repo.repository)
  const runs = readLatestMainRuns(repo.repository, repo.defaultBranch)

  const report = analyzeHostedTrustPosture({
    repository: repo.repository,
    defaultBranch: repo.defaultBranch,
    branchProtection: branch.branchProtection,
    rulesets: rulesets.rulesets,
    securityAndAnalysis: security.securityAndAnalysis,
    vulnerabilityAlerts: vulnerabilityAlerts.vulnerabilityAlerts,
    codeScanning: codeScanning.codeScanning,
    latestMainRuns: runs.latestMainRuns,
    discovery: {
      repositoryDiscovery: repo.discovery,
      branchProtectionDiscovery: branch.discovery,
      rulesetDiscovery: rulesets.discovery,
      securityAndAnalysisDiscovery: security.discovery,
      vulnerabilityAlertDiscovery: vulnerabilityAlerts.discovery,
      codeScanningDiscovery: codeScanning.discovery,
      workflowRunDiscovery: runs.discovery,
    },
  })

  if (mode === 'write') {
    writeReports(report)
  }

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log(`RESULT: ${report.status === 'hosted_trust_risks_detected' ? 'RISKS_RECORDED' : 'PASS'}`)
  console.log(`mode=${mode}`)
  console.log(`repository=${report.repository}`)
  console.log(`risk_count=${report.riskCount}`)
  console.log(`code_scanning_open_alert_count=${report.codeScanning.openAlertCount}`)

  const failed = report.evidenceChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
