import { expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { pathToFileURL } from 'node:url'

test('debug skill tails from the same opened file it stats', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'openclaude-debug-race-'))
  const testPath = join(tempDir, 'debug-race.test.ts')
  const debugModuleUrl = pathToFileURL(
    join(process.cwd(), 'src/skills/bundled/debug.ts'),
  ).href
  const bundledSkillsModuleUrl = pathToFileURL(
    join(process.cwd(), 'src/skills/bundledSkills.ts'),
  ).href

  try {
    writeFileSync(
      testPath,
      `
        import { expect, mock, test } from 'bun:test'

        test('isolated debug log race regression', async () => {
          const realFsPromises = await import('node:fs/promises')
          const debugLogPath = 'mock-debug.log'
          const logText = 'first captured line\\nsecond captured line\\nlast captured line'
          const logBytes = Buffer.from(logText)
          const calls = {
            close: 0,
            handleStat: 0,
            open: 0,
            pathStat: 0,
            read: 0,
          }

          mock.module('fs/promises', () => ({
            ...realFsPromises,
            appendFile: async () => {},
            mkdir: async () => {},
            open: async (path: string, flags: string) => {
              calls.open++
              expect(path).toBe(debugLogPath)
              expect(flags).toBe('r')
              return {
                close: async () => {
                  calls.close++
                },
                read: async ({ buffer, position }: { buffer: Buffer; position?: number }) => {
                  calls.read++
                  const start = position ?? 0
                  const bytesRead = logBytes.copy(buffer, 0, start)
                  return { buffer, bytesRead }
                },
                stat: async () => {
                  calls.handleStat++
                  return { size: logBytes.length }
                },
              }
            },
            stat: async (path: string) => {
              if (path === debugLogPath) {
                calls.pathStat++
                throw new Error('path stat should not be used before open')
              }
              return realFsPromises.stat(path)
            },
            symlink: async () => {},
            unlink: async () => {},
          }))

          const argvLength = process.argv.length
          process.argv.push('--debug-file', debugLogPath)
          try {
            const { clearBundledSkills, getBundledSkills } = await import(
              ${JSON.stringify(bundledSkillsModuleUrl)}
            )
            const { registerDebugSkill } = await import(
              ${JSON.stringify(debugModuleUrl)} + '?ts=' + Date.now() + '-' + Math.random()
            )

            clearBundledSkills()
            registerDebugSkill()

            const skill = getBundledSkills().find(command => command.name === 'debug')
            expect(skill).toBeDefined()
            expect(skill?.type).toBe('prompt')
            if (!skill || skill.type !== 'prompt') {
              throw new Error('debug bundled skill was not registered as a prompt command')
            }

            const blocks = await skill.getPromptForCommand('inspect the debug log', {} as never)
            const text = (blocks[0] as { text: string }).text

            expect(text).toContain('Log size:')
            expect(text).toContain('last captured line')
            expect(text).not.toContain('path stat should not be used before open')
            expect(calls.pathStat).toBe(0)
            expect(calls.open).toBe(1)
            expect(calls.handleStat).toBe(1)
            expect(calls.read).toBe(1)
            expect(calls.close).toBe(1)
          } finally {
            process.argv.length = argvLength
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
