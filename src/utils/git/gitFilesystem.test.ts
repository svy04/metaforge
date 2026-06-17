import { afterEach, describe, expect, test } from 'bun:test'
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { clearResolveGitDirCache, resolveGitDir } from './gitFilesystem.js'

const tempDirs: string[] = []

afterEach(async () => {
  clearResolveGitDirCache()
  await Promise.all(
    tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })),
  )
})

describe('resolveGitDir', () => {
  test('returns the regular .git directory', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'openclaude-git-fs-'))
    tempDirs.push(dir)
    await mkdir(join(dir, '.git'))

    await expect(resolveGitDir(dir)).resolves.toBe(join(dir, '.git'))
  })

  test('resolves a worktree .git file pointer', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'openclaude-git-worktree-'))
    tempDirs.push(dir)
    const actualGitDir = resolve(dir, 'actual.git')
    await mkdir(actualGitDir)
    await writeFile(join(dir, '.git'), 'gitdir: actual.git\n', 'utf8')

    await expect(resolveGitDir(dir)).resolves.toBe(actualGitDir)
  })
})
