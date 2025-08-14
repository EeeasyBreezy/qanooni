import { setupWorker } from 'msw/browser';
import { dashboardHandlers } from './handlers/dashboardHandlers';
import { filesHandlers } from './handlers/filesHandlers';
import { searchHandlers } from './handlers/searchHandlers';

export const worker = setupWorker(
  dashboardHandlers.default,
  filesHandlers.default,
  searchHandlers.default,
);


 
 