import { describe, expect, test } from 'bun:test'

import { evaluatePromoteRequest } from './promote.js'
import type { EvidenceMatrix } from './evidenceArbiter.js'
import type { ShadowCandidate } from './shadowExecutor.js'

const greenMatrix: EvidenceMatrix = {
  verdicts: [
    {
      candidateLabel: 'gpt-a',
      evidence: {} as any,
      recommendation: 'green',
      rationale: 'ok',
    },
    {
      candidateLabel: 'gpt-b',
      evidence: {} as any,
      recommendation: 'yellow',
      rationale: 'soft',
    },
    {
      candidateLabel: 'opus-shadow',
      evidence: {} as any,
      recommendation: 'green',
      rationale: 'ok',
    },
  ],
  topRecommended: 'gpt-a',
  generatedAt: 'now',
}

const completed = (label: ShadowCandidate['label']): ShadowCandidate => ({
  label,
  worktreePath: `/repo/.openclaude-shadows/t/${label}`,
  status: 'completed',
  diff: 'diff --git a b\n+ x\n',
})

const failed: ShadowCandidate = {
  label: 'gpt-b',
  worktreePath: '/p',
  status: 'failed',
  error: 'oops',
}

describe('promote — evaluatePromoteRequest', () => {
  test('approves a green gpt-a candidate', () => {
    const result = evaluatePromoteRequest({
      candidateLabel: 'gpt-a',
      candidates: [completed('gpt-a')],
      evidenceMatrix: greenMatrix,
    })
    expect(result.ok).toBe(true)
    if (result.ok) {
      expect(result.appliedLabel).toBe('gpt-a')
      expect(result.diff).toContain('diff --git')
    }
  })

  test('rejects when the candidate is not in the request', () => {
    const result = evaluatePromoteRequest({
      candidateLabel: 'gpt-b',
      candidates: [completed('gpt-a')],
      evidenceMatrix: greenMatrix,
    })
    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('candidate-not-found')
  })

  test('rejects when the candidate failed to execute', () => {
    const result = evaluatePromoteRequest({
      candidateLabel: 'gpt-b',
      candidates: [failed],
      evidenceMatrix: greenMatrix,
    })
    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('candidate-failed')
  })

  test('rejects when verdict is red', () => {
    const redMatrix: EvidenceMatrix = {
      ...greenMatrix,
      verdicts: greenMatrix.verdicts.map(v =>
        v.candidateLabel === 'gpt-a'
          ? { ...v, recommendation: 'red' as const }
          : v,
      ),
    }
    const result = evaluatePromoteRequest({
      candidateLabel: 'gpt-a',
      candidates: [completed('gpt-a')],
      evidenceMatrix: redMatrix,
    })
    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('red-verdict')
  })

  test('opus-shadow needs explicit second confirm even when green', () => {
    const result = evaluatePromoteRequest({
      candidateLabel: 'opus-shadow',
      candidates: [completed('opus-shadow')],
      evidenceMatrix: greenMatrix,
    })
    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('opus-shadow-needs-confirm')
  })

  test('opus-shadow approved when confirmedOpusShadow=true and green', () => {
    const result = evaluatePromoteRequest({
      candidateLabel: 'opus-shadow',
      candidates: [completed('opus-shadow')],
      evidenceMatrix: greenMatrix,
      confirmedOpusShadow: true,
    })
    expect(result.ok).toBe(true)
    if (result.ok) expect(result.appliedLabel).toBe('opus-shadow')
  })

  test('opus-shadow with confirmedOpusShadow but red verdict still rejected', () => {
    const redOpus: EvidenceMatrix = {
      ...greenMatrix,
      verdicts: greenMatrix.verdicts.map(v =>
        v.candidateLabel === 'opus-shadow'
          ? { ...v, recommendation: 'red' as const }
          : v,
      ),
    }
    const result = evaluatePromoteRequest({
      candidateLabel: 'opus-shadow',
      candidates: [completed('opus-shadow')],
      evidenceMatrix: redOpus,
      confirmedOpusShadow: true,
    })
    expect(result.ok).toBe(false)
    if (!result.ok) expect(result.reason).toBe('red-verdict')
  })
})
