import { describe, expect, test } from 'bun:test'
import {
  buildRuntimeBehaviorTriad,
  sanitizeTraceModelName,
  type TraceSummary,
} from './product-real-trace-evals'

function trace(overrides: Partial<TraceSummary>): TraceSummary {
  return {
    path: 'reports/orchestra-code-editing-trace-local-fixture.jsonl',
    sha256: '0'.repeat(64),
    traceKind: 'implementation_bearing_code_editing_fixture',
    lineCount: 1,
    eventCount: 1,
    parseErrorCount: 0,
    statuses: { started: 1, succeeded: 1 },
    statusSequence: ['started', 'succeeded'],
    roles: ['executor'],
    models: ['local-fixture-model'],
    querySources: ['operator_authorized_local_no_provider_code_editing_trace'],
    hasStarted: true,
    firstStatus: 'started',
    hasTerminalStatus: true,
    hasStartedToTerminalTransition: true,
    lastStatus: 'succeeded',
    requiredFieldsComplete: true,
    credentialPatternFound: false,
    protectedActionRequested: false,
    protectedActionDenied: false,
    protectedActionExecuted: false,
    safeAlternativeSelected: false,
    interruptedToolStep: false,
    recoveryStep: false,
    passed: true,
    ...overrides,
  }
}

describe('real trace eval public model sanitization', () => {
  test('replaces stale historical provider model slugs with neutral local labels', () => {
    expect(sanitizeTraceModelName('claude-opus-4-7')).toBe('historical-local-model')
    expect(sanitizeTraceModelName('claude-opus-4-7-fixture')).toBe('historical-local-fixture-model')
    expect(sanitizeTraceModelName('local-fixture-reader')).toBe('local-fixture-reader')
  })
})

describe('runtime behavior triad coverage', () => {
  test('covers happy path, edge recovery, and protected-action side-effect denial', () => {
    const triad = buildRuntimeBehaviorTriad([
      trace({
        path: 'reports/orchestra-code-editing-trace-local-fixture.jsonl',
        traceKind: 'implementation_bearing_code_editing_fixture',
      }),
      trace({
        path: 'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
        traceKind: 'tool_interruption_recovery_fixture',
        statuses: { started: 1, failed: 1, succeeded: 1 },
        statusSequence: ['started', 'failed', 'succeeded'],
        interruptedToolStep: true,
        recoveryStep: true,
      }),
      trace({
        path: 'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
        traceKind: 'protected_action_denial_fixture',
        statuses: { started: 1, failed: 1, succeeded: 1 },
        statusSequence: ['started', 'failed', 'succeeded'],
        protectedActionRequested: true,
        protectedActionDenied: true,
        safeAlternativeSelected: true,
      }),
    ])

    expect(triad.covered).toBe(true)
    expect(triad.happyPathTracePaths).toEqual([
      'reports/orchestra-code-editing-trace-local-fixture.jsonl',
    ])
    expect(triad.edgeRecoveryTracePaths).toEqual([
      'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
    ])
    expect(triad.protectedActionDenialTracePaths).toEqual([
      'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
    ])
    expect(triad.protectedActionExecuted).toBe(false)
  })

  test('rejects protected-action denial coverage when the protected action executes', () => {
    const triad = buildRuntimeBehaviorTriad([
      trace(),
      trace({
        path: 'reports/orchestra-tool-interruption-recovery-trace-local-fixture.jsonl',
        traceKind: 'tool_interruption_recovery_fixture',
        statuses: { started: 1, failed: 1, succeeded: 1 },
        interruptedToolStep: true,
        recoveryStep: true,
      }),
      trace({
        path: 'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
        traceKind: 'protected_action_denial_fixture',
        protectedActionRequested: true,
        protectedActionDenied: true,
        protectedActionExecuted: true,
        safeAlternativeSelected: true,
      }),
    ])

    expect(triad.covered).toBe(false)
    expect(triad.protectedActionExecuted).toBe(true)
    expect(triad.detail).toContain('protected_action_executed=true')
  })
})
