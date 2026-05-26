import { execFileSync } from 'node:child_process'
import {
  existsSync,
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

import { afterEach, describe, expect, test } from 'bun:test'

import { getLatestShadowReviewPath } from './promotionStore.js'
import { createOrchestraShadowReview } from './shadowReview.js'
import type { ShadowCandidate, ShadowWorkerFn } from './shadowExecutor.js'

const roots: string[] = []

function makeRepo(): string {
  const root = mkdtempSync(join(tmpdir(), 'openclaude-shadow-review-'))
  roots.push(root)
  writeFileSync(join(root, 'math.ts'), 'export const value = 1\n', 'utf8')
  execFileSync('git', ['init'], { cwd: root })
  execFileSync('git', ['config', 'user.email', 'openclaude@example.local'], {
    cwd: root,
  })
  execFileSync('git', ['config', 'user.name', 'OpenClaude Test'], { cwd: root })
  execFileSync('git', ['add', 'math.ts'], { cwd: root })
  execFileSync('git', ['commit', '-m', 'initial'], { cwd: root })
  return root
}

function worker(label: ShadowCandidate['label']): ShadowWorkerFn {
  return async input => {
    writeFileSync(
      join(input.worktree.path, 'math.ts'),
      `export const value = ${label === 'gpt-b' ? 3 : 2}\n`,
      'utf8',
    )
    execFileSync('git', ['-C', input.worktree.path, 'add', '-A'])
    const diff = execFileSync('git', ['-C', input.worktree.path, 'diff', 'HEAD'], {
      encoding: 'utf8',
    })
    return {
      label,
      worktreePath: input.worktree.path,
      status: 'completed',
      patchSummary: `${label} patch`,
      filesChanged: ['math.ts'],
      diff,
    }
  }
}

afterEach(() => {
  for (const root of roots.splice(0)) {
    rmSync(root, { recursive: true, force: true })
  }
})

describe('createOrchestraShadowReview persistence', () => {
  test('writes latest-shadow-review.json for follow-up apply commands', async () => {
    const root = makeRepo()
    const result = await createOrchestraShadowReview({
      taskScope: { intent: 'change math value', targetFiles: ['math.ts'] },
      cwd: root,
      toolUseContext: {
        getAppState: () => ({
          settings: { orchestra: { enabled: true, shadowEnabled: true } },
        }),
      } as never,
      workers: {
        'gpt-a': worker('gpt-a'),
        'gpt-b': worker('gpt-b'),
        'opus-shadow': worker('opus-shadow'),
      },
      reviewers: {
        gpt: async () => ({
          verdict: 'green',
          scoresOutOf5: { correctness: 5, minimality: 5, scopeFit: 5 },
          rationale: 'ok',
        }),
        opus: async () => ({
          verdict: 'green',
          scoresOutOf5: { correctness: 5, minimality: 5, scopeFit: 5 },
          rationale: 'ok',
        }),
      },
      understandableJudge: async () => ({ verdict: 'pass' }),
      recordUsageEvent: () => {},
      skipOAuthRefresh: true,
    })

    const latestPath = getLatestShadowReviewPath(root)
    expect(result.diagnostic).toContain(latestPath)
    expect(existsSync(latestPath)).toBe(true)
    const latest = JSON.parse(readFileSync(latestPath, 'utf8')) as {
      candidates: ShadowCandidate[]
    }
    expect(latest.candidates.map(c => c.label)).toEqual([
      'gpt-a',
      'gpt-b',
      'opus-shadow',
    ])
  })
})

