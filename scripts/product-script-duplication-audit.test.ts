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
    writeFileSync(join(repo, 'scripts', 'product-script-duplication-audit.ts'), helperSource)

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
      helperOccurrenceBaselines: Record<string, number>
      duplicateHelperClusterCount: number
      duplicateHelperClusterBaseline: number
      primarySourceInputs: Array<{
        sourceType: string
        sourceProject: string
        sourceUrl: string
      }>
      auditChecks: Array<{
        label: string
        ok: boolean
      }>
      duplicateHelperClusters: Array<{
        helperName: string
        occurrenceCount: number
        files: Array<{ path: string; line: number }>
      }>
    }
    expect(report.sourceProductScriptCount).toBe(3)
    expect(report.helperOccurrenceCounts.check).toBe(2)
    expect(report.helperOccurrenceCounts.readText).toBe(2)
    expect(report.helperOccurrenceBaselines.check).toBeGreaterThanOrEqual(report.helperOccurrenceCounts.check)
    expect(report.helperOccurrenceBaselines.sha256Text).toBeLessThanOrEqual(1)
    expect(report.duplicateHelperClusterBaseline).toBeGreaterThanOrEqual(report.duplicateHelperClusterCount)
    expect(report.primarySourceInputs.map((source) => source.sourceType)).toEqual(
      expect.arrayContaining(['oss_tool', 'research_survey', 'patent']),
    )
    expect(report.primarySourceInputs.map((source) => source.sourceProject)).toEqual(
      expect.arrayContaining([
        'jscpd',
        'Knip',
        'dependency-cruiser',
        'Roy and Cordy clone detection survey',
        'US11662998B2 duplicate code pattern patent',
        'US7904892B2 dependency graph cycle patent',
      ]),
    )
    expect(
      report.auditChecks.some(
        (item) => item.label === 'primary sources include OSS, research, and patent inputs' && item.ok,
      ),
    ).toBe(true)

    const checkCluster = report.duplicateHelperClusters.find((cluster) => cluster.helperName === 'check')
    expect(checkCluster?.occurrenceCount).toBe(2)
    expect(checkCluster?.files.map((file) => file.path).sort()).toEqual([
      'scripts/product-alpha.ts',
      'scripts/product-beta.ts',
    ])
  }, 30000)
})
