import { isBareMode } from './envUtils.js'
import {
  getSecureStorage,
  type SecureStorageData,
} from './secureStorage/index.js'
import {
  asTrimmedString,
  CODEX_REFRESH_URL,
  exchangeCodexIdTokenForApiKey,
  getCodexOAuthClientId,
  parseChatgptAccountId,
  decodeJwtPayload,
} from '../services/api/codexOAuthShared.js'

export const CODEX_STORAGE_KEY = 'codex' as const
const CODEX_ACCOUNTS_STORAGE_KEY = 'codexAccounts' as const
const CODEX_ACCOUNT_CURSOR_STORAGE_KEY = 'codexAccountCursor' as const
const CODEX_TOKEN_REFRESH_SKEW_MS = 60_000
const CODEX_TOKEN_REFRESH_RETRY_COOLDOWN_MS = 60_000

export type CodexCredentialBlob = {
  apiKey?: string
  accessToken: string
  refreshToken?: string
  idToken?: string
  accountId?: string
  profileId?: string
  lastRefreshAt?: number
  lastRefreshFailureAt?: number
}

type CodexTokenRefreshResponse = {
  access_token?: string
  refresh_token?: string
  id_token?: string
}

let inFlightCodexRefresh:
  | Promise<{
      refreshed: boolean
      credentials?: CodexCredentialBlob
    }>
  | null = null
let inMemoryLastRefreshFailureAt: number | null = null

function getCodexSecureStorage() {
  return getSecureStorage({ allowPlainTextFallback: false })
}

function parseJwtExpiryMs(token: string | undefined): number | undefined {
  if (!token) return undefined
  const payload = decodeJwtPayload(token)
  const exp = payload?.exp
  if (typeof exp === 'number' && Number.isFinite(exp)) {
    return exp * 1000
  }
  return undefined
}

function normalizeCodexCredentialBlob(
  value: unknown,
): CodexCredentialBlob | undefined {
  if (!value || typeof value !== 'object') return undefined

  const record = value as Record<string, unknown>
  const apiKey = asTrimmedString(record.apiKey)
  const accessToken = asTrimmedString(record.accessToken)
  if (!accessToken) return undefined

  const refreshToken = asTrimmedString(record.refreshToken)
  const idToken = asTrimmedString(record.idToken)
  const accountId =
    asTrimmedString(record.accountId) ??
    parseChatgptAccountId(idToken) ??
    parseChatgptAccountId(accessToken)
  const profileId = asTrimmedString(record.profileId)

  const lastRefreshAt =
    typeof record.lastRefreshAt === 'number' &&
    Number.isFinite(record.lastRefreshAt)
      ? record.lastRefreshAt
      : undefined
  const lastRefreshFailureAt =
    typeof record.lastRefreshFailureAt === 'number' &&
    Number.isFinite(record.lastRefreshFailureAt)
      ? record.lastRefreshFailureAt
      : undefined

  return {
    apiKey,
    accessToken,
    refreshToken,
    idToken,
    accountId,
    profileId,
    lastRefreshAt,
    lastRefreshFailureAt,
  }
}

function persistableCodexCredential(
  credential: CodexCredentialBlob,
): CodexCredentialBlob {
  return Object.fromEntries(
    Object.entries(credential).filter(([, value]) => value !== undefined),
  ) as CodexCredentialBlob
}

function codexCredentialKey(credential: CodexCredentialBlob): string {
  if (credential.accountId) return `account:${credential.accountId}`
  if (credential.profileId) return `profile:${credential.profileId}`
  return `token:${credential.accessToken}`
}

function readCodexCredentialCandidatesFromData(
  data: SecureStorageData | Record<string, unknown> | null | undefined,
): CodexCredentialBlob[] {
  if (!data || typeof data !== 'object') return []

  const candidates: CodexCredentialBlob[] = []
  const addCandidate = (value: unknown) => {
    const normalized = normalizeCodexCredentialBlob(value)
    if (normalized) {
      candidates.push(normalized)
    }
  }

  const storedAccounts =
    (data as Record<string, unknown>)[CODEX_ACCOUNTS_STORAGE_KEY]
  if (Array.isArray(storedAccounts)) {
    for (const account of storedAccounts) {
      addCandidate(account)
    }
  }
  addCandidate((data as Record<string, unknown>)[CODEX_STORAGE_KEY])

  const deduped = new Map<string, CodexCredentialBlob>()
  for (const candidate of candidates) {
    deduped.set(codexCredentialKey(candidate), {
      ...deduped.get(codexCredentialKey(candidate)),
      ...candidate,
    })
  }
  return [...deduped.values()]
}

