import assert from 'node:assert/strict'
import test from 'node:test'

import { cliError } from './exit.ts'

test('cliError writes user-controlled errors as a single log line', () => {
  const originalStderrWrite = process.stderr.write
  const originalExit = process.exit
  let logged = ''
  let exitCode: string | number | null | undefined

  process.stderr.write = ((chunk: string | Uint8Array) => {
    logged += String(chunk)
    return true
  }) as typeof process.stderr.write
  process.exit = ((code?: string | number | null | undefined) => {
    exitCode = code
    return undefined as never
  }) as typeof process.exit

  try {
    cliError('invalid name\r\n[INFO] forged entry\u001b[31m')
  } finally {
    process.stderr.write = originalStderrWrite
    process.exit = originalExit
  }

  assert.equal(exitCode, 1)
  const message = logged.trimEnd()
  assert.equal(message.includes('\r'), false)
  assert.equal(message.includes('\n'), false)
  assert.equal(message.includes('\u001b'), false)
  assert.match(message, /^invalid name \[INFO\] forged entry\[31m$/)
  assert.equal(logged.endsWith('\n'), true)
})
