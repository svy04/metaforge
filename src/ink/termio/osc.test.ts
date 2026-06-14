import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test'
import { join } from 'node:path'

import * as actualExecFileNoThrowModule from '../../utils/execFileNoThrow.js'

const originalEnv = { ...process.env }
const originalPlatform = process.platform
const mockedClipboardPath = join(process.cwd(), 'openclaude-clipboard.txt')

const generateTempFilePathMock = mock(() => mockedClipboardPath)

const execFileNoThrowMock = mock(
  async () => ({ code: 0, stdout: '', stderr: '' }),
)
let execFileNoThrowOverride:
  | typeof actualExecFileNoThrowModule.execFileNoThrow
  | undefined
type ExecFileNoThrowCall = [
  command: string,
  args?: string[],
  options?: Record<string, unknown>,
]

function execFileNoThrowCalls(): ExecFileNoThrowCall[] {
  return execFileNoThrowMock.mock.calls as unknown as ExecFileNoThrowCall[]
}

function restoreProcessEnv(): void {
  for (const key of Object.keys(process.env)) {
    delete process.env[key]
  }
  Object.assign(process.env, originalEnv)
}

function installOscMocks(): void {
  mock.module('../../utils/execFileNoThrow.js', () => ({
    ...actualExecFileNoThrowModule,
    execFileNoThrow: (
      ...args: Parameters<typeof actualExecFileNoThrowModule.execFileNoThrow>
    ) =>
      (
        execFileNoThrowOverride ??
        actualExecFileNoThrowModule.execFileNoThrow
      )(...args),
  }))

  mock.module('../../utils/tempfile.js', () => ({
    generateTempFilePath: generateTempFilePathMock,
  }))
}

async function importFreshOscModule() {
  return import(`./osc.ts?ts=${Date.now()}-${Math.random()}`)
}

async function flushClipboardCopy(): Promise<void> {
  await new Promise(resolve => setTimeout(resolve, 0))
}

async function waitForExecCall(
  command: string,
  attempts = 20,
): Promise<ExecFileNoThrowCall | undefined> {
  for (let attempt = 0; attempt < attempts; attempt++) {
    const call = execFileNoThrowCalls().find(([cmd]) => cmd === command)
    if (call) {
      return call
    }
    await flushClipboardCopy()
  }

  return undefined
}

describe('Windows clipboard fallback', () => {
  beforeEach(() => {
    installOscMocks()
    execFileNoThrowOverride =
      execFileNoThrowMock as unknown as typeof actualExecFileNoThrowModule.execFileNoThrow
    execFileNoThrowMock.mockClear()
    generateTempFilePathMock.mockClear()
    restoreProcessEnv()
    delete process.env['SSH_CONNECTION']
    delete process.env['TMUX']
    Object.defineProperty(process, 'platform', { value: 'win32' })
  })

  afterEach(() => {
    restoreProcessEnv()
    Object.defineProperty(process, 'platform', { value: originalPlatform })
    execFileNoThrowOverride = undefined
    mock.restore()
  })

  test('uses PowerShell instead of clip.exe for local Windows copy', async () => {
    const { setClipboard } = await importFreshOscModule()

    await setClipboard('Привет мир')
    const windowsCall = await waitForExecCall('powershell')

    expect(execFileNoThrowCalls().some(([cmd]) => cmd === 'clip')).toBe(
      false,
    )
    expect(windowsCall).toBeDefined()
  })

  test('passes Windows clipboard text through a UTF-8 temp file instead of stdin', async () => {
    const { setClipboard } = await importFreshOscModule()

    await setClipboard('Привет мир')
    await flushClipboardCopy()

    const windowsCall = await waitForExecCall('powershell')

    expect(windowsCall?.[2]).toMatchObject({
      stdin: 'ignore',
    })
    expect(windowsCall?.[2]).not.toMatchObject({ input: 'Привет мир' })
    expect(windowsCall?.[2]).not.toMatchObject({
      env: expect.objectContaining({
        OPENCLAUDE_CLIPBOARD_TEXT_B64: expect.any(String),
      }),
    })
    expect(windowsCall?.[1]).toContain(
      `$text = [System.IO.File]::ReadAllText('${mockedClipboardPath.replace(/'/g, "''")}', [System.Text.Encoding]::UTF8); Set-Clipboard -Value $text`,
    )
  })
})

describe('clipboard path behavior remains stable', () => {
  beforeEach(() => {
    installOscMocks()
    execFileNoThrowOverride =
      execFileNoThrowMock as unknown as typeof actualExecFileNoThrowModule.execFileNoThrow
    execFileNoThrowMock.mockClear()
    restoreProcessEnv()
    delete process.env['SSH_CONNECTION']
    delete process.env['TMUX']
  })

  afterEach(() => {
    restoreProcessEnv()
    Object.defineProperty(process, 'platform', { value: originalPlatform })
    execFileNoThrowOverride = undefined
    mock.restore()
  })

  test('getClipboardPath stays native on local macOS', async () => {
    Object.defineProperty(process, 'platform', { value: 'darwin' })
    const { getClipboardPath } = await importFreshOscModule()

    expect(getClipboardPath()).toBe('native')
  })

  test('getClipboardPath stays tmux-buffer when TMUX is set', async () => {
    Object.defineProperty(process, 'platform', { value: 'linux' })
    process.env['TMUX'] = '/tmp/tmux-1000/default,123,0'
    const { getClipboardPath } = await importFreshOscModule()

    expect(getClipboardPath()).toBe('tmux-buffer')
  })

  test('Windows clipboard fallback is skipped over SSH', async () => {
    Object.defineProperty(process, 'platform', { value: 'win32' })
    process.env['SSH_CONNECTION'] = '1 2 3 4'
    const { setClipboard } = await importFreshOscModule()

    await setClipboard('Привет мир')

    expect(execFileNoThrowCalls().some(([cmd]) => cmd === 'powershell')).toBe(
      false,
    )
  })

  test('local macOS clipboard fallback still uses pbcopy', async () => {
    Object.defineProperty(process, 'platform', { value: 'darwin' })
    const { setClipboard } = await importFreshOscModule()

    await setClipboard('hello')

    expect(execFileNoThrowCalls().some(([cmd]) => cmd === 'pbcopy')).toBe(
      true,
    )
  })
})
