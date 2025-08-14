from functools import lru_cache

from sqlalchemy.orm import Session
from fastapi import Depends

from app.db import get_db
from app.services.implementations.ImageProcessor import ImageProcessor
from app.services.implementations.OCRService import OCRService
from app.services.implementations.TextExtractor import TextExtractor
from app.services.implementations.MetadataExtractor import MetadataExtractor
from app.services.implementations.UploadService import UploadService
from app.repositories.implementations.DocumentRepository import DocumentRepository
from app.services.implementations.DocumentStatsService import DocumentStatsService

from app.services.interfaces.IImageProcessor import IImageProcessor
from app.services.interfaces.IOCR import IOCR
from app.services.interfaces.ITextExtractor import ITextExtractor
from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.interfaces.IUploadService import IUploadService
from app.services.interfaces.IDocumentStatsService import IDocumentStatsService


@lru_cache(maxsize=1)
def get_image_processor() -> IImageProcessor:
    return ImageProcessor()


@lru_cache(maxsize=1)
def get_ocr_service() -> IOCR:
    return OCRService(get_image_processor())


@lru_cache(maxsize=1)
def get_text_extractor() -> ITextExtractor:
    return TextExtractor(get_ocr_service())


@lru_cache(maxsize=1)
def get_metadata_extractor() -> IMetadataExtractor:
    return MetadataExtractor()


def get_upload_service(db: Session = Depends(get_db)) -> IUploadService:
    # Inject a repository factory so background worker can create repos with fresh Sessions
    def repository_factory(s: Session) -> DocumentRepository:
        return DocumentRepository(s)

    return UploadService(
        textExtractor=get_text_extractor(),
        metadataExtractor=get_metadata_extractor(),
        repository_factory=repository_factory,
    )


def get_document_stats_service(db: Session = Depends(get_db)) -> IDocumentStatsService:
    repo = DocumentRepository(db)
    return DocumentStatsService(repo)

