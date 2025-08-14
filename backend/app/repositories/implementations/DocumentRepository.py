import json
from typing import List

from sqlalchemy.orm import Session

from app.models.Document import Document
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.services.model.DocumentMetadata import DocumentMetadata


class DocumentRepository(IDocumentRepository):
    def __init__(self, db: Session):
        self._db = db

    def create_document(
        self,
        *,
        file_name: str,
        mime_type: str,
        size_bytes: int,
        text: str,
        metadata: DocumentMetadata,
    ) -> int:
        doc = Document(
            file_name=file_name,
            mime_type=mime_type,
            size_bytes=size_bytes,
            text=text,
            agreement_type=metadata.agreement_type,
            jurisdiction=metadata.jurisdiction,
            industry=metadata.industry,
            geography_json=json.dumps(metadata.geography_mentioned or []),
        )
        self._db.add(doc)
        self._db.flush()
        return int(doc.id)

    def bulk_create_documents(self, documents: List[dict]) -> List[int]:
        ids: List[int] = []
        for d in documents:
            meta: DocumentMetadata = d["metadata"]
            doc = Document(
                file_name=d["file_name"],
                mime_type=d["mime_type"],
                size_bytes=d["size_bytes"],
                text=d["text"],
                agreement_type=meta.agreement_type,
                jurisdiction=meta.jurisdiction,
                industry=meta.industry,
                geography_json=json.dumps(meta.geography_mentioned or []),
            )
            self._db.add(doc)
            self._db.flush()
            ids.append(int(doc.id))
        return ids