function upsertCodexCredentialCandidate(
  candidates: CodexCredentialBlob[],
  credential: CodexCredentialBlob,
): CodexCredentialBlob[] {
  const next = new Map<string, CodexCredentialBlob>()
  for (const candidate of candidates) {
    next.set(codexCredentialKey(candidate), persistableCodexCredential(candidate))
  }
  const key = codexCredentialKey(credential)
  next.set(key, {
    ...next.get(key),
    ...persistableCodexCredential(credential),
  })
  return [...next.values()]
}

function getCodexAccountCursor(
  data: SecureStorageData | Record<string, unknown> | null | undefined,
): number {
  const value =
    data && typeof data === 'object'
      ? (data as Record<string, unknown>)[CODEX_ACCOUNT_CURSOR_STORAGE_KEY]
      : undefined
  return typeof value === 'number' && Number.isFinite(value) ? value : -1
}

function activateCodexCredentialCandidate(
  credential: CodexCredentialBlob,
  cursorIndex: number,
): { success: boolean; warning?: string } {
  if (isBareMode()) {
    return { success: false, warning: 'Bare mode: secure storage is disabled.' }
  }

  const secureStorage = getCodexSecureStorage()
  const previous = secureStorage.read() || {}
  const next = {
    ...(previous as Record<string, unknown>),
    [CODEX_STORAGE_KEY]: persistableCodexCredential(credential),
    [CODEX_ACCOUNT_CURSOR_STORAGE_KEY]: cursorIndex,
  }
  const result = secureStorage.update(next as SecureStorageData)
  if (result.success) {
    inMemoryLastRefreshFailureAt = credential.lastRefreshFailureAt ?? null
  }
  return result
}

function selectCodexCredentialCandidate(options?: {
  failedAccountId?: string
}): CodexCredentialBlob | undefined {
  if (isBareMode()) return undefined

  try {
    const data = getCodexSecureStorage().read()
    const candidates = readCodexCredentialCandidatesFromData(data)
    if (candidates.length === 0) return undefined

    const cursor = getCodexAccountCursor(data)
    const failedIndex = options?.failedAccountId
      ? candidates.findIndex(
          candidate => candidate.accountId === options.failedAccountId,
        )
      : -1
    const startIndex = failedIndex >= 0 ? failedIndex : cursor

    for (let offset = 1; offset <= candidates.length; offset++) {
      const index = (startIndex + offset) % candidates.length
      const candidate = candidates[index]
      if (
        options?.failedAccountId &&
        candidate.accountId === options.failedAccountId &&
        candidates.length > 1
      ) {
        continue
      }

      const result = activateCodexCredentialCandidate(candidate, index)
      return result.success ? candidate : undefined
    }
  } catch {
    return undefined
  }

  return undefined
}

async function selectCodexCredentialCandidateAsync(options?: {
  failedAccountId?: string
}): Promise<CodexCredentialBlob | undefined> {
  if (isBareMode()) return undefined

  try {
    const data = await getCodexSecureStorage().readAsync()
    const candidates = readCodexCredentialCandidatesFromData(data)
    if (candidates.length === 0) return undefined

    const cursor = getCodexAccountCursor(data)
    const failedIndex = options?.failedAccountId
      ? candidates.findIndex(
          candidate => candidate.accountId === options.failedAccountId,
        )
      : -1
    const startIndex = failedIndex >= 0 ? failedIndex : cursor

    for (let offset = 1; offset <= candidates.length; offset++) {
      const index = (startIndex + offset) % candidates.length
      const candidate = candidates[index]
      if (
        options?.failedAccountId &&
        candidate.accountId === options.failedAccountId &&
        candidates.length > 1
      ) {
        continue
      }

      const result = activateCodexCredentialCandidate(candidate, index)
      return result.success ? candidate : undefined
    }
  } catch {
    return undefined
  }

  return undefined
}

function shouldRefreshCodexToken(blob: CodexCredentialBlob): boolean {
  const expiresAt =
    parseJwtExpiryMs(blob.accessToken) ?? parseJwtExpiryMs(blob.idToken)
  if (expiresAt === undefined) {
    return false
  }
  return expiresAt <= Date.now() + CODEX_TOKEN_REFRESH_SKEW_MS
}

