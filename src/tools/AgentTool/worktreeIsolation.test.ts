import { describe, expect, test } from 'bun:test'

import {
  resolveAgentWorktreeIsolation,
  shouldFallbackFromUnavailableWorktree,
} from './worktreeIsolation.js'

const unavailable =
  'Cannot create agent worktree: not in a git repository and no WorktreeCreate hooks are configured.'

describe('agent worktree isolation fallback', () => {
  test('falls back for verification agents even when worktree isolation was explicit', () => {
    expect(
      shouldFallbackFromUnavailableWorktree({
        message: unavailable,
        requestedIsolation: 'worktree',
        agentType: 'verification',
      }),
    ).toBe(true)
  })

  test('falls back for explicit worktree isolation when no worktree backend is available', () => {
    expect(
      shouldFallbackFromUnavailableWorktree({
        message: unavailable,
        requestedIsolation: 'worktree',
        agentType: 'worker',
      }),
    ).toBe(true)
  })

  test('falls back for definition-level worktree isolation', () => {
    expect(
      shouldFallbackFromUnavailableWorktree({
        message: unavailable,
        requestedIsolation: undefined,
        agentType: 'worker',
      }),
    ).toBe(true)
  })

  test('does not hide unrelated worktree creation failures', () => {
    expect(
      shouldFallbackFromUnavailableWorktree({
        message: 'git worktree add failed: permission denied',
        requestedIsolation: undefined,
        agentType: 'verification',
      }),
    ).toBe(false)
  })

  test('falls back when a configured WorktreeCreate hook is not a worktree provider', () => {
    expect(
      shouldFallbackFromUnavailableWorktree({
        message: 'WorktreeCreate hook failed: no successful output',
        requestedIsolation: 'worktree',
        agentType: 'worker',
      }),
    ).toBe(true)
  })

  test('downgrades worktree isolation before launch when no backend is available', () => {
    expect(
      resolveAgentWorktreeIsolation({
        effectiveIsolation: 'worktree',
        hasWorktreeCreateHook: false,
        gitRoot: null,
      }),
    ).toEqual({
      attemptWorktree: false,
      downgraded: true,
    })
  })

  test('keeps worktree isolation when a hook or git repo is available', () => {
    expect(
      resolveAgentWorktreeIsolation({
        effectiveIsolation: 'worktree',
        hasWorktreeCreateHook: true,
        gitRoot: null,
      }).attemptWorktree,
    ).toBe(true)
    expect(
      resolveAgentWorktreeIsolation({
        effectiveIsolation: 'worktree',
        hasWorktreeCreateHook: false,
        gitRoot: 'C:/repo',
      }).attemptWorktree,
    ).toBe(true)
  })
})
