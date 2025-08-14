import importlib
import os
import tempfile
import shutil
from typing import List, Optional

import pytest


class TestDocumentRepository:
    def setup_method(self) -> None:
        # Create isolated temporary SQLite database file
        self._tmp_dir = tempfile.mkdtemp(prefix="legalintel_test_")
        self._db_path = os.path.join(self._tmp_dir, "test.db")
        os.environ["DATABASE_URL"] = f"sqlite:///{self._db_path}"

        # Reload db module to pick up DATABASE_URL and rebuild engine/session
        from app import db as db_module  # type: ignore
        self.db = importlib.reload(db_module)

        # Initialize schema and FTS triggers for this database
        self.db.init_db()

        # Session for tests
        self.session = self.db.SessionLocal()

        # Repository under test
        from app.repositories.implementations.DocumentRepository import (
            DocumentRepository,
        )
        from app.repositories.entities.DocumentEntity import DocumentEntity

        self.DocumentRepository = DocumentRepository
        self.DocumentEntity = DocumentEntity
        self.repo = DocumentRepository(self.session)

    def teardown_method(self) -> None:
        try:
            self.session.close()
        finally:
            # Dispose engine and remove temp directory
            try:
                self.db.engine.dispose()
            except Exception:
                pass
            shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def _make_entity(
        self,
        *,
        file_name: str,
        mime_type: str = "application/pdf",
        size_bytes: int = 123,
        text: str,
        agreement_type: str = "NDA",
        jurisdiction: str = "UAE",
        industry: str = "Technology",
        geography_mentioned: Optional[List[str]] = None,
    ):
        return self.DocumentEntity(
            file_name=file_name,
            mime_type=mime_type,
            size_bytes=size_bytes,
            text=text,
            agreement_type=agreement_type,
            jurisdiction=jurisdiction,
            industry=industry,
            geography_json=None,
        )

    def test_create_and_search_basic(self) -> None:
        # Arrange: two documents with different content
        ids = self.repo.bulk_create_documents(
            [
                self._make_entity(
                    file_name="nda_abudhabi.pdf",
                    text="This Non-Disclosure Agreement is governed by the laws of UAE.",
                ),
                self._make_entity(
                    file_name="supplier_contract_dubai.docx",
                    text="Supplier contract for Dubai operations and logistics.",
                    agreement_type="Supply Agreement",
                    jurisdiction="Dubai",
                    industry="Logistics",
                ),
            ]
        )
        assert len(ids) == 2

        # Act: full text search for 'governed' should match first doc (FTS5)
        results = self.repo.search(fts_query="governed", jurisdiction=None, agreement_type=None, limit=10)

        # Assert
        assert any(r["file_name"] == "nda_abudhabi.pdf" for r in results)
        assert not any(r["file_name"] == "supplier_contract_dubai.docx" and r.get("rank") is not None for r in results)

    def test_search_with_filters(self) -> None:
        # Arrange
        self.repo.bulk_create_documents(
            [
                self._make_entity(
                    file_name="msa_uae.pdf",
                    text="Master Services Agreement for UAE operations.",
                    agreement_type="Master Services Agreement",
                    jurisdiction="UAE",
                    industry="Technology",
                ),
                self._make_entity(
                    file_name="msa_uk.pdf",
                    text="Master Services Agreement for UK operations.",
                    agreement_type="Master Services Agreement",
                    jurisdiction="UK",
                    industry="Technology",
                ),
            ]
        )

        # Act: no FTS, filter by jurisdiction
        results = self.repo.search(fts_query=None, jurisdiction="UAE", agreement_type=None, limit=10)

        # Assert: only UAE docs
        assert all(r["jurisdiction"] == "UAE" for r in results)
        assert any(r["file_name"] == "msa_uae.pdf" for r in results)

    def test_aggregations(self) -> None:
        # Arrange
        self.repo.bulk_create_documents(
            [
                self._make_entity(file_name="a.pdf", text="nda text", agreement_type="Non-Disclosure Agreement", jurisdiction="UAE", industry="Technology"),
                self._make_entity(file_name="b.pdf", text="msa text", agreement_type="Master Services Agreement", jurisdiction="UAE", industry="Oil & Gas"),
                self._make_entity(file_name="c.pdf", text="nda again", agreement_type="Non-Disclosure Agreement", jurisdiction="UK", industry="Technology"),
            ]
        )

        # Act
        agg = self.repo.get_aggregations()

        # Assert
        assert agg["agreement_types"].get("Non-Disclosure Agreement", 0) >= 2
        assert agg["jurisdictions"].get("UAE", 0) >= 2
        assert agg["industries"].get("Technology", 0) >= 2


