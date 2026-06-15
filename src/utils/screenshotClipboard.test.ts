import { afterEach, expect, test } from 'bun:test'
import { existsSync, mkdtempSync, statSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { basename, dirname, join } from 'node:path'
import { writeScreenshotTempPng } from './screenshotClipboard'

const tempRoots: string[] = []

function makeTempRoot(): string {
  const tempRoot = mkdtempSync(join(tmpdir(), 'openclaude-screenshot-test-'))
  tempRoots.push(tempRoot)
  return tempRoot
}

afterEach(() => {
  for (const tempRoot of tempRoots.splice(0)) {
    rmSync(tempRoot, { recursive: true, force: true })
  }
})

test('writeScreenshotTempPng creates a private unique temp directory and cleanup handle', async () => {
  const tempRoot = makeTempRoot()

  const first = await writeScreenshotTempPng(Buffer.from([0x89, 0x50]), tempRoot)
  const second = await writeScreenshotTempPng(Buffer.from([0x89, 0x51]), tempRoot)

  expect(dirname(first.pngPath)).toBe(first.tempDir)
  expect(dirname(second.pngPath)).toBe(second.tempDir)
  expect(first.tempDir).not.toBe(second.tempDir)
  expect(basename(first.tempDir).startsWith('claude-code-screenshot-')).toBe(true)
  expect(basename(first.pngPath)).toBe('screenshot.png')
  expect(existsSync(first.pngPath)).toBe(true)

  if (process.platform !== 'win32') {
    expect(statSync(first.pngPath).mode & 0o077).toBe(0)
  }

  await first.dispose()
  expect(existsSync(first.tempDir)).toBe(false)

  await second.dispose()
})
