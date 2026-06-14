import { afterEach, expect, mock, test } from 'bun:test'
import { homedir } from 'os'
import { join } from 'path'

import * as actualEnvModule from './env.js'

const originalEnv = { ...process.env }
const originalMacro = (globalThis as Record<string, unknown>).MACRO

function restoreProcessEnv(): void {
  for (const key of Object.keys(process.env)) {
    delete process.env[key]
  }
  Object.assign(process.env, originalEnv)
}

afterEach(() => {
  restoreProcessEnv()
  ;(globalThis as Record<string, unknown>).MACRO = originalMacro
  mock.restore()
})

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
