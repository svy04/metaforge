import { afterEach, describe, expect, test } from 'bun:test'
import { execFile } from 'node:child_process'
import { existsSync } from 'node:fs'
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { promisify } from 'node:util'

const execFileAsync = promisify(execFile)
const tempDirs: string[] = []
const MODEL_CACHE_MODULE_URL = pathToFileURL(join(import.meta.dir, 'modelCache.ts')).href
const PROVIDER_ENV_KEYS = [
  'CLAUDE_CODE_USE_OPENAI',
  'CLAUDE_CODE_USE_GITHUB',
  'CLAUDE_CODE_USE_GEMINI',
  'CLAUDE_CODE_USE_MISTRAL',
  'CLAUDE_CODE_USE_BEDROCK',
  'CLAUDE_CODE_USE_VERTEX',
  'CLAUDE_CODE_USE_FOUNDRY',
  'NVIDIA_NIM',
  'MINIMAX_API_KEY',
  'OPENAI_MODEL',
  'OPENAI_BASE_URL',
  'OPENAI_API_BASE',
] as const

type ProviderMode = 'openai' | 'firstParty'

function childEnv(tempHomeDir: string, mode: ProviderMode): NodeJS.ProcessEnv {
  const env: NodeJS.ProcessEnv = {
    ...process.env,
    HOME: tempHomeDir,
    USERPROFILE: tempHomeDir,
  }
  for (const key of PROVIDER_ENV_KEYS) {
    delete env[key]
  }
  if (mode === 'openai') {
    env.CLAUDE_CODE_USE_OPENAI = '1'
  }
  return env
}

async function runModelCacheScript<T>(
  tempHomeDir: string,
  body: string,
  mode: ProviderMode = 'openai',
): Promise<T> {
  const script = `
    const mod = await import(${JSON.stringify(MODEL_CACHE_MODULE_URL)});
    ${body}
  `
  const { stdout } = await execFileAsync(process.execPath, ['-e', script], {
    cwd: join(import.meta.dir, '..', '..', '..'),
    encoding: 'utf8',
    env: childEnv(tempHomeDir, mode),
  })

  return JSON.parse(stdout.trim()) as T
}

async function makeTempHome(): Promise<string> {
  const dir = await mkdtemp(join(tmpdir(), 'openclaude-model-cache-'))
  tempDirs.push(dir)
  return dir
}

afterEach(async () => {
  await Promise.all(
    tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })),
  )
})

describe('modelCache', () => {
  const mockModel = {
    value: 'gpt-test',
    label: 'GPT Test',
    description: 'Test model',
  }

  test('missing caches are invalid without creating the cache directory', async () => {
    const tempHomeDir = await makeTempHome()

    const result = await runModelCacheScript<{ valid: boolean }>(
      tempHomeDir,
      `
        const valid = await mod.isModelCacheValid('openai');
        console.log(JSON.stringify({ valid }));
      `,
    )

    expect(result.valid).toBe(false)
    expect(existsSync(join(tempHomeDir, '.openclaude-model-cache'))).toBe(false)
  })

  test('saveModelsToCache creates the directory and cached models read back', async () => {
    const tempHomeDir = await makeTempHome()

    const result = await runModelCacheScript<{
      valid: boolean
      models: unknown
      info: { provider: string } | null
    }>(
      tempHomeDir,
      `
        const models = ${JSON.stringify([mockModel])};
        await mod.saveModelsToCache(models);
        const valid = await mod.isModelCacheValid('openai');
        const cached = await mod.getCachedModelsFromDisk();
        const info = await mod.getModelCacheInfo();
        console.log(JSON.stringify({ valid, models: cached, info }));
      `,
    )

    expect(result.valid).toBe(true)
    expect(result.models).toEqual([mockModel])
    expect(result.info).toMatchObject({ provider: 'openai' })

    const cachePath = join(tempHomeDir, '.openclaude-model-cache', 'openai.json')
    const cache = JSON.parse(await readFile(cachePath, 'utf8'))
    expect(cache.models).toEqual([mockModel])
  })

  test('stale cache files are rejected by disk reads', async () => {
    const tempHomeDir = await makeTempHome()
    const cacheDir = join(tempHomeDir, '.openclaude-model-cache')
    await mkdir(cacheDir, { recursive: true })
    await writeFile(
      join(cacheDir, 'openai.json'),
      JSON.stringify({
        version: '1',
        timestamp: Date.now() - 25 * 60 * 60 * 1000,
        provider: 'openai',
        models: [mockModel],
      }),
      'utf8',
    )

    const result = await runModelCacheScript<{
      valid: boolean
      models: unknown
    }>(
      tempHomeDir,
      `
        const valid = await mod.isModelCacheValid('openai');
        const models = await mod.getCachedModelsFromDisk();
        console.log(JSON.stringify({ valid, models }));
      `,
    )

    expect(result.valid).toBe(false)
    expect(result.models).toBeNull()
  })

  test('providers without cache support still return null from disk reads', async () => {
    const tempHomeDir = await makeTempHome()

    const result = await runModelCacheScript<{ models: unknown }>(
      tempHomeDir,
      `
        const models = await mod.getCachedModelsFromDisk();
        console.log(JSON.stringify({ models }));
      `,
      'firstParty',
    )

    expect(result.models).toBeNull()
  })
})
