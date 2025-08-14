import json
from typing import List, Optional
import queue
import threading
import uuid
from app.common.ContentTypes import ContentType
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.interfaces.ITextExtractor import ITextExtractor
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File
from app.repositories.entities.DocumentEntity import DocumentEntity
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.notifications import publish_done


class UploadService(IUploadService):
    def __init__(self, textExtractor: ITextExtractor, metadataExtractor: IMetadataExtractor, repository: IDocumentRepository):
        self._text_extractor = textExtractor
        self._metadata_extractor = metadataExtractor
        self._repository = repository
        self._queue: "queue.Queue[File]" = queue.Queue(maxsize=1000)
        self._worker = threading.Thread(target=self._consume_loop, daemon=True)
        self._worker.start()

    def upload_files(self, files: List[File]) -> List[str]:
        out: List[str] = []
        for idx, f in enumerate(files):
            self._queue.put(f)
            out.append(f.request_id)
        return out
    
    def _extract_text(self, file: File) -> str:
        if file.mime_type == ContentType.pdf:
            return self._text_extractor.parse_pdf(file.content)
        elif file.mime_type == ContentType.docx:
            return self._text_extractor.parse_docx(file.content)
        else:
            raise ValueError(f"Unsupported file type: {file.mime_type}")

    def _consume_loop(self) -> None:
        while True:
            try:
                f = self._queue.get()
                try:
                    text = self._extract_text(f)
                    metadata = self._metadata_extractor.extract_metadata(text)
                    entity = DocumentEntity(
                        file_name=f.file_name,
                        mime_type=f.mime_type,
                        size_bytes=f.size_bytes,
                        text=text,
                        agreement_type=metadata.agreement_type,
                        jurisdiction=metadata.jurisdiction,
                        industry=metadata.industry,
                        geography_json=json.dumps(metadata.geography_mentioned or []),
                    )
                    self._repository.bulk_create_documents([entity])
                    # Notify completion (uses generated or provided request_id string)
                    try:
                        publish_done(entity.file_name, "processed")
                    except Exception:
                        pass
                finally:
                    self._queue.task_done()
            except Exception:
                continue