import { describe, expect, test } from 'bun:test'
import { existsSync, mkdtempSync, rmSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
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

function readTextFrom(basePath: string, relativePath: string): string {
  return readFileSync(join(basePath, relativePath), 'utf8')
}

function validateKoreanReadmeRoute(basePath: string): string[] {
  const issues: string[] = []
  const readme = readTextFrom(basePath, 'README.md')
  const koreanLink = readme.match(/\[한국어\]\(([^)]+)\)/)

  if (!koreanLink) {
    issues.push('README missing Korean README link')
    return issues
  }

  if (koreanLink[1] !== 'README.ko.md') {
    issues.push('README Korean link must be repo-relative README.ko.md')
    return issues
  }

  const koreanReadmePath = join(basePath, 'README.ko.md')
  if (!existsSync(koreanReadmePath)) {
    issues.push('README.ko.md target is missing')
    return issues
  }

  const koreanReadme = readTextFrom(basePath, 'README.ko.md')
  if (!koreanReadme.includes('Meta/MFH/Orchestra')) {
    issues.push('README.ko.md missing Meta/MFH/Orchestra framing')
  }
  if (!koreanReadme.includes('OpenClaude')) {
    issues.push('README.ko.md missing OpenClaude substrate wording')
  }
  if (!koreanReadme.includes('검증')) {
    issues.push('README.ko.md missing Korean verification wording')
  }

  return issues
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
    expect(validateKoreanReadmeRoute(root)).toEqual([])
  })

  test('Korean README route contract rejects broken public navigation fixtures', () => {
    const fixtureRoot = mkdtempSync(join(tmpdir(), 'metaforge-readme-route-'))
    try {
      writeFileSync(join(fixtureRoot, 'README.md'), '[한국어](README.ko.md)\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md target is missing')

      writeFileSync(join(fixtureRoot, 'README.ko.md'), 'OpenClaude only\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md missing Meta/MFH/Orchestra framing')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README.ko.md missing Korean verification wording')

      writeFileSync(join(fixtureRoot, 'README.md'), '[한국어](C:/Users/example/README.ko.md)\n')
      expect(validateKoreanReadmeRoute(fixtureRoot)).toContain('README Korean link must be repo-relative README.ko.md')
    } finally {
      rmSync(fixtureRoot, { recursive: true, force: true })
    }
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
