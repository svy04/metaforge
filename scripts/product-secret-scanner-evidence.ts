import { spawnSync } from 'node:child_process'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { check, readText, sha256 } from './quality-report-helpers'

type SourceInput = {
  sourceType: 'github_doc' | 'oss_tool' | 'standard' | 'paper' | 'patent'
  sourceProject: string
  sourceUrl: string
  observedPattern: string
  localAbsorption: string
}

type ExternalScanner = {
  name: 'Gitleaks' | 'TruffleHog' | 'detect-secrets' | string
  command: string
  status: 'available' | 'unavailable'
  detail: string
}

type HostedSecretScanning = {
  secretScanning: 'enabled' | 'disabled' | 'unavailable'
  pushProtection: 'enabled' | 'disabled' | 'unavailable'
  sourceReportPath: string
}

type RemoteSurfaceAudit = {
  status: 'no_public_github_surface_findings_detected' | 'blocked_public_github_surface_findings' | 'unavailable'
  blockerCount: number
  sourceReportPath: string
}

type EvidenceCheck = {
  label: string
  ok: boolean
  detail: string
}

type SecretScannerFinding = {
  category:
    | 'external_scanner_unavailable'
    | 'hosted_secret_scanning_disabled'
    | 'hosted_secret_scanning_unavailable'
    | 'hosted_push_protection_disabled'
    | 'hosted_push_protection_unavailable'
    | 'remote_surface_blockers_present'
    | 'remote_surface_audit_unavailable'
  severity: 'info' | 'medium' | 'high'
  detail: string
}

export type SecretScannerEvidenceReport = {
  generatedAt: string
  mode: 'claim_bounded_secret_scanner_evidence'
  repository: string
  sourceCommit: string
  generatedFrom: string[]
  status: 'secret_scanner_evidence_recorded' | 'secret_scanner_evidence_gaps_recorded'
  primarySourceInputs: SourceInput[]
  externalScanners: ExternalScanner[]
  externalScannerUnavailableCount: number
  hostedSecretScanning: HostedSecretScanning
  remoteSurfaceAudit: RemoteSurfaceAudit
  findings: SecretScannerFinding[]
  findingCount: number
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  protectedActionsExecuted: []
  settingsMutationsPerformed: []
  fullHistorySecretCleanClaimAllowed: false
  hostedSecretScanningCleanClaimAllowed: false
  verifiedSecretCleanClaimAllowed: false
  publicSecurityPostureClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  evidenceChecks: EvidenceCheck[]
  claimBoundary: string
}

type HostedTrustReportLike = {
  repository?: string
  securityAndAnalysis?: {
    secretScanning?: HostedSecretScanning['secretScanning']
    pushProtection?: HostedSecretScanning['pushProtection']
  }
}

