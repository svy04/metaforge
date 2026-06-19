import type { SettingsJson } from '../../utils/settings/types.js'
import { getInitialSettings } from '../../utils/settings/settings.js'
import {
  createSystemMessage,
  createUserMessage,
  type SystemInformationalMessage,
} from '../../utils/messages.js'
import type { SystemPrompt } from '../../utils/systemPromptType.js'
import { logForDebugging } from '../../utils/debug.js'
import {
  checkAndRefreshOAuthTokenIfNeeded,
  getClaudeAIOAuthTokens,
} from '../../utils/auth.js'
import { shouldUseClaudeAIAuth } from '../oauth/client.js'
import { EFFORT_BETA_HEADER } from '../../constants/betas.js'
import { OAUTH_BETA_HEADER } from '../../constants/oauth.js'
import { sideQuery } from '../../utils/sideQuery.js'
import type { ToolUseContext } from '../../Tool.js'
import {
  CLAUDE_OPUS_ALIAS,
  resolveOrchestraSettings,
  type OrchestraPlannerFailurePolicy,
  type OrchestraPlannerPolicy,
} from './config.js'
import { resolveOrchestraModelAlias } from './modelAliases.js'
import {
  persistProjectMemoryCandidates,
  type PersistMemoryCandidatesParams,
  type PersistMemoryCandidatesResult,
} from './memory.js'
import {
  recordOrchestraUsageEvent,
  type OrchestraUsageEvent,
  type OrchestraUsageRecorder,
} from './usageLog.js'
import {
  buildSkepticPrompt,
  callOpusSkeptic,
  dissentSeverityToMessageLevel,
  formatDissent,
  hasCritiqueWorthyAssistantText,
  type DissentReport,
} from './skeptic.js'

export type OrchestraAdvisory = {
  goal: string
  architectureNotes: string[]
  implementationConstraints: string[]
  risks: string[]
  researchNeeds: string[]
  memoryCandidates: string[]
}

export type OrchestraGuidanceResult = {
  metaMessage?: ReturnType<typeof createUserMessage>
  diagnostic?: string
  noticeMessage?: string
  blockingError?: string
}

type OrchestraMessage = {
  type: string
  isMeta?: boolean
  message?: {
    content?: string | unknown[]
  }
}

type PlannerParams = {
  messages: OrchestraMessage[]
  systemPrompt: SystemPrompt | string
  userContext: Record<string, string>
  settings: Pick<SettingsJson, 'orchestra'> | null | undefined
  signal?: AbortSignal
  toolUseContext?: ToolUseContext
  claudeLoginPlanner?: ClaudeLoginPlanner
}

type ClaudeLoginPlanner = (params: {
  model: string
  prompt: string
  signal: AbortSignal
}) => Promise<OrchestraAdvisory>

export type OrchestraPlanner = (
  params: PlannerParams,
) => Promise<OrchestraAdvisory>

export type BuildOrchestraGuidanceParams = PlannerParams & {
  querySource: string
  turnCount: number
  agentId?: string
  planner?: OrchestraPlanner
  persistMemoryCandidates?: (
    params: PersistMemoryCandidatesParams,
  ) => Promise<PersistMemoryCandidatesResult>
  recordUsageEvent?: OrchestraUsageRecorder
}

const EMPTY_ADVISORY: OrchestraAdvisory = {
  goal: '',
  architectureNotes: [],
  implementationConstraints: [],
  risks: [],
  researchNeeds: [],
  memoryCandidates: [],
}

const PLANNER_TIMEOUT_MS = 180_000
const OPUS_47_PLANNER_EFFORT = 'max' as const

type PlannerFailureKind = 'rate_limit' | 'auth' | 'availability' | 'unknown'

function toStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) return []
  return value.filter((item): item is string => typeof item === 'string')
}

function toStringValue(value: unknown): string {
  return typeof value === 'string' ? value : ''
}

function extractJson(text: string): string {
  const fenced = text.match(/```(?:json)?\s*([\s\S]*?)```/i)
  if (fenced?.[1]) return fenced[1].trim()
  return text.trim()
}

