import React from "react";
import Typography from "@shared/components/Typography";
import Box from "@shared/components/Box";
import PieChart from "@shared/components/charts/PieChart";
import { useCountries } from "@entities/dashboardStats/queries/useCountries";
import Loader from "@shared/components/Loader";
import Alert from "@shared/components/Alert";

export const GoverningLawChart: React.FC = () => {
  const { isLoading, isError, data } = useCountries();

  if (isLoading) return <Loader />;
  if (isError)
    return <Alert severity="error">Error loading governing law</Alert>;
  if (!data) return <Alert severity="error">No data available</Alert>;

  const pieData = data.map(({ category, count }) => ({
    name: category,
    value: count,
  }));

  return (
    <Box sx={{ flex: 1 }}>
      <Typography variant="h6">Governing Law</Typography>
      <PieChart data={pieData} testId="governing-law-chart" />
    </Box>
  );
};

export default GoverningLawChart;
