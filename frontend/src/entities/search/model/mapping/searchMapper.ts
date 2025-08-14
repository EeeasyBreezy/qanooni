import type { SearchResultRow } from '../Search';
import type { SearchResultRowDTO } from '../../dto/SearchDTO';

export const mapSearchResultDtoToModel = (rows: SearchResultRowDTO[]): SearchResultRow[] =>
  rows.map((r) => ({
    document: r.document,
    governingLaw: r.governing_law ?? null,
    agreementType: r.agreement_type ?? null,
    industry: r.industry ?? null,
    score: r.score ?? null,
  }));


