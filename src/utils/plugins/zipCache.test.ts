import { afterEach, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import {
  mkdir,
  mkdtemp,
  readFile,
  rm,
  writeFile,
} from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
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

test('createZipFromDirectory reads file contents from the same opened file it stats', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaude-zip-cache-race-'))
  const testPath = join(tempDir, 'zip-cache-race.test.ts')
  const zipCacheModuleUrl = pathToFileURL(
    join(process.cwd(), 'src/utils/plugins/zipCache.ts'),
  ).href
  const fflateModuleUrl = pathToFileURL(
    join(process.cwd(), 'node_modules/fflate/esm/index.mjs'),
  ).href

  try {
    writeFileSync(
      testPath,
      `
        import { expect, mock, test } from 'bun:test'
        import { join } from 'node:path'

        test('isolated ZIP cache race regression', async () => {
          const realFsPromises = await import('node:fs/promises')
          const sourceDir = join('virtual-plugin-root', 'source')
          const filePath = join(sourceDir, 'plugin.txt')
          const originalText = 'original plugin payload'
          const replacementText = 'replacement payload from path read'
          const calls = {
            close: 0,
            handleReadFile: 0,
            handleStat: 0,
            open: 0,
            pathReadFile: 0,
          }
          const fileDirent = {
            name: 'plugin.txt',
            isDirectory: () => false,
            isFile: () => true,
            isSymbolicLink: () => false,
          }
          const fileStat = {
            isFile: () => true,
            mode: 0o100755,
          }

          mock.module('fs/promises', () => ({
            ...realFsPromises,
            open: async (path: string, flags: string) => {
              if (path !== filePath) return realFsPromises.open(path, flags)
              calls.open++
              expect(flags).toBe('r')
              return {
                close: async () => {
                  calls.close++
                },
                readFile: async () => {
                  calls.handleReadFile++
                  return Buffer.from(originalText)
                },
                stat: async () => {
                  calls.handleStat++
                  return fileStat
                },
              }
            },
            readFile: async (path: string) => {
              if (path === filePath) {
                calls.pathReadFile++
                return Buffer.from(replacementText)
              }
              return realFsPromises.readFile(path)
            },
            readdir: async (path: string, options?: object) => {
              if (path === sourceDir) {
                expect(options).toEqual({ withFileTypes: true })
                return [fileDirent]
              }
              return realFsPromises.readdir(path, options)
            },
            stat: async (path: string, options?: object) => {
              if (path === sourceDir) return { dev: 1n, ino: 2n }
              if (path === filePath) return fileStat
              return realFsPromises.stat(path, options)
            },
          }))

          try {
            const { createZipFromDirectory } = await import(
              ${JSON.stringify(zipCacheModuleUrl)} + '?ts=' + Date.now() + '-' + Math.random()
            )
            const { unzipSync } = await import(${JSON.stringify(fflateModuleUrl)})
            const zipData = await createZipFromDirectory(sourceDir)
            const unzipped = unzipSync(zipData)

            expect(Buffer.from(unzipped['plugin.txt']).toString('utf8')).toBe(originalText)
            expect(calls.pathReadFile).toBe(0)
            expect(calls.open).toBe(1)
            expect(calls.handleStat).toBe(1)
            expect(calls.handleReadFile).toBe(1)
            expect(calls.close).toBe(1)
          } finally {
            mock.restore()
          }
        })
      `,
    )

    const result = spawnSync(process.execPath, ['test', testPath], {
      cwd: process.cwd(),
      encoding: 'utf8',
    })

    if (result.status !== 0) {
      expect(`${result.stdout}\n${result.stderr}`).toBe('')
    }
    expect(result.status).toBe(0)
  } finally {
    rmSync(tempDir, { recursive: true, force: true })
  }
})
