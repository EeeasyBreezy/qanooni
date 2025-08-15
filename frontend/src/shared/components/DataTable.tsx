import React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

export type Column<T> = {
  key: keyof T | string;
  header: string;
  render?: (row: T) => React.ReactNode;
  width?: number | string;
};

type DataTableProps<T> = {
  columns: Column<T>[];
  rows: T[];
  getRowId: (row: T, index: number) => string | number;
  testId?: string;
};

const DataTable = <T,>({
  columns,
  rows,
  getRowId,
  testId,
}: DataTableProps<T>) => {
  return (
    <Paper elevation={0} variant="outlined">
      <Table size="small" data-testid={testId}>
        <TableHead>
          <TableRow>
            {columns.map((c) => (
              <TableCell key={String(c.key)} style={{ width: c.width }}>
                {c.header}
              </TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((r, idx) => (
            <TableRow key={getRowId(r, idx)}>
              {columns.map((c) => (
                <TableCell key={String(c.key)}>
                  {c.render ? c.render(r) : (r as any)[c.key]}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
};

export default DataTable;
