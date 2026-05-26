import type { StdoutMessage } from 'src/entrypoints/sdk/controlTypes.js'

export interface Transport {
  connect(): Promise<void>
  close(): void
  write(message: StdoutMessage): Promise<void>
  isConnectedStatus(): boolean
  setOnData(callback: (data: string) => void): void
  setOnClose(callback: (closeCode?: number) => void): void
  setOnConnect?(callback: () => void): void
}
