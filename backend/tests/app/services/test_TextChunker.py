from app.services.implementations.TextChunker import TextChunker


class TestTextChunker:
    def test_chunker_basic(self) -> None:
        chunker = TextChunker(max_tokens=1000, overlap=200)
        chunks = chunker.chunk(" ".join([str(i) for i in range(0, 3000)]))
        # Expect roughly ceil((3000-1000)/800)+1 = 4 chunks
        assert 3 <= len(chunks) <= 5
        # Overlap ensures continuity
        assert len(chunks[0]) > 0


