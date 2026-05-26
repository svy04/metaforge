export type RemoteSkillLoadResult = {
  cacheHit: boolean
  latencyMs: number
  skillPath: string
  content: string
  fileCount: number
  totalBytes: number
  fetchMethod: string
}

export async function loadRemoteSkill(
  _slug?: string,
  _url?: string,
): Promise<RemoteSkillLoadResult> {
  throw new Error('Remote skill loading is unavailable in this OpenClaude build')
}
