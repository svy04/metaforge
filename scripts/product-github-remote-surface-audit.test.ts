import { describe, expect, test } from 'bun:test'
import { analyzePublicGithubSurface, buildAuditJsonl } from './product-github-remote-surface-audit'

describe('GitHub public surface analysis', () => {
  test('remote forbidden-pattern matcher covers generic local paths and token shapes', async () => {
    const audit = await import('./product-github-remote-surface-audit')
    const matchesForbiddenPattern = audit.matchesRemoteForbiddenPattern as ((text: string) => boolean) | undefined

    expect(typeof matchesForbiddenPattern).toBe('function')

    const windowsHome = ['C:', 'Users', 'private-owner'].join('\\')
    const windowsHomeWithSpaces = ['C:', 'Users', 'private owner'].join('\\')
    const posixHomeWithSpaces = ['', 'Users', 'private owner'].join('/')
    const relativeHomeWithSpaces = ['Users', 'private owner'].join('/')
    const forbiddenSamples = [
      ['cd', `${windowsHome}\\Desktop\\private-run\\AGENTS.md`].join(' '),
      ['cd', `${windowsHomeWithSpaces}\\Desktop\\private run\\AGENTS.md`].join(' '),
      ['type', `${windowsHome}\\Documents\\private run\\session.log`].join(' '),
      ['cat', `${windowsHome}\\AppData\\Local\\hermes\\auth.json`].join(' '),
      ['type', `${windowsHome}\\Documents\\private-run\\session.log`].join(' '),
      `Example leak: ${windowsHome}\\Desktop\\private-run\\trace.md`,
      ['cat', `${posixHomeWithSpaces}/Desktop/private run/trace.json`].join(' '),
      ['Example leak:', `${['', 'Users', 'real owner'].join('/')}/Desktop/private run/trace.json`].join(' '),
      ['cat', `${relativeHomeWithSpaces}/Documents/private run/notes.md`].join(' '),
      ['GITHUB_TOKEN=', 'ghp_', 'A'.repeat(36)].join(''),
      ['GITHUB_PAT=', 'github', '_pat_', 'A'.repeat(40)].join(''),
      ['AWS_ACCESS_KEY_ID=', 'AKIA', 'A'.repeat(16)].join(''),
      ['SLACK_BOT_TOKEN=', 'xoxb', '-', 'A'.repeat(16)].join(''),
    ]

    for (const sample of forbiddenSamples) {
      expect(matchesForbiddenPattern?.(sample), sample).toBe(true)
    }

    expect(matchesForbiddenPattern?.(['e.g.', ['C:', 'Users', 'Example', 'Documents', 'fixture'].join('\\')].join(' '))).toBe(false)
    expect(matchesForbiddenPattern?.(['e.g.', ['C:', 'Users', 'Example User', 'Documents', 'fixture with spaces'].join('\\')].join(' '))).toBe(false)
  })

  test('remote forbidden-pattern matcher covers local-hygiene-only public breadcrumbs', async () => {
    const audit = await import('./product-github-remote-surface-audit')
    const matchesForbiddenPattern = audit.matchesRemoteForbiddenPattern as ((text: string) => boolean) | undefined
    const forbiddenPatternId = audit.remoteForbiddenPatternId as ((text: string, path?: string) => string | null) | undefined

    expect(typeof matchesForbiddenPattern).toBe('function')
    expect(typeof forbiddenPatternId).toBe('function')

    const forbiddenSamples = [
      '<environment_context>',
      '.codex/memories/session-note.md',
      '<private-codex-memory-dir>',
      '<private-agent-skill-dir>',
      'OpenClaude Orchestrator Memory',
      'AGENTS.md instructions for C:',
      ['OPENAI_API_KEY=', 'sk', '-openai-placeholder'].join(''),
    ]

    for (const sample of forbiddenSamples) {
      expect(matchesForbiddenPattern?.(sample), sample).toBe(true)
    }

    expect(forbiddenPatternId?.('<environment_context>', 'docs/public-note.md')).toBe('public_artifact_hygiene_pattern')
    expect(forbiddenPatternId?.('<private-codex-memory-dir>', 'README.md')).toBe('public_artifact_hygiene_pattern')
    expect(forbiddenPatternId?.('<private-agent-skill-dir>', 'SUPPORT.md')).toBe('public_artifact_hygiene_pattern')
    expect(forbiddenPatternId?.('OpenClaude Orchestrator Memory', 'AGENTS.md')).toBe('public_artifact_hygiene_pattern')
    expect(forbiddenPatternId?.('<environment_context>', 'scripts/public-artifact-hygiene.test.ts')).toBe(null)
  })

  test('blocks stale remote branches and disclosure findings on public refs', () => {
    const report = analyzePublicGithubSurface({
      defaultBranch: 'main',
      remoteHeads: [
        { name: 'main', oid: 'a'.repeat(40) },
        { name: 'codex/stale-proof-branch', oid: 'b'.repeat(40) },
      ],
      openPullRequests: [],
      refScans: [
        {
          refName: 'codex/stale-proof-branch',
          patternFindings: [
            {
              path: 'PLAYBOOK.md',
              line: 135,
              patternId: 'local_windows_user_path',
              text: ['cd', ['C:', 'Users', 'Example', 'Documents', 'private-repo'].join('\\')].join(' '),
            },
          ],
          treeFindings: [
            {
              path: 'bin/.playwright-mcp/page.yml',
              patternId: 'playwright_mcp_capture',
            },
          ],
        },
      ],
      discovery: {
        gitFetchPerformed: true,
        remoteHeadDiscovery: 'git_ls_remote',
        openPullRequestDiscovery: 'gh_cli',
      },
    })

    expect(report.remoteHeadCount).toBe(2)
    expect(report.openPullRequestCount).toBe(0)
    expect(report.blockerCount).toBe(3)
    expect(report.status).toBe('blocked_public_github_surface_findings')
    expect(report.blockers.map((blocker) => blocker.category)).toEqual([
      'unexpected_remote_branch',
      'forbidden_pattern',
      'browser_capture_artifact',
    ])
  })

  test('allows clean non-default branches that are attached to open same-repo PRs', () => {
    const report = analyzePublicGithubSurface({
      defaultBranch: 'main',
      remoteHeads: [
        { name: 'main', oid: 'a'.repeat(40) },
        { name: 'codex/clean-public-surface', oid: 'c'.repeat(40) },
      ],
      openPullRequests: [
        {
          number: 42,
          title: 'Clean public surface',
          url: 'https://github.com/svy04/metaforge/pull/42',
          headRefName: 'codex/clean-public-surface',
          isSameRepository: true,
        },
      ],
      refScans: [
        {
          refName: 'codex/clean-public-surface',
          patternFindings: [],
          treeFindings: [],
        },
      ],
      discovery: {
        gitFetchPerformed: true,
        remoteHeadDiscovery: 'git_ls_remote',
        openPullRequestDiscovery: 'gh_cli',
      },
    })

    expect(report.blockerCount).toBe(0)
    expect(report.status).toBe('no_public_github_surface_findings_detected')
    expect(report.allowedOpenPrHeadBranches).toEqual(['codex/clean-public-surface'])
  })

  test('writes a nonempty JSONL evidence record when no blockers exist', () => {
    const report = analyzePublicGithubSurface({
      defaultBranch: 'main',
      remoteHeads: [{ name: 'main', oid: 'a'.repeat(40) }],
      openPullRequests: [],
      refScans: [{ refName: 'main', patternFindings: [], treeFindings: [] }],
      discovery: {
        gitFetchPerformed: true,
        remoteHeadDiscovery: 'git_ls_remote',
        openPullRequestDiscovery: 'gh_cli',
      },
    })

    const jsonl = buildAuditJsonl(report)

    expect(jsonl.trim().length).toBeGreaterThan(0)
    expect(JSON.parse(jsonl.trim())).toMatchObject({
      kind: 'github_remote_surface_audit_summary',
      status: 'no_public_github_surface_findings_detected',
      blockerCount: 0,
    })
  })
})
