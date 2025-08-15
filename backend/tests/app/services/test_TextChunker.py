from app.services.implementations.UploadService import UploadService


class Dummy:
    def __init__(self) -> None:
        pass


def test_chunker_basic():
    # Prepare a minimal UploadService with dummy deps to access _chunk_text
    us = UploadService.__new__(UploadService)  # bypass __init__
    chunks = UploadService._chunk_text(us, " ".join([str(i) for i in range(0, 3000)]), max_tokens=1000, overlap=200)
    # Expect roughly ceil((3000-1000)/800)+1 = 4 chunks
    assert 3 <= len(chunks) <= 5
    # Overlap ensures continuity
    assert len(chunks[0]) > 0


