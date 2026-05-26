function unsupportedAntHandler(): never {
  throw new Error('The internal ant handler is not included in this source snapshot.')
}

export function logHandler(_logId?: string | number): never {
  return unsupportedAntHandler()
}

export function errorHandler(_number?: number): never {
  return unsupportedAntHandler()
}

export function exportHandler(_source: string, _outputFile: string): never {
  return unsupportedAntHandler()
}

export function taskCreateHandler(_subject: string, _opts?: unknown): never {
  return unsupportedAntHandler()
}

export function taskListHandler(_opts?: unknown): never {
  return unsupportedAntHandler()
}

export function taskGetHandler(_id: string, _opts?: unknown): never {
  return unsupportedAntHandler()
}

export function taskUpdateHandler(_id: string, _opts?: unknown): never {
  return unsupportedAntHandler()
}

export function taskDirHandler(_opts?: unknown): never {
  return unsupportedAntHandler()
}

export function completionHandler(_shell: string, _opts?: unknown, _program?: unknown): never {
  return unsupportedAntHandler()
}
