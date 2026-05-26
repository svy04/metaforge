export async function connectHeadless(): Promise<void> {
  throw new Error('Headless server connect is unavailable in this OpenClaude build')
}

export async function runConnectHeadless(
  _config: unknown,
  _prompt: string,
  _outputFormat: string | undefined,
  _interactive: boolean,
): Promise<void> {
  throw new Error('Headless server connect is unavailable in this OpenClaude build')
}
