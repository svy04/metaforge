// Generated-compatible type aliases derived from coreSchemas.ts.
// This source snapshot does not include the generator, so the committed
// surface keeps schemas as the single source of truth for SDK data types.
import type { z } from 'zod/v4'
import type {
  Message as APIAssistantMessage,
  MessageParam as APIUserMessage,
  RawMessageStreamEvent,
} from '@anthropic-ai/sdk/resources/messages/messages.mjs'
import type * as coreSchemas from './coreSchemas.js'
import type { NonNullableUsage } from './sdkUtilityTypes.js'

type InferSchema<T extends () => z.ZodType> = z.infer<ReturnType<T>>

export type ModelUsage = InferSchema<typeof coreSchemas.ModelUsageSchema>
export type OutputFormatType = InferSchema<
  typeof coreSchemas.OutputFormatTypeSchema
>
export type BaseOutputFormat = InferSchema<
  typeof coreSchemas.BaseOutputFormatSchema
>
export type JsonSchemaOutputFormat = InferSchema<
  typeof coreSchemas.JsonSchemaOutputFormatSchema
>
export type OutputFormat = InferSchema<typeof coreSchemas.OutputFormatSchema>
export type ApiKeySource = InferSchema<typeof coreSchemas.ApiKeySourceSchema>
export type ConfigScope = InferSchema<typeof coreSchemas.ConfigScopeSchema>
export type SdkBeta = InferSchema<typeof coreSchemas.SdkBetaSchema>
export type ThinkingAdaptive = InferSchema<
  typeof coreSchemas.ThinkingAdaptiveSchema
>
export type ThinkingEnabled = InferSchema<
  typeof coreSchemas.ThinkingEnabledSchema
>
export type ThinkingDisabled = InferSchema<
  typeof coreSchemas.ThinkingDisabledSchema
>
export type ThinkingConfig = InferSchema<typeof coreSchemas.ThinkingConfigSchema>
export type McpStdioServerConfig = InferSchema<
  typeof coreSchemas.McpStdioServerConfigSchema
>
export type McpSSEServerConfig = InferSchema<
  typeof coreSchemas.McpSSEServerConfigSchema
>
export type McpHttpServerConfig = InferSchema<
  typeof coreSchemas.McpHttpServerConfigSchema
>
export type McpSdkServerConfig = InferSchema<
  typeof coreSchemas.McpSdkServerConfigSchema
>
export type McpServerConfigForProcessTransport = InferSchema<
  typeof coreSchemas.McpServerConfigForProcessTransportSchema
>
export type McpClaudeAIProxyServerConfig = InferSchema<
  typeof coreSchemas.McpClaudeAIProxyServerConfigSchema
>
export type McpServerStatusConfig = InferSchema<
  typeof coreSchemas.McpServerStatusConfigSchema
>
export type McpServerStatus = InferSchema<
  typeof coreSchemas.McpServerStatusSchema
>
export type McpSetServersResult = InferSchema<
  typeof coreSchemas.McpSetServersResultSchema
>
export type PermissionUpdateDestination = InferSchema<
  typeof coreSchemas.PermissionUpdateDestinationSchema
>
export type PermissionBehavior = InferSchema<
  typeof coreSchemas.PermissionBehaviorSchema
>
export type PermissionRuleValue = InferSchema<
  typeof coreSchemas.PermissionRuleValueSchema
>
export type PermissionUpdate = InferSchema<
  typeof coreSchemas.PermissionUpdateSchema
>
export type PermissionDecisionClassification = InferSchema<
  typeof coreSchemas.PermissionDecisionClassificationSchema
>
export type PermissionResult = InferSchema<
  typeof coreSchemas.PermissionResultSchema
>
export type PermissionMode = InferSchema<typeof coreSchemas.PermissionModeSchema>
export type HookEvent = InferSchema<typeof coreSchemas.HookEventSchema>
export type BaseHookInput = InferSchema<typeof coreSchemas.BaseHookInputSchema>
export type PreToolUseHookInput = InferSchema<
  typeof coreSchemas.PreToolUseHookInputSchema
