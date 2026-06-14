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
  top10: BaselineProject[]
}

type GitHubReadme = {
  name: string
  path: string
  sha: string
  size: number
  html_url: string | null
  download_url: string | null
  content?: string
  encoding?: string
}

type GitHubContentItem = {
  name: string
  path: string
  type: string
  size: number
  sha: string
  html_url: string | null
}

type ReviewRecord = {
  schemaVersion: 'openclaude_oss_source_review_v1'
  baselineSnapshotDate: string
  rank: number
  fullName: string
  sourceUrl: string
  stars: number
  readmeFetched: boolean
  rootContentsFetched: boolean
  readmeSourceKind: 'github_rest_readme' | 'github_raw_readme' | 'none'
  rootContentsSourceKind: 'github_rest_contents' | 'github_web_root' | 'none'
  readmeSha: string | null
  readmeHtmlUrl: string | null
  readmeSizeBytes: number
  readmeDigest: string | null
  rootManifestMarkers: string[]
  rootSourceMarkers: string[]
  readmeProductSignals: string[]
  sourceReviewStatus: 'source_supported_candidate' | 'metadata_only_needs_deeper_review'
  reviewRationale: string
  absorptionCandidate: boolean
  immediateAbsorptionAction: string
  recordDigest: string
}

type SourceReviewReport = {
  generatedAt: string
  mode: 'external_github_api_oss_source_review'
  sourceBaselinePath: string
  sourceBaselineSha256: string
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
  externalGitHubSourceReviewPerformed: true
  githubApiCallPerformed: true
  publicComparisonClaimAllowed: false
  superiorityClaimAllowed: false
  releaseReadinessClaimAllowed: false
  productionReadinessClaimAllowed: false
  publicReadinessClaimAllowed: false
  externalValidationClaimAllowed: false
  autonomousReliabilityClaimAllowed: false
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  protectedActionsExecuted: []
  externalCallsPerformed: Array<{
    kind: 'github_rest_readme' | 'github_rest_contents' | 'github_raw_readme' | 'github_web_root'
    url: string
    status: number | null
    rateLimitRemaining: string | null
    rateLimitReset: string | null
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
    localAbsorption: string
  }>
  selfImprovementActions: string[]
  sourceReviewChecks: Check[]
  reviewRecords: ReviewRecord[]
  claimBoundary: string
}

const root = process.cwd()
const baselinePath = 'docs/product-quality/oss-top10-baseline-2026-05-21.json'
const reportJsonPath = 'docs/product-quality/oss-source-review-report.json'
const reportMdPath = 'docs/product-quality/oss-source-review-report.md'
const provenanceJsonlPath = 'reports/openclaude-oss-source-review-provenance.jsonl'
const userAgent = 'OpenClaudeProductQualitySourceReview'
const newTop10Candidates = new Set(['ultraworkers/claw-code', 'warpdotdev/warp', 'ruvnet/ruflo'])
const githubToken = process.env.GITHUB_TOKEN || process.env.GH_TOKEN

const manifestNames = new Set([
  'package.json',
  'Cargo.toml',
  'pyproject.toml',
  'setup.py',
  'go.mod',
  'bun.lock',
  'pnpm-lock.yaml',
  'yarn.lock',
  'package-lock.json',
])

const sourceDirectoryNames = new Set([
  'src',
  'crates',
  'packages',
  'apps',
  'cli',
  'cmd',
  'internal',
  'lib',
  'python',
  'app',
])

