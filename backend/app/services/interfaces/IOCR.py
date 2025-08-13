from abc import ABC, abstractmethod
from typing import Tuple


class IOCR(ABC):
    @abstractmethod
    def extract_text(self, image_bytes: bytes) -> Tuple[str, str]:
        raise NotImplementedError


