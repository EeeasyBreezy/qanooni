import type { DashboardStats } from '../model/DashboardStats';
import type { DashboardStatsDTO } from '../dto/DashboardStatsDTO';

export const mapDashboardStatsDtoToModel = (dto: DashboardStatsDTO): DashboardStats => ({
  agreementTypes: dto.agreement_types,
  jurisdictions: dto.jurisdictions,
  industries: dto.industries,
});


