export type ParsedConnectUrl = {
  url: string
  serverUrl: string
  authToken?: string
  sessionId?: string
}

export function parseConnectUrl(url: string): ParsedConnectUrl {
  return { url, serverUrl: url }
}
