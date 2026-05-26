import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { shouldUseClaudeAIAuth } from '../oauth/client.js'
import { EFFORT_BETA_HEADER } from '../../constants/betas.js'
import { OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { sideQuery } from '../../utils/sideQuery.js'

/**
 * Phase 2 Opus Skeptic — read-only post-implementation dissent.
 *
 * Companion to the planner in orchestrator.ts. The planner runs BEFORE Codex
 * implements; the skeptic runs AFTER, on the user-facing assistant response.
 * Same OAuth + sideQuery + forceFirstParty plumbing, different role:
 *
 *   planner   → "what should Codex do, and what risks should it watch for?"
 *   skeptic   → "what did Codex actually produce, and where is it wrong?"
 *
 * The skeptic is intentionally read-only: it never proposes edits, never sees
 * tool definitions, and its output is rendered as a separate system message
 * — it does NOT feed back into Codex's prompt (Phase 4 may revisit).
 */
export type DissentReport = {
  /** One-line headline so the user can read the verdict in 0.5s. */
  headline: string
  /** Risks Codex missed or under-weighted. */
  risks: string[]
  /** Assumptions Codex made that the skeptic challenges. */
  questionedAssumptions: string[]
  /** Parts of Codex's output that drift past the user's actual ask. */
  scopeDrift: string[]
  /** Visual weight: info=참고, caution=주의, block=명백한 결함 의심. */
  severity: DissentSeverity
}

export type DissentSeverity = 'info' | 'caution' | 'block'

export const EMPTY_DISSENT: DissentReport = {
  headline: '',
  risks: [],
  questionedAssumptions: [],
  scopeDrift: [],
  severity: 'info',
}

const VALID_SEVERITIES: ReadonlySet<DissentSeverity> = new Set([
  'info',
  'caution',
  'block',
])

const SKEPTIC_TIMEOUT_MS = 180_000
const OPUS_47_SKEPTIC_EFFORT = 'max' as const

type SkepticMessage = {
  type: string
  isMeta?: boolean
  message?: {
    content?: string | unknown[]
  }
}

type AnthropicTextBlock = { type: 'text'; text: string }

function isTextBlock(block: unknown): block is AnthropicTextBlock {
  if (typeof block !== 'object' || block === null) return false
  const candidate = block as { type?: unknown; text?: unknown }
  return candidate.type === 'text' && typeof candidate.text === 'string'
}

function extractJson(text: string): string {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  if (fenced?.[1]) return fenced[1].trim()
  return text.trim()
}

function toStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) return []
  return value.filter((item): item is string => typeof item === 'string')
}

function toStringValue(value: unknown): string {
  return typeof value === 'string' ? value : ''
}

function coerceSeverity(value: unknown): DissentSeverity {
  if (typeof value === 'string' && VALID_SEVERITIES.has(value as DissentSeverity)) {
    return value as DissentSeverity
  }
  return 'info'
}

export function parseDissentReport(text: string): DissentReport {
  const parsed = JSON.parse(extractJson(text)) as Record<string, unknown>
  return {
    headline: toStringValue(parsed.headline),
    risks: toStringArray(parsed.risks),
    questionedAssumptions: toStringArray(parsed.questionedAssumptions),
    scopeDrift: toStringArray(parsed.scopeDrift),
    severity: coerceSeverity(parsed.severity),
  }
}

function latestUserIntent(messages: SkepticMessage[]): string {
  const user = [...messages].reverse().find(m => m.type === 'user')
  const content = user?.message?.content
  return typeof content === 'string' ? content : ''
}

export function latestAssistantText(messages: SkepticMessage[]): string {
  const assistant = [...messages].reverse().find(m => m.type === 'assistant')
  const content = assistant?.message?.content
  if (typeof content === 'string') return content
  if (!Array.isArray(content)) return ''
  return content
    .filter(isTextBlock)
    .map(block => block.text)
    .join('\n')
    .slice(0, 4000)
}

const MIN_CRITIQUE_LENGTH = 30

