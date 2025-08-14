
import { httpClient } from '@shared/http/httpClient';
import { dashboardApiPaths } from '../apiPaths';
import type { DashboardStatsDTO } from '../dto/DashboardStatsDTO';
import type { AggregationResultDTO } from '../dto/AggregationResultDTO';
import type { IndustriesQueryParams } from '../model/IndustriesQueryParams';
import type { Pagination } from '@shared/types/Pagination';

export const getDashboardStats = async (): Promise<DashboardStatsDTO> => {
  return httpClient.get<DashboardStatsDTO>(dashboardApiPaths.root);
};

export const getAgreementTypeCounts = async (): Promise<AggregationResultDTO[]> => {
  return httpClient.get<AggregationResultDTO[]>(dashboardApiPaths.agreementTypes);
};

export const getCountryCounts = async (): Promise<AggregationResultDTO[]> => {
  return httpClient.get<AggregationResultDTO[]>(dashboardApiPaths.countries);
};

export const getIndustryCounts = async (params: IndustriesQueryParams): Promise<Pagination<AggregationResultDTO>> => {
  return httpClient.get<Pagination<AggregationResultDTO>>(dashboardApiPaths.industries(params));
};


