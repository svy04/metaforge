import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { env, exit } from 'node:process'
import { spawnSync } from 'node:child_process'
import { check, sha256, type Check } from './quality-report-helpers'

type RemoteHead = {
  name: string
  oid: string
}

type OpenPullRequest = {
  number: number
  title: string
  url: string
  headRefName: string
  isSameRepository: boolean
}

type PatternFinding = {
  path: string
  line: number
  patternId: string
  text: string
}

type TreeFinding = {
  path: string
  patternId: string
}

type RefScan = {
  refName: string
  patternFindings: PatternFinding[]
  treeFindings: TreeFinding[]
}

type Discovery = {
  gitFetchPerformed: boolean
  remoteHeadDiscovery: 'git_ls_remote'
  openPullRequestDiscovery: 'github_pr_api' | 'gh_cli' | 'unavailable'
  openPullRequestDiscoveryError?: string
}

type Blocker = {
  category:
    | 'unexpected_remote_branch'
    | 'forbidden_pattern'
    | 'browser_capture_artifact'
    | 'open_pull_request_discovery_unavailable'
  refName?: string
  path?: string
  line?: number
  detail: string
}

type AnalyzeInput = {
  defaultBranch: string
  remoteHeads: RemoteHead[]
  openPullRequests: OpenPullRequest[]
  refScans: RefScan[]
  discovery: Discovery
}

type PublicGithubSurfaceReport = {
  generatedAt: string
  mode: 'github_public_remote_surface_audit'
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
    observedPattern: string
  }>
  defaultBranch: string
  remoteHeads: RemoteHead[]
  remoteHeadCount: number
  openPullRequests: OpenPullRequest[]
  openPullRequestCount: number
  allowedOpenPrHeadBranches: string[]
  refScans: RefScan[]
  blockers: Blocker[]
  blockerCount: number
  status: 'no_public_github_surface_findings_detected' | 'blocked_public_github_surface_findings'
  discovery: Discovery
  providerCallsPerformed: []
  liveModelCallsPerformed: []
  protectedActionsExecuted: []
  externalCallsPerformed: string[]
  evidenceChecks: Check[]
  claimBoundary: string
}

const root = process.cwd()
const docsDir = resolve(root, 'docs/product-quality')
const reportsDir = resolve(root, 'reports')
const reportJsonPath = 'docs/product-quality/github-remote-surface-audit-report.json'
const reportMdPath = 'docs/product-quality/github-remote-surface-audit-report.md'
const reportJsonlPath = 'reports/openclaude-github-remote-surface-audit.jsonl'
const koreanLocalWorkspaceName = String.fromCharCode(0xb0b4, 0x20, 0xc21c, 0xc218, 0x20, 0xc7ac, 0xbbf8)
const privateLocalOrTokenPatterns = [
  String.raw`C:(\\+|/)Users(\\+|/)[^\\/"' ]+(\\+|/)(Desktop|Documents|AppData)(\\+|/)[^\\/"' ]+`,
  String.raw`/Users/[^/"' ]+/(Desktop|Documents)/[^/"' ]+`,
  String.raw`Users/[^/"' ]+/(Desktop|Documents)/[^/"' ]+`,
  String.raw`(%USERPROFILE%|\$HOME|\$\{HOME\}|~)(\\+|/)(Desktop|Documents)(\\+|/)[^\\/"' ]+`,
  koreanLocalWorkspaceName,
  ['Digital', ' Factory'].join(''),
  ['Token: ', 'gho_'].join(''),
  String.raw`gh[pousr]_[A-Za-z0-9_]{30,}`,
  String.raw`github_pat_[A-Za-z0-9_]{30,}`,
  String.raw`AKIA[0-9A-Z]{16}`,
  String.raw`ASIA[0-9A-Z]{16}`,
  String.raw`xox[baprs]-[A-Za-z0-9-]{10,}`,
  String.raw`-----BEGIN (RSA|DSA|EC|OPENSSH|PGP) PRIVATE KEY-----`,
]
const publicArtifactHygienePatterns = [
  String.raw`<codex_internal_context`,
  String.raw`<environment_context`,
  String.raw`<workspace_roots`,
  String.raw`<permissions instructions`,
  String.raw`\.` + 'codex' + String.raw`[\\/]+` + 'memories',
  String.raw`\.` + 'agents' + String.raw`[\\/]+` + 'skills',
  String.raw`AGENTS\.md instructions for C:`,
  String.raw`sk-\.\.\.`,
  String.raw`(api[-_ ]?key|token).{0,80}sk-[A-Za-z0-9_-]{8,}`,
]
const privateLocalOrTokenPattern = privateLocalOrTokenPatterns.join('|')
const publicArtifactHygienePattern = publicArtifactHygienePatterns.join('|')
const privatePattern = [
  privateLocalOrTokenPattern,
  publicArtifactHygienePattern,
].join('|')
const tokenPattern = /(gh[pousr]_|github_pat_|AKIA|ASIA|xox[baprs]-|sk-[A-Za-z0-9_-]{8,})/i
const documentedPlaceholderPattern = new RegExp(String.raw`(?:^|[\\/\s"'\x60])(?:Example|example|foo|me|fixture-owner|John[ _]Smith|\{user\}|\.\.\.)(?:[\\/\s"'\x60]|$)`)

