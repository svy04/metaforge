// Stub — snipCompact not included in source snapshot
import type { Message, SystemMessage } from '../../types/message.js'

export const SNIP_NUDGE_TEXT =
  'Snip compact is unavailable in this source snapshot. Continue with standard context compaction.'

export function isSnipRuntimeEnabled(): boolean {
  return false
}

export function snipCompact() {
  return null
}

export function shouldNudgeForSnips(_messages?: Message[]): boolean {
  return false
}

export function snipCompactIfNeeded(messages: Message[]): {
  messages: Message[]
  tokensFreed: number
  boundaryMessage?: SystemMessage
} {
  return {
    messages,
    tokensFreed: 0,
  }
}