>
export type PermissionRequestHookInput = InferSchema<
  typeof coreSchemas.PermissionRequestHookInputSchema
>
export type PostToolUseHookInput = InferSchema<
  typeof coreSchemas.PostToolUseHookInputSchema
>
export type PostToolUseFailureHookInput = InferSchema<
  typeof coreSchemas.PostToolUseFailureHookInputSchema
>
export type PermissionDeniedHookInput = InferSchema<
  typeof coreSchemas.PermissionDeniedHookInputSchema
>
export type NotificationHookInput = InferSchema<
  typeof coreSchemas.NotificationHookInputSchema
>
export type UserPromptSubmitHookInput = InferSchema<
  typeof coreSchemas.UserPromptSubmitHookInputSchema
>
export type SessionStartHookInput = InferSchema<
  typeof coreSchemas.SessionStartHookInputSchema
>
export type SetupHookInput = InferSchema<typeof coreSchemas.SetupHookInputSchema>
export type StopHookInput = InferSchema<typeof coreSchemas.StopHookInputSchema>
export type StopFailureHookInput = InferSchema<
  typeof coreSchemas.StopFailureHookInputSchema
>
export type SubagentStartHookInput = InferSchema<
  typeof coreSchemas.SubagentStartHookInputSchema
>
export type SubagentStopHookInput = InferSchema<
  typeof coreSchemas.SubagentStopHookInputSchema
>
export type PreCompactHookInput = InferSchema<
  typeof coreSchemas.PreCompactHookInputSchema
>
export type PostCompactHookInput = InferSchema<
  typeof coreSchemas.PostCompactHookInputSchema
>
export type TeammateIdleHookInput = InferSchema<
  typeof coreSchemas.TeammateIdleHookInputSchema
>
export type TaskCreatedHookInput = InferSchema<
  typeof coreSchemas.TaskCreatedHookInputSchema
>
export type TaskCompletedHookInput = InferSchema<
  typeof coreSchemas.TaskCompletedHookInputSchema
>
export type ElicitationHookInput = InferSchema<
  typeof coreSchemas.ElicitationHookInputSchema
>
export type ElicitationResultHookInput = InferSchema<
  typeof coreSchemas.ElicitationResultHookInputSchema
>
export type ConfigChangeHookInput = InferSchema<
  typeof coreSchemas.ConfigChangeHookInputSchema
>
export type InstructionsLoadedHookInput = InferSchema<
  typeof coreSchemas.InstructionsLoadedHookInputSchema
>
export type WorktreeCreateHookInput = InferSchema<
  typeof coreSchemas.WorktreeCreateHookInputSchema
>
export type WorktreeRemoveHookInput = InferSchema<
  typeof coreSchemas.WorktreeRemoveHookInputSchema
>
export type CwdChangedHookInput = InferSchema<
  typeof coreSchemas.CwdChangedHookInputSchema
>
export type FileChangedHookInput = InferSchema<
  typeof coreSchemas.FileChangedHookInputSchema
>
export type ExitReason = InferSchema<typeof coreSchemas.ExitReasonSchema>
export type SessionEndHookInput = InferSchema<
  typeof coreSchemas.SessionEndHookInputSchema
>
export type HookInput = InferSchema<typeof coreSchemas.HookInputSchema>
export type AsyncHookJSONOutput = InferSchema<
  typeof coreSchemas.AsyncHookJSONOutputSchema
>
export type PreToolUseHookSpecificOutput = InferSchema<
  typeof coreSchemas.PreToolUseHookSpecificOutputSchema
>
export type UserPromptSubmitHookSpecificOutput = InferSchema<
  typeof coreSchemas.UserPromptSubmitHookSpecificOutputSchema
>
export type SessionStartHookSpecificOutput = InferSchema<
  typeof coreSchemas.SessionStartHookSpecificOutputSchema
