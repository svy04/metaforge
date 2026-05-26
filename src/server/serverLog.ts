export function logServerMessage(_message: string): void {}

export function createServerLogger(): {
  log: (message: string) => void
  error: (message: string) => void
} {
  return {
    log: logServerMessage,
    error: logServerMessage,
  }
}
