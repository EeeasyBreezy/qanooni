import { http, HttpResponse, delay } from 'msw';
import { dashboardApiPaths } from '@entities/dashboardStats/apiPaths';

type Options = {
  mode?: 'success' | 'error' | 'loading';
  status?: number;
  delayMs?: number;
};

export const createDashboardHandlers = (opts: Options = {}) => {
  const { mode = 'success', status = 500, delayMs = 300 } = opts;

  return [
    http.get(dashboardApiPaths.root, async () => {
      if (mode === 'loading') {
        await delay(delayMs);
      }
      if (mode === 'error') {
        return HttpResponse.json({ message: 'Failed' }, { status });
      }
      return HttpResponse.json({
        agreement_types: { NDA: 4, MSA: 2 },
        jurisdictions: { UAE: 3, UK: 1 },
        industries: { Technology: 2, 'Oil & Gas': 1 },
      });
    }),
  ];
};


