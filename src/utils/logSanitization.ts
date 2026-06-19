function stringifyForLog(value: unknown): string {
  if (typeof value === 'string') {
    return value
  }
  if (value instanceof Error) {
    return value.message
  }

  try {
    const serialized = JSON.stringify(value, (_key, nestedValue: unknown) => {
      if (nestedValue instanceof Error) {
        return sanitizePlainTextLogValue(nestedValue.message)
      }
      return typeof nestedValue === 'string'
        ? sanitizePlainTextLogValue(nestedValue)
        : nestedValue
    })
    return serialized ?? String(value)
  } catch {
    return String(value)
  }
}

export function sanitizePlainTextLogValue(value: unknown): string {
  return stringifyForLog(value)
    .replace(/[\r\n\u0085\u2028\u2029]+/g, ' ')
    .replace(/\t+/g, ' ')
    .replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/g, '')
}
