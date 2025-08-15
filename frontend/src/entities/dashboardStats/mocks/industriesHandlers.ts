import { http, HttpResponse, delay } from 'msw';
import { dashboardApiPaths } from '../apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const url = `*${dashboardApiPaths.industries}`

const success = http.get(url, async () =>
  HttpResponse.json({
    items: [
      { category: 'Technology', count: 2 },
      { category: 'Oil & Gas', count: 1 },
    ],
    total: 2,
    limit: 10,
    offset: 0,
  })
);

const loading = (delayMs: number) =>
  http.get(url, async () => {
    await delay(delayMs);
    return HttpResponse.json({ items: [], total: 0, limit: 10, offset: 0 });
  });

const error = (status: ApiStatusCode) =>
  http.get(url, async () =>
    HttpResponse.json({ message: 'Failed' }, { status })
  );

export const industriesHandlers = {
  default: success,
  loading,
  error,
};


