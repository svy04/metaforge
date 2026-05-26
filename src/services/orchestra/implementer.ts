import type { SettingsJson } from '../../utils/settings/types.js'
import {
  DEFAULT_CODEX_BASE_URL,
  resolveRuntimeCodexCredentials,
  type ResolvedCodexCredentials,
} from '../api/providerConfig.js'
import {
  resolveOrchestraSettings,
  type OrchestraWorkerPolicy,
} from './config.js'
import { resolveOrchestraModelAlias } from './modelAliases.js'

type ProviderOverride = {
  model: string
  baseURL: string
  apiKey: string
}

export type CodexImplementerRoute = {
  model: string
  providerOverride: ProviderOverride
}

export type CodexImplementerRouteResult = {
  route?: CodexImplementerRoute
  diagnostic?: string
}

type ResolveCodexImplementerRouteParams = {
  settings?: Pick<SettingsJson, 'orchestra'> | null
  querySource: string
  turnCount: number
  agentId?: string
  existingProviderOverride?: ProviderOverride
  credentials?: ResolvedCodexCredentials
  env?: Record<string, string | undefined>
}

function isBlockedOrchestraRoute(params: {
  querySource: string
}): boolean {
  if (params.querySource === 'orchestra_planner') return true
  if (params.querySource === 'compact' || params.querySource === 'session_memory') {
    return true
  }
  return false
}

function isAgentWorkerTurn(params: {
  querySource: string
  agentId?: string
}): boolean {
  return Boolean(params.agentId) || params.querySource.startsWith('agent:')
}

function shouldRouteCodexImplementer(params: {
  querySource: string
  turnCount: number
  agentId?: string
  workerPolicy: OrchestraWorkerPolicy
  everyTurn: boolean
}): boolean {
  if (isBlockedOrchestraRoute(params)) return false
  if (isAgentWorkerTurn(params)) {
    return params.workerPolicy === 'codex-first'
  }
  if (params.turnCount !== 1 && !params.everyTurn) return false
  return true
}

function normalizeCodexRequestModel(model: string, source: string): string {
  const trimmed = model.trim()
  if (source === 'fallback' && trimmed.toLowerCase() === 'gpt-5.5') {
    return 'codexplan'
  }
  return trimmed
}

function runtimeModelForCodexRequest(model: string): string {
  const base = model.trim().toLowerCase().split('?', 1)[0] ?? model
  if (base === 'codexplan') return 'gpt-5.5'
  if (base === 'codexspark') return 'gpt-5.3-codex-spark'
  return model.trim()
}

export function resolveCodexImplementerRoute(
  params: ResolveCodexImplementerRouteParams,
): CodexImplementerRouteResult {
  const settings = resolveOrchestraSettings(params.settings)
  if (!settings.enabled || settings.lead !== 'codex') {
    return {}
  }
  if (
    !shouldRouteCodexImplementer({
      ...params,
      workerPolicy: settings.workerPolicy,
      everyTurn: settings.everyTurn,
    })
  ) {
    return {}
  }
  if (params.existingProviderOverride) {
    return {
      diagnostic:
        'orchestra codex implementer skipped; existing provider override is configured.',
    }
  }

  const credentials =
    params.credentials ?? resolveRuntimeCodexCredentials({ env: process.env })
  if (!credentials.apiKey) {
    const authPath = credentials.authPath ? ` at ${credentials.authPath}` : ''
    return {
      diagnostic:
        `orchestra codex implementer unavailable; missing Codex auth${authPath}. ` +
        'Continuing with the current model.',
    }
  }
  if (!credentials.accountId) {
    return {
      diagnostic:
        'orchestra codex implementer unavailable; missing chatgpt_account_id. ' +
        'Continuing with the current model.',
    }
  }

  const resolution = resolveOrchestraModelAlias('implementer', {
    settings: params.settings,
    env: params.env,
    apiProvider: 'codex',
  })
  const requestModel = normalizeCodexRequestModel(
    resolution.model,
    resolution.source,
  )
  const runtimeModel = runtimeModelForCodexRequest(requestModel)

  return {
    route: {
      model: runtimeModel,
      providerOverride: {
        model: requestModel,
        baseURL: DEFAULT_CODEX_BASE_URL,
        apiKey: '',
      },
    },
    diagnostic:
      `orchestra codex implementer active: ${resolution.displayAlias} -> ` +
      `${requestModel} (${runtimeModel}) via ${DEFAULT_CODEX_BASE_URL}.`,
  }
}
