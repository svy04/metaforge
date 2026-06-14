import { afterEach, describe, expect, test } from 'bun:test'

import {
  _resetUserTestHooks,
  _setUserTestHooks,
  getCoreUserData,
  initUser,
} from './user.js'

const originalEnv = { ...process.env }

function installCommonMocks(options?: {
  oauthEmail?: string
  gitEmail?: string
}) {
  _setUserTestHooks({
    getSessionId: (() => 'session-test') as never,
    getOauthAccountInfo: () =>
      options?.oauthEmail
        ? {
            emailAddress: options.oauthEmail,
            organizationUuid: 'org-test',
            accountUuid: 'acct-test',
          }
        : undefined,
    getRateLimitTier: () => null,
    getSubscriptionType: () => null,
    getGlobalConfig: (() => ({})) as never,
    getOrCreateUserID: () => 'device-test',
    getCwd: () => 'C:\\repo',
    getHostPlatformForAnalytics: (() => 'windows') as never,
    isEnvTruthy: (value: string | boolean | undefined) =>
      !!value &&
      value !== '0' &&
      String(value).toLowerCase() !== 'false',
    execa: (async () => ({
      exitCode: options?.gitEmail ? 0 : 1,
      stdout: options?.gitEmail ?? '',
    })) as never,
  })
}

afterEach(() => {
  _resetUserTestHooks()
  process.env = { ...originalEnv }
  delete (globalThis as Record<string, unknown>).MACRO
})

describe('user email fallbacks', () => {
  test('getCoreUserData does not synthesize Anthropic email from COO_CREATOR', async () => {
    process.env.USER_TYPE = 'ant'
    process.env.COO_CREATOR = 'alice'
    ;(globalThis as Record<string, unknown>).MACRO = { VERSION: '0.0.0' }

    installCommonMocks()

    const result = getCoreUserData()

    expect(result.email).toBeUndefined()
  })

  test('initUser falls back to git email when oauth email is missing', async () => {
    process.env.USER_TYPE = 'ant'
    process.env.COO_CREATOR = 'alice'
    ;(globalThis as Record<string, unknown>).MACRO = { VERSION: '0.0.0' }

    installCommonMocks({ gitEmail: 'git@example.com' })

    await initUser()

    const result = getCoreUserData()
    expect(result.email).toBe('git@example.com')
  })
})
