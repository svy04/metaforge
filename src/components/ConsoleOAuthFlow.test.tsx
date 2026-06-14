import { PassThrough } from 'node:stream'

import { expect, mock, test } from 'bun:test'
import React from 'react'
import stripAnsi from 'strip-ansi'

import { AppStateProvider } from '../state/AppState.js'
import { Box, Text, createRoot } from '../ink.js'
import { KeybindingSetup } from '../keybindings/KeybindingProviderSetup.js'

mock.module('./ProviderManager.js', () => ({
  ProviderManager: ({ mode }: { mode: 'first-run' | 'manage' }) => (
    <Box flexDirection="column">
      <Text>{mode === 'first-run' ? 'Set up provider' : 'Provider manager'}</Text>
      <Text>Anthropic</Text>
      <Text>Azure OpenAI</Text>
      <Text>DeepSeek</Text>
      <Text>Google Gemini</Text>
    </Box>
  ),
}))

const { ConsoleOAuthFlow } = await import('./ConsoleOAuthFlow.js')

const SYNC_START = '\x1B[?2026h'
const SYNC_END = '\x1B[?2026l'

function extractLastFrame(output: string): string {
  let lastFrame: string | null = null
  let cursor = 0

  while (cursor < output.length) {
    const start = output.indexOf(SYNC_START, cursor)
    if (start === -1) {
      break
    }

    const contentStart = start + SYNC_START.length
    const end = output.indexOf(SYNC_END, contentStart)
    if (end === -1) {
      break
    }

    const frame = output.slice(contentStart, end)
    if (frame.trim().length > 0) {
      lastFrame = frame
    }
    cursor = end + SYNC_END.length
  }

  return lastFrame ?? output
}

function createTestStreams(): {
  stdout: PassThrough
  stdin: PassThrough & {
    isTTY: boolean
    setRawMode: (mode: boolean) => void
    ref: () => void
    unref: () => void
  }
  getOutput: () => string
} {
  let output = ''
  const stdout = new PassThrough()
  const stdin = new PassThrough() as PassThrough & {
    isTTY: boolean
    setRawMode: (mode: boolean) => void
    ref: () => void
    unref: () => void
  }

  stdin.isTTY = true
  stdin.setRawMode = () => {}
  stdin.ref = () => {}
  stdin.unref = () => {}
  ;(stdout as unknown as { columns: number }).columns = 120
  stdout.on('data', chunk => {
    output += chunk.toString()
  })

  return {
    stdout,
    stdin,
    getOutput: () => output,
  }
}

async function waitForCondition(
  predicate: () => boolean,
  options?: { timeoutMs?: number; intervalMs?: number },
): Promise<void> {
  const timeoutMs = options?.timeoutMs ?? 2500
  const intervalMs = options?.intervalMs ?? 10
  const startedAt = Date.now()

  while (Date.now() - startedAt < timeoutMs) {
    if (predicate()) {
      return
    }
    await Bun.sleep(intervalMs)
  }

  throw new Error('Timed out waiting for ConsoleOAuthFlow test condition')
}

async function waitForFrameOutput(
  getOutput: () => string,
  predicate: (output: string) => boolean,
  timeoutMs = 2500,
): Promise<string> {
  let output = ''

  await waitForCondition(() => {
    output = stripAnsi(extractLastFrame(getOutput()))
    return predicate(output)
  }, { timeoutMs })

  return output
}

async function renderFrame(
  node: React.ReactNode,
  options?: {
    waitForOutput?: (output: string) => boolean
    timeoutMs?: number
  },
): Promise<string> {
  const { stdout, stdin, getOutput } = createTestStreams()
  const root = await createRoot({
    stdout: stdout as unknown as NodeJS.WriteStream,
    stdin: stdin as unknown as NodeJS.ReadStream,
    patchConsole: false,
  })

  root.render(
    <AppStateProvider>
      <KeybindingSetup>{node}</KeybindingSetup>
    </AppStateProvider>,
  )

  try {
    if (options?.waitForOutput) {
      return await waitForFrameOutput(
        getOutput,
        options.waitForOutput,
        options.timeoutMs,
      )
    }

    await Bun.sleep(50)
    return stripAnsi(extractLastFrame(getOutput()))
  } finally {
    root.unmount()
    stdin.end()
    stdout.end()
    await Bun.sleep(0)
  }
}

test('login picker shows the third-party platform option', async () => {
  const output = await renderFrame(<ConsoleOAuthFlow onDone={() => {}} />)

  expect(output).toContain('Select login method:')
  expect(output).toContain('3rd-party platform')
})

test('third-party provider branch opens the first-run provider manager', async () => {
  const output = await renderFrame(
    <ConsoleOAuthFlow
      initialStatus={{ state: 'platform_setup' }}
      onDone={() => {}}
    />,
    {
      waitForOutput: frame =>
        frame.includes('Set up provider') &&
        frame.includes('Anthropic') &&
        frame.includes('Azure OpenAI') &&
        frame.includes('DeepSeek') &&
        frame.includes('Google Gemini'),
    },
  )

  expect(output).toContain('Set up provider')
  // Use alphabetically-early sentinels so they remain visible in the
  // 13-row test frame after the provider list was sorted A→Z.
  expect(output).toContain('Anthropic')
  expect(output).toContain('Azure OpenAI')
  expect(output).toContain('DeepSeek')
  expect(output).toContain('Google Gemini')
})
