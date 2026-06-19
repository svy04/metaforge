import { appendFileSync, mkdirSync } from 'fs'
import { dirname, join } from 'path'

import { logForDebugging } from '../../utils/debug.js'
import { getClaudeConfigHomeDir } from '../../utils/envUtils.js'

export type OrchestraUsageEvent = {
  timestamp?: string
  // v0.2 added 'skeptic' — configured Claude Opus 야당 post-implementation dissent role.
  // It runs read-only on turn end (after the GPT response yields) and is
  // logged with the same status transitions as planner/implementer.
  //
  // v0.2 Phase 3 added the shadow / cross-reviewer roles for opt-in shadow
  // executor + cross-review matrix. shadow-* are the alternative-approach
  // executors (GPT-B + Opus Shadow); cross-reviewer-* are GPT/Opus reviewing
  // all 3 candidates. GPT-A primary stays under the existing 'implementer'
  // role to preserve historical accounting.
  role:
    | 'planner'
    | 'implementer'
    | 'skeptic'
    | 'shadow-gpt-b'
    | 'shadow-opus'
    | 'cross-reviewer-gpt'
    | 'cross-reviewer-opus'
  model: string
  status: 'started' | 'succeeded' | 'failed' | 'routed' | 'skipped'
  querySource?: string
  turnCount?: number
  errorName?: string
  errorType?: string
  errorStatus?: number | string
  errorCode?: string
  errorMessage?: string
}

export type OrchestraUsageRecorder = (
  event: OrchestraUsageEvent,
) => void | Promise<void>

export function getOrchestraUsageLogPath(
  env: Record<string, string | undefined> = process.env,
): string {
  return (
    env.OPENCLAUDE_ORCHESTRA_USAGE_LOG ??
    join(getClaudeConfigHomeDir(), 'orchestra-usage.jsonl')
  )
}

export function recordOrchestraUsageEvent(event: OrchestraUsageEvent): void {
  try {
    const logPath = getOrchestraUsageLogPath()
    mkdirSync(dirname(logPath), { recursive: true })
    appendFileSync(
      logPath,
      `${JSON.stringify({ timestamp: new Date().toISOString(), ...event })}\n`,
      'utf8',
    )
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    logForDebugging(`orchestra usage log write failed: ${message}`, {
      level: 'warn',
    })
  }
}
