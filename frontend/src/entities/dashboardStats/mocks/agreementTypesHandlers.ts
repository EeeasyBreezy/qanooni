import { http, HttpResponse, delay } from 'msw';
import { dashboardApiPaths } from '../apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const url = `*${dashboardApiPaths.agreementTypes}`

const success = http.get(url, async () =>
  HttpResponse.json([
    { category: 'NDA', count: 4 },
    { category: 'MSA', count: 2 },
  ])
);

const loading = (delayMs: number) =>
  http.get(url, async () => {
    await delay(delayMs);
    return HttpResponse.json([]);
  });

const error = (status: ApiStatusCode) =>
  http.get(url, async () =>
    HttpResponse.json({ message: 'Failed' }, { status })
  );

export const agreementTypesHandlers = {
  default: success,
  loading,
  error,
};


