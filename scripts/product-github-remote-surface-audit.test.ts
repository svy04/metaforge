import { describe, expect, test } from 'bun:test'
import { analyzePublicGithubSurface, buildAuditJsonl } from './product-github-remote-surface-audit'

describe('GitHub public surface analysis', () => {
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
              text: 'cd C:\\Users\\Example\\Documents\\private-repo',
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
        openPullRequestDiscovery: 'github_pr_api',
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
        openPullRequestDiscovery: 'github_pr_api',
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