function isTextBlock(block: unknown): block is { type: 'text'; text: string } {
  if (typeof block !== 'object' || block === null) return false
  const candidate = block as { type?: unknown; text?: unknown }
  return candidate.type === 'text' && typeof candidate.text === 'string'
}

export function parseOrchestraAdvisory(text: string): OrchestraAdvisory {
  const parsed = JSON.parse(extractJson(text)) as Record<string, unknown>
  return {
    ...EMPTY_ADVISORY,
    goal: toStringValue(parsed.goal),
    architectureNotes: toStringArray(parsed.architectureNotes),
    implementationConstraints: toStringArray(parsed.implementationConstraints),
    risks: toStringArray(parsed.risks),
    researchNeeds: toStringArray(parsed.researchNeeds),
    memoryCandidates: toStringArray(parsed.memoryCandidates),
  }
}

export function shouldRunOrchestra({
  querySource,
  turnCount,
  agentId,
  settings,
  messages = [],
}: {
  querySource: string
  turnCount: number
  agentId?: string
  settings?: Pick<SettingsJson, 'orchestra'> | null
  messages?: OrchestraMessage[]
}): boolean {
  const orchestra = resolveOrchestraSettings(settings)
  if (!orchestra.enabled) return false
  // v0.2 always-on mode: when everyTurn is true the orchestra runs on every
  // user turn, not only turn 1. Other recursion / loop / token gates below
  // still apply — agent subturns, orchestra_planner self-recursion, compact,
  // and session_memory must remain blocked regardless of everyTurn.
  if (turnCount !== 1 && !orchestra.everyTurn) return false
  if (agentId) return false
  if (querySource === 'orchestra_planner') return false
  // v0.2 Phase 2: skeptic must not retrigger orchestra on its own dissent
  // response. Same self-block reason as the planner — recursion prevention.
  if (querySource === 'orchestra_skeptic') return false
  if (querySource === 'compact' || querySource === 'session_memory') return false
  if (querySource.startsWith('agent:')) return false
  if (orchestra.plannerPolicy === 'off') return false
  if (orchestra.plannerPolicy === 'always') return true
  return isRiskGatedPlannerTurn(messages)
}

function plannerSignal(parent?: AbortSignal): AbortSignal {
  if (parent?.aborted) return parent
  const timeout = AbortSignal.timeout(PLANNER_TIMEOUT_MS)
  return parent ? AbortSignal.any([parent, timeout]) : timeout
}

function latestUserIntent(messages: OrchestraMessage[]): string {
  const user = [...messages].reverse().find(message => message.type === 'user')
  const content = user?.message?.content
  return typeof content === 'string' ? content : ''
}

const RISK_GATED_PLANNER_MARKERS = [
  'architecture',
  'architect',
  'orchestr',
  'planner',
  'planning',
  'design',
  'research',
  'paper',
  'patent',
  'framework',
  'open-source',
  'opensource',
  'implementation plan',
  'refactor',
  'migration',
  'risk',
  'security',
  'failure',
  'failing',
  'error',
  'bug',
  'test',
  'build',
  'hook',
  'worktree',
  'agent',
  'subagent',
  'memory',
  'token',
  'model',
  'routing',
  'provider',
  '설계',
  '구조',
  '아키텍처',
  '기획',
  '계획',
  '리서치',
  '연구',
  '논문',
  '특허',
  '프레임워크',
  '오픈소스',
  '구현',
  '수정',
  '조치',
  '해결',
  '위험',
  '리스크',
  '오류',
  '실패',
  '테스트',
  '빌드',
  '훅',
  '에이전트',
  '메모리',
  '토큰',
  '모델',
  '라우팅',
]

function isRiskGatedPlannerTurn(messages: OrchestraMessage[]): boolean {
  const intent = latestUserIntent(messages).trim()
  if (!intent) return false
  if (intent.length > 1500) return true
  const normalized = intent.toLowerCase()
  return RISK_GATED_PLANNER_MARKERS.some(marker =>
    normalized.includes(marker),
  )
}