function isRemotePublicArtifactPath(path?: string): boolean {
  if (!path) {
    return true
  }
  const normalized = path.replace(/\\/g, '/')
  return [
    '.github/',
    '.planning/',
    'avf/',
    'bin/',
    'docs/',
    'reports/',
    'packages/openclaude-vscode/',
    'vscode-extension/openclaude-vscode/',
  ].some((prefix) => normalized.startsWith(prefix)) || [
    '.env.example',
    'AGENTS.md',
    'ANDROID_INSTALL.md',
    'CHANGELOG.md',
    'CONTRIBUTING.md',
    'LICENSE',
    'PLAYBOOK.md',
    'README.md',
    'README.ko.md',
    'SECURITY.md',
    'SUPPORT.md',
    'package.json',
    'scripts/public-artifact-hygiene.ts',
  ].includes(normalized)
}

export function remoteForbiddenPatternId(text: string, path?: string): string | null {
  if (new RegExp(privateLocalOrTokenPattern, 'i').test(text)) {
    if (documentedPlaceholderPattern.test(text) && !tokenPattern.test(text)) {
      return null
    }
    return 'private_local_or_token_pattern'
  }

  if (isRemotePublicArtifactPath(path) && new RegExp(publicArtifactHygienePattern, 'i').test(text)) {
    return 'public_artifact_hygiene_pattern'
  }

  return null
}

export function matchesRemoteForbiddenPattern(text: string): boolean {
  return remoteForbiddenPatternId(text) !== null
}

function isIntentionalRemoteAuditFixture(finding: PatternFinding): boolean {
  if (!/\.(?:test|spec)\.[jt]sx?$/.test(finding.path)) {
    return false
  }
  return /(?:%USERPROFILE%|\$HOME|\$\{HOME\}|~)(?:\\+|\/)(?:Desktop|Documents)(?:\\+|\/)/i.test(finding.text)
}

const browserArtifactPatterns: Array<{ id: string; pattern: RegExp }> = [
  { id: 'playwright_mcp_capture', pattern: /(^|\/)\.playwright-mcp(\/|$)/i },
  { id: 'playwright_report', pattern: /(^|\/)playwright-report(\/|$)/i },
  { id: 'playwright_blob_report', pattern: /(^|\/)blob-report(\/|$)/i },
  { id: 'browser_trace_archive', pattern: /(^|\/)trace\.zip$/i },
  { id: 'browser_network_har', pattern: /\.har$/i },
  { id: 'browser_video_capture', pattern: /\.webm$/i },
]

