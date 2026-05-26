export function getDefaultUdsSocketPath(): string {
  return ''
}

export async function startUdsMessaging(
  _socketPath: string,
  _options?: { isExplicit?: boolean },
): Promise<void> {}