function compactContext(messages: OrchestraMessage[]): string {
  return messages
    .slice(-12)
    .map(message => {
      if (message.type === 'assistant') {
        const content = message.message?.content
        const text = (Array.isArray(content) ? content : [])
          .filter(isTextBlock)
          .map(block => block.text)
          .join('\n')
        return `assistant: ${text.slice(0, 1200)}`
      }
      if (message.type === 'user') {
        const rawContent = message.message?.content
        const content = Array.isArray(rawContent)
          ? '[structured user content]'
          : (rawContent ?? '')
        return `${message.isMeta ? 'meta-user' : 'user'}: ${content.slice(0, 1200)}`
      }
      return `${message.type}: [omitted]`
    })
    .join('\n\n')
}

function buildPlannerPrompt(params: PlannerParams): string {
  const systemPrompt = Array.isArray(params.systemPrompt)
    ? params.systemPrompt.join('\n\n')
    : params.systemPrompt
  return [
    'You are Claude Opus acting as a private planning, architecture, and critique partner for Codex.',
    'Codex is the visible lead and the only writer/executor. You must return JSON only.',
    '',
    'Return this exact JSON shape:',
    '{"goal":"","architectureNotes":[],"implementationConstraints":[],"risks":[],"researchNeeds":[],"memoryCandidates":[]}',
    '',
    '# User Intent',
    latestUserIntent(params.messages),
    '',
    '# Project/System Rules',
    systemPrompt.slice(0, 6000),
    '',
    '# User Context',
    JSON.stringify(params.userContext).slice(0, 3000),
    '',
    '# Recent Context',
    compactContext(params.messages),
  ].join('\n')
}

export function resolveClaudeLoginPlannerAuth(
  tokens = getClaudeAIOAuthTokens(),
): { authToken: string } | null {
  if (!tokens?.accessToken || !shouldUseClaudeAIAuth(tokens.scopes)) {
    return null
  }
  return { authToken: tokens.accessToken }
}

export function buildClaudeLoginPlannerRequest(params: {
  model: string
  prompt: string
}) {
  const betas: string[] = [OAUTH_BETA_HEADER]
  const outputConfig = params.model.toLowerCase().includes('opus-4-7')
    ? { effort: OPUS_47_PLANNER_EFFORT }
    : undefined

  if (outputConfig) {
    betas.push(EFFORT_BETA_HEADER)
  }

  return {
    model: params.model,
    // max_tokens caps the JSON output, NOT thinking. Opus on max effort with
    // a long-ish prompt routinely emits 3–6KB of structured JSON; the old
    // 2048 cap would cut a response mid-string and crash JSON.parse with
    // "Unterminated string". 8192 leaves a comfortable margin.
    max_tokens: 8192,
    system:
      'Private orchestra planner. Return structured JSON only. Do not use tools.',
    betas,
    messages: [{ role: 'user' as const, content: params.prompt }],
    ...(outputConfig && { output_config: outputConfig }),
  }
}

async function callClaudeLoginPlanner(
  params: Parameters<ClaudeLoginPlanner>[0],
): Promise<OrchestraAdvisory> {
  if (!params.model.startsWith('claude-')) {
    throw new Error('Claude login planner requires a Claude model id')
  }
  await checkAndRefreshOAuthTokenIfNeeded()
  const auth = resolveClaudeLoginPlannerAuth()
  if (!auth) {
    throw new Error(
      'Claude login credentials are not available; run Claude login before using the Opus planner.',
    )
  }
  const request = buildClaudeLoginPlannerRequest(params)
  const response = await sideQuery({
    model: request.model,
    max_tokens: request.max_tokens,
    system: request.system,
    messages: request.messages,
    querySource: 'orchestra_planner' as any,
    maxRetries: 0,
    signal: params.signal,
    skipSystemPromptPrefix: false,
    effort: request.output_config?.effort,
    // Orchestra planner is Claude-OAuth-only. Bypass user-primary-provider
    // routing so an OpenAI/Codex/Gemini-default user still reaches Anthropic
    // for the planner call instead of getting silently shimmed to OpenAI.
    forceFirstParty: true,
  })
  const text = response.content
    .map(block => (block.type === 'text' ? block.text : ''))
    .filter(text => text.length > 0)
    .join('\n')
  return parseOrchestraAdvisory(text)
}

