import {
  copyFileSync,
  existsSync,
  mkdirSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs'
import { dirname, join, relative, resolve } from 'node:path'

import { evaluatePromoteRequest } from './promote.js'
import type { CrossReviewMatrix } from './crossReview.js'
import type { EvidenceMatrix } from './evidenceArbiter.js'
import type { ShadowCandidate } from './shadowExecutor.js'
import type { ShadowLabel } from './worktreeManager.js'
import { checkWorktreeAvailability, pruneShadowWorktrees } from './worktreeManager.js'

const DETAIL_DIR_REL = join('.planning', 'phase-3')
const LATEST_REVIEW_FILE = 'latest-shadow-review.json'

export type StoredShadowReview = {
  generatedAt: string
  taskScope: { intent: string; targetFiles?: string[] }
  candidates: ShadowCandidate[]
  matrix: CrossReviewMatrix
  evidenceMatrix: EvidenceMatrix
  detailPath?: string
}

export type WriteLatestShadowReviewParams = Omit<
  StoredShadowReview,
  'generatedAt'
> & {
  generatedAt?: string
}

export type ApplyStoredShadowCandidateResult =
  | { ok: true; appliedLabel: ShadowLabel; appliedFiles: string[] }
  | {
      ok: false
      reason:
        | 'not-git'
        | 'latest-review-missing'
        | 'candidate-not-found'
        | 'candidate-failed'
        | 'red-verdict'
        | 'opus-shadow-needs-confirm'
        | 'unsafe-path'
        | 'source-file-missing'
      detail?: string
    }

export type RejectStoredShadowReviewResult =
  | { ok: true; removedLatest: boolean; pruned: string[]; failedPrune: string[] }
  | { ok: false; reason: 'not-git' | 'latest-review-missing'; detail?: string }

export function getLatestShadowReviewPath(gitRoot: string): string {
  return join(gitRoot, DETAIL_DIR_REL, LATEST_REVIEW_FILE)
}

function safeJsonParse(text: string): StoredShadowReview | null {
  try {
    return JSON.parse(text) as StoredShadowReview
  } catch {
    return null
  }
}

function isSafeRelativePath(path: string): boolean {
  if (!path || path.includes('\0')) return false
  if (/^(?:[a-zA-Z]:)?[\\/]/.test(path)) return false
  const segments = path.split(/[\\/]/)
  return !segments.some(segment => segment === '..' || segment === '')
}

function isInside(parent: string, child: string): boolean {
  const rel = relative(resolve(parent), resolve(child))
  return rel === '' || (!rel.startsWith('..') && !resolve(rel).startsWith('..'))
}

async function resolveGitRoot(cwd: string): Promise<
  | { ok: true; gitRoot: string }
  | { ok: false; reason: 'not-git'; detail: string }
> {
  const availability = await checkWorktreeAvailability(cwd)
  if (!availability.ok) {
    return { ok: false, reason: 'not-git', detail: availability.reason }
  }
  return { ok: true, gitRoot: availability.gitRoot }
}

export async function writeLatestShadowReview(
  gitRoot: string,
  params: WriteLatestShadowReviewParams,
): Promise<string> {
  const latestPath = getLatestShadowReviewPath(gitRoot)
  mkdirSync(dirname(latestPath), { recursive: true })
  const payload: StoredShadowReview = {
    generatedAt: params.generatedAt ?? new Date().toISOString(),
    taskScope: params.taskScope,
    candidates: params.candidates,
    matrix: params.matrix,
    evidenceMatrix: params.evidenceMatrix,
    ...(params.detailPath && { detailPath: params.detailPath }),
  }
  writeFileSync(latestPath, JSON.stringify(payload, null, 2) + '\n', 'utf8')
  return latestPath
}

export async function readLatestShadowReview(
  cwd: string,
): Promise<
  | { ok: true; gitRoot: string; path: string; review: StoredShadowReview }
  | { ok: false; reason: 'not-git' | 'latest-review-missing'; detail?: string }
> {
  const root = await resolveGitRoot(cwd)
  if (!root.ok) return root
  const latestPath = getLatestShadowReviewPath(root.gitRoot)
  if (!existsSync(latestPath)) {
    return { ok: false, reason: 'latest-review-missing' }
  }
  const review = safeJsonParse(readFileSync(latestPath, 'utf8'))
  if (!review) {
    return {
      ok: false,
      reason: 'latest-review-missing',
      detail: 'latest shadow review JSON could not be parsed',
    }
  }
  return { ok: true, gitRoot: root.gitRoot, path: latestPath, review }
}

export async function applyStoredShadowCandidate(params: {
  cwd: string
  candidateLabel: ShadowLabel
  confirmedOpusShadow?: boolean
}): Promise<ApplyStoredShadowCandidateResult> {
  const loaded = await readLatestShadowReview(params.cwd)
  if (!loaded.ok) return loaded

  const promotion = evaluatePromoteRequest({
    candidateLabel: params.candidateLabel,
    candidates: loaded.review.candidates,
    evidenceMatrix: loaded.review.evidenceMatrix,
    confirmedOpusShadow: params.confirmedOpusShadow,
  })
  if (!promotion.ok) return promotion

  const candidate = loaded.review.candidates.find(
    c => c.label === params.candidateLabel,
  )
  if (!candidate) return { ok: false, reason: 'candidate-not-found' }

  const appliedFiles: string[] = []
  for (const file of candidate.filesChanged ?? []) {
    if (!isSafeRelativePath(file)) {
      return { ok: false, reason: 'unsafe-path', detail: file }
    }
    const source = resolve(candidate.worktreePath, file)
    const target = resolve(loaded.gitRoot, file)
    if (
      !isInside(candidate.worktreePath, source) ||
      !isInside(loaded.gitRoot, target)
    ) {
      return { ok: false, reason: 'unsafe-path', detail: file }
    }
    if (!existsSync(source)) {
      return { ok: false, reason: 'source-file-missing', detail: file }
    }
    mkdirSync(dirname(target), { recursive: true })
    copyFileSync(source, target)
    appliedFiles.push(file)
  }

  return {
    ok: true,
    appliedLabel: promotion.appliedLabel,
    appliedFiles,
  }
}

export async function rejectStoredShadowReview(params: {
  cwd: string
}): Promise<RejectStoredShadowReviewResult> {
  const loaded = await readLatestShadowReview(params.cwd)
  if (!loaded.ok) return loaded
  rmSync(loaded.path, { force: true })
  const prune = await pruneShadowWorktrees({ gitRoot: loaded.gitRoot })
  return {
    ok: true,
    removedLatest: true,
    pruned: prune.pruned,
    failedPrune: prune.failed,
  }
}

