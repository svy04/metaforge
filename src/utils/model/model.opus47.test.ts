import { afterEach, beforeEach, expect, test } from 'bun:test'

import { resetModelStringsForTestingOnly } from '../../bootstrap/state.js'
import {
  firstPartyNameToCanonical,
  getMarketingNameForModel,
  parseUserSpecifiedModel,
} from './model.js'
import { getPublicModelDisplayName } from './model.js'

const originalEnv = {
  ANTHROPIC_DEFAULT_OPUS_MODEL: process.env.ANTHROPIC_DEFAULT_OPUS_MODEL,
  ANTHROPIC_MODEL: process.env.ANTHROPIC_MODEL,
  CLAUDE_CODE_USE_OPENAI: process.env.CLAUDE_CODE_USE_OPENAI,
  CLAUDE_CODE_USE_GEMINI: process.env.CLAUDE_CODE_USE_GEMINI,
  CLAUDE_CODE_USE_GITHUB: process.env.CLAUDE_CODE_USE_GITHUB,
  CLAUDE_CODE_USE_BEDROCK: process.env.CLAUDE_CODE_USE_BEDROCK,
  CLAUDE_CODE_USE_VERTEX: process.env.CLAUDE_CODE_USE_VERTEX,
  CLAUDE_CODE_USE_FOUNDRY: process.env.CLAUDE_CODE_USE_FOUNDRY,
}

function clearProviderFlags(): void {
  delete process.env.CLAUDE_CODE_USE_OPENAI
  delete process.env.CLAUDE_CODE_USE_GEMINI
  delete process.env.CLAUDE_CODE_USE_GITHUB
  delete process.env.CLAUDE_CODE_USE_BEDROCK
  delete process.env.CLAUDE_CODE_USE_VERTEX
  delete process.env.CLAUDE_CODE_USE_FOUNDRY
}

function restoreEnv(name: keyof typeof originalEnv): void {
  const value = originalEnv[name]
  if (value === undefined) {
    delete process.env[name]
    return
  }
  process.env[name] = value
}

beforeEach(() => {
  clearProviderFlags()
  delete process.env.ANTHROPIC_DEFAULT_OPUS_MODEL
  delete process.env.ANTHROPIC_MODEL
  resetModelStringsForTestingOnly()
})

afterEach(() => {
  restoreEnv('ANTHROPIC_DEFAULT_OPUS_MODEL')
  restoreEnv('ANTHROPIC_MODEL')
  restoreEnv('CLAUDE_CODE_USE_OPENAI')
  restoreEnv('CLAUDE_CODE_USE_GEMINI')
  restoreEnv('CLAUDE_CODE_USE_GITHUB')
  restoreEnv('CLAUDE_CODE_USE_BEDROCK')
  restoreEnv('CLAUDE_CODE_USE_VERTEX')
  restoreEnv('CLAUDE_CODE_USE_FOUNDRY')
  resetModelStringsForTestingOnly()
})

test('first-party opus alias resolves to Opus 4.7', () => {
  expect(parseUserSpecifiedModel('opus')).toBe('claude-opus-4-7')
})

test('Opus 4.7 has canonical and display mappings', () => {
  expect(firstPartyNameToCanonical('claude-opus-4-7')).toBe('claude-opus-4-7')
  expect(getPublicModelDisplayName('claude-opus-4-7')).toBe('Opus 4.7')
  expect(getMarketingNameForModel('claude-opus-4-7')).toBe('Opus 4.7')
})
