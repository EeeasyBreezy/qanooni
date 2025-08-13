from app.services.interfaces.IMetadataExtractor import IMetadataExtractor
from app.services.model.DocumentMetadata import DocumentMetadata


class MetadataExtractor(IMetadataExtractor):
    def extract_metadata(self, text: str) -> DocumentMetadata:
        pass