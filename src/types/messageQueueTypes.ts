export type QueueOperation = 'enqueue' | 'dequeue' | 'remove' | 'clear' | 'popAll'

export type QueueOperationMessage = {
  type: 'queue-operation'
  operation: QueueOperation
  timestamp: string
  sessionId?: string
  content?: string
  [key: string]: unknown
}
