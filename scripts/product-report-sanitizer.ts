const sep = String.raw`(?:\\+|/)`
const segment = String.raw`[^\\/"]+`
const userSegment = String.raw`[^\\/"]+`

const replacements: Array<{ pattern: RegExp; replacement: string }> = [
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

export function scrubPublicArtifactText(text: string): string {
  return replacements.reduce(
    (current, item) => current.replace(item.pattern, item.replacement),
    text,
  )
}

export function scrubPublicArtifactValue<T>(value: T): T {
  if (typeof value === 'string') {
    return scrubPublicArtifactText(value) as T
  }
  if (Array.isArray(value)) {
    return value.map((item) => scrubPublicArtifactValue(item)) as T
  }
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, item]) => [key, scrubPublicArtifactValue(item)]),
    ) as T
  }
  return value
}