export function analyzePublicGithubSurface(input: AnalyzeInput): PublicGithubSurfaceReport {
  const allowedOpenPrHeadBranches = input.openPullRequests
    .filter((pullRequest) => pullRequest.isSameRepository)
    .map((pullRequest) => pullRequest.headRefName)
    .sort()
  const allowedBranchSet = new Set([input.defaultBranch, ...allowedOpenPrHeadBranches])
  const blockers: Blocker[] = []

  for (const head of input.remoteHeads) {
    if (!allowedBranchSet.has(head.name)) {
      blockers.push({
        category: 'unexpected_remote_branch',
        refName: head.name,
        detail: `remote branch is not the default branch and is not attached to an open same-repository PR: ${head.name}`,
      })
    }
  }

  const nonDefaultRemoteHeads = input.remoteHeads.filter((head) => head.name !== input.defaultBranch)
  if (input.discovery.openPullRequestDiscovery === 'unavailable' && nonDefaultRemoteHeads.length > 0) {
    blockers.push({
      category: 'open_pull_request_discovery_unavailable',
      detail: input.discovery.openPullRequestDiscoveryError ?? 'open pull request discovery was unavailable while non-default remote branches exist',
    })
  }

  for (const refScan of input.refScans) {
    for (const finding of refScan.patternFindings) {
      blockers.push({
        category: 'forbidden_pattern',
        refName: refScan.refName,
        path: finding.path,
        line: finding.line,
        detail: `${finding.patternId}: ${finding.text}`,
      })
    }
    for (const finding of refScan.treeFindings) {
      blockers.push({
        category: 'browser_capture_artifact',
        refName: refScan.refName,
        path: finding.path,
        detail: finding.patternId,
      })
    }
  }

  const report: PublicGithubSurfaceReport = {
    generatedAt: new Date().toISOString(),
    mode: 'github_public_remote_surface_audit',
    primarySourceInputs: [
      {
        sourceProject: 'GitHub REST Pull Requests API',
        sourceUrl: 'https://docs.github.com/en/rest/pulls/pulls',
        observedPattern: 'Open pull requests and their head branches are public review surfaces and should be inventoried before claiming a repository is clean.',
      },
      {
        sourceProject: 'Git git-ls-remote',
        sourceUrl: 'https://git-scm.com/docs/git-ls-remote',
        observedPattern: 'Remote refs should be listed by ref name and object ID as the public branch inventory, not inferred from the local default branch only.',
      },
      {
        sourceProject: 'GitHub Secret Scanning',
        sourceUrl: 'https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning',
        observedPattern: 'Secret hygiene claims should distinguish current-tree local scans from full-history hosted secret scanning and alert status.',
      },
      {
        sourceProject: 'Gitleaks',
        sourceUrl: 'https://github.com/gitleaks/gitleaks',
        observedPattern: 'Security findings are strongest when they are rule-addressed and tied to Git refs, files, and lines.',
      },
      {
        sourceProject: 'Playwright Trace Viewer',
        sourceUrl: 'https://playwright.dev/docs/trace-viewer',
        observedPattern: 'Browser traces, DOM snapshots, network logs, videos, console output, and generated reports are data-bearing artifacts and should be blocked from public refs unless intentionally published.',
      },
      {
        sourceProject: 'OWASP Full Path Disclosure',
        sourceUrl: 'https://owasp.org/www-community/attacks/Full_Path_Disclosure',
        observedPattern: 'Absolute local paths are disclosure risks and should be scanned as privacy findings on public repository surfaces.',
      },
    ],
    defaultBranch: input.defaultBranch,
    remoteHeads: input.remoteHeads,
    remoteHeadCount: input.remoteHeads.length,
    openPullRequests: input.openPullRequests,
    openPullRequestCount: input.openPullRequests.length,
    allowedOpenPrHeadBranches,
    refScans: input.refScans,
    blockers,
    blockerCount: blockers.length,
    status: blockers.length === 0
      ? 'no_public_github_surface_findings_detected'
      : 'blocked_public_github_surface_findings',
    discovery: input.discovery,
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    protectedActionsExecuted: [],
    externalCallsPerformed: [
      input.discovery.remoteHeadDiscovery,
      input.discovery.openPullRequestDiscovery,
    ],
    evidenceChecks: [],
    claimBoundary: 'This public GitHub surface audit inventories remote refs and open PR heads for privacy/security blockers only. It does not claim full GitHub secret-scanning alert status, full-history credential cleanliness, release readiness, production readiness, or external validation.',
  }

  report.evidenceChecks = [
    check('default branch is present in remote heads', input.remoteHeads.some((head) => head.name === input.defaultBranch), input.defaultBranch),
    check('remote heads were inventoried', input.remoteHeads.length > 0, `${input.remoteHeads.length} heads`),
    check('open PR discovery is usable when non-default branches exist', input.discovery.openPullRequestDiscovery !== 'unavailable' || nonDefaultRemoteHeads.length === 0, input.discovery.openPullRequestDiscovery),
    check('unexpected stale remote branches are absent', !blockers.some((blocker) => blocker.category === 'unexpected_remote_branch'), `${blockers.filter((blocker) => blocker.category === 'unexpected_remote_branch').length} findings`),
    check('private local path and token patterns are absent from scanned public refs', !blockers.some((blocker) => blocker.category === 'forbidden_pattern'), `${blockers.filter((blocker) => blocker.category === 'forbidden_pattern').length} findings`),
    check('browser capture artifacts are absent from scanned public refs', !blockers.some((blocker) => blocker.category === 'browser_capture_artifact'), `${blockers.filter((blocker) => blocker.category === 'browser_capture_artifact').length} findings`),
    check('provider and live model calls remain absent', report.providerCallsPerformed.length === 0 && report.liveModelCallsPerformed.length === 0, 'all call arrays empty'),
    check('protected actions remain absent', report.protectedActionsExecuted.length === 0, 'zero protected actions'),
  ]

  return report
}

