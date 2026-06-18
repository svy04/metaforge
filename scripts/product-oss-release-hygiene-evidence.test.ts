import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const scriptPath = join(__dirname, 'product-oss-release-hygiene-evidence.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-release-evidence-'))
  tempDirs.push(dir)
  mkdirSync(join(dir, 'docs', 'product-quality'), { recursive: true })
  return dir
}

function writeSafeBacklogPlan(repo: string): void {
  const report = {
    mode: 'local_no_provider_oss_safe_backlog_plan',
    sourceAxisArchitectureReviewReportPath: 'docs/product-quality/oss-axis-architecture-review-report.json',
    nextSafeInternalGateCandidates: [
      {
        gateId: 'openclaude_internal_terminal_workflow_evidence_gate',
        axis: 'terminal_workflow',
        protectedActionRequiredForPlanning: false,
        sourceBacklogItemCount: 1,
      },
    ],
    providerCallsPerformed: [],
    liveModelCallsPerformed: [],
    externalCallsPerformed: [],
    protectedActionsExecuted: [],
    planItems: [
      {
        planItemId: 'terminal-workflow-1',
        sourceProject: 'fixture/cli',
        sourceUrl: 'https://github.com/fixture/cli',
        axis: 'terminal_workflow',
        backlogText: 'keep terminal workflow local',
        currentLocalEvidence: ['docs/product-quality/terminal-report.json'],
        unresolvedEvidenceGap: 'terminal evidence remains local',
        protectedBoundary: 'terminal claim expansion remains blocked',
        forbiddenShortcuts: ['no claims'],
      },
    ],
  }

  writeFileSync(
    join(repo, 'docs', 'product-quality', 'oss-safe-backlog-plan-report.json'),
    `${JSON.stringify(report, null, 2)}\n`,
  )
}

function runReleaseEvidence(repo: string) {
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

describe('OSS release hygiene evidence', () => {
  test('passes as claim-blocked skipped evidence when the current high-priority backlog has no release axis', () => {
    const repo = makeTempRepo()
    writeSafeBacklogPlan(repo)

    const result = runReleaseEvidence(repo)

    expect(result.status).toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('RESULT: PASS')
    expect(`${result.stdout}\n${result.stderr}`).toContain('source_plan_item_count=0')

    const report = JSON.parse(
      readFileSync(
        join(repo, 'docs', 'product-quality', 'oss-release-hygiene-evidence-report.json'),
        'utf8',
      ),
    ) as {
      evidenceItemCount: number
      releaseReadinessClaimAllowed: boolean
      evidenceChecks: Array<{ ok: boolean }>
    }

    expect(report.evidenceItemCount).toBe(0)
    expect(report.releaseReadinessClaimAllowed).toBe(false)
    expect(report.evidenceChecks.every((item) => item.ok)).toBe(true)
  })
})
