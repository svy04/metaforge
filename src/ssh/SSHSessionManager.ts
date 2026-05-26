import type { SSHSession } from './createSSHSession.js'

export class SSHSessionManager {
  async createSession(): Promise<SSHSession> {
    throw new Error('SSH session manager is unavailable in this OpenClaude build')
  }

  async close(): Promise<void> {}
}
