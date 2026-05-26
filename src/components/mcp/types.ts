import type {
  ConfigScope,
  MCPServerConnection,
  McpClaudeAIProxyServerConfig,
  McpHTTPServerConfig,
  McpSSEServerConfig,
  McpStdioServerConfig,
} from '../../services/mcp/types.js'

type BaseServerInfo<
  TTransport extends string,
  TConfig,
> = {
  name: string
  client: MCPServerConnection
  scope: ConfigScope
  transport: TTransport
  config: TConfig
  isAuthenticated?: boolean
}

export type StdioServerInfo = BaseServerInfo<'stdio', McpStdioServerConfig>
export type SSEServerInfo = BaseServerInfo<'sse', McpSSEServerConfig>
export type HTTPServerInfo = BaseServerInfo<'http', McpHTTPServerConfig>
export type ClaudeAIServerInfo = BaseServerInfo<
  'claudeai-proxy',
  McpClaudeAIProxyServerConfig
>

export type ServerInfo =
  | StdioServerInfo
  | SSEServerInfo
  | HTTPServerInfo
  | ClaudeAIServerInfo

export type AgentMcpServerInfo = {
  name: string
  sourceAgents: string[]
  transport: 'stdio' | 'sse' | 'http' | 'ws'
  command?: string
  url?: string
  needsAuth: boolean
  isAuthenticated?: boolean
}

export type MCPViewState =
  | {
      type: 'list'
      defaultTab?: string
    }
  | {
      type: 'server-menu'
      server: ServerInfo
    }
  | {
      type: 'server-tools'
      server: ServerInfo
    }
  | {
      type: 'server-tool-detail'
      server: ServerInfo
      toolIndex: number
    }
  | {
      type: 'agent-server-menu'
      agentServer: AgentMcpServerInfo
    }
