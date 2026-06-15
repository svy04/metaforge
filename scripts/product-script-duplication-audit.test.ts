import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'

const root = join(__dirname, '..')
const scriptPath = join(__dirname, 'product-script-duplication-audit.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-script-dup-audit-'))
  tempDirs.push(dir)
  mkdirSync(join(dir, 'scripts'), { recursive: true })
  mkdirSync(join(dir, 'docs', 'product-quality'), { recursive: true })
  return dir
}

function runAudit(cwd: string) {
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

describe('product script duplication audit', () => {
  test('reports repeated helper clusters without leaking absolute temp paths', () => {
    const repo = makeTempRepo()
    const helperSource = `
type Check = { label: string; ok: boolean; detail: string }
function check(label: string, ok: boolean, detail: string): Check {
  return { label, ok, detail }
}
function readText(path: string): string {
  return path.trim()
}
`
    writeFileSync(join(repo, 'scripts', 'product-alpha.ts'), helperSource)
    writeFileSync(join(repo, 'scripts', 'product-beta.ts'), helperSource)
    writeFileSync(join(repo, 'scripts', 'product-gamma.ts'), 'export const gamma = true\n')

    const result = runAudit(repo)

    expect(result.status, result.stderr || result.stdout).toBe(0)
    expect(result.stdout).toContain('RESULT: PASS')

    const reportText = readFileSync(
      join(repo, 'docs', 'product-quality', 'script-duplication-audit-report.json'),
      'utf8',
    )
    expect(reportText).not.toContain(repo)

    const report = JSON.parse(reportText) as {
      sourceProductScriptCount: number
      helperOccurrenceCounts: Record<string, number>
      duplicateHelperClusters: Array<{
        helperName: string
        occurrenceCount: number
        files: Array<{ path: string; line: number }>
      }>
    }
    expect(report.sourceProductScriptCount).toBe(3)
    expect(report.helperOccurrenceCounts.check).toBe(2)
    expect(report.helperOccurrenceCounts.readText).toBe(2)

    const checkCluster = report.duplicateHelperClusters.find((cluster) => cluster.helperName === 'check')
    expect(checkCluster?.occurrenceCount).toBe(2)
    expect(checkCluster?.files.map((file) => file.path).sort()).toEqual([
      'scripts/product-alpha.ts',
      'scripts/product-beta.ts',
    ])
  })
})
