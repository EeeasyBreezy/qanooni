export type SearchResultRow = {
  document: string;
  governingLaw: string | null;
  agreementType: string | null;
  industry: string | null;
  score: number | null;
};

export type SearchParams = {
  question: string;
  limit?: number;
  offset?: number;
};


