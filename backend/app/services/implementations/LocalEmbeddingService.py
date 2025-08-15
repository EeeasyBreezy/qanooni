from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from app.services.interfaces.IEmbeddingService import IEmbeddingService


class LocalEmbeddingService(IEmbeddingService):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self._model = SentenceTransformer(model_name)
        # Warm up to record dimension
        vec = self._model.encode(["warmup"], normalize_embeddings=True)
        self._dim = int(vec.shape[1]) if hasattr(vec, "shape") else len(vec[0])

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        embeddings = self._model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return embeddings.astype(np.float32).tolist()

    def dimension(self) -> int:
        return self._dim


