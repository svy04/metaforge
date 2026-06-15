import { afterEach, expect, test } from 'bun:test'
import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  writeFile,
} from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { createZipFromDirectory, extractZipToDirectory } from './zipCache'

const tempDirs: string[] = []

async function makeTempDir(): Promise<string> {
  const dir = await mkdtemp(join(tmpdir(), 'openclaude-zip-cache-'))
  tempDirs.push(dir)
  return dir
}

afterEach(async () => {
  await Promise.all(
    tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })),
  )
})

test('extractZipToDirectory refuses to overwrite an existing extracted file', async () => {
  const root = await makeTempDir()
  const sourceDir = join(root, 'source')
  const targetDir = join(root, 'target')
  const fileName = 'plugin.txt'
  const targetFile = join(targetDir, fileName)

  await mkdir(sourceDir)
  await mkdir(targetDir)
  await writeFile(join(sourceDir, fileName), 'from zip', 'utf8')
  await writeFile(targetFile, 'existing', 'utf8')

  const zipPath = join(root, 'plugin.zip')
  const zipData = await createZipFromDirectory(sourceDir)
  await writeFile(zipPath, zipData)

  await expect(extractZipToDirectory(zipPath, targetDir)).rejects.toThrow()
  await expect(readFile(targetFile, 'utf8')).resolves.toBe('existing')
})
