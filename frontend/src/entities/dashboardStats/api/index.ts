
import { httpClient } from '@shared/http/httpClient';
import { dashboardApiPaths } from '../apiPaths';
import type { DashboardStatsDTO } from '../dto/DashboardStatsDTO';

export const getDashboardStats = async (): Promise<DashboardStatsDTO> => {
  return httpClient.get<DashboardStatsDTO>(dashboardApiPaths.root);
};


