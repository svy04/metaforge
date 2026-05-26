import { randomUUID } from 'crypto'
import { queryModelWithStreaming } from '../services/api/claude.js'
import { autoCompactIfNeeded } from '../services/compact/autoCompact.js'
import { microcompactMessages } from '../services/compact/microCompact.js'
import { resolveCodexImplementerRoute } from '../services/orchestra/implementer.js'
import {
  createOrchestraGuidance,
  createOrchestraSkepticDissent,
} from '../services/orchestra/orchestrator.js'
import { createOrchestraShadowReview } from '../services/orchestra/shadowReview.js'
import type { CrossReviewMatrix } from '../services/orchestra/crossReview.js'
import type { EvidenceMatrix } from '../services/orchestra/evidenceArbiter.js'
import type { SystemInformationalMessage } from '../utils/messages.js'
import type { ToolUseContext } from '../Tool.js'

// -- deps

// I/O dependencies for query(). Passing a `deps` override into QueryParams
// lets tests inject fakes directly instead of spyOn-per-module — the most
// common mocks (callModel, autocompact) are each spied in 6-8 test files
// today with module-import-and-spy boilerplate.
//
// Using `typeof fn` keeps signatures in sync with the real implementations
// automatically. This file imports the real functions for both typing and
// the production factory — tests that import this file for typing are
// already importing query.ts (which imports everything), so there's no
// new module-graph cost.
//
// Scope is intentionally narrow to prove the pattern. Followup
// PRs can add runTools, handleStopHooks, logEvent, queue ops, etc.
export type QueryDeps = {
  // -- model
  callModel: typeof queryModelWithStreaming

  // -- compaction
  microcompact: typeof microcompactMessages
  autocompact: typeof autoCompactIfNeeded

  // -- lead/partner orchestration
  orchestraGuidance: typeof createOrchestraGuidance
  orchestraImplementerRoute?: typeof resolveCodexImplementerRoute
  /**
   * v0.2 Phase 2 — post-implementation Opus skeptic dispatch. Fires once per
   * turn AFTER a tool_use-free assistant message yields, producing a separate
   * SystemInformationalMessage rendered to the user as 야당 dissent. Optional
   * so legacy fixtures and non-orchestra paths skip the call cleanly.
   */
  skepticDissent?: typeof createOrchestraSkepticDissent
  /**
   * v0.2 Phase 3 — opt-in shadow executor + cross-review dispatch. Fires
   * after a code-mutating turn (Edit / Write / etc. tool_use seen during the
   * turn) when `orchestra.shadowEnabled === true`. Best-effort: failures must
   * never block the user-facing assistant response. Production wiring lands
   * with the cross-review reviewer + worker integration in a follow-up; the
   * type lives here now so the query.ts hook + tests have a stable contract.
   */
  shadowReview?: ShadowReviewFn

  // -- platform
  uuid: () => string
}

export type ShadowReviewFn = (params: {
  taskScope: { intent: string; targetFiles?: string[] }
  cwd: string
  signal?: AbortSignal
  toolUseContext: ToolUseContext
}) => Promise<{
  summaryMessage?: SystemInformationalMessage
  /**
   * v0.2 Phase 4 — Human Gate system message rendered by humanGate.ts on top
   * of the evidenceMatrix. Optional so legacy fixtures and pre-Phase-4
   * production wirings still type-check; query.ts yields it when present.
   */
  humanGateMessage?: SystemInformationalMessage
  diagnostic?: string
  matrix?: CrossReviewMatrix
  /** v0.2 Phase 4 — full 5-axis arbiter output for downstream slash cmds. */
  evidenceMatrix?: EvidenceMatrix
}>

export function productionDeps(): QueryDeps {
  return {
    callModel: queryModelWithStreaming,
    microcompact: microcompactMessages,
    autocompact: autoCompactIfNeeded,
    orchestraGuidance: createOrchestraGuidance,
    orchestraImplementerRoute: resolveCodexImplementerRoute,
    skepticDissent: createOrchestraSkepticDissent,
    // v0.2 Phase 3+4 production wiring: real sideQuery-driven worker trio +
    // git worktree isolation + cross-review + evidence arbiter + Human Gate.
    // Gracefully self-skips when shadowEnabled is false or when cwd is not a
    // git repository (system message yields a user-visible explanation).
    shadowReview: createOrchestraShadowReview,
    uuid: randomUUID,
  }
}
