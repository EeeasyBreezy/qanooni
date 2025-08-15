import React from "react";
import {
  BarChart as RBarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

export type BarDatum = { name: string; value: number };

type Props = {
  data: BarDatum[];
  color?: string;
  height?: number;
  testId?: string;
};

const BarChart: React.FC<Props> = ({
  data,
  color = "#1976d2",
  height = 260,
  testId,
}) => {
  return (
    <div data-testid={testId}>
      <ResponsiveContainer width="100%" height={height}>
        <RBarChart
          data={data}
          margin={{ top: 8, right: 16, left: 0, bottom: 8 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="value" fill={color} />
        </RBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChart;
