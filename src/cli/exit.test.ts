import assert from 'node:assert/strict'
import test from 'node:test'

import { cliError } from './exit.ts'

test('cliError writes user-controlled errors as a single log line', () => {
  const originalConsoleError = console.error
  const originalExit = process.exit
  const logged: unknown[][] = []
  let exitCode: string | number | null | undefined

  console.error = (...args: unknown[]) => {
    logged.push(args)
  }
  process.exit = ((code?: string | number | null | undefined) => {
    exitCode = code
    return undefined as never
  }) as typeof process.exit

  try {
    cliError('invalid name\r\n[INFO] forged entry\u001b[31m')
  } finally {
    console.error = originalConsoleError
    process.exit = originalExit
  }

  assert.equal(exitCode, 1)
  assert.equal(logged.length, 1)
  assert.equal(logged[0]?.length, 1)
  const message = String(logged[0]?.[0])
  assert.equal(message.includes('\r'), false)
  assert.equal(message.includes('\n'), false)
  assert.equal(message.includes('\u001b'), false)
  assert.match(message, /^invalid name \[INFO\] forged entry\[31m$/)
})
