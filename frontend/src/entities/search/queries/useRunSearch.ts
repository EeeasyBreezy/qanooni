import { useMutation } from '@tanstack/react-query';
import { runSearch } from '../api';
import type { SearchRequestDTO } from '../dto/SearchDTO';
import { mapSearchResultDtoToModel } from '../model/mapping/searchMapper';

export const useRunSearch = () => {
  return useMutation({
    mutationFn: async (payload: SearchRequestDTO) => {
      const rows = await runSearch(payload);
      return mapSearchResultDtoToModel(rows);
    },
  });
};


