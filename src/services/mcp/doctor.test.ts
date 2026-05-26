import assert from 'node:assert/strict'
import test from 'node:test'

import type { ValidationError } from '../../utils/settings/validation.js'

import {
  buildEmptyDoctorReport,
  doctorAllServers,
  doctorServer,
  findingsFromValidationErrors,
  type McpDoctorDependencies,
} from './doctor.js'
import type { MCPServerConnection, ScopedMcpServerConfig } from './types.js'

type Scope = Parameters<McpDoctorDependencies['getMcpConfigsByScope']>[0]
type ScopeConfigResult = ReturnType<McpDoctorDependencies['getMcpConfigsByScope']>
type ConnectToServer = McpDoctorDependencies['connectToServer']
type ConnectResult = Awaited<ReturnType<ConnectToServer>>

function stdioConfig(
  scope: 'local' | 'project' | 'user' | 'enterprise',
  command: string,
): ScopedMcpServerConfig {
  return {
    type: 'stdio' as const,
    command,
    args: [],
    scope,
  }
}

function scopeResult(
  servers: Record<string, ScopedMcpServerConfig> = {},
  errors: ValidationError[] = [],
): ScopeConfigResult {
  return { servers, errors }
}

function scopeConfigs(
  fn: (scope: Scope) => ScopeConfigResult,
): McpDoctorDependencies['getMcpConfigsByScope'] {
  return fn
}

function connectStub(
  fn: (name: string, config: ScopedMcpServerConfig) => Promise<ConnectResult>,
): ConnectToServer {
  return fn as ConnectToServer
}

function connectedResult(
  name: string,
  config: ScopedMcpServerConfig,
): MCPServerConnection {
  return {
    name,
    type: 'connected',
    capabilities: {},
    client: {} as never,
    config,
    cleanup: async () => {},
  }
}

function makeDependencies(overrides: Partial<McpDoctorDependencies> = {}): McpDoctorDependencies {
  return {
    getAllMcpConfigs: async () => ({ servers: {}, errors: [] }),
    getMcpConfigsByScope: () => scopeResult(),
    getProjectMcpServerStatus: () => 'approved',
    isMcpServerDisabled: () => false,
    describeMcpConfigFilePath: scope => `scope://${scope}`,
    clearServerCache: async () => {},
    connectToServer: connectStub(async (name, config) => connectedResult(name, config)),
    ...overrides,
  }
}

test('buildEmptyDoctorReport returns zeroed summary', () => {
  const report = buildEmptyDoctorReport({
    configOnly: true,
    scopeFilter: 'project',
    targetName: 'filesystem',
  })

  assert.equal(report.targetName, 'filesystem')
  assert.equal(report.scopeFilter, 'project')
  assert.equal(report.configOnly, true)
  assert.deepEqual(report.summary, {
    totalReports: 0,
    healthy: 0,
    warnings: 0,
    blocking: 0,
  })
  assert.deepEqual(report.findings, [])
  assert.deepEqual(report.servers, [])
})

test('findingsFromValidationErrors maps missing env warnings into doctor findings', () => {
  const validationErrors: ValidationError[] = [
    {
      file: '.mcp.json',
      path: 'mcpServers.filesystem',
      message: 'Missing environment variables: API_KEY, API_URL',
      suggestion: 'Set the following environment variables: API_KEY, API_URL',
      mcpErrorMetadata: {
        scope: 'project',
        serverName: 'filesystem',
        severity: 'warning',
      },
    },
  ]

  const findings = findingsFromValidationErrors(validationErrors)

  assert.equal(findings.length, 1)
  assert.deepEqual(findings[0], {
    blocking: false,
    code: 'config.missing_env_vars',
    message: 'Missing environment variables: API_KEY, API_URL',
    remediation: 'Set the following environment variables: API_KEY, API_URL',
    scope: 'project',
    serverName: 'filesystem',
    severity: 'warn',
    sourcePath: '.mcp.json',
  })
})

