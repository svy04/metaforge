import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

type Check = {
  label: string
  ok: boolean
  detail: string
}

type GitHubLicense = {
  spdx_id?: string | null
}

type GitHubRepo = {
  full_name: string
  html_url: string
  description: string | null
  stargazers_count: number
  forks_count: number
  open_issues_count: number
  pushed_at: string
  updated_at: string
  archived: boolean
  disabled: boolean
  fork: boolean
  visibility: string
  license: GitHubLicense | null
  topics?: string[]
}

type SearchResponse = {
  total_count: number
  incomplete_results: boolean
  items: GitHubRepo[]
}

type BaselineProject = {
  rank: number
  full_name: string
  stars: number
  license: string
  source_url: string
  positioning: string
  pushed_at: string
  forks: number
  open_issues: number
  discovered_from: string[]
  relevance_terms: string[]
}

type Baseline = {
  snapshot_date: string
  category: string
  collection_method: string
  claim_boundary: string
  top10: BaselineProject[]
  required_product_axes: string[]
}

type RefreshReport = {
  generatedAt: string
  mode: 'external_github_api_oss_baseline_refresh'
  snapshotDate: string
  outputBaselinePath: string
  outputBaselineSha256: string
  previousBaselinePath: string
  previousBaselineSha256: string | null
  provenanceJsonlPath: string
  provenanceJsonlSha256: string
  provenanceJsonlRecordCount: number
  searchQueryCount: number
  searchedRepositoryCount: number
  explicitSeedRepositoryCount: number
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
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  externalGitHubRefreshPerformed: true
  githubApiCallPerformed: true
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  protectedActionsExecuted: []
  externalCallsPerformed: Array<{
    kind: 'github_rest_search' | 'github_rest_repo'
    url: string
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  refreshChecks: Check[]
}

type CachedRefreshReport = Pick<
  RefreshReport,
  'snapshotDate' |
  'outputBaselinePath' |
  'top10ProjectCount' |
  'publicComparisonClaimAllowed' |
  'superiorityClaimAllowed' |
  'releaseReadinessClaimAllowed' |
  'productionReadinessClaimAllowed' |
  'publicReadinessClaimAllowed' |
  'externalValidationClaimAllowed' |
  'autonomousReliabilityClaimAllowed' |
  'providerCallsPerformed' |
  'liveModelCallsPerformed' |
  'protectedActionsExecuted' |
  'refreshChecks'
>

const root = process.cwd()
const snapshotDate = '2026-05-21'
const previousBaselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-17.json'
const outputBaselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
const reportJsonPath = 'docs/product-quality/oss-baseline-refresh-report.json'
const reportMdPath = 'docs/product-quality/oss-baseline-refresh-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-baseline-refresh-provenance.jsonl'
const userAgent = 'OpenClaudeProductQualityBaselineRefresh'
const githubToken = process.env.GITHUB_TOKEN || process.env.GH_TOKEN

const requiredProductAxes = [
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
]

const explicitSeedRepositories = [
  'ultraworkers/claw-code',
  'anomalyco/opencode',
  'anthropics/claude-code',
  'google-gemini/gemini-cli',
  'openai/codex',
  'OpenHands/OpenHands',
  'openinterpreter/open-interpreter',
  'cline/cline',
  'aaif-goose/goose',
  'Aider-AI/aider',
  'continuedev/continue',
]

const searchQueries = [
  '"coding agent" in:name,description,readme stars:>1000 fork:false archived:false',
  '"ai coding agent" in:name,description,readme stars:>1000 fork:false archived:false',
  '"agentic coding" in:name,description,readme stars:>1000 fork:false archived:false',
  '"terminal coding assistant" in:name,description,readme stars:>1000 fork:false archived:false',
  '"AI pair programming" in:name,description,readme stars:>1000 fork:false archived:false',
  '"autonomous coding agent" in:name,description,readme stars:>1000 fork:false archived:false',
]

const excludedRepositoryReasons = new Map<string, string>([
  ['sindresorhus/awesome', 'awesome-list, not an executable coding-agent product'],
  ['vinta/awesome-python', 'awesome-list, not an executable coding-agent product'],
  ['awesome-selfhosted/awesome-selfhosted', 'awesome-list, not an executable coding-agent product'],
  ['jaywcjlove/awesome-mac', 'awesome-list, not an executable coding-agent product'],
  ['punkpeye/awesome-mcp-servers', 'awesome-list, not an executable coding-agent product'],
  ['steven2358/awesome-generative-ai', 'awesome-list, not an executable coding-agent product'],
  ['kyrolabs/awesome-langchain', 'awesome-list, not an executable coding-agent product'],
  ['torvalds/linux', 'operating-system kernel, not an AI coding-agent product'],
  ['ollama/ollama', 'model runtime, not a coding-agent product by itself'],
  ['github/spec-kit', 'spec-driven development toolkit, not a coding-agent CLI or IDE product'],
  ['garrytan/gstack', 'Claude Code setup/workflow package, not a coding-agent runtime product by itself'],
  ['msitarzewski/agency-agents', 'general agency role pack, not a coding-agent CLI or IDE product'],
  ['obra/superpowers', 'workflow/skill package, not a coding-agent runtime product by itself'],
  ['anthropics/claude-quickstarts', 'quickstart examples, not a coding-agent product by itself'],
  ['Piebald-AI/claude-code-system-prompts', 'prompt archive, not a coding-agent product by itself'],
  ['VoltAgent/awesome-design-md', 'awesome-list, not an executable coding-agent product'],
  ['ComposioHQ/awesome-claude-skills', 'awesome-list, not an executable coding-agent product'],
])

function sha256(input: string | Buffer): string {
  return createHash('sha256').update(input).digest('hex')
}

function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}

