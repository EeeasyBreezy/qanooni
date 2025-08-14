import type { AggregationResultDTO } from '../dto/AggregationResultDTO';
import type { AggregationResult } from '../model/AggregationResult';

export const mapAggregationDtoListToModel = (dto: AggregationResultDTO[]): AggregationResult[] =>
  dto.map((r) => ({ category: r.category, count: r.count }));


