// Stub — assistant command not included in source snapshot
import React from 'react'

type NewInstallWizardProps = {
  defaultDir: string
  onInstalled: (dir: string) => void
  onCancel: () => void
  onError: (message: string) => void
}

export async function computeDefaultInstallDir(): Promise<string> {
  return ''
}

export function NewInstallWizard(_props: NewInstallWizardProps): React.ReactNode {
  return null
}

export default null
