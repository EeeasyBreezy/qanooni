from typing import List
from app.common.ContentTypes import ContentType
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.interfaces.ITextExtractor import ITextExtractor
from app.services.interfaces.IUploadService import IUploadService
from app.services.model.File import File


class UploadService(IUploadService):
    def __init__(self, textExtractor: ITextExtractor, metadataExtractor: IMetadataExtractor):
        self._text_extractor = textExtractor
        self._metadata_extractor = metadataExtractor

    def upload_files(self, files: List[File]) -> str:
        for file in files:
            if file.mime_type == ContentType.pdf:
                text = self._text_extractor.parse_pdf(file.content)
            elif file.mime_type == ContentType.docx:
                text = self._text_extractor.parse_docx(file.content)
            else:
                raise ValueError(f"Unsupported file type: {file.mime_type}")
            metadata = self._metadata_extractor.extract_metadata(text)
            
            return ""
    
    def _extract_text(self, file: File) -> str:
        if file.mime_type == ContentType.pdf:
            return self._text_extractor.parse_pdf(file.content)
        elif file.mime_type == ContentType.docx:
            return self._text_extractor.parse_docx(file.content)
        else:
            raise ValueError(f"Unsupported file type: {file.mime_type}")