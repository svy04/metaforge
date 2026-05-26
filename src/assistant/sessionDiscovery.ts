export type AssistantSession = {
  id: string
  title?: string
  cwd?: string
  updatedAt?: number
  source?: string
}

export async function discoverAssistantSessions(): Promise<AssistantSession[]> {
  return []
}
