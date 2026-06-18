import { afterEach, describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

const scriptPath = join(__dirname, 'product-oss-safe-backlog-closure.ts')
const tempDirs: string[] = []

function makeTempRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-backlog-closure-'))
  tempDirs.push(dir)
  mkdirSync(join(dir, 'docs', 'product-quality'), { recursive: true })
  mkdirSync(join(dir, 'reports'), { recursive: true })
  return dir
}

function writeFixture(repo: string): void {
  writeFileSync(
    join(repo, 'package.json'),
    JSON.stringify({
      scripts: {
        'product:oss-terminal-workflow-evidence': 'bun run scripts/product-oss-terminal-workflow-evidence.ts',
      },
    }),
  )
  writeFileSync(
    join(repo, 'docs', 'product-quality', 'oss-safe-backlog-plan-report.json'),
    `${JSON.stringify({
      nextSafeInternalGateCandidates: [
        {
          gateId: 'openclaude_internal_terminal_workflow_evidence_gate',
          axis: 'terminal_workflow',
          sourceBacklogItemCount: 1,
          protectedActionRequiredForPlanning: false,
        },
      ],
    }, null, 2)}\n`,
  )
  writeFileSync(
    join(repo, 'docs', 'product-quality', 'oss-terminal-workflow-evidence-report.json'),
    `${JSON.stringify({
      providerCallsPerformed: [],
      liveModelCallsPerformed: [],
      externalCallsPerformed: [],
      protectedActionsExecuted: [],
      releaseReadinessClaimAllowed: false,
      productionReadinessClaimAllowed: false,
      publicReadinessClaimAllowed: false,
      externalValidationClaimAllowed: false,
      autonomousReliabilityClaimAllowed: false,
      superiorityClaimAllowed: false,
      publicComparisonClaimAllowed: false,
    }, null, 2)}\n`,
  )
  writeFileSync(
    join(repo, 'docs', 'product-quality', 'oss-terminal-workflow-evidence-report.md'),
    '# terminal evidence\n',
  )
  writeFileSync(
    join(repo, 'reports', 'openclaude-oss-terminal-workflow-evidence.jsonl'),
    '{"ok":true}\n',
  )
}

function runClosure(repo: string) {
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

describe('OSS safe backlog closure', () => {
  test('passes when the current safe backlog contains a subset of known evidence gates', () => {
    const repo = makeTempRepo()
    writeFixture(repo)

    const result = runClosure(repo)

    expect(result.status).toBe(0)
    expect(`${result.stdout}\n${result.stderr}`).toContain('RESULT: PASS')
    expect(`${result.stdout}\n${result.stderr}`).toContain('source_candidate_count=1')

    const report = JSON.parse(
      readFileSync(
        join(repo, 'docs', 'product-quality', 'oss-safe-backlog-closure-report.json'),
        'utf8',
      ),
    ) as {
      sourceCandidateCount: number
      openCandidateCount: number
      closureChecks: Array<{ ok: boolean }>
    }

    expect(report.sourceCandidateCount).toBe(1)
    expect(report.openCandidateCount).toBe(0)
    expect(report.closureChecks.every((item) => item.ok)).toBe(true)
  })
})
