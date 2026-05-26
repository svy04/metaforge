export type Terminal = {
  type?: 'terminal'
  value?: unknown
  reason?: string
  error?: unknown
  turnCount?: number
}

export type Continue = {
  type?: 'continue'
  value?: unknown
  reason?: string
  committed?: number
  attempt?: number
}
