import { readdirSync } from 'node:fs'
import { resolve } from 'node:path'

export type TraceDiscoveryOptions = {
  root?: string
  traceDirectory?: string
}

const historicalLiveProbeTracePattern = /^orchestra-live(?:-|$).*\.jsonl$/

function traceBasename(path: string): string {
  return path.replace(/\\/g, '/').split('/').pop() ?? path
}

export function isHistoricalLiveProbeTracePath(path: string): boolean {
  return historicalLiveProbeTracePattern.test(traceBasename(path))
}

export function discoverPublishableTraceFiles({
  root = process.cwd(),
  traceDirectory = 'reports',
}: TraceDiscoveryOptions = {}): string[] {
  return readdirSync(resolve(root, traceDirectory), { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .filter((name) => /^orchestra-.*\.jsonl$/.test(name))
    .filter((name) => !isHistoricalLiveProbeTracePath(name))
    .sort((a, b) => a.localeCompare(b))
    .map((name) => `${traceDirectory}/${name}`)
}
