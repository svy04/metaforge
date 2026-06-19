import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')
const reportPath = join(root, 'docs/product-quality/dead-export-candidates-report.json')
const triagePath = join(root, 'docs/product-quality/dead-export-candidate-triage.json')
const packageJsonPath = join(root, 'package.json')
const qualityGatePath = join(root, 'scripts/product-quality-gate.ts')
const evidenceManifestPath = join(root, 'scripts/product-evidence-manifest.ts')

type DeadExportCandidatesReport = {
  mode: string
  knipVersion: string
  providerCallsPerformed: unknown[]
  liveModelCallsPerformed: unknown[]
  externalCallsPerformed: unknown[]
  protectedActionsExecuted: unknown[]
  candidateFileCount: number
  candidateUnusedExportCount: number
  candidateUnusedTypeCount: number
  candidateDuplicateExportCount: number
  candidateFileBaseline: number
  candidateUnusedExportBaseline: number
  candidateUnusedTypeBaseline: number
  candidateDuplicateExportBaseline: number
  sampleCandidateFiles: Array<{
    file: string
    sampleExports: string[]
    sampleTypes: string[]
  }>
  triageLedgerPath: string
  triageRecordCount: number
  triageCurrentCandidateCount: number
  triageActionCounts: Record<string, number>
  triageRecords: Array<{
    file: string
    symbol: string
    kind: string
    action: string
    currentCandidate: boolean
    rationale: string
    guardrail: string
    resolvedEvidence?: {
      state: string
      validationCommands: string[]
      evidencePaths: string[]
      checkedBehaviors: string[]
      claimBoundary: string
    }
  }>
  removedCandidateRatchets: Array<{
    file: string
    symbol: string
    kind: string
    currentCandidate: boolean
    guardrail: string
  }>
  deletionClaimAllowed: boolean
  cleanupCompletionClaimAllowed: boolean
  publicReadinessClaimAllowed: boolean
  knipCommands: Array<{
    name: string
    command: string[]
    exitCode: number | null
    passed: boolean
    missingSubstrings: string[]
    stdoutPreview: string[]
  }>
  primarySourceInputs: Array<{
    sourceProject: string
    sourceUrl: string
  }>
  deadExportChecks: Array<{
    label: string
    ok: boolean
  }>
}

