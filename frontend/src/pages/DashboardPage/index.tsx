import React from 'react';
import PageContainer from '@shared/components/PageContainer';
import Typography from '@shared/components/Typography';
import Stack from '@shared/components/Stack';
import DataTable from '@shared/components/DataTable';
import BarChart from '@shared/components/charts/BarChart';
import PieChart from '@shared/components/charts/PieChart';
import { useDashboardPage } from './state/useDashboardPage';

export function DashboardPage() {
  const { stats, isLoading, isError, agreementBarData, jurisdictionsPieData } = useDashboardPage();

  const industryRows = React.useMemo(() => {
    return stats ? Object.entries(stats.industries).map(([name, value]) => ({ name, value })) : [];
  }, [stats]);

  const columns = [
    { key: 'name', header: 'Name' },
    { key: 'value', header: 'Count' },
  ] as const;

  return (
    <PageContainer isLoading={isLoading} error={isError ? 'Error loading dashboard data' : undefined}>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>

      <Stack direction="row" spacing={2}>
        <div style={{ flex: 1 }}>
          <Typography variant="h6">Agreements by Type</Typography>
          <BarChart data={agreementBarData} />
        </div>
        <div style={{ flex: 1 }}>
          <Typography variant="h6">Governing Law</Typography>
          <PieChart data={jurisdictionsPieData} />
        </div>
      </Stack>

      <Stack spacing={2} sx={{ mt: 3 }}>
        <Typography variant="h6">Industry Coverage</Typography>
        <DataTable columns={columns as any} rows={industryRows} getRowId={(r) => r.name} />
      </Stack>
    </PageContainer>
  );
};

export default DashboardPage;


