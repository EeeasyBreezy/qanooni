import json
from typing import List
from app.common.ContentTypes import ContentType
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.interfaces.ITextExtractor import ITextExtractor
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File
from app.repositories.entities.DocumentEntity import DocumentEntity
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository


class UploadService(IUploadService):
    def __init__(self, textExtractor: ITextExtractor, metadataExtractor: IMetadataExtractor, repository: IDocumentRepository):
        self._text_extractor = textExtractor
        self._metadata_extractor = metadataExtractor
        self._repository = repository

    def upload_files(self, files: List[File]) -> List[int]:
        entities: List[DocumentEntity] = []
        for file in files:
            if file.mime_type == ContentType.pdf:
                text = self._text_extractor.parse_pdf(file.content)
            elif file.mime_type == ContentType.docx:
                text = self._text_extractor.parse_docx(file.content)
            else:
                raise ValueError(f"Unsupported file type: {file.mime_type}")

            metadata = self._metadata_extractor.extract_metadata(text)
            entities.append(
                DocumentEntity(
                    file_name=file.file_name,
                    mime_type=file.mime_type,
                    size_bytes=file.size_bytes,
                    text=text,
                    agreement_type=metadata.agreement_type,
                    jurisdiction=metadata.jurisdiction,
                    industry=metadata.industry,
                    geography_json=json.dumps(metadata.geography_mentioned or []),
                )
            )

        return self._repository.bulk_create_documents(entities)
    
    def _extract_text(self, file: File) -> str:
        if file.mime_type == ContentType.pdf:
            return self._text_extractor.parse_pdf(file.content)
        elif file.mime_type == ContentType.docx:
            return self._text_extractor.parse_docx(file.content)
        else:
            raise ValueError(f"Unsupported file type: {file.mime_type}")