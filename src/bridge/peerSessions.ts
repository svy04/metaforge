export async function postInterClaudeMessage(
  _target: string,
  _message: string,
): Promise<{ ok: false; error: string }> {
  return {
    ok: false,
    error: 'Peer sessions are unavailable in this OpenClaude build',
  }
}
