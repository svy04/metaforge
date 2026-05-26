import { describe, expect, test } from 'bun:test'

import {
  formatHumanGateMessage,
  humanGateMessageLevel,
} from './humanGate.js'
import type { EvidenceMatrix } from './evidenceArbiter.js'

const matrixWithGreen: EvidenceMatrix = {
  verdicts: [
    {
      candidateLabel: 'gpt-a',
      evidence: {
        testsRan: { ran: true, passed: true, pass: true },
        diffMinimal: { lineCount: 12, under: 200, pass: true },
        scopeFit: { keywordsMatched: 3, keywordsTotal: 4, pass: true },
        rollbackable: { branchIsolated: true, pass: true },
        understandable: { gptVerdict: 'pass', pass: true },
      },
      recommendation: 'green',
      rationale: 'all 5 axes pass',
    },
    {
      candidateLabel: 'gpt-b',
      evidence: {
        testsRan: { ran: true, passed: true, pass: true },
        diffMinimal: { lineCount: 30, under: 200, pass: true },
        scopeFit: { keywordsMatched: 2, keywordsTotal: 4, pass: true },
        rollbackable: { branchIsolated: true, pass: true },
        understandable: { gptVerdict: 'fail', pass: false },
      },
      recommendation: 'yellow',
      rationale: 'understandability check failed',
    },
    {
      candidateLabel: 'opus-shadow',
      evidence: {
        testsRan: { ran: true, passed: false, pass: false },
        diffMinimal: { lineCount: 10, under: 200, pass: true },
        scopeFit: { keywordsMatched: 4, keywordsTotal: 4, pass: true },
        rollbackable: { branchIsolated: true, pass: true },
        understandable: { gptVerdict: 'pass', pass: true },
      },
      recommendation: 'red',
      rationale: 'tests did not pass',
    },
  ],
  topRecommended: 'gpt-a',
  generatedAt: '2026-05-07T00:00:00Z',
}

describe('humanGate — formatHumanGateMessage', () => {
  test('shows the top recommended candidate prominently for green verdicts', () => {
    const text = formatHumanGateMessage(matrixWithGreen)
    expect(text).toContain('[Phase 4 Human Gate]')
    expect(text).toContain('추천')
    expect(text).toContain('gpt-a')
    expect(text).toContain('green')
  })

  test('lists per-axis evidence for the recommended candidate', () => {
    const text = formatHumanGateMessage(matrixWithGreen)
    expect(text).toMatch(/테스트/)
    expect(text).toMatch(/diff/i)
    expect(text).toMatch(/scope|범위/i)
    expect(text).toMatch(/rollback|롤백/i)
    expect(text).toMatch(/이해/)
  })

  test('lists slash command options for each completed candidate', () => {
    const text = formatHumanGateMessage(matrixWithGreen)
    expect(text).toContain('/orchestra-apply gpt-a')
    expect(text).toContain('/orchestra-apply gpt-b')
    expect(text).toContain('/orchestra-apply opus-shadow')
    expect(text).toContain('/orchestra-reject')
  })

  test('warns explicitly about extra confirm step for opus-shadow promotion', () => {
    const text = formatHumanGateMessage(matrixWithGreen)
    // The opus-shadow line must hint that an extra confirm is required so the
    // user is not surprised when /orchestra-apply opus-shadow returns
    // "needs confirm".
    expect(text.toLowerCase()).toMatch(/opus-shadow.*(confirm|확인|야당)/s)
    expect(text).toContain('/orchestra-apply opus-shadow --confirm-opus')
  })

  test('flags absence of any green candidate so the user understands red state', () => {
    const allRed: EvidenceMatrix = {
      verdicts: matrixWithGreen.verdicts.map(v => ({
        ...v,
        recommendation: 'red' as const,
        rationale: 'forced red',
      })),
      topRecommended: undefined,
      generatedAt: '2026-05-07T00:00:00Z',
    }
    const text = formatHumanGateMessage(allRed)
    expect(text.toLowerCase()).toMatch(/권장 안 함|모두 red|all red|no green/)
  })
})

describe('humanGate — humanGateMessageLevel', () => {
  test('green → info, yellow → warning, red-only → error', () => {
    expect(humanGateMessageLevel(matrixWithGreen)).toBe('info')
    const yellow: EvidenceMatrix = {
      verdicts: matrixWithGreen.verdicts.map(v => ({
        ...v,
        recommendation: 'yellow' as const,
      })),
      topRecommended: undefined,
      generatedAt: '2026-05-07T00:00:00Z',
    }
    expect(humanGateMessageLevel(yellow)).toBe('warning')
    const red: EvidenceMatrix = {
      verdicts: matrixWithGreen.verdicts.map(v => ({
        ...v,
        recommendation: 'red' as const,
      })),
      topRecommended: undefined,
      generatedAt: '2026-05-07T00:00:00Z',
    }
    expect(humanGateMessageLevel(red)).toBe('error')
  })
})
