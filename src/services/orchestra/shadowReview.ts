import { writeFileSync, mkdirSync, existsSync } from 'fs'
import { dirname, join, resolve } from 'path'

import { execFileNoThrowWithCwd as runShell } from '../../utils/execFileNoThrow.js'
import { sideQuery } from '../../utils/sideQuery.js'
import {
  DEFAULT_CODEX_BASE_URL,
  resolveRuntimeCodexCredentials,
} from '../api/providerConfig.js'
import { collectCodexCompletedResponse } from '../api/codexShim.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  createSystemMessage,
  type SystemInformationalMessage,
} from '../../utils/messages.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { shouldUseClaudeAIAuth } from '../oauth/client.js'
import { OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { EFFORT_BETA_HEADER } from '../../constants/betas.js'
import type { ToolUseContext } from '../../Tool.js'
import { getInitialSettings } from '../../utils/settings/settings.js'

import {
  buildEvidenceMatrix,
  type EvidenceMatrix,
  type UnderstandableJudgeFn,
} from './evidenceArbiter.js'
import {
  buildCrossReviewMatrix,
  formatMatrixDetail,
  formatMatrixSummary,
  type CrossReviewMatrix,
  type ReviewerFn,
} from './crossReview.js'
import { resolveOrchestraSettings } from './config.js'
import {
  formatHumanGateMessage,
  humanGateMessageLevel,
} from './humanGate.js'
import {
  recordOrchestraUsageEvent,
  type OrchestraUsageEvent,
  type OrchestraUsageRecorder,
} from './usageLog.js'
import {
  runShadowExecutors,
  shadowSystemPromptFor,
  type ShadowCandidate,
  type ShadowWorkerInput,
  type ShadowWorkerSet,
} from './shadowExecutor.js'
import {
  checkWorktreeAvailability,
  createShadowWorktrees,
  pruneShadowWorktrees,
  type ShadowLabel,
  type ShadowWorktree,
} from './worktreeManager.js'
import { writeLatestShadowReview } from './promotionStore.js'

export type ShadowReviewResult = {
  summaryMessage?: SystemInformationalMessage
  humanGateMessage?: SystemInformationalMessage
  diagnostic?: string
  matrix?: CrossReviewMatrix
  evidenceMatrix?: EvidenceMatrix
}

export type ShadowReviewParams = {
  taskScope: { intent: string; targetFiles?: string[] }
  cwd: string
  signal?: AbortSignal
  toolUseContext: ToolUseContext
  workers?: ShadowWorkerSet
  reviewers?: { gpt: ReviewerFn; opus: ReviewerFn }
  understandableJudge?: UnderstandableJudgeFn
  recordUsageEvent?: OrchestraUsageRecorder
  skipOAuthRefresh?: boolean
}

const DETAIL_DIR_REL = join('.planning', 'phase-3')
const WORKER_TIMEOUT_MS = 180_000

// Session-scoped guard: emit the "Phase 3 skipped because cwd is not-git"
// message at most ONCE per process. Without this the user sees the same
// notice on every assistant turn — pure noise after the first read.
let notGitNoticeEmitted = false

function extractText(blocks: { type: string; text?: string }[]): string {
  return blocks
    .map(b => (b.type === 'text' && typeof b.text === 'string' ? b.text : ''))
    .filter(t => t.length > 0)
    .join('\n')
}

function extractJsonBody(text: string): string {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  if (fenced?.[1]) return fenced[1].trim()
  const firstBrace = text.indexOf('{')
  const lastBrace = text.lastIndexOf('}')
  if (firstBrace >= 0 && lastBrace > firstBrace) {
    return text.slice(firstBrace, lastBrace + 1)
  }
  return text.trim()
}

type WorkerProposal = {
  summary?: string
  files?: { path: string; content: string }[]
}

function parseWorkerProposal(text: string): WorkerProposal {
  try {
    const parsed = JSON.parse(extractJsonBody(text)) as Record<string, unknown>
    const summary = typeof parsed.summary === 'string' ? parsed.summary : ''
    const filesRaw = Array.isArray(parsed.files) ? parsed.files : []
    const files = filesRaw
      .filter(
        (f): f is { path: string; content: string } =>
          typeof f === 'object' &&
          f !== null &&
          typeof (f as { path?: unknown }).path === 'string' &&
          typeof (f as { content?: unknown }).content === 'string',
      )
      .map(f => ({ path: f.path, content: f.content }))
    return { summary, files }
  } catch {
    return {}
  }
}

function isSafeRelativePath(p: string): boolean {
  if (!p || p.includes('\0')) return false
  if (/^(?:[a-zA-Z]:)?[\\/]/.test(p)) return false
  const segments = p.split(/[\\/]/)
  if (segments.some(s => s === '..' || s === '')) return false
  return true
}

function applyProposalToWorktree(
  worktreePath: string,
  proposal: WorkerProposal,
): { written: string[]; rejected: string[] } {
  const written: string[] = []
  const rejected: string[] = []
  for (const file of proposal.files ?? []) {
    if (!isSafeRelativePath(file.path)) {
      rejected.push(file.path)
      continue
    }
    const target = resolve(worktreePath, file.path)
    if (!target.startsWith(resolve(worktreePath))) {
      rejected.push(file.path)
      continue
    }
    try {
      const dir = dirname(target)
      if (dir && !existsSync(dir)) {
        mkdirSync(dir, { recursive: true })
      }
      writeFileSync(target, file.content, 'utf8')
      written.push(file.path)
    } catch {
      rejected.push(file.path)
    }
  }
  return { written, rejected }
}

async function captureWorktreeDiff(worktreePath: string): Promise<string> {
  // Stage untracked files first so `git diff HEAD` can show them; otherwise
  // worker-created files appear as untracked and the diff reads empty.
  await runShell('git', ['add', '-A'], {
    cwd: worktreePath,
    preserveOutputOnError: true,
  })
  const result = await runShell('git', ['diff', 'HEAD'], {
    cwd: worktreePath,
    preserveOutputOnError: true,
  })
  return result.stdout.slice(0, 8192)
}

/**
 * v0.2 Phase 3 production helper — bypass sideQuery for the GPT shadow
 * workers because sideQuery routes through the Anthropic SDK. Codex is
 * OpenAI-compatible (Responses API), so we call it directly with the user's
 * Codex credentials. Falls back to throwing a recognizable error if the user
 * has no Codex auth, which then surfaces in jsonl as `status: failed`.
 */
async function callCodexCompletion(params: {
  prompt: string
  system: string
  signal?: AbortSignal
  maxOutputTokens?: number
}): Promise<string> {
  const creds = resolveRuntimeCodexCredentials()
  // User mandate (2026-05-07): "api 방식은 모두 안쓸거고 둘다 gpt 계정과
  // claude 계정으로". accessToken (ChatGPT-account OAuth) is preferred. The
  // apiKey field is honoured as a fallback because OpenClaude's
  // ResolvedCodexCredentials packs the OAuth Bearer token into apiKey on
  // some auth code paths (e.g. CODEX_HOME / auth.json discovery). The user
  // can fully enforce OAuth-only by clearing API-key env vars
  // (CODEX_API_KEY, OPENAI_API_KEY) so only the OAuth-discovered token
  // remains.
  const auth = creds.apiKey
  if (!auth) {
    throw new Error(
      'Codex OAuth missing — sign in via ChatGPT/Codex (run the OpenClaude codex login flow).',
    )
  }
  const baseURL = DEFAULT_CODEX_BASE_URL
  const model =
    process.env.OPENCLAUDE_ORCHESTRA_SHADOW_GPT?.trim() || 'gpt-5.5'
  const body: Record<string, unknown> = {
    model,
    input: [
      {
        type: 'message',
        role: 'user',
        content: [{ type: 'input_text', text: params.prompt }],
      },
    ],
    instructions: params.system,
    store: false,
    stream: true,
    // gpt-5.5 xhigh effort by user mandate. Codex Responses API accepts
    // reasoning.effort with the same enum the OpenClaude main loop uses.
    reasoning: { effort: 'xhigh' },
  }
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${auth}`,
  }
  if (creds.accountId) {
    headers['chatgpt-account-id'] = creds.accountId
  }
  const response = await fetch(`${baseURL}/responses`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
    signal: params.signal,
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(`Codex API ${response.status}: ${text.slice(0, 300)}`)
  }
  const completed = await collectCodexCompletedResponse(
    response as never,
    params.signal,
  )
  const output = (completed as { output?: unknown[] }).output ?? []
  for (const item of output as Array<{
    type?: unknown
    content?: unknown
  }>) {
    if (item?.type === 'message' && Array.isArray(item.content)) {
      for (const c of item.content as Array<{ type?: unknown; text?: unknown }>) {
        if (c?.type === 'output_text' && typeof c.text === 'string') {
          return c.text
        }
      }
    }
  }
  return ''
}

function workerPrompt(
  input: ShadowWorkerInput,
  label: ShadowLabel,
): string {
  return [
    shadowSystemPromptFor(label),
    '',
    'Task intent:',
    input.taskScope.intent,
    '',
    input.taskScope.targetFiles && input.taskScope.targetFiles.length > 0
      ? `Targeted files (relative): ${input.taskScope.targetFiles.join(', ')}`
      : 'No specific target files provided; choose minimally.',
    '',
    'Respond with JSON ONLY (no surrounding prose, no markdown fence). Shape:',
    '{"summary":"one line description of the change","files":[{"path":"relative/path.ext","content":"full file contents"}]}',
    '',
    'Rules:',
    '- All file paths must be relative and inside the working dir.',
    '- "content" is the FULL final file contents, not a diff.',
    '- Keep the change minimal and scoped to the task.',
    '- If you cannot reasonably solve it, return {"summary":"unable","files":[]}.',
  ].join('\n')
}

async function gptShadowWorker(
  input: ShadowWorkerInput,
  label: 'gpt-a' | 'gpt-b',
): Promise<ShadowCandidate> {
  try {
    const text = await callCodexCompletion({
      prompt: workerPrompt(input, label),
      system:
        'You are a code-patch generator. Output JSON only — no prose, no markdown fence.',
      signal: input.signal ?? AbortSignal.timeout(WORKER_TIMEOUT_MS),
      maxOutputTokens: 4096,
    })
    const proposal = parseWorkerProposal(text)
    const apply = applyProposalToWorktree(input.worktree.path, proposal)
    if (apply.written.length === 0) {
      // No files != worker failure. Modern code models routinely answer
      //   {"summary":"unable","files":[]}
      // when the prompt has nothing meaningful to patch (e.g. a plain
      // greeting). We mark the candidate 'skipped' instead of 'failed' so
      // the cross-review + evidence arbiter still produces a coherent
      // matrix entry without polluting failure metrics. Real failures
      // (network/auth/throw) still hit the catch below as 'failed'.
      const unsafePaths = apply.rejected.length
      const reason =
        proposal.files && proposal.files.length > 0
          ? `all proposed files rejected (${unsafePaths} unsafe paths)`
          : 'worker chose not to produce a patch (empty files array)'
      return {
        label: input.worktree.label,
        worktreePath: input.worktree.path,
        status: 'skipped',
        error: reason,
        patchSummary: proposal.summary,
      }
    }
    const diff = await captureWorktreeDiff(input.worktree.path)
    return {
      label: input.worktree.label,
      worktreePath: input.worktree.path,
      status: 'completed',
      patchSummary: proposal.summary || `${label} candidate`,
      filesChanged: apply.written,
      diff,
    }
  } catch (error) {
    return {
      label: input.worktree.label,
      worktreePath: input.worktree.path,
      status: 'failed',
      error: error instanceof Error ? error.message : String(error),
    }
  }
}

async function opusShadowWorker(
  input: ShadowWorkerInput,
): Promise<ShadowCandidate> {
  try {
    const response = await sideQuery({
      model: 'claude-opus-4-7',
      max_tokens: 4096,
      system:
        'You are Claude Opus acting as the configured shadow patch generator (야당 그림자). Output JSON only.',
      messages: [{ role: 'user', content: workerPrompt(input, 'opus-shadow') }],
      querySource: 'orchestra_shadow_worker' as never,
      maxRetries: 0,
      signal: input.signal ?? AbortSignal.timeout(WORKER_TIMEOUT_MS),
      skipSystemPromptPrefix: false,
      forceFirstParty: true,
      effort: 'max',
    })
    const text = extractText(response.content as never)
    const proposal = parseWorkerProposal(text)
    const apply = applyProposalToWorktree(input.worktree.path, proposal)
    if (apply.written.length === 0) {
      return {
        label: 'opus-shadow',
        worktreePath: input.worktree.path,
        status: 'failed',
        error:
          proposal.files && proposal.files.length > 0
            ? `all proposed files rejected (${apply.rejected.length} unsafe paths)`
            : 'opus shadow returned no files',
        patchSummary: proposal.summary,
      }
    }
    const diff = await captureWorktreeDiff(input.worktree.path)
    return {
      label: 'opus-shadow',
      worktreePath: input.worktree.path,
      status: 'completed',
      patchSummary: proposal.summary || 'opus shadow candidate',
      filesChanged: apply.written,
      diff,
    }
  } catch (error) {
    return {
      label: 'opus-shadow',
      worktreePath: input.worktree.path,
      status: 'failed',
      error: error instanceof Error ? error.message : String(error),
    }
  }
}

const PRODUCTION_WORKERS: ShadowWorkerSet = {
  'gpt-a': input => gptShadowWorker(input, 'gpt-a'),
  'gpt-b': input => gptShadowWorker(input, 'gpt-b'),
  'opus-shadow': opusShadowWorker,
}

function reviewerPrompt(candidate: ShadowCandidate): string {
  return [
    'You are reviewing a candidate code patch.',
    `Candidate label: ${candidate.label}`,
    `Summary: ${candidate.patchSummary ?? 'n/a'}`,
    '',
    'Diff (truncated to 8KB):',
    candidate.diff?.slice(0, 8192) ?? '(empty diff)',
    '',
    'Respond with JSON ONLY:',
    '{"verdict":"green|yellow|red","scoresOutOf5":{"correctness":0,"minimality":0,"scopeFit":0},"rationale":"one short sentence in Korean"}',
  ].join('\n')
}

type ReviewerJson = {
  verdict?: 'green' | 'yellow' | 'red'
  scoresOutOf5?: { correctness?: number; minimality?: number; scopeFit?: number }
  rationale?: string
}

function parseReviewerOutput(
  text: string,
): Awaited<ReturnType<ReviewerFn>> {
  try {
    const parsed = JSON.parse(extractJsonBody(text)) as ReviewerJson
    const verdict =
      parsed.verdict === 'green' || parsed.verdict === 'red'
        ? parsed.verdict
        : 'yellow'
    const s = parsed.scoresOutOf5 ?? {}
    return {
      verdict,
      scoresOutOf5: {
        correctness: typeof s.correctness === 'number' ? s.correctness : 3,
        minimality: typeof s.minimality === 'number' ? s.minimality : 3,
        scopeFit: typeof s.scopeFit === 'number' ? s.scopeFit : 3,
      },
      rationale: typeof parsed.rationale === 'string' ? parsed.rationale : '',
    }
  } catch {
    return {
      verdict: 'yellow',
      scoresOutOf5: { correctness: 0, minimality: 0, scopeFit: 0 },
      rationale: 'reviewer JSON parse failed',
    }
  }
}

const gptReviewer: ReviewerFn = async ({ candidate, signal }) => {
  try {
    const text = await callCodexCompletion({
      prompt: reviewerPrompt(candidate),
      system: 'Code reviewer. Output JSON only.',
      signal: signal ?? AbortSignal.timeout(WORKER_TIMEOUT_MS),
      maxOutputTokens: 1024,
    })
    return parseReviewerOutput(text)
  } catch (e) {
    return {
      verdict: 'red',
      scoresOutOf5: { correctness: 0, minimality: 0, scopeFit: 0 },
      rationale: `gpt reviewer failed: ${
        e instanceof Error ? e.message : String(e)
      }`,
    }
  }
}

const opusReviewer: ReviewerFn = async ({ candidate, signal }) => {
  const response = await sideQuery({
    model: 'claude-opus-4-7',
    max_tokens: 1024,
    system:
      'You are Claude Opus reviewing a candidate patch as the configured opposition (야당). Output JSON only.',
    messages: [{ role: 'user', content: reviewerPrompt(candidate) }],
    querySource: 'orchestra_cross_reviewer_opus' as never,
    maxRetries: 0,
    signal: signal ?? AbortSignal.timeout(WORKER_TIMEOUT_MS),
    skipSystemPromptPrefix: false,
    forceFirstParty: true,
    effort: 'max',
  })
  return parseReviewerOutput(extractText(response.content as never))
}

const PRODUCTION_REVIEWERS = { gpt: gptReviewer, opus: opusReviewer }

const PRODUCTION_JUDGE: UnderstandableJudgeFn = async ({
  candidate,
  taskScope,
  signal,
}) => {
  try {
    const text = await callCodexCompletion({
      prompt: [
        `Task: ${taskScope.intent}`,
        `Candidate ${candidate.label} summary: ${candidate.patchSummary ?? '?'}`,
        `Diff (8KB cap):\n${candidate.diff?.slice(0, 8192) ?? '(empty)'}`,
        '',
        'Respond JSON: {"verdict":"pass|fail"}',
      ].join('\n'),
      system:
        'Judge whether a candidate patch is understandable. Output JSON only.',
      signal: signal ?? AbortSignal.timeout(WORKER_TIMEOUT_MS),
      maxOutputTokens: 256,
    })
    const parsed = JSON.parse(extractJsonBody(text)) as { verdict?: string }
    return { verdict: parsed.verdict === 'fail' ? 'fail' : 'pass' }
  } catch {
    return { verdict: 'fail' }
  }
}

async function safeRecord(
  recorder: OrchestraUsageRecorder,
  event: OrchestraUsageEvent,
): Promise<void> {
  try {
    await recorder(event)
  } catch (e) {
    logForDebugging(
      `shadow review usage record failed: ${e instanceof Error ? e.message : String(e)}`,
      { level: 'warn' },
    )
  }
}

export async function createOrchestraShadowReview(
  params: ShadowReviewParams,
): Promise<ShadowReviewResult> {
  const settings =
    params.toolUseContext.getAppState().settings ?? getInitialSettings()
  const orchestra = resolveOrchestraSettings(settings)
  if (!orchestra.shadowEnabled) return {}

  const recorder = params.recordUsageEvent ?? recordOrchestraUsageEvent

  const availability = await checkWorktreeAvailability(params.cwd)
  if (!availability.ok) {
    if (notGitNoticeEmitted) {
      // Already told the user once this process; subsequent turns are
      // silent so the same notice does not echo on every reply.
      return {}
    }
    notGitNoticeEmitted = true
    return {
      summaryMessage: createSystemMessage(
        `[Phase 3 Cross-Review] skipped: cwd is ${availability.reason} — shadowEnabled requires a git repository to run worktree-isolated candidates. (this notice appears only once per session)`,
        'warning',
      ),
    }
  }

  if (!params.skipOAuthRefresh) {
    try {
      await checkAndRefreshOAuthTokenIfNeeded()
    } catch {
      /* surfaced below */
    }
    const tokens = getClaudeAIOAuthTokens()
    if (!tokens?.accessToken || !shouldUseClaudeAIAuth(tokens.scopes)) {
      return {
        summaryMessage: createSystemMessage(
          '[Phase 3 Cross-Review] skipped: Claude OAuth credentials missing — Opus shadow worker cannot run. Sign in to Claude before enabling shadowEnabled.',
          'warning',
        ),
      }
    }
  }

  const taskId = `t-${Date.now()}`
  let worktrees: ShadowWorktree[]
  try {
    await pruneShadowWorktrees({ gitRoot: availability.gitRoot })
    worktrees = await createShadowWorktrees({
      gitRoot: availability.gitRoot,
      taskId,
    })
  } catch (error) {
    return {
      diagnostic: `Phase 3 worktree setup failed: ${
        error instanceof Error ? error.message : String(error)
      }`,
    }
  }

  const workers: ShadowWorkerSet = params.workers ?? PRODUCTION_WORKERS
  const reviewers = params.reviewers ?? PRODUCTION_REVIEWERS
  const judge = params.understandableJudge ?? PRODUCTION_JUDGE

  await safeRecord(recorder, {
    role: 'shadow-gpt-b',
    model: 'gpt-5.5',
    status: 'started',
  })
  await safeRecord(recorder, {
    role: 'shadow-opus',
    model: 'claude-opus-4-7',
    status: 'started',
  })
  const shadowResult = await runShadowExecutors({
    taskScope: params.taskScope,
    worktrees,
    workers,
    signal: params.signal,
  })
  for (const c of shadowResult.candidates) {
    if (c.label === 'gpt-b') {
      await safeRecord(recorder, {
        role: 'shadow-gpt-b',
        model: 'gpt-5.5',
        status:
          c.status === 'completed'
            ? 'succeeded'
            : c.status === 'skipped'
              ? 'skipped'
              : 'failed',
        ...(c.error && { errorMessage: c.error }),
      })
    } else if (c.label === 'opus-shadow') {
      await safeRecord(recorder, {
        role: 'shadow-opus',
        model: 'claude-opus-4-7',
        status:
          c.status === 'completed'
            ? 'succeeded'
            : c.status === 'skipped'
              ? 'skipped'
              : 'failed',
        ...(c.error && { errorMessage: c.error }),
      })
    }
  }

  await safeRecord(recorder, {
    role: 'cross-reviewer-gpt',
    model: 'gpt-5.5',
    status: 'started',
  })
  await safeRecord(recorder, {
    role: 'cross-reviewer-opus',
    model: 'claude-opus-4-7',
    status: 'started',
  })
  const matrix = await buildCrossReviewMatrix({
    candidates: shadowResult.candidates,
    reviewers,
    signal: params.signal,
  })
  await safeRecord(recorder, {
    role: 'cross-reviewer-gpt',
    model: 'gpt-5.5',
    status: 'succeeded',
  })
  await safeRecord(recorder, {
    role: 'cross-reviewer-opus',
    model: 'claude-opus-4-7',
    status: 'succeeded',
  })

  const evidence = await buildEvidenceMatrix({
    candidates: shadowResult.candidates,
    crossReview: matrix,
    taskScope: params.taskScope,
    understandableJudge: judge,
    testEvidence: { ran: false },
    signal: params.signal,
  })

  let detailDiagnostic: string | undefined
  try {
    const detailDir = join(availability.gitRoot, DETAIL_DIR_REL)
    if (!existsSync(detailDir)) mkdirSync(detailDir, { recursive: true })
    const ts = new Date().toISOString().replace(/[:.]/g, '-')
    const detailPath = join(detailDir, `cross-review-${ts}.md`)
    writeFileSync(detailPath, formatMatrixDetail(matrix), 'utf8')
    const latestPath = await writeLatestShadowReview(availability.gitRoot, {
      taskScope: params.taskScope,
      candidates: shadowResult.candidates,
      matrix,
      evidenceMatrix: evidence,
      detailPath,
    })
    detailDiagnostic =
      `Phase 3 detail saved: ${detailPath}; ` +
      `latest review saved: ${latestPath}`
  } catch (e) {
    detailDiagnostic = `Phase 3 artifact write failed: ${
      e instanceof Error ? e.message : String(e)
    }`
  }

  return {
    summaryMessage: createSystemMessage(formatMatrixSummary(matrix), 'info'),
    humanGateMessage: createSystemMessage(
      formatHumanGateMessage(evidence),
      humanGateMessageLevel(evidence),
    ),
    matrix,
    evidenceMatrix: evidence,
    diagnostic: detailDiagnostic,
  }
}
