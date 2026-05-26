import { useContext } from 'react'
import type { WizardContextValue, WizardData } from './types.js'
import { WizardContext } from './WizardProvider.js'

export function useWizard<
  T extends WizardData = WizardData,
>(): WizardContextValue<T> {
  const context = useContext(WizardContext) as WizardContextValue<T> | null
  if (!context) {
    throw new Error('useWizard must be used within a WizardProvider')
  }
  return context
}
