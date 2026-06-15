import { expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

test('readFileInRange fast path reads from the same opened file it stats', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaude-read-range-race-'))
  const testPath = join(tempDir, 'readFileInRange-race.test.ts')
  const moduleUrl = pathToFileURL(
    join(process.cwd(), 'src/utils/readFileInRange.ts'),
  ).href

  try {
    writeFileSync(
      testPath,
      `
        import { expect, mock, test } from 'bun:test'

        test('isolated fs race regression', async () => {
          const originalText = 'original line 1\\noriginal line 2'
          const replacementText = 'replacement line 1\\nreplacement line 2'
          const calls = {
            close: 0,
            handleReadFile: 0,
            pathReadFile: 0,
          }
          const stats = {
            isDirectory: () => false,
            isFile: () => true,
            mtimeMs: 42,
            size: Buffer.byteLength(originalText),
          }

          const fsPromisesMock = {
            open: async () => ({
              stat: async () => stats,
              readFile: async () => {
                calls.handleReadFile++
                return originalText
              },
              close: async () => {
                calls.close++
              },
            }),
            readFile: async () => {
              calls.pathReadFile++
              return replacementText
            },
            stat: async () => stats,
          }
          mock.module('fs/promises', () => fsPromisesMock)

          const { readFileInRange } = await import(
            ${JSON.stringify(moduleUrl)} + '?ts=' + Date.now() + '-' + Math.random()
          )

          const result = await readFileInRange('race.txt', 0, 2)
          expect(result.content).toBe(originalText)
          expect(calls.pathReadFile).toBe(0)
          expect(calls.handleReadFile).toBe(1)
          expect(calls.close).toBe(1)
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