test('findingsFromValidationErrors maps Windows npx warnings into doctor findings', () => {
  const validationErrors: ValidationError[] = [
    {
      file: '.mcp.json',
      path: 'mcpServers.node-tools',
      message: "Windows requires 'cmd /c' wrapper to execute npx",
      suggestion:
        'Change command to "cmd" with args ["/c", "npx", ...]. See: https://code.claude.com/docs/en/mcp#configure-mcp-servers',
      mcpErrorMetadata: {
        scope: 'project',
        serverName: 'node-tools',
        severity: 'warning',
      },
    },
  ]

  const findings = findingsFromValidationErrors(validationErrors)

  assert.equal(findings.length, 1)
  assert.equal(findings[0]?.code, 'config.windows_npx_wrapper_required')
  assert.equal(findings[0]?.serverName, 'node-tools')
  assert.equal(findings[0]?.severity, 'warn')
  assert.equal(findings[0]?.blocking, false)
})

test('findingsFromValidationErrors maps fatal parse errors into blocking findings', () => {
  const validationErrors: ValidationError[] = [
    {
      file: 'C:/repo/.mcp.json',
      path: '',
      message: 'MCP config is not a valid JSON',
      suggestion: 'Fix the JSON syntax errors in the file',
      mcpErrorMetadata: {
        scope: 'project',
        severity: 'fatal',
      },
    },
  ]

  const findings = findingsFromValidationErrors(validationErrors)

  assert.equal(findings.length, 1)
  assert.equal(findings[0]?.code, 'config.invalid_json')
  assert.equal(findings[0]?.severity, 'error')
  assert.equal(findings[0]?.blocking, true)
})

test('doctorAllServers reports global validation findings once without duplicating them into every server', async () => {
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { filesystem: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'project'
        ? scopeResult(
            {},
            [
              {
                file: '.mcp.json',
                path: '',
                message: 'MCP config is not a valid JSON',
                suggestion: 'Fix the JSON syntax errors in the file',
                mcpErrorMetadata: {
                  scope: 'project',
                  severity: 'fatal',
                },
              },
            ],
          )
        : scope === 'local'
          ? scopeResult({ filesystem: localConfig })
          : scopeResult(),
    ),
  })

  const report = await doctorAllServers({ configOnly: true }, deps)

  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.summary.blocking, 1)
  assert.equal(report.findings.length, 1)
  assert.equal(report.findings[0]?.code, 'config.invalid_json')
  assert.deepEqual(report.servers[0]?.findings, [])
})

test('doctorServer explains same-name shadowing across scopes', async () => {
  const localConfig = stdioConfig('local', 'node-local')
  const userConfig = stdioConfig('user', 'node-user')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: {
        filesystem: localConfig,
      },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope => {
      switch (scope) {
        case 'local':
          return scopeResult({ filesystem: localConfig })
        case 'user':
          return scopeResult({ filesystem: userConfig })
        default:
          return scopeResult()
      }
    }),
  })

  const report = await doctorServer('filesystem', { configOnly: true }, deps)
  assert.equal(report.servers.length, 1)
  assert.equal(report.servers[0]?.definitions.length, 2)
  assert.equal(report.servers[0]?.definitions.find(def => def.sourceType === 'local')?.runtimeActive, true)
  assert.equal(report.servers[0]?.definitions.find(def => def.sourceType === 'user')?.runtimeActive, false)
  assert.deepEqual(
    report.servers[0]?.findings.map(finding => finding.code).sort(),
    ['duplicate.same_name_multiple_scopes', 'scope.shadowed'],
  )
})

test('doctorServer reports project servers pending approval', async () => {
  const projectConfig = stdioConfig('project', 'node-project')
  const deps = makeDependencies({
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'project'
        ? scopeResult({ sentry: projectConfig })
        : scopeResult(),
    ),
    getProjectMcpServerStatus: name => (name === 'sentry' ? 'pending' : 'approved'),
  })

  const report = await doctorServer('sentry', { configOnly: true }, deps)
  assert.equal(report.servers.length, 1)
  assert.equal(report.servers[0]?.definitions[0]?.pendingApproval, true)
  assert.equal(report.servers[0]?.definitions[0]?.runtimeActive, false)
  assert.equal(report.servers[0]?.definitions[0]?.runtimeVisible, false)
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'state.pending_project_approval'),
    true,
  )
})

