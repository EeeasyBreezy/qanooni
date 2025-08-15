from abc import ABC, abstractmethod
from typing import List


class IEmbeddingService(ABC):
    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Return a list of embedding vectors, one per input text.

        Implementations should return fixed-length vectors.
        """
        raise NotImplementedError

    @abstractmethod
    def dimension(self) -> int:
        """Embedding dimensionality."""
        raise NotImplementedError


