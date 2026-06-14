import { afterEach, expect, test } from 'bun:test'

type FetchType = typeof globalThis.fetch

const originalFetch = globalThis.fetch
const originalMacro = (globalThis as Record<string, unknown>).MACRO
const originalEnv = {
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  ANTHROPIC_AUTH_TOKEN: process.env.ANTHROPIC_AUTH_TOKEN,
  CLAUDE_CODE_OAUTH_TOKEN: process.env.CLAUDE_CODE_OAUTH_TOKEN,
  CLAUDE_CODE_SIMPLE: process.env.CLAUDE_CODE_SIMPLE,
  CLAUDE_CODE_USE_OPENAI: process.env.CLAUDE_CODE_USE_OPENAI,
  CLAUDE_CODE_USE_GEMINI: process.env.CLAUDE_CODE_USE_GEMINI,
  CLAUDE_CODE_USE_GITHUB: process.env.CLAUDE_CODE_USE_GITHUB,
  CLAUDE_CODE_USE_MISTRAL: process.env.CLAUDE_CODE_USE_MISTRAL,
  CLAUDE_CODE_USE_BEDROCK: process.env.CLAUDE_CODE_USE_BEDROCK,
  CLAUDE_CODE_USE_VERTEX: process.env.CLAUDE_CODE_USE_VERTEX,
  CLAUDE_CODE_USE_FOUNDRY: process.env.CLAUDE_CODE_USE_FOUNDRY,
  NVIDIA_NIM: process.env.NVIDIA_NIM,
  MINIMAX_API_KEY: process.env.MINIMAX_API_KEY,
}

function restoreEnv(key: keyof typeof originalEnv): void {
  const value = originalEnv[key]
  if (value === undefined) {
    delete process.env[key]
  } else {
    process.env[key] = value
  }
}

function forceApiKeyFirstPartyAuth(): void {
  process.env.ANTHROPIC_API_KEY = 'sk-ant-test'
  process.env.CLAUDE_CODE_SIMPLE = '1'
  delete process.env.ANTHROPIC_AUTH_TOKEN
  delete process.env.CLAUDE_CODE_OAUTH_TOKEN
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_VERTEX
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
  delete process.env.NVIDIA_NIM
  delete process.env.MINIMAX_API_KEY
}

afterEach(() => {
  globalThis.fetch = originalFetch
  ;(globalThis as Record<string, unknown>).MACRO = originalMacro
  for (const key of Object.keys(originalEnv) as Array<keyof typeof originalEnv>) {
    restoreEnv(key)
  }
})

test('sideQuery forwards string effort through output_config with the effort beta', async () => {
  ;(globalThis as Record<string, unknown>).MACRO = { VERSION: '0.6.0' }
  forceApiKeyFirstPartyAuth()

  let capturedBody: Record<string, unknown> | undefined
  let capturedHeaders: Headers | undefined

  globalThis.fetch = (async (_input, init) => {
    capturedBody = JSON.parse(String(init?.body)) as Record<string, unknown>
    capturedHeaders = new Headers(init?.headers)

    return new Response(
      JSON.stringify({
        id: 'msg_test',
        type: 'message',
        role: 'assistant',
        model: 'claude-opus-4-7',
        content: [{ type: 'text', text: '{}' }],
        stop_reason: 'end_turn',
        usage: {
          input_tokens: 1,
          output_tokens: 1,
          cache_read_input_tokens: 0,
          cache_creation_input_tokens: 0,
        },
      }),
      { headers: { 'Content-Type': 'application/json' } },
    )
  }) as FetchType

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

  expect(capturedBody?.output_config).toEqual({ effort: 'max' })
  expect(capturedHeaders?.get('anthropic-beta')).toContain('effort-2025-11-24')
})
