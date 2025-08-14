import { httpClient } from '@shared/http/httpClient';
import { searchApiPaths } from '../apiPaths';
import type { SearchRequestDTO, SearchResponseDTO } from '../dto/SearchDTO';

export const runSearch = async (payload: SearchRequestDTO): Promise<SearchResponseDTO> => {
  const params = new URLSearchParams();
  params.set('question', payload.question);
  params.set('limit', String(payload.limit));
  params.set('offset', String(payload.offset));
  return httpClient.get<SearchResponseDTO>(searchApiPaths.root, {
    params,
  });
};


