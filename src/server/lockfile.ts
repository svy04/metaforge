export async function acquireServerLock(): Promise<() => void> {
  return () => {}
}

export type ServerLockInfo = {
  pid: number
  port: number
  host: string
  httpUrl: string
  startedAt: number
}

export async function writeServerLock(_info: ServerLockInfo): Promise<void> {}

export async function removeServerLock(): Promise<void> {}

export async function probeRunningServer(): Promise<ServerLockInfo | null> {
  return null
}