/**
 * "Is the latest assistant message substantive enough to critique?"
 * If the GPT side only emitted tool_use blocks (no text) or returned a
 * one-word reply, calling Opus would just produce a meta-essay about the
 * absence of content. That helps nobody and noise-spams stderr. Returning
 * false here lets buildSkepticDissent short-circuit before the OAuth call.
 */
export function hasCritiqueWorthyAssistantText(
  messages: SkepticMessage[],
): boolean {
  return latestAssistantText(messages).trim().length >= MIN_CRITIQUE_LENGTH
}

function compactContext(messages: SkepticMessage[]): string {
  return messages
    .slice(-10)
    .map(message => {
      if (message.type === 'assistant') {
        const content = message.message?.content
        const text = (Array.isArray(content) ? content : [])
          .filter(isTextBlock)
          .map(b => b.text)
          .join('\n')
        return `assistant: ${text.slice(0, 1000)}`
      }
      if (message.type === 'user') {
        const raw = message.message?.content
        const c = Array.isArray(raw) ? '[structured user content]' : (raw ?? '')
        return `${message.isMeta ? 'meta-user' : 'user'}: ${String(c).slice(0, 1000)}`
      }
      return `${message.type}: [omitted]`
    })
    .join('\n\n')
}

export type SkepticPromptParams = {
  messages: SkepticMessage[]
  systemPrompt: string | string[]
  userContext: Record<string, string>
  /** Optional planner guidance from earlier in the same turn. */
  plannerAdvisory?: { goal?: string; risks?: string[] }
}

export function buildSkepticPrompt(params: SkepticPromptParams): string {
  const systemPrompt = Array.isArray(params.systemPrompt)
    ? params.systemPrompt.join('\n\n')
    : params.systemPrompt
  const plannerLines = params.plannerAdvisory
    ? [
        '# Earlier Planner Advisory (your own pre-implementation guidance)',
        `goal: ${params.plannerAdvisory.goal ?? ''}`,
        ...(params.plannerAdvisory.risks ?? []).map(r => `- risk: ${r}`),
        '',
      ]
    : []
  return [
    'You are Claude Opus 4.7 acting as the opposition party (야당) in an orchestra.',
    'The visible lead Codex/GPT 5.5 has just produced a response. Your role is read-only critique.',
    'You have NO tool access and MUST NOT propose code edits — only highlight risks,',
    'questioned assumptions, and scope drift. Output JSON ONLY in Korean.',
    '',
    'Return this exact JSON shape:',
    '{"headline":"","risks":[],"questionedAssumptions":[],"scopeDrift":[],"severity":"info|caution|block"}',
    '',
    'Rules:',
    '- All string values MUST be in Korean (한국어).',
    '- Use empty arrays + headline "유의미한 이견 없음" if you genuinely have no dissent.',
    '- severity: "info" = 참고, "caution" = 주의 권장, "block" = 명백한 결함 의심.',
    '- Be specific. Quote the smallest concrete fragment from the assistant response when possible.',
    '',
    '# User Intent',
    latestUserIntent(params.messages),
    '',
    '# Codex Final Response (target of critique)',
    latestAssistantText(params.messages),
    '',
    ...plannerLines,
    '# Project/System Rules',
    systemPrompt.slice(0, 4000),
    '',
    '# User Context',
    JSON.stringify(params.userContext).slice(0, 2000),
    '',
    '# Recent Conversation',
    compactContext(params.messages),
  ].join('\n')
}

export type SkepticRequest = {
  model: string
  max_tokens: number
  system: string
  betas: string[]
  messages: { role: 'user'; content: string }[]
  output_config?: { effort: 'max' }
}

export function buildClaudeLoginSkepticRequest(params: {
  model: string
  prompt: string
}): SkepticRequest {
  const betas: string[] = [OAUTH_BETA_HEADER]
  const isOpus47 = params.model.toLowerCase().includes('opus-4-7')
  const outputConfig = isOpus47
    ? { effort: OPUS_47_SKEPTIC_EFFORT }
    : undefined
  if (outputConfig) {
    betas.push(EFFORT_BETA_HEADER)
  }
  return {
    model: params.model,
    // Same reason as the planner: JSON.parse needs a complete payload, and
    // Opus-max on a contentful prompt often emits 3–5KB of dissent JSON.
    max_tokens: 8192,
    system:
      'Private orchestra skeptic (야당). read-only critique. ' +
      'You have NO tool access. Return structured JSON ONLY in Korean.',
    betas,
    messages: [{ role: 'user' as const, content: params.prompt }],
    ...(outputConfig && { output_config: outputConfig }),
  }
}

