import { afterEach, expect, test } from 'bun:test'

const originalAbortSignalTimeout = AbortSignal.timeout

afterEach(() => {
  ;(AbortSignal as unknown as { timeout: typeof originalAbortSignalTimeout }).timeout =
    originalAbortSignalTimeout
})

test('Opus planner uses a 180s abort timeout', async () => {
  ;(globalThis as unknown as { MACRO?: { VERSION: string } }).MACRO = {
    VERSION: '0.6.0',
  }
  let plannerTimeoutMs: number | undefined
  ;(AbortSignal as unknown as { timeout: (ms: number) => AbortSignal }).timeout =
    (ms: number) => {
      plannerTimeoutMs = ms
      return new AbortController().signal
    }

  const { callOpusPlanner } = await import('./orchestrator.js')

  try {
    await expect(
      callOpusPlanner({
        messages: [{ type: 'user', message: { content: 'plan this' } }],
        systemPrompt: 'system',
        userContext: {},
        settings: {},
        claudeLoginPlanner: async () => ({
          goal: 'ok',
          architectureNotes: [],
          implementationConstraints: [],
          risks: [],
          researchNeeds: [],
          memoryCandidates: [],
        }),
      }),
    ).resolves.toMatchObject({ goal: 'ok' })

    expect(plannerTimeoutMs).toBe(180_000)
  } finally {
    ;(AbortSignal as unknown as { timeout: typeof originalAbortSignalTimeout }).timeout =
      originalAbortSignalTimeout
  }
})
