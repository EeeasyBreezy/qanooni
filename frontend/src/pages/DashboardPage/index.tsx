import React from "react";
import PageContainer from "@shared/components/PageContainer";
import Typography from "@shared/components/Typography";
import Stack from "@shared/components/Stack";
import BarChart from "@shared/components/charts/BarChart";
import PieChart from "@shared/components/charts/PieChart";
import { useDashboardPage } from "./state/useDashboardPage";

export function DashboardPage() {
  const { isLoading, isError, agreementBarData, jurisdictionsPieData } =
    useDashboardPage();

  return (
    <PageContainer
      isLoading={isLoading}
      error={isError ? "Error loading dashboard data" : undefined}
    >
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

      {/* Industry coverage table moved to a dedicated view using useIndustries() */}
    </PageContainer>
  );
}

export default DashboardPage;
