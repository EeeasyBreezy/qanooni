import React from 'react';
import { useDashboardStats } from '@entities/dashboardStats/queries/useDashboardStats';
import type { DashboardStats } from '@entities/dashboardStats/model/DashboardStats';

export const useDashboardPage = () => {
  const { data, isLoading, isError, refetch } = useDashboardStats();

  const agreementBarData = React.useMemo(() => {
    const s = data as DashboardStats | undefined;
    if (!s) return [] as Array<{ name: string; value: number }>;
    return Object.entries(s.agreementTypes).map(([name, value]) => ({ name, value }));
  }, [data]);

  const jurisdictionsPieData = React.useMemo(() => {
    const s = data as DashboardStats | undefined;
    if (!s) return [] as Array<{ name: string; value: number }>;
    return Object.entries(s.jurisdictions).map(([name, value]) => ({ name, value }));
  }, [data]);

  return { stats: data, isLoading, isError, refetch, agreementBarData, jurisdictionsPieData };
};


