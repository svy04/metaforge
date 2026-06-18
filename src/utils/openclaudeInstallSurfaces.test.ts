import { afterEach, expect, mock, test } from 'bun:test'
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { homedir } from 'os'
import { join } from 'path'

import * as actualEnvModule from './env.js'

const originalEnv = { ...process.env }
const originalMacro = (globalThis as Record<string, unknown>).MACRO
const tempDirs: string[] = []

function restoreProcessEnv(): void {
  for (const key of Object.keys(process.env)) {
    delete process.env[key]
  }
  Object.assign(process.env, originalEnv)
}

afterEach(async () => {
  restoreProcessEnv()
  ;(globalThis as Record<string, unknown>).MACRO = originalMacro
  mock.restore()
  await Promise.all(tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })))
})

async function makeTempDir(): Promise<string> {
  const dir = await mkdtemp(join(tmpdir(), 'openclaude-native-installer-'))
  tempDirs.push(dir)
  return dir
}

async function importFreshInstallCommand() {
  return import(`../commands/install.tsx?ts=${Date.now()}-${Math.random()}`)
}

async function importFreshInstaller() {
  return import(`./nativeInstaller/installer.ts?ts=${Date.now()}-${Math.random()}`)
}

test('install command displays ~/.local/bin/openclaude on non-Windows', async () => {
  mock.module('../utils/env.js', () => ({
    ...actualEnvModule,
    env: { platform: 'darwin' },
  }))

  const { getInstallationPath } = await importFreshInstallCommand()

  expect(getInstallationPath()).toBe('~/.local/bin/openclaude')
})

test('install command displays openclaude.exe path on Windows', async () => {
  mock.module('../utils/env.js', () => ({
    ...actualEnvModule,
    env: { platform: 'win32' },
  }))

  const { getInstallationPath } = await importFreshInstallCommand()

  expect(getInstallationPath()).toBe(
    join(homedir(), '.local', 'bin', 'openclaude.exe').replace(/\//g, '\\'),
  )
})

test('cleanupNpmInstallations removes both openclaude and legacy claude local install dirs', async () => {
  const removedPaths: string[] = []
  ;(globalThis as Record<string, unknown>).MACRO = {
    PACKAGE_URL: '@gitlawb/openclaude',
  }

  const { cleanupNpmInstallations } = await importFreshInstaller()
  await cleanupNpmInstallations({
    attemptNpmUninstall: async () => ({ success: false }),
    configHomeDir: join(homedir(), '.openclaude'),
    homeDir: homedir(),
    removeLocalInstallDir: async (path: string) => {
      removedPaths.push(path)
    },
  })

  expect(removedPaths).toContain(join(homedir(), '.openclaude', 'local'))
  expect(removedPaths).toContain(join(homedir(), '.claude', 'local'))
})

test('native installer creates version placeholder atomically without clobbering existing files', async () => {
  const root = await makeTempDir()
  const missingPath = join(root, 'missing-version')
  const existingPath = join(root, 'existing-version')
  const collidingDirectory = join(root, 'directory-version')

  await writeFile(existingPath, 'already installed', 'utf8')
  await mkdir(collidingDirectory)

  const { ensureVersionPlaceholderFile } = await importFreshInstaller()

  await ensureVersionPlaceholderFile(missingPath)
  await expect(readFile(missingPath, 'utf8')).resolves.toBe('')

  await ensureVersionPlaceholderFile(existingPath)
  await expect(readFile(existingPath, 'utf8')).resolves.toBe('already installed')

  await expect(ensureVersionPlaceholderFile(collidingDirectory)).rejects.toThrow()
})
