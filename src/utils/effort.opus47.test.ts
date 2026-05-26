import { afterEach, beforeEach, expect, test } from 'bun:test'

import {
  getDefaultEffortForModel,
  getDisplayedEffortLevel,
  modelSupportsMaxEffort,
  resolveAppliedEffort,
} from './effort.js'

let previousEffortEnv: string | undefined
let previousUserType: string | undefined

beforeEach(() => {
  previousEffortEnv = process.env.CLAUDE_CODE_EFFORT_LEVEL
  previousUserType = process.env.USER_TYPE
  delete process.env.CLAUDE_CODE_EFFORT_LEVEL
  delete process.env.USER_TYPE
})

afterEach(() => {
  if (previousEffortEnv === undefined) {
    delete process.env.CLAUDE_CODE_EFFORT_LEVEL
  } else {
    process.env.CLAUDE_CODE_EFFORT_LEVEL = previousEffortEnv
  }

  if (previousUserType === undefined) {
    delete process.env.USER_TYPE
  } else {
    process.env.USER_TYPE = previousUserType
  }
})

test('Opus 4.7 defaults to max effort', () => {
  expect(modelSupportsMaxEffort('claude-opus-4-7')).toBe(true)
  expect(getDefaultEffortForModel('claude-opus-4-7')).toBe('max')
  expect(resolveAppliedEffort('claude-opus-4-7', undefined)).toBe('max')
  expect(getDisplayedEffortLevel('claude-opus-4-7', undefined)).toBe('max')
})
