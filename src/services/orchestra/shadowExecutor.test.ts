import { describe, expect, test } from 'bun:test'

import {
  runShadowExecutors,
  type ShadowCandidate,
  type ShadowWorkerSet,
} from './shadowExecutor.js'
import { SHADOW_LABELS, type ShadowWorktree } from './worktreeManager.js'

function fixtureWorktrees(): ShadowWorktree[] {
  return SHADOW_LABELS.map(label => ({
    label,
    path: `/repo/.openclaude-shadows/task-1/${label}`,
    branch: `openclaude-shadow/task-1/${label}`,
    createdAt: '2026-05-07T00:00:00.000Z',
  }))
}

function makeWorker(
  result: Partial<ShadowCandidate>,
): ShadowWorkerSet[keyof ShadowWorkerSet] {
  return async ({ worktree }) => ({
    label: worktree.label,
    worktreePath: worktree.path,
    status: 'completed',
    patchSummary: `${worktree.label} did the thing`,
    ...result,
  })
}

describe('shadowExecutor — runShadowExecutors', () => {
  test('produces one candidate per worktree label, in label order', async () => {
    const workers: ShadowWorkerSet = {
      'gpt-a': makeWorker({}),
      'gpt-b': makeWorker({}),
      'opus-shadow': makeWorker({}),
    }
    const result = await runShadowExecutors({
      taskScope: { intent: 'add a license header' },
      worktrees: fixtureWorktrees(),
      workers,
    })
    expect(result.candidates.length).toBe(SHADOW_LABELS.length)
    expect(result.candidates.map(c => c.label)).toEqual([...SHADOW_LABELS])
    for (const c of result.candidates) {
      expect(c.status).toBe('completed')
      expect(c.worktreePath).toContain(c.label)
    }
    expect(result.taskId).toBe('task-1')
    expect(typeof result.durationMs).toBe('number')
  })

  test('a single worker throwing yields a failed candidate but lets the rest complete', async () => {
    const workers: ShadowWorkerSet = {
      'gpt-a': makeWorker({}),
      'gpt-b': async () => {
        throw new Error('boom')
      },
      'opus-shadow': makeWorker({}),
    }
    const result = await runShadowExecutors({
      taskScope: { intent: 'cause one to fail' },
      worktrees: fixtureWorktrees(),
      workers,
    })
    const byLabel = Object.fromEntries(
      result.candidates.map(c => [c.label, c]),
    )
    expect(byLabel['gpt-a']?.status).toBe('completed')
    expect(byLabel['gpt-b']?.status).toBe('failed')
    expect(byLabel['gpt-b']?.error).toContain('boom')
    expect(byLabel['opus-shadow']?.status).toBe('completed')
  })

  test('aborted signal short-circuits remaining workers as skipped', async () => {
    const controller = new AbortController()
    const workers: ShadowWorkerSet = {
      'gpt-a': async () => {
        controller.abort()
        return {
          label: 'gpt-a',
          worktreePath: 'p',
          status: 'completed' as const,
        }
      },
      'gpt-b': makeWorker({}),
      'opus-shadow': makeWorker({}),
    }
    const result = await runShadowExecutors({
      taskScope: { intent: 'abort mid-flight' },
      worktrees: fixtureWorktrees(),
      workers,
      signal: controller.signal,
    })
    const byLabel = Object.fromEntries(
      result.candidates.map(c => [c.label, c]),
    )
    expect(byLabel['gpt-a']?.status).toBe('completed')
    expect(byLabel['gpt-b']?.status).toBe('skipped')
    expect(byLabel['opus-shadow']?.status).toBe('skipped')
  })

  test('throws when a worker for one of the labels is missing (no silent gap)', async () => {
    const partial = {
      'gpt-a': makeWorker({}),
      'opus-shadow': makeWorker({}),
    } as unknown as ShadowWorkerSet
    await expect(
      runShadowExecutors({
        taskScope: { intent: 'missing worker' },
        worktrees: fixtureWorktrees(),
        workers: partial,
      }),
    ).rejects.toThrow(/gpt-b/)
  })
})
