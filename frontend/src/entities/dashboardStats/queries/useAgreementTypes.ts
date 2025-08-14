import { useQuery } from '@tanstack/react-query';
import { getAgreementTypeCounts } from '../api';
import { dashboardStatsQueryKeyFactory } from './dashboardStatsQueryKeyFactory';
import { mapAggregationDtoListToModel } from '../mapping/aggregationMapper';
import type { AggregationResult } from '../model/AggregationResult';

export const useAgreementTypes = () =>
  useQuery({
    queryKey: dashboardStatsQueryKeyFactory.agreementTypes(),
    queryFn: async (): Promise<AggregationResult[]> => {
      const dto = await getAgreementTypeCounts();
      return mapAggregationDtoListToModel(dto);
    },
  });


