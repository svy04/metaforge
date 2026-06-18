import { describe, expect, test } from 'bun:test'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import {
  discoverPublishableTraceFiles,
  isHistoricalLiveProbeTracePath,
} from './product-trace-discovery'

describe('product trace discovery', () => {
  test('excludes historical live probe traces while preserving no-provider evidence traces', () => {
    const root = mkdtempSync(join(tmpdir(), 'openclaude-trace-discovery-'))
    try {
      mkdirSync(join(root, 'reports'), { recursive: true })
      writeFileSync(join(root, 'reports/orchestra-live-20260506-163448.jsonl'), '{}\n')
      writeFileSync(join(root, 'reports/orchestra-live-adaptive-20260506-164441.jsonl'), '{}\n')
      writeFileSync(join(root, 'reports/orchestra-live-sidequery-20260506-172336.jsonl'), '{}\n')
      writeFileSync(join(root, 'reports/orchestra-real-session-capture-local-cli.jsonl'), '{}\n')
      writeFileSync(join(root, 'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl'), '{}\n')
      writeFileSync(join(root, 'reports/openclaude-portable-trace-events.jsonl'), '{}\n')

      expect(isHistoricalLiveProbeTracePath('reports/orchestra-live-20260506-163448.jsonl')).toBe(true)
      expect(isHistoricalLiveProbeTracePath('reports/orchestra-real-session-capture-local-cli.jsonl')).toBe(false)
      expect(discoverPublishableTraceFiles({ root })).toEqual([
        'reports/orchestra-protected-action-denial-trace-local-fixture.jsonl',
        'reports/orchestra-real-session-capture-local-cli.jsonl',
      ])
    } finally {
      rmSync(root, { recursive: true, force: true })
    }
  })
})
