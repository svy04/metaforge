import { describe, expect, test } from 'bun:test'

import { EFFORT_BETA_HEADER } from '../../constants/betas.js'
import { OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { createUserMessage } from '../../utils/messages.js'
import {
  buildClaudeLoginSkepticRequest,
  buildSkepticPrompt,
  callOpusSkeptic,
  dissentSeverityToMessageLevel,
  EMPTY_DISSENT,
  formatDissent,
  parseDissentReport,
  type DissentReport,
} from './skeptic.js'

describe('orchestra skeptic — DissentReport parser', () => {
  test('parses well-formed Korean dissent JSON', () => {
    const report = parseDissentReport(
      JSON.stringify({
        headline: 'GPT 답변에 데이터 손실 위험',
        risks: ['DROP TABLE이 백업 없이 실행됨'],
        questionedAssumptions: ['idempotent하다는 가정이 검증 안 됨'],
        scopeDrift: ['요청은 SELECT였는데 DROP까지 진행'],
        severity: 'block',
      }),
    )
    expect(report.headline).toBe('GPT 답변에 데이터 손실 위험')
    expect(report.risks).toEqual(['DROP TABLE이 백업 없이 실행됨'])
    expect(report.questionedAssumptions).toEqual([
      'idempotent하다는 가정이 검증 안 됨',
    ])
    expect(report.scopeDrift).toEqual(['요청은 SELECT였는데 DROP까지 진행'])
    expect(report.severity).toBe('block')
  })

  test('parses fenced JSON output', () => {
    const report = parseDissentReport(
      '```json\n{"headline":"x","risks":[],"questionedAssumptions":[],"scopeDrift":[],"severity":"caution"}\n```',
    )
    expect(report.headline).toBe('x')
    expect(report.severity).toBe('caution')
  })

  test('falls back to info severity when invalid', () => {
    const report = parseDissentReport(
      JSON.stringify({
        headline: 'h',
        risks: [],
        questionedAssumptions: [],
        scopeDrift: [],
        severity: 'totally-invalid',
      }),
    )
    expect(report.severity).toBe('info')
  })

  test('coerces missing fields to empty arrays / empty headline', () => {
    const report = parseDissentReport(JSON.stringify({}))
    expect(report).toEqual(EMPTY_DISSENT)
  })

  test('throws on non-JSON garbage', () => {
    expect(() => parseDissentReport('not json at all')).toThrow()
  })
})

describe('orchestra skeptic — prompt builder', () => {
  const baseParams = {
    messages: [
      createUserMessage({ content: '데이터베이스를 SELECT 한번만 해줘' }),
      {
        type: 'assistant' as const,
        message: {
          content: [
            { type: 'text' as const, text: 'OK 진행하겠습니다. 그리고 DROP TABLE도 실행했습니다.' },
          ],
        },
      },
    ],
    systemPrompt: 'system instructions',
    userContext: { cwd: '/tmp' },
  }

  test('marks itself read-only and 야당 in Korean', () => {
    const prompt = buildSkepticPrompt(baseParams)
    expect(prompt).toContain('read-only')
    expect(prompt).toContain('야당')
    expect(prompt.toLowerCase()).toContain('korean')
  })

  test('embeds the latest assistant response so skeptic can critique it', () => {
    const prompt = buildSkepticPrompt(baseParams)
    expect(prompt).toContain('DROP TABLE도 실행했습니다')
  })

  test('embeds the latest user intent', () => {
    const prompt = buildSkepticPrompt(baseParams)
    expect(prompt).toContain('SELECT 한번만')
  })
})

describe('orchestra skeptic — Claude login request shape', () => {
  test('opus-4-7 request uses max effort and OAuth + effort betas', () => {
    const request = buildClaudeLoginSkepticRequest({
      model: 'claude-opus-4-7',
      prompt: 'critique this',
    })
    expect(request.model).toBe('claude-opus-4-7')
    expect(request.system).toContain('read-only')
    expect(request.system).toContain('JSON')
    expect(request.betas).toContain(OAUTH_BETA_HEADER)
    expect(request.betas).toContain(EFFORT_BETA_HEADER)
    expect(request.output_config).toEqual({ effort: 'max' })
    expect(request.messages[0]?.role).toBe('user')
    expect(request.messages[0]?.content).toBe('critique this')
  })

  test('non-opus model omits effort beta and output_config', () => {
    const request = buildClaudeLoginSkepticRequest({
      model: 'claude-sonnet-4-6',
      prompt: 'critique',
    })
    expect(request.betas).toContain(OAUTH_BETA_HEADER)
    expect(request.betas).not.toContain(EFFORT_BETA_HEADER)
    expect(request.output_config).toBeUndefined()
  })
})

describe('orchestra skeptic — callOpusSkeptic dispatch', () => {
  test('rejects non-Claude model ids before any side-effect', async () => {
    await expect(
      callOpusSkeptic({
        model: 'gpt-5.5',
        prompt: 'p',
        signal: new AbortController().signal,
      }),
    ).rejects.toThrow(/Claude login skeptic requires a Claude model/i)
  })

  test('throws clear error when OAuth credentials missing', async () => {
    // Inject a null auth resolver to simulate "no Claude login token" in a
    // way that's robust to whatever the host machine has in process.env or
    // ~/.claude/.credentials.json. Production path still uses the default
    // resolveClaudeLoginPlannerAuth() helper.
    await expect(
      callOpusSkeptic({
        model: 'claude-opus-4-7',
        prompt: 'p',
        signal: new AbortController().signal,
        authResolver: () => null,
      }),
    ).rejects.toThrow(/Claude login credentials/i)
  })
})

describe('orchestra skeptic — formatDissent display', () => {
  test('emits header and labelled sections in Korean for non-empty dissent', () => {
    const report: DissentReport = {
      headline: '테스트 누락',
      risks: ['오류 처리 없음'],
      questionedAssumptions: ['idempotent 가정'],
      scopeDrift: [],
      severity: 'caution',
    }
    const text = formatDissent(report)
    expect(text).toContain('[Opus 4.7 야당]')
    expect(text).toContain('테스트 누락')
    expect(text).toContain('오류 처리 없음')
    expect(text).toContain('idempotent 가정')
    // Empty section should not appear.
    expect(text).not.toMatch(/Scope Drift|범위 이탈/)
  })

  test('compresses fully empty dissent into a single advisory line', () => {
    const text = formatDissent(EMPTY_DISSENT)
    expect(text).toContain('[Opus 4.7 야당]')
    expect(text.split('\n').length).toBeLessThanOrEqual(2)
  })
})

describe('orchestra skeptic — severity → message level mapping', () => {
  test('info → info, caution → warning, block → error', () => {
    expect(dissentSeverityToMessageLevel('info')).toBe('info')
    expect(dissentSeverityToMessageLevel('caution')).toBe('warning')
    expect(dissentSeverityToMessageLevel('block')).toBe('error')
  })
})
