import json
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.Document import Document
from app.repositories.entities.DocumentEntity import DocumentEntity
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository



class DocumentRepository(IDocumentRepository):
    def __init__(self, db: Session):
        self._db = db

    def create_document(self, document: DocumentEntity) -> int:
        doc = Document(
            file_name=document.file_name,
            mime_type=document.mime_type,
            size_bytes=document.size_bytes,
            text=document.text,
            agreement_type=document.agreement_type,
            jurisdiction=document.jurisdiction,
            industry=document.industry,
            geography_json=json.dumps(document.geography_mentioned or []),
        )
        self._db.add(doc)
        self._db.flush()
        return int(doc.id)

    def bulk_create_documents(self, documents: List[DocumentEntity]) -> List[int]:
        doc_models: List[Document] = []
        for d in documents:
            doc_models.append(
                Document(
                    file_name=d.file_name,
                    mime_type=d.mime_type,
                    size_bytes=d.size_bytes,
                    text=d.text,
                    agreement_type=d.agreement_type,
                    jurisdiction=d.jurisdiction,
                    industry=d.industry,
                    geography_json=json.dumps(d.geography_mentioned or []),
                )
            )
        self._db.add_all(doc_models)
        self._db.flush()
        return [int(m.id) for m in doc_models]

    def search(
        self,
        *,
        fts_query: Optional[str],
        jurisdiction: Optional[str],
        agreement_type: Optional[str],
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        if fts_query and self._db.bind and self._db.bind.dialect.name == "sqlite":
            sql = text(
                """
                SELECT d.id, d.file_name, d.jurisdiction, d.agreement_type, d.industry,
                       bm25(fts) AS rank
                FROM documents d
                JOIN doc_fts fts ON fts.rowid = d.id
                WHERE fts MATCH :fts_query
                  AND (:jurisdiction IS NULL OR d.jurisdiction = :jurisdiction)
                  AND (:agreement_type IS NULL OR d.agreement_type = :agreement_type)
                ORDER BY rank ASC
                LIMIT :limit OFFSET :offset
                """
            )
            rows = self._db.execute(
                sql,
                {
                    "fts_query": fts_query,
                    "jurisdiction": jurisdiction,
                    "agreement_type": agreement_type,
                    "limit": limit,
                    "offset": offset,
                },
            ).mappings().all()
            return [dict(r) for r in rows]

        # Fallback LIKE search or no fts_query
        q = self._db.query(Document)
        if fts_query:
            like = f"%{fts_query}%"
            q = q.filter(Document.text.ilike(like))
        if jurisdiction:
            q = q.filter(Document.jurisdiction == jurisdiction)
        if agreement_type:
            q = q.filter(Document.agreement_type == agreement_type)
        q = q.limit(limit).offset(offset)
        docs = q.all()
        return [
            {
                "id": d.id,
                "file_name": d.file_name,
                "jurisdiction": d.jurisdiction,
                "agreement_type": d.agreement_type,
                "industry": d.industry,
                "rank": None,
            }
            for d in docs
        ]

    def get_aggregations(self) -> Dict[str, Dict[str, int]]:
        def count_by(field: str) -> Dict[str, int]:
            sql = text(f"SELECT {field} AS key, COUNT(*) AS cnt FROM documents GROUP BY {field}")
            rows = self._db.execute(sql).mappings().all()
            return {str(r["key"]): int(r["cnt"]) for r in rows if r["key"] is not None}

        return {
            "agreement_types": count_by("agreement_type"),
            "jurisdictions": count_by("jurisdiction"),
            "industries": count_by("industry"),
        }


