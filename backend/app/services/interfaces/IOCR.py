from abc import ABC, abstractmethod
from typing import List, Tuple


class IOCR(ABC):
    @abstractmethod
    def extract_text_and_tables(self, image_bytes: bytes) -> Tuple[str, str, List[List[List[str]]]]:
        """
        Perform OCR on the provided image and return a tuple of:
        - detected_language: ISO 639-1/639-3 like code (best-effort)
        - full_text: the recognized text as a single string
        - tables: list of tables, where each table is a matrix (list of rows), and each row is a list of cell strings
        """
        raise NotImplementedError


