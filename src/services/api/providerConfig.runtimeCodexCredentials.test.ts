import { afterEach, expect, mock, test } from 'bun:test'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

import { resolveRuntimeCodexCredentials } from './providerConfig.js'

const importFresh = (specifier: string): Promise<any> => import(specifier)

afterEach(() => {
  mock.restore()
})

function makeJwt(payload: Record<string, unknown>): string {
  const header = Buffer.from(JSON.stringify({ alg: 'none', typ: 'JWT' }))
    .toString('base64url')
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url')
  return `${header}.${body}.signature`
}

test('runtime credential resolution honors explicit auth.json over stored secure-storage tokens', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaude-codex-explicit-auth-'))
  const authPath = join(tempDir, 'auth.json')

  writeFileSync(
    authPath,
    JSON.stringify({
      openai_api_key: makeJwt({
        'https://api.openai.com/auth': {
          chatgpt_account_id: 'acct_explicit_auth_json',
        },
      }),
    }),
    'utf8',
  )

  try {
    const credentials = resolveRuntimeCodexCredentials({
      env: {
        CODEX_AUTH_JSON_PATH: authPath,
      } as NodeJS.ProcessEnv,
      storedCredentials: {
        apiKey: 'stored-api-key',
        accessToken: 'stored-access-token',
        accountId: 'acct_stored',
      },
    })

    expect(credentials.source).toBe('auth.json')
    expect(credentials.accountId).toBe('acct_explicit_auth_json')
    expect(credentials.apiKey).not.toBe('stored-api-key')
  } finally {
    rmSync(tempDir, { force: true, recursive: true })
  }
})

test('runtime credential resolution preserves an explicit auth.json path even when it is missing', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaude-codex-missing-auth-'))
  const authPath = join(tempDir, 'missing-auth.json')

  try {
    const credentials = resolveRuntimeCodexCredentials({
      env: {
        CODEX_AUTH_JSON_PATH: authPath,
      } as NodeJS.ProcessEnv,
      storedCredentials: {
        apiKey: 'stored-api-key',
        accessToken: 'stored-access-token',
        accountId: 'acct_stored',
      },
    })

    expect(credentials.source).toBe('none')
    expect(credentials.authPath).toBe(authPath)
    expect(credentials.apiKey).toBe('')
  } finally {
    rmSync(tempDir, { force: true, recursive: true })
  }
})

test('runtime credential resolution avoids sync secure-storage reads when async credentials are provided', async () => {
  let syncReadCalled = false

  mock.module('../../utils/codexCredentials.js', () => ({
    isCodexRefreshFailureCoolingDown: () => false,
    readCodexCredentials: () => {
      syncReadCalled = true
      throw new Error('sync secure-storage read should not run in runtime resolution')
    },
  }))

  // @ts-ignore cache-busting query string for Bun module mocks
  const { resolveRuntimeCodexCredentials } = await importFresh('./providerConfig.js?runtime-no-sync-secure-storage')

  const credentials = resolveRuntimeCodexCredentials({
    env: {} as NodeJS.ProcessEnv,
    storedCredentials: {
      accessToken: 'stored-access-token',
      accountId: 'acct_stored',
    },
  })

  expect(syncReadCalled).toBe(false)
  expect(credentials.source).toBe('secure-storage')
  expect(credentials.apiKey).toBe('stored-access-token')
  expect(credentials.accountId).toBe('acct_stored')
})

test('stored Codex credentials prefer explicit account id and never require auth.json lookup', async () => {
  let syncReadCalled = false

  mock.module('../../utils/codexCredentials.js', () => ({
    isCodexRefreshFailureCoolingDown: () => false,
    readCodexCredentials: () => {
      syncReadCalled = true
      throw new Error('sync secure-storage read should not run')
    },
  }))

  // @ts-ignore cache-busting query string for Bun module mocks
  const { resolveStoredCodexCredentials } = await importFresh('./providerConfig.js?stored-codex-direct-guard')

  const credentials = resolveStoredCodexCredentials({
    envAccountId: 'acct_env',
    storedCredentials: {
      apiKey: 'stored-api-key',
      accessToken: makeJwt({
        'https://api.openai.com/auth': {
          chatgpt_account_id: 'acct_from_access_token',
        },
      }),
      idToken: makeJwt({
        'https://api.openai.com/auth': {
          chatgpt_account_id: 'acct_from_id_token',
        },
      }),
      accountId: 'acct_stored',
    },
  })

  expect(syncReadCalled).toBe(false)
  expect(credentials.source).toBe('secure-storage')
  expect(credentials.apiKey).toBe('stored-api-key')
  expect(credentials.accountId).toBe('acct_env')
  expect(credentials.authPath).toBeUndefined()
})

test('stored Codex credentials resolve account id by fallback priority', async () => {
  // @ts-ignore cache-busting query string for isolated import
  const { resolveStoredCodexCredentials } = await importFresh('./providerConfig.js?stored-codex-account-fallbacks')
  const accessTokenWithAccount = makeJwt({
    'https://api.openai.com/auth': {
      chatgpt_account_id: 'acct_from_access_token',
    },
  })
  const idTokenWithAccount = makeJwt({
    'https://api.openai.com/auth': {
      chatgpt_account_id: 'acct_from_id_token',
    },
  })

  expect(resolveStoredCodexCredentials({
    storedCredentials: {
      accessToken: accessTokenWithAccount,
      idToken: idTokenWithAccount,
      accountId: 'acct_stored',
    },
  }).accountId).toBe('acct_stored')

  expect(resolveStoredCodexCredentials({
    storedCredentials: {
      accessToken: accessTokenWithAccount,
      idToken: idTokenWithAccount,
    },
  }).accountId).toBe('acct_from_id_token')

  expect(resolveStoredCodexCredentials({
    storedCredentials: {
      accessToken: accessTokenWithAccount,
    },
  }).accountId).toBe('acct_from_access_token')
})
