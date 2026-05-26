export type JobClassification = {
  isJob: boolean
  kind?: string
}

export function classifyJobRequest(_input: unknown): JobClassification {
  return { isJob: false }
}

export async function classifyAndWriteState(
  _jobDir: string | undefined,
  _messages: unknown[],
): Promise<void> {}
