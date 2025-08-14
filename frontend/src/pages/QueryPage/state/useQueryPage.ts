import React from 'react';
import { useRunSearch } from '@entities/search/queries/useRunSearch';
import type { GridPaginationModel } from '@shared/components/DataGrid';

const DEFAULT_PAGE_SIZE = 10;

export const useQueryPage = () => {
  const [question, setQuestion] = React.useState('');
  const [page, setPage] = React.useState(0);
  const [pageSize, setPageSize] = React.useState(DEFAULT_PAGE_SIZE);
  const { mutateAsync, data, isPending, reset } = useRunSearch();

  const submit = async () => {
    setPage(0);
    await mutateAsync({ question, limit: pageSize, offset: 0 });
  };

  const clear = () => {
    reset();
    setQuestion('');
  };

  const onPaginationModelChange = async (m: GridPaginationModel) => {
    const nextPage = m.page;
    const nextPageSize = m.pageSize;
    setPage(nextPage);
    setPageSize(nextPageSize);
    await mutateAsync({ question, limit: nextPageSize, offset: nextPage * nextPageSize });
  };

  const canSubmit = question.trim().length > 0 && !isPending;

  return { question, setQuestion, page, pageSize, isPending, data, canSubmit, submit, clear, onPaginationModelChange };
};


