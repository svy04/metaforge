import { describe, expect, test, beforeEach, afterEach } from 'bun:test'
import { mkdtempSync, rmSync, readFileSync, existsSync } from 'fs'
import { join } from 'path'
import { tmpdir } from 'os'

import {
  getOrchestraUsageLogPath,
  recordOrchestraUsageEvent,
  type OrchestraUsageEvent,
} from './usageLog.js'

describe('orchestra usageLog', () => {
  let tmpDir: string
  let logPath: string
  let originalEnv: string | undefined

  beforeEach(() => {
    tmpDir = mkdtempSync(join(tmpdir(), 'orchestra-usagelog-'))
    logPath = join(tmpDir, 'orchestra-usage.jsonl')
    originalEnv = process.env.OPENCLAUDE_ORCHESTRA_USAGE_LOG
    process.env.OPENCLAUDE_ORCHESTRA_USAGE_LOG = logPath
  })

  afterEach(() => {
    if (originalEnv === undefined) {
      delete process.env.OPENCLAUDE_ORCHESTRA_USAGE_LOG
    } else {
      process.env.OPENCLAUDE_ORCHESTRA_USAGE_LOG = originalEnv
    }
    rmSync(tmpDir, { recursive: true, force: true })
  })

  test('getOrchestraUsageLogPath honors env override', () => {
    expect(getOrchestraUsageLogPath()).toBe(logPath)
  })

  test('records skeptic role events with status transitions', () => {
    const startedEvent: OrchestraUsageEvent = {
      role: 'skeptic',
      model: 'claude-opus-4-7',
      status: 'started',
      querySource: 'sdk',
      turnCount: 1,
    }
    const succeededEvent: OrchestraUsageEvent = {
      role: 'skeptic',
      model: 'claude-opus-4-7',
      status: 'succeeded',
      querySource: 'sdk',
      turnCount: 1,
    }

    recordOrchestraUsageEvent(startedEvent)
    recordOrchestraUsageEvent(succeededEvent)

    expect(existsSync(logPath)).toBe(true)
    const lines = readFileSync(logPath, 'utf8')
      .split('\n')
      .filter(line => line.length > 0)
    expect(lines.length).toBe(2)

    const first = JSON.parse(lines[0]!)
    const second = JSON.parse(lines[1]!)
    expect(first.role).toBe('skeptic')
    expect(first.status).toBe('started')
    expect(second.role).toBe('skeptic')
    expect(second.status).toBe('succeeded')
    expect(typeof first.timestamp).toBe('string')
  })

  test('records skeptic failure with error metadata', () => {
    recordOrchestraUsageEvent({
      role: 'skeptic',
      model: 'claude-opus-4-7',
      status: 'failed',
      errorName: 'AuthError',
      errorMessage: 'OAuth token missing',
    })
    const line = readFileSync(logPath, 'utf8').trim()
    const parsed = JSON.parse(line)
    expect(parsed.role).toBe('skeptic')
    expect(parsed.status).toBe('failed')
    expect(parsed.errorName).toBe('AuthError')
    expect(parsed.errorMessage).toBe('OAuth token missing')
  })

  test('records new Phase 3 shadow / cross-reviewer roles', () => {
    const phase3Roles: OrchestraUsageEvent['role'][] = [
      'shadow-gpt-b',
      'shadow-opus',
      'cross-reviewer-gpt',
      'cross-reviewer-opus',
    ]
    for (const role of phase3Roles) {
      recordOrchestraUsageEvent({
        role,
        model: 'mock-model',
        status: 'started',
      })
    }
    const lines = readFileSync(logPath, 'utf8')
      .split('\n')
      .filter(line => line.length > 0)
    expect(lines.length).toBe(phase3Roles.length)
    const recorded = lines.map(line => JSON.parse(line).role)
    expect(recorded).toEqual(phase3Roles)
  })

  test('still accepts existing planner and implementer roles (no regression)', () => {
    recordOrchestraUsageEvent({
      role: 'planner',
      model: 'claude-opus-4-7',
      status: 'succeeded',
    })
    recordOrchestraUsageEvent({
      role: 'implementer',
      model: 'gpt-5.5',
      status: 'routed',
    })
    const lines = readFileSync(logPath, 'utf8')
      .split('\n')
      .filter(line => line.length > 0)
    expect(lines.length).toBe(2)
    expect(JSON.parse(lines[0]!).role).toBe('planner')
    expect(JSON.parse(lines[1]!).role).toBe('implementer')
  })
})
