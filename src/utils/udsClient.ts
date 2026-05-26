export type LiveSession = {
  kind?: string
  sessionId?: string
}

export async function sendToUdsSocket(_target: string, _message: string): Promise<void> {
  throw new Error('UDS messaging is unavailable in this OpenClaude build')
}

export async function listAllLiveSessions(): Promise<LiveSession[]> {
  return []
}
