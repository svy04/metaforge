import type { CrossReviewMatrix } from './crossReview.js'
import type { ShadowCandidate } from './shadowExecutor.js'
import type { ShadowLabel } from './worktreeManager.js'

/**
 * Phase 4 Evidence Arbiter — fact-based 5-axis judgment over shadow
 * candidates. The arbiter does NOT auto-promote anything; it produces a
 * recommendation that the Human Gate (Phase 4 humanGate.ts) renders so the
 * user can apply via slash command.
 *
 * D1=c (evidence + pass/fail boolean, not 0-5 score)
 * D2=β (test fail OR scope fail → red immediately; else any fail → yellow)
 * D5=γ+α (code extracts deterministic facts; injected GPT judge handles
 *         the soft "understandable" axis)
 */

export type AxisResult<T> = T & { pass: boolean }

export type FiveAxisEvidence = {
  testsRan: AxisResult<{ ran: boolean; passed?: boolean; evidencePath?: string }>
  diffMinimal: AxisResult<{ lineCount: number; under: number }>
  scopeFit: AxisResult<{ keywordsMatched: number; keywordsTotal: number }>
  rollbackable: AxisResult<{ branchIsolated: boolean }>
  understandable: AxisResult<{ gptVerdict?: 'pass' | 'fail' | 'unavailable' }>
}

export type EvidenceVerdict = {
  candidateLabel: ShadowLabel
  evidence: FiveAxisEvidence
  recommendation: 'green' | 'yellow' | 'red'
  rationale: string
}

export type EvidenceMatrix = {
  verdicts: EvidenceVerdict[]
  topRecommended?: ShadowLabel
  generatedAt: string
}

export type UnderstandableJudgeFn = (params: {
  candidate: ShadowCandidate
  taskScope: { intent: string }
  signal?: AbortSignal
}) => Promise<{ verdict: 'pass' | 'fail' }>

export type TestEvidence = {
  ran: boolean
  passed?: boolean
  evidencePath?: string
}

const DEFAULT_DIFF_LINE_BUDGET = 200

function countDiffLines(diff: string | undefined): number {
  if (!diff) return 0
  return diff.split('\n').filter(line => line.length > 0).length
}

function tokenize(text: string): string[] {
  return (text.toLowerCase().match(/[a-z0-9_가-힣]+/gi) ?? []).filter(
    token => token.length >= 3,
  )
}

function scoreScopeFit(
  candidate: ShadowCandidate,
  intent: string,
): { keywordsMatched: number; keywordsTotal: number; pass: boolean } {
  const intentTokens = new Set(tokenize(intent))
  const keywordsTotal = Math.max(intentTokens.size, 1)
  if (intentTokens.size === 0) {
    // No intent text = cannot judge scope; treat as pass to avoid false reds
    return { keywordsMatched: 0, keywordsTotal: 0, pass: true }
  }
  const haystack =
    (candidate.diff ?? '') +
    ' ' +
    (candidate.patchSummary ?? '') +
    ' ' +
    (candidate.filesChanged?.join(' ') ?? '')
  const haystackTokens = new Set(tokenize(haystack))
  let keywordsMatched = 0
  for (const t of intentTokens) {
    if (haystackTokens.has(t)) keywordsMatched++
  }
  // β rule: scope passes when at least 1 of the intent tokens shows up in the
  // candidate's surface area. Stricter heuristics belong in v0.3 experiments.
  return {
    keywordsMatched,
    keywordsTotal,
    pass: keywordsMatched >= 1,
  }
}

function isolatedFromMain(candidate: ShadowCandidate): boolean {
  return candidate.worktreePath.includes('.openclaude-shadows')
}

