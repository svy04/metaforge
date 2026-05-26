import { afterEach, expect, mock, test } from 'bun:test'

afterEach(() => {
  mock.restore()
})

test('sideQuery forwards string effort through output_config with the effort beta', async () => {
  ;(globalThis as unknown as { MACRO?: { VERSION: string } }).MACRO = {
    VERSION: '0.6.0',
  }
  const createCalls: any[] = []

  mock.module('../services/api/client.js', () => ({
    getAnthropicClient: async () => ({
      beta: {
        messages: {
          create: async (params: any) => {
            createCalls.push(params)
            return {
              content: [{ type: 'text', text: '{}' }],
              usage: {
                input_tokens: 1,
                output_tokens: 1,
                cache_read_input_tokens: 0,
                cache_creation_input_tokens: 0,
              },
            }
          },
        },
      },
    }),
  }))
  mock.module('../services/analytics/index.js', () => ({
    logEvent: () => {},
  }))
  mock.module('../services/api/claude.js', () => ({
    getAPIMetadata: () => ({ user_id: '{}' }),
  }))
  mock.module('./betas.js', () => ({
    getModelBetas: () => ['oauth-2025-04-20'],
    modelSupportsStructuredOutputs: () => false,
  }))
  mock.module('./fingerprint.js', () => ({
    computeFingerprint: () => 'fingerprint',
  }))
  mock.module('../constants/system.js', () => ({
    getAttributionHeader: () => 'x-anthropic-billing-header: test',
    getCLISyspromptPrefix: () => 'You are OpenClaude.',
  }))
  mock.module('./model/model.js', () => ({
    normalizeModelStringForAPI: (model: string) => model,
  }))
  mock.module('../bootstrap/state.js', () => ({
    getLastApiCompletionTimestamp: () => null,
    setLastApiCompletionTimestamp: () => {},
  }))

  const { sideQuery } = await import(`./sideQuery.js?effort=${Date.now()}`)
  await sideQuery({
    model: 'claude-opus-4-7',
    max_tokens: 128,
    system: 'Private planner.',
    messages: [{ role: 'user', content: 'Return JSON.' }],
    querySource: 'orchestra_planner' as any,
    maxRetries: 0,
    effort: 'max' as any,
  })

  expect(createCalls).toHaveLength(1)
  expect(createCalls[0].output_config).toEqual({ effort: 'max' })
  expect(createCalls[0].betas).toContain('effort-2025-11-24')
})
