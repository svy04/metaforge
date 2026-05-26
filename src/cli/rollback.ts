export async function rollbackMain(args: string[] = []): Promise<void> {
  throw new Error(`Rollback command is unavailable in this OpenClaude build: ${args.join(' ')}`)
}

export async function rollback(
  target?: string,
  options?: {
    list?: boolean
    dryRun?: boolean
    safe?: boolean
  },
): Promise<void> {
  const args = [target, options?.list ? '--list' : '', options?.dryRun ? '--dry-run' : '', options?.safe ? '--safe' : ''].filter((arg): arg is string => Boolean(arg))
  return rollbackMain(args)
}
