import type { AgentColorName } from '../../../tools/AgentTool/agentColorManager.js'
import type { AgentMemoryScope } from '../../../tools/AgentTool/agentMemory.js'
import type { CustomAgentDefinition } from '../../../tools/AgentTool/loadAgentsDir.js'
import type { SettingSource } from '../../../utils/settings/constants.js'

type CreationMethod = 'generate' | 'manual'

type GeneratedAgentDraft = {
  identifier: string
  whenToUse: string
  systemPrompt: string
}

export type AgentWizardData = {
  location?: SettingSource
  method?: CreationMethod
  generationPrompt?: string
  agentType?: string
  systemPrompt?: string
  whenToUse?: string
  selectedTools?: string[]
  selectedModel?: string
  selectedColor?: AgentColorName
  selectedMemory?: AgentMemoryScope
  generatedAgent?: GeneratedAgentDraft
  finalAgent?: CustomAgentDefinition
  isGenerating?: boolean
  wasGenerated?: boolean
}
