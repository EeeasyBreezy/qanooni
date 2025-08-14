import type { AggregationResultDTO } from '../dto/AggregationResultDTO';
import type { AggregationResult } from '../model/AggregationResult';
import type { Pagination } from '@shared/types/Pagination';

export const mapAggregationDtoListToModel = (dto: AggregationResultDTO[]): AggregationResult[] =>
  dto.map((r) => ({ category: r.category, count: r.count }));

export const mapAggregationDtoPageToModel = (
  page: Pagination<AggregationResultDTO>
): Pagination<AggregationResult> => ({
  items: mapAggregationDtoListToModel(page.items),
  offset: page.offset,
  limit: page.limit,
  total: page.total,
});


