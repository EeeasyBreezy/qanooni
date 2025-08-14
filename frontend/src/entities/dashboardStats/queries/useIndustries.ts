import { useQuery } from '@tanstack/react-query';
import { getIndustryCounts } from '../api';
import { dashboardStatsQueryKeyFactory } from './dashboardStatsQueryKeyFactory';
import { mapAggregationDtoPageToModel } from '../mapping/aggregationMapper';
import type { AggregationResult } from '../model/AggregationResult';
import type { IndustriesQueryParams } from '../model/IndustriesQueryParams';
import type { Pagination } from '@shared/types/Pagination';

export const useIndustries = (params: IndustriesQueryParams) =>
  useQuery({
    queryKey: dashboardStatsQueryKeyFactory.industries(params),
    queryFn: async (): Promise<Pagination<AggregationResult>> => {
      const page = await getIndustryCounts(params);
      return mapAggregationDtoPageToModel(page);
    },
  });


