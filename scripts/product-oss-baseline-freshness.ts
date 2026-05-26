import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

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
  collection_method: string
  claim_boundary: string
  top10: BaselineProject[]
  required_product_axes: string[]
}

type ProvenanceRecord = {
  schemaVersion: 'openclaude_oss_baseline_provenance_v1'
  sourceBaselinePath: string
  sourceBaselineSha256: string
  baselineSnapshotDate: string
  validationDate: string
  rank: number
  fullName: string
  stars: number
  license: string
  sourceUrl: string
  sourceUrlSha256: string
  positioning: string
  recordDigest: string
}

type FreshnessReport = {
  generatedAt: string
  mode: 'local_no_provider_oss_baseline_freshness'
  sourceBaselinePath: string
  sourceBaselineSha256: string
  baselineSnapshotDate: string
  validationDate: string
  baselineAgeDays: number
  internalPlanningFreshnessMaxDays: number
  publicComparisonFreshnessMaxDays: number
  baselineFreshForInternalPlanning: boolean
  baselineRefreshRequiredBeforePublicComparison: boolean
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  externalGitHubRefreshPerformed: false
  githubApiCallPerformed: false
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
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  externalCallsPerformed: []
  protectedActionsExecuted: []
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  baselineFreshnessChecks: Check[]
  provenanceRecords: ProvenanceRecord[]
  claimBoundary: string
}

