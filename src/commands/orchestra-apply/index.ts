import type { Command } from '../../commands.js'

export const orchestraApply = {
  type: 'local',
  name: 'orchestra-apply',
  description: 'Apply the selected latest OpenClaude shadow candidate',
  argumentHint: '<gpt-a|gpt-b|opus-shadow> [--confirm-opus]',
  supportsNonInteractive: true,
  load: () => import('./orchestra-apply.js'),
} satisfies Command

export const orchestraReject = {
  type: 'local',
  name: 'orchestra-reject',
  description: 'Reject the latest OpenClaude shadow review and prune its worktrees',
  supportsNonInteractive: true,
  load: () => import('./orchestra-reject.js'),
} satisfies Command