test('doctorServer does not treat disabled servers as runtime-active or live-check targets', async () => {
  let connectCalls = 0
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { github: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'local'
        ? scopeResult({ github: localConfig })
        : scopeResult(),
    ),
    isMcpServerDisabled: name => name === 'github',
    connectToServer: connectStub(async (name, config) => {
      connectCalls += 1
      return {
        name,
        type: 'failed',
        config,
        error: 'should not connect',
      }
    }),
  })

  const report = await doctorServer('github', { configOnly: false }, deps)

  assert.equal(connectCalls, 0)
  assert.equal(report.summary.blocking, 0)
  assert.equal(report.summary.warnings, 1)
  assert.equal(report.servers[0]?.definitions[0]?.disabled, true)
  assert.equal(report.servers[0]?.definitions[0]?.runtimeActive, false)
  assert.equal(report.servers[0]?.definitions[0]?.runtimeVisible, false)
  assert.equal(report.servers[0]?.liveCheck.result, 'disabled')
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'state.disabled' && finding.severity === 'warn'),
    true,
  )
})

test('doctorAllServers skips live checks in config-only mode', async () => {
  let connectCalls = 0
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { linear: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'local'
        ? scopeResult({ linear: localConfig })
        : scopeResult(),
    ),
    connectToServer: connectStub(async (name, config) => {
      connectCalls += 1
      return connectedResult(name, config)
    }),
  })

  const report = await doctorAllServers({ configOnly: true }, deps)
  assert.equal(connectCalls, 0)
  assert.equal(report.servers[0]?.liveCheck.attempted, false)
  assert.equal(report.servers[0]?.liveCheck.result, 'skipped')
})

test('doctorAllServers honors scopeFilter when collecting names', async () => {
  const pluginConfig = {
    type: 'http' as const,
    url: 'https://example.test/mcp',
    scope: 'dynamic' as const,
    pluginSource: 'plugin:github@official',
  }
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { 'plugin:github:github': pluginConfig },
      errors: [],
    }),
  })

  const report = await doctorAllServers({ configOnly: true, scopeFilter: 'user' }, deps)

  assert.equal(report.summary.totalReports, 0)
  assert.deepEqual(report.servers, [])
})

test('doctorAllServers honors scopeFilter when collecting validation errors', async () => {
  const userConfig = stdioConfig('user', 'node-user')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { filesystem: userConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope => {
      switch (scope) {
        case 'project':
          return scopeResult(
            {},
            [
              {
                file: '.mcp.json',
                path: '',
                message: 'MCP config is not a valid JSON',
                suggestion: 'Fix the JSON syntax errors in the file',
                mcpErrorMetadata: {
                  scope: 'project',
                  severity: 'fatal',
                },
              },
            ],
          )
        case 'user':
          return scopeResult({ filesystem: userConfig })
        default:
          return scopeResult()
      }
    }),
  })

  const report = await doctorAllServers({ configOnly: true, scopeFilter: 'user' }, deps)

  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.summary.blocking, 0)
  assert.deepEqual(report.findings, [])
  assert.deepEqual(report.servers[0]?.findings, [])
})

test('doctorAllServers includes observed runtime definitions for plugin-only servers', async () => {
  const pluginConfig = {
    type: 'http' as const,
    url: 'https://example.test/mcp',
    scope: 'dynamic' as const,
    pluginSource: 'plugin:github@official',
  }
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { 'plugin:github:github': pluginConfig },
      errors: [],
    }),
  })

  const report = await doctorAllServers({ configOnly: true }, deps)

  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.servers[0]?.definitions.length, 1)
  assert.equal(report.servers[0]?.definitions[0]?.sourceType, 'plugin')
  assert.equal(report.servers[0]?.definitions[0]?.runtimeActive, true)
})

