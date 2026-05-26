import type { CallToolResult, ToolAnnotations } from '@modelcontextprotocol/sdk/types.js'
import type { z } from 'zod/v4'
import type {
  McpSdkServerConfig,
  SDKMessage,
  SDKSessionInfo,
  SDKUserMessage,
} from './coreTypes.js'

export type EffortLevel = 'low' | 'medium' | 'high' | 'max'

export type AnyZodRawShape = Record<string, z.ZodType>

export type InferShape<Schema extends AnyZodRawShape> = {
  [Key in keyof Schema]: z.infer<Schema[Key]>
}

export type SdkMcpToolDefinition<Schema extends AnyZodRawShape> = {
  type: 'tool'
  name: string
  description: string
  inputSchema: Schema
  handler: (
    args: InferShape<Schema>,
    extra: unknown,
  ) => Promise<CallToolResult>
  annotations?: ToolAnnotations
  searchHint?: string
  alwaysLoad?: boolean
}

export type McpSdkServerConfigWithInstance = McpSdkServerConfig & {
  instance: unknown
}

export type SessionMessage = SDKMessage

export type GetSessionMessagesOptions = {
  dir?: string
  limit?: number
  offset?: number
  includeSystemMessages?: boolean
}

export type ListSessionsOptions = {
  dir?: string
  limit?: number
  offset?: number
}

export type GetSessionInfoOptions = {
  dir?: string
}

export type SessionMutationOptions = {
  dir?: string
}

export type ForkSessionOptions = {
  dir?: string
  upToMessageId?: string
  title?: string
}

export type ForkSessionResult = {
  sessionId: string
}

export type SDKSessionOptions = Options

export type Options = {
  cwd?: string
  abortController?: AbortController
  maxTurns?: number
  model?: string
  fallbackModel?: string
  permissionMode?: string
  allowedTools?: string[]
  disallowedTools?: string[]
  appendSystemPrompt?: string
  customSystemPrompt?: string
  mcpServers?: Record<string, unknown>
}

export type InternalOptions = Options & {
  [key: string]: unknown
}

export type Query = AsyncGenerator<SDKMessage, void, unknown>
export type InternalQuery = AsyncGenerator<SDKMessage, void, unknown>

export type SDKSession = {
  query(prompt: string | AsyncIterable<SDKUserMessage>): Query
  interrupt?(): void
  close?(): Promise<void>
}
