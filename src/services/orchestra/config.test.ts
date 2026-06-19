import { describe, expect, test } from 'bun:test'

import {
  CODEX_GPT_55_ALIAS,
  CLAUDE_OPUS_ALIAS,
  DEFAULT_ORCHESTRA_SETTINGS,
  resolveOrchestraSettings,
} from './config.js'

describe('orchestra config', () => {
  test('defaults to always-on Codex lead with project-scoped memory', () => {
    const settings = resolveOrchestraSettings({})

    expect(settings).toEqual(DEFAULT_ORCHESTRA_SETTINGS)
    expect(settings.enabled).toBe(true)
    expect(settings.lead).toBe('codex')
    expect(settings.visibility).toBe('codex-final')
    expect(settings.memoryScope).toBe('project')
    expect(settings.mode).toBe('codex-dominant')
    expect(settings.plannerPolicy).toBe('always')
    expect(settings.workerPolicy).toBe('codex-first')
    expect(settings.verifierPolicy).toBe('codex-default-opus-on-risk')
    expect(settings.parallelism).toBe('independent-lanes-only')
    expect(settings.roles.planner).toBe(CLAUDE_OPUS_ALIAS)
    expect(settings.roles.implementer).toBe(CODEX_GPT_55_ALIAS)
  })

  test('merges explicit settings over defaults without losing role defaults', () => {
    const settings = resolveOrchestraSettings({
      orchestra: {
        enabled: false,
        mode: 'codex-max',
        plannerPolicy: 'off',
        workerPolicy: 'inherit',
        verifierPolicy: 'inherit',
        parallelism: 'off',
        visibility: 'codex-final',
        roles: { planner: 'custom opus alias' },
        models: { planner: 'claude-opus-test' },
      },
    })

    expect(settings.enabled).toBe(false)
    expect(settings.lead).toBe('codex')
    expect(settings.mode).toBe('codex-max')
    expect(settings.plannerPolicy).toBe('off')
    expect(settings.workerPolicy).toBe('inherit')
    expect(settings.verifierPolicy).toBe('inherit')
    expect(settings.parallelism).toBe('off')
    expect(settings.roles.planner).toBe('custom opus alias')
    expect(settings.roles.implementer).toBe(CODEX_GPT_55_ALIAS)
    expect(settings.models.planner).toBe('claude-opus-test')
    expect(settings.models.implementer).toBeUndefined()
  })

  test('everyTurn opt-in flips on without affecting other fields', () => {
    const settings = resolveOrchestraSettings({
      orchestra: { everyTurn: true },
    })
    expect(settings.everyTurn).toBe(true)
    expect(settings.enabled).toBe(true)
    expect(settings.plannerPolicy).toBe('always')
  })

  test('v0.2-locked mode forces enabled=true, plannerPolicy=always, everyTurn=true regardless of user overrides', () => {
    // The lock guarantees the v0.2 contract: GPT 5.5 + Claude Opus ALWAYS run
    // together on every turn. Even if a user accidentally writes
    // `enabled: false` or `plannerPolicy: 'off'` in settings.json, the lock
    // wins. This protects the v0.2 invariant from accidental footguns.
    const locked = resolveOrchestraSettings({
      orchestra: {
        mode: 'v0.2-locked',
        enabled: false,
        plannerPolicy: 'off',
        everyTurn: false,
      },
    })
    expect(locked.mode).toBe('v0.2-locked')
    expect(locked.enabled).toBe(true)
    expect(locked.plannerPolicy).toBe('always')
    expect(locked.everyTurn).toBe(true)
  })

  test('non-locked modes preserve user overrides (no implicit lock leak)', () => {
    const unlocked = resolveOrchestraSettings({
      orchestra: {
        mode: 'codex-dominant',
        enabled: false,
        plannerPolicy: 'off',
      },
    })
    expect(unlocked.enabled).toBe(false)
    expect(unlocked.plannerPolicy).toBe('off')
  })

  test('shadowEnabled defaults to false and is NOT forced on by v0.2-locked', () => {
    // v0.2 Phase 3 — Shadow Executor / Cross Review opt-in. Default false so
    // existing users (including v0.2-locked) do not get a surprise 5x
    // model-call latency on every code-mutating turn. Users explicitly turn
    // on shadowEnabled when they want the cross-review matrix.
    expect(DEFAULT_ORCHESTRA_SETTINGS.shadowEnabled).toBe(false)
    expect(resolveOrchestraSettings({}).shadowEnabled).toBe(false)
    expect(
      resolveOrchestraSettings({ orchestra: { mode: 'v0.2-locked' } })
        .shadowEnabled,
    ).toBe(false)
  })

  test('shadowEnabled honors explicit opt-in', () => {
    expect(
      resolveOrchestraSettings({ orchestra: { shadowEnabled: true } })
        .shadowEnabled,
    ).toBe(true)
    expect(
      resolveOrchestraSettings({
        orchestra: { mode: 'v0.2-locked', shadowEnabled: true },
      }).shadowEnabled,
    ).toBe(true)
  })

  test('users opt into v0.2 always-on by setting mode to v0.2-locked in settings.json', () => {
    // Backward-compatibility-preserving design: the DEFAULT keeps the
    // legacy turn-1-only conservative behaviour so existing users do not
    // see surprise extra Opus calls. Users explicitly opt into v0.2 by
    // setting `orchestra.mode: 'v0.2-locked'` in ~/.claude/settings.json
    // or in the project's local settings, at which point enabled,
    // plannerPolicy, and everyTurn all snap to the v0.2 contract.
    const optedIn = resolveOrchestraSettings({
      orchestra: { mode: 'v0.2-locked' },
    })
    expect(optedIn.mode).toBe('v0.2-locked')
    expect(optedIn.enabled).toBe(true)
    expect(optedIn.plannerPolicy).toBe('always')
    expect(optedIn.everyTurn).toBe(true)
    // Default (no explicit user opt-in) keeps legacy turn-1 behaviour:
    expect(DEFAULT_ORCHESTRA_SETTINGS.mode).toBe('codex-dominant')
    expect(DEFAULT_ORCHESTRA_SETTINGS.everyTurn).toBe(false)
  })
})
