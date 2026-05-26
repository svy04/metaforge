import { join } from 'path'

import { execFileNoThrowWithCwd } from '../../utils/execFileNoThrow.js'

/**
 * Phase 3 Shadow Executor — git worktree life-cycle.
 *
 * Three shadow worktrees per task: GPT-A primary alternative, GPT-B alternative
 * approach, Opus 4.7 shadow. Each lives under `{gitRoot}/.openclaude-shadows/
 * {taskId}/{label}` on a dedicated branch `openclaude-shadow/{taskId}/{label}`,
 * so the user's main worktree is never touched (D3=i: Phase 3 is read-only
 * compared, Phase 4 will decide promotion).
 *
 * All git invocations go through `execFileNoThrow` (no shell, structured
 * stdout/stderr/code/error). The runner is injectable for unit tests.
 */

export type ExecFileRunner = (
  file: string,
  args: string[],
  options?: { cwd?: string },
) => Promise<{ stdout: string; stderr: string; code: number; error?: string }>

export const SHADOW_LABELS = ['gpt-a', 'gpt-b', 'opus-shadow'] as const
export type ShadowLabel = (typeof SHADOW_LABELS)[number]

export type ShadowWorktree = {
  label: ShadowLabel
  path: string
  branch: string
  createdAt: string
}

export type WorktreeAvailability =
  | { ok: true; gitRoot: string }
  | { ok: false; reason: 'not-git' | 'git-not-found' | 'detached-bare' }

const SHADOW_DIR = '.openclaude-shadows'
const TASK_ID_PATTERN = /^[A-Za-z0-9._-]+$/

function defaultRunner(): ExecFileRunner {
  return async (file, args, options) => {
    return execFileNoThrowWithCwd(file, args, {
      cwd: options?.cwd,
      preserveOutputOnError: true,
    })
  }
}

function validateTaskId(taskId: string): void {
  if (!TASK_ID_PATTERN.test(taskId)) {
    throw new Error(
      `Invalid taskId for shadow worktree: ${JSON.stringify(taskId)}. ` +
        'taskId may only contain letters, digits, ".", "_", "-".',
    )
  }
}

export async function checkWorktreeAvailability(
  cwd: string,
  runner: ExecFileRunner = defaultRunner(),
): Promise<WorktreeAvailability> {
  const result = await runner('git', ['rev-parse', '--show-toplevel'], { cwd })
  if (result.error?.includes('ENOENT')) {
    return { ok: false, reason: 'git-not-found' }
  }
  if (result.code !== 0) {
    if (result.stderr.toLowerCase().includes('not a git repository')) {
      return { ok: false, reason: 'not-git' }
    }
    if (result.stderr.toLowerCase().includes('bare')) {
      return { ok: false, reason: 'detached-bare' }
    }
    return { ok: false, reason: 'not-git' }
  }
  const gitRoot = result.stdout.trim()
  if (!gitRoot) {
    return { ok: false, reason: 'not-git' }
  }
  return { ok: true, gitRoot }
}

function shadowPath(gitRoot: string, taskId: string, label: ShadowLabel): string {
  return join(gitRoot, SHADOW_DIR, taskId, label)
}

function shadowBranch(taskId: string, label: ShadowLabel): string {
  return `openclaude-shadow/${taskId}/${label}`
}

export async function createShadowWorktrees(params: {
  gitRoot: string
  taskId: string
  runner?: ExecFileRunner
  baseBranch?: string
}): Promise<ShadowWorktree[]> {
  validateTaskId(params.taskId)
  const runner = params.runner ?? defaultRunner()
  const created: ShadowWorktree[] = []
  for (const label of SHADOW_LABELS) {
    const path = shadowPath(params.gitRoot, params.taskId, label)
    const branch = shadowBranch(params.taskId, label)
    const args = ['worktree', 'add', '-b', branch, path]
    if (params.baseBranch) {
      args.push(params.baseBranch)
    }
    const result = await runner('git', args, { cwd: params.gitRoot })
    if (result.code !== 0) {
      throw new Error(
        `git worktree add failed for ${label}: ${result.stderr || result.error || 'unknown error'}`,
      )
    }
    created.push({
      label,
      path,
      branch,
      createdAt: new Date().toISOString(),
    })
  }
  return created
}

type WorktreeListEntry = {
  worktree: string
  branch?: string
  head?: string
}

function parseWorktreeListPorcelain(output: string): WorktreeListEntry[] {
  const entries: WorktreeListEntry[] = []
  let current: WorktreeListEntry | null = null
  for (const rawLine of output.split('\n')) {
    const line = rawLine.trim()
    if (line === '') {
      if (current) {
        entries.push(current)
        current = null
      }
      continue
    }
    if (line.startsWith('worktree ')) {
      if (current) entries.push(current)
      current = { worktree: line.slice('worktree '.length) }
    } else if (current && line.startsWith('branch ')) {
      current.branch = line.slice('branch '.length)
    } else if (current && line.startsWith('HEAD ')) {
      current.head = line.slice('HEAD '.length)
    }
  }
  if (current) entries.push(current)
  return entries
}

export async function pruneShadowWorktrees(params: {
  gitRoot: string
  runner?: ExecFileRunner
}): Promise<{ pruned: string[]; failed: string[] }> {
  const runner = params.runner ?? defaultRunner()
  const list = await runner('git', ['worktree', 'list', '--porcelain'], {
    cwd: params.gitRoot,
  })
  const pruned: string[] = []
  const failed: string[] = []
  if (list.code !== 0) {
    return { pruned, failed }
  }
  const entries = parseWorktreeListPorcelain(list.stdout)
  for (const entry of entries) {
    if (!entry.worktree.includes(SHADOW_DIR)) continue
    const removeResult = await runner(
      'git',
      ['worktree', 'remove', '--force', entry.worktree],
      { cwd: params.gitRoot },
    )
    if (removeResult.code === 0) {
      pruned.push(entry.worktree)
    } else {
      failed.push(entry.worktree)
    }
  }
  return { pruned, failed }
}
