import importlib
import os
import shutil
import tempfile


def test_chunk_persistence_flow():
    # Use isolated SQLite for unit test of persistence logic
    tmp_dir = tempfile.mkdtemp(prefix="legalintel_chunk_test_")
    try:
        db_path = os.path.join(tmp_dir, "test.db")
        os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

        from app import db as db_module  # type: ignore
        db = importlib.reload(db_module)
        db.init_db()
        session = db.SessionLocal()

        from app.repositories.implementations.DocumentRepository import DocumentRepository
        from app.repositories.entities.DocumentEntity import DocumentEntity
        from app.repositories.entities.DocumentChunkEntity import DocumentChunkEntity

        repo = DocumentRepository(session)

        # Create a document and chunks
        doc = DocumentEntity(
            file_name="doc.pdf",
            mime_type="application/pdf",
            size_bytes=100,
            text="word " * 2500,
            agreement_type="NDA",
            jurisdiction="UAE",
            industry="Tech",
            geography_json=None,
        )
        repo.bulk_create_documents([doc])

        # Create 3 chunks
        chunks = [
            DocumentChunkEntity(document_id=int(doc.id), chunk_index=i, content=f"chunk {i}")
            for i in range(3)
        ]
        ids = repo.bulk_create_document_chunks(chunks)

        assert len(ids) == 3
        # Verify they are persisted and linked
        rows = session.execute(
            db_module.text("SELECT COUNT(*) FROM document_chunks WHERE document_id = :doc_id"),
            {"doc_id": int(doc.id)},
        ).scalar_one()
        assert rows == 3
    finally:
        try:
            db.engine.dispose()  # type: ignore
        except Exception:
            pass
        shutil.rmtree(tmp_dir, ignore_errors=True)


