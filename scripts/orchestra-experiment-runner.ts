#!/usr/bin/env bun
/**
 * Phase 5 Validation Experiment runner — scaffold.
 *
 * Reads `.planning/phase-5/tasks/*.md` (one task per file with a
 * `groundTruth` block), simulates a 4-model trace per task (or, in production,
 * dispatches the real planner / skeptic / shadow / reviewer), then computes
 * `computeExperimentMetrics` and writes JSON to
 * `.planning/phase-5/results-{timestamp}.json` plus a markdown decision summary.
 *
 * MVP behaviour: if no task files found, emits a single mock task so the
 * pipeline is fully exercised. Real 20-task execution is operator-driven —
 * see .planning/phase-5/SPEC.md.
 */
import { readdirSync, existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs'
import { join, resolve } from 'path'

import {
  computeExperimentMetrics,
  type TaskOutcome,
} from '../src/services/orchestra/experimentMetrics.js'

const PHASE_5_DIR = resolve(process.cwd(), '.planning', 'phase-5')
const TASK_DIR = join(PHASE_5_DIR, 'tasks')

function loadTaskOutcomes(): TaskOutcome[] {
  if (!existsSync(TASK_DIR)) {
    console.warn(`[phase-5] no task dir at ${TASK_DIR}; using one mock task.`)
    return [
      {
        taskId: 'mock-001',
        groundTruthDefects: ['null deref', 'race'],
        gptDefectsFlagged: ['null deref'],
        opusDefectsFlagged: ['null deref', 'race'],
        scopeDrifts: {
          byGpt: [],
          byOpus: ['extra config'],
          truth: ['extra config'],
        },
      },
    ]
  }
  const files = readdirSync(TASK_DIR).filter(f => f.endsWith('.json'))
  const outcomes: TaskOutcome[] = []
  for (const file of files) {
    try {
      const raw = readFileSync(join(TASK_DIR, file), 'utf8')
      outcomes.push(JSON.parse(raw))
    } catch (e) {
      console.error(`[phase-5] failed to parse ${file}: ${(e as Error).message}`)
    }
  }
  return outcomes
}

function main(): void {
  if (!existsSync(PHASE_5_DIR)) mkdirSync(PHASE_5_DIR, { recursive: true })
  const outcomes = loadTaskOutcomes()
  const metrics = computeExperimentMetrics(outcomes)
  const ts = new Date().toISOString().replace(/[:.]/g, '-')
  const jsonPath = join(PHASE_5_DIR, `results-${ts}.json`)
  writeFileSync(jsonPath, JSON.stringify({ metrics, outcomes }, null, 2))
  const summary = [
    '# Phase 5 — Run Summary',
    `- timestamp: ${new Date().toISOString()}`,
    `- tasks: ${metrics.totalTasks}`,
    `- UVD: ${(metrics.uvdRate * 100).toFixed(1)}%`,
    `- FPR: ${(metrics.fprRate * 100).toFixed(1)}%`,
    `- SDC: ${(metrics.sdcRate * 100).toFixed(1)}%`,
    `- agreement-with-GPT: ${(metrics.agreementWithGpt * 100).toFixed(1)}%`,
    `- **recommendation**: ${metrics.recommendation}`,
    '',
    `Detailed JSON: ${jsonPath}`,
  ].join('\n')
  const summaryPath = join(PHASE_5_DIR, `summary-${ts}.md`)
  writeFileSync(summaryPath, summary)
  console.log(summary)
}

main()
