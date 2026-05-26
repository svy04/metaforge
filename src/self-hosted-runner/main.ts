export async function selfHostedRunnerMain(args: string[] = []): Promise<void> {
  throw new Error(`Self-hosted runner is unavailable in this OpenClaude build: ${args.join(' ')}`)
}
