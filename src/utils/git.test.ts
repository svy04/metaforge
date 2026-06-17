import { afterEach, describe, expect, test } from 'bun:test'
import { execFile } from 'node:child_process'
import { mkdtemp, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'
import { promisify } from 'node:util'
import { execFileNoThrowWithCwd } from './execFileNoThrow.js'

const tempDirs: string[] = []
const execFileAsync = promisify(execFile)

afterEach(async () => {
  await Promise.all(
    tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })),
  )
})

describe('git issue state preservation', () => {
  test('captures untracked text files through the issue preserve path', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'openclaude-git-state-'))
    tempDirs.push(dir)

    const init = await execFileNoThrowWithCwd('git', ['init'], {
      cwd: dir,
      preserveOutputOnError: false,
    })
    expect(init.code).toBe(0)

    await writeFile(join(dir, 'note.txt'), 'hello from an untracked file', 'utf8')

    const gitModuleUrl = pathToFileURL(join(import.meta.dir, 'git.ts')).href
    const script = `
      const { preserveGitStateForIssue } = await import(${JSON.stringify(gitModuleUrl)});
      const state = await preserveGitStateForIssue();
      console.log(JSON.stringify(state?.untracked_files ?? null));
    `
    const { stdout } = await execFileAsync(process.execPath, ['-e', script], {
      cwd: dir,
      encoding: 'utf8',
    })

    expect(JSON.parse(stdout.trim())).toEqual([
      {
        path: 'note.txt',
        content: 'hello from an untracked file',
      },
    ])
  })
})
