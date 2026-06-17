import { afterEach, describe, expect, test } from 'bun:test'
import { mkdtemp, open, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { parseJSONL, readJSONLFile } from './json'

const tempDirs: string[] = []
const TEST_MAX_JSONL_READ_BYTES = 100 * 1024 * 1024

afterEach(async () => {
  await Promise.all(tempDirs.splice(0).map(dir => rm(dir, { recursive: true, force: true })))
})

describe('JSONL utilities', () => {
  test('parseJSONL skips malformed and empty lines', () => {
    const rows = parseJSONL<{ id: number }>(
      [
        '{"id":1}',
        '',
        'not-json',
        '{"id":2}',
      ].join('\n'),
    )

    expect(rows).toEqual([{ id: 1 }, { id: 2 }])
  })

  test('readJSONLFile reads through one file handle and skips malformed lines', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'openclaude-jsonl-'))
    tempDirs.push(dir)
    const filePath = join(dir, 'events.jsonl')
    await writeFile(
      filePath,
      [
        '{"kind":"ok","value":1}',
        'malformed',
        '{"kind":"ok","value":2}',
        '',
      ].join('\n'),
      'utf8',
    )

    const rows = await readJSONLFile<{ kind: string; value: number }>(filePath)

    expect(rows).toEqual([
      { kind: 'ok', value: 1 },
      { kind: 'ok', value: 2 },
    ])
  })

  test('readJSONLFile reads only the tail of large files and skips the first partial line', async () => {
    const dir = await mkdtemp(join(tmpdir(), 'openclaude-jsonl-tail-'))
    tempDirs.push(dir)
    const filePath = join(dir, 'large-events.jsonl')
    const tail = [
      'partial-prefix-without-json-ending',
      '{"kind":"tail","value":1}',
      'malformed',
      '{"kind":"tail","value":2}',
      '',
    ].join('\n')
    const tailBytes = Buffer.from(tail)

    const fd = await open(filePath, 'w')
    try {
      await fd.truncate(TEST_MAX_JSONL_READ_BYTES + tailBytes.length)
      await fd.write(tailBytes, 0, tailBytes.length, TEST_MAX_JSONL_READ_BYTES)
    } finally {
      await fd.close()
    }

    const rows = await readJSONLFile<{ kind: string; value: number }>(filePath)

    expect(rows).toEqual([
      { kind: 'tail', value: 1 },
      { kind: 'tail', value: 2 },
    ])
  })
})
