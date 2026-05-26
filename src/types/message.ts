import type { APIError } from '@anthropic-ai/sdk'
import type {
  BetaContentBlock,
  BetaMessage,
  BetaUsage,
} from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'
import type {
  ContentBlockParam,
  ToolResultBlockParam,
} from '@anthropic-ai/sdk/resources/index.mjs'
import type { UUID } from 'crypto'
import type { Progress } from '../Tool.js'
import type { PermissionMode } from './permissions.js'

export type PartialCompactDirection = 'from' | 'up_to'
export type SystemMessageLevel = 'info' | 'warning' | 'error'
export type MessageOrigin =
  | { kind: 'human' }
  | { kind: 'local'; source?: string }
  | { kind: 'remote'; source?: string }
  | { kind: 'hook'; source?: string }
  | { kind: 'system'; source?: string }
  | { kind: 'channel'; server: string; source?: string }
  | { kind: string; source?: string }

export type CompactMetadata = {
  trigger: 'manual' | 'auto'
  preTokens: number
  userContext?: string
  messagesSummarized?: number
  preCompactDiscoveredTools?: string[]
  preservedSegment?: {
    headUuid: UUID
    anchorUuid: UUID
    tailUuid: UUID
  }
}

export type StopHookInfo = {
  command?: string
  promptText?: string
  hookName?: string
  hookEvent?: string
  toolUseID?: string
  stdout?: string
  stderr?: string
  output?: string
  exitCode?: number
  durationMs?: number
}

type MessageBase = {
  uuid: UUID
  timestamp?: string
  isMeta?: boolean
  isVirtual?: true
  isVisibleInTranscriptOnly?: true
  logicalParentUuid?: UUID
  [key: string]: any
}

export type AssistantMessage = MessageBase & {
  type: 'assistant'
  message: BetaMessage
  requestId?: string
  apiError?: APIError | 'max_output_tokens'
  error?: string
  errorDetails?: string
  isApiErrorMessage?: boolean
}

export type UserMessage = MessageBase & {
  type: 'user'
  message: {
    role: 'user'
    content: string | ContentBlockParam[]
  }
  isCompactSummary?: true
  summarizeMetadata?: {
    messagesSummarized: number
    userContext?: string
    direction?: PartialCompactDirection
  }
  toolUseResult?: unknown
  mcpMeta?: {
    _meta?: Record<string, unknown>
    structuredContent?: Record<string, unknown>
  }
  imagePasteIds?: number[]
  sourceToolAssistantUUID?: UUID
  permissionMode?: PermissionMode
  origin?: MessageOrigin
}

export type ProgressMessage<P extends Progress = Progress> = MessageBase & {
  type: 'progress'
  data: P
  toolUseID: string
  parentToolUseID: string
}

export type HookResultMessage = UserMessage

type SystemBase = MessageBase & {
  type: 'system'
  subtype: string
  content?: string
  level?: SystemMessageLevel
}

export type SystemInformationalMessage = SystemBase & {
  subtype: 'informational'
  content: string
  level: SystemMessageLevel
  toolUseID?: string
  preventContinuation?: boolean
}

export type SystemPermissionRetryMessage = SystemBase & {
  subtype: 'permission_retry'
  content: string
  commands: string[]
  level: 'info'
}

export type SystemBridgeStatusMessage = SystemBase & {
  subtype: 'bridge_status'
  content: string
  url: string
  upgradeNudge?: string
}

export type SystemScheduledTaskFireMessage = SystemBase & {
  subtype: 'scheduled_task_fire'
  content: string
}

export type SystemStopHookSummaryMessage = SystemBase & {
  subtype: 'stop_hook_summary'
  hookCount: number
  hookInfos: StopHookInfo[]
  hookErrors: string[]
  preventedContinuation: boolean
  stopReason?: string
  hasOutput: boolean
  toolUseID?: string
  hookLabel?: string
  totalDurationMs?: number
}

export type SystemTurnDurationMessage = SystemBase & {
  subtype: 'turn_duration'
  durationMs: number
  budgetTokens?: number
  budgetLimit?: number
  budgetNudges?: number
  messageCount?: number
}

export type SystemAwaySummaryMessage = SystemBase & {
  subtype: 'away_summary'
  content: string
}

