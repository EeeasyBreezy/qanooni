from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.repositories.entities.AggregationResultEntity import AggregationResultEntity

from app.repositories.entities.DocumentEntity import DocumentEntity
from app.common.model.Pagination import Pagination
from app.common.model.Pagination import Pagination
from app.repositories.entities.DocumentChunkEntity import DocumentChunkEntity


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
    ) -> Pagination[Dict[str, Any]]:
        """Full-text search joined with optional metadata filters, returns paginated items + total count."""
        raise NotImplementedError

    # Segregated aggregation methods
    @abstractmethod
    def count_by_agreement_type(self) -> List[AggregationResultEntity]:
        """Returns a list of AggregationResultEntity grouped by agreement_type."""
        raise NotImplementedError

    @abstractmethod
    def count_by_country(self) -> List[AggregationResultEntity]:
        """Returns a list of AggregationResultEntity grouped by jurisdiction (country)."""
        raise NotImplementedError

    @abstractmethod
    def count_by_industry(self, *, limit: int = 10, offset: int = 0, sort: str = "desc") -> Pagination[AggregationResultEntity]:
        """Returns a paginated list of AggregationResultEntity sorted by count. sort: 'asc' | 'desc'."""
        raise NotImplementedError

    # Chunk persistence
    @abstractmethod
    def bulk_create_document_chunks(self, chunks: List[DocumentChunkEntity]) -> List[int]:
        """Persists multiple document chunks and returns their IDs."""
        raise NotImplementedError

    @abstractmethod
    def search_vector(
        self,
        *,
        query_vector: List[float],
        jurisdiction: Optional[str],
        agreement_type: Optional[str],
        limit: int = 50,
        offset: int = 0,
    ) -> Pagination[Dict[str, Any]]:
        """Vector similarity search over chunks joined with metadata filters; falls back to text search if unsupported."""
        raise NotImplementedError


