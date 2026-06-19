import { SHADOW_LABELS, type ShadowLabel, type ShadowWorktree } from './worktreeManager.js'

/**
 * Phase 3 Shadow Executor — orchestrates 3 candidate patches in isolated
 * worktrees: GPT-A primary alternative, GPT-B alternative-approach, Claude Opus
 * shadow. Each worker is responsible for actually mutating its own worktree
 * (commits + diff capture) and returning a ShadowCandidate summary.
 *
 * The worker functions themselves are wired in a follow-up: production
 * implementations need access to the OpenClaude sub-agent / Codex API and
 * Claude OAuth side-query infra. Phase 3.2 here defines the contract +
 * the dispatch loop so the rest of the orchestra (cross-review, query.ts
 * hook) can be built on a stable surface.
 */

export type ShadowCandidateStatus = 'completed' | 'failed' | 'skipped'

export type ShadowCandidate = {
  label: ShadowLabel
  worktreePath: string
  status: ShadowCandidateStatus
  patchSummary?: string
  filesChanged?: string[]
  diff?: string
  error?: string
}

export type ShadowTaskScope = {
  intent: string
  targetFiles?: string[]
}

export type ShadowWorkerInput = {
  worktree: ShadowWorktree
  taskScope: ShadowTaskScope
  signal?: AbortSignal
}

export type ShadowWorkerFn = (input: ShadowWorkerInput) => Promise<ShadowCandidate>

export type ShadowWorkerSet = Record<ShadowLabel, ShadowWorkerFn>

export type ShadowExecutionResult = {
  candidates: ShadowCandidate[]
  taskId: string
  durationMs: number
}

const TASK_ID_FROM_PATH = /[\\/]\.openclaude-shadows[\\/]([^\\/]+)[\\/]/

function extractTaskId(worktrees: ShadowWorktree[]): string {
  for (const w of worktrees) {
    const match = w.path.match(TASK_ID_FROM_PATH)
    if (match?.[1]) return match[1]
  }
  return 'unknown-task'
}

function assertCompleteWorkerSet(workers: Partial<ShadowWorkerSet>): asserts workers is ShadowWorkerSet {
  for (const label of SHADOW_LABELS) {
    if (typeof workers[label] !== 'function') {
      throw new Error(
        `runShadowExecutors: missing worker for label "${label}". Provide a worker for every shadow label.`,
      )
    }
  }
}

function skippedCandidate(worktree: ShadowWorktree, reason: string): ShadowCandidate {
  return {
    label: worktree.label,
    worktreePath: worktree.path,
    status: 'skipped',
    error: reason,
  }
}

export async function runShadowExecutors(params: {
  taskScope: ShadowTaskScope
  worktrees: ShadowWorktree[]
  workers: Partial<ShadowWorkerSet>
  signal?: AbortSignal
}): Promise<ShadowExecutionResult> {
  assertCompleteWorkerSet(params.workers)
  const start = Date.now()
  const candidates: ShadowCandidate[] = []
  // Iterate in canonical SHADOW_LABELS order so the result is deterministic
  // regardless of how the worktrees array was constructed by the caller.
  const byLabel = new Map(params.worktrees.map(w => [w.label, w]))
  for (const label of SHADOW_LABELS) {
    const worktree = byLabel.get(label)
    if (!worktree) {
      candidates.push({
        label,
        worktreePath: '',
        status: 'skipped',
        error: `no worktree provided for label ${label}`,
      })
      continue
    }
    if (params.signal?.aborted) {
      candidates.push(skippedCandidate(worktree, 'aborted before worker dispatch'))
      continue
    }
    const worker = params.workers[label]!
    try {
      const candidate = await worker({
        worktree,
        taskScope: params.taskScope,
        signal: params.signal,
      })
      candidates.push(candidate)
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error)
      candidates.push({
        label,
        worktreePath: worktree.path,
        status: 'failed',
        error: message,
      })
    }
  }
  return {
    candidates,
    taskId: extractTaskId(params.worktrees),
    durationMs: Date.now() - start,
  }
}

/**
 * Differentiates the system prompt for each shadow label so the 3 workers
 * actually take different approaches rather than producing 3 identical
 * patches. Used by future production worker wiring.
 */
export function shadowSystemPromptFor(label: ShadowLabel): string {
  switch (label) {
    case 'gpt-a':
      return 'You are GPT-A, the primary executor. Solve the task with your best, most direct approach.'
    case 'gpt-b':
      return 'You are GPT-B. The other GPT instance is solving this same task with its primary approach. You MUST take a deliberately different approach — different data structure, different algorithm, different abstraction boundary. If your first instinct matches GPT-A, pick the second-best alternative.'
    case 'opus-shadow':
      return 'You are Claude Opus acting as the configured shadow executor (야당 그림자 구현). The visible lead is GPT 5.5. Produce your own implementation independently, paying special attention to risks and edge cases the GPT path may underweight.'
  }
}
