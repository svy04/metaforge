import { describe, expect, test } from 'bun:test'

import { EFFORT_BETA_HEADER } from '../../constants/betas.js'
import { OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { createUserMessage } from '../../utils/messages.js'
import {
  buildClaudeLoginPlannerRequest,
  buildOrchestraGuidance,
  buildSkepticDissent,
  parseOrchestraAdvisory,
  resolveClaudeLoginPlannerAuth,
  shouldRunOrchestra,
} from './orchestrator.js'
import { EMPTY_DISSENT, type DissentReport } from './skeptic.js'

const topLevelContext = {
  querySource: 'repl_main_thread',
  turnCount: 1,
  agentId: undefined,
}

describe('orchestra advisory orchestration', () => {
  test('uses Claude login tokens for the Opus planner auth path', () => {
    expect(
      resolveClaudeLoginPlannerAuth({
        accessToken: 'login-token',
        refreshToken: 'refresh-token',
        expiresAt: Date.now() + 60_000,
        scopes: ['user:inference'],
        subscriptionType: 'max',
        rateLimitTier: null,
      }),
    ).toEqual({ authToken: 'login-token' })

    expect(
      resolveClaudeLoginPlannerAuth({
        accessToken: 'api-like-token',
        refreshToken: null,
        expiresAt: null,
        scopes: ['org:create_api_key'],
        subscriptionType: null,
        rateLimitTier: null,
      }),
    ).toBeNull()
  })

  test('builds hidden Claude Opus planner requests with max effort', () => {
    const request = buildClaudeLoginPlannerRequest({
      model: 'claude-opus-4-7',
      prompt: 'Plan the next step.',
    })

    expect(request.output_config).toEqual({ effort: 'max' })
    expect(request.betas).toContain(OAUTH_BETA_HEADER)
    expect(request.betas).toContain(EFFORT_BETA_HEADER)
  })

  test('parses structured Opus advisory JSON', () => {
    const advisory = parseOrchestraAdvisory(
      JSON.stringify({
        goal: 'Implement always-on orchestration.',
        architectureNotes: ['Reuse query loop.'],
        implementationConstraints: ['Codex keeps write authority.'],
        risks: ['Avoid recursive planner calls.'],
        researchNeeds: ['Verify exact model ids.'],
        memoryCandidates: ['Keep orchestration project scoped.'],
      }),
    )

    expect(advisory.goal).toBe('Implement always-on orchestration.')
    expect(advisory.architectureNotes).toEqual(['Reuse query loop.'])
    expect(advisory.memoryCandidates).toEqual([
      'Keep orchestration project scoped.',
    ])
  })

  test('runs only for top-level non-recursive first turns', () => {
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        messages: [createUserMessage({ content: 'hello' })],
      }),
    ).toBe(true)
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        messages: [createUserMessage({ content: 'hello' })],
        settings: { orchestra: { plannerPolicy: 'risk-gated' } },
      }),
    ).toBe(false)
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        messages: [
          createUserMessage({
            content: '리서치 기반으로 아키텍처 설계하고 구현 계획을 세워줘',
          }),
        ],
      }),
    ).toBe(true)
    expect(
      shouldRunOrchestra({ ...topLevelContext, turnCount: 2 }),
    ).toBe(false)
    expect(
      shouldRunOrchestra({ ...topLevelContext, agentId: 'agent-1' }),
    ).toBe(false)
    expect(
      shouldRunOrchestra({ ...topLevelContext, querySource: 'orchestra_planner' }),
    ).toBe(false)
  })

  test('everyTurn config opens orchestra to every user turn (v0.2 always-on mode)', () => {
    // v0.2 vision: GPT 5.5 + Claude Opus must run together on EVERY turn, not just
    // turn 1. The everyTurn config knob enables this without a hard breaking
    // change — default stays false, but v0.2-locked mode flips it on.
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        turnCount: 2,
        settings: { orchestra: { everyTurn: true } },
      }),
    ).toBe(true)
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        turnCount: 7,
        settings: { orchestra: { everyTurn: true } },
      }),
    ).toBe(true)
    // everyTurn does NOT bypass agent / orchestra_planner / compact gates —
    // these have independent reasons (recursion / loops / token budget).
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        turnCount: 2,
        agentId: 'agent-1',
        settings: { orchestra: { everyTurn: true } },
      }),
    ).toBe(false)
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        turnCount: 2,
        querySource: 'orchestra_planner',
        settings: { orchestra: { everyTurn: true } },
      }),
    ).toBe(false)
    // explicit opt-out: everyTurn=false (default) keeps the legacy turn-1-only
    // behavior so non-v0.2 users see no behavior drift.
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        turnCount: 2,
        settings: { orchestra: { everyTurn: false } },
      }),
    ).toBe(false)
  })

  test('planner policy off skips Opus even for risky turns', async () => {
    let plannerCalls = 0
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: '복잡한 아키텍처 리스크를 검토하고 구현 계획을 세워줘',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: { orchestra: { plannerPolicy: 'off' } },
      planner: async () => {
        plannerCalls++
        throw new Error('should not be called')
      },
    })

    expect(plannerCalls).toBe(0)
    expect(result).toEqual({})
  })

  test('risk-gated planner skips simple top-level turns', async () => {
    let plannerCalls = 0
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [createUserMessage({ content: '안녕' })],
      systemPrompt: 'system',
      userContext: {},
      settings: { orchestra: { plannerPolicy: 'risk-gated' } },
      planner: async () => {
        plannerCalls++
        throw new Error('should not be called')
      },
    })

    expect(plannerCalls).toBe(0)
    expect(result).toEqual({})
  })

  test('returns hidden meta guidance and captures memory candidates', async () => {
    const writes: string[][] = []
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: '설계 리스크를 보고 이 아키텍처 계획을 구현해줘',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      planner: async () => ({
        goal: 'Ship the orchestrator.',
        architectureNotes: ['Inject advisory as meta context.'],
        implementationConstraints: ['Opus is read-only.'],
        risks: ['Planner recursion.'],
        researchNeeds: [],
        memoryCandidates: ['Codex remains the execution authority.'],
      }),
      persistMemoryCandidates: async ({ candidates }) => {
        writes.push(candidates)
        return { written: candidates, skipped: [] }
      },
      recordUsageEvent: () => {},
    })

    expect(result.metaMessage?.isMeta).toBe(true)
    expect(result.metaMessage?.message.content).toContain('Ship the orchestrator.')
    expect(result.diagnostic).toBeUndefined()
    expect(writes).toEqual([['Codex remains the execution authority.']])
  })

  test('fails open when planner throws', async () => {
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: 'architecture planning failure case',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      planner: async () => {
        throw new Error('auth failed')
      },
      recordUsageEvent: () => {},
    })

    expect(result.metaMessage).toBeUndefined()
    expect(result.diagnostic).toContain('auth failed')
  })

  test('adaptive planner failure policy blocks Opus rate limits instead of hiding them', async () => {
    const events: any[] = []
    const rateLimit = Object.assign(new Error('rate limited'), {
      status: 429,
      type: 'rate_limit_error',
    })

    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: 'architecture planning failure case',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      planner: async () => {
        throw rateLimit
      },
      recordUsageEvent: event => {
        events.push(event)
      },
    })

    expect(result.metaMessage).toBeUndefined()
    expect(result.diagnostic).toContain('rate limited')
    expect(result.blockingError).toContain(
      'Claude Opus (configured) planner failed',
    )
    expect(result.blockingError).toContain('rate limited')
    expect(events).toEqual([
      expect.objectContaining({
        role: 'planner',
        model: 'claude-opus-4-7',
        status: 'started',
      }),
      expect.objectContaining({
        role: 'planner',
        model: 'claude-opus-4-7',
        status: 'failed',
        errorStatus: 429,
        errorType: 'rate_limit_error',
      }),
    ])
  })

  test('warn planner failure policy surfaces a notice and continues with Codex', async () => {
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: 'architecture planning failure case',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: { orchestra: { plannerFailurePolicy: 'warn' } },
      planner: async () => {
        throw Object.assign(new Error('rate limited'), {
          status: 429,
          type: 'rate_limit_error',
        })
      },
      recordUsageEvent: () => {},
    })

    expect(result.metaMessage).toBeUndefined()
    expect(result.blockingError).toBeUndefined()
    expect(result.noticeMessage).toContain(
      'Claude Opus (configured) planner failed',
    )
  })

  test('blocks orchestra recursion from skeptic self-call', () => {
    // shouldRunOrchestra must skip when the call originates from the skeptic
    // itself (mirror of the existing 'orchestra_planner' self-block). Without
    // this, a skeptic response could re-trigger orchestra on its own output
    // and infinite-loop.
    expect(
      shouldRunOrchestra({
        ...topLevelContext,
        querySource: 'orchestra_skeptic',
        messages: [createUserMessage({ content: '아키텍처 설계' })],
      }),
    ).toBe(false)
  })

  test('skeptic dispatch yields a system message on success', async () => {
    const events: any[] = []
    const dissent: DissentReport = {
      headline: '테스트 누락',
      risks: ['의도되지 않은 DROP TABLE'],
      questionedAssumptions: [],
      scopeDrift: [],
      severity: 'caution',
    }
    const result = await buildSkepticDissent({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: '아키텍처 설계 위험을 검토해줘',
        }),
        {
          type: 'assistant',
          message: {
            content: [
              {
                type: 'text',
                text: 'Codex 응답: 아키텍처 설계 검토를 마쳤습니다 — 핵심 위험 3가지 식별',
              },
            ],
          },
        } as never,
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      skeptic: async () => dissent,
      recordUsageEvent: event => {
        events.push(event)
      },
    })
    expect(result.dissent).toEqual(dissent)
    expect(result.systemMessage).toBeDefined()
    // SystemInformationalMessage carries `content` text that should embed the
    // formatted dissent; level must derive from severity.
    expect(result.systemMessage?.content).toContain('테스트 누락')
    expect(result.systemMessage?.level).toBe('warning')
    expect(events).toEqual([
      expect.objectContaining({
        role: 'skeptic',
        model: 'claude-opus-4-7',
        status: 'started',
      }),
      expect.objectContaining({
        role: 'skeptic',
        model: 'claude-opus-4-7',
        status: 'succeeded',
      }),
    ])
  })

  test('skeptic dispatch fails open with a diagnostic when the skeptic throws', async () => {
    const events: any[] = []
    const result = await buildSkepticDissent({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: '구현 후 비판해줘 — 위험 분석 필요',
        }),
        {
          type: 'assistant',
          message: {
            content: [
              {
                type: 'text',
                text: 'Codex 응답: 구현이 완료되었으며 위험 분석을 수행하였습니다.',
              },
            ],
          },
        } as never,
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      skeptic: async () => {
        throw new Error('OAuth probe failed')
      },
      recordUsageEvent: event => {
        events.push(event)
      },
    })
    expect(result.systemMessage).toBeUndefined()
    expect(result.dissent).toBeUndefined()
    expect(result.diagnostic).toContain('OAuth probe failed')
    const failed = events.find(e => e.status === 'failed')
    expect(failed).toBeDefined()
    expect(failed.role).toBe('skeptic')
  })

  test('skeptic dispatch skips when shouldRunOrchestra would also skip', async () => {
    let calls = 0
    const result = await buildSkepticDissent({
      ...topLevelContext,
      agentId: 'sub-agent-1',
      messages: [createUserMessage({ content: 'design risks' })],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      skeptic: async () => {
        calls++
        return EMPTY_DISSENT
      },
      recordUsageEvent: () => {},
    })
    expect(calls).toBe(0)
    expect(result).toEqual({})
  })

  test('skeptic dispatch never recurses into itself', async () => {
    let calls = 0
    const result = await buildSkepticDissent({
      ...topLevelContext,
      querySource: 'orchestra_skeptic',
      messages: [createUserMessage({ content: 'design risks' })],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      skeptic: async () => {
        calls++
        return EMPTY_DISSENT
      },
      recordUsageEvent: () => {},
    })
    expect(calls).toBe(0)
    expect(result).toEqual({})
  })

  test('fails open when planner returns malformed advisory JSON', async () => {
    const result = await buildOrchestraGuidance({
      ...topLevelContext,
      messages: [
        createUserMessage({
          content: 'architecture planning malformed json case',
        }),
      ],
      systemPrompt: 'system',
      userContext: {},
      settings: {},
      planner: async () => parseOrchestraAdvisory('not json'),
      recordUsageEvent: () => {},
    })

    expect(result.metaMessage).toBeUndefined()
    expect(result.diagnostic).toContain('Orchestra planner unavailable')
  })
})
