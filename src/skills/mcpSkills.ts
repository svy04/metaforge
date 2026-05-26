type CachedFetch = ((client: unknown) => Promise<unknown[]>) & {
  cache: {
    delete(key: string): void
  }
}

export const fetchMcpSkillsForClient: CachedFetch = Object.assign(
  async (_client: unknown) => [],
  {
    cache: {
      delete(_key: string) {},
    },
  },
)
