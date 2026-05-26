import { createHash } from 'node:crypto'

export type TraceEnrichmentFields = {
  eventName: string
  traceId: string
  spanId: string
  actionName?: string
  observationSummary?: string
}

type TraceEnrichmentOptions = {
  traceSeed: string
  spanSeed: string
  eventName: string
  actionName?: string
  observationSummary?: string
}

function sha256(text: string): string {
  return createHash('sha256').update(text).digest('hex')
}

function normalizeLabel(value: string): string {
  return value
    .trim()
    .replace(/[^A-Za-z0-9_.-]+/g, '_')
    .replace(/^_+|_+$/g, '')
}

export function buildTraceEventName(
  captureKind: string,
  role: string,
  status: string,
  actionName?: string,
): string {
  const actionSegment = actionName && actionName.trim().length > 0 ? actionName : role
  return normalizeLabel(`${captureKind}.${actionSegment}.${status}`)
}

export function describeTraceObservation(status: string, fields: {
  exitCode?: number | null
  passed?: boolean
  stdoutByteLength?: number
  stderrByteLength?: number
  testCaseCount?: number
}): string {
  const details = [`status=${status}`]
  if (fields.exitCode !== undefined) details.push(`exitCode=${fields.exitCode}`)
  if (fields.passed !== undefined) details.push(`passed=${fields.passed}`)
  if (fields.testCaseCount !== undefined) details.push(`testCaseCount=${fields.testCaseCount}`)
  if (fields.stdoutByteLength !== undefined) details.push(`stdoutBytes=${fields.stdoutByteLength}`)
  if (fields.stderrByteLength !== undefined) details.push(`stderrBytes=${fields.stderrByteLength}`)
  return details.join(';')
}

export function enrichTraceEvent<T extends Record<string, unknown>>(
  event: T,
  options: TraceEnrichmentOptions,
): T & TraceEnrichmentFields {
  const enriched: T & TraceEnrichmentFields = {
    ...event,
    eventName: normalizeLabel(options.eventName),
    traceId: sha256(options.traceSeed).slice(0, 32),
    spanId: sha256(`${options.traceSeed}:${options.spanSeed}`).slice(0, 16),
  }
  if (options.actionName && options.actionName.trim().length > 0) {
    enriched.actionName = normalizeLabel(options.actionName)
  }
  if (options.observationSummary && options.observationSummary.trim().length > 0) {
    enriched.observationSummary = options.observationSummary
  }
  return enriched
}
