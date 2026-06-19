import { afterEach, expect, mock, test } from 'bun:test'

type CapabilityLike = {
  max_input_tokens?: number
  max_tokens?: number
}

const originalEnv = {
  CLAUDE_CODE_USE_OPENAI: process.env.CLAUDE_CODE_USE_OPENAI,
  CLAUDE_CODE_USE_GEMINI: process.env.CLAUDE_CODE_USE_GEMINI,
  CLAUDE_CODE_USE_GITHUB: process.env.CLAUDE_CODE_USE_GITHUB,
  CLAUDE_CODE_USE_MISTRAL: process.env.CLAUDE_CODE_USE_MISTRAL,
  USER_TYPE: process.env.USER_TYPE,
}

let capabilityForModel: (_model: string) => CapabilityLike | undefined = () =>
  undefined
let importCounter = 0

mock.module('./model/modelCapabilities.js', () => ({
  getModelCapability: (model: string) => capabilityForModel(model),
  refreshModelCapabilities: async () => {},
}))

afterEach(() => {
  capabilityForModel = () => undefined
  restoreEnv('CLAUDE_CODE_USE_OPENAI')
  restoreEnv('CLAUDE_CODE_USE_GEMINI')
  restoreEnv('CLAUDE_CODE_USE_GITHUB')
  restoreEnv('CLAUDE_CODE_USE_MISTRAL')
  restoreEnv('USER_TYPE')
})

function restoreEnv(name: keyof typeof originalEnv): void {
  const value = originalEnv[name]
  if (value === undefined) {
    delete process.env[name]
  } else {
    process.env[name] = value
  }
}

function clearProviderEnv(): void {
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.USER_TYPE
}

async function importFreshContext() {
  importCounter += 1
  return import(`./context.ts?model-capability-${importCounter}`)
}

test('getContextWindowForModel snapshots model capability input tokens before comparing', async () => {
  clearProviderEnv()
  let reads = 0
  capabilityForModel = () => ({
    get max_input_tokens() {
      reads += 1
      if (reads > 1) {
        throw new Error('max_input_tokens should only be read once')
      }
      return 250_000
    },
  })

  const { getContextWindowForModel } = await importFreshContext()

  expect(getContextWindowForModel('capability-model')).toBe(250_000)
  expect(reads).toBe(1)
})

test('getModelMaxOutputTokens snapshots model capability output tokens before comparing', async () => {
  clearProviderEnv()
  let reads = 0
  capabilityForModel = () => ({
    get max_tokens() {
      reads += 1
      if (reads > 1) {
        throw new Error('max_tokens should only be read once')
      }
      return 96_000
    },
  })

  const { getModelMaxOutputTokens } = await importFreshContext()

  expect(getModelMaxOutputTokens('capability-model')).toEqual({
    default: 32_000,
    upperLimit: 96_000,
  })
  expect(reads).toBe(1)
})
