declare module '*.md' {
  const content: string
  export default content
}

declare module 'asciichart' {
  export function plot(series: number[] | number[][], options?: Record<string, unknown>): string
}

declare module 'plist' {
  export function parse(content: string): unknown
  export function build(value: unknown): string
}

declare module 'audio-capture-napi' {
  export const AudioCapture: any
  export function isNativeAudioAvailable(): boolean
  export function isNativeRecordingActive(): boolean
  export function startNativeRecording(
    onData: (data: Buffer) => void,
    onError?: (error: Error) => void,
  ): boolean
  export function stopNativeRecording(): void
  const moduleExports: any
  export default moduleExports
}

declare module 'image-processor-napi' {
  const moduleExports: any
  export default moduleExports
}

declare module 'cacache' {
  const moduleExports: any
  export default moduleExports
}

declare module '@ant/computer-use-mcp/sentinelApps' {
  export const SentinelAppCategory: any
  export const sentinelApps: any
  export function getSentinelCategory(app: unknown): unknown
}

declare module '@ant/computer-use-mcp/types' {
  export const DEFAULT_GRANT_FLAGS: any
  export type CoordinateMode = any
  export type CuPermissionRequest = any
  export type CuPermissionResponse = any
  export type CuSubGates = any
  export type ComputerUseHostAdapter = any
  export type Logger = any
  export type ComputerUsePermission = any
  export type ComputerUseAction = any
  export type SentinelApp = any
}

declare module '@ant/computer-use-mcp' {
  export const API_RESIZE_PARAMS: any
  export const DEFAULT_GRANT_FLAGS: any
  export type FrontmostApp = any
  export type InstalledApp = any
  export type ResolvePrepareCaptureResult = any
  export type RunningApp = any
  export type ScreenshotResult = any
  export function bindSessionContext(...args: any[]): any
  export function buildComputerUseTools(...args: any[]): any
  export function createComputerUseMcpServer(...args: any[]): any
  export function targetImageSize(...args: any[]): any
  export type ComputerExecutor = any
  export type ComputerUseSessionContext = any
  export type CuCallToolResult = any
  export type CuPermissionRequest = any
  export type CuPermissionResponse = any
  export type DisplayGeometry = any
  export type ScreenshotDims = any
}

declare module '@ant/computer-use-input' {
  export type ComputerUseInputAPI = any
  export type ComputerUseInput = any
  const moduleExports: any
  export default moduleExports
}

declare module '@ant/computer-use-swift' {
  export type ComputerUseAPI = any
  const moduleExports: any
  export default moduleExports
}

declare module '@ant/claude-for-chrome-mcp' {
  export const BROWSER_TOOLS: any
  export type ClaudeForChromeContext = any
  export function createClaudeForChromeMcpServer(...args: any[]): any
  export type Logger = any
  export type PermissionMode = any
  const moduleExports: any
  export default moduleExports
}

declare module '@opentelemetry/exporter-metrics-otlp-grpc' {
  export class OTLPMetricExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-metrics-otlp-http' {
  export class OTLPMetricExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-metrics-otlp-proto' {
  export class OTLPMetricExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-prometheus' {
  export class PrometheusExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-logs-otlp-grpc' {
  export class OTLPLogExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-logs-otlp-proto' {
  export class OTLPLogExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-trace-otlp-http' {
  export class OTLPTraceExporter {
    constructor(...args: any[])
  }
}

declare module '@opentelemetry/exporter-trace-otlp-proto' {
  export class OTLPTraceExporter {
    constructor(...args: any[])
  }
}

declare module 'url-handler-napi' {
  export function waitForUrlEvent(timeoutMs: number): string | null
}