export type SystemMemorySavedMessage = SystemBase & {
  subtype: 'memory_saved'
  writtenPaths: string[]
}

export type SystemAgentsKilledMessage = SystemBase & {
  subtype: 'agents_killed'
}

export type SystemApiMetricsMessage = SystemBase & {
  subtype: 'api_metrics'
  ttftMs: number
  otps: number
  isP50?: boolean
  hookDurationMs?: number
  turnDurationMs?: number
  toolDurationMs?: number
  classifierDurationMs?: number
  toolCount?: number
  hookCount?: number
  classifierCount?: number
  configWriteCount?: number
}

export type SystemLocalCommandMessage = SystemBase & {
  subtype: 'local_command'
  content: string
  level: 'info'
}

export type SystemCompactBoundaryMessage = SystemBase & {
  subtype: 'compact_boundary'
  content: string
  level: 'info'
  compactMetadata: CompactMetadata
}

export type SystemMicrocompactBoundaryMessage = SystemBase & {
  subtype: 'microcompact_boundary'
  content: string
  level: 'info'
  microcompactMetadata: {
    trigger: 'auto'
    preTokens: number
    tokensSaved: number
    compactedToolIds: string[]
    clearedAttachmentUUIDs: string[]
  }
}

export type SystemAPIErrorMessage = SystemBase & {
  subtype: 'api_error'
  level: 'error'
  cause?: Error
  error: APIError
  retryInMs: number
  retryAttempt: number
  maxRetries: number
}

export type SystemFileSnapshotMessage = SystemBase & {
  subtype: 'file_snapshot'
  files?: unknown[]
}

export type SystemThinkingMessage = SystemBase & {
  subtype: 'thinking'
  content: string
}

export type SystemMessage =
  | SystemInformationalMessage
  | SystemPermissionRetryMessage
  | SystemBridgeStatusMessage
  | SystemScheduledTaskFireMessage
  | SystemStopHookSummaryMessage
  | SystemTurnDurationMessage
  | SystemAwaySummaryMessage
  | SystemMemorySavedMessage
  | SystemAgentsKilledMessage
  | SystemApiMetricsMessage
  | SystemLocalCommandMessage
  | SystemCompactBoundaryMessage
  | SystemMicrocompactBoundaryMessage
  | SystemAPIErrorMessage
  | SystemFileSnapshotMessage
  | SystemThinkingMessage
  | SystemBase

export type AttachmentMessage = MessageBase & {
  type: 'attachment'
  attachment: any
  content?: string
}

export type GroupedToolUseMessage = MessageBase & {
  type: 'grouped_tool_use'
  messages: Message[]
  toolUseID?: string
}

export type CollapsedReadSearchGroup = MessageBase & {
  type: 'collapsed_read_search'
  messages: Message[]
  toolUseID?: string
}

export type ToolUseSummaryMessage = MessageBase & {
  type: 'tool_use_summary'
  summary: string
  precedingToolUseIds: string[]
}

export type TombstoneMessage = MessageBase & {
  type: 'tombstone'
}

export type RequestStartEvent = {
  type: 'request_start'
  requestId?: string
  timestamp?: string
}

export type StreamEvent = RequestStartEvent | any

export type NormalizedUserMessage = UserMessage & {
  normalizedContent?: BetaContentBlock[]
}

export type NormalizedAssistantMessage = AssistantMessage & {
  normalizedContent?: BetaContentBlock[]
  usage?: BetaUsage
}

export type NormalizedMessage =
  | NormalizedUserMessage
  | NormalizedAssistantMessage
  | SystemMessage
  | AttachmentMessage
  | ProgressMessage
  | ToolUseSummaryMessage
  | GroupedToolUseMessage
  | CollapsedReadSearchGroup
  | TombstoneMessage

export type RenderableMessage = NormalizedMessage
export type CollapsibleMessage = RenderableMessage

export type Message =
  | UserMessage
  | AssistantMessage
  | SystemMessage
  | AttachmentMessage
  | ProgressMessage
  | ToolUseSummaryMessage
  | GroupedToolUseMessage
  | CollapsedReadSearchGroup
  | TombstoneMessage

export type ToolResultMessage = ToolResultBlockParam
