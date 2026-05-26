import { describe, expect, test } from 'bun:test'

import {
  DEFAULT_CODEX_BASE_URL,
  resolveProviderRequest,
} from '../api/providerConfig.js'
import { resolveCodexImplementerRoute } from './implementer.js'

const topLevelContext = {
  querySource: 'repl_main_thread',
  turnCount: 1,
  agentId: undefined,
}

describe('orchestra Codex implementer route', () => {
  test('resolves the default Codex lead route through codexplan', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      settings: {},
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route).toEqual({
      model: 'gpt-5.5',
      providerOverride: {
        model: 'codexplan',
        baseURL: DEFAULT_CODEX_BASE_URL,
        apiKey: '',
      },
    })
    expect(
      resolveProviderRequest({
        model: result.route!.providerOverride.model,
        baseUrl: result.route!.providerOverride.baseURL,
      }),
    ).toMatchObject({
      transport: 'codex_responses',
      requestedModel: 'codexplan',
      resolvedModel: 'gpt-5.5',
      reasoning: { effort: 'xhigh' },
    })
    expect(result.diagnostic).toContain('orchestra codex implementer active')
  })

  test('fails open when Codex login credentials are missing', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      settings: {},
      credentials: {
        apiKey: '',
        source: 'none',
      },
    })

    expect(result.route).toBeUndefined()
    expect(result.diagnostic).toContain('missing Codex auth')
  })

  test('does not override an explicit provider route', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      settings: {},
      existingProviderOverride: {
        model: 'deepseek-chat',
        baseURL: 'https://api.deepseek.com/v1',
        apiKey: 'explicit-provider-key',
      },
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route).toBeUndefined()
    expect(result.diagnostic).toContain('existing provider override')
  })

  test('routes subagent workers through Codex when worker policy is codex-first', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      querySource: 'agent:worker',
      agentId: 'agent-1',
      settings: {},
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route?.providerOverride.model).toBe('codexplan')
    expect(result.route?.model).toBe('gpt-5.5')
  })

  test('routes top-level follow-up turns through Codex when v0.2 lock enables everyTurn', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      turnCount: 3,
      settings: {
        orchestra: {
          mode: 'v0.2-locked',
        },
      },
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route?.providerOverride.model).toBe('codexplan')
    expect(result.route?.model).toBe('gpt-5.5')
  })

  test('routes subagent worker follow-up turns through Codex when worker policy is codex-first', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      querySource: 'agent:worker',
      turnCount: 3,
      agentId: 'agent-1',
      settings: {},
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route?.providerOverride.model).toBe('codexplan')
    expect(result.route?.model).toBe('gpt-5.5')
  })

  test('does not route subagent workers when worker policy inherits existing model', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      querySource: 'agent:worker',
      agentId: 'agent-1',
      settings: {
        orchestra: {
          workerPolicy: 'inherit',
        },
      },
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route).toBeUndefined()
    expect(result.diagnostic).toBeUndefined()
  })

  test('does not route recursive planner or compaction turns', () => {
    const result = resolveCodexImplementerRoute({
      ...topLevelContext,
      querySource: 'orchestra_planner',
      settings: {},
      credentials: {
        apiKey: 'codex-login-token',
        accountId: 'chatgpt-account',
        source: 'auth.json',
      },
    })

    expect(result.route).toBeUndefined()
    expect(result.diagnostic).toBeUndefined()
  })
})
