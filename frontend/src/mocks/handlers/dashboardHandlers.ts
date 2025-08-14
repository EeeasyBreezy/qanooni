import { http, HttpResponse, delay } from 'msw';
import { dashboardApiPaths } from '@entities/dashboardStats/apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const success = http.get(dashboardApiPaths.root, async () =>
  HttpResponse.json({
    agreement_types: { NDA: 4, MSA: 2 },
    jurisdictions: { UAE: 3, UK: 1 },
    industries: { Technology: 2, 'Oil & Gas': 1 },
  })
);

const loading = (delayMs: number) =>
  http.get(dashboardApiPaths.root, async () => {
    await delay(delayMs);
    return HttpResponse.json({
      agreement_types: {},
      jurisdictions: {},
      industries: {},
    });
  });

const error = (status: ApiStatusCode) =>
  http.get(dashboardApiPaths.root, async () =>
    HttpResponse.json({ message: 'Failed' }, { status })
  );

export const dashboardHandlers = {
  default: success,
  loading,
  error,
};


