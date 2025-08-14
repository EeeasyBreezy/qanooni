import json
from typing import List

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


