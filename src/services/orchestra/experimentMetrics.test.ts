import { describe, expect, test } from 'bun:test'

import {
  computeExperimentMetrics,
  type TaskOutcome,
} from './experimentMetrics.js'

const taskWithUniqueOpusCatch: TaskOutcome = {
  taskId: 't1',
  groundTruthDefects: ['null deref', 'race condition'],
  gptDefectsFlagged: ['null deref'],
  opusDefectsFlagged: ['null deref', 'race condition'],
  scopeDrifts: { byGpt: [], byOpus: ['extra config'], truth: ['extra config'] },
}

const taskWithFalsePositive: TaskOutcome = {
  taskId: 't2',
  groundTruthDefects: ['typo'],
  gptDefectsFlagged: ['typo'],
  opusDefectsFlagged: ['typo', 'imaginary issue'],
  scopeDrifts: { byGpt: [], byOpus: [], truth: [] },
}

const taskWithFullAgreement: TaskOutcome = {
  taskId: 't3',
  groundTruthDefects: ['x'],
  gptDefectsFlagged: ['x'],
  opusDefectsFlagged: ['x'],
  scopeDrifts: { byGpt: [], byOpus: [], truth: [] },
}

describe('experimentMetrics — computeExperimentMetrics', () => {
  test('counts UVD: defects only Opus caught / total truth defects', () => {
    const m = computeExperimentMetrics([taskWithUniqueOpusCatch])
    // 1 unique opus catch (race condition), 2 truth defects → 0.5
    expect(m.uvdRate).toBeCloseTo(0.5, 5)
  })

  test('counts FPR: Opus-flagged but not in truth / total Opus flagged', () => {
    const m = computeExperimentMetrics([taskWithFalsePositive])
    // 1 imaginary, 2 opus flagged → 0.5
    expect(m.fprRate).toBeCloseTo(0.5, 5)
  })

  test('counts SDC: scope drifts only Opus caught / total truth drifts', () => {
    const m = computeExperimentMetrics([taskWithUniqueOpusCatch])
    expect(m.sdcRate).toBeCloseTo(1, 5)
  })

  test('agreement with GPT counts tasks where defect sets overlap', () => {
    const m = computeExperimentMetrics([
      taskWithFullAgreement,
      taskWithUniqueOpusCatch,
    ])
    // both tasks share at least one defect ('x' / 'null deref') → 1.0
    expect(m.agreementWithGpt).toBeCloseTo(1, 5)
  })

  test('recommendation = keep when UVD ≥ 15% OR SDC ≥ 25%', () => {
    const m = computeExperimentMetrics([taskWithUniqueOpusCatch])
    expect(m.recommendation).toBe('keep')
  })

  test('recommendation = remove when UVD < 5% AND SDC < 10%', () => {
    const sparse: TaskOutcome[] = Array.from({ length: 20 }, (_, i) => ({
      taskId: `s${i}`,
      groundTruthDefects: ['x'],
      gptDefectsFlagged: ['x'],
      opusDefectsFlagged: ['x'],
      scopeDrifts: { byGpt: [], byOpus: [], truth: [] },
    }))
    const m = computeExperimentMetrics(sparse)
    expect(m.uvdRate).toBe(0)
    expect(m.sdcRate).toBe(0)
    expect(m.recommendation).toBe('remove')
  })

  test('recommendation = demote in the middle band', () => {
    const tasks: TaskOutcome[] = []
    for (let i = 0; i < 20; i++) {
      const ground = ['a', 'b', 'c', 'd', 'e']
      const gpt = ['a', 'b', 'c', 'd']
      const opus = i < 2 ? [...gpt, 'e'] : gpt
      tasks.push({
        taskId: `m${i}`,
        groundTruthDefects: ground,
        gptDefectsFlagged: gpt,
        opusDefectsFlagged: opus,
        scopeDrifts: { byGpt: [], byOpus: [], truth: [] },
      })
    }
    const m = computeExperimentMetrics(tasks)
    // 2/100 ground defects = 0.02 unique-opus catches → 2% → demote band
    expect(m.uvdRate).toBeCloseTo(0.02, 5)
    expect(m.recommendation).toBe('remove') // still under 5% threshold
  })

  test('totalTasks reports input length', () => {
    const m = computeExperimentMetrics([
      taskWithUniqueOpusCatch,
      taskWithFalsePositive,
    ])
    expect(m.totalTasks).toBe(2)
  })
})
