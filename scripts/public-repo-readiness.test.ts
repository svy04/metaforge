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
})
