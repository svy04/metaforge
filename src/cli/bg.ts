function unavailable(command: string): never {
  throw new Error(`Background session command is unavailable in this OpenClaude build: ${command}`)
}

export async function psHandler(_args: string[] = []): Promise<void> {
  unavailable('ps')
}

export async function logsHandler(_sessionId?: string): Promise<void> {
  unavailable('logs')
}

export async function attachHandler(_sessionId?: string): Promise<void> {
  unavailable('attach')
}

export async function killHandler(_sessionId?: string): Promise<void> {
  unavailable('kill')
}

export async function handleBgFlag(_args: string[] = []): Promise<void> {
  unavailable('background')
}
