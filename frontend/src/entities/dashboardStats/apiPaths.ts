import type { IndustriesQueryParams } from './model/IndustriesQueryParams';

export const dashboardApiPaths = {
  root: '/dashboard',
  agreementTypes: '/dashboard/agreement-types',
  countries: '/dashboard/countries',
  industries: (params: IndustriesQueryParams) => {
    const query = new URLSearchParams();
    query.set('limit', String(params.limit));
    query.set('offset', String(params.offset));
    query.set('sort', params.sort ?? 'desc');
    return `/dashboard/industries?${query.toString()}`;
  },
} as const;


