import { describe, expect, test } from 'bun:test'
import { sanitizeTraceModelName } from './product-real-trace-evals'

describe('real trace eval public model sanitization', () => {
  test('replaces stale historical provider model slugs with neutral local labels', () => {
    expect(sanitizeTraceModelName('claude-opus-4-7')).toBe('historical-local-model')
    expect(sanitizeTraceModelName('claude-opus-4-7-fixture')).toBe('historical-local-fixture-model')
    expect(sanitizeTraceModelName('local-fixture-reader')).toBe('local-fixture-reader')
  })
})