function applyBetaThreshold(evidence: FiveAxisEvidence): {
  recommendation: 'green' | 'yellow' | 'red'
  rationale: string
} {
  // β: critical axes — fail-on-test ONLY when tests actually ran and failed.
  // If tests have not been run yet (production: there's no test runner wired
  // into the shadow flow yet), we degrade to 'yellow' instead of auto-red,
  // because "we don't know" should not look identical to "we proved it
  // broken". Scope mismatch stays a hard-red trigger because that's a
  // fact-based extraction, not a missing signal.
  if (evidence.testsRan.ran && !evidence.testsRan.pass) {
    return {
      recommendation: 'red',
      rationale: 'tests ran and did not pass',
    }
  }
  if (!evidence.scopeFit.pass) {
    return {
      recommendation: 'red',
      rationale: `scope mismatch (matched ${evidence.scopeFit.keywordsMatched}/${evidence.scopeFit.keywordsTotal} intent keywords)`,
    }
  }
  const softFails: string[] = []
  if (!evidence.testsRan.ran) {
    softFails.push('tests not run yet — manual verification required')
  }
  if (!evidence.diffMinimal.pass) {
    softFails.push(
      `diff exceeds budget (${evidence.diffMinimal.lineCount} > ${evidence.diffMinimal.under})`,
    )
  }
  if (!evidence.rollbackable.pass) {
    softFails.push('candidate not isolated to a shadow branch')
  }
  if (!evidence.understandable.pass) {
    softFails.push(
      `understandability check: ${evidence.understandable.gptVerdict ?? 'unavailable'}`,
    )
  }
  if (softFails.length === 0) {
    return { recommendation: 'green', rationale: 'all 5 axes pass' }
  }
  return {
    recommendation: 'yellow',
    rationale: softFails.join('; '),
  }
}

const FAILED_CANDIDATE_EVIDENCE: FiveAxisEvidence = {
  testsRan: { ran: false, pass: false },
  diffMinimal: { lineCount: 0, under: DEFAULT_DIFF_LINE_BUDGET, pass: false },
  scopeFit: { keywordsMatched: 0, keywordsTotal: 0, pass: false },
  rollbackable: { branchIsolated: false, pass: false },
  understandable: { gptVerdict: 'unavailable', pass: false },
}

export async function buildEvidenceMatrix(params: {
  candidates: ShadowCandidate[]
  crossReview: CrossReviewMatrix
  taskScope: { intent: string }
  understandableJudge?: UnderstandableJudgeFn
  testEvidence?: TestEvidence
  diffLineBudget?: number
  signal?: AbortSignal
}): Promise<EvidenceMatrix> {
  const budget = params.diffLineBudget ?? DEFAULT_DIFF_LINE_BUDGET
  const verdicts: EvidenceVerdict[] = []
  for (const candidate of params.candidates) {
    if (candidate.status !== 'completed') {
      verdicts.push({
        candidateLabel: candidate.label,
        evidence: FAILED_CANDIDATE_EVIDENCE,
        recommendation: 'red',
        rationale: `candidate did not complete: ${candidate.error ?? 'unknown'}`,
      })
      continue
    }
    const lineCount = countDiffLines(candidate.diff)
    const diffMinimal = {
      lineCount,
      under: budget,
      pass: lineCount > 0 && lineCount <= budget,
    }
    const scopeFit = scoreScopeFit(candidate, params.taskScope.intent)
    const rollbackable = {
      branchIsolated: isolatedFromMain(candidate),
      pass: isolatedFromMain(candidate),
    }
    const testsRan: FiveAxisEvidence['testsRan'] = {
      ran: params.testEvidence?.ran ?? false,
      ...(params.testEvidence?.passed !== undefined && {
        passed: params.testEvidence.passed,
      }),
      ...(params.testEvidence?.evidencePath !== undefined && {
        evidencePath: params.testEvidence.evidencePath,
      }),
      pass: Boolean(
        params.testEvidence?.ran && params.testEvidence?.passed === true,
      ),
    }
    let understandable: FiveAxisEvidence['understandable']
    if (params.understandableJudge) {
      try {
        const result = await params.understandableJudge({
          candidate,
          taskScope: params.taskScope,
          signal: params.signal,
        })
        understandable = {
          gptVerdict: result.verdict,
          pass: result.verdict === 'pass',
        }
      } catch {
        understandable = { gptVerdict: 'unavailable', pass: false }
      }
    } else {
      understandable = { gptVerdict: 'unavailable', pass: false }
    }
    const evidence: FiveAxisEvidence = {
      testsRan,
      diffMinimal,
      scopeFit,
      rollbackable,
      understandable,
    }
    const { recommendation, rationale } = applyBetaThreshold(evidence)
    verdicts.push({
      candidateLabel: candidate.label,
      evidence,
      recommendation,
      rationale,
    })
  }
  const topRecommended = verdicts.find(v => v.recommendation === 'green')
    ?.candidateLabel
  return {
    verdicts,
    topRecommended,
    generatedAt: new Date().toISOString(),
  }
}
