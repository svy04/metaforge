import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'

const root = join(__dirname, '..')
const scriptPath = join(__dirname, 'product-script-duplication-audit.ts')
const packageJsonPath = join(root, 'package.json')
const jscpdConfigPath = join(root, '.jscpd.json')
const qualityGatePath = join(root, 'scripts', 'product-quality-gate.ts')
const evidenceManifestPath = join(root, 'scripts', 'product-evidence-manifest.ts')
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

  test('records jscpd token-clone ratchet evidence for product scripts without cleanup claims', () => {
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8')) as {
      devDependencies: Record<string, string>
    }
    const jscpdConfig = JSON.parse(readFileSync(jscpdConfigPath, 'utf8')) as {
      path: string[]
      pattern: string
      reporters: string[]
      minLines: number
      minTokens: number
      format: string[]
    }

    expect(packageJson.devDependencies.jscpd).toBe('5.0.9')
    expect(jscpdConfig.path).toEqual(['scripts'])
    expect(jscpdConfig.pattern).toBe('**/product-*.ts')
    expect(jscpdConfig.reporters).toContain('json')
    expect(jscpdConfig.minLines).toBe(20)
    expect(jscpdConfig.minTokens).toBe(120)
    expect(jscpdConfig.format).toContain('typescript')

    const result = runAudit(root)
    expect(result.status, result.stderr || result.stdout).toBe(0)

    const reportText = readFileSync(
      join(root, 'docs', 'product-quality', 'script-duplication-audit-report.json'),
      'utf8',
    )
    expect(reportText).not.toContain(root)

    const report = JSON.parse(reportText) as {
      helperOccurrenceCounts: Record<string, number>
      helperOccurrenceBaselines: Record<string, number>
      jscpdEnabled: boolean
      jscpdVersion: string
      jscpdConfigPath: string
      jscpdCommand: {
        name: string
        command: string[]
        exitCode: number | null
        passed: boolean
        missingSubstrings: string[]
      }
      jscpdCloneCount: number
      jscpdCloneBaseline: number
      jscpdDuplicatedLines: number
      jscpdDuplicatedLinesBaseline: number
      jscpdDuplicatedTokens: number
      jscpdDuplicatedTokensBaseline: number
      jscpdDuplicatedPercentage: number
      jscpdDuplicatedPercentageBaseline: number
      jscpdReportSha256: string
      jscpdTopClonePairs: Array<{
        firstFile: string
        secondFile: string
        lines: number
        tokens: number
      }>
      publicReadinessClaimAllowed: boolean
      refactorCompletionClaimAllowed: boolean
      auditChecks: Array<{
        label: string
        ok: boolean
      }>
    }

    expect(report.helperOccurrenceCounts.check).toBe(72)
    expect(report.helperOccurrenceCounts.readText).toBe(35)
    expect(report.helperOccurrenceBaselines.check).toBe(72)
    expect(report.helperOccurrenceBaselines.readText).toBe(35)
    expect(report.jscpdEnabled).toBe(true)
    expect(report.jscpdVersion).toContain('5.0.9')
    expect(report.jscpdConfigPath).toBe('.jscpd.json')
    expect(report.jscpdCommand.name).toBe('jscpd_product_scripts_json')
    expect(report.jscpdCommand.command).toContain('jscpd')
    expect(report.jscpdCommand.command).toContain('--config')
    expect(report.jscpdCommand.command).toContain('.jscpd.json')
    expect(report.jscpdCommand.command).toContain('--reporters')
    expect(report.jscpdCommand.command).toContain('json')
    expect(report.jscpdCommand.exitCode).toBe(0)
    expect(report.jscpdCommand.passed).toBe(true)
    expect(report.jscpdCommand.missingSubstrings).toEqual([])
    expect(report.jscpdCloneCount).toBeGreaterThan(0)
    expect(report.jscpdCloneBaseline).toBe(26)
    expect(report.jscpdDuplicatedLinesBaseline).toBe(774)
    expect(report.jscpdDuplicatedTokensBaseline).toBe(4790)
    expect(report.jscpdDuplicatedPercentageBaseline).toBe(1.9)
    expect(report.jscpdCloneCount).toBeLessThanOrEqual(report.jscpdCloneBaseline)
    expect(report.jscpdDuplicatedLines).toBeLessThanOrEqual(report.jscpdDuplicatedLinesBaseline)
    expect(report.jscpdDuplicatedTokens).toBeLessThanOrEqual(report.jscpdDuplicatedTokensBaseline)
    expect(report.jscpdDuplicatedPercentage).toBeLessThanOrEqual(report.jscpdDuplicatedPercentageBaseline)
    expect(report.jscpdReportSha256).toHaveLength(64)
    expect(report.jscpdTopClonePairs.length).toBeGreaterThan(0)
    expect(report.jscpdTopClonePairs.every((pair) => !pair.firstFile.includes('\\') && !pair.secondFile.includes('\\'))).toBe(true)
    expect(report.publicReadinessClaimAllowed).toBe(false)
    expect(report.refactorCompletionClaimAllowed).toBe(false)
    expect(
      report.auditChecks.some((item) => item.label === 'jscpd token clone count does not exceed baseline' && item.ok),
    ).toBe(true)
  }, 120000)

  test('wires script duplication evidence into aggregate product quality and manifest surfaces', () => {
    const qualityGate = readFileSync(qualityGatePath, 'utf8')
    const evidenceManifest = readFileSync(evidenceManifestPath, 'utf8')

    expect(qualityGate).toContain('ScriptDuplicationAuditReport')
    expect(qualityGate).toContain('script duplication jscpd ratchet does not exceed baseline')
    expect(qualityGate).toContain('script_duplication_jscpd_clones=')
    expect(evidenceManifest).toContain('.jscpd.json')
    expect(evidenceManifest).toContain('docs/product-quality/script-duplication-audit-report.json')
    expect(evidenceManifest).toContain('docs/product-quality/script-duplication-audit-report.md')
  })
})
