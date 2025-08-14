import React from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'
import { config } from '@shared/config/env'


if (config.useMocks) {
  const { worker } = await import('./mocks/browser')
  await worker.start({ onUnhandledRequest: 'bypass' })
}

const container = document.getElementById('root')
if (!container) {
  throw new Error('Root container not found')
}

const root = createRoot(container)
root.render(<React.StrictMode><App /></React.StrictMode>)