import type { BetaUsage as Usage } from '@anthropic-ai/sdk/resources/beta/messages/messages.mjs'

export type NonNullableUsage = {
  [Key in keyof Usage]-?: NonNullable<Usage[Key]>
}
