import type { SettingsJson } from '../../utils/settings/types.js'

export const CODEX_GPT_55_ALIAS = 'Codex GPT 5.5'
export const CLAUDE_OPUS_47_ALIAS = 'Claude Opus 4.7'

export type OrchestraLead = 'codex'
export type OrchestraVisibility = 'codex-final'
export type OrchestraMemoryScope = 'project'
export type OrchestraMode =
  | 'balanced'
  | 'codex-dominant'
  | 'codex-max'
  /**
   * v0.2 always-on opposition mode. The lock forces enabled=true,
   * plannerPolicy='always', and everyTurn=true regardless of any user
   * settings.json overrides. Used by users who have explicitly opted into
   * the GPT 5.5-king + Opus 4.7-opposition vision and don't want a
   * footgun setting (e.g. an accidental `enabled: false`) to silently
   * collapse the orchestra back into single-model behaviour.
   */
  | 'v0.2-locked'
export type OrchestraPlannerPolicy = 'always' | 'risk-gated' | 'off'
export type OrchestraPlannerFailurePolicy = 'adaptive' | 'warn' | 'block'
export type OrchestraWorkerPolicy = 'codex-first' | 'inherit'
export type OrchestraVerifierPolicy =
  | 'codex-default-opus-on-risk'
  | 'inherit'
export type OrchestraParallelismPolicy = 'independent-lanes-only' | 'off'

export type ResolvedOrchestraSettings = {
  enabled: boolean
  lead: OrchestraLead
  visibility: OrchestraVisibility
  memoryScope: OrchestraMemoryScope
  mode: OrchestraMode
  plannerPolicy: OrchestraPlannerPolicy
  plannerFailurePolicy: OrchestraPlannerFailurePolicy
  workerPolicy: OrchestraWorkerPolicy
  verifierPolicy: OrchestraVerifierPolicy
  parallelism: OrchestraParallelismPolicy
  /**
   * When true, the orchestra runs on EVERY user turn instead of only the
   * first. Pairs with the v0.2 "always-on opposition" vision: GPT 5.5 as
   * the king + Opus 4.7 as the constant opposition party. Default false
   * for backward compatibility — token-conservative users keep the legacy
   * turn-1-only behaviour.
   */
  everyTurn: boolean
  /**
   * v0.2 Phase 3 — opt-in cross-review of code-mutating turns. When true,
   * each turn that produces an Edit/Write tool_use spawns a shadow trio
   * (GPT-A + GPT-B + Opus Shadow) in isolated git worktrees and renders a
   * cross-review matrix back to the user. Default false because each
   * activation is a 5x model-call burst (planner + skeptic + 3 shadows +
   * 2 reviewers) and not every workflow wants that latency. Even
   * v0.2-locked does NOT force this on — users opt in deliberately.
   */
  shadowEnabled: boolean
  /**
   * v0.2 Phase 3 verification helper. When true, the shadow review hook
   * runs on every user turn regardless of whether a mutation tool fired.
   * Some OpenClaude -p (print) modes restrict Edit/Write/Bash, which
   * makes mutation-gated firing untestable in those environments.
   * Default false; pairs with shadowEnabled: true. Explicit opt-in.
   */
  shadowEveryTurn: boolean
  roles: {
    planner: string
    implementer: string
  }
  models: {
    planner?: string
    implementer?: string
  }
}

export const DEFAULT_ORCHESTRA_SETTINGS: ResolvedOrchestraSettings = {
  enabled: true,
  lead: 'codex',
  visibility: 'codex-final',
  memoryScope: 'project',
  mode: 'codex-dominant',
  plannerPolicy: 'always',
  plannerFailurePolicy: 'adaptive',
  workerPolicy: 'codex-first',
  verifierPolicy: 'codex-default-opus-on-risk',
  parallelism: 'independent-lanes-only',
  // Default false for backward compatibility with existing token-conservative
  // users. Users opting into v0.2 always-on opposition flip this to true
  // either explicitly (orchestra.everyTurn: true) or implicitly via
  // orchestra.mode: 'v0.2-locked' (see resolveOrchestraSettings).
  everyTurn: false,
  // v0.2 Phase 3 default off. Users opt in via orchestra.shadowEnabled: true.
  // Even v0.2-locked does NOT force this — Phase 3 is heavyweight (3 worktrees
  // + 5 model calls per code-mutating turn) and the v0.3 experiment will
  // decide whether to flip the default.
  shadowEnabled: false,
  shadowEveryTurn: false,
  roles: {
    planner: CLAUDE_OPUS_47_ALIAS,
    implementer: CODEX_GPT_55_ALIAS,
  },
  models: {},
}

export function resolveOrchestraSettings(
  settings: Pick<SettingsJson, 'orchestra'> | null | undefined,
): ResolvedOrchestraSettings {
  const orchestra = settings?.orchestra
  const mode = orchestra?.mode ?? DEFAULT_ORCHESTRA_SETTINGS.mode
  const isLocked = mode === 'v0.2-locked'
  return {
    ...DEFAULT_ORCHESTRA_SETTINGS,
    // v0.2-locked overrides any user-provided enabled / plannerPolicy /
    // everyTurn — these three together are the v0.2 contract and must not
    // be silently weakened by stale settings.json overrides.
    enabled: isLocked
      ? true
      : (orchestra?.enabled ?? DEFAULT_ORCHESTRA_SETTINGS.enabled),
    lead: orchestra?.lead ?? DEFAULT_ORCHESTRA_SETTINGS.lead,
    visibility:
      orchestra?.visibility ?? DEFAULT_ORCHESTRA_SETTINGS.visibility,
    memoryScope:
      orchestra?.memoryScope ?? DEFAULT_ORCHESTRA_SETTINGS.memoryScope,
    mode,
    plannerPolicy: isLocked
      ? 'always'
      : (orchestra?.plannerPolicy ?? DEFAULT_ORCHESTRA_SETTINGS.plannerPolicy),
    plannerFailurePolicy:
      orchestra?.plannerFailurePolicy ??
      DEFAULT_ORCHESTRA_SETTINGS.plannerFailurePolicy,
    workerPolicy:
      orchestra?.workerPolicy ?? DEFAULT_ORCHESTRA_SETTINGS.workerPolicy,
    verifierPolicy:
      orchestra?.verifierPolicy ?? DEFAULT_ORCHESTRA_SETTINGS.verifierPolicy,
    parallelism:
      orchestra?.parallelism ?? DEFAULT_ORCHESTRA_SETTINGS.parallelism,
    everyTurn: isLocked
      ? true
      : (orchestra?.everyTurn ?? DEFAULT_ORCHESTRA_SETTINGS.everyTurn),
    // shadowEnabled is intentionally NOT locked even when mode === 'v0.2-locked'.
    // Phase 3 is opt-in (3 worktrees + 5 model calls per code turn), so users
    // explicitly raise their hand by setting orchestra.shadowEnabled: true.
    shadowEnabled:
      orchestra?.shadowEnabled ?? DEFAULT_ORCHESTRA_SETTINGS.shadowEnabled,
    shadowEveryTurn:
      (orchestra as { shadowEveryTurn?: boolean })?.shadowEveryTurn ??
      DEFAULT_ORCHESTRA_SETTINGS.shadowEveryTurn,
    roles: {
      ...DEFAULT_ORCHESTRA_SETTINGS.roles,
      ...orchestra?.roles,
    },
    models: {
      ...DEFAULT_ORCHESTRA_SETTINGS.models,
      ...orchestra?.models,
    },
  }
}
