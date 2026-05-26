import type { z } from 'zod/v4'
import type {
  ControlErrorResponseSchema,
  ControlResponseSchema,
  JSONRPCMessagePlaceholder,
  SDKControlApplyFlagSettingsRequestSchema,
  SDKControlCancelAsyncMessageRequestSchema,
  SDKControlCancelAsyncMessageResponseSchema,
  SDKControlCancelRequestSchema,
  SDKControlElicitationRequestSchema,
  SDKControlElicitationResponseSchema,
  SDKControlGetContextUsageRequestSchema,
  SDKControlGetContextUsageResponseSchema,
  SDKControlGetSettingsRequestSchema,
  SDKControlGetSettingsResponseSchema,
  SDKControlInitializeRequestSchema,
  SDKControlInitializeResponseSchema,
  SDKControlInterruptRequestSchema,
  SDKControlMcpMessageRequestSchema,
  SDKControlMcpReconnectRequestSchema,
  SDKControlMcpSetServersRequestSchema,
  SDKControlMcpSetServersResponseSchema,
  SDKControlMcpStatusRequestSchema,
  SDKControlMcpStatusResponseSchema,
  SDKControlMcpToggleRequestSchema,
  SDKControlPermissionRequestSchema,
  SDKControlReloadPluginsRequestSchema,
  SDKControlReloadPluginsResponseSchema,
  SDKControlRequestInnerSchema,
  SDKControlRequestSchema,
  SDKControlResponseSchema,
  SDKControlRewindFilesRequestSchema,
  SDKControlRewindFilesResponseSchema,
  SDKControlSeedReadStateRequestSchema,
  SDKControlSetMaxThinkingTokensRequestSchema,
  SDKControlSetModelRequestSchema,
  SDKControlSetPermissionModeRequestSchema,
  SDKControlStopTaskRequestSchema,
  SDKHookCallbackMatcherSchema,
  SDKHookCallbackRequestSchema,
  SDKKeepAliveMessageSchema,
  SDKUpdateEnvironmentVariablesMessageSchema,
  StdinMessageSchema,
  StdoutMessageSchema,
} from './controlSchemas.js'
export type { SDKPartialAssistantMessage } from './coreTypes.js'

type InferSchema<T extends () => z.ZodType> = z.infer<ReturnType<T>>

export type JSONRPCMessage = InferSchema<typeof JSONRPCMessagePlaceholder>
export type SDKHookCallbackMatcher = InferSchema<
  typeof SDKHookCallbackMatcherSchema
>
export type SDKControlInitializeRequest = InferSchema<
  typeof SDKControlInitializeRequestSchema
>
export type SDKControlInitializeResponse = InferSchema<
  typeof SDKControlInitializeResponseSchema
>
export type SDKControlInterruptRequest = InferSchema<
  typeof SDKControlInterruptRequestSchema
>
export type SDKControlPermissionRequest = InferSchema<
  typeof SDKControlPermissionRequestSchema
>
export type SDKControlSetPermissionModeRequest = InferSchema<
  typeof SDKControlSetPermissionModeRequestSchema
>
export type SDKControlSetModelRequest = InferSchema<
  typeof SDKControlSetModelRequestSchema
>
export type SDKControlSetMaxThinkingTokensRequest = InferSchema<
  typeof SDKControlSetMaxThinkingTokensRequestSchema
>
export type SDKControlMcpStatusRequest = InferSchema<
  typeof SDKControlMcpStatusRequestSchema
>
export type SDKControlMcpStatusResponse = InferSchema<
  typeof SDKControlMcpStatusResponseSchema
>
export type SDKControlGetContextUsageRequest = InferSchema<
  typeof SDKControlGetContextUsageRequestSchema
>
export type SDKControlGetContextUsageResponse = InferSchema<
  typeof SDKControlGetContextUsageResponseSchema
>
export type SDKControlRewindFilesRequest = InferSchema<
  typeof SDKControlRewindFilesRequestSchema
>
export type SDKControlRewindFilesResponse = InferSchema<
  typeof SDKControlRewindFilesResponseSchema
>
export type SDKControlCancelAsyncMessageRequest = InferSchema<
  typeof SDKControlCancelAsyncMessageRequestSchema
>
export type SDKControlCancelAsyncMessageResponse = InferSchema<
  typeof SDKControlCancelAsyncMessageResponseSchema
>
export type SDKControlSeedReadStateRequest = InferSchema<
  typeof SDKControlSeedReadStateRequestSchema
>
export type SDKHookCallbackRequest = InferSchema<
  typeof SDKHookCallbackRequestSchema
>
export type SDKControlMcpMessageRequest = InferSchema<
  typeof SDKControlMcpMessageRequestSchema
>
export type SDKControlMcpSetServersRequest = InferSchema<
  typeof SDKControlMcpSetServersRequestSchema
>
export type SDKControlMcpSetServersResponse = InferSchema<
  typeof SDKControlMcpSetServersResponseSchema
>
export type SDKControlReloadPluginsRequest = InferSchema<
  typeof SDKControlReloadPluginsRequestSchema
>
export type SDKControlReloadPluginsResponse = InferSchema<
  typeof SDKControlReloadPluginsResponseSchema
>
export type SDKControlMcpReconnectRequest = InferSchema<
  typeof SDKControlMcpReconnectRequestSchema
>
export type SDKControlMcpToggleRequest = InferSchema<
  typeof SDKControlMcpToggleRequestSchema
>
export type SDKControlStopTaskRequest = InferSchema<
  typeof SDKControlStopTaskRequestSchema
>
export type SDKControlApplyFlagSettingsRequest = InferSchema<
  typeof SDKControlApplyFlagSettingsRequestSchema
>
export type SDKControlGetSettingsRequest = InferSchema<
  typeof SDKControlGetSettingsRequestSchema
>
export type SDKControlGetSettingsResponse = InferSchema<
  typeof SDKControlGetSettingsResponseSchema
>
export type SDKControlElicitationRequest = InferSchema<
  typeof SDKControlElicitationRequestSchema
>
export type SDKControlElicitationResponse = InferSchema<
  typeof SDKControlElicitationResponseSchema
>
export type SDKControlRequestInner = InferSchema<
  typeof SDKControlRequestInnerSchema
>
export type SDKControlRequest = InferSchema<typeof SDKControlRequestSchema>
export type ControlResponse = InferSchema<typeof ControlResponseSchema>
export type ControlErrorResponse = InferSchema<typeof ControlErrorResponseSchema>
export type SDKControlResponse = InferSchema<typeof SDKControlResponseSchema>
export type SDKControlCancelRequest = InferSchema<
  typeof SDKControlCancelRequestSchema
>
export type SDKKeepAliveMessage = InferSchema<typeof SDKKeepAliveMessageSchema>
export type SDKUpdateEnvironmentVariablesMessage = InferSchema<
  typeof SDKUpdateEnvironmentVariablesMessageSchema
>
export type StdoutMessage = InferSchema<typeof StdoutMessageSchema>
export type StdinMessage = InferSchema<typeof StdinMessageSchema>
