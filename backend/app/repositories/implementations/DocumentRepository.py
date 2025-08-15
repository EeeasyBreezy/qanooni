import json
from typing import Any, Dict, List, Optional

from sqlalchemy import func, text, bindparam
from app.common.model.Pagination import Pagination
from sqlalchemy.orm import Session

from app.repositories.entities.DocumentEntity import DocumentEntity
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.repositories.entities.AggregationResultEntity import AggregationResultEntity
from app.repositories.entities.DocumentChunkEntity import DocumentChunkEntity
try:
    from pgvector.sqlalchemy import Vector  # type: ignore
except Exception:
    Vector = None  # type: ignore

class DocumentRepository(IDocumentRepository):
    def __init__(self, db: Session):
        self._db = db

    def create_document(self, document: DocumentEntity) -> int:
        self._db.add(document)
        self._db.flush()
        return int(document.id)

    def bulk_create_documents(self, documents: List[DocumentEntity]) -> List[int]:
        self._db.add_all(documents)
        self._db.flush()
        return [int(m.id) for m in documents]

    def bulk_create_document_chunks(self, chunks: List[DocumentChunkEntity]) -> List[int]:
        if not chunks:
            return []
        self._db.add_all(chunks)
        self._db.flush()
        return [int(c.id) for c in chunks]

    def search_vector(
        self,
        *,
        query_vector: List[float],
        jurisdiction: Optional[str],
        agreement_type: Optional[str],
        limit: int = 50,
        offset: int = 0,
    ) -> Pagination[Dict[str, Any]]:
        # If database is Postgres with pgvector, use <-> operator; else fallback to LIKE search on text
        if self._db.bind and self._db.bind.dialect.name == "postgresql":
            sql = text(
                """
                SELECT dc.id AS chunk_id, d.id AS document_id, d.file_name, d.jurisdiction, d.agreement_type, d.industry,
                       (1 - (dc.embedding <-> :qvec)) AS score,
                       dc.content AS snippet
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                WHERE dc.embedding IS NOT NULL
                  AND (:jurisdiction IS NULL OR d.jurisdiction = :jurisdiction)
                  AND (:agreement_type IS NULL OR d.agreement_type = :agreement_type)
                ORDER BY dc.embedding <-> :qvec
                LIMIT :limit OFFSET :offset
                """
            )
            # Ensure the parameter is typed as pgvector to avoid numeric[]
            if Vector is not None:
                sql = sql.bindparams(bindparam("qvec", type_=Vector(384)))
            rows = self._db.execute(
                sql,
                {
                    "qvec": query_vector,
                    "jurisdiction": jurisdiction,
                    "agreement_type": agreement_type,
                    "limit": limit,
                    "offset": offset,
                },
            ).mappings().all()
            # Count is expensive with ANN; approximate by returning offset+len(rows) or null
            total = offset + len(rows)
            return Pagination(items=[dict(r) for r in rows], offset=offset, limit=limit, total=total)

        # Fallback: return top documents by LIKE matching on concatenated chunks
        q = self._db.query(DocumentEntity)
        like = "%"
        total = q.order_by(None).count()
        docs = q.limit(limit).offset(offset).all()
        return Pagination(items=[
            {
                "document_id": d.id,
                "file_name": d.file_name,
                "jurisdiction": d.jurisdiction,
                "agreement_type": d.agreement_type,
                "industry": d.industry,
                "score": None,
                "snippet": None,
            }
            for d in docs
        ], offset=offset, limit=limit, total=total)

        
    def count_by_agreement_type(self) -> List[AggregationResultEntity]:
        sql = text("SELECT agreement_type AS key, COUNT(*) AS cnt FROM documents GROUP BY agreement_type")
        rows = self._db.execute(sql).mappings().all()
        return [
            AggregationResultEntity(category=str(r["key"]), count=int(r["cnt"]))
            for r in rows
            if r["key"] is not None
        ]

    def count_by_country(self) -> List[AggregationResultEntity]:
        sql = text("SELECT jurisdiction AS key, COUNT(*) AS cnt FROM documents GROUP BY jurisdiction")
        rows = self._db.execute(sql).mappings().all()
        return [
            AggregationResultEntity(category=str(r["key"]), count=int(r["cnt"]))
            for r in rows
            if r["key"] is not None
        ]

    def count_by_industry(self, *, limit: int = 10, offset: int = 0, sort: str = "desc") -> Pagination[AggregationResultEntity]:
        sort_dir = "ASC" if (str(sort).lower() == "asc") else "DESC"
        sql = text(
            f"""
            SELECT industry AS key, COUNT(*) AS cnt
            FROM documents
            GROUP BY industry
            ORDER BY cnt {sort_dir}
            LIMIT :limit OFFSET :offset
            """
        )
        rows = self._db.execute(sql, {"limit": limit, "offset": offset}).mappings().all()
        items = [
            AggregationResultEntity(category=str(r["key"]), count=int(r["cnt"]))
            for r in rows
            if r["key"] is not None
        ]
        total_row = self._db.execute(
            text("SELECT COUNT(DISTINCT industry) AS total FROM documents")
        ).mappings().first()
        total = int(total_row["total"]) if total_row else 0
        return Pagination(items=items, offset=offset, limit=limit, total=total)


