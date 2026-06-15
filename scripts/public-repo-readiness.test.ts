import { describe, expect, test } from 'bun:test'
import { existsSync, readFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')

function readRepoText(path: string): string {
  return readFileSync(join(root, path), 'utf8')
}

function privateLocalPathNeedles(): string[] {
  return [
    `C:${'\\\\'}Users`,
    `C:${'/'}Users`,
    ['내 순수', ' 재미'].join(''),
  ]
}

describe('public repository readiness surfaces', () => {
  test('AGENTS.md is public-facing guidance, not a private memory dump', () => {
    const agents = readRepoText('AGENTS.md')
    const lineCount = agents.split(/\r?\n/).length

    expect(lineCount).toBeLessThanOrEqual(220)
    expect(agents).toContain('Meta/MFH/Orchestra')
    expect(agents).toContain('OpenClaude runtime')
    expect(agents).not.toContain('OpenClaude Orchestrator Memory')
    expect(agents).not.toMatch(/\b(gpt-5\.1|sonnet 4\.5|Opus 4\.7)\b/i)
    for (const needle of privateLocalPathNeedles()) {
      expect(agents).not.toContain(needle)
    }
  })

  test('README routes Korean readers to a maintained Korean README', () => {
    const readme = readRepoText('README.md')
    const koreanReadmePath = join(root, 'README.ko.md')

    expect(readme).toMatch(/\[한국어\]\(README\.ko\.md\)/)
    expect(existsSync(koreanReadmePath)).toBe(true)

    const koreanReadme = readRepoText('README.ko.md')
    expect(koreanReadme).toContain('Meta/MFH/Orchestra')
    expect(koreanReadme).toContain('OpenClaude')
    expect(koreanReadme).toContain('검증')
  })

  test('advanced setup uses the current public repository source URL', () => {
    const advancedSetup = readRepoText('docs/advanced-setup.md')

    expect(advancedSetup).toContain('https://github.com/svy04/metaforge.git')
    expect(advancedSetup).not.toContain('node.gitlawb.com')
    expect(advancedSetup).not.toContain('Gitlawb/openclaude')
  })

  test('release workflow is a public boundary gate, not an active publish pipeline', () => {
    const releaseWorkflow = readRepoText('.github/workflows/release.yml')

    expect(releaseWorkflow).toContain('Release Boundary')
    expect(releaseWorkflow).toContain('No npm publish, Docker push, or release creation is authorized')
    expect(releaseWorkflow).not.toMatch(/^\s*run:\s*npm publish\b/m)
    expect(releaseWorkflow).not.toMatch(/docker\/build-push-action/)
    expect(releaseWorkflow).not.toMatch(/release-please-action/)
    expect(releaseWorkflow).not.toContain('Gitlawb/openclaude')
  })

  test('README states runtime wiring honestly', () => {
    const readme = readRepoText('README.md')

    expect(readme).toContain('Orchestra is the runtime-wired layer in this package today')
    expect(readme).toContain('Meta and MFH are governance, schema, and evidence-gate surfaces')
    expect(readme).toContain('AVF Influence Factory is a repo-local manual artifact lane')
    expect(readme).not.toContain('Meta, MFH, and AVF are runtime-wired modules')
  })
})