type RemoteSurfaceReportLike = {
  status?: RemoteSurfaceAudit['status']
  blockerCount?: number
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const hostedTrustPath = 'docs/product-quality/github-hosted-trust-posture-report.json'
const remoteSurfacePath = 'docs/product-quality/github-remote-surface-audit-report.json'
const reportJsonPath = 'docs/product-quality/secret-scanner-evidence-report.json'
const reportMdPath = 'docs/product-quality/secret-scanner-evidence-report.md'
const reportJsonlPath = 'reports/openclaude-secret-scanner-evidence.jsonl'

export function secretScannerEvidenceMode(args = process.argv): 'check' | 'write' {
  return args.includes('--check') ? 'check' : 'write'
}

function primarySourceInputs(): SourceInput[] {
  return [
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Secret Scanning',
      sourceUrl: 'https://docs.github.com/code-security/secret-scanning/about-secret-scanning',
      observedPattern: 'Hosted secret scanning covers supported patterns across repository content and GitHub surfaces, with alert status separate from local checks.',
      localAbsorption: 'This report records hosted secret-scanning status as a separate evidence layer instead of treating local grep as full-history proof.',
    },
    {
      sourceType: 'github_doc',
      sourceProject: 'GitHub Push Protection',
      sourceUrl: 'https://docs.github.com/en/code-security/concepts/secret-security/push-protection',
      observedPattern: 'Push protection blocks supported secrets before they are pushed and is a repository setting rather than a code-only gate.',
      localAbsorption: 'Disabled or unavailable push protection is tracked as a hosted gap, not silently hidden by local scanner output.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'Gitleaks',
      sourceUrl: 'https://github.com/gitleaks/gitleaks',
      observedPattern: 'Git secret scanning should produce redacted, rule-addressed findings over Git content and history.',
      localAbsorption: 'The gate detects whether Gitleaks is available and keeps full-history cleanliness claims blocked until a configured scan is actually run and reviewed.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'TruffleHog',
      sourceUrl: 'https://github.com/trufflesecurity/trufflehog',
      observedPattern: 'Verified-secret scanning can reduce noise but may depend on detector-specific verification behavior.',
      localAbsorption: 'TruffleHog availability is inventoried without claiming verified-secret cleanliness or making provider/service verification calls.',
    },
    {
      sourceType: 'oss_tool',
      sourceProject: 'detect-secrets',
      sourceUrl: 'https://github.com/Yelp/detect-secrets',
      observedPattern: 'Baseline-oriented scanning separates known findings from newly introduced candidates.',
      localAbsorption: 'The report treats detect-secrets as a future baseline option and does not normalize a baseline before review.',
    },
    {
      sourceType: 'standard',
      sourceProject: 'NIST SSDF',
      sourceUrl: 'https://csrc.nist.gov/projects/ssdf',
      observedPattern: 'Secure development practices require protecting source code and managing vulnerabilities through defined processes.',
      localAbsorption: 'Secret scanning is framed as one repeatable control in the public hygiene process, not a standalone security certification.',
    },
    {
      sourceType: 'paper',
      sourceProject: 'How Bad Can It Git? Characterizing Secret Leakage in Public GitHub Repositories',
      sourceUrl: 'https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/',
      observedPattern: 'Secret leakage in public repositories is a measurable historical and ecosystem problem, not just a current-tree text problem.',
      localAbsorption: 'The report keeps full-history and current-tree evidence separate.',
    },
    {
      sourceType: 'patent',
      sourceProject: 'US11463478B2 DevSecOps remediation optimization',
      sourceUrl: 'https://patents.google.com/patent/US11463478B2/en',
      observedPattern: 'Security findings can be aggregated and prioritized into remediation plans instead of being treated as isolated scan output.',
      localAbsorption: 'Scanner gaps become remediation evidence without claiming the gaps are already fixed.',
    },
  ]
}

function findingForHostedSecretScanning(status: HostedSecretScanning['secretScanning']): SecretScannerFinding | null {
  if (status === 'disabled') {
    return {
      category: 'hosted_secret_scanning_disabled',
      severity: 'high',
      detail: 'GitHub hosted secret scanning is reported disabled.',
    }
  }
  if (status === 'unavailable') {
    return {
      category: 'hosted_secret_scanning_unavailable',
      severity: 'medium',
      detail: 'GitHub hosted secret scanning status is unavailable.',
    }
  }
  return null
}

function findingForPushProtection(status: HostedSecretScanning['pushProtection']): SecretScannerFinding | null {
  if (status === 'disabled') {
    return {
      category: 'hosted_push_protection_disabled',
      severity: 'high',
      detail: 'GitHub secret scanning push protection is reported disabled.',
    }
  }
  if (status === 'unavailable') {
    return {
      category: 'hosted_push_protection_unavailable',
      severity: 'medium',
      detail: 'GitHub push protection status is unavailable.',
    }
  }
  return null
}

