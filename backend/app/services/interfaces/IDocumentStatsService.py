from abc import ABC, abstractmethod
from typing import List

from app.services.model.AggregationResult import AggregationResult


class IDocumentStatsService(ABC):
    @abstractmethod
    def get_agreement_type_counts(self) -> List[AggregationResult]:
        raise NotImplementedError

    @abstractmethod
    def get_country_counts(self) -> List[AggregationResult]:
        raise NotImplementedError

    @abstractmethod
    def get_industry_counts(self, *, limit: int = 10, offset: int = 0, sort: str = "desc") -> List[AggregationResult]:
        raise NotImplementedError


