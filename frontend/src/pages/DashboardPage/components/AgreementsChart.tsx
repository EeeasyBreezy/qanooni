import { Box, Typography } from "@mui/material";
import BarChart from "@shared/components/charts/BarChart";
import { useAgreementTypes } from "@entities/dashboardStats/queries/useAgreementTypes";
import Loader from "@shared/components/Loader";
import Alert from "@shared/components/Alert";

export function AgreementsChart() {
  const { isLoading, isError, data: agreementBarData } = useAgreementTypes();

  if (isLoading) return <Loader />;
  if (isError) return <Alert severity="error">Error loading agreements</Alert>;
  if (!agreementBarData)
    return <Alert severity="error">No data available</Alert>;

  return (
    <Box sx={{ flex: 1 }}>
      <Typography variant="h6">Agreements by Type</Typography>
      <BarChart
        data={agreementBarData.map(({ category, count }) => ({
          name: category,
          value: count,
        }))}
      />
    </Box>
  );
}
