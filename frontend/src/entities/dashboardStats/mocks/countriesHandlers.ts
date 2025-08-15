import { http, HttpResponse, delay } from 'msw';
import { dashboardApiPaths } from '../apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const url = `*${dashboardApiPaths.countries}`

const success = http.get(url, async () =>
  HttpResponse.json([
    { category: 'UAE', count: 3 },
    { category: 'UK', count: 1 },
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

export const countriesHandlers = {
  default: success,
  loading,
  error,
};


