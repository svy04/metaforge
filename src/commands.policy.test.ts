import { afterEach, describe, expect, test } from 'bun:test'

import {
  BRIDGE_SAFE_COMMANDS,
  isBridgeSafeCommand,
  meetsAvailabilityRequirement,
} from './commands'
import type { Command } from './types/command'

const envKeys = [
  'ANTHROPIC_API_KEY',
  'ANTHROPIC_AUTH_TOKEN',
  'ANTHROPIC_BASE_URL',
  'ANTHROPIC_UNIX_SOCKET',
  'CLAUDE_CODE_API_KEY_FILE_DESCRIPTOR',
  'CLAUDE_CODE_ENTRYPOINT',
  'CLAUDE_CODE_OAUTH_TOKEN',
  'CLAUDE_CODE_REMOTE',
  'CLAUDE_CODE_USE_BEDROCK',
  'CLAUDE_CODE_USE_FOUNDRY',
  'CLAUDE_CODE_USE_GEMINI',
  'CLAUDE_CODE_USE_GITHUB',
  'CLAUDE_CODE_USE_MISTRAL',
  'CLAUDE_CODE_USE_OPENAI',
  'CLAUDE_CODE_USE_VERTEX',
] as const
const originalEnv = new Map<string, string | undefined>(
  envKeys.map((key) => [key, process.env[key]]),
)

function resetCommandPolicyEnv(): void {
  for (const key of envKeys) {
    const originalValue = originalEnv.get(key)
    if (originalValue === undefined) {
      delete process.env[key]
    } else {
      process.env[key] = originalValue
    }
  }
}

function forceNonSubscriber(): void {
  process.env.ANTHROPIC_API_KEY = 'test-only-anthropic-key'
  delete process.env.ANTHROPIC_AUTH_TOKEN
  delete process.env.ANTHROPIC_UNIX_SOCKET
  delete process.env.CLAUDE_CODE_API_KEY_FILE_DESCRIPTOR
  delete process.env.CLAUDE_CODE_ENTRYPOINT
  delete process.env.CLAUDE_CODE_OAUTH_TOKEN
  delete process.env.CLAUDE_CODE_REMOTE
}

function clearThirdPartyProviderEnv(): void {
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_MISTRAL
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_VERTEX
}

afterEach(() => {
  resetCommandPolicyEnv()
})

function promptCommand(name: string, availability?: Command['availability']): Command {
  return {
    type: 'prompt',
    name,
    description: name,
    contentLength: 0,
    progressMessage: name,
    source: 'builtin',
    availability,
    getPromptForCommand: async () => [],
  }
}

function localCommand(name: string, availability?: Command['availability']): Command {
  return {
    type: 'local',
    name,
    description: name,
    availability,
    supportsNonInteractive: true,
    load: async () => ({
      call: async () => ({ type: 'text', value: '' }),
    }),
  }
}

function localJsxCommand(name: string): Command {
  return {
    type: 'local-jsx',
    name,
    description: name,
    load: async () => ({
      call: async () => null,
    }),
  }
}

describe('command policy gates', () => {
  test('treats commands without availability as universal', () => {
    forceNonSubscriber()
    process.env.CLAUDE_CODE_USE_OPENAI = '1'

    expect(meetsAvailabilityRequirement(promptCommand('universal'))).toBe(true)
  })

  test('rejects claude-ai and console commands outside matching auth environments', () => {
    forceNonSubscriber()
    process.env.CLAUDE_CODE_USE_OPENAI = '1'

    expect(meetsAvailabilityRequirement(promptCommand('subscriber-only', ['claude-ai']))).toBe(false)
    expect(meetsAvailabilityRequirement(promptCommand('console-only', ['console']))).toBe(false)
  })

  test('allows first-party console command environments', () => {
    forceNonSubscriber()
    clearThirdPartyProviderEnv()
    delete process.env.ANTHROPIC_BASE_URL

    expect(meetsAvailabilityRequirement(promptCommand('console-only', ['console']))).toBe(true)
  })

  test('keeps bridge-safe slash commands explicit', () => {
    const arbitraryLocal = localCommand('arbitrary-local')
    const arbitraryPrompt = promptCommand('skill-prompt')
    const arbitraryLocalJsx = localJsxCommand('local-picker')

    expect(isBridgeSafeCommand(arbitraryPrompt)).toBe(true)
    expect(isBridgeSafeCommand(arbitraryLocal)).toBe(false)
    expect(isBridgeSafeCommand(arbitraryLocalJsx)).toBe(false)
    expect([...BRIDGE_SAFE_COMMANDS].every((command) => isBridgeSafeCommand(command))).toBe(true)
  })
})
