import { setupWorker } from 'msw/browser';
import { handlers as dashboardHandlers } from '@entities/dashboardStats/mocks/handlers';
import { handlers as filesHandlers } from '@entities/files/mocks/handlers';
import { handlers as searchHandlers } from '@entities/search/mocks/handlers';

export const worker = setupWorker(
  dashboardHandlers.default,
  filesHandlers.default,
  searchHandlers.default,
);


 
 