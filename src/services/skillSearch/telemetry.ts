export function logRemoteSkillTelemetry(_event: string, _fields?: Record<string, unknown>): void {}

export function logRemoteSkillLoaded(_fields: {
  slug: string
  cacheHit: boolean
  latencyMs: number
  urlScheme: 'gs' | 'http' | 'https' | 's3'
  fileCount?: number
  totalBytes?: number
  fetchMethod?: string
  error?: string
}): void {}
