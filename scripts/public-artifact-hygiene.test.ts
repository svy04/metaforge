import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'

const scriptPath = join(__dirname, 'public-artifact-hygiene.ts')
const tempDirs: string[] = []
const windowsPrivatePath = ['C:', 'Users', 'fixture-owner', 'Desktop', 'private-space', 'openclaude-0.6.0'].join('\\')
const secretLikePlaceholder = ['OPENAI_API_KEY=', 'sk', 'openai', 'placeholder'].join('-')

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-public-hygiene-'))
  tempDirs.push(dir)
  return dir
}

function runHygiene(cwd: string) {
  return spawnSync('bun', ['run', scriptPath], {
    cwd,
    encoding: 'utf8',
    shell: false,
  })
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('public artifact hygiene scanner', () => {
  test('scans root environment examples for local path disclosure', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, '.env.example'),
      `OPENCLAUDE_HOME=${windowsPrivatePath}`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.env.example')
  })

  test('rejects scanner-unfriendly fake API key placeholders in public examples', () => {
    const repo = makeTempRepo()
    writeFileSync(join(repo, '.env.example'), `${secretLikePlaceholder}\n`)

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('.env.example')
  })

  test('rejects private workspace placeholders in public docs', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'README.md'),
      'Use <private-workspace>/meta/CLAUDE.md as the authority file.\n',
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('README.md')
  })

  test('scans the root license for local path disclosure', () => {
    const repo = makeTempRepo()
    writeFileSync(
      join(repo, 'LICENSE'),
      `Derived runtime note copied from ${windowsPrivatePath}\n`,
    )

    const result = runHygiene(repo)

    expect(result.status).not.toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('LICENSE')
  })
})
