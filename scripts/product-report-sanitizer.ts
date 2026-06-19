const sep = String.raw`(?:\\+|/)`
const segment = String.raw`[^\\/"]+`
const userSegment = String.raw`[^\\/"]+`

type ScrubOptions = {
  repoRoot?: string
}

type Replacement = {
  pattern: RegExp
  replacement: string
}

function escapeRegExp(input: string): string {
  return input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function pathPattern(input: string): RegExp {
  const parts = input.split(/[\\/]+/).filter(Boolean).map(escapeRegExp)
  if (parts.length === 0) {
    return /$^/
  }
  const first = parts[0]
  const body = parts.slice(1).join(sep)
  const prefix = /^[A-Za-z]:$/.test(first)
    ? `${first}${body ? sep : ''}`
    : input.startsWith('/') || input.startsWith('\\')
      ? sep
      : ''
  return new RegExp(`${prefix}${body || (!/^[A-Za-z]:$/.test(first) ? first : '')}`, 'g')
}

const staticReplacements: Replacement[] = [
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}Desktop${sep}${segment}${sep}openclaude-0\.6\.0`,
      'g',
    ),
    replacement: '<repo>',
  },
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}AppData${sep}Roaming${sep}npm${sep}node_modules${sep}bun${sep}bin${sep}bun\.exe`,
      'g',
    ),
    replacement: '<bun>',
  },
  {
    pattern: new RegExp(
      String.raw`C:${sep}Users${sep}${userSegment}${sep}AppData${sep}Local${sep}Programs${sep}Microsoft VS Code${sep}resources${sep}app${sep}updating`,
      'g',
    ),
    replacement: '<vscode-updating-sentinel>',
  },
  {
    pattern: new RegExp(String.raw`C:${sep}Users${sep}${userSegment}`, 'g'),
    replacement: '<user-home>',
  },
  {
    pattern: /\/Users\/[^/\s"']+/g,
    replacement: '<user-home>',
  },
]

function replacementsFor(options: ScrubOptions): Replacement[] {
  return [
    {
      pattern: pathPattern(options.repoRoot ?? process.cwd()),
      replacement: '<repo>',
    },
    ...staticReplacements,
  ]
}

export function scrubPublicArtifactText(text: string, options: ScrubOptions = {}): string {
  return replacementsFor(options).reduce(
    (current, item) => current.replace(item.pattern, item.replacement),
    text,
  )
}

export function scrubPublicArtifactValue<T>(value: T, options: ScrubOptions = {}): T {
  if (typeof value === 'string') {
    return scrubPublicArtifactText(value, options) as T
  }
  if (Array.isArray(value)) {
    return value.map((item) => scrubPublicArtifactValue(item, options)) as T
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, scrubPublicArtifactValue(item, options)]),
    ) as T
  }
  return value
}
