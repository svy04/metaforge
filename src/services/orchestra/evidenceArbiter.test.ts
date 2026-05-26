import { describe, expect, test } from 'bun:test'

import {
  buildEvidenceMatrix,
  type UnderstandableJudgeFn,
} from './evidenceArbiter.js'
import type { CrossReviewMatrix } from './crossReview.js'
import type { ShadowCandidate } from './shadowExecutor.js'

const completedCandidate = (
  label: ShadowCandidate['label'],
  diff: string,
): ShadowCandidate => ({
  label,
  worktreePath: `/repo/.openclaude-shadows/t/${label}`,
  status: 'completed',
  patchSummary: `${label} did the thing`,
  filesChanged: ['src/x.ts'],
  diff,
})

const trivialCrossReview = (
  candidates: ShadowCandidate[],
): CrossReviewMatrix => ({
  candidates,
  verdicts: candidates.flatMap(c =>
    (['gpt', 'opus'] as const).map(reviewer => ({
      candidateLabel: c.label,
      reviewer,
      scoresOutOf5: { correctness: 4, minimality: 4, scopeFit: 4 },
      verdict: 'green' as const,
      rationale: 'looks ok',
    })),
  ),
  generatedAt: '2026-05-07T00:00:00Z',
})

const passingJudge: UnderstandableJudgeFn = async () => ({ verdict: 'pass' })

describe('evidenceArbiter — buildEvidenceMatrix', () => {
  test('green when all 5 axes pass', async () => {
    const candidate = completedCandidate('gpt-a', 'diff --git a b\n+ small\n')
    const matrix = await buildEvidenceMatrix({
      candidates: [candidate],
      crossReview: trivialCrossReview([candidate]),
      taskScope: { intent: 'add small thing' },
      understandableJudge: passingJudge,
      // For tests we mark "tests ran" as injected fact rather than running
      // them for real.
      testEvidence: { ran: true, passed: true, evidencePath: '/tmp/log' },
    })
    expect(matrix.verdicts.length).toBe(1)
    const v = matrix.verdicts[0]!
    expect(v.recommendation).toBe('green')
    expect(v.evidence.testsRan.pass).toBe(true)
    expect(v.evidence.diffMinimal.pass).toBe(true)
    expect(v.evidence.scopeFit.pass).toBe(true)
    expect(v.evidence.rollbackable.pass).toBe(true)
    expect(v.evidence.understandable.pass).toBe(true)
    expect(matrix.topRecommended).toBe('gpt-a')
  })

  test('red immediately when tests fail (β: 핵심 축 fail = red)', async () => {
    const candidate = completedCandidate('gpt-a', 'diff\n+ x\n')
    const matrix = await buildEvidenceMatrix({
      candidates: [candidate],
      crossReview: trivialCrossReview([candidate]),
      taskScope: { intent: 'do thing' },
      understandableJudge: passingJudge,
      testEvidence: { ran: true, passed: false },
    })
    expect(matrix.verdicts[0]?.recommendation).toBe('red')
  })

  test('red when scope keywords do not match user intent (핵심 축)', async () => {
    const candidate = completedCandidate('gpt-a', 'diff\n+ irrelevant\n')
    const matrix = await buildEvidenceMatrix({
      candidates: [candidate],
      crossReview: trivialCrossReview([candidate]),
      taskScope: { intent: 'totally different topic' },
      understandableJudge: passingJudge,
      testEvidence: { ran: true, passed: true },
    })
    expect(matrix.verdicts[0]?.recommendation).toBe('red')
  })

  test('yellow when only a non-critical axis fails (e.g. understandable)', async () => {
    const candidate = completedCandidate('gpt-a', 'diff\n+ small\n')
    const matrix = await buildEvidenceMatrix({
      candidates: [candidate],
      crossReview: trivialCrossReview([candidate]),
      taskScope: { intent: 'small thing' },
      understandableJudge: async () => ({ verdict: 'fail' }),
      testEvidence: { ran: true, passed: true },
    })
    expect(matrix.verdicts[0]?.recommendation).toBe('yellow')
  })

  test('failed candidate is reported as red without running judge', async () => {
    let judgeCalls = 0
    const candidate: ShadowCandidate = {
      label: 'opus-shadow',
      worktreePath: '/p',
      status: 'failed',
      error: 'OAuth missing',
    }
    const matrix = await buildEvidenceMatrix({
      candidates: [candidate],
      crossReview: trivialCrossReview([candidate]),
      taskScope: { intent: 'x' },
      understandableJudge: async () => {
        judgeCalls++
        return { verdict: 'pass' }
      },
      testEvidence: { ran: false },
    })
    expect(matrix.verdicts[0]?.recommendation).toBe('red')
    expect(judgeCalls).toBe(0)
  })

  test('topRecommended picks the first green candidate, undefined when all red/yellow', async () => {
    const a = completedCandidate('gpt-a', 'huge diff\n' + 'x\n'.repeat(500))
    const b = completedCandidate('gpt-b', 'small\n+ done\n')
    const matrix = await buildEvidenceMatrix({
      candidates: [a, b],
      crossReview: trivialCrossReview([a, b]),
      taskScope: { intent: 'done' },
      understandableJudge: passingJudge,
      testEvidence: { ran: true, passed: true },
    })
    expect(matrix.topRecommended).toBe('gpt-b')
  })
})
