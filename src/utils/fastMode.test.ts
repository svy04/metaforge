import { afterEach, describe, expect, mock, test } from 'bun:test'

import * as actualStateModule from '../bootstrap/state.js'
import * as actualAnalyticsModule from '../services/analytics/index.js'
import * as actualAuthModule from './auth.js'
import * as actualBundledModeModule from './bundledMode.js'
import * as actualConfigModule from './config.js'
import * as actualDebugModule from './debug.js'
import * as actualEnvUtilsModule from './envUtils.js'
import * as actualPrivacyLevelModule from './privacyLevel.js'

const originalEnv = { ...process.env }

function restoreProcessEnv(): void {
  for (const key of Object.keys(process.env)) {
    if (!(key in originalEnv)) {
      delete process.env[key]
    }
  }
  for (const [key, value] of Object.entries(originalEnv)) {
    process.env[key] = value
  }
}

async function importFreshFastModeModule() {
  return import(`./fastMode.ts?ts=${Date.now()}-${Math.random()}`)
}

function installCommonMocks(options?: {
  cachedEnabled?: boolean
  apiKey?: string | null
  oauthToken?: string | null
  hasProfileScope?: boolean
  axiosReject?: boolean
}) {
  mock.module('axios', () => ({
    default: {
      get: options?.axiosReject
        ? async () => {
            throw new Error('network fail')
          }
        : async () => ({ data: { enabled: false, disabled_reason: 'preference' } }),
      isAxiosError: () => false,
    },
  }))

  mock.module('src/constants/oauth.js', () => ({
    getOauthConfig: () => ({ BASE_API_URL: 'https://api.anthropic.com' }),
    OAUTH_BETA_HEADER: 'test-beta',
  }))

  mock.module('src/services/analytics/growthbook.js', () => ({
    getFeatureValue_CACHED_MAY_BE_STALE: (_name: string, defaultValue: unknown) =>
      defaultValue,
  }))

  mock.module('../bootstrap/state.js', () => ({
    ...actualStateModule,
    getIsNonInteractiveSession: () => false,
    getKairosActive: () => false,
    preferThirdPartyAuthentication: () => false,
  }))

  mock.module('../services/analytics/index.js', () => ({
    ...actualAnalyticsModule,
    logEvent: () => {},
  }))

  mock.module('./auth.js', () => ({
    ...actualAuthModule,
    getAnthropicApiKey: () => options?.apiKey ?? null,
    getClaudeAIOAuthTokens: () =>
      options?.oauthToken ? { accessToken: options.oauthToken } : null,
    handleOAuth401Error: async () => {},
    hasProfileScope: () => options?.hasProfileScope ?? false,
  }))

  mock.module('./bundledMode.js', () => ({
    ...actualBundledModeModule,
    isInBundledMode: () => true,
  }))

  mock.module('./config.js', () => ({
    ...actualConfigModule,
    getGlobalConfig: () => ({
      penguinModeOrgEnabled: options?.cachedEnabled === true,
    }),
    saveGlobalConfig: (updater: (current: Record<string, unknown>) => Record<string, unknown>) =>
      updater({ penguinModeOrgEnabled: options?.cachedEnabled === true }),
  }))

  mock.module('./debug.js', () => ({
    ...actualDebugModule,
    logForDebugging: () => {},
  }))

  mock.module('./envUtils.js', () => ({
    ...actualEnvUtilsModule,
    isEnvTruthy: (value: string | undefined) =>
      !!value && value !== '0' && value.toLowerCase() !== 'false',
  }))

  mock.module('./privacyLevel.js', () => ({
    ...actualPrivacyLevelModule,
    isEssentialTrafficOnly: () => false,
  }))
}

afterEach(() => {
  mock.restore()
  restoreProcessEnv()
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
    } = await importFreshFastModeModule()

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
      axiosReject: true,
    })

    const {
      prefetchFastModeStatus,
      getFastModeUnavailableReason,
    } = await importFreshFastModeModule()

    await prefetchFastModeStatus()

    expect(getFastModeUnavailableReason()).toBe(
      'Fast mode unavailable due to network connectivity issues',
    )
  })
})
