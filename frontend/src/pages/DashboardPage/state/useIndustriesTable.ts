import React from 'react';
import { useIndustries } from '@entities/dashboardStats/queries/useIndustries';
import type { SortOrder } from '@entities/dashboardStats/model/IndustriesQueryParams';
import type { GridPaginationModel, GridSortModel } from '@shared/components/DataGrid';

const DEFAULT_PAGE_SIZE = 10;

export const useIndustriesTable = () => {
  const [pageSize, setPageSize] = React.useState<number>(DEFAULT_PAGE_SIZE);
  const [page, setPage] = React.useState<number>(0);
  const [sort, setSort] = React.useState<SortOrder>('desc');

  const offset = page * pageSize;
  const { data, isLoading } = useIndustries({ limit: pageSize, offset, sort });

  const rows = React.useMemo(
    () => (data?.items ?? []).map((r) => ({ id: r.category, ...r })),
    [data?.items]
  );
  const rowCount = data?.total ?? 0;

  const onPaginationModelChange = (m: GridPaginationModel) => {
    if (m.pageSize !== pageSize) setPageSize(m.pageSize);
    if (m.page !== page) setPage(m.page);
  };

  const onSortModelChange = (model: GridSortModel) => {
    const s = (model[0]?.sort ?? 'desc') as SortOrder;
    setPage(0);
    setSort(s);
  };

  return {
    isLoading,
    rows,
    rowCount,
    page,
    pageSize,
    onPaginationModelChange,
    onSortModelChange,
    initialSortModel: [{ field: 'count', sort: 'desc' as const }],
    pageSizeOptions: [5, 10, 25, 50] as const,
  };
};

export type UseIndustriesTableReturn = ReturnType<typeof useIndustriesTable>;


