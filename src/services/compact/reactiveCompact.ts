import type { Message, StreamEvent } from '../../types/message.js'
import type { CacheSafeParams } from '../../utils/forkedAgent.js'
import type { QuerySource } from '../../constants/querySource.js'
import type { CompactionResult } from './compact.js'

export type ReactiveCompactResult = {
  compacted: boolean
  [key: string]: unknown
}

export type ReactiveCompactParams = {
  hasAttempted: boolean
  querySource: QuerySource
  aborted: boolean
  messages: Message[]
  cacheSafeParams: CacheSafeParams
}

export type ReactiveCompactOnPromptTooLongResult =
  | {
      ok: true
      result: CompactionResult
    }
  | {
      ok: false
      reason:
        | 'too_few_groups'
        | 'aborted'
        | 'exhausted'
        | 'error'
        | 'media_unstrippable'
    }

export type ReactiveCompactManualOptions = {
  customInstructions?: string
  trigger: 'manual'
}

export function isReactiveCompactEnabled(): boolean {
  return false
}

export function isReactiveOnlyMode(): boolean {
  return false
}

export async function runReactiveCompact(): Promise<ReactiveCompactResult> {
  return { compacted: false }
}

export function isWithheldPromptTooLong(_message: Message | StreamEvent): boolean {
  return false
}

export function isWithheldMediaSizeError(_message: Message | StreamEvent): boolean {
  return false
}

export async function tryReactiveCompact(
  _params: ReactiveCompactParams,
): Promise<CompactionResult | null> {
  return null
}

export async function reactiveCompactOnPromptTooLong(
  _messages: Message[],
  _cacheSafeParams: CacheSafeParams,
  _options: ReactiveCompactManualOptions,
): Promise<ReactiveCompactOnPromptTooLongResult> {
  return { ok: false, reason: 'error' }
}
