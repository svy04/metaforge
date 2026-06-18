import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { resolve } from 'node:path'

const allowedIdeSmokeEnvNames = new Set([
  'APPDATA',
  'COMSPEC',
  'HOMEDRIVE',
  'HOMEPATH',
  'LOCALAPPDATA',
  'NUMBER_OF_PROCESSORS',
  'OS',
  'PATH',
  'PATHEXT',
  'PROCESSOR_ARCHITECTURE',
  'PROCESSOR_IDENTIFIER',
  'PROCESSOR_LEVEL',
  'PROCESSOR_REVISION',
  'PROGRAMDATA',
  'PROGRAMFILES',
  'PROGRAMFILES(X86)',
  'PROGRAMW6432',
  'PSMODULEPATH',
  'PUBLIC',
  'SYSTEMDRIVE',
  'SYSTEMROOT',
  'TEMP',
  'TMP',
  'USERDOMAIN',
  'USERNAME',
  'USERPROFILE',
  'WINDIR',
])

type CliResultLike = {
  error?: {
    message?: string
  }
}

export function buildSanitizedIdeSmokeEnv(
  extraEnv: Record<string, string>,
  sourceEnv: NodeJS.ProcessEnv = process.env,
): NodeJS.ProcessEnv {
  const env: NodeJS.ProcessEnv = {}

  for (const [key, value] of Object.entries(sourceEnv)) {
    if (allowedIdeSmokeEnvNames.has(key.toUpperCase()) && typeof value === 'string') {
      env[key] = value
    }
  }

  const pathValue = sourceEnv.PATH ?? sourceEnv.Path
  if (typeof pathValue === 'string') {
    env.PATH = pathValue
    env.Path = pathValue
  }

  for (const [key, value] of Object.entries(extraEnv)) {
    env[key] = value
  }

  return env
}

export function getVscodeCliVersion(root = process.cwd()): string {
  const result = spawnSync('code', ['--version'], {
    cwd: root,
    encoding: 'utf8',
    shell: false,
  })

  if (result.status !== 0) {
    return 'not_available'
  }

  return (result.stdout ?? '').trim().split(/\r?\n/).filter(Boolean).join(' / ')
}

export function sleep(ms: number): void {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms)
}

export function waitForJsonResult<T>(resultPath: string, timeoutMs: number, intervalMs = 250): T | null {
  const deadline = Date.now() + timeoutMs

  while (Date.now() < deadline) {
    if (existsSync(resultPath)) {
      try {
        return JSON.parse(readFileSync(resultPath, 'utf8')) as T
      } catch {
        sleep(intervalMs)
        continue
      }
    }

    sleep(intervalMs)
  }

  return null
}

export function scanVscodeEnvironmentBlockers(logsDir: string): string[] {
  const blockers = new Set<string>()

  if (!existsSync(logsDir)) {
    return []
  }

  const pendingDirs = [logsDir]
  while (pendingDirs.length > 0) {
    const dir = pendingDirs.pop()
    if (!dir) {
      continue
    }

    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const entryPath = resolve(dir, entry.name)
      if (entry.isDirectory()) {
        pendingDirs.push(entryPath)
        continue
      }
      if (!entry.isFile() || !entry.name.endsWith('.log')) {
        continue
      }

      const logText = readFileSync(entryPath, 'utf8')
      if (logText.includes('Code is currently being updated') || logText.includes('vscode-updating still held')) {
        blockers.add('vscode_update_in_progress')
      }
    }
  }

  return [...blockers]
}

export function collectVscodeEnvironmentBlockers(logsDir: string, timeoutMs = 2000, intervalMs = 250): string[] {
  const deadline = Date.now() + timeoutMs
  while (Date.now() < deadline) {
    const blockers = scanVscodeEnvironmentBlockers(logsDir)
    if (blockers.length > 0) {
      return blockers
    }
    sleep(intervalMs)
  }
  return scanVscodeEnvironmentBlockers(logsDir)
}

export function withCliEnvironmentBlockers(
  blockers: string[],
  result: CliResultLike,
  vscodeCliVersion: string,
): string[] {
  const next = new Set(blockers)
  const errorMessage = result.error?.message ?? ''
  if (vscodeCliVersion === 'not_available' || errorMessage.includes('Executable not found')) {
    next.add('vscode_cli_unavailable')
  }
  return [...next]
}
