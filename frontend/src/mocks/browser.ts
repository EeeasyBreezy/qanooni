 import { setupWorker } from 'msw/browser';
import { createDashboardHandlers } from './handlers/dashboardHandlers';
import { createFilesHandlers } from './handlers/filesHandlers';
import { createSearchHandlers } from './handlers/searchHandlers';

function resolveMode(): 'success' | 'error' | 'loading' {
  const m = localStorage.getItem('msw:mode') as any
  return m === 'error' || m === 'loading' ? m : 'success'
}

export const worker = setupWorker(
  ...createDashboardHandlers({ mode: resolveMode() }),
  ...createFilesHandlers({ mode: resolveMode() }),
  ...createSearchHandlers({ mode: resolveMode() })
);


 
 