test('doctorAllServers reports disabled plugin servers as disabled, not not-found', async () => {
  const pluginConfig = {
    type: 'http' as const,
    url: 'https://example.test/mcp',
    scope: 'dynamic' as const,
    pluginSource: 'plugin:github@official',
  }
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { 'plugin:github:github': pluginConfig },
      errors: [],
    }),
    isMcpServerDisabled: name => name === 'plugin:github:github',
  })

  const report = await doctorAllServers({ configOnly: true }, deps)

  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.summary.warnings, 1)
  assert.equal(report.summary.blocking, 0)
  assert.equal(report.servers[0]?.definitions.length, 1)
  assert.equal(report.servers[0]?.definitions[0]?.sourceType, 'plugin')
  assert.equal(report.servers[0]?.definitions[0]?.disabled, true)
  assert.equal(report.servers[0]?.definitions[0]?.runtimeActive, false)
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'state.disabled' && !finding.blocking),
    true,
  )
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'state.not_found'),
    false,
  )
})

test('doctorServer converts failed live checks into blocking findings', async () => {
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { github: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'local'
        ? scopeResult({ github: localConfig })
        : scopeResult(),
    ),
    connectToServer: connectStub(async (name, config) => ({
      name,
      type: 'failed',
      config,
      error: 'command not found: node-local',
    })),
  })

  const report = await doctorServer('github', { configOnly: false }, deps)

  assert.equal(report.summary.blocking, 1)
  assert.equal(report.servers[0]?.liveCheck.result, 'failed')
  assert.equal(
    report.servers[0]?.findings.some(
      finding => finding.code === 'stdio.command_not_found' && finding.blocking,
    ),
    true,
  )
})

test('doctorServer converts needs-auth live checks into warning findings', async () => {
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { sentry: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'local'
        ? scopeResult({ sentry: localConfig })
        : scopeResult(),
    ),
    connectToServer: connectStub(async (name, config) => ({
      name,
      type: 'needs-auth',
      config,
    })),
  })

  const report = await doctorServer('sentry', { configOnly: false }, deps)

  assert.equal(report.summary.warnings, 1)
  assert.equal(report.summary.blocking, 0)
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'auth.needs_auth' && finding.severity === 'warn'),
    true,
  )
})

test('doctorServer includes observed runtime definition for plugin-only targets', async () => {
  const pluginConfig = {
    type: 'http' as const,
    url: 'https://example.test/mcp',
    scope: 'dynamic' as const,
    pluginSource: 'plugin:github@official',
  }
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { 'plugin:github:github': pluginConfig },
      errors: [],
    }),
  })

  const report = await doctorServer('plugin:github:github', { configOnly: true }, deps)

  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.servers[0]?.definitions.length, 1)
  assert.equal(report.servers[0]?.definitions[0]?.sourceType, 'plugin')
  assert.equal(report.servers[0]?.definitions[0]?.runtimeActive, true)
})

test('doctorServer with scopeFilter does not leak runtime definition from another scope when target is absent', async () => {
  let connectCalls = 0
  const localConfig = stdioConfig('local', 'node-local')
  const deps = makeDependencies({
    getAllMcpConfigs: async () => ({
      servers: { github: localConfig },
      errors: [],
    }),
    getMcpConfigsByScope: scopeConfigs(scope =>
      scope === 'local'
        ? scopeResult({ github: localConfig })
        : scopeResult(),
    ),
    connectToServer: connectStub(async (name, config) => {
      connectCalls += 1
      return connectedResult(name, config)
    }),
  })

  const report = await doctorServer('github', { configOnly: false, scopeFilter: 'user' }, deps)

  assert.equal(connectCalls, 0)
  assert.equal(report.summary.totalReports, 1)
  assert.equal(report.summary.blocking, 1)
  assert.deepEqual(report.servers[0]?.definitions, [])
  assert.equal(report.servers[0]?.liveCheck.result, 'skipped')
  assert.equal(
    report.servers[0]?.findings.some(finding => finding.code === 'state.not_found' && finding.blocking),
    true,
  )
})

test('doctorServer reports blocking not-found state when no definition exists', async () => {
  const report = await doctorServer('missing-server', { configOnly: true }, makeDependencies())

  assert.equal(report.summary.blocking, 1)
  assert.equal(report.servers[0]?.findings.some(finding => finding.code === 'state.not_found' && finding.blocking), true)
})
