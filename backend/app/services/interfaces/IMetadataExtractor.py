from abc import ABC, abstractmethod
from app.services.model.DocumentMetadata import DocumentMetadata


class IMetadataExtractor(ABC):
    @abstractmethod
    def extract_metadata(self, text: str) -> DocumentMetadata:
        pass