export async function callOpusPlanner(
  params: PlannerParams,
): Promise<OrchestraAdvisory> {
  const resolution = resolveOrchestraModelAlias('planner', {
    settings: params.settings,
  })
  if (resolution.diagnostic) {
    logForDebugging(resolution.diagnostic)
  }
  const signal = plannerSignal(params.signal)
  const prompt = buildPlannerPrompt(params)
  const planner =
    'claudeLoginPlanner' in params && params.claudeLoginPlanner
      ? params.claudeLoginPlanner
      : callClaudeLoginPlanner
  return await planner({
    model: resolution.model,
    prompt,
    signal,
  })
}

function formatList(title: string, items: string[]): string {
  if (items.length === 0) return ''
  return [`${title}:`, ...items.map(item => `- ${item}`)].join('\n')
}

export function formatOrchestraMeta(advisory: OrchestraAdvisory): string {
  return [
    '<orchestra-advisory source="Claude Opus (configured)" visibility="hidden">',
    'Use this as private planning guidance. Codex remains the only execution and write authority.',
    '',
    `Goal: ${advisory.goal}`,
    formatList('Architecture Notes', advisory.architectureNotes),
    formatList('Implementation Constraints', advisory.implementationConstraints),
    formatList('Risks', advisory.risks),
    formatList('Research Needs', advisory.researchNeeds),
    '</orchestra-advisory>',
  ]
    .filter(Boolean)
    .join('\n')
}

function plannerFailureKind(error: unknown, message: string): PlannerFailureKind {
  const candidate = error as {
    type?: unknown
    status?: unknown
    code?: unknown
  }
  const status =
    typeof candidate?.status === 'number'
      ? candidate.status
      : typeof candidate?.status === 'string'
        ? Number.parseInt(candidate.status, 10)
        : undefined
  const normalized = [
    message,
    typeof candidate?.type === 'string' ? candidate.type : '',
    typeof candidate?.code === 'string' ? candidate.code : '',
  ]
    .join(' ')
    .toLowerCase()

  if (status === 429 || normalized.includes('rate_limit')) {
    return 'rate_limit'
  }
  if (
    status === 401 ||
    status === 403 ||
    normalized.includes('auth') ||
    normalized.includes('credential') ||
    normalized.includes('login')
  ) {
    return 'auth'
  }
  if (
    (typeof status === 'number' && status >= 500) ||
    normalized.includes('overload') ||
    normalized.includes('unavailable') ||
    normalized.includes('timeout')
  ) {
    return 'availability'
  }
  return 'unknown'
}

function shouldBlockPlannerFailure({
  kind,
  plannerPolicy,
  plannerFailurePolicy,
}: {
  kind: PlannerFailureKind
  plannerPolicy: OrchestraPlannerPolicy
  plannerFailurePolicy: OrchestraPlannerFailurePolicy
}): boolean {
  if (plannerFailurePolicy === 'block') return true
  if (plannerFailurePolicy === 'warn') return false
  return plannerPolicy === 'always' && kind !== 'unknown'
}

function formatPlannerFailureMessage(params: {
  model: string
  kind: PlannerFailureKind
  message: string
}): string {
  return (
    `${CLAUDE_OPUS_ALIAS} planner failed before implementation guidance was available ` +
    `(${params.model}, ${params.kind}): ${params.message}`
  )
}

