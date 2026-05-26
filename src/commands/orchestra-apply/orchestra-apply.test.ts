import { execFileSync } from 'node:child_process'
import {
  mkdtempSync,
  readFileSync,
  rmSync,
  writeFileSync,
} from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'

import { afterEach, describe, expect, test } from 'bun:test'

import { writeLatestShadowReview } from '../../services/orchestra/promotionStore.js'
import type { ShadowCandidate } from '../../services/orchestra/shadowExecutor.js'
import { runWithCwdOverride } from '../../utils/cwd.js'
import { call as applyCall } from './orchestra-apply.js'
import { call as rejectCall } from './orchestra-reject.js'

const roots: string[] = []

function makeRepo(): string {
  const root = mkdtempSync(join(tmpdir(), 'openclaude-orchestra-command-'))
  roots.push(root)
  writeFileSync(join(root, 'math.ts'), 'export const value = 1\n', 'utf8')
  execFileSync('git', ['init'], { cwd: root })
  execFileSync('git', ['config', 'user.email', 'openclaude@example.local'], {
    cwd: root,
  })
  execFileSync('git', ['config', 'user.name', 'OpenClaude Test'], { cwd: root })
  execFileSync('git', ['add', 'math.ts'], { cwd: root })
  execFileSync('git', ['commit', '-m', 'initial'], { cwd: root })
  return root
}

async function seedLatest(root: string): Promise<void> {
  const worktree = join(root, '.openclaude-shadows', 't-1', 'gpt-a')
  execFileSync('git', ['worktree', 'add', '-b', 'shadow/gpt-a', worktree], {
    cwd: root,
  })
  writeFileSync(join(worktree, 'math.ts'), 'export const value = 2\n', 'utf8')
  const candidate: ShadowCandidate = {
    label: 'gpt-a',
    worktreePath: worktree,
    status: 'completed',
    filesChanged: ['math.ts'],
    diff: 'diff --git a/math.ts b/math.ts\n',
  }
  await writeLatestShadowReview(root, {
    taskScope: { intent: 'change value' },
    candidates: [candidate],
    matrix: { candidates: [candidate], verdicts: [], generatedAt: 'now' },
    evidenceMatrix: {
      verdicts: [
        {
          candidateLabel: 'gpt-a',
          evidence: {} as never,
          recommendation: 'green',
          rationale: 'ok',
        },
      ],
      topRecommended: 'gpt-a',
      generatedAt: 'now',
    },
  })
}

afterEach(() => {
  for (const root of roots.splice(0)) {
    rmSync(root, { recursive: true, force: true })
  }
})

describe('/orchestra-apply and /orchestra-reject', () => {
  test('applies the selected latest candidate from the current git repo', async () => {
    const root = makeRepo()
    await seedLatest(root)

    const result = await runWithCwdOverride(root, () =>
      applyCall('gpt-a', {} as never),
    )

    expect(result.type).toBe('text')
    if (result.type === 'text') {
      expect(result.value).toContain('Applied gpt-a')
      expect(result.value).toContain('math.ts')
    }
    expect(readFileSync(join(root, 'math.ts'), 'utf8')).toBe(
      'export const value = 2\n',
    )
  })

  test('reject clears the latest candidate pointer', async () => {
    const root = makeRepo()
    await seedLatest(root)

    const result = await runWithCwdOverride(root, () =>
      rejectCall('', {} as never),
    )

    expect(result.type).toBe('text')
    if (result.type === 'text') {
      expect(result.value).toContain('Rejected latest shadow review')
    }
  })
})