function runDeadExportGate(): DeadExportCandidatesReport {
  const result = spawnSync('bun', ['run', 'product:dead-export-candidates'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  expect(result.status, `${result.stdout}\n${result.stderr}`).toBe(0)
  return JSON.parse(readFileSync(reportPath, 'utf8')) as DeadExportCandidatesReport
}

describe('product dead export candidate gate', () => {
  test('records Knip no-autofix candidate evidence without cleanup claims', () => {
    const report = runDeadExportGate()
    const reportText = readFileSync(reportPath, 'utf8')

    expect(reportText).not.toContain(root)
    expect(report.mode).toBe('local_no_provider_dead_export_candidate_gate')
    expect(report.knipVersion).toMatch(/^\d+\.\d+\.\d+/)
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.protectedActionsExecuted).toEqual([])
    expect(report.candidateFileCount).toBeGreaterThan(0)
    expect(report.candidateUnusedExportCount).toBeGreaterThan(0)
    expect(report.candidateUnusedTypeCount).toBeLessThanOrEqual(364)
    expect(report.candidateUnusedExportCount).toBeLessThanOrEqual(1399)
    expect(
      report.sampleCandidateFiles.find((item) => item.file === 'src/utils/providerDiscovery.ts')?.sampleExports ?? [],
    ).not.toContain('getOpenAICompatibleModelsBaseUrl')
    expect(
      report.sampleCandidateFiles.find((item) => item.file === 'src/bridge/sessionRunner.ts')?.sampleTypes ?? [],
    ).not.toContain('PermissionRequest')
    expect(
      report.sampleCandidateFiles.find((item) => item.file === 'src/utils/providerProfile.ts')?.sampleExports ?? [],
    ).not.toContain('buildMiniMaxProfileEnv')
    expect(report.candidateFileBaseline).toBeGreaterThanOrEqual(report.candidateFileCount)
    expect(report.candidateUnusedExportBaseline).toBeGreaterThanOrEqual(report.candidateUnusedExportCount)
    expect(report.candidateUnusedTypeBaseline).toBeGreaterThanOrEqual(report.candidateUnusedTypeCount)
    expect(report.candidateDuplicateExportBaseline).toBeGreaterThanOrEqual(report.candidateDuplicateExportCount)
    expect(report.triageLedgerPath).toBe('docs/product-quality/dead-export-candidate-triage.json')
    expect(report.triageRecordCount).toBeGreaterThanOrEqual(3)
    expect(report.triageCurrentCandidateCount).toBe(report.triageRecordCount)
    expect(report.triageActionCounts['runtime_guarded']).toBeGreaterThanOrEqual(2)
    expect(report.triageActionCounts['needs_runtime_guard'] ?? 0).toBe(0)
    expect(report.triageActionCounts['review_for_removal']).toBeGreaterThanOrEqual(1)
    expect(report.triageRecords.every((item) => item.currentCandidate)).toBe(true)
    expect(report.triageRecords.every((item) => item.rationale.length > 20 && item.guardrail.length > 20)).toBe(true)
    const credentialRuntimeGuardCommand =
      'bun test src/services/api/providerConfig.runtimeCodexCredentials.test.ts src/utils/geminiCredentials.test.ts'
    const runtimeGuardedCredentialRecords = report.triageRecords.filter((item) => (
      item.symbol === 'resolveStoredCodexCredentials' ||
      item.symbol === 'clearGeminiAccessToken'
    ))
    expect(runtimeGuardedCredentialRecords).toHaveLength(2)
    expect(runtimeGuardedCredentialRecords.every((item) => item.action === 'runtime_guarded')).toBe(true)
    expect(runtimeGuardedCredentialRecords.every((item) => item.resolvedEvidence?.state === 'resolved_with_runtime_guard')).toBe(true)
    expect(runtimeGuardedCredentialRecords.every((item) => (
      item.resolvedEvidence?.validationCommands.includes(credentialRuntimeGuardCommand)
    ))).toBe(true)
    expect(runtimeGuardedCredentialRecords.flatMap((item) => item.resolvedEvidence?.evidencePaths ?? [])).toEqual(
      expect.arrayContaining([
        'src/services/api/providerConfig.runtimeCodexCredentials.test.ts',
        'src/utils/geminiCredentials.test.ts',
      ]),
    )
    expect(report.removedCandidateRatchets.length).toBeGreaterThanOrEqual(4)
    expect(report.removedCandidateRatchets.every((item) => item.currentCandidate)).toBe(false)
    expect(
      report.removedCandidateRatchets.find((item) => (
        item.file === 'src/projectOnboardingState.ts' &&
        item.kind === 'export' &&
        item.symbol === 'isProjectOnboardingComplete'
      ))?.currentCandidate,
    ).toBe(false)
    expect(report.deletionClaimAllowed).toBe(false)
    expect(report.cleanupCompletionClaimAllowed).toBe(false)
    expect(report.publicReadinessClaimAllowed).toBe(false)

    const command = report.knipCommands.find((item) => item.name === 'knip_exports_json')
    expect(command?.command).toContain('knip')
    expect(command?.command).toContain('--config')
    expect(command?.command).toContain('knip.jsonc')
    expect(command?.command).toContain('--exports')
    expect(command?.command).toContain('--reporter')
    expect(command?.command).toContain('json')
    expect(command?.exitCode).toBe(0)
    expect(command?.passed).toBe(true)
    expect(command?.missingSubstrings).toEqual([])
    expect(command?.stdoutPreview.every((line) => line.length <= 260)).toBe(true)
    expect(report.primarySourceInputs.map((source) => source.sourceProject)).toEqual(
      expect.arrayContaining(['Knip', 'fallow']),
    )
    expect(report.deadExportChecks.every((item) => item.ok)).toBe(true)
  }, 120000)

  test('wires dead export candidate evidence into the public quality surface', () => {
    const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8')) as {
      scripts: Record<string, string>
      devDependencies: Record<string, string>
    }
    const qualityGate = readFileSync(qualityGatePath, 'utf8')
    const evidenceManifest = readFileSync(evidenceManifestPath, 'utf8')

    expect(packageJson.devDependencies.knip).toBeDefined()
    expect(packageJson.scripts['product:dead-export-candidates']).toBe('bun run scripts/product-dead-export-candidates.ts')
    expect(packageJson.scripts['product:quality']).toContain('bun run product:dead-export-candidates')
    expect(qualityGate).toContain('DeadExportCandidatesReport')
    expect(qualityGate).toContain('dead export candidate commands pass')
    expect(qualityGate).toContain('dead export candidate triage entries remain current')
    expect(qualityGate).toContain('dead export candidate removed ratchets remain absent')
    expect(qualityGate).toContain('dead_export_candidate_unused_exports=')
    expect(evidenceManifest).toContain('docs/product-quality/dead-export-candidates-report.json')
    expect(evidenceManifest).toContain('docs/product-quality/dead-export-candidates-report.md')
    expect(evidenceManifest).toContain('docs/product-quality/dead-export-candidate-triage.json')
    expect(readFileSync(triagePath, 'utf8')).toContain('runtime_guarded')
    expect(readFileSync(triagePath, 'utf8')).toContain('resolved_with_runtime_guard')
  })
})
