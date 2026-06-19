import { describe, expect, test } from 'bun:test'

import {
  CODEX_GPT_55_ALIAS,
  CLAUDE_OPUS_ALIAS,
  resolveOrchestraModelAlias,
} from './modelAliases.js'

describe('orchestra model alias resolver', () => {
  test('preserves display aliases while using explicit settings model ids first', () => {
    const result = resolveOrchestraModelAlias('planner', {
      settings: {
        orchestra: {
          models: { planner: 'claude-opus-explicit' },
        },
      },
      env: { OPENCLAUDE_ORCHESTRA_PLANNER_MODEL: 'claude-opus-env' },
    })

    expect(result.displayAlias).toBe(CLAUDE_OPUS_ALIAS)
    expect(result.model).toBe('claude-opus-explicit')
    expect(result.source).toBe('settings')
    expect(result.diagnostic).toBeUndefined()
  })

  test('uses env model ids when settings do not provide one', () => {
    const result = resolveOrchestraModelAlias('implementer', {
      settings: {},
      env: { OPENCLAUDE_ORCHESTRA_IMPLEMENTER_MODEL: 'gpt-5.5-test' },
    })

    expect(result.displayAlias).toBe(CODEX_GPT_55_ALIAS)
    expect(result.model).toBe('gpt-5.5-test')
    expect(result.source).toBe('env')
  })

  test('falls back to repo-supported defaults with a diagnostic', () => {
    const planner = resolveOrchestraModelAlias('planner', {
      settings: {},
      env: {},
      apiProvider: 'firstParty',
    })
    const implementer = resolveOrchestraModelAlias('implementer', {
      settings: {},
      env: {},
      apiProvider: 'codex',
    })

    expect(planner.displayAlias).toBe(CLAUDE_OPUS_ALIAS)
    expect(planner.model).toBe('claude-opus-4-7')
    expect(planner.source).toBe('fallback')
    expect(planner.diagnostic).toContain(CLAUDE_OPUS_ALIAS)

    expect(implementer.displayAlias).toBe(CODEX_GPT_55_ALIAS)
    expect(implementer.model).toBe('gpt-5.5')
    expect(implementer.source).toBe('fallback')
    expect(implementer.diagnostic).toContain(CODEX_GPT_55_ALIAS)
  })

  test('planner fallback uses Claude OAuth model regardless of user provider', () => {
    // Orchestra planner is hardcoded to callClaudeLoginPlanner (Claude OAuth),
    // which rejects any non-claude model id. Provider translation must NOT
    // apply to the planner — even when the user's primary apiProvider is
    // openai/codex/gemini/etc., the planner fallback must remain a Claude
    // model id so the OAuth call site accepts it.
    for (const provider of ['openai', 'codex', 'gemini', 'github'] as const) {
      const planner = resolveOrchestraModelAlias('planner', {
        settings: {},
        env: {},
        apiProvider: provider,
      })
      expect(planner.model).toBe('claude-opus-4-7')
      expect(planner.source).toBe('fallback')
    }
  })
})
