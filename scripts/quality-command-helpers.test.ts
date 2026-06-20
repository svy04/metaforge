import { describe, expect, test } from 'bun:test'
import { runNoProviderPackageCommand, type PackageCommandSpawn } from './quality-command-helpers'

describe('runNoProviderPackageCommand', () => {
  test('runs package commands through bun x with provider credentials disabled', () => {
    const calls: Array<{ executable: string; args: string[]; options: Record<string, unknown> }> = []
    const spawn: PackageCommandSpawn = (executable, args, options) => {
      calls.push({ executable, args, options })
      return {
        status: 0,
        stdout: 'ok marker\n',
        stderr: '',
      }
    }

    const result = runNoProviderPackageCommand({
      root: 'C:/repo',
      name: 'tool_version',
      command: ['tool', '--version'],
      requiredSubstrings: ['ok marker'],
      noProviderEnvName: 'OPENCLAUDE_TEST_NO_PROVIDER',
      normalize: (value) => String(value ?? '').trim(),
      preview: (value) => [`preview:${value}`],
      spawn,
    })

    expect(calls).toHaveLength(1)
    expect(calls[0]?.executable).toBe(process.execPath)
    expect(calls[0]?.args).toEqual(['x', 'tool', '--version'])
    expect(calls[0]?.options.cwd).toBe('C:/repo')
    expect(calls[0]?.options.shell).toBe(false)
    expect(calls[0]?.options.maxBuffer).toBe(128 * 1024 * 1024)

    const env = calls[0]?.options.env as Record<string, string>
    expect(env.CLAUDE_CODE_USE_OPENAI).toBe('0')
    expect(env.CLAUDE_CODE_USE_GEMINI).toBe('0')
    expect(env.CLAUDE_CODE_USE_GITHUB).toBe('0')
    expect(env.CLAUDE_CODE_USE_MISTRAL).toBe('0')
    expect(env.OPENAI_API_KEY).toBe('')
    expect(env.CODEX_API_KEY).toBe('')
    expect(env.GEMINI_API_KEY).toBe('')
    expect(env.GOOGLE_API_KEY).toBe('')
    expect(env.MISTRAL_API_KEY).toBe('')
    expect(env.GITHUB_TOKEN).toBe('')
    expect(env.GH_TOKEN).toBe('')
    expect(env.ANTHROPIC_API_KEY).toBe('')
    expect(env.OPENCLAUDE_TEST_NO_PROVIDER).toBe('1')

    expect(result).toEqual({
      name: 'tool_version',
      command: ['tool', '--version'],
      exitCode: 0,
      passed: true,
      requiredSubstrings: ['ok marker'],
      missingSubstrings: [],
      stdoutPreview: ['preview:ok marker'],
      stderrPreview: ['preview:'],
      stdoutText: 'ok marker',
    })
  })

  test('checks required substrings against normalized stdout and stderr before passing', () => {
    const spawn: PackageCommandSpawn = () => ({
      status: 1,
      stdout: 'stdout marker',
      stderr: 'stderr marker',
    })

    const result = runNoProviderPackageCommand({
      root: 'C:/repo',
      name: 'tool_json',
      command: ['tool', '--json'],
      requiredSubstrings: ['stdout marker', 'stderr marker', 'missing marker'],
      noProviderEnvName: 'OPENCLAUDE_TEST_NO_PROVIDER',
      normalize: (value) => String(value ?? '').replace(/\r\n/g, '\n'),
      preview: (value) => value.split('\n'),
      spawn,
    })

    expect(result.exitCode).toBe(1)
    expect(result.passed).toBe(false)
    expect(result.missingSubstrings).toEqual(['missing marker'])
    expect(result.stdoutText).toBe('stdout marker')
    expect(result.stdoutPreview).toEqual(['stdout marker'])
    expect(result.stderrPreview).toEqual(['stderr marker'])
  })
})
