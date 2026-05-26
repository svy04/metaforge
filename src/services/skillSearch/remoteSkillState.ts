export type DiscoveredRemoteSkill = {
  slug: string
  url: string
}

export function getRemoteSkillState(): null {
  return null
}

export function stripCanonicalPrefix(name: string): string | null {
  return name.startsWith('_canonical_') ? name.slice('_canonical_'.length) : null
}

export function getDiscoveredRemoteSkill(_slug: string): DiscoveredRemoteSkill | null {
  return null
}
