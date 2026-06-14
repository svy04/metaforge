import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test'
import axios from 'axios'

const originalEnv = { ...process.env }
const originalAxiosGet = axios.get

async function importFreshModule() {
  return import(`./utils.ts?ts=${Date.now()}-${Math.random()}`)
}

beforeEach(() => {
  process.env = { ...originalEnv }
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_VERTEX
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
  delete process.env.NVIDIA_NIM
  delete process.env.MINIMAX_API_KEY
})

afterEach(() => {
  process.env = { ...originalEnv }
  axios.get = originalAxiosGet
  mock.restore()
})

describe('checkDomainBlocklist', () => {
  test('returns allowed without API call in OpenAI mode', async () => {
    process.env.CLAUDE_CODE_USE_OPENAI = '1'
    const getSpy = mock(() =>
      Promise.resolve({ status: 200, data: { can_fetch: true } }),
    )
    axios.get = getSpy as typeof axios.get

    const { checkDomainBlocklist } = await importFreshModule()
    const result = await checkDomainBlocklist('example.com')

    expect(result.status).toBe('allowed')
    expect(getSpy).not.toHaveBeenCalled()
  })

  test('returns allowed without API call in Gemini mode', async () => {
    process.env.CLAUDE_CODE_USE_GEMINI = '1'
    const getSpy = mock(() =>
      Promise.resolve({ status: 200, data: { can_fetch: true } }),
    )
    axios.get = getSpy as typeof axios.get

    const { checkDomainBlocklist } = await importFreshModule()
    const result = await checkDomainBlocklist('example.com')

    expect(result.status).toBe('allowed')
    expect(getSpy).not.toHaveBeenCalled()
  })

  test('calls Anthropic domain check in first-party mode', async () => {
    const getSpy = mock(() =>
      Promise.resolve({ status: 200, data: { can_fetch: true } }),
    )
    axios.get = getSpy as typeof axios.get

    const { checkDomainBlocklist } = await importFreshModule()
    const result = await checkDomainBlocklist('example.com')

    expect(result.status).toBe('allowed')
    expect(getSpy).toHaveBeenCalledTimes(1)
  })
})
