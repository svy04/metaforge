import type {
  AssistantMessage,
  NormalizedUserMessage,
} from './message.js'

export type ShellProgress = {
  type?: string
  output: string
  fullOutput?: string
  elapsedTimeSeconds: number
  totalLines?: number
  totalBytes?: number
  timeoutMs?: number
  taskId?: string
  [key: string]: any
}

export type BashProgress = ShellProgress
export type PowerShellProgress = ShellProgress

export type AgentToolProgress = {
  type?: string
  message: AssistantMessage | NormalizedUserMessage
  usage?: unknown
  taskId?: string
  [key: string]: any
}

export type MCPProgress = {
  type?: string
  message?: string
  elapsedTimeSeconds?: number
  toolUseId?: string
  progress?: number
  total?: number
  progressMessage?: string
  [key: string]: any
}

export type SkillToolProgress = {
  type?: string
  message?: any
  elapsedTimeSeconds?: number
  [key: string]: any
}

export type WebSearchProgress = {
  type?: string
  query?: string
  message?: string
  results?: unknown[]
  resultCount?: number
  elapsedTimeSeconds?: number
  [key: string]: any
}

export type SdkWorkflowProgress = {
  type?: string
  message?: string
  step?: string
  status?: 'running' | 'completed' | 'failed' | string
  elapsedTimeSeconds?: number
  [key: string]: any
}

export type TaskOutputProgress = {
  type?: string
  taskId?: string
  status?: 'running' | 'completed' | 'failed' | 'timeout' | string
  message?: string
  elapsedTimeSeconds?: number
  [key: string]: any
}

export type REPLToolProgress =
  | ShellProgress
  | AgentToolProgress
  | MCPProgress
  | SkillToolProgress
  | WebSearchProgress
  | TaskOutputProgress
  | SdkWorkflowProgress

export type ToolProgressData = REPLToolProgress
