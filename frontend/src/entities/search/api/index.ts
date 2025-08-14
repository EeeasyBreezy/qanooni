import { httpClient } from '@shared/http/httpClient';
import { searchApiPaths } from '../apiPaths';
import type { SearchRequestDTO, SearchResultRowDTO } from '../dto/SearchDTO';

export const runSearch = async (payload: SearchRequestDTO): Promise<SearchResultRowDTO[]> => {
  return httpClient.post<SearchResultRowDTO[]>(searchApiPaths.root, payload);
};