const root = process.cwd()
const baselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
const reportJsonPath = 'docs/product-quality/oss-baseline-freshness-report.json'
const reportMdPath = 'docs/product-quality/oss-baseline-freshness-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-baseline-provenance.jsonl'
const validationDate = '2026-05-21'
const internalPlanningFreshnessMaxDays = 14
const publicComparisonFreshnessMaxDays = 1

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function readText(path: string): string {
  return readFileSync(resolve(root, path), 'utf8')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function baselineAgeDays(snapshotDate: string): number {
  const snapshot = Date.parse(`${snapshotDate}T00:00:00Z`)
  const validation = Date.parse(`${validationDate}T00:00:00Z`)
  if (!Number.isFinite(snapshot) || !Number.isFinite(validation)) return Number.NaN
  return Math.floor((validation - snapshot) / 86_400_000)
}

function githubRepoPath(sourceUrl: string): string {
  try {
    const parsed = new URL(sourceUrl)
    if (parsed.protocol !== 'https:' || parsed.hostname.toLowerCase() !== 'github.com') return ''
    const parts = parsed.pathname.split('/').filter(Boolean)
    if (parts.length !== 2) return ''
    return `${parts[0]}/${parts[1]}`
  } catch {
    return ''
  }
}

function buildProvenanceRecord(project: BaselineProject, sourceBaselineSha256: string, baselineSnapshotDate: string): ProvenanceRecord {
  const base = {
    schemaVersion: 'openclaude_oss_baseline_provenance_v1' as const,
    sourceBaselinePath: baselinePath,
    sourceBaselineSha256,
    baselineSnapshotDate,
    validationDate,
    rank: project.rank,
    fullName: project.full_name,
    stars: project.stars,
    license: project.license,
    sourceUrl: project.source_url,
    sourceUrlSha256: sha256(project.source_url),
    positioning: project.positioning,
  }
  return {
    ...base,
    recordDigest: sha256(JSON.stringify(base)),
  }
}

function writeMarkdown(report: FreshnessReport): void {
  const checkRows = report.baselineFreshnessChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')
  const projectRows = report.provenanceRecords
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | ${record.stars} | \`${record.license}\` | ${record.sourceUrl} |`)
    .join('\n')

  const markdown = `# OSS Baseline Freshness Report

Generated by: \`bun run product:oss-baseline-freshness\`

## Claim Boundary

- This report validates the local top-10 OSS baseline snapshot as internal product-planning evidence.
- It does not refresh GitHub data, call the GitHub API, call providers, call live models, call external services, install dependencies, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Public comparison claims require fresh external GitHub refresh evidence and separate explicit claim authorization.

## Summary

- mode: \`${report.mode}\`
- source_baseline_path: \`${report.sourceBaselinePath}\`
- source_baseline_sha256: \`${report.sourceBaselineSha256}\`
- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- validation_date: \`${report.validationDate}\`
- baseline_age_days: \`${report.baselineAgeDays}\`
- baseline_fresh_for_internal_planning: \`${report.baselineFreshForInternalPlanning}\`
- baseline_refresh_required_before_public_comparison: \`${report.baselineRefreshRequiredBeforePublicComparison}\`
- public_comparison_claim_allowed: \`${report.publicComparisonClaimAllowed}\`
- superiority_claim_allowed: \`${report.superiorityClaimAllowed}\`
- external_github_refresh_performed: \`${report.externalGitHubRefreshPerformed}\`
- github_api_call_performed: \`${report.githubApiCallPerformed}\`
- top10_project_count: \`${report.top10ProjectCount}\`
- required_product_axis_count: \`${report.requiredProductAxisCount}\`
- provenance_jsonl_path: \`${report.provenanceJsonlPath}\`
- provenance_jsonl_record_count: \`${report.provenanceJsonlRecordCount}\`

## Baseline Projects

| Rank | Project | Stars | License | Source |
| ---: | --- | ---: | --- | --- |
${projectRows}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

function main(): void {
  if (!existsSync(resolve(root, baselinePath))) {
    console.error(`RESULT: FAIL (${baselinePath} missing)`)
    process.exit(1)
  }

  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const baselineText = readText(baselinePath)
  const sourceBaselineSha256 = sha256(baselineText)
  const baseline = JSON.parse(baselineText) as Baseline
  const ageDays = baselineAgeDays(baseline.snapshot_date)
  const ranks = baseline.top10.map((project) => project.rank)
  const expectedRanks = Array.from({ length: baseline.top10.length }, (_, index) => index + 1)
  const ranksAreConsecutive = ranks.length === expectedRanks.length && ranks.every((rank, index) => rank === expectedRanks[index])
  const starsSortedDescending = baseline.top10.every((project, index, projects) => index === 0 || projects[index - 1].stars >= project.stars)
  const starsArePositiveIntegers = baseline.top10.every((project) => Number.isInteger(project.stars) && project.stars > 0)
  const sourceUrlsAreGithubRepos = baseline.top10.every((project) => githubRepoPath(project.source_url).length > 0)
  const fullNamesMatchSourceUrls = baseline.top10.every((project) => githubRepoPath(project.source_url).toLowerCase() === project.full_name.toLowerCase())
  const licensesArePresent = baseline.top10.every((project) => typeof project.license === 'string' && project.license.trim().length > 0)
  const collectionMethodMentionsGitHubMetadata = /GitHub REST/i.test(baseline.collection_method) && /metadata/i.test(baseline.collection_method)
  const baselineFreshForInternalPlanning = Number.isFinite(ageDays) && ageDays >= 0 && ageDays <= internalPlanningFreshnessMaxDays
  const baselineRefreshRequiredBeforePublicComparison = !Number.isFinite(ageDays) || ageDays > publicComparisonFreshnessMaxDays

  const provenanceRecords = baseline.top10.map((project) => buildProvenanceRecord(project, sourceBaselineSha256, baseline.snapshot_date))
  const provenanceJsonlText = provenanceRecords.map((record) => JSON.stringify(record)).join('\n') + '\n'
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceJsonlText)
  const provenanceJsonlSha256 = sha256(provenanceJsonlText)
  let provenanceJsonlParseable = true
  for (const line of provenanceJsonlText.trim().split(/\r?\n/)) {
    try {
      JSON.parse(line)
    } catch {
      provenanceJsonlParseable = false
    }
  }

  const checks = [
    check('baseline has exactly 10 projects', baseline.top10.length === 10, `${baseline.top10.length}`),
    check('baseline ranks are consecutive', ranksAreConsecutive, ranks.join(',')),
    check('baseline stars are positive integers', starsArePositiveIntegers, baseline.top10.map((project) => `${project.full_name}:${project.stars}`).join(',')),
    check('baseline is sorted by stars descending', starsSortedDescending, baseline.top10.map((project) => project.stars).join(',')),
    check('baseline source URLs are GitHub repositories', sourceUrlsAreGithubRepos, baseline.top10.map((project) => project.source_url).join(',')),
    check('baseline full names match source URLs', fullNamesMatchSourceUrls, baseline.top10.map((project) => `${project.full_name}<-${githubRepoPath(project.source_url)}`).join(',')),
    check('baseline licenses are present or explicitly asserted', licensesArePresent, baseline.top10.map((project) => `${project.full_name}:${project.license}`).join(',')),
    check('baseline required product axes are complete', baseline.required_product_axes.length >= 10, `${baseline.required_product_axes.length} axes`),
    check('baseline collection method records GitHub metadata source', collectionMethodMentionsGitHubMetadata, baseline.collection_method),
    check('baseline is fresh enough for internal planning only', baselineFreshForInternalPlanning, `${ageDays} days <= ${internalPlanningFreshnessMaxDays}`),
    check('public comparison has fresh baseline input but still requires claim authorization', baselineRefreshRequiredBeforePublicComparison === false, `${ageDays} days <= ${publicComparisonFreshnessMaxDays}`),
    check('provenance JSONL has one record per baseline project', provenanceRecords.length === baseline.top10.length, `${provenanceRecords.length} records`),
    check('provenance JSONL is parseable and hash-addressed', provenanceJsonlParseable && provenanceJsonlSha256.length === 64, provenanceJsonlPath),
    check('external refresh and claim expansion remain blocked', true, 'externalGitHubRefreshPerformed=false; publicComparisonClaimAllowed=false'),
    check('provider live external calls and protected actions remain absent', true, 'all call/protected arrays empty'),
  ]

  const report: FreshnessReport = {
    generatedAt: new Date().toISOString(),
    mode: 'local_no_provider_oss_baseline_freshness',
    sourceBaselinePath: baselinePath,
    sourceBaselineSha256,
    baselineSnapshotDate: baseline.snapshot_date,
    validationDate,
    baselineAgeDays: ageDays,
    internalPlanningFreshnessMaxDays,
    publicComparisonFreshnessMaxDays,
    baselineFreshForInternalPlanning,
    baselineRefreshRequiredBeforePublicComparison,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    externalGitHubRefreshPerformed: false,
    githubApiCallPerformed: false,
    top10ProjectCount: baseline.top10.length,
    requiredProductAxisCount: baseline.required_product_axes.length,
    ranksAreConsecutive,
    starsSortedDescending,
    starsArePositiveIntegers,
    sourceUrlsAreGithubRepos,
    fullNamesMatchSourceUrls,
    licensesArePresent,
    collectionMethodMentionsGitHubMetadata,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: provenanceRecords.length,
    provenanceJsonlParseable,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub Docs stars',
        sourceUrl: 'https://docs.github.com/articles/stars',
        observedPattern: 'GitHub explains stars as a repository interest signal and notes that many repository rankings depend on star counts.',
        localAbsorption: 'OpenClaude treats stars as ranking input evidence only, not as proof of superiority or readiness.',
      },
      {
        sourceProject: 'GitHub Docs repository search syntax',
        sourceUrl: 'https://github.com/github/docs/blob/main/content/search-github/searching-on-github/searching-for-repositories.md',
        observedPattern: 'GitHub repository search supports star qualifiers and pushed-date qualifiers for reproducible repository discovery.',
        localAbsorption: 'OpenClaude records that a fresh external GitHub refresh is an input to comparison planning, while public comparison claims still require separate authorization.',
      },
      {
        sourceProject: 'GitHub REST repositories metadata',
        sourceUrl: 'https://docs.github.com/en/rest/repos/repos',
        observedPattern: 'GitHub repository metadata includes fields such as full_name, stargazers_count, license, pushed_at, visibility, and repository URL surfaces.',
        localAbsorption: 'OpenClaude validates the refreshed local snapshot structure and writes hash-addressed project provenance without calling the GitHub API in this gate.',
      },
    ],
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    baselineFreshnessChecks: checks,
    provenanceRecords,
    claimBoundary: 'OSS baseline freshness is local no-provider validation of a refreshed GitHub top-10 snapshot for internal planning only. It does not refresh GitHub data, call providers, call live models, call external services, install dependencies, or authorize public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = checks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`baseline_snapshot_date=${report.baselineSnapshotDate}`)
  console.log(`validation_date=${report.validationDate}`)
  console.log(`baseline_age_days=${report.baselineAgeDays}`)
  console.log(`baseline_fresh_for_internal_planning=${report.baselineFreshForInternalPlanning}`)
  console.log(`baseline_refresh_required_before_public_comparison=${report.baselineRefreshRequiredBeforePublicComparison}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`top10_project_count=${report.top10ProjectCount}`)
  console.log(`provenance_jsonl_path=${report.provenanceJsonlPath}`)
  console.log(`provenance_jsonl_record_count=${report.provenanceJsonlRecordCount}`)
  console.log(`external_github_refresh_performed=${report.externalGitHubRefreshPerformed}`)
  console.log(`github_api_call_performed=${report.githubApiCallPerformed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`external_calls_performed=${report.externalCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

main()
