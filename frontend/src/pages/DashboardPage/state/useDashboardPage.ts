import React from 'react';
import { useAgreementTypes } from '@entities/dashboardStats/queries/useAgreementTypes';
import { useCountries } from '@entities/dashboardStats/queries/useCountries';

export const useDashboardPage = () => {
  const agreements = useAgreementTypes();
  const countries = useCountries();

  const agreementBarData = React.useMemo(() => {
    const items = agreements.data ?? [];
    return items.map(({ category, count }) => ({ name: category, value: count }));
  }, [agreements.data]);

  const jurisdictionsPieData = React.useMemo(() => {
    const items = countries.data ?? [];
    return items.map(({ category, count }) => ({ name: category, value: count }));
  }, [countries.data]);

  return {
    isLoading: agreements.isLoading || countries.isLoading,
    isError: agreements.isError || countries.isError,
    refetch: () => {
      void agreements.refetch();
      void countries.refetch();
    },
    agreementBarData,
    jurisdictionsPieData,
  };
};


