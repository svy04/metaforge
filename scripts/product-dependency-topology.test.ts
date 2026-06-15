import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')
const reportPath = join(root, 'docs/product-quality/dependency-topology-report.json')
const packageJsonPath = join(root, 'package.json')
const qualityGatePath = join(root, 'scripts/product-quality-gate.ts')
const evidenceManifestPath = join(root, 'scripts/product-evidence-manifest.ts')

type DependencyTopologyReport = {
  mode: string
  dependencyCruiserVersion: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  circularDependencyCount: number
  circularDependencyBaseline: number
  topologyCommands: Array<{
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  topologyChecks: Array<{
    label: string
    ok: boolean
  }>
}

function runTopologyGate(): DependencyTopologyReport {
  const result = spawnSync('bun', ['run', 'product:dependency-topology'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
  return JSON.parse(readFileSync(reportPath, 'utf8')) as DependencyTopologyReport
}

describe('product dependency topology gate', () => {
  test('records real dependency-cruiser no-provider topology evidence', () => {
    const report = runTopologyGate()
    const reportText = readFileSync(reportPath, 'utf8')

    expect(reportText).not.toContain(root)
    expect(report.mode).toBe('local_no_provider_dependency_topology_gate')
    expect(report.dependencyCruiserVersion).toMatch(/^\d+\.\d+\.\d+/)
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.protectedActionsExecuted).toEqual([])
    expect(report.circularDependencyCount).toBeGreaterThanOrEqual(0)
    expect(report.circularDependencyBaseline).toBeGreaterThanOrEqual(report.circularDependencyCount)
    expect(report.topologyCommands.length).toBeGreaterThanOrEqual(1)

    const command = report.topologyCommands[0]
    expect(command.name).toBe('dependency_cruiser_src_scripts')
    expect(command.command).toContain('depcruise')
    expect(command.command).toContain('--output-type')
    expect(command.command).toContain('json')
    expect(command.command).toContain('src')
    expect(command.command).toContain('scripts')
    expect(command.exitCode).toBe(0)
    expect(command.passed).toBe(true)
    expect(command.missingSubstrings).toEqual([])
    expect(report.primarySourceInputs.map((source) => source.sourceProject)).toEqual(
      expect.arrayContaining(['dependency-cruiser', 'US7904892B2 dependency graph cycle patent']),
    )
    expect(report.topologyChecks.every((item) => item.ok)).toBe(true)
  }, 120000)

  test('wires dependency topology evidence into the public quality surface', () => {
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8')) as {
      scripts: Record<string, string>
      devDependencies: Record<string, string>
    }
    const qualityGate = readFileSync(qualityGatePath, 'utf8')
    const evidenceManifest = readFileSync(evidenceManifestPath, 'utf8')

    expect(packageJson.devDependencies['dependency-cruiser']).toBeDefined()
    expect(packageJson.scripts['product:dependency-topology']).toBe('bun run scripts/product-dependency-topology.ts')
    expect(packageJson.scripts['product:quality']).toContain('bun run product:dependency-topology')
    expect(qualityGate).toContain('DependencyTopologyReport')
    expect(qualityGate).toContain('dependency topology commands pass')
    expect(qualityGate).toContain('dependency_topology_cycles=')
    expect(evidenceManifest).toContain('docs/product-quality/dependency-topology-report.json')
    expect(evidenceManifest).toContain('docs/product-quality/dependency-topology-report.md')
  })
})
