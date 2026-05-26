import { describe, expect, test } from 'bun:test'

import { query } from '../query.js'
import { getDefaultAppState } from '../state/AppStateStore.js'
import { asSystemPrompt } from '../utils/systemPromptType.js'
import {
  createAssistantMessage,
  createSystemMessage,
  createUserMessage,
} from '../utils/messages.js'

function createToolUseContext(opts: {
  agentId?: string
  shadowEnabled?: boolean
  shadowEveryTurn?: boolean
} = {}) {
  const appState = getDefaultAppState()
  ;(appState as { settings?: unknown }).settings = {
    orchestra: {
      shadowEnabled: opts.shadowEnabled ?? false,
      shadowEveryTurn: opts.shadowEveryTurn ?? false,
    },
  } as any
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
    agentId: opts.agentId,
  } as any
}

async function collect(it: AsyncGenerator<any>) {
  const out: any[] = []
  for await (const v of it) out.push(v)
  return out
}

const baseDeps = {
  microcompact: async (messages: any[]) => ({ messages }),
  autocompact: async () => ({
    compactionResult: null,
    consecutiveFailures: undefined,
  }),
  uuid: () => 'cid',
  orchestraGuidance: async () => ({ metaMessage: undefined }),
}

describe('query orchestra shadow hook', () => {
  test('does NOT fire shadow review when shadowEnabled is false (default)', async () => {
    const calls: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'final answer' })
      },
      shadowReview: async (p: any) => {
        calls.push(p)
        return { summaryMessage: undefined }
      },
    }
    await collect(
      query({
        messages: [createUserMessage({ content: 'edit a file' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext(),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )
    expect(calls.length).toBe(0)
  })

  test('does NOT fire shadow review on a text-only turn even when shadowEnabled', async () => {
    const calls: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({ content: 'just talking' })
      },
      shadowReview: async (p: any) => {
        calls.push(p)
        return { summaryMessage: undefined }
      },
    }
    await collect(
      query({
        messages: [createUserMessage({ content: 'how are you?' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext({ shadowEnabled: true }),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
      }),
    )
    expect(calls.length).toBe(0)
  })

  test('fires shadow review once after a turn that contained an Edit tool_use', async () => {
    const calls: any[] = []
    const summary = createSystemMessage(
      '[Phase 3 Cross-Review] gpt-a: 🟢×2',
      'info',
    )
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        // First yield: assistant uses Edit (mutation)
        yield createAssistantMessage({
          content: [
            {
              type: 'tool_use',
              id: 'tu-edit-1',
              name: 'Edit',
              input: {
                file_path: '/repo/x.ts',
                old_string: 'a',
                new_string: 'b',
              },
            } as any,
          ],
        })
        // Second yield: tool_use-free final answer (turn end)
        yield createAssistantMessage({ content: 'I edited the file.' })
      },
      shadowReview: async (p: any) => {
        calls.push(p)
        return { summaryMessage: summary }
      },
    }

    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'apply the edit' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext({ shadowEnabled: true }),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
        maxTurns: 1,
      }),
    )

    expect(calls.length).toBe(1)
    expect(yielded.some(m => m.uuid === summary.uuid)).toBe(true)
  })

  test('does NOT fire shadow review on subagent turns even when shadowEnabled', async () => {
    const calls: any[] = []
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({
          content: [
            {
              type: 'tool_use',
              id: 'tu-w-1',
              name: 'Write',
              input: { file_path: '/repo/y.ts', content: 'x' },
            } as any,
          ],
        })
        yield createAssistantMessage({ content: 'subagent done' })
      },
      shadowReview: async (p: any) => {
        calls.push(p)
        return { summaryMessage: undefined }
      },
    }
    await collect(
      query({
        messages: [createUserMessage({ content: 'subagent edit' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext({
          agentId: 'sub-1',
          shadowEnabled: true,
        }),
        querySource: 'agent:worker' as any,
        deps: deps as any,
        maxTurns: 1,
      }),
    )
    expect(calls.length).toBe(0)
  })

  test('shadow review yields the Phase 4 humanGateMessage when provided', async () => {
    const summary = createSystemMessage(
      '[Phase 3 Cross-Review] gpt-a: 🟢×2',
      'info',
    )
    const gate = createSystemMessage(
      '[Phase 4 Human Gate] 추천: gpt-a (green)',
      'info',
    )
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({
          content: [
            {
              type: 'tool_use',
              id: 'tu-edit-x',
              name: 'Edit',
              input: { file_path: '/repo/x.ts', old_string: 'a', new_string: 'b' },
            } as any,
          ],
        })
        yield createAssistantMessage({ content: 'edited!' })
      },
      shadowReview: async () => ({
        summaryMessage: summary,
        humanGateMessage: gate,
      }),
    }
    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'edit it' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext({ shadowEnabled: true }),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
        maxTurns: 1,
      }),
    )
    const sawSummary = yielded.some(m => m.uuid === summary.uuid)
    const sawGate = yielded.some(m => m.uuid === gate.uuid)
    expect(sawSummary).toBe(true)
    expect(sawGate).toBe(true)
  })

  test('shadow review throwing does not block the assistant response', async () => {
    const deps = {
      ...baseDeps,
      callModel: async function* () {
        yield createAssistantMessage({
          content: [
            {
              type: 'tool_use',
              id: 'tu-edit-2',
              name: 'Edit',
              input: { file_path: '/repo/z.ts', old_string: 'a', new_string: 'b' },
            } as any,
          ],
        })
        yield createAssistantMessage({ content: 'edited!' })
      },
      shadowReview: async () => {
        throw new Error('shadow exploded')
      },
    }
    const yielded = await collect(
      query({
        messages: [createUserMessage({ content: 'edit' })],
        systemPrompt: asSystemPrompt(['system']),
        userContext: {},
        systemContext: {},
        canUseTool: async () => ({ behavior: 'allow', updatedInput: undefined }),
        toolUseContext: createToolUseContext({ shadowEnabled: true }),
        querySource: 'repl_main_thread' as any,
        deps: deps as any,
        maxTurns: 1,
      }),
    )
    const sawFinal = yielded.some(
      (m: any) =>
        m.type === 'assistant' &&
        Array.isArray(m.message?.content) &&
        m.message.content.some(
          (b: any) => b.type === 'text' && b.text === 'edited!',
        ),
    )
    expect(sawFinal).toBe(true)
  })
})
