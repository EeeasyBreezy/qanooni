from typing import List

from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.repositories.entities.AggregationResultEntity import AggregationResultEntity
from app.services.interfaces.IDocumentStatsService import IDocumentStatsService
from app.services.model.AggregationResult import AggregationResult


class DocumentStatsService(IDocumentStatsService):
    def __init__(self, repository: IDocumentRepository):
        self._repo = repository

    def _map_entity(self, e: AggregationResultEntity) -> AggregationResult:
        return AggregationResult(category=e.category, count=e.count)

    def get_agreement_type_counts(self) -> List[AggregationResult]:
        rows = self._repo.count_by_agreement_type()
        return [self._map_entity(r) for r in rows]

    def get_country_counts(self) -> List[AggregationResult]:
        rows = self._repo.count_by_country()
        return [self._map_entity(r) for r in rows]

    def get_industry_counts(self, *, limit: int = 10, offset: int = 0, sort: str = "desc") -> List[AggregationResult]:
        rows = self._repo.count_by_industry(limit=limit, offset=offset, sort=sort)
        return [self._map_entity(r) for r in rows]


