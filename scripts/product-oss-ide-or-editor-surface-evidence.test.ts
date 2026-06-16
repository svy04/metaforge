import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join, resolve } from 'node:path'

const root = process.cwd()
const scriptPath = resolve(root, 'scripts/product-oss-ide-or-editor-surface-evidence.ts')
const tempDirs: string[] = []

const noClaims = {
  providerCallsPerformed: [],
  liveModelCallsPerformed: [],
  externalCallsPerformed: [],
  protectedActionsExecuted: [],
  extensionAvailabilityClaimAllowed: false,
  publicComparisonClaimAllowed: false,
  superiorityClaimAllowed: false,
  releaseReadinessClaimAllowed: false,
  productionReadinessClaimAllowed: false,
  publicReadinessClaimAllowed: false,
  externalValidationClaimAllowed: false,
  autonomousReliabilityClaimAllowed: false,
}

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-oss-ide-evidence-'))
  tempDirs.push(dir)
  return dir
}

function writeText(rootDir: string, path: string, value: string): void {
  const absolutePath = join(rootDir, path)
  mkdirSync(dirname(absolutePath), { recursive: true })
  writeFileSync(absolutePath, value)
}

function writeJson(rootDir: string, path: string, value: Record<string, any>): void {
  writeText(rootDir, path, `${JSON.stringify(value, null, 2)}\n`)
}

