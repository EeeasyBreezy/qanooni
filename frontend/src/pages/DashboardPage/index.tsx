import React from "react";
import PageContainer from "@shared/components/PageContainer";
import Typography from "@shared/components/Typography";
import Stack from "@shared/components/Stack";
import { AgreementsChart } from "./components/AgreementsChart";
import { GoverningLawChart } from "./components/GoverningLawChart";
import { IndustriesTable } from "./components/IndustriesTable";

export function DashboardPage() {
  return (
    <PageContainer>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>

      <Stack direction="row" spacing={2}>
        <AgreementsChart />
        <GoverningLawChart />
      </Stack>

      <IndustriesTable />
    </PageContainer>
  );
}

export default DashboardPage;