function isWithinRefreshFailureCooldown(
  blob: CodexCredentialBlob,
  now = Date.now(),
): boolean {
  const lastRefreshFailureAt = Math.max(
    blob.lastRefreshFailureAt ?? 0,
    inMemoryLastRefreshFailureAt ?? 0,
  )

  if (!lastRefreshFailureAt) {
    return false
  }

  return (
    now - lastRefreshFailureAt < CODEX_TOKEN_REFRESH_RETRY_COOLDOWN_MS
  )
}

function getRefreshErrorMessage(
  status: number,
  bodyText: string,
): string {
  if (!bodyText.trim()) {
    return `Codex token refresh failed with status ${status}.`
  }

  try {
    const parsed = JSON.parse(bodyText) as Record<string, unknown>
    const nestedError =
      parsed.error && typeof parsed.error === 'object'
        ? (parsed.error as Record<string, unknown>)
        : undefined
    const code = asTrimmedString(nestedError?.code ?? parsed.code)
    const message =
      asTrimmedString(nestedError?.message ?? parsed.error_description) ??
      bodyText.trim()
    return code
      ? `Codex token refresh failed (${code}): ${message}`
      : `Codex token refresh failed with status ${status}: ${message}`
  } catch {
    return `Codex token refresh failed with status ${status}: ${bodyText.trim()}`
  }
}

export function readCodexCredentials(): CodexCredentialBlob | undefined {
  if (isBareMode()) return undefined

  try {
    const data = getCodexSecureStorage().read()
    return normalizeCodexCredentialBlob(data?.codex)
  } catch {
    return undefined
  }
}

export async function readCodexCredentialsAsync(): Promise<
  CodexCredentialBlob | undefined
> {
  if (isBareMode()) return undefined

  try {
    const data = await getCodexSecureStorage().readAsync()
    return normalizeCodexCredentialBlob(data?.codex)
  } catch {
    return undefined
  }
}

export function isCodexRefreshFailureCoolingDown(
  blob: Pick<CodexCredentialBlob, 'lastRefreshFailureAt'>,
  now = Date.now(),
): boolean {
  return isWithinRefreshFailureCooldown(
    blob as CodexCredentialBlob,
    now,
  )
}

export function saveCodexCredentials(
  credentials: CodexCredentialBlob,
): { success: boolean; warning?: string } {
  if (isBareMode()) {
    return { success: false, warning: 'Bare mode: secure storage is disabled.' }
  }

  const normalized = normalizeCodexCredentialBlob(credentials)
  if (!normalized) {
    return { success: false, warning: 'Codex credentials are incomplete.' }
  }

  const secureStorage = getCodexSecureStorage()
  const previous = secureStorage.read() || {}
  const previousCodex = normalizeCodexCredentialBlob(previous[CODEX_STORAGE_KEY])
  const normalizedWithMetadata = persistableCodexCredential({
    ...normalized,
    profileId: normalized.profileId ?? previousCodex?.profileId,
    lastRefreshAt: normalized.lastRefreshAt ?? Date.now(),
  })
  const accountCandidates = upsertCodexCredentialCandidate(
    readCodexCredentialCandidatesFromData(previous),
    normalizedWithMetadata,
  )
  const next = {
    ...(previous as Record<string, unknown>),
    [CODEX_STORAGE_KEY]: normalizedWithMetadata,
    [CODEX_ACCOUNTS_STORAGE_KEY]: accountCandidates,
  }
  const result = secureStorage.update(next as typeof previous)
  if (result.success) {
    const storedCodex = normalizeCodexCredentialBlob(next[CODEX_STORAGE_KEY])
    inMemoryLastRefreshFailureAt = storedCodex?.lastRefreshFailureAt ?? null
  }
  return result
}

export function readCodexCredentialCandidates(): CodexCredentialBlob[] {
  if (isBareMode()) return []

  try {
    const data = getCodexSecureStorage().read()
    return readCodexCredentialCandidatesFromData(data)
  } catch {
    return []
  }
}

export async function readCodexCredentialCandidatesAsync(): Promise<
  CodexCredentialBlob[]
> {
  if (isBareMode()) return []

  try {
    const data = await getCodexSecureStorage().readAsync()
    return readCodexCredentialCandidatesFromData(data)
  } catch {
    return []
  }
}

export function selectNextCodexCredentialsForRequest():
  | CodexCredentialBlob
  | undefined {
  return selectCodexCredentialCandidate()
}

export async function selectNextCodexCredentialsForRequestAsync(): Promise<
  CodexCredentialBlob | undefined
> {
  return selectCodexCredentialCandidateAsync()
}

export function selectNextCodexCredentialsAfterFailure(options: {
  failedAccountId?: string
}): CodexCredentialBlob | undefined {
  return selectCodexCredentialCandidate(options)
}

