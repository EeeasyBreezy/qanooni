import React from "react";
import Typography from "@shared/components/Typography";
import Box from "@shared/components/Box";
import PieChart from "@shared/components/charts/PieChart";
import { useCountries } from "@entities/dashboardStats/queries/useCountries";

export const GoverningLawChart: React.FC = () => {
  const { data = [] } = useCountries();

  const pieData = React.useMemo(
    () => data.map(({ category, count }) => ({ name: category, value: count })),
    [data]
  );

  return (
    <Box sx={{ flex: 1 }}>
      <Typography variant="h6">Governing Law</Typography>
      <PieChart data={pieData} />
    </Box>
  );
};

export default GoverningLawChart;
