import type { EvidenceMatrix } from './evidenceArbiter.js'
import type { ShadowCandidate } from './shadowExecutor.js'
import type { ShadowLabel } from './worktreeManager.js'

/**
 * Phase 4 Promote Gate — pure decision function for whether a user-issued
 * /orchestra-apply may proceed. Does NOT touch git; that's the follow-up
 * Task 4.6 once the slash-command wiring lands.
 *
 * D4=i+iii: this layer is the third gate. The first two are
 *  i. code layer — Opus skeptic / shadow runs without write tools (Phase 2/3)
 *  iii. promote layer — explicit verdict + label-based confirm gate (here)
 */

export type PromoteRequest = {
  candidateLabel: ShadowLabel
  candidates: ShadowCandidate[]
  evidenceMatrix: EvidenceMatrix
  /** Set true after the user has answered the second-confirm prompt. */
  confirmedOpusShadow?: boolean
}

export type PromoteOutcome =
  | { ok: true; appliedLabel: ShadowLabel; diff: string }
  | {
      ok: false
      reason:
        | 'candidate-not-found'
        | 'candidate-failed'
        | 'red-verdict'
        | 'opus-shadow-needs-confirm'
    }

export function evaluatePromoteRequest(req: PromoteRequest): PromoteOutcome {
  const candidate = req.candidates.find(c => c.label === req.candidateLabel)
  if (!candidate) return { ok: false, reason: 'candidate-not-found' }
  if (candidate.status !== 'completed') {
    return { ok: false, reason: 'candidate-failed' }
  }
  const verdict = req.evidenceMatrix.verdicts.find(
    v => v.candidateLabel === req.candidateLabel,
  )
  if (verdict?.recommendation === 'red') {
    return { ok: false, reason: 'red-verdict' }
  }
  if (req.candidateLabel === 'opus-shadow' && !req.confirmedOpusShadow) {
    return { ok: false, reason: 'opus-shadow-needs-confirm' }
  }
  return {
    ok: true,
    appliedLabel: req.candidateLabel,
    diff: candidate.diff ?? '',
  }
}
