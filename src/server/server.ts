export type ServerHandle = {
  port?: number
  stop: (force?: boolean) => void
}

export function startServer(
  _config?: unknown,
  _sessionManager?: unknown,
  _logger?: unknown,
): ServerHandle {
  throw new Error('Server mode is unavailable in this OpenClaude build')
}
