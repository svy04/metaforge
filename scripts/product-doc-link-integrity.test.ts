import { describe, expect, test } from 'bun:test'
import { spawnSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const root = join(__dirname, '..')

describe('product doc link integrity report', () => {
  test('writes public-safe resolved paths without local user directories', () => {
    const result = spawnSync('bun', ['run', 'product:doc-link-integrity'], {
      cwd: root,
      encoding: 'utf8',
      shell: process.platform === 'win32',
    })

    expect(result.status, result.stderr || result.stdout).toBe(0)

    const reportText = readFileSync(
      join(root, 'docs/product-quality/doc-link-integrity-report.json'),
      'utf8',
    )
    expect(reportText).not.toMatch(/C:\\\\Users|C:\/Users|\/Users\//)

    const report = JSON.parse(reportText) as {
      relativeLinksChecked: Array<{ resolvedPath: string }>
    }
    expect(report.relativeLinksChecked.length).toBeGreaterThan(0)
    for (const item of report.relativeLinksChecked) {
      expect(item.resolvedPath.startsWith('<repo>')).toBe(true)
    }
  })
})
