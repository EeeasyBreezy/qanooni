from abc import ABC, abstractmethod
from typing import List, Optional

from app.services.model.DocumentMetadata import DocumentMetadata


class IDocumentRepository(ABC):
    @abstractmethod
    def create_document(
        self,
        *,
        file_name: str,
        mime_type: str,
        size_bytes: int,
        text: str,
        metadata: DocumentMetadata,
    ) -> int:
        """Persists a single document and returns its ID."""
        raise NotImplementedError

    @abstractmethod
    def bulk_create_documents(
        self,
        documents: List[dict],
    ) -> List[int]:
        """Persists multiple documents and returns their IDs.

        Each dict must contain: file_name, mime_type, size_bytes, text, metadata
        """
        raise NotImplementedError