export async function buildOrchestraGuidance({
  planner = callOpusPlanner,
  persistMemoryCandidates = persistProjectMemoryCandidates,
  recordUsageEvent = recordOrchestraUsageEvent,
  ...params
}: BuildOrchestraGuidanceParams): Promise<OrchestraGuidanceResult> {
  const settings = resolveOrchestraSettings(params.settings)
  if (!settings.enabled) return {}
  if (
    !shouldRunOrchestra({
      querySource: params.querySource,
      turnCount: params.turnCount,
      agentId: params.agentId,
      settings: params.settings,
      messages: params.messages,
    })
  ) {
    return {}
  }
  const plannerResolution = resolveOrchestraModelAlias('planner', {
    settings: params.settings,
  })
  const baseUsageEvent = {
    role: 'planner' as const,
    model: plannerResolution.model,
    querySource: params.querySource,
    turnCount: params.turnCount,
  }

  try {
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'started',
    })
    const advisory = await planner(params)
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'succeeded',
    })
    if (advisory.memoryCandidates.length > 0) {
      await persistMemoryCandidates({
        candidates: advisory.memoryCandidates,
        memoryScope: settings.memoryScope,
      })
    }
    return {
      metaMessage: createUserMessage({
        content: formatOrchestraMeta(advisory),
        isMeta: true,
      }),
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    const kind = plannerFailureKind(error, message)
    const plannerFailureMessage = formatPlannerFailureMessage({
      model: plannerResolution.model,
      kind,
      message,
    })
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'failed',
      ...orchestraErrorMetadata(error),
    })
    const diagnostic = `Orchestra planner unavailable; continuing with Codex only: ${message}`
    const blockingError = shouldBlockPlannerFailure({
      kind,
      plannerPolicy: settings.plannerPolicy,
      plannerFailurePolicy: settings.plannerFailurePolicy,
    })
      ? plannerFailureMessage
      : undefined
    return {
      diagnostic,
      noticeMessage: plannerFailureMessage,
      ...(blockingError && { blockingError }),
    }
  }
}

function orchestraErrorMetadata(error: unknown): Partial<OrchestraUsageEvent> {
  const candidate = error as {
    name?: unknown
    type?: unknown
    status?: unknown
    code?: unknown
    message?: unknown
  }
  const errorMessage =
    typeof candidate?.message === 'string'
      ? candidate.message.replace(/\s+/g, ' ').slice(0, 300)
      : undefined

  return {
    errorName:
      typeof candidate?.name === 'string'
        ? candidate.name
        : error instanceof Error
          ? error.name
          : undefined,
    errorType: typeof candidate?.type === 'string' ? candidate.type : undefined,
    errorStatus:
      typeof candidate?.status === 'number' ||
      typeof candidate?.status === 'string'
        ? candidate.status
        : undefined,
    errorCode: typeof candidate?.code === 'string' ? candidate.code : undefined,
    ...(errorMessage && { errorMessage }),
  }
}

async function safeRecordUsageEvent(
  recorder: OrchestraUsageRecorder,
  event: OrchestraUsageEvent,
): Promise<void> {
  try {
    await recorder(event)
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    logForDebugging(`orchestra usage recorder failed: ${message}`, {
      level: 'warn',
    })
  }
}

export async function createOrchestraGuidance(params: {
  messages: OrchestraMessage[]
  systemPrompt: SystemPrompt
  userContext: Record<string, string>
  querySource: string
  turnCount: number
  toolUseContext: ToolUseContext
  signal?: AbortSignal
}): Promise<OrchestraGuidanceResult> {
  const settings =
    params.toolUseContext.getAppState().settings ?? getInitialSettings()
  return buildOrchestraGuidance({
    messages: params.messages,
    systemPrompt: params.systemPrompt,
    userContext: params.userContext,
    querySource: params.querySource,
    turnCount: params.turnCount,
    agentId: params.toolUseContext.agentId,
    settings,
    signal: params.signal,
    toolUseContext: params.toolUseContext,
  })
}

// ---------------------------------------------------------------------------
// v0.2 Phase 2 — Opus Skeptic (post-implementation dissent)
//
// Mirror of buildOrchestraGuidance but for the AFTER-Codex critique role.
// Same OAuth + sideQuery + forceFirstParty plumbing, different role,
// different output: a SystemInformationalMessage rendered to the user
// in addition to (not in place of) the Codex final response.
// ---------------------------------------------------------------------------

