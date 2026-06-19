import { describe, expect, test } from 'bun:test'

describe('SettingsSchema orchestra', () => {
  test('accepts orchestra settings', async () => {
    const { SettingsSchema } = await import('./types.js')
    const result = SettingsSchema().safeParse({
      orchestra: {
        enabled: true,
        lead: 'codex',
        visibility: 'codex-final',
        memoryScope: 'project',
        mode: 'codex-dominant',
        plannerPolicy: 'risk-gated',
        plannerFailurePolicy: 'adaptive',
        workerPolicy: 'codex-first',
        verifierPolicy: 'codex-default-opus-on-risk',
        parallelism: 'independent-lanes-only',
        roles: {
          planner: 'Claude Opus (configured)',
          implementer: 'Codex GPT 5.5',
        },
        models: {
          planner: 'claude-opus-4-7-custom',
          implementer: 'gpt-5.5-custom',
        },
      },
    })

    expect(result.success).toBe(true)
  })

  test('rejects non-project memory scope', async () => {
    const { SettingsSchema } = await import('./types.js')
    const result = SettingsSchema().safeParse({
      orchestra: { memoryScope: 'global' },
    })

    expect(result.success).toBe(false)
  })

  test('rejects invalid planner policy', async () => {
    const { SettingsSchema } = await import('./types.js')
    const result = SettingsSchema().safeParse({
      orchestra: { plannerPolicy: 'vote' },
    })

    expect(result.success).toBe(false)
  })

  test('rejects invalid planner failure policy', async () => {
    const { SettingsSchema } = await import('./types.js')
    const result = SettingsSchema().safeParse({
      orchestra: { plannerFailurePolicy: 'silent' },
    })

    expect(result.success).toBe(false)
  })
})
