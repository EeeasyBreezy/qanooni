import { useQuery } from '@tanstack/react-query';
import { getCountryCounts } from '../api';
import { dashboardStatsQueryKeyFactory } from './dashboardStatsQueryKeyFactory';
import { mapAggregationDtoListToModel } from '../mapping/aggregationMapper';
import type { AggregationResult } from '../model/AggregationResult';

export const useCountries = () =>
  useQuery({
    queryKey: dashboardStatsQueryKeyFactory.countries(),
    queryFn: async (): Promise<AggregationResult[]> => {
      const dto = await getCountryCounts();
      return mapAggregationDtoListToModel(dto);
    },
  });


