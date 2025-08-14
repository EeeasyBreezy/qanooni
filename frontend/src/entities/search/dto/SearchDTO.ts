export type SearchRequestDTO = {
  question: string;
  limit: number;
  offset: number;
};

export type SearchResultRowDTO = {
  document: string;
  governing_law: string | null;
  agreement_type: string | null;
  industry: string | null;
  score: number | null;
};

export type SearchResponseDTO = {
  items: SearchResultRowDTO[];
  limit: number;
  offset: number;
  total: number;
};