function readTextIfExists(path: string): string | null {
  const absolute = resolve(root, path)
  if (!existsSync(absolute)) return null
  return readFileSync(absolute, 'utf8')
}

function githubHeaders(): Headers {
  const headers = new Headers({
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': userAgent,
  })
  if (githubToken) headers.set('Authorization', `Bearer ${githubToken}`)
  return headers
}

async function githubRateLimitRemaining(): Promise<{ remaining: number | null; reset: string | null; status: number | null }> {
  const response = await fetch('https://api.github.com/rate_limit', { headers: githubHeaders() })
  const reset = response.headers.get('x-ratelimit-reset')
  if (!response.ok) return { remaining: null, reset, status: response.status }
  const body = await response.json() as { resources?: { core?: { remaining?: number } } }
  const remaining = body.resources?.core?.remaining
  return { remaining: typeof remaining === 'number' ? remaining : null, reset, status: response.status }
}

function readJsonIfExists<T>(path: string): T | null {
  const text = readTextIfExists(path)
  if (!text) return null
  return JSON.parse(text) as T
}

function useCachedSameDayRefreshIfRateLimited(rateLimit: { remaining: number | null; reset: string | null; status: number | null }): boolean {
  if (githubToken || rateLimit.remaining !== 0) return false
  const baseline = readJsonIfExists<Baseline>(outputBaselinePath)
  const report = readJsonIfExists<CachedRefreshReport>(reportJsonPath)
  const provenanceText = readTextIfExists(provenanceJsonlPath)
  const cachedChecks = [
    check('cached same-day baseline exists', Boolean(baseline), outputBaselinePath),
    check('cached same-day refresh report exists', Boolean(report), reportJsonPath),
    check('cached same-day provenance exists', Boolean(provenanceText), provenanceJsonlPath),
    check('cached baseline snapshot date is current', baseline?.snapshot_date === snapshotDate, baseline?.snapshot_date ?? 'missing'),
    check('cached baseline has exactly 10 projects', baseline?.top10.length === 10, String(baseline?.top10.length ?? 0)),
    check('cached refresh report matches current baseline', report?.snapshotDate === snapshotDate && report?.outputBaselinePath === outputBaselinePath && report?.top10ProjectCount === baseline?.top10.length, `${report?.snapshotDate ?? 'missing'}/${report?.top10ProjectCount ?? 'missing'}`),
    check('cached refresh report keeps claim expansion blocked', report?.publicComparisonClaimAllowed === false && report?.superiorityClaimAllowed === false && report?.releaseReadinessClaimAllowed === false && report?.productionReadinessClaimAllowed === false && report?.publicReadinessClaimAllowed === false && report?.externalValidationClaimAllowed === false && report?.autonomousReliabilityClaimAllowed === false, 'all claim flags false'),
    check('cached refresh report performed no provider live or protected calls', (report?.providerCallsPerformed.length ?? -1) === 0 && (report?.liveModelCallsPerformed.length ?? -1) === 0 && (report?.protectedActionsExecuted.length ?? -1) === 0, 'provider/live/protected counts zero'),
    check('cached refresh report prior checks pass', Boolean(report?.refreshChecks.every((item) => item.ok)), 'refreshChecks ok'),
  ]
  for (const item of cachedChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  const failed = cachedChecks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed cached refresh checks)`)
    process.exit(1)
  }
  console.log('RESULT: PASS')
  console.log('cached_same_day_refresh_used=true')
  console.log(`github_rate_limit_remaining=${rateLimit.remaining}`)
  console.log(`github_rate_limit_reset=${rateLimit.reset ?? 'unknown'}`)
  console.log(`snapshot_date=${snapshotDate}`)
  console.log(`output_baseline_path=${outputBaselinePath}`)
  console.log(`top10_project_count=${baseline?.top10.length ?? 0}`)
  console.log(`public_comparison_claim_allowed=${report?.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report?.superiorityClaimAllowed}`)
  console.log('provider_calls_performed=0')
  console.log('live_model_calls_performed=0')
  console.log('protected_actions_executed=0')
  return true
}

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url, { headers: githubHeaders() })
  if (!response.ok) {
    const body = await response.text()
    throw new Error(`GitHub request failed ${response.status} ${response.statusText}: ${url}: ${body.slice(0, 300)}`)
  }
  return await response.json() as T
}

function repoApiUrl(fullName: string): string {
  return `https://api.github.com/repos/${fullName}`
}