export type SkepticDispatchResult = {
  dissent?: DissentReport
  systemMessage?: SystemInformationalMessage
  diagnostic?: string
}

type SkepticFn = (params: {
  model: string
  prompt: string
  signal: AbortSignal
}) => Promise<DissentReport>

export type BuildSkepticDispatchParams = PlannerParams & {
  querySource: string
  turnCount: number
  agentId?: string
  /** Optional planner advisory captured earlier in the same turn. */
  plannerAdvisory?: OrchestraAdvisory
  skeptic?: SkepticFn
  recordUsageEvent?: OrchestraUsageRecorder
}

export async function buildSkepticDissent({
  skeptic = callOpusSkeptic,
  recordUsageEvent = recordOrchestraUsageEvent,
  ...params
}: BuildSkepticDispatchParams): Promise<SkepticDispatchResult> {
  const settings = resolveOrchestraSettings(params.settings)
  if (!settings.enabled) return {}
  if (
    !shouldRunOrchestra({
      querySource: params.querySource,
      turnCount: params.turnCount,
      agentId: params.agentId,
      settings: params.settings,
      messages: params.messages,
    })
  ) {
    return {}
  }
  // If the latest assistant message has no substantive text (e.g. the GPT
  // side only emitted tool_use blocks, or a one-word reply), there is
  // nothing for the opposition to critique. Calling Opus here would only
  // produce a meta-dissent about the absence of content, which is pure
  // stderr noise. Skip silently — the next turn that DOES yield an
  // assistant reply will fire the skeptic normally.
  if (!hasCritiqueWorthyAssistantText(params.messages)) {
    return {}
  }
  // Skeptic uses the same configured Claude Opus path as the planner — same model
  // resolution alias keeps env / settings overrides consistent across roles.
  const skepticResolution = resolveOrchestraModelAlias('planner', {
    settings: params.settings,
  })
  const baseUsageEvent = {
    role: 'skeptic' as const,
    model: skepticResolution.model,
    querySource: params.querySource,
    turnCount: params.turnCount,
  }
  const signal = plannerSignal(params.signal)
  const prompt = buildSkepticPrompt({
    messages: params.messages,
    systemPrompt: Array.isArray(params.systemPrompt)
      ? Array.from(params.systemPrompt as readonly string[])
      : (params.systemPrompt as string),
    userContext: params.userContext,
    plannerAdvisory: params.plannerAdvisory
      ? {
          goal: params.plannerAdvisory.goal,
          risks: params.plannerAdvisory.risks,
        }
      : undefined,
  })

  try {
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'started',
    })
    const dissent = await skeptic({
      model: skepticResolution.model,
      prompt,
      signal,
    })
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'succeeded',
    })
    const formatted = formatDissent(dissent)
    const level = dissentSeverityToMessageLevel(dissent.severity)
    return {
      dissent,
      systemMessage: createSystemMessage(formatted, level),
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error)
    await safeRecordUsageEvent(recordUsageEvent, {
      ...baseUsageEvent,
      status: 'failed',
      ...orchestraErrorMetadata(error),
    })
    return {
      diagnostic: `Orchestra skeptic unavailable; continuing without dissent: ${message}`,
    }
  }
}

export async function createOrchestraSkepticDissent(params: {
  messages: OrchestraMessage[]
  systemPrompt: SystemPrompt
  userContext: Record<string, string>
  querySource: string
  turnCount: number
  toolUseContext: ToolUseContext
  signal?: AbortSignal
  plannerAdvisory?: OrchestraAdvisory
}): Promise<SkepticDispatchResult> {
  const settings =
    params.toolUseContext.getAppState().settings ?? getInitialSettings()
  return buildSkepticDissent({
    messages: params.messages,
    systemPrompt: params.systemPrompt,
    userContext: params.userContext,
    querySource: params.querySource,
    turnCount: params.turnCount,
    agentId: params.toolUseContext.agentId,
    settings,
    signal: params.signal,
    toolUseContext: params.toolUseContext,
    plannerAdvisory: params.plannerAdvisory,
  })
}
