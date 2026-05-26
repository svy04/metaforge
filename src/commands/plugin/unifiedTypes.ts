export type UnifiedInstalledItem = {
  id: string
  type:
    | 'plugin'
    | 'flagged-plugin'
    | 'failed-plugin'
    | 'mcp-server'
    | (string & {})
  name: string
  scope?: string
  marketplace?: string
  isEnabled?: boolean
  pendingToggle?: 'will-enable' | 'will-disable'
  errorCount?: number
  status?: string
  indented?: boolean
  [key: string]: unknown
}

