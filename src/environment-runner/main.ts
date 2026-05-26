export async function environmentRunnerMain(args: string[] = []): Promise<void> {
  throw new Error(`Environment runner is unavailable in this OpenClaude build: ${args.join(' ')}`)
}
