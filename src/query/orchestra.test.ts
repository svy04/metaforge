import { describe, expect, test } from 'bun:test'

import { query } from '../query.js'
import { getDefaultAppState } from '../state/AppStateStore.js'
import { asSystemPrompt } from '../utils/systemPromptType.js'
import { createAssistantMessage, createUserMessage } from '../utils/messages.js'

function createToolUseContext(agentId?: string) {
  const appState = getDefaultAppState()
  return {
    options: {
      commands: [],
      debug: false,
      mainLoopModel: 'gpt-5.5',
      tools: [],
      verbose: false,
      thinkingConfig: { type: 'disabled' },
      mcpClients: [],
      mcpResources: {},
      isNonInteractiveSession: false,
      agentDefinitions: { activeAgents: [], allAgents: [] },
    },
    abortController: new AbortController(),
    readFileState: new Map(),
    getAppState: () => appState,
    setAppState: () => {},
    setInProgressToolUseIDs: () => {},
    setResponseLength: () => {},
    updateFileHistoryState: () => {},
    updateAttributionState: () => {},
    messages: [],
    agentId,
  } as any
}

async function collect(iterator: AsyncGenerator<any>) {
  const values: any[] = []
  for await (const value of iterator) {
    values.push(value)
  }
  return values
}

describe('query orchestra integration', () => {
  test('calls Opus advisory once for top-level turns and hides it from output', async () => {
    const modelCalls: any[] = []
    const orchestraCalls: any[] = []
    const hidden = createUserMessage({
      content: '<orchestra-advisory>hidden opus note</orchestra-advisory>',
      isMeta: true,
    })

    const deps = {
      callModel: async function* (params: any) {
        modelCalls.push(params)
        yield createAssistantMessage({ content: 'done' })
      },
      microcompact: async (messages: any[]) => ({ messages }),
      autocompact: async () => ({
        compactionResult: null,
        consecutiveFailures: undefined,
      }),
      uuid: () => 'query-chain-id',
      orchestraGuidance: async (params: any) => {
        orchestraCalls.push(params)
        return { metaMessage: hidden }
      },
    }

    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'implement this' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )

    expect(orchestraCalls.length).toBe(1)
    expect(modelCalls.length).toBe(1)
    expect(modelCalls[0].messages.some((m: any) => m.uuid === hidden.uuid)).toBe(true)
    expect(yielded.some((m: any) => m.uuid === hidden.uuid)).toBe(false)
  })

  test('routes top-level orchestra turns through the Codex implementer', async () => {
    const modelCalls: any[] = []
    const deps = {
      callModel: async function* (params: any) {
        modelCalls.push(params)
        yield createAssistantMessage({ content: 'done' })
      },
      microcompact: async (messages: any[]) => ({ messages }),
      autocompact: async () => ({
        compactionResult: null,
        consecutiveFailures: undefined,
      }),
      uuid: () => 'query-chain-id',
      orchestraGuidance: async () => ({ metaMessage: undefined }),
      orchestraImplementerRoute: () => ({
        route: {
          model: 'gpt-5.5',
          providerOverride: {
            model: 'codexplan',
            baseURL: 'https://chatgpt.com/backend-api/codex',
            apiKey: '',
          },
        },
      }),
    }

    await collect(
      query({
        messages: [createUserMessage({ content: 'implement this' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )

    expect(modelCalls.length).toBe(1)
    expect(modelCalls[0].options.model).toBe('gpt-5.5')
    expect(modelCalls[0].options.providerOverride).toEqual({
      model: 'codexplan',
      baseURL: 'https://chatgpt.com/backend-api/codex',
      apiKey: '',
    })
  })

  test('blocks the GPT implementer call when required Opus guidance fails', async () => {
    const modelCalls: any[] = []
    const deps = {
      callModel: async function* (params: any) {
        modelCalls.push(params)
        yield createAssistantMessage({ content: 'should not run' })
      },
      microcompact: async (messages: any[]) => ({ messages }),
      autocompact: async () => ({
        compactionResult: null,
        consecutiveFailures: undefined,
      }),
      uuid: () => 'query-chain-id',
      orchestraGuidance: async () => ({
        blockingError:
          'Claude Opus (configured) planner failed before GPT implementation could start.',
      }),
      orchestraImplementerRoute: () => ({
        route: {
          model: 'gpt-5.5',
          providerOverride: {
            model: 'codexplan',
            baseURL: 'https://chatgpt.com/backend-api/codex',
            apiKey: '',
          },
        },
      }),
    }

    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'implement this' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )

    expect(modelCalls.length).toBe(0)
    expect(
      yielded.some((m: any) =>
        JSON.stringify(m.message?.content ?? '').includes(
          'Claude Opus (configured)',
        ),
      ),
    ).toBe(true)
  })

  test('does not call Opus advisory for subagent turns', async () => {
    const orchestraCalls: any[] = []
    const deps = {
      callModel: async function* () {
        yield createAssistantMessage({ content: 'done' })
      },
      microcompact: async (messages: any[]) => ({ messages }),
      autocompact: async () => ({
        compactionResult: null,
        consecutiveFailures: undefined,
      }),
      uuid: () => 'query-chain-id',
      orchestraGuidance: async (params: any) => {
        orchestraCalls.push(params)
        return { metaMessage: undefined }
      },
    }

    await collect(
      query({
        messages: [createUserMessage({ content: 'implement this' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext('agent-1'),
        querySource: 'agent:worker' as any,
        deps: deps as any,
      }),
    )

    expect(orchestraCalls.length).toBe(0)
  })

  test('routes subagent turns through Codex when implementer policy allows it', async () => {
    const modelCalls: any[] = []
    const deps = {
      callModel: async function* (params: any) {
        modelCalls.push(params)
        yield createAssistantMessage({ content: 'done' })
      },
      microcompact: async (messages: any[]) => ({ messages }),
      autocompact: async () => ({
        compactionResult: null,
        consecutiveFailures: undefined,
      }),
      uuid: () => 'query-chain-id',
      orchestraGuidance: async () => ({ metaMessage: undefined }),
      orchestraImplementerRoute: () => ({
        route: {
          model: 'gpt-5.5',
          providerOverride: {
            model: 'codexplan',
            baseURL: 'https://chatgpt.com/backend-api/codex',
            apiKey: '',
          },
        },
      }),
    }

    await collect(
      query({
        messages: [createUserMessage({ content: 'implement this' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext('agent-1'),
        querySource: 'agent:worker' as any,
        deps: deps as any,
      }),
    )

    expect(modelCalls.length).toBe(1)
    expect(modelCalls[0].options.model).toBe('gpt-5.5')
    expect(modelCalls[0].options.providerOverride.model).toBe('codexplan')
  })
})
