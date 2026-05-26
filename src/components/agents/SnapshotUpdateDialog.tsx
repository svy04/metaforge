// Stub
import React from 'react'
import type { AgentMemoryScope } from '../../tools/AgentTool/agentMemory.js'

type SnapshotUpdateDialogProps = {
  agentType: string
  scope: AgentMemoryScope
  snapshotTimestamp: string
  onComplete: (result: 'merge' | 'keep' | 'replace') => void
  onCancel: () => void
}

export function SnapshotUpdateDialog(_props: SnapshotUpdateDialogProps) { return null }

export function buildMergePrompt(agentType: string, scope: string): string {
  return `Merge pending memory snapshot for ${agentType} (${scope}).`
}