export function buildSecretScannerEvidenceReport({
  repository,
  sourceCommit,
  generatedFrom,
  externalScanners,
  hostedSecretScanning,
  remoteSurfaceAudit,
  generatedAt = new Date().toISOString(),
}: {
  repository: string
  sourceCommit: string
  generatedFrom: string[]
  externalScanners: ExternalScanner[]
  hostedSecretScanning: HostedSecretScanning
  remoteSurfaceAudit: RemoteSurfaceAudit
  generatedAt?: string
}): SecretScannerEvidenceReport {
  const findings: SecretScannerFinding[] = [
    ...externalScanners
      .filter((scanner) => scanner.status === 'unavailable')
      .map((scanner) => ({
        category: 'external_scanner_unavailable' as const,
        severity: 'info' as const,
        detail: `${scanner.name} (${scanner.command}) is unavailable: ${scanner.detail}`,
      })),
    ...[findingForHostedSecretScanning(hostedSecretScanning.secretScanning)].filter((item): item is SecretScannerFinding => item !== null),
    ...[findingForPushProtection(hostedSecretScanning.pushProtection)].filter((item): item is SecretScannerFinding => item !== null),
  ]

  if (remoteSurfaceAudit.status === 'blocked_public_github_surface_findings' || remoteSurfaceAudit.blockerCount > 0) {
    findings.push({
      category: 'remote_surface_blockers_present',
      severity: 'high',
      detail: `${remoteSurfaceAudit.blockerCount} GitHub remote-surface blockers are recorded.`,
    })
  }
  if (remoteSurfaceAudit.status === 'unavailable') {
    findings.push({
      category: 'remote_surface_audit_unavailable',
      severity: 'medium',
      detail: 'GitHub remote-surface audit report is unavailable.',
    })
  }

  const sourceTypes = new Set(primarySourceInputs().map((source) => source.sourceType))
  const report: SecretScannerEvidenceReport = {
    generatedAt,
    mode: 'claim_bounded_secret_scanner_evidence',
    repository,
    sourceCommit,
    generatedFrom,
    status: findings.length === 0
      ? 'secret_scanner_evidence_recorded'
      : 'secret_scanner_evidence_gaps_recorded',
    primarySourceInputs: primarySourceInputs(),
    externalScanners,
    externalScannerUnavailableCount: externalScanners.filter((scanner) => scanner.status === 'unavailable').length,
    hostedSecretScanning,
    remoteSurfaceAudit,
    findings,
    findingCount: findings.length,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    protectedActionsExecuted: [],
    settingsMutationsPerformed: [],
    fullHistorySecretCleanClaimAllowed: false,
    hostedSecretScanningCleanClaimAllowed: false,
    verifiedSecretCleanClaimAllowed: false,
    publicSecurityPostureClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    evidenceChecks: [],
    claimBoundary: 'Secret scanner evidence is a claim-bounded inventory of local scanner availability plus existing hosted and remote-surface reports. It does not claim full-history secret cleanliness, hosted secret-scanning alert cleanliness, verified-secret cleanliness, public security posture, release readiness, production readiness, or external validation.',
  }

  report.evidenceChecks = [
    check('external scanner availability is classified', externalScanners.length > 0 && externalScanners.every((scanner) => scanner.status === 'available' || scanner.status === 'unavailable'), `${externalScanners.length} scanners`),
    check('hosted secret scanning status is classified', ['enabled', 'disabled', 'unavailable'].includes(hostedSecretScanning.secretScanning), hostedSecretScanning.secretScanning),
    check('hosted push protection status is classified', ['enabled', 'disabled', 'unavailable'].includes(hostedSecretScanning.pushProtection), hostedSecretScanning.pushProtection),
    check('remote surface audit status is classified', ['no_public_github_surface_findings_detected', 'blocked_public_github_surface_findings', 'unavailable'].includes(remoteSurfaceAudit.status), remoteSurfaceAudit.status),
    check('primary sources cover GitHub docs, OSS, standard, paper, and patent inputs', ['github_doc', 'oss_tool', 'standard', 'paper', 'patent'].every((sourceType) => sourceTypes.has(sourceType as SourceInput['sourceType'])), [...sourceTypes].join(',')),
    check('no provider live model settings or protected action was performed', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0 && report.settingsMutationsPerformed.length === 0 && report.protectedActionsExecuted.length === 0, 'all mutation/call arrays empty'),
    check('secret-clean and readiness claims remain blocked', report.fullHistorySecretCleanClaimAllowed === false && report.hostedSecretScanningCleanClaimAllowed === false && report.verifiedSecretCleanClaimAllowed === false && report.publicSecurityPostureClaimAllowed === false && report.releaseReadinessClaimAllowed === false && report.productionReadinessClaimAllowed === false && report.externalValidationClaimAllowed === false, 'all claim flags false'),
  ]

  return report
}

