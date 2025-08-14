import { useQuery } from '@tanstack/react-query';
import { getIndustryCounts } from '../api';
import { dashboardStatsQueryKeyFactory } from './dashboardStatsQueryKeyFactory';
import { mapAggregationDtoListToModel } from '../mapping/aggregationMapper';
import type { AggregationResult } from '../model/AggregationResult';
import type { IndustriesQueryParams } from '../model/IndustriesQueryParams';

export const useIndustries = (params: IndustriesQueryParams) =>
  useQuery({
    queryKey: dashboardStatsQueryKeyFactory.industries(params),
    queryFn: async (): Promise<AggregationResult[]> => {
      const dto = await getIndustryCounts(params);
      return mapAggregationDtoListToModel(dto);
    },
  });


