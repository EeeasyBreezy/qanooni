from typing import List, Optional, TYPE_CHECKING

import numpy as np

from app.services.interfaces.IEmbeddingService import IEmbeddingService


class LocalEmbeddingService(IEmbeddingService):
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self._model_name = model_name
        # Avoid importing heavy libs at module import time
        self._model: Optional[object] = None
        self._dim: Optional[int] = None

    def _ensure_model_loaded(self) -> None:
        if self._model is None:
            # Local import to defer heavy dependency load
            from sentence_transformers import SentenceTransformer  # type: ignore
            model = SentenceTransformer(self._model_name)
            vec = model.encode(["warmup"], normalize_embeddings=True)
            self._model = model
            self._dim = int(vec.shape[1]) if hasattr(vec, "shape") else len(vec[0])

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        self._ensure_model_loaded()
        model = self._model  # type: ignore[assignment]
        assert model is not None
        embeddings = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)  # type: ignore[attr-defined]
        return embeddings.astype(np.float32).tolist()

    def dimension(self) -> int:
        self._ensure_model_loaded()
        assert self._dim is not None
        return self._dim
 
 