export function buildAuditJsonl(report: PublicGithubSurfaceReport): string {
  const records = report.blockers.length > 0
    ? report.blockers.map((blocker) => ({
      kind: 'github_remote_surface_audit_blocker',
      ...blocker,
    }))
    : [{
      kind: 'github_remote_surface_audit_summary',
      status: report.status,
      defaultBranch: report.defaultBranch,
      remoteHeadCount: report.remoteHeadCount,
      openPullRequestCount: report.openPullRequestCount,
      blockerCount: report.blockerCount,
    }]
  return `${records.map((record) => JSON.stringify(record)).join('\n')}\n`
}

function runGit(args: string[]): string {
  const result = spawnSync('git', args, {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })
  if (result.status !== 0) {
    throw new Error(`git ${args.join(' ')} failed: ${result.stderr || result.stdout}`)
  }
  return result.stdout
}

function fetchRemoteTrackingRefs(): void {
  runGit(['fetch', '--prune', 'origin', '+refs/heads/*:refs/remotes/origin/*'])
}

function discoverDefaultBranch(): string {
  const output = runGit(['ls-remote', '--symref', 'origin', 'HEAD'])
  const match = output.match(/^ref:\s+refs\/heads\/([^\t ]+)\s+HEAD/m)
  if (match?.[1]) {
    return match[1]
  }
  return 'main'
}

function discoverRemoteHeads(): RemoteHead[] {
  return runGit(['ls-remote', '--heads', 'origin'])
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => {
      const [oid, ref] = line.split(/\s+/)
      return {
        oid,
        name: ref.replace(/^refs\/heads\//, ''),
      }
    })
    .sort((a, b) => a.name.localeCompare(b.name))
}

function repositoryFullNameFromRemote(): string | null {
  const remoteUrl = runGit(['remote', 'get-url', 'origin']).trim()
  const httpsMatch = remoteUrl.match(/github\.com[:/]([^/]+)\/(.+?)(?:\.git)?$/i)
  if (!httpsMatch) {
    return env.GITHUB_REPOSITORY ?? null
  }
  return `${httpsMatch[1]}/${httpsMatch[2].replace(/\.git$/i, '')}`
}

