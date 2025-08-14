from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.repositories.entities.DocumentEntity import DocumentEntity


class IDocumentRepository(ABC):
    @abstractmethod
    def create_document(self, document: DocumentEntity) -> int:
        """Persists a single document and returns its ID."""
        raise NotImplementedError

    @abstractmethod
    def bulk_create_documents(self, documents: List[DocumentEntity]) -> List[int]:
        """Persists multiple documents and returns their IDs.

        Each item is a DocumentEntity
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        *,
        fts_query: Optional[str],
        jurisdiction: Optional[str],
        agreement_type: Optional[str],
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """Full-text search joined with optional metadata filters."""
        raise NotImplementedError

    @abstractmethod
    def get_aggregations(self) -> Dict[str, Dict[str, int]]:
        """Counts for agreement_types, jurisdictions, industries."""
        raise NotImplementedError

    # Segregated aggregation methods
    @abstractmethod
    def count_by_agreement_type(self) -> Dict[str, int]:
        """Returns counts grouped by agreement_type as a mapping of value -> count."""
        raise NotImplementedError

    @abstractmethod
    def count_by_country(self) -> Dict[str, int]:
        """Returns counts grouped by jurisdiction (country) as a mapping of value -> count."""
        raise NotImplementedError

    @abstractmethod
    def count_by_industry(self, *, limit: int = 10, offset: int = 0) -> List[Dict[str, int]]:
        """Returns a list of {"key": str, "cnt": int} sorted by count desc with pagination."""
        raise NotImplementedError


