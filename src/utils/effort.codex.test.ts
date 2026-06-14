import { afterEach, beforeEach, expect, test } from 'bun:test'

const originalEnv = {
  CLAUDE_CODE_USE_OPENAI: process.env.CLAUDE_CODE_USE_OPENAI,
  CLAUDE_CODE_USE_GEMINI: process.env.CLAUDE_CODE_USE_GEMINI,
  CLAUDE_CODE_USE_GITHUB: process.env.CLAUDE_CODE_USE_GITHUB,
  CLAUDE_CODE_USE_MISTRAL: process.env.CLAUDE_CODE_USE_MISTRAL,
  CLAUDE_CODE_USE_BEDROCK: process.env.CLAUDE_CODE_USE_BEDROCK,
  CLAUDE_CODE_USE_VERTEX: process.env.CLAUDE_CODE_USE_VERTEX,
  CLAUDE_CODE_USE_FOUNDRY: process.env.CLAUDE_CODE_USE_FOUNDRY,
  OPENAI_BASE_URL: process.env.OPENAI_BASE_URL,
  OPENAI_API_BASE: process.env.OPENAI_API_BASE,
  OPENAI_MODEL: process.env.OPENAI_MODEL,
}

function restoreEnv(name: keyof typeof originalEnv): void {
  const value = originalEnv[name]
  if (value === undefined) {
    delete process.env[name]
    return
  }
  process.env[name] = value
}

function clearProviderEnv(): void {
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_VERTEX
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
  delete process.env.OPENAI_BASE_URL
  delete process.env.OPENAI_API_BASE
  delete process.env.OPENAI_MODEL
}

beforeEach(() => {
  clearProviderEnv()
})

afterEach(() => {
  for (const name of Object.keys(originalEnv) as Array<keyof typeof originalEnv>) {
    restoreEnv(name)
  }
})

test('gpt-5.5 on the ChatGPT Codex backend supports effort selection', async () => {
  process.env.CLAUDE_CODE_USE_OPENAI = '1'
  process.env.OPENAI_MODEL = 'gpt-5.5'

  const { getAvailableEffortLevels, modelSupportsEffort } = await import(
    `./effort.js?ts=${Date.now()}-${Math.random()}`
  )

  expect(modelSupportsEffort('gpt-5.5')).toBe(true)
  expect(getAvailableEffortLevels('gpt-5.5')).toEqual([
    'low',
    'medium',
    'high',
    'xhigh',
  ])
})

test('gpt-5.5 on the OpenAI provider still supports effort selection', async () => {
  process.env.CLAUDE_CODE_USE_OPENAI = '1'
  process.env.OPENAI_BASE_URL = 'https://api.openai.com/v1'
  process.env.OPENAI_MODEL = 'gpt-5.5'

  const { getAvailableEffortLevels, modelSupportsEffort } = await import(
    `./effort.js?ts=${Date.now()}-${Math.random()}`
  )

  expect(modelSupportsEffort('gpt-5.5')).toBe(true)
  expect(getAvailableEffortLevels('gpt-5.5')).toEqual([
    'low',
    'medium',
    'high',
    'xhigh',
  ])
})

test('gpt-5.3-codex-spark stays without effort controls', async () => {
  process.env.CLAUDE_CODE_USE_OPENAI = '1'
  process.env.OPENAI_MODEL = 'gpt-5.3-codex-spark'

  const { getAvailableEffortLevels, modelSupportsEffort } = await import(
    `./effort.js?ts=${Date.now()}-${Math.random()}`
  )

  expect(modelSupportsEffort('gpt-5.3-codex-spark')).toBe(false)
  expect(getAvailableEffortLevels('gpt-5.3-codex-spark')).toEqual([])
})
