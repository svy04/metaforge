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

import type { CrossReviewMatrix } from './crossReview.js'
import type { EvidenceMatrix } from './evidenceArbiter.js'
import type { ShadowCandidate } from './shadowExecutor.js'
import {
  applyStoredShadowCandidate,
  getLatestShadowReviewPath,
  rejectStoredShadowReview,
  writeLatestShadowReview,
} from './promotionStore.js'

const roots: string[] = []

function makeRepo(): string {
  const root = mkdtempSync(join(tmpdir(), 'openclaude-orchestra-promote-'))
  roots.push(root)
  execFileSync('git', ['init'], { cwd: root })
  execFileSync('git', ['config', 'user.email', 'openclaude@example.local'], {
    cwd: root,
  })
  execFileSync('git', ['config', 'user.name', 'OpenClaude Test'], { cwd: root })
  return root
}

function commitFile(root: string, rel: string, content: string): void {
  const full = join(root, rel)
  writeFileSync(full, content, 'utf8')
  execFileSync('git', ['add', rel], { cwd: root })
  execFileSync('git', ['commit', '-m', `add ${rel}`], { cwd: root })
}

function matrix(candidates: ShadowCandidate[]): CrossReviewMatrix {
  return {
    candidates,
    verdicts: [],
    generatedAt: 'now',
  }
}

function evidence(label: ShadowCandidate['label']): EvidenceMatrix {
  return {
    verdicts: [
      {
        candidateLabel: label,
        evidence: {} as never,
        recommendation: 'green',
        rationale: 'ok',
      },
    ],
    topRecommended: label,
    generatedAt: 'now',
  }
}

afterEach(() => {
  for (const root of roots.splice(0)) {
    rmSync(root, { recursive: true, force: true })
  }
})

describe('orchestra promotion store', () => {
  test('persists the latest shadow review and applies a selected candidate', async () => {
    const root = makeRepo()
    commitFile(root, 'math.ts', 'export const value = 1\n')
    const worktree = join(root, '.openclaude-shadows', 't-1', 'gpt-a')
    execFileSync('git', ['worktree', 'add', '-b', 'shadow/gpt-a', worktree], {
      cwd: root,
    })
    writeFileSync(join(worktree, 'math.ts'), 'export const value = 2\n', 'utf8')

    const candidate: ShadowCandidate = {
      label: 'gpt-a',
      worktreePath: worktree,
      status: 'completed',
      filesChanged: ['math.ts'],
      diff: 'diff --git a/math.ts b/math.ts\n',
    }
    await writeLatestShadowReview(root, {
      taskScope: { intent: 'change value' },
      candidates: [candidate],
      matrix: matrix([candidate]),
      evidenceMatrix: evidence('gpt-a'),
      detailPath: join(root, '.planning', 'phase-3', 'cross-review.md'),
    })

    expect(existsSync(getLatestShadowReviewPath(root))).toBe(true)
    const result = await applyStoredShadowCandidate({
      cwd: root,
      candidateLabel: 'gpt-a',
    })

    expect(result.ok).toBe(true)
    if (result.ok) expect(result.appliedFiles).toEqual(['math.ts'])
    expect(readFileSync(join(root, 'math.ts'), 'utf8')).toBe(
      'export const value = 2\n',
    )
  })

  test('requires a second confirm before applying opus-shadow', async () => {
    const root = makeRepo()
    commitFile(root, 'math.ts', 'export const value = 1\n')
    const worktree = join(root, '.openclaude-shadows', 't-1', 'opus-shadow')
    execFileSync(
      'git',
      ['worktree', 'add', '-b', 'shadow/opus-shadow', worktree],
      { cwd: root },
    )
    writeFileSync(join(worktree, 'math.ts'), 'export const value = 3\n', 'utf8')
    const candidate: ShadowCandidate = {
      label: 'opus-shadow',
      worktreePath: worktree,
      status: 'completed',
      filesChanged: ['math.ts'],
      diff: 'diff --git a/math.ts b/math.ts\n',
    }
    await writeLatestShadowReview(root, {
      taskScope: { intent: 'change value' },
      candidates: [candidate],
      matrix: matrix([candidate]),
      evidenceMatrix: evidence('opus-shadow'),
    })

    const result = await applyStoredShadowCandidate({
      cwd: root,
      candidateLabel: 'opus-shadow',
    })

    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('opus-shadow-needs-confirm')
    expect(readFileSync(join(root, 'math.ts'), 'utf8')).toBe(
      'export const value = 1\n',
    )
  })

  test('reject removes the latest review pointer', async () => {
    const root = makeRepo()
    commitFile(root, 'math.ts', 'export const value = 1\n')
    await writeLatestShadowReview(root, {
      taskScope: { intent: 'noop' },
      candidates: [],
      matrix: matrix([]),
      evidenceMatrix: { verdicts: [], generatedAt: 'now' },
    })

    const result = await rejectStoredShadowReview({ cwd: root })

    expect(result.ok).toBe(true)
    expect(existsSync(getLatestShadowReviewPath(root))).toBe(false)
  })
})

