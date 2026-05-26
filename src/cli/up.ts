export async function upMain(args: string[] = []): Promise<void> {
  throw new Error(`Update command is unavailable in this OpenClaude build: ${args.join(' ')}`)
}

export async function up(): Promise<void> {
  return upMain()
}
