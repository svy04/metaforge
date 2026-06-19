import assert from 'node:assert/strict'
import test from 'node:test'

import { formatChromeNativeHostLogLine } from './chromeNativeHost.ts'

test('formatChromeNativeHostLogLine keeps message and args on one log line', () => {
  const line = formatChromeNativeHostLogLine('socket\r\n[INFO] forged', [
    'arg\nnext',
    { reason: 'bad\rvalue' },
    new Error('boom\nagain'),
  ])

  assert.equal(line.includes('\r'), false)
  assert.equal(line.includes('\n'), false)
  assert.match(line, /^\[Claude Chrome Native Host\] socket \[INFO\] forged /)
  assert.match(line, /arg next/)
  assert.match(line, /bad value/)
  assert.match(line, /boom again/)
})
