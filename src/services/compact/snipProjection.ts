import type { Message } from '../../types/message.js'

export function isSnipBoundaryMessage(message: Message): boolean {
  return message.type === 'system' && message.subtype === 'snip_boundary'
}

export function projectSnippedView<T extends Message>(messages: T[]): T[] {
  return messages
}

