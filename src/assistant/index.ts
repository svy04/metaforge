export function isAssistantMode(): boolean {
  return false
}

export function isAssistantForced(): boolean {
  return false
}

export function markAssistantForced(): void {}

export async function initializeAssistantTeam(): Promise<undefined> {
  return undefined
}

export function getAssistantSystemPromptAddendum(): string {
  return ''
}

export function getAssistantActivationPath(): string | undefined {
  return undefined
}
