import { describe, expect, test } from 'bun:test'

const heapBootstrapPath = '../../bin/' + 'nodeHeapBootstrap.mjs'
const {
  buildHeapBootstrapArgs,
  resolveHeapSizeMb,
  shouldBootstrapHeap,
} = await import(heapBootstrapPath)

describe('OpenClaude Node heap bootstrap', () => {
  test('bootstraps when OpenClaude starts without an explicit Node heap limit', () => {
    expect(
      shouldBootstrapHeap({
        execArgv: [],
        env: {},
      }),
    ).toBe(true)
  })

  test('does not bootstrap when the user already configured max-old-space-size', () => {
    expect(
      shouldBootstrapHeap({
        execArgv: ['--max-old-space-size=12288'],
        env: {},
      }),
    ).toBe(false)

    expect(
      shouldBootstrapHeap({
        execArgv: [],
        env: { NODE_OPTIONS: '--max-old-space-size=12288' },
      }),
    ).toBe(false)
  })

  test('uses 8192 MB by default and allows an env override', () => {
    expect(resolveHeapSizeMb({})).toBe(8192)
    expect(
      resolveHeapSizeMb({
        OPENCLAUDE_NODE_MAX_OLD_SPACE_SIZE_MB: '12288',
      }),
    ).toBe(12288)
  })

  test('builds a re-exec argv that preserves existing Node flags and CLI args', () => {
    expect(
      buildHeapBootstrapArgs({
        execArgv: ['--trace-warnings'],
        argv: ['node', 'openclaude', '--permission-mode', 'bypassPermissions'],
        scriptPath: 'C:/repo/bin/openclaude',
        heapSizeMb: 8192,
        env: {},
      }),
    ).toEqual([
      '--max-old-space-size=8192',
      '--trace-warnings',
      'C:/repo/bin/openclaude',
      '--permission-mode',
      'bypassPermissions',
    ])
  })
})
