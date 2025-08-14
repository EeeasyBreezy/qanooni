import { http, HttpResponse, delay } from 'msw';
import { searchApiPaths } from '@entities/search/apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const success = http.post(searchApiPaths.root, async () =>
  HttpResponse.json([
    {
      document: 'nda_abudhabi.pdf',
      governing_law: 'UAE',
      agreement_type: 'NDA',
      industry: 'Technology',
      score: 0.1,
    },
  ])
);

const loading = (delayMs: number) =>
  http.post(searchApiPaths.root, async () => {
    await delay(delayMs);
    return HttpResponse.json([]);
  });

const error = (status: ApiStatusCode) =>
  http.post(searchApiPaths.root, async () =>
    HttpResponse.json({ message: 'Search failed' }, { status })
  );

export const handlers = {
  default: success,
  loading,
  error,
};