async function discoverOpenPullRequests(repositoryFullName: string): Promise<{
  pullRequests: OpenPullRequest[]
  discovery: Discovery['openPullRequestDiscovery']
  error?: string
}> {
  const token = env.GITHUB_TOKEN ?? env.GH_TOKEN
  if (token) {
    const pullRequests: OpenPullRequest[] = []
    for (let page = 1; page <= 10; page += 1) {
      const response = await fetch(`https://api.github.com/repos/${repositoryFullName}/pulls?state=open&per_page=100&page=${page}`, {
        headers: {
          accept: 'application/vnd.github+json',
          authorization: `Bearer ${token}`,
          'x-github-api-version': '2022-11-28',
        },
      })
      if (!response.ok) {
        return { pullRequests: [], discovery: 'unavailable', error: `GitHub PR API HTTP ${response.status}` }
      }
      const pageItems = await response.json() as Array<{
        number: number
        title: string
        html_url: string
        head: { ref: string; repo: { full_name: string } | null }
      }>
      for (const item of pageItems) {
        pullRequests.push({
          number: item.number,
          title: item.title,
          url: item.html_url,
          headRefName: item.head.ref,
          isSameRepository: item.head.repo?.full_name?.toLowerCase() === repositoryFullName.toLowerCase(),
        })
      }
      if (pageItems.length < 100) {
        break
      }
    }
    return { pullRequests, discovery: 'github_pr_api' }
  }

  const result = spawnSync('gh', [
    'pr',
    'list',
    '--repo',
    repositoryFullName,
    '--state',
    'open',
    '--limit',
    '100',
    '--json',
    'number,title,url,headRefName,headRepository',
  ], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })
  if (result.status !== 0) {
    return { pullRequests: [], discovery: 'unavailable', error: result.stderr || result.stdout || 'gh pr list failed' }
  }
  const items = JSON.parse(result.stdout) as Array<{
    number: number
    title: string
    url: string
    headRefName: string
    headRepository?: { nameWithOwner?: string }
  }>
  return {
    pullRequests: items.map((item) => ({
      number: item.number,
      title: item.title,
      url: item.url,
      headRefName: item.headRefName,
      isSameRepository: item.headRepository?.nameWithOwner?.toLowerCase() === repositoryFullName.toLowerCase(),
    })),
    discovery: 'gh_cli',
  }
}

function parseGrepFindings(output: string): PatternFinding[] {
  const findings: PatternFinding[] = []
  for (const line of output
    .split(/\r?\n/)
    .filter(Boolean)) {
    const match = line.match(/^(?:[^:]+:)?(.+?):(\d+):(.*)$/)
    const finding = match
      ? {
        path: match[1],
        line: Number(match[2]),
        text: match[3].trim().replace(/\s+/g, ' ').slice(0, 240),
      }
      : {
        path: '<unknown>',
        line: 0,
        text: line.trim().slice(0, 240),
      }
    const patternId = remoteForbiddenPatternId(finding.text, finding.path)
    if (!patternId) {
      continue
    }
    const patternFinding = { ...finding, patternId }
    if (!isIntentionalRemoteAuditFixture(patternFinding)) {
      findings.push(patternFinding)
    }
  }
  return findings
}

function scanRef(refName: string): RefScan {
  const ref = `refs/remotes/origin/${refName}`
  const grep = spawnSync('git', [
    'grep',
    '-n',
    '-I',
    '-E',
    privatePattern,
    ref,
    '--',
    '.',
    ':!bun.lock',
    ':!package-lock.json',
  ], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })
  if (grep.status !== 0 && grep.status !== 1) {
    throw new Error(`git grep failed for ${refName}: ${grep.stderr || grep.stdout}`)
  }

  const tree = runGit(['ls-tree', '-r', '--name-only', ref])
  const treeFindings = tree
    .split(/\r?\n/)
    .filter(Boolean)
    .flatMap((path) => browserArtifactPatterns
      .filter((item) => item.pattern.test(path))
      .map((item) => ({ path, patternId: item.id })))

  return {
    refName,
    patternFindings: grep.status === 0 ? parseGrepFindings(grep.stdout) : [],
    treeFindings,
  }
}