export function buildSecretScannerEvidenceJsonl(report: SecretScannerEvidenceReport): string {
  const records = report.findings.length > 0
    ? report.findings.map((finding) => ({
      kind: 'secret_scanner_evidence_finding',
      repository: report.repository,
      sourceCommit: report.sourceCommit,
      ...finding,
    }))
    : [{
      kind: 'secret_scanner_evidence_summary',
      repository: report.repository,
      sourceCommit: report.sourceCommit,
      status: report.status,
      findingCount: report.findingCount,
    }]
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

export function buildSecretScannerEvidenceMarkdown(report: SecretScannerEvidenceReport, jsonlSha256: string): string {
  const scannerRows = report.externalScanners
    .map((scanner) => `| ${scanner.name} | \`${scanner.command}\` | \`${scanner.status}\` | ${scanner.detail} |`)
    .join('\n')
  const findingRows = report.findings.length === 0
    ? '| none | info | no claim-bounded scanner gaps recorded |'
    : report.findings.map((finding) => `| ${finding.category} | ${finding.severity} | ${finding.detail} |`).join('\n')
  const sourceRows = report.primarySourceInputs
    .map((source) => `| ${source.sourceType} | ${source.sourceProject} | ${source.sourceUrl} | ${source.localAbsorption} |`)
    .join('\n')
  const checkRows = report.evidenceChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  return `# Secret Scanner Evidence Report

Generated by: \`bun run product:secret-scanner-evidence\`

## Claim Boundary

- This report records secret-scanner availability and already-generated hosted/remote-surface evidence.
- It does not install external scanners, enable GitHub settings, verify live credentials, call providers, or mutate repository settings.
- It does not claim full-history secret cleanliness, hosted secret-scanning alert cleanliness, verified-secret cleanliness, public security posture, release readiness, production readiness, or external validation.

## Summary

- generated_at: \`${report.generatedAt}\`
- repository: \`${report.repository}\`
- source_commit: \`${report.sourceCommit}\`
- status: \`${report.status}\`
- finding_count: \`${report.findingCount}\`
- external_scanner_unavailable_count: \`${report.externalScannerUnavailableCount}\`
- hosted_secret_scanning: \`${report.hostedSecretScanning.secretScanning}\`
- hosted_push_protection: \`${report.hostedSecretScanning.pushProtection}\`
- remote_surface_status: \`${report.remoteSurfaceAudit.status}\`
- remote_surface_blocker_count: \`${report.remoteSurfaceAudit.blockerCount}\`
- full_history_secret_clean_claim_allowed: \`${report.fullHistorySecretCleanClaimAllowed}\`
- hosted_secret_scanning_clean_claim_allowed: \`${report.hostedSecretScanningCleanClaimAllowed}\`
- verified_secret_clean_claim_allowed: \`${report.verifiedSecretCleanClaimAllowed}\`
- public_security_posture_claim_allowed: \`${report.publicSecurityPostureClaimAllowed}\`
- jsonl_sha256: \`${jsonlSha256}\`

## External Scanner Availability

| Scanner | Command | Status | Detail |
| --- | --- | --- | --- |
${scannerRows}

## Findings

| Category | Severity | Detail |
| --- | --- | --- |
${findingRows}

## Primary Sources

| Type | Source | URL | Local Absorption |
| --- | --- | --- | --- |
${sourceRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`
}

function run(command: string, args: string[]): { status: number | null; stdout: string; stderr: string; error?: NodeJS.ErrnoException } {
  const result = spawnSync(command, args, {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })
  return {
    status: result.status,
    stdout: result.stdout ?? '',
    stderr: result.stderr ?? '',
    error: result.error as NodeJS.ErrnoException | undefined,
  }
}

function detectExternalScanner(name: ExternalScanner['name'], command: string, versionArgs: string[]): ExternalScanner {
  const result = run(command, versionArgs)
  if (result.status === 0) {
    return {
      name,
      command,
      status: 'available',
      detail: (result.stdout || result.stderr).trim().replace(/\s+/g, ' ').slice(0, 160) || 'version command succeeded',
    }
  }
  return {
    name,
    command,
    status: 'unavailable',
    detail: result.error?.code ?? (result.stderr || result.stdout || 'version command failed').trim().slice(0, 160),
  }
}

function readJson<T>(path: string): T | null {
  try {
    return JSON.parse(readText(path, root)) as T
  } catch {
    return null
  }
}

function readRepository(): string {
  const result = run('gh', ['repo', 'view', '--json', 'nameWithOwner', '--jq', '.nameWithOwner'])
  if (result.status === 0 && result.stdout.trim()) {
    return result.stdout.trim()
  }
  const remote = run('git', ['remote', 'get-url', 'origin']).stdout.trim()
  const match = remote.match(/github\.com[:/]([^/]+)\/(.+?)(?:\.git)?$/i)
  return match ? `${match[1]}/${match[2].replace(/\.git$/i, '')}` : 'unknown/unknown'
}

function readGitHead(): string {
  const result = run('git', ['rev-parse', 'HEAD'])
  return result.status === 0 ? result.stdout.trim() : 'unknown'
}

function readHostedSecretScanning(): HostedSecretScanning {
  const report = readJson<HostedTrustReportLike>(hostedTrustPath)
  return {
    secretScanning: report?.securityAndAnalysis?.secretScanning ?? 'unavailable',
    pushProtection: report?.securityAndAnalysis?.pushProtection ?? 'unavailable',
    sourceReportPath: hostedTrustPath,
  }
}

function readRemoteSurfaceAudit(): RemoteSurfaceAudit {
  const report = readJson<RemoteSurfaceReportLike>(remoteSurfacePath)
  return {
    status: report?.status ?? 'unavailable',
    blockerCount: report?.blockerCount ?? 0,
    sourceReportPath: remoteSurfacePath,
  }
}

function writeReports(report: SecretScannerEvidenceReport): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  const jsonl = buildSecretScannerEvidenceJsonl(report)
  const jsonlSha256 = sha256(jsonl)
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, reportJsonlPath), jsonl)
  writeFileSync(resolve(root, reportMdPath), buildSecretScannerEvidenceMarkdown(report, jsonlSha256))
}

