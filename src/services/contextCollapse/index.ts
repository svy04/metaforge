// Stub — contextCollapse not included in source snapshot (feature-gated)
import type { QuerySource } from '../../constants/querySource.js'
import type { ToolUseContext } from '../../Tool.js'
import type { Message, StreamEvent } from '../../types/message.js'

export function isContextCollapseEnabled(): boolean {
  return false
}
export function getContextCollapseState() {
  return null
}

export function getStats() {
  return {
    collapsedSpans: 0,
    collapsedMessages: 0,
    stagedSpans: 0,
    health: {
      totalSpawns: 0,
      totalErrors: 0,
      lastError: null as string | null,
      emptySpawnWarningEmitted: false,
      totalEmptySpawns: 0,
    },
  }
}

export function subscribe(_listener: () => void): () => void {
  return () => {}
}

export function resetContextCollapse(): void {}

export function initContextCollapse(): void {}

export async function applyCollapsesIfNeeded(
  messages: Message[],
  _toolUseContext: ToolUseContext,
  _querySource: QuerySource,
): Promise<{ messages: Message[] }> {
  return { messages }
}

export function isWithheldPromptTooLong(
  _message: Message | StreamEvent,
  _isPromptTooLongMessage: (message: Message | StreamEvent | undefined) => boolean,
  _querySource: QuerySource,
): boolean {
  return false
}

export function recoverFromOverflow(
  messages: Message[],
  _querySource: QuerySource,
): { committed: number; messages: Message[] } {
  return { committed: 0, messages }
}
