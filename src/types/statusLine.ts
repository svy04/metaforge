import type { PermissionMode } from './permissions.js'

export type StatusLineRateLimitWindow = {
  used_percentage?: number
  resets_at?: string
  remaining_tokens?: number
  [key: string]: unknown
}

export type StatusLineCommandInput = {
  hook_event_name?: 'StatusLine'
  session_id?: string
  transcript_path?: string
  cwd?: string
  permission_mode?: PermissionMode | string
  model?: {
    id?: string
    display_name?: string
    [key: string]: unknown
  }
  workspace?: {
    current_dir?: string
    project_dir?: string
    added_dirs?: string[]
    [key: string]: unknown
  }
  version?: string
  output_style?: {
    name?: string
    [key: string]: unknown
  }
  cost?: Record<string, unknown>
  tokens?: Record<string, unknown>
  rate_limits?: any
  vim?: Record<string, unknown>
  worktree?: Record<string, unknown>
  agent?: Record<string, unknown>
  [key: string]: unknown
}
