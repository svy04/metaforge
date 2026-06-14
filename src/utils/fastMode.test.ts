import { afterEach, describe, expect, mock, test } from 'bun:test'
import {
  getIsInteractive,
  getKairosActive,
  setIsInteractive,
  setKairosActive,
} from '../bootstrap/state.js'
import { saveGlobalConfig } from './config.js'

const originalEnv = { ...process.env }
const originalState = {
  isInteractive: getIsInteractive(),
  kairosActive: getKairosActive(),
}

async function importFreshFastModeModule() {
  return import(`./fastMode.ts?ts=${Date.now()}-${Math.random()}`)
}

function installCommonMocks(options?: {
  cachedEnabled?: boolean
  apiKey?: string | null
  oauthToken?: string | null
  hasProfileScope?: boolean
}) {
  setIsInteractive(true)
  setKairosActive(false)
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_VERTEX
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
  delete process.env.NVIDIA_NIM
  delete process.env.MINIMAX_API_KEY
  delete process.env.ANTHROPIC_AUTH_TOKEN
  delete process.env.CLAUDE_CODE_OAUTH_TOKEN
  process.env.CLAUDE_CODE_SIMPLE = '1'
  if (options?.apiKey) {
    process.env.ANTHROPIC_API_KEY = options.apiKey
  } else {
    delete process.env.ANTHROPIC_API_KEY
  }
  saveGlobalConfig(current => ({
    ...current,
    penguinModeOrgEnabled: options?.cachedEnabled === true,
  }))

  mock.module('../services/analytics/index.js', () => ({
    logEvent: () => {},
  }))

  mock.module('./debug.js', () => ({
    logForDebugging: () => {},
  }))

  mock.module('./privacyLevel.js', () => ({
    isEssentialTrafficOnly: () => false,
  }))

  mock.module('./signal.js', () => ({
    createSignal: () => {
      const subscribe = () => () => {}
      const emit = () => {}
      return { subscribe, emit }
    },
  }))
}

afterEach(() => {
  mock.restore()
  process.env = { ...originalEnv }
  setIsInteractive(originalState.isInteractive)
  setKairosActive(originalState.kairosActive)
})

describe('fastMode ant-only fallback cleanup', () => {
  test('resolveFastModeStatusFromCache does not force-enable from USER_TYPE=ant', async () => {
    process.env.USER_TYPE = 'ant'
    installCommonMocks({ cachedEnabled: false })

    const {
      resolveFastModeStatusFromCache,
      getFastModeUnavailableReason,
    } = await importFreshFastModeModule()

    resolveFastModeStatusFromCache()

    expect(getFastModeUnavailableReason()).toBe(
      'Fast mode is currently unavailable',
    )
  })

  test('prefetchFastModeStatus without auth does not force-enable from USER_TYPE=ant', async () => {
    process.env.USER_TYPE = 'ant'
    installCommonMocks({ cachedEnabled: false, apiKey: null, oauthToken: null })

    const {
      prefetchFastModeStatus,
      getFastModeUnavailableReason,
      _setFastModeTestHooks,
    } = await importFreshFastModeModule()
    _setFastModeTestHooks({
      getAnthropicApiKey: () => null,
      getClaudeAIOAuthTokens: () => null,
      hasProfileScope: () => false,
    })

    await prefetchFastModeStatus()

    expect(getFastModeUnavailableReason()).toBe(
      'Fast mode has been disabled by your organization',
    )
  })

  test('prefetchFastModeStatus network failure does not force-enable from USER_TYPE=ant', async () => {
    process.env.USER_TYPE = 'ant'
    installCommonMocks({
      cachedEnabled: false,
      apiKey: 'test-key',
    })

    const {
      prefetchFastModeStatus,
      getFastModeUnavailableReason,
      _setFastModeTestHooks,
    } = await importFreshFastModeModule()
    _setFastModeTestHooks({
      getAnthropicApiKey: () => 'test-key',
      getClaudeAIOAuthTokens: () => null,
      hasProfileScope: () => false,
      fetchFastModeStatus: async () => {
        throw new Error('network fail')
      },
    })

    await prefetchFastModeStatus()

    expect(getFastModeUnavailableReason()).toBe(
      'Fast mode unavailable due to network connectivity issues',
    )
  })
})