const productSignalPatterns = [
  ['coding-agent', /coding agent|agentic coding|autonomous coding agent/i],
  ['terminal-cli', /terminal|command line|command-line|\bcli\b/i],
  ['ide-extension', /\bide\b|vs code|vscode|extension|editor/i],
  ['tool-use', /tool use|tools?|execute|edit files?|run commands?|shell|mcp/i],
  ['codebase-workflow', /codebase|git workflow|pull request|software engineering|developer/i],
  ['provider-model', /llm|model|openai|anthropic|claude|gemini|codex|ollama/i],
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

function githubHeaders(): Headers {
  const headers = new Headers({
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': userAgent,
  })
  if (githubToken) headers.set('Authorization', `Bearer ${githubToken}`)
  return headers
}

function genericHeaders(): Headers {
  return new Headers({
    'User-Agent': userAgent,
  })
}

function recordCall(
  calls: SourceReviewReport['externalCallsPerformed'],
  kind: SourceReviewReport['externalCallsPerformed'][number]['kind'],
  url: string,
  response: Response | null,
): void {
  calls.push({
    kind,
    url,
    status: response?.status ?? null,
    rateLimitRemaining: response?.headers.get('x-ratelimit-remaining') ?? null,
    rateLimitReset: response?.headers.get('x-ratelimit-reset') ?? null,
  })
}

async function fetchJson<T>(
  url: string,
  calls: SourceReviewReport['externalCallsPerformed'],
  kind: 'github_rest_readme' | 'github_rest_contents',
): Promise<T | null> {
  const response = await fetch(url, { headers: githubHeaders() })
  recordCall(calls, kind, url, response)
  if (response.status === 404) return null
  if (response.status === 403 || response.status === 429) return null
  if (!response.ok) {
    const body = await response.text()
    throw new Error(`GitHub request failed ${response.status} ${response.statusText}: ${url}: ${body.slice(0, 300)}`)
  }
  return await response.json() as T
}

async function fetchText(
  url: string,
  calls: SourceReviewReport['externalCallsPerformed'],
  kind: 'github_raw_readme' | 'github_web_root',
): Promise<string | null> {
  const response = await fetch(url, { headers: genericHeaders() })
  recordCall(calls, kind, url, response)
  if (!response.ok) return null
  return await response.text()
}

function readmeText(readme: GitHubReadme | null): string {
  if (!readme?.content || readme.encoding !== 'base64') return ''
  return Buffer.from(readme.content.replace(/\s/g, ''), 'base64').toString('utf8')
}

async function fetchRawReadme(owner: string, repo: string, calls: SourceReviewReport['externalCallsPerformed']): Promise<{ text: string; url: string } | null> {
  const candidatePaths = ['README.md', 'readme.md', 'README']
  for (const path of candidatePaths) {
    const url = `https://raw.githubusercontent.com/${owner}/${repo}/HEAD/${path}`
    const text = await fetchText(url, calls, 'github_raw_readme')
    if (text && text.trim().length > 0) return { text, url }
  }
  return null
}

function htmlMentionsRootEntry(html: string, owner: string, repo: string, entry: string, kind: 'blob' | 'tree'): boolean {
  const encodedEntry = entry.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const ownerRepo = `${owner}/${repo}`.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return new RegExp(`/${ownerRepo}/${kind}/[^"']+/${encodedEntry}["'#?]`, 'i').test(html)
    || new RegExp(`"name"\\s*:\\s*"${encodedEntry}"`, 'i').test(html)
}

async function fetchRootMarkers(owner: string, repo: string, calls: SourceReviewReport['externalCallsPerformed']): Promise<{ manifestMarkers: string[]; sourceMarkers: string[]; fetched: boolean }> {
  const url = `https://github.com/${owner}/${repo}`
  const html = await fetchText(url, calls, 'github_web_root')
  if (!html) return { manifestMarkers: [], sourceMarkers: [], fetched: false }
  const manifestMarkers = [...manifestNames]
    .filter((name) => htmlMentionsRootEntry(html, owner, repo, name, 'blob') || html.includes(`>${name}<`) || html.includes(`"${name}"`))
    .sort((left, right) => left.localeCompare(right))
  const sourceMarkers = [...sourceDirectoryNames]
    .filter((name) => htmlMentionsRootEntry(html, owner, repo, name, 'tree') || html.includes(`>${name}<`) || html.includes(`"${name}"`))
    .sort((left, right) => left.localeCompare(right))
  return { manifestMarkers, sourceMarkers, fetched: true }
}

function productSignals(text: string, project: BaselineProject): string[] {
  const haystack = `${project.full_name} ${project.positioning} ${text}`.slice(0, 120_000)
  return productSignalPatterns
    .filter(([, pattern]) => pattern.test(haystack))
    .map(([label]) => label)
}

function markerNames(items: GitHubContentItem[], names: Set<string>): string[] {
  return items
    .filter((item) => names.has(item.name))
    .map((item) => item.name)
    .sort((left, right) => left.localeCompare(right))
}

function sourceMarkerNames(items: GitHubContentItem[]): string[] {
  return items
    .filter((item) => item.type === 'dir' && sourceDirectoryNames.has(item.name))
    .map((item) => item.name)
    .sort((left, right) => left.localeCompare(right))
}

function reviewStatus(
  readmeFetched: boolean,
  rootContentsFetched: boolean,
  readmeSignals: string[],
  manifestMarkers: string[],
  sourceMarkers: string[],
): ReviewRecord['sourceReviewStatus'] {
  const hasSourceShape = manifestMarkers.length > 0 || sourceMarkers.length > 0
  if (readmeFetched && rootContentsFetched && readmeSignals.length >= 2 && hasSourceShape) return 'source_supported_candidate'
  return 'metadata_only_needs_deeper_review'
}

function immediateAction(project: BaselineProject, status: ReviewRecord['sourceReviewStatus'], signals: string[]): string {
  if (status === 'metadata_only_needs_deeper_review') {
    return `Keep ${project.full_name} in metadata baseline only; require deeper source review before implementation-pattern absorption.`
  }
  if (newTop10Candidates.has(project.full_name)) {
    return `Review ${project.full_name} architecture/docs next because it newly entered the top-10 baseline and has source-level product signals: ${signals.join(', ')}.`
  }
  return `Use ${project.full_name} as source-supported benchmark input for future axis-specific reviews without claiming OpenClaude superiority.`
}

function writeMarkdown(report: SourceReviewReport): void {
  const rows = report.reviewRecords
    .map((record) => `| ${record.rank} | \`${record.fullName}\` | \`${record.sourceReviewStatus}\` | ${record.readmeProductSignals.join(', ') || 'none'} | ${[...record.rootManifestMarkers, ...record.rootSourceMarkers].join(', ') || 'none'} | ${record.immediateAbsorptionAction} |`)
    .join('\n')
  const checkRows = report.sourceReviewChecks
    .map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`)
    .join('\n')

  const markdown = `# OSS Source Review Report

Generated by: \`bun run product:oss-source-review\`

## Claim Boundary

- This report reviews README and root source markers for the refreshed GitHub top-10 baseline.
- It does not clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, modify external repos, publish, deploy, launch, or claim public comparison, superiority, release readiness, production readiness, external validation, or autonomous reliability.
- Metadata-only candidates remain benchmark-planning inputs until deeper source review is completed.

## Summary

- mode: \`${report.mode}\`
- source_baseline_path: \`${report.sourceBaselinePath}\`
- baseline_snapshot_date: \`${report.baselineSnapshotDate}\`
- reviewed_project_count: \`${report.reviewedProjectCount}\`
- source_supported_candidate_count: \`${report.sourceSupportedCandidateCount}\`
- metadata_only_needs_review_count: \`${report.metadataOnlyNeedsReviewCount}\`
- absorption_candidate_count: \`${report.absorptionCandidateCount}\`
- public_comparison_claim_allowed: \`${report.publicComparisonClaimAllowed}\`
- superiority_claim_allowed: \`${report.superiorityClaimAllowed}\`

## Reviewed Projects

| Rank | Project | Status | README product signals | Root source markers | Immediate action |
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

async function main(): Promise<void> {
  if (!existsSync(resolve(root, baselinePath))) {
    console.error(`RESULT: FAIL (${baselinePath} missing)`)
    process.exit(1)
  }

  mkdirSync(resolve(root, 'docs/product-quality'), { recursive: true })
  mkdirSync(resolve(root, 'reports'), { recursive: true })

  const baselineText = readText(baselinePath)
  const baselineSha256 = sha256(baselineText)
  const baseline = JSON.parse(baselineText) as Baseline
  const externalCallsPerformed: SourceReviewReport['externalCallsPerformed'] = []
  const reviewRecords: ReviewRecord[] = []

  for (const project of baseline.top10) {
    const [owner, repo] = project.full_name.split('/')
    const readmeUrl = `https://api.github.com/repos/${owner}/${repo}/readme`
    const contentsUrl = `https://api.github.com/repos/${owner}/${repo}/contents`
    const readme = await fetchJson<GitHubReadme>(readmeUrl, externalCallsPerformed, 'github_rest_readme')
    const contents = await fetchJson<GitHubContentItem[]>(contentsUrl, externalCallsPerformed, 'github_rest_contents')
    const safeContents = Array.isArray(contents) ? contents : []
    const rawReadme = readme ? null : await fetchRawReadme(owner, repo, externalCallsPerformed)
    const webRootMarkers = safeContents.length > 0
      ? { manifestMarkers: [] as string[], sourceMarkers: [] as string[], fetched: false }
      : await fetchRootMarkers(owner, repo, externalCallsPerformed)
    const decodedReadme = readmeText(readme) || rawReadme?.text || ''
    const readmeDigest = decodedReadme ? sha256(decodedReadme) : null
    const rootManifestMarkers = (safeContents.length > 0 ? markerNames(safeContents, manifestNames) : webRootMarkers.manifestMarkers)
    const rootSourceMarkers = (safeContents.length > 0 ? sourceMarkerNames(safeContents) : webRootMarkers.sourceMarkers)
    const readmeProductSignals = productSignals(decodedReadme, project)
    const readmeFetched = Boolean(readme || rawReadme)
    const rootContentsFetched = safeContents.length > 0 || webRootMarkers.fetched
    const sourceReviewStatus = reviewStatus(readmeFetched, rootContentsFetched, readmeProductSignals, rootManifestMarkers, rootSourceMarkers)
    const absorptionCandidate = sourceReviewStatus === 'source_supported_candidate'
    const recordBase = {
      schemaVersion: 'openclaude_oss_source_review_v1' as const,
      baselineSnapshotDate: baseline.snapshot_date,
      rank: project.rank,
      fullName: project.full_name,
      sourceUrl: project.source_url,
      stars: project.stars,
      readmeFetched,
      rootContentsFetched,
      readmeSourceKind: readme ? 'github_rest_readme' as const : rawReadme ? 'github_raw_readme' as const : 'none' as const,
      rootContentsSourceKind: safeContents.length > 0 ? 'github_rest_contents' as const : webRootMarkers.fetched ? 'github_web_root' as const : 'none' as const,
      readmeSha: readme?.sha ?? null,
      readmeHtmlUrl: readme?.html_url ?? rawReadme?.url ?? null,
      readmeSizeBytes: decodedReadme.length,
      readmeDigest,
      rootManifestMarkers,
      rootSourceMarkers,
      readmeProductSignals,
      sourceReviewStatus,
      reviewRationale: sourceReviewStatus === 'source_supported_candidate'
        ? 'README product signals and root source markers support treating this as a source-reviewed benchmark candidate.'
        : 'GitHub metadata is not enough; README or root source markers were insufficient for implementation-pattern absorption.',
      absorptionCandidate,
      immediateAbsorptionAction: immediateAction(project, sourceReviewStatus, readmeProductSignals),
    }
    reviewRecords.push({
      ...recordBase,
      recordDigest: sha256(JSON.stringify(recordBase)),
    })
  }

  const provenanceText = `${reviewRecords.map((record) => JSON.stringify(record)).join('\n')}\n`
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

  const sourceSupportedCandidateCount = reviewRecords.filter((record) => record.sourceReviewStatus === 'source_supported_candidate').length
  const metadataOnlyNeedsReviewCount = reviewRecords.filter((record) => record.sourceReviewStatus === 'metadata_only_needs_deeper_review').length
  const baselineNewTop10Candidates = baseline.top10
    .map((project) => project.full_name)
    .filter((name) => newTop10Candidates.has(name))
  const newTop10SourceReviewed = reviewRecords
    .filter((record) => newTop10Candidates.has(record.fullName))
    .map((record) => record.fullName)
  const checks = [
    check('source review imports refreshed baseline', baseline.snapshot_date === '2026-05-21' && baseline.top10.length === 10, `${baseline.snapshot_date}/${baseline.top10.length}`),
    check('source review covers every baseline project', reviewRecords.length === baseline.top10.length, `${reviewRecords.length}/${baseline.top10.length}`),
    check('source review fetched README and root contents for most candidates', reviewRecords.filter((record) => record.readmeFetched && record.rootContentsFetched).length >= 8, `${reviewRecords.filter((record) => record.readmeFetched && record.rootContentsFetched).length}/10`),
    check('source review records source-supported or metadata-only classification for every candidate', reviewRecords.every((record) => record.sourceReviewStatus === 'source_supported_candidate' || record.sourceReviewStatus === 'metadata_only_needs_deeper_review'), 'all classified'),
    check('source review preserves newly discovered top-10 candidates', baselineNewTop10Candidates.every((name) => newTop10SourceReviewed.includes(name)), newTop10SourceReviewed.join(',')),
    check('source review keeps metadata-only candidates bounded when evidence is insufficient', metadataOnlyNeedsReviewCount >= 0 && sourceSupportedCandidateCount + metadataOnlyNeedsReviewCount === reviewRecords.length, `${metadataOnlyNeedsReviewCount}`),
    check('source review finds source-supported benchmark candidates', sourceSupportedCandidateCount >= 5, `${sourceSupportedCandidateCount}`),
    check('source review writes parseable provenance JSONL', provenanceJsonlParseable && provenanceJsonlSha256.length === 64 && reviewRecords.length === baseline.top10.length, provenanceJsonlPath),
    check('source review performed GitHub source calls only', externalCallsPerformed.length >= baseline.top10.length * 2 && externalCallsPerformed.every((call) => call.url.startsWith('https://api.github.com/') || call.url.startsWith('https://raw.githubusercontent.com/') || call.url.startsWith('https://github.com/')), `${externalCallsPerformed.length} GitHub calls`),
  ]

  const providerCallsPerformed: [] = []
  const liveModelCallsPerformed: [] = []
  const protectedActionsExecuted: [] = []
  const report: SourceReviewReport = {
    generatedAt: new Date().toISOString(),
    mode: 'external_github_api_oss_source_review',
    sourceBaselinePath: baselinePath,
    sourceBaselineSha256: baselineSha256,
    baselineSnapshotDate: baseline.snapshot_date,
    reviewedProjectCount: reviewRecords.length,
    sourceSupportedCandidateCount,
    metadataOnlyNeedsReviewCount,
    absorptionCandidateCount: reviewRecords.filter((record) => record.absorptionCandidate).length,
    newTop10SourceReviewed,
    provenanceJsonlPath,
    provenanceJsonlSha256,
    provenanceJsonlRecordCount: reviewRecords.length,
    provenanceJsonlParseable,
    externalGitHubSourceReviewPerformed: true,
    githubApiCallPerformed: true,
    publicComparisonClaimAllowed: false,
    superiorityClaimAllowed: false,
    releaseReadinessClaimAllowed: false,
    productionReadinessClaimAllowed: false,
    publicReadinessClaimAllowed: false,
    externalValidationClaimAllowed: false,
    autonomousReliabilityClaimAllowed: false,
    providerCallsPerformed,
    liveModelCallsPerformed,
    protectedActionsExecuted,
    externalCallsPerformed,
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST repository README endpoint',
        sourceUrl: 'https://docs.github.com/en/rest/repos/contents#get-a-repository-readme',
        observedPattern: 'Repository README content is a primary project source for product positioning, installation, and usage evidence.',
        localAbsorption: 'OpenClaude reviews README content before treating high-star candidates as implementation-pattern inputs.',
      },
      {
        sourceProject: 'GitHub REST repository contents endpoint',
        sourceUrl: 'https://docs.github.com/en/rest/repos/contents#get-repository-content',
        observedPattern: 'Repository contents expose root manifests and source directories that distinguish executable products from metadata-only candidates.',
        localAbsorption: 'OpenClaude records root manifest/source markers before absorbing benchmark implementation patterns.',
      },
    ],
    selfImprovementActions: [
      'Require README and root source marker review after every fresh GitHub top-10 metadata refresh.',
      'Treat metadata-only high-star projects as planning inputs only until deeper source review is complete.',
      'Prioritize source-supported newly discovered candidates for architecture-specific absorption reviews.',
      'Keep source review separate from public comparison or superiority claims.',
    ],
    sourceReviewChecks: checks,
    reviewRecords,
    claimBoundary: 'OSS source review is external GitHub README and contents metadata review for internal benchmark planning only. It does not clone repositories, install dependencies, call providers, call live models, mutate production OpenClaude, mutate external repositories, publish, deploy, launch, or authorize public comparison, superiority, release, production, external-validation, or autonomous-reliability claims.',
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
  console.log(`reviewed_project_count=${report.reviewedProjectCount}`)
  console.log(`source_supported_candidate_count=${report.sourceSupportedCandidateCount}`)
  console.log(`metadata_only_needs_review_count=${report.metadataOnlyNeedsReviewCount}`)
  console.log(`absorption_candidate_count=${report.absorptionCandidateCount}`)
  console.log(`new_top10_source_reviewed=${report.newTop10SourceReviewed.join(',') || 'none'}`)
  console.log(`public_comparison_claim_allowed=${report.publicComparisonClaimAllowed}`)
  console.log(`superiority_claim_allowed=${report.superiorityClaimAllowed}`)
  console.log(`external_github_source_review_performed=${report.externalGitHubSourceReviewPerformed}`)
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
