import { afterEach, describe, expect, mock, test } from 'bun:test'

import * as actualStateModule from '../bootstrap/state.js'
import * as actualAuthModule from './auth.js'
import * as actualConfigModule from './config.js'
import * as actualEnvModule from './env.js'
import * as actualEnvUtilsModule from './envUtils.js'

const originalEnv = { ...process.env }

function restoreProcessEnv(): void {
  for (const key of Object.keys(process.env)) {
    delete process.env[key]
  }
  Object.assign(process.env, originalEnv)
}

async function importFreshUserModule() {
  return import(`./user.ts?ts=${Date.now()}-${Math.random()}`)
}

function installCommonMocks(options?: {
  oauthEmail?: string
  gitEmail?: string
}) {
  mock.module('../bootstrap/state.js', () => ({
    ...actualStateModule,
    getSessionId: () => 'session-test',
  }))

  mock.module('./auth.js', () => ({
    ...actualAuthModule,
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
  }))

  mock.module('./config.js', () => ({
    ...actualConfigModule,
    getGlobalConfig: () => ({}),
    getOrCreateUserID: () => 'device-test',
  }))

  mock.module('./env.js', () => ({
    ...actualEnvModule,
    env: { platform: 'windows' },
    getHostPlatformForAnalytics: () => 'windows',
  }))

  mock.module('./envUtils.js', () => ({
    ...actualEnvUtilsModule,
    isEnvTruthy: (value: string | undefined) =>
      !!value && value !== '0' && value.toLowerCase() !== 'false',
  }))

  mock.module('execa', () => ({
    execa: async () => ({
      exitCode: options?.gitEmail ? 0 : 1,
      stdout: options?.gitEmail ?? '',
    }),
  }))
}

afterEach(() => {
  mock.restore()
  restoreProcessEnv()
  delete (globalThis as Record<string, unknown>).MACRO
})

describe('user email fallbacks', () => {
  test('getCoreUserData does not synthesize Anthropic email from COO_CREATOR', async () => {
    process.env.USER_TYPE = 'ant'
    process.env.COO_CREATOR = 'alice'
    ;(globalThis as Record<string, unknown>).MACRO = { VERSION: '0.0.0' }

    installCommonMocks()

    const { getCoreUserData } = await importFreshUserModule()
    const result = getCoreUserData()

    expect(result.email).toBeUndefined()
  })

  test('initUser falls back to git email when oauth email is missing', async () => {
    process.env.USER_TYPE = 'ant'
    process.env.COO_CREATOR = 'alice'
    ;(globalThis as Record<string, unknown>).MACRO = { VERSION: '0.0.0' }

    installCommonMocks({ gitEmail: 'git@example.com' })

    const { initUser, getCoreUserData } = await importFreshUserModule()
    await initUser()

    const result = getCoreUserData()
    expect(result.email).toBe('git@example.com')
  })
})
