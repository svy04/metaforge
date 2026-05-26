export type CachedMCConfig = {
  supportedModels?: string[]
  [key: string]: unknown
}

export function getCachedMCConfig(): CachedMCConfig | null {
  return null
}

