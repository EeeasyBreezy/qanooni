import React from "react";
import Typography from "@shared/components/Typography";
import Box from "@shared/components/Box";
import DataGrid, { type GridColDef } from "@shared/components/DataGrid";
import { useIndustriesTable } from "../state/useIndustriesTable";

export const IndustriesTable: React.FC = () => {
  const {
    isLoading,
    rows,
    rowCount,
    page,
    pageSize,
    onPaginationModelChange,
    onSortModelChange,
  } = useIndustriesTable();

  const columns: GridColDef[] = [
    { field: "category", headerName: "Industry", flex: 1, sortable: false },
    { field: "count", headerName: "Count", width: 120, sortable: true },
  ];

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>
        Industry Coverage
      </Typography>
      <Box sx={{ width: "100%" }}>
        <DataGrid
          autoHeight
          rows={rows}
          columns={columns}
          loading={isLoading}
          rowCount={rowCount}
          paginationMode="server"
          sortingMode="server"
          initialState={{
            sorting: { sortModel: [{ field: "count", sort: "desc" }] },
          }}
          onSortModelChange={onSortModelChange}
          pageSizeOptions={[5, 10, 25, 50]}
          paginationModel={{ page, pageSize }}
          onPaginationModelChange={onPaginationModelChange}
        />
      </Box>
    </Box>
  );
};

export default IndustriesTable;
