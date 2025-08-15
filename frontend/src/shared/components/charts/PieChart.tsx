import React from "react";
import {
  PieChart as RPieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

export type PieDatum = { name: string; value: number };

type Props = {
  data: PieDatum[];
  colors?: string[];
  height?: number;
  testId?: string;
};

const defaultColors = [
  "#1976d2",
  "#9c27b0",
  "#ef6c00",
  "#2e7d32",
  "#d32f2f",
  "#455a64",
];

const PieChart: React.FC<Props> = ({
  data,
  colors = defaultColors,
  height = 260,
  testId,
}) => {
  return (
    <ResponsiveContainer width="100%" height={height} data-testid={testId}>
      <RPieChart>
        <Tooltip />
        <Legend />
        <Pie data={data} dataKey="value" nameKey="name" outerRadius={90} label>
          {data.map((_, idx) => (
            <Cell key={idx} fill={colors[idx % colors.length]} />
          ))}
        </Pie>
      </RPieChart>
    </ResponsiveContainer>
  );
};

export default PieChart;
