import { setupWorker } from 'msw/browser';
import { agreementTypesHandlers, countriesHandlers, industriesHandlers } from '@entities/dashboardStats/mocks/handlers';
import { handlers as filesHandlers } from '@entities/files/mocks/handlers';
import { handlers as searchHandlers } from '@entities/search/mocks/handlers';

export const worker = setupWorker(
  agreementTypesHandlers.default,
  countriesHandlers.default,
  industriesHandlers.default,
  filesHandlers.default,
  searchHandlers.default,
);


 
 