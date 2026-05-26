export type SSHSession = {
  id?: string
  host?: string
  remoteCwd: string
  close?: () => void | Promise<void>
}

export class SSHSessionError extends Error {}

export function createLocalSSHSession({
  cwd,
}: {
  cwd?: string
  permissionMode?: string
  dangerouslySkipPermissions?: boolean
}): SSHSession {
  return { remoteCwd: cwd ?? '', host: 'local' }
}

export async function createSSHSession(
  {
    host,
    cwd,
  }: {
    host?: string
    cwd?: string
    localVersion?: string
    permissionMode?: string
    dangerouslySkipPermissions?: boolean
    extraCliArgs?: string[]
  },
  _options?: {
    onProgress?: (message: string) => void
  },
): Promise<SSHSession> {
  throw new Error('SSH sessions are unavailable in this OpenClaude build')
}
