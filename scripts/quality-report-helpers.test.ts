import { describe, expect, test } from 'bun:test'
import { mkdtempSync, rmSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { tmpdir } from 'node:os'

import { check, fileSha256, includesAll, readText, sha256 } from './quality-report-helpers'

describe('quality report helpers', () => {
  test('builds the shared check shape used by product reports', () => {
    expect(check('public surface is bounded', true, 'local check only')).toEqual({
      label: 'public surface is bounded',
      ok: true,
      detail: 'local check only',
    })
  })

  test('hashes text and files deterministically without exposing absolute paths', () => {
    const dir = mkdtempSync(join(tmpdir(), 'openclaude-quality-report-helpers-'))
    try {
      writeFileSync(join(dir, 'signal.txt'), 'Meta + MFH + Orchestra OS\n')

      expect(sha256('hello')).toBe('2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824')
      expect(readText('signal.txt', dir)).toBe('Meta + MFH + Orchestra OS\n')
      expect(fileSha256('signal.txt', dir)).toBe(sha256('Meta + MFH + Orchestra OS\n'))
    } finally {
      rmSync(dir, { recursive: true, force: true })
    }
  })

  test('finds required terms case-insensitively and preserves requested labels', () => {
    expect(includesAll('Metaforge keeps OpenClaude as the runtime substrate.', [
      'metaforge',
      'OpenClaude',
      'MFH',
    ])).toEqual(['metaforge', 'OpenClaude'])
  })
})