function writeReports(report: PublicGithubSurfaceReport): void {
  mkdirSync(docsDir, { recursive: true })
  mkdirSync(reportsDir, { recursive: true })
  writeFileSync(resolve(root, reportJsonPath), `${JSON.stringify(report, null, 2)}\n`)
  writeFileSync(resolve(root, reportJsonlPath), buildAuditJsonl(report))

  const refRows = report.remoteHeads.map((head) => `| \`${head.name}\` | \`${head.oid}\` |`).join('\n')
  const prRows = report.openPullRequests.length === 0
    ? '| none | none | none | none |'
    : report.openPullRequests.map((pullRequest) => `| #${pullRequest.number} | ${pullRequest.title} | \`${pullRequest.headRefName}\` | \`${pullRequest.isSameRepository}\` |`).join('\n')
  const blockerRows = report.blockers.length === 0
    ? '| none | none | none | none |'
    : report.blockers.map((blocker) => `| \`${blocker.category}\` | \`${blocker.refName ?? ''}\` | \`${blocker.path ?? ''}${blocker.line ? `:${blocker.line}` : ''}\` | ${blocker.detail} |`).join('\n')
  const checkRows = report.evidenceChecks.map((item) => `| ${item.label} | \`${item.ok}\` | ${item.detail} |`).join('\n')

  writeFileSync(resolve(root, reportMdPath), `# GitHub Public Surface Report

Generated by: \`bun run product:github-remote-surface-audit\`

## Claim Boundary

- This report inventories GitHub remote branches and open pull request heads for public privacy/security blockers.
- It does not claim full-history secret cleanliness, GitHub secret-scanning alert status, release readiness, production readiness, or external validation.

## Summary

- default_branch: \`${report.defaultBranch}\`
- remote_head_count: \`${report.remoteHeadCount}\`
- open_pull_request_count: \`${report.openPullRequestCount}\`
- allowed_open_pr_head_branches: \`${report.allowedOpenPrHeadBranches.join(',') || 'none'}\`
- blocker_count: \`${report.blockerCount}\`
- status: \`${report.status}\`
- git_fetch_performed: \`${report.discovery.gitFetchPerformed}\`
- remote_head_discovery: \`${report.discovery.remoteHeadDiscovery}\`
- open_pull_request_discovery: \`${report.discovery.openPullRequestDiscovery}\`
- blocker_jsonl_sha256: \`${sha256(readFileSync(resolve(root, reportJsonlPath)))}\`

## Primary Source Inputs

| Source | URL | Pattern |
| --- | --- | --- |
${report.primarySourceInputs.map((source) => `| ${source.sourceProject} | ${source.sourceUrl} | ${source.observedPattern} |`).join('\n')}

## Remote Heads

| Branch | OID |
| --- | --- |
${refRows}

## Open Pull Requests

| PR | Title | Head | Same repository |
| --- | --- | --- | --- |
${prRows}

## Blockers

| Category | Ref | Path | Detail |
| --- | --- | --- | --- |
${blockerRows}

## Checks

| Check | OK | Detail |
| --- | --- | --- |
${checkRows}
`)
}

async function main(): Promise<void> {
  const gitFetchPerformed = !env.OPENCLAUDE_GITHUB_PUBLIC_SURFACE_SKIP_FETCH
  if (gitFetchPerformed) {
    fetchRemoteTrackingRefs()
  }

  const repositoryFullName = repositoryFullNameFromRemote()
  if (!repositoryFullName) {
    throw new Error('Could not determine GitHub repository from origin remote')
  }

  const defaultBranch = discoverDefaultBranch()
  const remoteHeads = discoverRemoteHeads()
  const pullRequestDiscovery = await discoverOpenPullRequests(repositoryFullName)
  const refScans = remoteHeads.map((head) => scanRef(head.name))
  const report = analyzePublicGithubSurface({
    defaultBranch,
    remoteHeads,
    openPullRequests: pullRequestDiscovery.pullRequests,
    refScans,
    discovery: {
      gitFetchPerformed,
      remoteHeadDiscovery: 'git_ls_remote',
      openPullRequestDiscovery: pullRequestDiscovery.discovery,
      openPullRequestDiscoveryError: pullRequestDiscovery.error,
    },
  })
  writeReports(report)

  for (const item of report.evidenceChecks) {
    console.log(`${item.ok ? 'PASS' : 'FAIL'}: ${item.label} (${item.detail})`)
  }
  console.log('')
  console.log(`RESULT: ${report.blockerCount === 0 ? 'PASS' : 'FAIL'}`)
  console.log(`remote_head_count=${report.remoteHeadCount}`)
  console.log(`open_pull_request_count=${report.openPullRequestCount}`)
  console.log(`blocker_count=${report.blockerCount}`)
  console.log(`status=${report.status}`)
  console.log(`provider_calls_performed=${report.providerCallsPerformed.length}`)
  console.log(`live_model_calls_performed=${report.liveModelCallsPerformed.length}`)
  console.log(`protected_actions_executed=${report.protectedActionsExecuted.length}`)

  if (report.blockerCount > 0 || !report.evidenceChecks.every((item) => item.ok)) {
    exit(1)
  }
}

if (import.meta.main) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error))
    exit(1)
  })
}
