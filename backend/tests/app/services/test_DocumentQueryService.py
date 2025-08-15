from typing import Any, Dict, List, Optional

from app.common.model.Pagination import Pagination
from app.services.implementations.DocumentQueryService import DocumentQueryService
from app.services.implementations.MetadataExtractor import MetadataExtractor
from app.services.interfaces.IEmbeddingService import IEmbeddingService
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository


class _FakeEmbeddings(IEmbeddingService):
    def __init__(self, dim: int = 384) -> None:
        self._dim = dim

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [[0.0] * self._dim for _ in texts]

    def dimension(self) -> int:
        return self._dim


class _FakeRepo(IDocumentRepository):
    def __init__(self) -> None:
        self.last_args: Dict[str, Any] = {}

    # Unused in this test suite
    def create_document(self, document) -> int:  # type: ignore[no-untyped-def]
        return 0

    def bulk_create_documents(self, documents) -> List[int]:  # type: ignore[no-untyped-def]
        return []

    def bulk_create_document_chunks(self, chunks) -> List[int]:  # type: ignore[no-untyped-def]
        return []

    def count_by_agreement_type(self):  # type: ignore[no-untyped-def]
        return []

    def count_by_country(self):  # type: ignore[no-untyped-def]
        return []

    def count_by_industry(self, *, limit: int = 10, offset: int = 0, sort: str = "desc") -> Pagination:  # type: ignore[no-untyped-def]
        return Pagination(items=[], offset=offset, limit=limit, total=0)

    def search_vector(
        self,
        *,
        query_vector: List[float],
        jurisdiction: Optional[str],
        agreement_type: Optional[str],
        limit: int = 50,
        offset: int = 0,
    ) -> Pagination[Dict[str, Any]]:
        self.last_args = {
            "query_vector_len": len(query_vector),
            "jurisdiction": jurisdiction,
            "agreement_type": agreement_type,
            "limit": limit,
            "offset": offset,
        }
        # Return two chunks from two docs; doc 1 has higher score
        items: List[Dict[str, Any]] = [
            {"document_id": 1, "file_name": "a.pdf", "jurisdiction": "California", "agreement_type": "Non-Disclosure Agreement", "industry": "Tech", "score": 0.9},
            {"document_id": 2, "file_name": "b.pdf", "jurisdiction": "California", "agreement_type": "Non-Disclosure Agreement", "industry": "Tech", "score": 0.5},
        ]
        return Pagination(items=items, offset=offset, limit=limit, total=2)


class TestDocumentQueryService:
    def test_uses_metadata_extractor_filters(self) -> None:
        repo = _FakeRepo()
        svc = DocumentQueryService(
            repository=repo,
            embeddings=_FakeEmbeddings(),
            metadata_extractor=MetadataExtractor(),
        )

        question = "This NDA is governed by the laws of California."
        page = svc.run_query(question=question, limit=10, offset=0)

        # Assert repo was called with extracted filters
        assert repo.last_args.get("jurisdiction") in {"California", "United States"}
        assert repo.last_args.get("agreement_type") == "Non-Disclosure Agreement"

        # Assert aggregation returned unique docs
        assert len(page.items) == 2
        assert page.items[0].document == "a.pdf"


