from typing import List


class TextChunker:
    def __init__(self, max_tokens: int = 1000, overlap: int = 200):
        self._max_tokens = max_tokens
        self._overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if self._max_tokens <= 0:
            return [text]
        words = text.split()
        if not words:
            return []
        chunks: List[str] = []
        start = 0
        step = max(1, self._max_tokens - self._overlap)
        while start < len(words):
            end = min(len(words), start + self._max_tokens)
            chunk_text = " ".join(words[start:end]).strip()
            if chunk_text:
                chunks.append(chunk_text)
            start += step
        return chunks


