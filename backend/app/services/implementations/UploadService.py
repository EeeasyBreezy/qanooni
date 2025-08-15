import json
from typing import List, Callable, Iterable
import queue
import threading
from app.common.ContentTypes import ContentType
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.interfaces.ITextExtractor import ITextExtractor
from app.services.interfaces.IUploadService import IUploadService
from app.services.interfaces.ITextChunker import ITextChunker
from app.services.interfaces.IEmbeddingService import IEmbeddingService
from app.services.model.File import File
from app.repositories.entities.DocumentEntity import DocumentEntity
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.db import session_scope
from sqlalchemy.orm import Session
from app.notifications import publish_done
from app.repositories.entities.DocumentChunkEntity import DocumentChunkEntity


class UploadService(IUploadService):
    def __init__(
        self,
        textExtractor: ITextExtractor,
        metadataExtractor: IMetadataExtractor,
        repository_factory: Callable[[Session], IDocumentRepository],
        chunker: ITextChunker,
        embeddings: IEmbeddingService,
    ):
        self._text_extractor = textExtractor
        self._metadata_extractor = metadataExtractor
        # Repository factory allows creating a repository bound to a fresh Session per background job
        self._repository_factory = repository_factory
        self._chunker = chunker
        self._embeddings = embeddings
        self._queue: "queue.Queue[File]" = queue.Queue(maxsize=1000)
        self._worker = threading.Thread(target=self._consume_loop, daemon=True)
        self._worker.start()

    def _chunk_text(self, text: str) -> List[str]:
        return self._chunker.chunk(text)

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
                    # Persist using a new session for the background thread
                    with session_scope() as s:
                        repo = self._repository_factory(s)
                        repo.bulk_create_documents([entity])
                        # Create chunks for semantic retrieval (embeddings populated later)
                        chunks_text = self._chunk_text(text)
                        chunks_entities: List[DocumentChunkEntity] = []
                        if chunks_text:
                            # Compute embeddings locally for each chunk
                            vectors = self._embeddings.embed_texts(chunks_text)
                            for idx, (chunk_text, vec) in enumerate(zip(chunks_text, vectors)):
                                dc = DocumentChunkEntity(
                                    document_id=int(entity.id),
                                    chunk_index=idx,
                                    content=chunk_text,
                                    embedding=vec,
                                )
                                chunks_entities.append(dc)
                        if chunks_entities:
                            repo.bulk_create_document_chunks(chunks_entities)

                    try:
                        # Use the upload request id as the notification channel key
                        publish_done(f.request_id, "processed")
                    except Exception as exception:
                        print(exception)
                finally:
                    self._queue.task_done()
            except Exception:
                continue