export async function daemonMain(args: string[] = []): Promise<void> {
  throw new Error(`Daemon mode is unavailable in this OpenClaude build: ${args.join(' ')}`)
}