function searchApiUrl(query: string): string {
  const params = new URLSearchParams({
    q: query,
    sort: 'stars',
    order: 'desc',
    per_page: '10',
  })
  return `https://api.github.com/search/repositories?${params.toString()}`
}

function licenseSpdx(repo: GitHubRepo): string {
  const spdx = repo.license?.spdx_id
  return typeof spdx === 'string' && spdx.trim().length > 0 ? spdx : 'NOASSERTION'
}

function relevanceTerms(repo: GitHubRepo): string[] {
  const haystack = `${repo.full_name} ${repo.description ?? ''} ${(repo.topics ?? []).join(' ')}`.toLowerCase()
  const terms = [
    ['coding-agent', /coding agent|agentic coding|autonomous coding agent/],
    ['terminal', /terminal|cli|command-line/],
    ['ide', /\bide\b|vs code|vscode|jetbrains|extension/],
    ['code-editing', /code suggestions|codebase|pair programming|coding assistant|developer-tools/],
    ['tool-execution', /execute|edit|test|tool|mcp|agent/],
    ['codex-compatible', /codex|claude code|gemini-cli|opencode|aider|openhands|goose|cline|continue/],
  ] as const
  return terms.filter(([, pattern]) => pattern.test(haystack)).map(([term]) => term)
}

function positioning(repo: GitHubRepo): string {
  const description = repo.description?.trim()
  if (description) return description
  return 'AI coding-agent, terminal, IDE, or agentic development project discovered from GitHub repository metadata.'
}

