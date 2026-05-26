import { mkdir, readFile, writeFile } from 'fs/promises'
import { dirname } from 'path'

import { getMemoryPath } from '../../utils/config.js'
import type { OrchestraMemoryScope } from './config.js'

const SECTION_HEADER = '## OpenClaude Orchestrator Memory'

export type PersistMemoryCandidatesParams = {
  candidates: string[]
  memoryPath?: string
  memoryScope?: OrchestraMemoryScope | 'user' | 'local' | 'managed'
}

export type PersistMemoryCandidatesResult = {
  written: string[]
  skipped: string[]
}

function normalizeCandidate(candidate: string): string {
  return candidate.trim().replace(/\s+/g, ' ')
}

function dedupeKey(candidate: string): string {
  return normalizeCandidate(candidate).toLowerCase()
}

function existingKeys(content: string): Set<string> {
  const keys = new Set<string>()
  for (const line of content.split(/\r?\n/)) {
    const trimmed = line.trim()
    if (!trimmed.startsWith('- ')) continue
    keys.add(dedupeKey(trimmed.slice(2)))
  }
  return keys
}

export async function persistProjectMemoryCandidates({
  candidates,
  memoryPath = getMemoryPath('Project'),
  memoryScope = 'project',
}: PersistMemoryCandidatesParams): Promise<PersistMemoryCandidatesResult> {
  if (memoryScope !== 'project') {
    return { written: [], skipped: candidates }
  }

  const normalized = candidates.map(normalizeCandidate).filter(Boolean)
  if (normalized.length === 0) {
    return { written: [], skipped: [] }
  }

  let content = ''
  try {
    content = await readFile(memoryPath, 'utf8')
  } catch {
    content = ''
  }

  const keys = existingKeys(content)
  const written: string[] = []
  const skipped: string[] = []
  for (const candidate of normalized) {
    const key = dedupeKey(candidate)
    if (keys.has(key)) {
      skipped.push(candidate)
      continue
    }
    keys.add(key)
    written.push(candidate)
  }

  if (written.length === 0) {
    return { written, skipped }
  }

  const prefix = content.trimEnd()
  const entries = written.map(candidate => `- ${candidate}`).join('\n')
  const section = prefix.includes(SECTION_HEADER)
    ? `\n${entries}\n`
    : `\n\n${SECTION_HEADER}\n${entries}\n`
  const nextContent = prefix
    ? `${prefix}${section}`
    : `${SECTION_HEADER}\n${entries}\n`

  await mkdir(dirname(memoryPath), { recursive: true })
  await writeFile(memoryPath, nextContent, 'utf8')
  return { written, skipped }
}