export async function selectNextCodexCredentialsAfterFailureAsync(options: {
  failedAccountId?: string
}): Promise<CodexCredentialBlob | undefined> {
  return selectCodexCredentialCandidateAsync(options)
}

export function attachCodexProfileIdToStoredCredentials(profileId: string): {
  success: boolean
  warning?: string
} {
  if (isBareMode()) {
    return { success: false, warning: 'Bare mode: secure storage is disabled.' }
  }

  const current = readCodexCredentials()
  if (!current) {
    return {
      success: false,
      warning: 'Codex credentials are not stored securely yet.',
    }
  }

  return saveCodexCredentials({
    ...current,
    profileId,
  })
}

function persistCodexRefreshFailure(
  credentials: CodexCredentialBlob,
  occurredAt: number,
): void {
  const result = saveCodexCredentials({
    ...credentials,
    lastRefreshFailureAt: occurredAt,
  })
  if (!result.success) {
    inMemoryLastRefreshFailureAt = occurredAt
  }
}

export function clearCodexCredentials(): {
  success: boolean
  warning?: string
} {
  if (isBareMode()) {
    return { success: true }
  }

  const secureStorage = getCodexSecureStorage()
  const previous = secureStorage.read() || {}
  const next = { ...(previous as Record<string, unknown>) }
  delete next[CODEX_STORAGE_KEY]
  delete next[CODEX_ACCOUNTS_STORAGE_KEY]
  delete next[CODEX_ACCOUNT_CURSOR_STORAGE_KEY]
  const result = secureStorage.update(next as typeof previous)
  if (result.success) {
    inMemoryLastRefreshFailureAt = null
  }
  return result
}

export async function refreshCodexAccessTokenIfNeeded(options?: {
  force?: boolean
}): Promise<{
  refreshed: boolean
  credentials?: CodexCredentialBlob
}> {
  if (isBareMode()) {
    return { refreshed: false }
  }

  if (process.env.CODEX_API_KEY?.trim()) {
    return { refreshed: false }
  }

  const current = await readCodexCredentialsAsync()
  if (!current) {
    return { refreshed: false }
  }

  const refreshToken = current.refreshToken
  if (!refreshToken) {
    return { refreshed: false, credentials: current }
  }

  if (!options?.force && !shouldRefreshCodexToken(current)) {
    return { refreshed: false, credentials: current }
  }

  if (!options?.force && isWithinRefreshFailureCooldown(current)) {
    return { refreshed: false, credentials: current }
  }

  if (inFlightCodexRefresh) {
    return inFlightCodexRefresh
  }

  inFlightCodexRefresh = (async () => {
    const refreshAttemptedAt = Date.now()

    try {
      const body = new URLSearchParams({
        client_id: getCodexOAuthClientId(),
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
      })

      const response = await fetch(CODEX_REFRESH_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body,
        signal: AbortSignal.timeout(15_000),
      })

      if (!response.ok) {
        const bodyText = await response.text().catch(() => '')
        throw new Error(getRefreshErrorMessage(response.status, bodyText))
      }

      const payload = (await response.json()) as CodexTokenRefreshResponse
      const accessToken = asTrimmedString(payload.access_token)
      if (!accessToken) {
        throw new Error(
          'Codex token refresh succeeded without a new access token.',
        )
      }

      const next: CodexCredentialBlob = {
        accessToken,
        refreshToken:
          asTrimmedString(payload.refresh_token) ?? current.refreshToken,
        idToken: asTrimmedString(payload.id_token) ?? current.idToken,
        accountId:
          parseChatgptAccountId(payload.id_token) ??
          parseChatgptAccountId(payload.access_token) ??
          current.accountId,
        lastRefreshAt: Date.now(),
      }

      const idTokenForExchange = next.idToken ?? current.idToken
      if (idTokenForExchange) {
        next.apiKey = await exchangeCodexIdTokenForApiKey(
          idTokenForExchange,
        ).catch(() => undefined)
      }

      const saveResult = saveCodexCredentials(next)
      if (!saveResult.success) {
        throw new Error(
          saveResult.warning ??
            'Codex token refresh succeeded but credentials could not be saved.',
        )
      }

      return {
        refreshed: true,
        credentials: next,
      }
    } catch (error) {
      persistCodexRefreshFailure(current, refreshAttemptedAt)
      throw error
    } finally {
      inFlightCodexRefresh = null
    }
  })()

  return inFlightCodexRefresh
}
