import React from "react";
import Typography from "@shared/components/Typography";
import Box from "@shared/components/Box";
import Stack from "@shared/components/Stack";
import { useIndustries } from "@entities/dashboardStats/queries/useIndustries";
import type { SortOrder } from "@entities/dashboardStats/model/IndustriesQueryParams";
import DataGrid, {
  type GridColDef,
  type GridPaginationModel,
  type GridSortModel,
} from "@shared/components/DataGrid";

const DEFAULT_PAGE_SIZE = 10;

export const IndustriesTable: React.FC = () => {
  const [pageSize, setPageSize] = React.useState<number>(DEFAULT_PAGE_SIZE);
  const [page, setPage] = React.useState<number>(0);
  const [sort, setSort] = React.useState<SortOrder>("desc");

  const offset = page * pageSize;
  const { data, isLoading } = useIndustries({ limit: pageSize, offset, sort });

  const rows = (data?.items ?? []).map((r) => ({ id: r.category, ...r }));
  const rowCount = data?.total ?? 0;

  const columns: GridColDef[] = [
    { field: "category", headerName: "Industry", flex: 1, sortable: false },
    { field: "count", headerName: "Count", width: 120, sortable: true },
  ];

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" sx={{ mb: 1 }}>
        Industry Coverage
      </Typography>
      <div style={{ width: "100%" }}>
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
          onSortModelChange={(model: GridSortModel) => {
            const s = (model[0]?.sort ?? "desc") as SortOrder;
            setPage(0);
            setSort(s);
          }}
          pageSizeOptions={[5, 10, 25, 50]}
          paginationModel={{ page, pageSize }}
          onPaginationModelChange={(m: GridPaginationModel) => {
            if (m.pageSize !== pageSize) setPageSize(m.pageSize);
            if (m.page !== page) setPage(m.page);
          }}
        />
      </div>
    </Box>
  );
};

export default IndustriesTable;
