export function isUnavailableWorktreeError(message: string): boolean {
  return (
    message.includes('Cannot create agent worktree: not in a git repository') ||
    message.includes('WorktreeCreate hook failed:')
  )
}

export function resolveAgentWorktreeIsolation(params: {
  effectiveIsolation?: 'worktree' | 'remote'
  hasWorktreeCreateHook: boolean
  gitRoot: string | null
}): {
  attemptWorktree: boolean
  downgraded: boolean
} {
  if (params.effectiveIsolation !== 'worktree') {
    return {
      attemptWorktree: false,
      downgraded: false,
    }
  }

  const hasBackend = params.hasWorktreeCreateHook || params.gitRoot !== null
  return {
    attemptWorktree: hasBackend,
    downgraded: !hasBackend,
  }
}

export function shouldFallbackFromUnavailableWorktree(params: {
  message: string
  requestedIsolation?: 'worktree' | 'remote'
  agentType: string
}): boolean {
  return isUnavailableWorktreeError(params.message)
}