function resolveDefaultSkepticAuth(): { authToken: string } | null {
  const tokens = getClaudeAIOAuthTokens()
  if (!tokens?.accessToken || !shouldUseClaudeAIAuth(tokens.scopes)) {
    return null
  }
  return { authToken: tokens.accessToken }
}

export type CallOpusSkepticParams = {
  model: string
  prompt: string
  signal: AbortSignal
  /** Override for tests — bypass real OAuth probe. */
  authResolver?: () => { authToken: string } | null
}

export async function callOpusSkeptic(
  params: CallOpusSkepticParams,
): Promise<DissentReport> {
  if (!params.model.startsWith('claude-')) {
    throw new Error('Claude login skeptic requires a Claude model id')
  }
  const resolver = params.authResolver ?? resolveDefaultSkepticAuth
  if (!params.authResolver) {
    // Real path: refresh token before resolving. Test path with injected
    // resolver skips this so the test stays hermetic (no network probe).
    await checkAndRefreshOAuthTokenIfNeeded()
  }
  const auth = resolver()
  if (!auth) {
    throw new Error(
      'Claude login credentials are not available; run Claude login before using the Opus skeptic.',
    )
  }
  const request = buildClaudeLoginSkepticRequest({
    model: params.model,
    prompt: params.prompt,
  })
  const response = await sideQuery({
    model: request.model,
    max_tokens: request.max_tokens,
    system: request.system,
    messages: request.messages,
    // 'orchestra_skeptic' is a v0.2 internal querySource. The shouldRunOrchestra
    // gate filters it out alongside 'orchestra_planner' to prevent the skeptic
    // from triggering more orchestra work on its own response.
    querySource: 'orchestra_skeptic' as never,
    maxRetries: 0,
    signal: params.signal,
    skipSystemPromptPrefix: false,
    effort: request.output_config?.effort,
    forceFirstParty: true,
  })
  const text = response.content
    .map(block => (block.type === 'text' ? block.text : ''))
    .filter(t => t.length > 0)
    .join('\n')
  return parseDissentReport(text)
}

export function dissentSeverityToMessageLevel(
  severity: DissentSeverity,
): 'info' | 'warning' | 'error' {
  switch (severity) {
    case 'info':
      return 'info'
    case 'caution':
      return 'warning'
    case 'block':
      return 'error'
  }
}

const SKEPTIC_HEADER = '[Opus 4.7 야당]'
const EMPTY_HEADLINE_FALLBACK = '유의미한 이견 없음'

function isReportEmpty(report: DissentReport): boolean {
  return (
    report.headline.trim() === '' &&
    report.risks.length === 0 &&
    report.questionedAssumptions.length === 0 &&
    report.scopeDrift.length === 0
  )
}

function formatSection(title: string, items: string[]): string | null {
  if (items.length === 0) return null
  return [`${title}:`, ...items.map(item => `- ${item}`)].join('\n')
}

export function formatDissent(report: DissentReport): string {
  if (isReportEmpty(report)) {
    return `${SKEPTIC_HEADER} ${EMPTY_HEADLINE_FALLBACK}`
  }
  const headline = report.headline.trim() || EMPTY_HEADLINE_FALLBACK
  const sections = [
    formatSection('⚠ Risks (위험)', report.risks),
    formatSection('? Questioned Assumptions (의심되는 가정)', report.questionedAssumptions),
    formatSection('📍 Scope Drift (범위 이탈)', report.scopeDrift),
  ].filter((s): s is string => s !== null)
  return [`${SKEPTIC_HEADER} ${headline}`, '', ...sections].join('\n')
}
