import type { LocalCommandCall } from '../../types/command.js'
import { getCwd } from '../../utils/cwd.js'
import {
  applyStoredShadowCandidate,
  readLatestShadowReview,
} from '../../services/orchestra/promotionStore.js'
import type { ShadowLabel } from '../../services/orchestra/worktreeManager.js'

const VALID_LABELS = new Set(['gpt-a', 'gpt-b', 'opus-shadow'])

function parseArgs(args: string): {
  candidateLabel?: ShadowLabel
  confirmedOpusShadow: boolean
} {
  const parts = args.trim().split(/\s+/).filter(Boolean)
  const label = parts[0]
  return {
    candidateLabel: VALID_LABELS.has(label ?? '')
      ? (label as ShadowLabel)
      : undefined,
    confirmedOpusShadow:
      parts.includes('--confirm-opus') || parts.includes('confirm'),
  }
}

function failureMessage(reason: string, detail?: string): string {
  switch (reason) {
    case 'not-git':
      return `Cannot apply orchestra candidate: current directory is not a git repository${detail ? ` (${detail})` : ''}.`
    case 'latest-review-missing':
      return 'Cannot apply orchestra candidate: no latest shadow review was found. Run a shadow-enabled code task first.'
    case 'candidate-not-found':
      return 'Cannot apply orchestra candidate: that label is not in the latest shadow review.'
    case 'candidate-failed':
      return 'Cannot apply orchestra candidate: that candidate did not complete.'
    case 'red-verdict':
      return 'Cannot apply orchestra candidate: evidence verdict is red.'
    case 'opus-shadow-needs-confirm':
      return 'Opus shadow needs a second confirmation. Re-run: /orchestra-apply opus-shadow --confirm-opus'
    case 'unsafe-path':
      return `Cannot apply orchestra candidate: unsafe file path${detail ? ` (${detail})` : ''}.`
    case 'source-file-missing':
      return `Cannot apply orchestra candidate: source file missing from shadow worktree${detail ? ` (${detail})` : ''}.`
    default:
      return `Cannot apply orchestra candidate: ${reason}.`
  }
}

export const call: LocalCommandCall = async args => {
  const parsed = parseArgs(args)
  if (!parsed.candidateLabel) {
    const latest = await readLatestShadowReview(getCwd())
    const labels = latest.ok
      ? latest.review.candidates.map(c => c.label).join(', ')
      : 'gpt-a, gpt-b, opus-shadow'
    return {
      type: 'text',
      value: `Usage: /orchestra-apply <${labels}> [--confirm-opus]`,
    }
  }

  const result = await applyStoredShadowCandidate({
    cwd: getCwd(),
    candidateLabel: parsed.candidateLabel,
    confirmedOpusShadow: parsed.confirmedOpusShadow,
  })
  if (!result.ok) {
    return {
      type: 'text',
      value: failureMessage(result.reason, result.detail),
    }
  }
  return {
    type: 'text',
    value:
      `Applied ${result.appliedLabel} from latest shadow review.\n` +
      `Files:\n${result.appliedFiles.map(f => `- ${f}`).join('\n')}`,
  }
}

