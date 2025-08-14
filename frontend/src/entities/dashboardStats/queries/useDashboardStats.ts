import { useQuery } from '@tanstack/react-query';
import { getDashboardStats } from '../api';
import { dashboardStatsQueryKeyFactory } from './dashboardStatsQueryKeyFactory';
import { type DashboardStats } from '../model/DashboardStats';
import { mapDashboardStatsDtoToModel } from '../mapping/dashboardStatsMapper';

export const useDashboardStats = () => {
  return useQuery({
    queryKey: dashboardStatsQueryKeyFactory.all,
    queryFn: async (): Promise<DashboardStats> => {
      const dto = await getDashboardStats();
      return mapDashboardStatsDtoToModel(dto);
    },
  });
};


