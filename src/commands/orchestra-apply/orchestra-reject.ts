import type { LocalCommandCall } from '../../types/command.js'
import { getCwd } from '../../utils/cwd.js'
import { rejectStoredShadowReview } from '../../services/orchestra/promotionStore.js'

export const call: LocalCommandCall = async () => {
  const result = await rejectStoredShadowReview({ cwd: getCwd() })
  if (!result.ok) {
    const suffix = result.detail ? ` (${result.detail})` : ''
    return {
      type: 'text',
      value:
        result.reason === 'not-git'
          ? `Cannot reject orchestra review: current directory is not a git repository${suffix}.`
          : 'Cannot reject orchestra review: no latest shadow review was found.',
    }
  }
  return {
    type: 'text',
    value:
      `Rejected latest shadow review.\n` +
      `Pruned worktrees: ${result.pruned.length}\n` +
      `Failed prune attempts: ${result.failedPrune.length}`,
  }
}

