import { CLAUDE_OPUS_4_7_CONFIG } from '../../utils/model/configs.js'
import { getAPIProvider, type APIProvider } from '../../utils/model/providers.js'
import type { SettingsJson } from '../../utils/settings/types.js'
import {
  CODEX_GPT_55_ALIAS,
  CLAUDE_OPUS_47_ALIAS,
  resolveOrchestraSettings,
} from './config.js'

export { CODEX_GPT_55_ALIAS, CLAUDE_OPUS_47_ALIAS }

export type OrchestraRole = 'planner' | 'implementer'

export type OrchestraModelResolution = {
  role: OrchestraRole
  displayAlias: string
  model: string
  source: 'settings' | 'env' | 'fallback'
  diagnostic?: string
}

type ResolverEnv = Record<string, string | undefined>

const ROLE_ENV_KEYS: Record<OrchestraRole, readonly string[]> = {
  planner: [
    'OPENCLAUDE_ORCHESTRA_PLANNER_MODEL',
    'OPENCLAUDE_ORCHESTRA_OPUS_MODEL',
  ],
  implementer: [
    'OPENCLAUDE_ORCHESTRA_IMPLEMENTER_MODEL',
    'OPENCLAUDE_ORCHESTRA_CODEX_MODEL',
  ],
}

function trim(value: string | undefined): string | undefined {
  const trimmed = value?.trim()
  return trimmed ? trimmed : undefined
}

function envModel(role: OrchestraRole, env: ResolverEnv): string | undefined {
  for (const key of ROLE_ENV_KEYS[role]) {
    const value = trim(env[key])
    if (value) return value
  }
  return undefined
}

function fallbackModel(role: OrchestraRole, _provider: APIProvider): string {
  if (role === 'implementer') {
    return 'gpt-5.5'
  }
  // Orchestra planner uses callClaudeLoginPlanner (Claude OAuth), which
  // rejects any non-claude model id. The cross-provider translation in
  // CLAUDE_OPUS_4_7_CONFIG (e.g. openai → 'gpt-4o') exists for the main
  // loop's model substitution and must NOT apply here, otherwise an OpenAI
  // user's planner gets fallback 'gpt-4o' which the OAuth call site refuses.
  return CLAUDE_OPUS_4_7_CONFIG.firstParty
}

export function resolveOrchestraModelAlias(
  role: OrchestraRole,
  options: {
    settings?: Pick<SettingsJson, 'orchestra'> | null
    env?: ResolverEnv
    apiProvider?: APIProvider
  } = {},
): OrchestraModelResolution {
  const env = options.env ?? process.env
  const apiProvider = options.apiProvider ?? getAPIProvider()
  const orchestra = resolveOrchestraSettings(options.settings)
  const displayAlias =
    role === 'planner'
      ? CLAUDE_OPUS_47_ALIAS
      : CODEX_GPT_55_ALIAS
  const explicitSetting = trim(orchestra.models[role])
  if (explicitSetting) {
    return {
      role,
      displayAlias,
      model: explicitSetting,
      source: 'settings',
    }
  }

  const explicitEnv = envModel(role, env)
  if (explicitEnv) {
    return {
      role,
      displayAlias,
      model: explicitEnv,
      source: 'env',
    }
  }

  const model = fallbackModel(role, apiProvider)
  return {
    role,
    displayAlias,
    model,
    source: 'fallback',
    diagnostic:
      `${displayAlias} has no explicit model id configured; ` +
      `using repo-supported fallback ${model}.`,
  }
}