>
export type SetupHookSpecificOutput = InferSchema<
  typeof coreSchemas.SetupHookSpecificOutputSchema
>
export type SubagentStartHookSpecificOutput = InferSchema<
  typeof coreSchemas.SubagentStartHookSpecificOutputSchema
>
export type PostToolUseHookSpecificOutput = InferSchema<
  typeof coreSchemas.PostToolUseHookSpecificOutputSchema
>
export type PostToolUseFailureHookSpecificOutput = InferSchema<
  typeof coreSchemas.PostToolUseFailureHookSpecificOutputSchema
>
export type PermissionDeniedHookSpecificOutput = InferSchema<
  typeof coreSchemas.PermissionDeniedHookSpecificOutputSchema
>
export type NotificationHookSpecificOutput = InferSchema<
  typeof coreSchemas.NotificationHookSpecificOutputSchema
>
export type PermissionRequestHookSpecificOutput = InferSchema<
  typeof coreSchemas.PermissionRequestHookSpecificOutputSchema
>
export type CwdChangedHookSpecificOutput = InferSchema<
  typeof coreSchemas.CwdChangedHookSpecificOutputSchema
>
export type FileChangedHookSpecificOutput = InferSchema<
  typeof coreSchemas.FileChangedHookSpecificOutputSchema
>
export type SyncHookJSONOutput = InferSchema<
  typeof coreSchemas.SyncHookJSONOutputSchema
>
export type ElicitationHookSpecificOutput = InferSchema<
  typeof coreSchemas.ElicitationHookSpecificOutputSchema
>
export type ElicitationResultHookSpecificOutput = InferSchema<
  typeof coreSchemas.ElicitationResultHookSpecificOutputSchema
>
export type WorktreeCreateHookSpecificOutput = InferSchema<
  typeof coreSchemas.WorktreeCreateHookSpecificOutputSchema
>
export type HookJSONOutput = InferSchema<
  typeof coreSchemas.HookJSONOutputSchema
>
export type PromptRequestOption = InferSchema<
  typeof coreSchemas.PromptRequestOptionSchema
>
export type PromptRequest = InferSchema<typeof coreSchemas.PromptRequestSchema>
export type PromptResponse = InferSchema<
  typeof coreSchemas.PromptResponseSchema
>
export type SlashCommand = InferSchema<typeof coreSchemas.SlashCommandSchema>
export type AgentInfo = InferSchema<typeof coreSchemas.AgentInfoSchema>
export type ModelInfo = InferSchema<typeof coreSchemas.ModelInfoSchema>
export type AccountInfo = InferSchema<typeof coreSchemas.AccountInfoSchema>
export type AgentMcpServerSpec = InferSchema<
  typeof coreSchemas.AgentMcpServerSpecSchema
>
export type AgentDefinition = InferSchema<
  typeof coreSchemas.AgentDefinitionSchema
>
export type SettingSource = InferSchema<typeof coreSchemas.SettingSourceSchema>
export type SdkPluginConfig = InferSchema<
  typeof coreSchemas.SdkPluginConfigSchema
>
export type RewindFilesResult = InferSchema<
  typeof coreSchemas.RewindFilesResultSchema
>
export type SDKAssistantMessageError = InferSchema<
  typeof coreSchemas.SDKAssistantMessageErrorSchema
>
export type SDKStatus = InferSchema<typeof coreSchemas.SDKStatusSchema>
export type SDKUserMessage = Omit<
  InferSchema<typeof coreSchemas.SDKUserMessageSchema>,
  'message'
> & {
  message: any
}
export type SDKUserMessageReplay = Omit<
  InferSchema<typeof coreSchemas.SDKUserMessageReplaySchema>,
  'isReplay' | 'message'
> & {
  isReplay?: true
  message: any
}
export type SDKRateLimitInfo = InferSchema<
  typeof coreSchemas.SDKRateLimitInfoSchema
>
export type SDKAssistantMessage = Omit<
  InferSchema<typeof coreSchemas.SDKAssistantMessageSchema>,
  'message'
