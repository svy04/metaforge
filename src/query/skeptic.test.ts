import { describe, expect, test } from 'bun:test'

import { query } from '../query.js'
import { getDefaultAppState } from '../state/AppStateStore.js'
import { asSystemPrompt } from '../utils/systemPromptType.js'
import {
  createAssistantMessage,
  createSystemMessage,
  createUserMessage,
} from '../utils/messages.js'

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

const baseDeps = {
  microcompact: async (messages: any[]) => ({ messages }),
  autocompact: async () => ({
    compactionResult: null,
    consecutiveFailures: undefined,
  }),
  uuid: () => 'query-chain-id',
  orchestraGuidance: async () => ({ metaMessage: undefined }),
}

describe('query orchestra skeptic integration', () => {
  test('fires the skeptic exactly once per turn after a tool_use-free assistant message', async () => {
    const skepticCalls: any[] = []
    const skepticMessage = createSystemMessage('[Opus 야당] dissent', 'warning')

    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'Codex final answer' })
      },
      skepticDissent: async (params: any) => {
        skepticCalls.push(params)
        return { systemMessage: skepticMessage }
      },
    }

    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'design risks please' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )

    expect(skepticCalls.length).toBe(1)
    expect(yielded.some((m: any) => m.uuid === skepticMessage.uuid)).toBe(true)
  })

  test('does not fire the skeptic when the assistant message contains tool_use', async () => {
    const skepticCalls: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({
          content: [
            {
              type: 'tool_use',
              id: 'tu-1',
              name: 'Read',
              input: { file_path: '/tmp/x' },
            } as any,
          ],
        })
      },
      skepticDissent: async (params: any) => {
        skepticCalls.push(params)
        return { systemMessage: undefined }
      },
    }

    await collect(
      query({
        messages: [createUserMessage({ content: 'read this file' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
        // tool_use yields needsFollowUp; we only care about the first turn's
        // skeptic gate, so cap turns to keep this test under the 5s timeout.
        maxTurns: 1,
      }),
    )

    expect(skepticCalls.length).toBe(0)
  })

  test('does not fire the skeptic on subagent turns', async () => {
    const skepticCalls: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'subagent answer' })
      },
      skepticDissent: async (params: any) => {
        skepticCalls.push(params)
        return { systemMessage: undefined }
      },
    }

    await collect(
      query({
        messages: [createUserMessage({ content: 'subagent task' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext('agent-1'),
        querySource: 'agent:worker' as any,
        deps: deps as any,
      }),
    )

    expect(skepticCalls.length).toBe(0)
  })

  test('skeptic dispatch failure does not block the assistant response from yielding', async () => {
    const yielded: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'Codex final answer' })
      },
      skepticDissent: async () => {
        throw new Error('skeptic exploded')
      },
    }

    for await (const message of query({
      messages: [createUserMessage({ content: 'design risks' })],
      systemPrompt: asSystemPrompt(['system']),
      userContext: {},
      systemContext: {},
      canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
      toolUseContext: createToolUseContext(),
      querySource: 'repl_main_thread' as any,
      deps: deps as any,
    })) {
      yielded.push(message)
    }

    // Codex final answer must still be present even though skeptic threw.
    const sawAssistant = yielded.some(
      (m: any) =>
        m.type === 'assistant' &&
        Array.isArray(m.message?.content) &&
        m.message.content.some(
          (b: any) => b.type === 'text' && b.text === 'Codex final answer',
        ),
    )
    expect(sawAssistant).toBe(true)
  })

  test('skeptic returning undefined systemMessage does not yield a phantom message', async () => {
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'Codex final answer' })
      },
      skepticDissent: async () => ({
        diagnostic: 'skeptic skipped silently',
      }),
    }

    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'design risks' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )

    const systemMessages = yielded.filter(
      (m: any) => m.type === 'system' && m.subtype === 'informational',
    )
    expect(systemMessages.length).toBe(0)
  })
})
