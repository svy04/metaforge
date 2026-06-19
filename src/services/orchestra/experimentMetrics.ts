/**
 * Phase 5 Validation Experiment metrics.
 *
 * Goal: quantify whether the configured Claude Opus route is "differently wrong than GPT 5.5" enough
 * to justify keeping it in the orchestra. v0.3 will use these numbers to
 * decide keep / demote / remove.
 *
 * Metric definitions (D4 from SPEC):
 *   UVD — unique valid defect catch rate. Defects in groundTruth that ONLY
 *         Opus flagged (not GPT) / total truth defects.
 *   FPR — Opus false positive rate. Opus-flagged items NOT in truth / total
 *         Opus flagged.
 *   SDC — scope drift catch rate. Truth scope drifts ONLY Opus caught / total
 *         truth drifts.
 *   agreementWithGpt — % of tasks where Opus and GPT defect sets share at
 *         least one element (rough proxy for "different vs same wrongness").
 *
 * Recommendation thresholds (D5 from SPEC):
 *   keep   — UVD ≥ 15% OR SDC ≥ 25%
 *   remove — UVD < 5% AND SDC < 10%
 *   demote — everything else
 */

export type TaskOutcome = {
  taskId: string
  groundTruthDefects: string[]
  gptDefectsFlagged: string[]
  opusDefectsFlagged: string[]
  scopeDrifts: { byGpt: string[]; byOpus: string[]; truth: string[] }
}

export type ExperimentRecommendation = 'keep' | 'demote' | 'remove'

export type ExperimentMetrics = {
  totalTasks: number
  uvdRate: number
  fprRate: number
  sdcRate: number
  agreementWithGpt: number
  recommendation: ExperimentRecommendation
}

function difference<T>(a: readonly T[], b: readonly T[]): T[] {
  const set = new Set(b)
  return a.filter(x => !set.has(x))
}

function intersection<T>(a: readonly T[], b: readonly T[]): T[] {
  const set = new Set(b)
  return a.filter(x => set.has(x))
}

function classify(uvd: number, sdc: number): ExperimentRecommendation {
  if (uvd >= 0.15 || sdc >= 0.25) return 'keep'
  if (uvd < 0.05 && sdc < 0.1) return 'remove'
  return 'demote'
}

export function computeExperimentMetrics(
  outcomes: TaskOutcome[],
): ExperimentMetrics {
  let truthDefectsTotal = 0
  let uniqueOpusCatches = 0
  let opusFlaggedTotal = 0
  let opusFalsePositives = 0
  let truthDriftsTotal = 0
  let uniqueOpusDriftCatches = 0
  let agreementTasks = 0

  for (const task of outcomes) {
    const truth = task.groundTruthDefects
    const gpt = task.gptDefectsFlagged
    const opus = task.opusDefectsFlagged

    truthDefectsTotal += truth.length
    const opusUnique = difference(opus, gpt) // defects only Opus claimed
    const opusUniqueValid = intersection(opusUnique, truth)
    uniqueOpusCatches += opusUniqueValid.length

    opusFlaggedTotal += opus.length
    opusFalsePositives += difference(opus, truth).length

    truthDriftsTotal += task.scopeDrifts.truth.length
    const opusDriftUnique = difference(
      task.scopeDrifts.byOpus,
      task.scopeDrifts.byGpt,
    )
    uniqueOpusDriftCatches += intersection(
      opusDriftUnique,
      task.scopeDrifts.truth,
    ).length

    if (intersection(gpt, opus).length > 0) {
      agreementTasks += 1
    }
  }

  const uvdRate =
    truthDefectsTotal > 0 ? uniqueOpusCatches / truthDefectsTotal : 0
  const fprRate =
    opusFlaggedTotal > 0 ? opusFalsePositives / opusFlaggedTotal : 0
  const sdcRate =
    truthDriftsTotal > 0 ? uniqueOpusDriftCatches / truthDriftsTotal : 0
  const agreementWithGpt =
    outcomes.length > 0 ? agreementTasks / outcomes.length : 0

  return {
    totalTasks: outcomes.length,
    uvdRate,
    fprRate,
    sdcRate,
    agreementWithGpt,
    recommendation: classify(uvdRate, sdcRate),
  }
}
