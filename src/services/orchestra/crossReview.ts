import type { ShadowCandidate } from './shadowExecutor.js'
import type { ShadowLabel } from './worktreeManager.js'

/**
 * Phase 3 Cross Review — 3 candidates × 2 reviewers grid.
 *
 * Reviewer functions are injected (production wiring in a follow-up); this
 * module provides the dispatch loop and the markdown rendering used by
 * query.ts for stdout summary + persistent file at
 * `.planning/phase-3/cross-review-{ts}.md` (D4=c).
 *
 * Verdict semantics (Phase 4 will refine):
 *   green  — reviewer believes the candidate is safe to land
 *   yellow — needs follow-up before landing
 *   red    — reject or major rework
 *
 * Phase 3 does NOT auto-promote any candidate. Phase 4 Evidence Arbiter
 * decides; this matrix is the input.
 */

export type CandidateVerdict = 'green' | 'yellow' | 'red'
export type ReviewerName = 'gpt' | 'opus'

export type ReviewerVerdict = {
  candidateLabel: ShadowLabel
  reviewer: ReviewerName
  scoresOutOf5: { correctness: number; minimality: number; scopeFit: number }
  verdict: CandidateVerdict
  rationale: string
}

export type ReviewerFn = (params: {
  candidate: ShadowCandidate
  signal?: AbortSignal
}) => Promise<Omit<ReviewerVerdict, 'candidateLabel' | 'reviewer'>>

export type CrossReviewMatrix = {
  candidates: ShadowCandidate[]
  verdicts: ReviewerVerdict[]
  generatedAt: string
}

const REVIEWERS: ReviewerName[] = ['gpt', 'opus']

const ZERO_SCORES = { correctness: 0, minimality: 0, scopeFit: 0 }

function executionFailedVerdict(
  candidate: ShadowCandidate,
  reviewer: ReviewerName,
): ReviewerVerdict {
  return {
    candidateLabel: candidate.label,
    reviewer,
    scoresOutOf5: ZERO_SCORES,
    verdict: 'red',
    rationale: `execution_failed: ${candidate.error ?? 'candidate did not produce a patch'}`,
  }
}

function reviewerFailedVerdict(
  candidate: ShadowCandidate,
  reviewer: ReviewerName,
  message: string,
): ReviewerVerdict {
  return {
    candidateLabel: candidate.label,
    reviewer,
    scoresOutOf5: ZERO_SCORES,
    verdict: 'red',
    rationale: `reviewer_failed: ${message}`,
  }
}

export async function buildCrossReviewMatrix(params: {
  candidates: ShadowCandidate[]
  reviewers: { gpt: ReviewerFn; opus: ReviewerFn }
  signal?: AbortSignal
}): Promise<CrossReviewMatrix> {
  const verdicts: ReviewerVerdict[] = []
  for (const candidate of params.candidates) {
    for (const reviewer of REVIEWERS) {
      if (candidate.status !== 'completed') {
        verdicts.push(executionFailedVerdict(candidate, reviewer))
        continue
      }
      const fn = params.reviewers[reviewer]
      try {
        const partial = await fn({ candidate, signal: params.signal })
        verdicts.push({
          candidateLabel: candidate.label,
          reviewer,
          ...partial,
        })
      } catch (error) {
        const message = error instanceof Error ? error.message : String(error)
        verdicts.push(reviewerFailedVerdict(candidate, reviewer, message))
      }
    }
  }
  return {
    candidates: params.candidates,
    verdicts,
    generatedAt: new Date().toISOString(),
  }
}

function digestVerdictForCandidate(
  matrix: CrossReviewMatrix,
  label: ShadowLabel,
): string {
  const cells = matrix.verdicts.filter(v => v.candidateLabel === label)
  const tally = cells.reduce(
    (acc, v) => {
      acc[v.verdict] = (acc[v.verdict] ?? 0) + 1
      return acc
    },
    {} as Record<CandidateVerdict, number>,
  )
  const parts: string[] = []
  if (tally.green) parts.push(`🟢×${tally.green}`)
  if (tally.yellow) parts.push(`🟡×${tally.yellow}`)
  if (tally.red) parts.push(`🔴×${tally.red}`)
  return `${label}: ${parts.join(' ') || '—'}`
}

export function formatMatrixSummary(matrix: CrossReviewMatrix): string {
  const labels = Array.from(new Set(matrix.candidates.map(c => c.label)))
  const parts = labels.map(l => digestVerdictForCandidate(matrix, l))
  return `[Phase 3 Cross-Review] ${parts.join(' | ')}`
}

export function formatMatrixDetail(matrix: CrossReviewMatrix): string {
  const lines: string[] = []
  lines.push(`# Phase 3 Cross-Review Matrix`)
  lines.push(`Generated: ${matrix.generatedAt}`)
  lines.push('')
  lines.push('| candidate | reviewer | verdict | correctness | minimality | scopeFit | rationale |')
  lines.push('|-----------|----------|---------|-------------|------------|----------|-----------|')
  for (const v of matrix.verdicts) {
    const s = v.scoresOutOf5
    lines.push(
      `| ${v.candidateLabel} | ${v.reviewer} | ${v.verdict} | ${s.correctness} | ${s.minimality} | ${s.scopeFit} | ${v.rationale.replace(/\|/g, '\\|')} |`,
    )
  }
  lines.push('')
  lines.push('## Candidate summaries')
  for (const c of matrix.candidates) {
    lines.push(`### ${c.label} (${c.status})`)
    if (c.patchSummary) lines.push(`- summary: ${c.patchSummary}`)
    if (c.filesChanged?.length) lines.push(`- files: ${c.filesChanged.join(', ')}`)
    if (c.error) lines.push(`- error: ${c.error}`)
    lines.push('')
  }
  return lines.join('\n')
}
