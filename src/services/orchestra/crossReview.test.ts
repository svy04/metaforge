import { describe, expect, test } from 'bun:test'

import {
  buildCrossReviewMatrix,
  formatMatrixDetail,
  formatMatrixSummary,
  type ReviewerFn,
} from './crossReview.js'
import type { ShadowCandidate } from './shadowExecutor.js'

const baseCandidates: ShadowCandidate[] = [
  {
    label: 'gpt-a',
    worktreePath: '/repo/.openclaude-shadows/t/gpt-a',
    status: 'completed',
    patchSummary: 'add license header',
    diff: 'diff --git a/x b/x\n',
  },
  {
    label: 'gpt-b',
    worktreePath: '/repo/.openclaude-shadows/t/gpt-b',
    status: 'completed',
    patchSummary: 'license header via macro',
    diff: 'diff --git a/x b/x\n',
  },
  {
    label: 'opus-shadow',
    worktreePath: '/repo/.openclaude-shadows/t/opus-shadow',
    status: 'completed',
    patchSummary: 'license header + lint guard',
    diff: 'diff --git a/x b/x\n',
  },
]

const trivialReviewer: ReviewerFn = async ({ candidate }) => ({
  scoresOutOf5: { correctness: 4, minimality: 3, scopeFit: 5 },
  verdict: 'green',
  rationale: `${candidate.label} looks fine`,
})

describe('crossReview — buildCrossReviewMatrix', () => {
  test('produces 3 candidates × 2 reviewers = 6 verdicts', async () => {
    const matrix = await buildCrossReviewMatrix({
      candidates: baseCandidates,
      reviewers: { gpt: trivialReviewer, opus: trivialReviewer },
    })
    expect(matrix.candidates.length).toBe(3)
    expect(matrix.verdicts.length).toBe(6)
    const reviewerCounts: Record<string, number> = {}
    for (const v of matrix.verdicts) {
      reviewerCounts[v.reviewer] = (reviewerCounts[v.reviewer] ?? 0) + 1
    }
    expect(reviewerCounts['gpt']).toBe(3)
    expect(reviewerCounts['opus']).toBe(3)
  })

  test('failed candidates get an execution_failed placeholder verdict per reviewer (no model call)', async () => {
    let realCalls = 0
    const counting: ReviewerFn = async () => {
      realCalls++
      return {
        scoresOutOf5: { correctness: 0, minimality: 0, scopeFit: 0 },
        verdict: 'red',
        rationale: 'should not run on failed candidates',
      }
    }
    const candidates: ShadowCandidate[] = [
      ...baseCandidates.slice(0, 2),
      {
        label: 'opus-shadow',
        worktreePath: '/p',
        status: 'failed',
        error: 'OAuth missing',
      },
    ]
    const matrix = await buildCrossReviewMatrix({
      candidates,
      reviewers: { gpt: counting, opus: counting },
    })
    // 2 completed candidates × 2 reviewers = 4 real calls; the failed
    // candidate must NOT trigger reviewer model calls but must still be
    // represented in verdicts so the matrix stays a 3×2 grid.
    expect(realCalls).toBe(4)
    expect(matrix.verdicts.length).toBe(6)
    const failedCells = matrix.verdicts.filter(
      v => v.candidateLabel === 'opus-shadow',
    )
    expect(failedCells.length).toBe(2)
    for (const cell of failedCells) {
      expect(cell.verdict).toBe('red')
      expect(cell.rationale.toLowerCase()).toContain('execution_failed')
    }
  })

  test('reviewer throwing degrades that single cell, rest of grid completes', async () => {
    const flaky: ReviewerFn = async ({ candidate }) => {
      if (candidate.label === 'gpt-b') {
        throw new Error('reviewer model unavailable')
      }
      return {
        scoresOutOf5: { correctness: 4, minimality: 4, scopeFit: 4 },
        verdict: 'green',
        rationale: 'ok',
      }
    }
    const matrix = await buildCrossReviewMatrix({
      candidates: baseCandidates,
      reviewers: { gpt: flaky, opus: trivialReviewer },
    })
    expect(matrix.verdicts.length).toBe(6)
    const flakyCell = matrix.verdicts.find(
      v => v.reviewer === 'gpt' && v.candidateLabel === 'gpt-b',
    )
    expect(flakyCell).toBeDefined()
    expect(flakyCell?.verdict).toBe('red')
    expect(flakyCell?.rationale).toContain('reviewer_failed')
  })
})

describe('crossReview — formatting helpers', () => {
  test('formatMatrixSummary renders a single-line per-candidate digest', async () => {
    const matrix = await buildCrossReviewMatrix({
      candidates: baseCandidates,
      reviewers: { gpt: trivialReviewer, opus: trivialReviewer },
    })
    const summary = formatMatrixSummary(matrix)
    expect(summary).toContain('gpt-a')
    expect(summary).toContain('gpt-b')
    expect(summary).toContain('opus-shadow')
    // No multi-line section breaks — one human-skim line.
    expect(summary.split('\n').length).toBeLessThanOrEqual(2)
  })

  test('formatMatrixDetail emits a markdown table containing all 6 cells', async () => {
    const matrix = await buildCrossReviewMatrix({
      candidates: baseCandidates,
      reviewers: { gpt: trivialReviewer, opus: trivialReviewer },
    })
    const detail = formatMatrixDetail(matrix)
    expect(detail).toContain('| candidate')
    expect(detail).toContain('gpt-a')
    expect(detail).toContain('gpt-b')
    expect(detail).toContain('opus-shadow')
    // Each verdict's rationale must appear at least once.
    for (const v of matrix.verdicts) {
      expect(detail).toContain(v.rationale)
    }
  })

  test('formatMatrixDetail escapes backslashes before markdown table pipes', () => {
    const detail = formatMatrixDetail({
      candidates: [baseCandidates[0]],
      generatedAt: '2026-06-19T00:00:00.000Z',
      verdicts: [
        {
          candidateLabel: 'gpt-a',
          reviewer: 'gpt',
          verdict: 'green',
          scoresOutOf5: { correctness: 4, minimality: 4, scopeFit: 4 },
          rationale: String.raw`windows path C:\tmp | table pipe`,
        },
      ],
    })

    expect(detail).toContain(
      String.raw`| gpt-a | gpt | green | 4 | 4 | 4 | windows path C:\\tmp \| table pipe |`,
    )
  })
})
