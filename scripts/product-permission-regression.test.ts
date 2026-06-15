import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')
const reportPath = join(root, 'docs/product-quality/permission-regression-fixtures.json')
const qualityGatePath = join(root, 'scripts/product-quality-gate.ts')

type BehavioralTestCommand = {
  name: string
  command: string[]
  exitCode: number | null
  passed: boolean
  requiredSubstrings: string[]
  missingSubstrings: string[]
  stdoutPreview: string[]
  stderrPreview: string[]
}

type PermissionRegressionReport = {
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  targetedTestFiles: string[]
  behavioralTestCommands?: BehavioralTestCommand[]
}

function runPermissionRegression(): PermissionRegressionReport {
  const result = spawnSync('bun', ['run', 'product:permission-regression'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
  return JSON.parse(readFileSync(reportPath, 'utf8')) as PermissionRegressionReport
}

describe('product permission regression evidence', () => {
  test('records a real no-provider targeted permission test command', () => {
    const report = runPermissionRegression()

    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.behavioralTestCommands?.length).toBeGreaterThanOrEqual(1)

    const command = report.behavioralTestCommands?.[0]
    expect(command?.name).toBe('targeted_permission_security_tests')
    expect(command?.command.join(' ')).toContain('bun test')
    for (const file of report.targetedTestFiles) {
      expect(command?.command).toContain(file)
    }
    expect(command?.passed).toBe(true)
    expect(command?.exitCode).toBe(0)
    expect(command?.missingSubstrings).toEqual([])
    expect(`${command?.stdoutPreview.join('\n')}\n${command?.stderrPreview.join('\n')}`).toContain('pass')
  })

  test('product quality gate requires behavioral permission command evidence', () => {
    const qualityGate = readFileSync(qualityGatePath, 'utf8')

    expect(qualityGate).toContain('behavioralTestCommands')
    expect(qualityGate).toContain('permission regression includes behavioral test command evidence')
    expect(qualityGate).toContain('permission regression behavioral commands pass')
  })
})