function main(): void {
  const mode = secretScannerEvidenceMode()
  const externalScanners = [
    detectExternalScanner('Gitleaks', 'gitleaks', ['version']),
    detectExternalScanner('TruffleHog', 'trufflehog', ['--version']),
    detectExternalScanner('detect-secrets', 'detect-secrets', ['--version']),
  ]
  const report = buildSecretScannerEvidenceReport({
    repository: readRepository(),
    sourceCommit: readGitHead(),
    generatedFrom: [remoteSurfacePath, hostedTrustPath],
    externalScanners,
    hostedSecretScanning: readHostedSecretScanning(),
    remoteSurfaceAudit: readRemoteSurfaceAudit(),
  })
  if (mode === 'write') {
    writeReports(report)
  }

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  console.log(`RESULT: ${report.evidenceChecks.every((item) => item.ok) ? 'PASS' : 'FAIL'}`)
  console.log(`mode=${mode}`)
  console.log(`status=${report.status}`)
  console.log(`finding_count=${report.findingCount}`)
  console.log(`external_scanner_unavailable_count=${report.externalScannerUnavailableCount}`)
  console.log(`full_history_secret_clean_claim_allowed=${report.fullHistorySecretCleanClaimAllowed}`)
  console.log(`hosted_secret_scanning_clean_claim_allowed=${report.hostedSecretScanningCleanClaimAllowed}`)
  console.log(`verified_secret_clean_claim_allowed=${report.verifiedSecretCleanClaimAllowed}`)

  if (!report.evidenceChecks.every((item) => item.ok)) {
    process.exit(1)
  }
}

if (import.meta.main) {
  main()
}