function isEligible(repo: GitHubRepo): { ok: boolean; reason: string; terms: string[] } {
  const explicitExclusion = excludedRepositoryReasons.get(repo.full_name)
  if (explicitExclusion) return { ok: false, reason: explicitExclusion, terms: [] }
  if (/\/awesome[-_]/i.test(repo.full_name) || /^awesome[-_]/i.test(repo.full_name.split('/')[1] ?? '')) {
    return { ok: false, reason: 'awesome-list, not an executable coding-agent product', terms: [] }
  }
  if (repo.archived) return { ok: false, reason: 'archived repository', terms: [] }
  if (repo.disabled) return { ok: false, reason: 'disabled repository', terms: [] }
  if (repo.fork) return { ok: false, reason: 'fork repository', terms: [] }
  if (repo.visibility !== 'public') return { ok: false, reason: `visibility=${repo.visibility}`, terms: [] }
  const terms = relevanceTerms(repo)
  if (explicitSeedRepositories.map((item) => item.toLowerCase()).includes(repo.full_name.toLowerCase())) {
    return { ok: true, reason: 'explicit related-project seed', terms: terms.length > 0 ? terms : ['explicit-related-project-seed'] }
  }
  if (terms.length >= 2) return { ok: true, reason: `matched relevance terms: ${terms.join(',')}`, terms }
  return { ok: false, reason: `insufficient coding-agent relevance terms: ${terms.join(',') || 'none'}`, terms }
}

function writeMarkdown(report: RefreshReport, baseline: Baseline): void {
  const projectRows = baseline.top10
    .map((project) => `| ${project.rank} | \`${project.full_name}\` | ${project.stars} | \`${project.license}\` | ${project.pushed_at} | ${project.source_url} |`)
    .join('\n')
  const changeRows = [
    ...report.newlyDiscoveredTop10Projects.map((project) => `| entered_top10 | \`${project}\` | Fresh GitHub metadata placed this related project in the top-10 baseline. |`),
    ...report.removedPreviousTop10Projects.map((project) => `| left_top10 | \`${project}\` | Fresh GitHub metadata and newly eligible candidates moved this project outside the top 10. |`),
  ].join('\n') || '| none | `none` | No top-10 membership change. |'
  const excludedRows = report.discoveredHigherStarCandidatesExcluded
    .map((item) => `| \`${item.fullName}\` | ${item.stars} | ${item.reason} |`)
    .join('\n') || '| `none` | 0 | No higher-star discovered candidates were excluded. |'
  const checkRows = report.refreshChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Baseline Refresh Report

Generated by: \`bun run product:oss-baseline-refresh\`

## Claim Boundary

- This report refreshes GitHub repository metadata for internal benchmark planning.
- It uses GitHub REST API metadata and does not call providers, live models, package managers, deployment services, production OpenClaude, MFH, or real product repos.
- It does not authorize public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability claims.

## Summary

- mode: \`${report.mode}\`
- snapshot_date: \`${report.snapshotDate}\`
- output_baseline_path: \`${report.outputBaselinePath}\`
- external_github_refresh_performed: \`${report.externalGitHubRefreshPerformed}\`
- github_api_call_performed: \`${report.githubApiCallPerformed}\`
- search_query_count: \`${report.searchQueryCount}\`
- unique_candidate_count: \`${report.uniqueCandidateCount}\`
- eligible_candidate_count: \`${report.eligibleCandidateCount}\`
- top10_project_count: \`${report.top10ProjectCount}\`
- public_comparison_claim_allowed: \`${report.publicComparisonClaimAllowed}\`
- superiority_claim_allowed: \`${report.superiorityClaimAllowed}\`

## Fresh Top 10

| Rank | Project | Stars | License | Pushed At | Source |
| ---: | --- | ---: | --- | --- | --- |
${projectRows}

## Top-10 Changes

| Change | Project | Note |
| --- | --- | --- |
${changeRows}

## Higher-Star Candidates Excluded

| Project | Stars | Reason |
| --- | ---: | --- |
${excludedRows}

## Self-Improvement Actions

${report.selfImprovementActions.map((item) => `- ${item}`).join('\n')}

## Checks

| Check | Result | Detail |
| --- | --- | --- |
${checkRows}
`

  writeFileSync(resolve(root, reportMdPath), markdown)
}

