import { spawnSync } from 'child_process'

const DEFAULT_HEAP_SIZE_MB = 8192
const BOOTSTRAPPED_ENV = 'OPENCLAUDE_NODE_HEAP_BOOTSTRAPPED'
const DISABLE_ENV = 'OPENCLAUDE_DISABLE_HEAP_BOOTSTRAP'
const HEAP_SIZE_ENV = 'OPENCLAUDE_NODE_MAX_OLD_SPACE_SIZE_MB'
const HEAPSNAPSHOT_ENV = 'OPENCLAUDE_HEAPSNAPSHOT_NEAR_LIMIT'

function hasHeapLimitFlag(values = []) {
  return values.some(value =>
    /--max[-_]old[-_]space[-_]size(?:=|\s|$)/i.test(String(value)),
  )
}

function nodeOptions(env = {}) {
  return String(env.NODE_OPTIONS ?? '')
    .split(/\s+/)
    .filter(Boolean)
}

export function shouldBootstrapHeap({ execArgv = [], env = {} }) {
  if (env[BOOTSTRAPPED_ENV] === '1') return false
  if (env[DISABLE_ENV] === '1') return false
  if (hasHeapLimitFlag(execArgv)) return false
  if (hasHeapLimitFlag(nodeOptions(env))) return false
  return true
}

export function resolveHeapSizeMb(env = {}) {
  const raw = Number.parseInt(String(env[HEAP_SIZE_ENV] ?? ''), 10)
  if (Number.isFinite(raw) && raw >= 1024) return raw
  return DEFAULT_HEAP_SIZE_MB
}

function resolveHeapSnapshotNearLimit(env = {}) {
  const raw = env[HEAPSNAPSHOT_ENV]
  if (raw === undefined || raw === '' || raw === '0' || raw === 'false') {
    return undefined
  }
  if (raw === '1' || raw === 'true') return 3
  const parsed = Number.parseInt(String(raw), 10)
  if (Number.isFinite(parsed) && parsed > 0) return parsed
  return undefined
}

export function buildHeapBootstrapArgs({
  execArgv = [],
  argv = [],
  scriptPath,
  heapSizeMb,
  env = {},
}) {
  const args = [`--max-old-space-size=${heapSizeMb}`, ...execArgv, scriptPath]
  const heapSnapshotNearLimit = resolveHeapSnapshotNearLimit(env)
  if (heapSnapshotNearLimit !== undefined) {
    args.unshift(`--heapsnapshot-near-heap-limit=${heapSnapshotNearLimit}`)
  }
  return [...args, ...argv.slice(2)]
}

function exitStatusFromSpawnResult(result) {
  if (typeof result.status === 'number') return result.status
  if (result.signal === 'SIGINT') return 130
  if (result.signal === 'SIGTERM') return 143
  return 1
}

export function bootstrapNodeHeapIfNeeded({
  execPath,
  execArgv = [],
  argv = [],
  env = {},
  scriptPath,
  spawnSyncImpl = spawnSync,
  exitImpl = process.exit,
  warnImpl = console.warn,
}) {
  if (!shouldBootstrapHeap({ execArgv, env })) return false

  const childEnv = {
    ...env,
    [BOOTSTRAPPED_ENV]: '1',
  }
  const args = buildHeapBootstrapArgs({
    execArgv,
    argv,
    scriptPath,
    heapSizeMb: resolveHeapSizeMb(env),
    env,
  })
  const result = spawnSyncImpl(execPath, args, {
    stdio: 'inherit',
    env: childEnv,
  })

  if (result.error) {
    warnImpl(
      `openclaude: failed to restart with a larger Node heap; continuing with the current process. ${result.error.message}`,
    )
    return false
  }

  exitImpl(exitStatusFromSpawnResult(result))
  return true
}
