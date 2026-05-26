import { describe, expect, test } from 'bun:test'

import {
  checkWorktreeAvailability,
  createShadowWorktrees,
  pruneShadowWorktrees,
  SHADOW_LABELS,
  type ExecFileRunner,
} from './worktreeManager.js'

type Recorded = {
  file: string
  args: string[]
  cwd?: string
}

function makeRunner(
  responses: Array<{
    match: (file: string, args: string[]) => boolean
    result: Awaited<ReturnType<ExecFileRunner>>
  }>,
): { runner: ExecFileRunner; calls: Recorded[] } {
  const calls: Recorded[] = []
  const runner: ExecFileRunner = async (file, args, options) => {
    calls.push({ file, args, cwd: options?.cwd })
    for (const r of responses) {
      if (r.match(file, args)) return r.result
    }
    return { stdout: '', stderr: 'no mock match', code: 1 }
  }
  return { runner, calls }
}

const ok = (stdout: string) => ({ stdout, stderr: '', code: 0 })
const fail = (stderr: string, code = 1) => ({ stdout: '', stderr, code })

describe('worktreeManager — availability', () => {
  test('detects non-git cwd via git rev-parse exit code', async () => {
    const { runner, calls } = makeRunner([
      {
        match: (f, a) => f === 'git' && a.includes('rev-parse'),
        result: fail('fatal: not a git repository', 128),
      },
    ])
    const result = await checkWorktreeAvailability('/tmp/non-git', runner)
    expect(result).toEqual({ ok: false, reason: 'not-git' })
    expect(calls.length).toBe(1)
    expect(calls[0]?.file).toBe('git')
    expect(calls[0]?.args).toContain('rev-parse')
    expect(calls[0]?.cwd).toBe('/tmp/non-git')
  })

  test('returns gitRoot on a real git repo', async () => {
    const { runner } = makeRunner([
      {
        match: (f, a) => f === 'git' && a.includes('rev-parse'),
        result: ok('/repo/root\n'),
      },
    ])
    const result = await checkWorktreeAvailability('/repo/sub', runner)
    expect(result).toEqual({ ok: true, gitRoot: '/repo/root' })
  })

  test('treats missing git binary as git-not-found', async () => {
    const { runner } = makeRunner([
      {
        match: (f, a) => f === 'git' && a.includes('rev-parse'),
        result: { stdout: '', stderr: '', code: 1, error: 'spawn git ENOENT' },
      },
    ])
    const result = await checkWorktreeAvailability('/anywhere', runner)
    expect(result).toEqual({ ok: false, reason: 'git-not-found' })
  })
})

describe('worktreeManager — createShadowWorktrees', () => {
  test('creates one worktree per shadow label with unique branch + path', async () => {
    const { runner, calls } = makeRunner([
      {
        match: (f, a) => f === 'git' && a[0] === 'worktree' && a[1] === 'add',
        result: ok(''),
      },
    ])
    const worktrees = await createShadowWorktrees({
      gitRoot: '/repo/root',
      taskId: 'task-42',
      runner,
    })
    expect(worktrees.length).toBe(SHADOW_LABELS.length)
    expect(worktrees.map(w => w.label).sort()).toEqual(
      [...SHADOW_LABELS].sort(),
    )
    const branches = new Set(worktrees.map(w => w.branch))
    const paths = new Set(worktrees.map(w => w.path))
    expect(branches.size).toBe(SHADOW_LABELS.length)
    expect(paths.size).toBe(SHADOW_LABELS.length)
    for (const w of worktrees) {
      expect(w.branch).toContain('task-42')
      expect(w.branch).toContain(w.label)
      expect(w.path).toContain('task-42')
      expect(w.path).toContain(w.label)
    }
    expect(calls.filter(c => c.args[0] === 'worktree' && c.args[1] === 'add')
      .length).toBe(SHADOW_LABELS.length)
  })

  test('rejects taskId with control characters (security)', async () => {
    const { runner } = makeRunner([])
    await expect(
      createShadowWorktrees({
        gitRoot: '/repo/root',
        taskId: 'evil\nrm -rf /',
        runner,
      }),
    ).rejects.toThrow(/taskId/i)
  })

  test('a single failing worktree add throws but does not corrupt return', async () => {
    let calls = 0
    const runner: ExecFileRunner = async (file, args) => {
      calls++
      if (file === 'git' && args[0] === 'worktree' && args[1] === 'add') {
        if (calls === 2) return fail('worktree already exists')
        return ok('')
      }
      return ok('')
    }
    await expect(
      createShadowWorktrees({
        gitRoot: '/repo/root',
        taskId: 'task-43',
        runner,
      }),
    ).rejects.toThrow(/worktree/i)
  })
})

describe('worktreeManager — pruneShadowWorktrees', () => {
  test('removes stale worktrees registered under .openclaude-shadows/', async () => {
    const list =
      'worktree /repo/root\n' +
      'HEAD abc\nbranch refs/heads/main\n\n' +
      'worktree /repo/root/.openclaude-shadows/task-1/gpt-a\n' +
      'HEAD def\nbranch refs/heads/openclaude-shadow/task-1/gpt-a\n\n' +
      'worktree /repo/root/.openclaude-shadows/task-1/gpt-b\n' +
      'HEAD ghi\nbranch refs/heads/openclaude-shadow/task-1/gpt-b\n'
    const removed: string[] = []
    const runner: ExecFileRunner = async (file, args) => {
      if (file === 'git' && args[0] === 'worktree' && args[1] === 'list') {
        return ok(list)
      }
      if (
        file === 'git' &&
        args[0] === 'worktree' &&
        args[1] === 'remove' &&
        typeof args[args.length - 1] === 'string'
      ) {
        removed.push(args[args.length - 1] as string)
        return ok('')
      }
      return ok('')
    }
    const result = await pruneShadowWorktrees({
      gitRoot: '/repo/root',
      runner,
    })
    expect(result.pruned.length).toBe(2)
    expect(result.pruned).toEqual(removed)
    expect(result.failed).toEqual([])
  })

  test('records failed removals in the failed list without throwing', async () => {
    const list =
      'worktree /repo/root\n' +
      'HEAD abc\nbranch refs/heads/main\n\n' +
      'worktree /repo/root/.openclaude-shadows/task-2/opus-shadow\n' +
      'HEAD jkl\nbranch refs/heads/openclaude-shadow/task-2/opus-shadow\n'
    const runner: ExecFileRunner = async (file, args) => {
      if (file === 'git' && args[0] === 'worktree' && args[1] === 'list') {
        return ok(list)
      }
      if (file === 'git' && args[0] === 'worktree' && args[1] === 'remove') {
        return fail('worktree locked', 128)
      }
      return ok('')
    }
    const result = await pruneShadowWorktrees({
      gitRoot: '/repo/root',
      runner,
    })
    expect(result.pruned).toEqual([])
    expect(result.failed.length).toBe(1)
  })
})
