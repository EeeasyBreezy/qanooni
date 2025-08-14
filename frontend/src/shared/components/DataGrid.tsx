import React from "react";
import { DataGrid as MuiDataGrid } from "@mui/x-data-grid";

export type {
  GridColDef,
  GridPaginationModel,
  GridSortModel,
} from "@mui/x-data-grid";

type Props = React.ComponentProps<typeof MuiDataGrid>;

const DataGrid: React.FC<Props> = (props) => {
  return <MuiDataGrid {...props} />;
};

export default DataGrid;