function writeFixture(rootDir: string): void {
  writeJson(rootDir, 'package.json', {
    scripts: {
      'product:oss-ide-or-editor-surface-evidence': 'bun run scripts/product-oss-ide-or-editor-surface-evidence.ts',
    },
  })
  writeJson(rootDir, 'docs/product-quality/oss-comparison-readiness-index-report.json', {
    mode: 'local_no_provider_oss_comparison_readiness_index',
    readinessIndexRecords: [{
      indexKind: 'axis',
      indexKey: 'ide_or_editor_surface',
      readinessTier: 'safe_internal_absorption_priority',
      localEvidenceBackedCellCount: 7,
      axisNotYetAbsorbedCellCount: 3,
      metadataOnlyCellCount: 0,
    }],
    top10ProjectCount: 10,
    ...noClaims,
  })
  writeJson(rootDir, 'docs/product-quality/oss-benchmark-comparison-matrix-report.json', {
    mode: 'local_no_provider_oss_benchmark_comparison_matrix',
    top10ProjectCount: 10,
    matrixRecords: Array.from({ length: 10 }, (_, index) => ({
      rank: index + 1,
      fullName: `example/project-${index + 1}`,
      sourceUrl: `https://github.com/example/project-${index + 1}`,
      axis: 'ide_or_editor_surface',
      sourceReviewStatus: 'source_supported_candidate',
      benchmarkabilityStatus: index < 7
        ? 'local_internal_evidence_present_protected_gap_open'
        : 'axis_not_yet_absorbed',
      openClaudeEvidencePresentCount: index < 7 ? 11 : 0,
      protectedActionRequiredForNextStep: true,
      protectedActionExecuted: false,
      publicComparisonClaimAllowed: false,
      superiorityClaimAllowed: false,
      releaseReadinessClaimAllowed: false,
      productionReadinessClaimAllowed: false,
      publicReadinessClaimAllowed: false,
      externalValidationClaimAllowed: false,
      autonomousReliabilityClaimAllowed: false,
    })),
    ...noClaims,
  })
  writeJson(rootDir, 'docs/product-quality/public-claim-boundary-report.json', {
    unauthorizedPositiveClaimCount: 0,
    ...noClaims,
  })
  writeJson(rootDir, 'docs/product-quality/ide-extension-host-smoke-report.json', {
    hostRuntime: 'real_vscode_extension_development_host',
    codeExitCode: 0,
    vscodeStartupBlocked: false,
    realExtensionHostLaunched: true,
    extensionActivated: true,
    environmentBlockers: [],
    extensionAvailabilityClaimAllowed: false,
    hostSmokeChecks: [{ label: 'host ok', ok: true, detail: 'ok' }],
  })
  writeJson(rootDir, 'docs/product-quality/ide-extension-workbench-smoke-report.json', {
    hostRuntime: 'real_vscode_extension_development_host',
    codeExitCode: 0,
    vscodeStartupBlocked: false,
    realExtensionHostLaunched: true,
    extensionActivated: true,
    environmentBlockers: [],
    registeredTreeViewIds: ['openclaude.chatView', 'openclaude.traceEvidenceView'],
    executedViewCommandIds: [
      'openclaude.openChat',
      'openclaude.runSelection',
      'openclaude.openRuntimeDoctor',
      'openclaude.explainSelection',
    ],
    extensionAvailabilityClaimAllowed: false,
    workbenchSmokeChecks: [{ label: 'workbench ok', ok: true, detail: 'ok' }],
  })
  for (const path of [
    'docs/product-quality/ide-extension-surface-report.json',
    'docs/product-quality/ide-extension-scope-report.json',
    'docs/product-quality/ide-extension-manifest-smoke-report.json',
    'docs/product-quality/ide-extension-runtime-smoke-report.json',
    'docs/product-quality/vscode-update-boundary-report.json',
    'docs/product-quality/vscode-startup-diagnostics-report.json',
    'docs/product-quality/ide-extension-webview-render-smoke-report.json',
    'docs/product-quality/ide-extension-rendered-workbench-screenshot-report.json',
    'docs/product-quality/ide-extension-webview-interaction-smoke-report.json',
    'packages/openclaude-vscode/package.json',
    'packages/openclaude-vscode/dist/extension.js',
  ]) {
    writeText(rootDir, path, `${path}\n`)
  }
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('OSS IDE/editor surface evidence', () => {
  test('runs after local VS Code IDE evidence in the product quality pipeline', () => {
    const packageJson = JSON.parse(readFileSync(resolve(root, 'package.json'), 'utf8')) as {
      scripts: Record<string, string>
    }
    const qualityScript = packageJson.scripts['product:quality'] ?? ''
    const ossIdeIndex = qualityScript.indexOf('bun run product:oss-ide-or-editor-surface-evidence')
    const hostSmokeIndex = qualityScript.indexOf('bun run product:ide-extension-host-smoke')
    const workbenchSmokeIndex = qualityScript.indexOf('bun run product:ide-extension-workbench-smoke')
    const webviewInteractionIndex = qualityScript.indexOf('bun run product:ide-extension-webview-interaction-smoke')
    const releaseArtifactIndex = qualityScript.indexOf('bun run product:release-artifact')

    expect(ossIdeIndex).toBeGreaterThan(webviewInteractionIndex)
    expect(ossIdeIndex).toBeGreaterThan(hostSmokeIndex)
    expect(ossIdeIndex).toBeGreaterThan(workbenchSmokeIndex)
    expect(ossIdeIndex).toBeLessThan(releaseArtifactIndex)
  })

  test('accepts real VS Code host evidence while keeping availability claims blocked', () => {
    const repo = makeTempRepo()
    writeFixture(repo)

    const result = spawnSync('bun', ['run', scriptPath], {
      cwd: repo,
      encoding: 'utf8',
      shell: false,
    })

    expect(result.status, result.stderr || result.stdout).toBe(0)
    const report = JSON.parse(
      readFileSync(join(repo, 'docs/product-quality/oss-ide-or-editor-surface-evidence-report.json'), 'utf8'),
    ) as Record<string, any>
    const hostCheck = (report.evidenceChecks as Array<Record<string, any>>).find((item) =>
      String(item.label).includes('host smoke records local real-host command evidence'),
    )

    expect(report.hostSmokePass).toBe(true)
    expect(report.hostSmokeRealHostBlockedByVscodeCli).toBe(false)
    expect(report.extensionAvailabilityClaimAllowed).toBe(false)
    expect(hostCheck?.ok).toBe(true)
  })
})
