import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const scriptPath = join(__dirname, 'product-oss-axis-architecture-review.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-axis-review-'))
  tempDirs.push(dir)
  mkdirSync(join(dir, 'docs', 'product-quality'), { recursive: true })
  return dir
}

function writeGapReview(repo: string, absorptionAxes: string[]): void {
  const evidence = absorptionAxes.map((axis) => ({
    axis,
    currentLocalEvidence: [`docs/product-quality/${axis}-report.json`],
    unresolvedGap: `${axis} remains local-only.`,
    protectedBoundary: `${axis} claim expansion remains blocked.`,
  }))
  const gapRecord = {
    fullName: 'fixture/cli',
    sourceUrl: 'https://github.com/fixture/cli',
    targetStatus: 'prioritized_source_supported_target',
    priority: 'high',
    absorptionAxes,
    sourceSignals: ['terminal-cli'],
    openClaudeEvidence: evidence,
    safeInternalNextActions: ['keep this local'],
    protectedActionsStillRequired: ['none in this fixture'],
    forbiddenShortcuts: ['no public claims'],
    claimAllowed: false,
  }
  const report = {
    mode: 'local_no_provider_oss_architecture_gap_review',
    sourceTargetsReportPath: 'docs/product-quality/oss-architecture-absorption-targets-report.json',
    sourceReviewReportPath: 'docs/product-quality/oss-source-review-report.json',
    baselineSnapshotDate: '2026-05-21',
    targetRecordCount: 1,
    prioritizedTargetCount: 1,
    deferredTargetCount: 0,
    gapRecordCount: 1,
    axesReviewed: absorptionAxes,
    gapChecks: [{ label: 'fixture gap checks pass', ok: true, detail: 'fixture' }],
    gapRecords: [gapRecord],
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
  }

  writeFileSync(
    join(repo, 'docs', 'product-quality', 'oss-architecture-gap-review-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )
}

function runAxisReview(repo: string) {
  return spawnSync('bun', ['run', scriptPath], {
    cwd: repo,
    encoding: 'utf8',
    shell: false,
  })
}

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

describe('OSS axis architecture review', () => {
  test('passes when every high-priority target axis is reviewed without requiring unrelated fixed axes', () => {
    const repo = makeTempRepo()
    writeGapReview(repo, ['eval_and_quality_gates', 'terminal_workflow'])

    const result = runAxisReview(repo)

    expect(result.status).toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('RESULT: PASS')

    const report = JSON.parse(
      readFileSync(
        join(repo, 'docs', 'product-quality', 'oss-axis-architecture-review-report.json'),
        'utf8',
      ),
    ) as {
      reviewedAxes: string[]
      reviewChecks: Array<{ ok: boolean }>
    }

    expect(report.reviewedAxes).toEqual([
      'eval_and_quality_gates',
      'terminal_workflow',
    ])
    expect(report.reviewChecks.every((item) => item.ok)).toBe(true)
  })
})