async function main(): Promise<void> {
  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const rateLimit = await githubRateLimitRemaining()
  if (useCachedSameDayRefreshIfRateLimited(rateLimit)) return

  const previousBaselineText = readTextIfExists(previousBaselinePath)
  const previousBaseline = previousBaselineText ? JSON.parse(previousBaselineText) as { top10: Array<{ full_name: string }> } : { top10: [] }
  const previousTop10 = new Set(previousBaseline.top10.map((project) => project.full_name.toLowerCase()))
  const previousBaselineSha256 = previousBaselineText ? sha256(previousBaselineText) : null

  const externalCallsPerformed: RefreshReport['externalCallsPerformed'] = []
  const candidateSources = new Map<string, Set<string>>()
  const candidateRepos = new Map<string, GitHubRepo>()
  const excludedCandidates: Array<{ fullName: string; stars: number; reason: string }> = []

  for (const query of searchQueries) {
    const url = searchApiUrl(query)
    externalCallsPerformed.push({ kind: 'github_rest_search', url })
    const result = await fetchJson<SearchResponse>(url)
    for (const item of result.items) {
      const key = item.full_name.toLowerCase()
      const sources = candidateSources.get(key) ?? new Set<string>()
      sources.add(`search:${query}`)
      candidateSources.set(key, sources)
      candidateRepos.set(key, item)
    }
  }

  for (const fullName of explicitSeedRepositories) {
    const url = repoApiUrl(fullName)
    externalCallsPerformed.push({ kind: 'github_rest_repo', url })
    const repo = await fetchJson<GitHubRepo>(url)
    const key = repo.full_name.toLowerCase()
    const sources = candidateSources.get(key) ?? new Set<string>()
    sources.add('explicit-seed')
    candidateSources.set(key, sources)
    candidateRepos.set(key, repo)
  }

  const eligible = Array.from(candidateRepos.values())
    .map((repo) => ({ repo, eligibility: isEligible(repo) }))
    .filter(({ repo, eligibility }) => {
      if (!eligibility.ok) {
        excludedCandidates.push({ fullName: repo.full_name, stars: repo.stargazers_count, reason: eligibility.reason })
      }
      return eligibility.ok
    })
    .sort((left, right) => right.repo.stargazers_count - left.repo.stargazers_count)

  const top10 = eligible.slice(0, 10).map(({ repo, eligibility }, index): BaselineProject => ({
    rank: index + 1,
    full_name: repo.full_name,
    stars: repo.stargazers_count,
    license: licenseSpdx(repo),
    source_url: repo.html_url,
    positioning: positioning(repo),
    pushed_at: repo.pushed_at,
    forks: repo.forks_count,
    open_issues: repo.open_issues_count,
    discovered_from: Array.from(candidateSources.get(repo.full_name.toLowerCase()) ?? []).sort(),
    relevance_terms: eligibility.terms,
  }))

  const baseline: Baseline = {
    snapshot_date: snapshotDate,
    category: 'AI coding agent / terminal coding assistant / agentic coding CLI or IDE',
    collection_method: 'Fresh GitHub REST Search API and Repository API metadata collected in this run; sorted by stargazers_count among repositories passing bounded coding-agent relevance filters.',
    claim_boundary: 'This refreshed baseline is an internal benchmark-planning reference, not a claim that OpenClaude is superior, release-ready, production-ready, externally validated, or publicly ready.',
    top10,
    required_product_axes: requiredProductAxes,
  }

  const baselineText = `${JSON.stringify(baseline, null, 2)}\n`
  writeFileSync(resolve(root, outputBaselinePath), baselineText)
  const outputBaselineSha256 = sha256(baselineText)

  const provenanceRecords = top10.map((project) => {
    const recordBase = {
      schemaVersion: 'openclaude_oss_baseline_refresh_provenance_v1',
      snapshotDate,
      outputBaselinePath,
      outputBaselineSha256,
      rank: project.rank,
      fullName: project.full_name,
      stars: project.stars,
      license: project.license,
      pushedAt: project.pushed_at,
      forks: project.forks,
      openIssues: project.open_issues,
      sourceUrl: project.source_url,
      discoveredFrom: project.discovered_from,
      relevanceTerms: project.relevance_terms,
    }
    return {
      ...recordBase,
      recordDigest: sha256(JSON.stringify(recordBase)),
    }
  })
  const provenanceJsonlText = `${provenanceRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
  writeFileSync(resolve(root, provenanceJsonlPath), provenanceJsonlText)
  const provenanceJsonlSha256 = sha256(provenanceJsonlText)

  const currentTop10 = new Set(top10.map((project) => project.full_name.toLowerCase()))
  const newlyDiscoveredTop10Projects = top10
    .filter((project) => !previousTop10.has(project.full_name.toLowerCase()))
    .map((project) => project.full_name)
  const removedPreviousTop10Projects = Array.from(previousTop10)
    .filter((project) => !currentTop10.has(project))
    .map((project) => previousBaseline.top10.find((item) => item.full_name.toLowerCase() === project)?.full_name ?? project)

  const top10LowestStars = Math.min(...top10.map((project) => project.stars))
  const discoveredHigherStarCandidatesExcluded = excludedCandidates
    .filter((item) => item.stars > top10LowestStars)
    .sort((left, right) => right.stars - left.stars)

  const ranksConsecutive = top10.every((project, index) => project.rank === index + 1)
  const starsSortedDescending = top10.every((project, index, projects) => index === 0 || projects[index - 1].stars >= project.stars)
  const sourceUrlsAreGithubRepos = top10.every((project) => /^https:\/\/github\.com\/[^/]+\/[^/]+$/.test(project.source_url))
  const providerCallsPerformed: [] = []
  const liveModelCallsPerformed: [] = []
  const protectedActionsExecuted: [] = []
  const checks = [
    check('fresh GitHub baseline has exactly 10 projects', top10.length === 10, `${top10.length}`),
    check('fresh GitHub baseline ranks are consecutive', ranksConsecutive, top10.map((project) => project.rank).join(',')),
    check('fresh GitHub baseline stars are sorted descending', starsSortedDescending, top10.map((project) => `${project.full_name}:${project.stars}`).join(',')),
    check('fresh GitHub baseline source URLs are GitHub repos', sourceUrlsAreGithubRepos, top10.map((project) => project.source_url).join(',')),
    check('fresh GitHub baseline contains explicit seed and search evidence', top10.every((project) => project.discovered_from.length > 0), top10.map((project) => `${project.full_name}:${project.discovered_from.join('+')}`).join(',')),
    check('fresh GitHub baseline records relevance terms', top10.every((project) => project.relevance_terms.length > 0), top10.map((project) => `${project.full_name}:${project.relevance_terms.join('+')}`).join(',')),
    check('fresh GitHub refresh discovered current high-star related candidate', top10.some((project) => project.full_name === 'ultraworkers/claw-code'), top10.map((project) => project.full_name).join(',')),
    check('fresh GitHub refresh excludes higher-star non-product candidates with reasons', discoveredHigherStarCandidatesExcluded.every((item) => item.reason.length > 0), discoveredHigherStarCandidatesExcluded.map((item) => `${item.fullName}:${item.reason}`).join(',')),
    check('fresh GitHub refresh wrote parseable provenance JSONL', provenanceRecords.length === top10.length && provenanceJsonlSha256.length === 64, provenanceJsonlPath),
    check('fresh GitHub refresh performed external GitHub calls only', externalCallsPerformed.length > 0 && providerCallsPerformed.length === 0 && liveModelCallsPerformed.length === 0 && protectedActionsExecuted.length === 0, `${externalCallsPerformed.length} GitHub calls`),
  ]

  const report: RefreshReport = {
    generatedAt: new Date().toISOString(),
    mode: 'external_github_api_oss_baseline_refresh',
    snapshotDate,
    outputBaselinePath,
    outputBaselineSha256,
    previousBaselinePath,
    previousBaselineSha256,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: provenanceRecords.length,
    searchQueryCount: searchQueries.length,
    searchedRepositoryCount: Array.from(candidateRepos.values()).filter((repo) => !explicitSeedRepositories.map((item) => item.toLowerCase()).includes(repo.full_name.toLowerCase())).length,
    explicitSeedRepositoryCount: explicitSeedRepositories.length,
    uniqueCandidateCount: candidateRepos.size,
    eligibleCandidateCount: eligible.length,
    top10ProjectCount: top10.length,
    newlyDiscoveredTop10Projects,
    removedPreviousTop10Projects,
    discoveredHigherStarCandidatesExcluded,
    baselineFreshForPublicComparisonInput: true,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    externalGitHubRefreshPerformed: true,
    githubApiCallPerformed: true,
    providerCallsPerformed,
    liveModelCallsPerformed,
    protectedActionsExecuted,
    externalCallsPerformed,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST Search repositories',
        sourceUrl: 'https://docs.github.com/en/rest/search/search#search-repositories',
        observedPattern: 'GitHub Search API supports repository discovery with query, sort=stars, order=desc, and repository metadata results.',
        localAbsorption: 'OpenClaude uses the Search API only to refresh internal candidate discovery evidence and writes the exact query URLs.',
      },
      {
        sourceProject: 'GitHub REST Repositories metadata',
        sourceUrl: 'https://docs.github.com/en/rest/repos/repos',
        observedPattern: 'Repository metadata exposes full_name, stargazers_count, license, pushed_at, fork, archived, topics, and repository URLs.',
        localAbsorption: 'OpenClaude stores hash-addressed repository metadata provenance before using a repo as a benchmark candidate.',
      },
      {
        sourceProject: 'GitHub Docs stars',
        sourceUrl: 'https://docs.github.com/articles/stars',
        observedPattern: 'GitHub stars are an interest signal and are used by some rankings, but they are not validation of product quality.',
        localAbsorption: 'OpenClaude uses star order as discovery input only and keeps superiority/release/readiness claims blocked.',
      },
    ],
    selfImprovementActions: [
      'Promote fresh GitHub metadata refresh to a repeatable evidence command instead of relying on stale hand-curated baseline files.',
      'Add newly discovered high-star related projects, including ultraworkers/claw-code when it passes bounded relevance filters, to benchmark review inputs.',
      'Keep higher-star non-product repositories visible as exclusions so OpenClaude does not learn from popularity signals that are unrelated to coding-agent product quality.',
      'Require separate source review before absorbing implementation patterns or claiming public benchmark comparison.',
    ],
    refreshChecks: checks,
  }

  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeMarkdown(report, baseline)

  for (const item of checks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }

  const failed = checks.filter((item) => !item.ok)
  if (failed.length > 0) {
    console.error(`RESULT: FAIL (${failed.length} failed checks)`)
    process.exit(1)
  }

  console.log('RESULT: PASS')
  console.log(`snapshot_date=${snapshotDate}`)
  console.log(`output_baseline_path=${outputBaselinePath}`)
  console.log(`top10_project_count=${top10.length}`)
  console.log(`unique_candidate_count=${candidateRepos.size}`)
  console.log(`eligible_candidate_count=${eligible.length}`)
  console.log(`newly_discovered_top10_projects=${newlyDiscoveredTop10Projects.join(',') || 'none'}`)
  console.log(`removed_previous_top10_projects=${removedPreviousTop10Projects.join(',') || 'none'}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report.superiorityClaimAllowed}`)
  console.log(`external_github_refresh_performed=${report.externalGitHubRefreshPerformed}`)
  console.log(`github_api_call_performed=${report.githubApiCallPerformed}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error))
  console.error('RESULT: FAIL')
  process.exit(1)
})
