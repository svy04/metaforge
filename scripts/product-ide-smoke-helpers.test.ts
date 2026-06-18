import { afterEach, describe, expect, test } from 'bun:test'
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import {
  buildSanitizedIdeSmokeEnv,
  scanVscodeEnvironmentBlockers,
  waitForJsonResult,
  withCliEnvironmentBlockers,
} from './product-ide-smoke-helpers'

const tempDirs: string[] = []

afterEach(() => {
  for (const dir of tempDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true })
  }
})

function makeTempDir(): string {
  const dir = mkdtempSync(join(tmpdir(), 'openclaude-ide-smoke-helpers-'))
  tempDirs.push(dir)
  return dir
}

describe('IDE smoke helpers', () => {
  test('builds a minimal VS Code smoke environment without carrying arbitrary secret-like variables', () => {
    const env = buildSanitizedIdeSmokeEnv(
      {
        OPENCLAUDE_EXTENSION_HOST_RESULT_PATH: 'result.json',
      },
      {
        PATH: 'C:/tools/bin',
        USERPROFILE: 'C:/example-profile',
        SECRET_TOKEN: 'should-not-leak',
        OPENAI_API_KEY: 'should-not-leak',
      },
    )

    expect(env.PATH).toBe('C:/tools/bin')
    expect(env.Path).toBe('C:/tools/bin')
    expect(env.USERPROFILE).toBe('C:/example-profile')
    expect(env.OPENCLAUDE_EXTENSION_HOST_RESULT_PATH).toBe('result.json')
    expect(env.SECRET_TOKEN).toBeUndefined()
    expect(env.OPENAI_API_KEY).toBeUndefined()
  })

  test('recursively classifies VS Code update blockers from local log files', () => {
    const root = makeTempDir()
    const nested = join(root, 'window1', 'renderer')
    mkdirSync(nested, { recursive: true })
    writeFileSync(join(nested, 'main.log'), 'Code is currently being updated\n')

    expect(scanVscodeEnvironmentBlockers(root)).toEqual(['vscode_update_in_progress'])
  })

  test('adds a CLI unavailable blocker when VS Code cannot be invoked', () => {
    const result = { error: { message: 'Executable not found in PATH' } }

    expect(withCliEnvironmentBlockers([], result, 'not_available')).toEqual(['vscode_cli_unavailable'])
  })

  test('keeps polling while a result file contains partial JSON', async () => {
    const root = makeTempDir()
    const resultPath = join(root, 'result.json')
    writeFileSync(resultPath, '{"ok":')

    const writer = Bun.spawn(
      [
        process.execPath,
        '--eval',
        "setTimeout(() => require('node:fs').writeFileSync(process.env.RESULT_PATH, JSON.stringify({ ok: true })), 100)",
      ],
      {
        env: {
          ...process.env,
          RESULT_PATH: resultPath,
        },
      },
    )

    const result = waitForJsonResult<{ ok: boolean }>(resultPath, 2000, 25)
    await writer.exited

    expect(result).toEqual({ ok: true })
  })
})
