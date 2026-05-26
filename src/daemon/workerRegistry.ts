export async function runDaemonWorker(workerId?: string): Promise<void> {
  throw new Error(`Daemon worker is unavailable in this OpenClaude build: ${workerId ?? 'unknown'}`)
}