> & {
  message: any
}
export type SDKRateLimitEvent = InferSchema<
  typeof coreSchemas.SDKRateLimitEventSchema
>
export type SDKStreamlinedTextMessage = InferSchema<
  typeof coreSchemas.SDKStreamlinedTextMessageSchema
>
export type SDKStreamlinedToolUseSummaryMessage = InferSchema<
  typeof coreSchemas.SDKStreamlinedToolUseSummaryMessageSchema
>
export type SDKPermissionDenial = InferSchema<
  typeof coreSchemas.SDKPermissionDenialSchema
>
export type SDKResultSuccess = Omit<
  InferSchema<typeof coreSchemas.SDKResultSuccessSchema>,
  'usage'
> & {
  usage: NonNullableUsage
}
export type SDKResultError = Omit<
  InferSchema<typeof coreSchemas.SDKResultErrorSchema>,
  'usage'
> & {
  usage: NonNullableUsage
}
export type SDKResultMessage = SDKResultSuccess | SDKResultError
export type SDKSystemMessage = InferSchema<
  typeof coreSchemas.SDKSystemMessageSchema
>
export type SDKPartialAssistantMessage = Omit<
  InferSchema<typeof coreSchemas.SDKPartialAssistantMessageSchema>,
  'event'
> & {
  event: any
}
export type SDKCompactBoundaryMessage = InferSchema<
  typeof coreSchemas.SDKCompactBoundaryMessageSchema
>
export type SDKStatusMessage = InferSchema<
  typeof coreSchemas.SDKStatusMessageSchema
>
export type SDKPostTurnSummaryMessage = InferSchema<
  typeof coreSchemas.SDKPostTurnSummaryMessageSchema
>
export type SDKAPIRetryMessage = InferSchema<
  typeof coreSchemas.SDKAPIRetryMessageSchema
>
export type SDKLocalCommandOutputMessage = InferSchema<
  typeof coreSchemas.SDKLocalCommandOutputMessageSchema
>
export type SDKHookStartedMessage = InferSchema<
  typeof coreSchemas.SDKHookStartedMessageSchema
>
export type SDKHookProgressMessage = InferSchema<
  typeof coreSchemas.SDKHookProgressMessageSchema
>
export type SDKHookResponseMessage = InferSchema<
  typeof coreSchemas.SDKHookResponseMessageSchema
>
export type SDKToolProgressMessage = InferSchema<
  typeof coreSchemas.SDKToolProgressMessageSchema
>
export type SDKAuthStatusMessage = InferSchema<
  typeof coreSchemas.SDKAuthStatusMessageSchema
>
export type SDKFilesPersistedEvent = InferSchema<
  typeof coreSchemas.SDKFilesPersistedEventSchema
>
export type SDKTaskNotificationMessage = InferSchema<
  typeof coreSchemas.SDKTaskNotificationMessageSchema
>
export type SDKTaskStartedMessage = InferSchema<
  typeof coreSchemas.SDKTaskStartedMessageSchema
>
export type SDKSessionStateChangedMessage = InferSchema<
  typeof coreSchemas.SDKSessionStateChangedMessageSchema
>
export type SDKTaskProgressMessage = InferSchema<
  typeof coreSchemas.SDKTaskProgressMessageSchema
>
export type SDKToolUseSummaryMessage = InferSchema<
  typeof coreSchemas.SDKToolUseSummaryMessageSchema
>
export type SDKElicitationCompleteMessage = InferSchema<
  typeof coreSchemas.SDKElicitationCompleteMessageSchema
>
export type SDKPromptSuggestionMessage = InferSchema<
  typeof coreSchemas.SDKPromptSuggestionMessageSchema
>
export type SDKSessionInfo = InferSchema<
  typeof coreSchemas.SDKSessionInfoSchema
>
export type SDKMessage = any
export type FastModeState = InferSchema<typeof coreSchemas.FastModeStateSchema>
