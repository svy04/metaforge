import type { Message } from '../../types/message.js'
import type { ToolUseContext } from '../../Tool.js'
import type { Attachment } from '../../utils/attachments.js'

export function getTurnZeroSkillDiscovery(): null {
  return null
}

export type SkillDiscoveryPrefetch = Promise<Attachment[]>

export function startSkillDiscoveryPrefetch(
  _input: unknown,
  _messages: Message[],
  _toolUseContext: ToolUseContext,
): SkillDiscoveryPrefetch {
  return Promise.resolve([])
}

export async function collectSkillDiscoveryPrefetch(
  pending: SkillDiscoveryPrefetch,
): Promise<Attachment[]> {
  return pending
}
