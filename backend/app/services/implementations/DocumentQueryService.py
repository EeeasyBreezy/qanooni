from typing import Dict, Optional

from app.common.model.Pagination import Pagination
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.services.interfaces.IDocumentQueryService import IDocumentQueryService
from app.services.model.SearchRow import SearchRow
from app.services.interfaces.IEmbeddingService import IEmbeddingService
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor


class DocumentQueryService(IDocumentQueryService):
    def __init__(
        self,
        repository: IDocumentRepository,
        embeddings: Optional[IEmbeddingService] = None,
        metadata_extractor: Optional[IMetadataExtractor] = None,
    ):
        self._repo = repository
        self._embeddings = embeddings
        self._metadata_extractor = metadata_extractor

    def run_query(self, *, question: str, limit: int, offset: int) -> Pagination[SearchRow]:
        if self._embeddings is None:
            raise RuntimeError("Embedding service is not configured")
        qvec = self._embeddings.embed_texts([question])[0]

        # Reuse existing MetadataExtractor to infer optional filters
        jurisdiction: Optional[str] = None
        agreement_type: Optional[str] = None
        if self._metadata_extractor is not None:
            meta = self._metadata_extractor.extract_metadata(question)
            jurisdiction = meta.jurisdiction if meta.jurisdiction and meta.jurisdiction != "Unknown" else None
            agreement_type = meta.agreement_type if meta.agreement_type and meta.agreement_type != "Unknown" else None

        page = self._repo.search_vector(
            query_vector=qvec,
            jurisdiction=jurisdiction,
            agreement_type=agreement_type,
            limit=limit,
            offset=offset,
        )
        best_by_doc: Dict[int, Dict] = {}
        for r in page.items:
            doc_id = r.get("document_id") or r.get("id")
            if doc_id is None:
                continue
            prev = best_by_doc.get(int(doc_id))
            if prev is None or (r.get("score") or 0) > (prev.get("score") or 0):
                best_by_doc[int(doc_id)] = r
        items = [
            SearchRow(
                document=r.get("file_name", ""),
                governing_law=r.get("jurisdiction"),
                agreement_type=r.get("agreement_type"),
                industry=r.get("industry"),
                score=r.get("score"),
            )
            for r in best_by_doc.values()
        ]
        return Pagination(items=items, offset=offset, limit=limit, total=len(items))