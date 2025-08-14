import { http, HttpResponse, delay } from 'msw';
import { searchApiPaths } from '@entities/search/apiPaths';

type Options = {
  mode?: 'success' | 'error' | 'loading';
  status?: number;
  delayMs?: number;
};

export const createSearchHandlers = (opts: Options = {}) => {
  const { mode = 'success', status = 500, delayMs = 300 } = opts;
  return [
    http.post(searchApiPaths.root, async () => {
      if (mode === 'loading') {
        await delay(delayMs);
      }
      if (mode === 'error') {
        return HttpResponse.json({ message: 'Search failed' }, { status });
      }
      return HttpResponse.json([
        {
          document: 'nda_abudhabi.pdf',
          governing_law: 'UAE',
          agreement_type: 'NDA',
          industry: 'Technology',
          score: 0.1,
        },
      ]);
    }),
  ];
};


