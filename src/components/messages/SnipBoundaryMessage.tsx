import * as React from 'react'
import { Text } from '../../ink.js'
import type { Message } from '../../types/message.js'

export function SnipBoundaryMessage(_props: { message: Message }): React.ReactNode {
  return <Text dimColor>snipped history boundary</Text>
}

