import { describe, expect, test } from 'bun:test'

import { buildGoalTraceReport, evaluateGoalTrace, type GoalTrace } from './validate-goal-traces'

const validTrace: GoalTrace = {
  goalId: 'CG-001',
  traceId: '11111111111111111111111111111111',
  claimBoundary: {
    allowed: ['Local Goal Kernel trace validation passed.'],
    forbidden: ['Production readiness', 'External validation'],
  },
  providerCallsPerformed: [],
  liveModelCallsPerformed: [],
  externalCallsPerformed: [],
  protectedActionsExecuted: [],
  events: [
    {
      timestamp: '2026-06-18T09:00:00.000Z',
      eventName: 'goal.loaded',
      status: 'started',
      actor: 'orchestrator',
      summary: 'Loaded CG-001 from docs/goals.',
    },
    {
      timestamp: '2026-06-18T09:01:00.000Z',
      eventName: 'checkpoint.completed',
      status: 'succeeded',
      actor: 'implementer',
      checkpointId: 'CP-001',
      summary: 'Goal validator was implemented.',
    },
    {
      timestamp: '2026-06-18T09:02:00.000Z',
      eventName: 'validation.ran',
      status: 'succeeded',
      actor: 'eval',
      command: 'bun run goals:validate',
      exitCode: 0,
      evidenceArtifacts: ['docs/product-quality/goal-validation-report.json'],
      summary: 'Goal validator passed.',
    },
    {
      timestamp: '2026-06-18T09:03:00.000Z',
      eventName: 'claim.reviewed',
      status: 'succeeded',
      actor: 'evidence-arbiter',
      disallowedClaimsFound: false,
      summary: 'Claim boundary review stayed local and no-provider.',
    },
    {
      timestamp: '2026-06-18T09:04:00.000Z',
      eventName: 'goal.validated',
      status: 'succeeded',
      actor: 'orchestrator',
      summary: 'CG-001 reached local validated status.',
    },
  ],
}

describe('goal trace validator', () => {
  test('accepts a local no-provider goal trace with validation and claim review evidence', () => {
    const result = evaluateGoalTrace(validTrace, new Set(['CG-001']))

    expect(result.ok).toBe(true)
    expect(result.goalId).toBe('CG-001')
    expect(result.traceId).toBe(validTrace.traceId)
    expect(result.errors).toEqual([])
    expect(result.eventSequence).toEqual([
      'goal.loaded',
      'checkpoint.completed',
      'validation.ran',
      'claim.reviewed',
      'goal.validated',
    ])
  })

  test('rejects validated traces that lack successful command evidence', () => {
    const missingCommandEvidence: GoalTrace = {
      ...validTrace,
      events: validTrace.events.filter((event) => event.eventName !== 'validation.ran'),
    }

    const result = evaluateGoalTrace(missingCommandEvidence, new Set(['CG-001']))

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('validated traces require a successful validation.ran event with command, exitCode 0, and evidence artifact')
  })

  test('rejects side-effect traces with provider, live model, external, or protected calls', () => {
    const sideEffectTrace: GoalTrace = {
      ...validTrace,
      providerCallsPerformed: ['provider-call'],
      liveModelCallsPerformed: ['live-model-call'],
      externalCallsPerformed: ['https://example.com'],
      protectedActionsExecuted: ['publish'],
    }

    const result = evaluateGoalTrace(sideEffectTrace, new Set(['CG-001']))

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('providerCallsPerformed must be empty')
    expect(result.errors).toContain('liveModelCallsPerformed must be empty')
    expect(result.errors).toContain('externalCallsPerformed must be empty')
    expect(result.errors).toContain('protectedActionsExecuted must be empty')
  })

  test('rejects traces whose goal id is not in the registry', () => {
    const unknownGoalTrace: GoalTrace = {
      ...validTrace,
      goalId: 'CG-999',
    }

    const result = evaluateGoalTrace(unknownGoalTrace, new Set(['CG-001']))

    expect(result.ok).toBe(false)
    expect(result.errors).toContain('goalId must refer to a known docs/goals/CG-*.md goal')
  })

  test('builds a report with pass/fail counts and no side-effect calls', () => {
    const invalidTrace: GoalTrace = {
      ...validTrace,
      traceId: '22222222222222222222222222222222',
      events: validTrace.events.filter((event) => event.eventName !== 'claim.reviewed'),
    }

    const report = buildGoalTraceReport([
      { path: 'docs/goals/traces/CG-001-goal-kernel-mvp.trace.json', trace: validTrace },
      { path: 'docs/goals/traces/CG-001-invalid.trace.json', trace: invalidTrace },
    ], new Set(['CG-001']))

    expect(report.traceFileCount).toBe(2)
    expect(report.validTraceCount).toBe(1)
    expect(report.invalidTraceCount).toBe(1)
    expect(report.providerCallsPerformed).toEqual([])
    expect(report.liveModelCallsPerformed).toEqual([])
    expect(report.externalCallsPerformed).toEqual([])
    expect(report.protectedActionsExecuted).toEqual([])
    expect(report.validationResults[1]?.errors).toContain('validated traces require claim.reviewed with disallowedClaimsFound=false before goal.validated')
  })
})
