import { afterEach, describe, expect, test } from 'bun:test'
import { existsSync, readFileSync, rmSync } from 'fs'
import { join } from 'path'
import { tmpdir } from 'os'

import { persistProjectMemoryCandidates } from './memory.js'

const tempRoot = join(tmpdir(), `openclaude-orchestra-memory-${process.pid}`)

afterEach(() => {
  rmSync(tempRoot, { recursive: true, force: true })
})

describe('orchestra project memory capture', () => {
  test('writes project-scoped candidates and deduplicates normalized entries', async () => {
    const memoryPath = join(tempRoot, 'CLAUDE.md')

    const first = await persistProjectMemoryCandidates({
      memoryPath,
      candidates: [
        'Keep Codex as the only writer.',
        'Keep Codex as the only writer. ',
        'Persist only project orchestration rules.',
      ],
    })
    const second = await persistProjectMemoryCandidates({
      memoryPath,
      candidates: [
        'keep codex as the only writer.',
        'Use Opus only for planning and critique.',
      ],
    })

    expect(first.written).toEqual([
      'Keep Codex as the only writer.',
      'Persist only project orchestration rules.',
    ])
    expect(second.written).toEqual(['Use Opus only for planning and critique.'])
    expect(existsSync(memoryPath)).toBe(true)

    const content = readFileSync(memoryPath, 'utf8')
    expect(content).toContain('## OpenClaude Orchestrator Memory')
    expect(content.match(/Keep Codex as the only writer\./g)?.length).toBe(1)
    expect(content.match(/Use Opus only for planning and critique\./g)?.length).toBe(1)
  })

  test('does not write when memory scope is not project', async () => {
    const memoryPath = join(tempRoot, 'CLAUDE.md')

    const result = await persistProjectMemoryCandidates({
      memoryPath,
      memoryScope: 'user',
      candidates: ['Do not write global memory automatically.'],
    })

    expect(result.written).toEqual([])
    expect(existsSync(memoryPath)).toBe(false)
  })
})
