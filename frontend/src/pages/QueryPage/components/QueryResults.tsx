import React from "react";
import Box from "@shared/components/Box";
import DataGrid, {
  type GridColDef,
  type GridPaginationModel,
} from "@shared/components/DataGrid";

type Props = {
  data: { items: Array<Record<string, unknown>>; total: number } | undefined;
  page: number;
  pageSize: number;
  isPending: boolean;
  onPaginationModelChange: (m: GridPaginationModel) => void | Promise<void>;
};

export const QueryResults: React.FC<Props> = ({
  data,
  page,
  pageSize,
  isPending,
  onPaginationModelChange,
}) => {
  const rows = React.useMemo(
    () =>
      (data?.items ?? []).map((r, i) => ({ id: i + page * pageSize, ...r })),
    [data, page, pageSize]
  );
  const rowCount = data?.total ?? 0;
  const columns: GridColDef[] = React.useMemo(() => {
    const first = data?.items?.[0] as Record<string, unknown> | undefined;
    if (!first) return [];
    return Object.keys(first).map((k) => ({
      field: k,
      headerName: k.replace(/_/g, " "),
      flex: 1,
    }));
  }, [data]);

  return (
    <Box sx={{ mt: 2 }}>
      <DataGrid
        autoHeight
        disableColumnFilter
        disableRowSelectionOnClick
        disableMultipleRowSelection
        rows={rows}
        columns={columns}
        loading={isPending}
        rowCount={rowCount}
        paginationMode="server"
        paginationModel={{ page, pageSize }}
        pageSizeOptions={[5, 10, 25, 50]}
        onPaginationModelChange={onPaginationModelChange}
        data-testid="query-results"
      />
    </Box>
  );
};
