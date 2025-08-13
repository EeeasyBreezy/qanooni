from abc import ABC, abstractmethod


class ITextExtractor(ABC):
    @abstractmethod
    def parse_docx(self, document_bytes: bytes) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def parse_pdf(self, document_bytes: bytes) -> str:
        raise NotImplementedError
