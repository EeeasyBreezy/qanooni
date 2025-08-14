import type { IndustriesQueryParams } from '../model/IndustriesQueryParams';

export const dashboardStatsQueryKeyFactory = {
  all: ['dashboardStats'] as const,
  agreementTypes: () => [...dashboardStatsQueryKeyFactory.all, 'agreementTypes'] as const,
  countries: () => [...dashboardStatsQueryKeyFactory.all, 'countries'] as const,
  industries: (params: IndustriesQueryParams) => [
    ...dashboardStatsQueryKeyFactory.all,
    'industries',
    params.limit,
    params.offset,
    params.sort,
  ] as const,
};


