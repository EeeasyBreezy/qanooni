import { useMutation } from '@tanstack/react-query';
import { runSearch } from '../api';
import type { SearchRequestDTO } from '../dto/SearchDTO';
import { mapSearchResultDtoToModel } from '../model/mapping/searchMapper';

export const useRunSearch = () =>
  useMutation({
    mutationFn: async (payload: SearchRequestDTO) => {
      const res = await runSearch(payload);
      return {
        items: mapSearchResultDtoToModel(res.items),
        limit: res.limit,
        offset: res.offset,
        total: res.total,
      };
    },
  });


