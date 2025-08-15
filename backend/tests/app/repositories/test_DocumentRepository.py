import importlib
import os
from typing import List, Optional

import pytest


class TestDocumentRepository:
    def setup_method(self) -> None:
        # Ensure DATABASE_URL points to Postgres with pgvector (falls back to default if not set)
        if not os.getenv("DATABASE_URL"):
            os.environ["DATABASE_URL"] = "postgresql+psycopg2://qanooni:qanooni@localhost:5432/qanooni"

        # Reload db module to pick up DATABASE_URL and rebuild engine/session
        from app import db as db_module  # type: ignore
        self.db = importlib.reload(db_module)

        # Initialize schema for this database
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
            try:
                self.db.engine.dispose()
            except Exception:
                pass

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
            geography_json=geography_mentioned,
        )

    def test_create_documents_smoke(self) -> None:
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

    def test_insertions_and_counts(self) -> None:
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

        count = self.session.query(self.DocumentEntity).count()
        assert count >= 2

    def test_segregated_aggregations(self) -> None:
        self.repo.bulk_create_documents(
            [
                self._make_entity(file_name="a.pdf", text="nda text", agreement_type="Non-Disclosure Agreement", jurisdiction="UAE", industry="Technology"),
                self._make_entity(file_name="b.pdf", text="msa text", agreement_type="Master Services Agreement", jurisdiction="UAE", industry="Oil & Gas"),
                self._make_entity(file_name="c.pdf", text="nda again", agreement_type="Non-Disclosure Agreement", jurisdiction="UK", industry="Technology"),
            ]
        )

        agreements = self.repo.count_by_agreement_type()
        agreements_map = {a.category: a.count for a in agreements}

        countries = self.repo.count_by_country()
        countries_map = {c.category: c.count for c in countries}

        industries_page = self.repo.count_by_industry(limit=10, offset=0, sort="desc")
        industries_map = {i.category: i.count for i in industries_page.items}

        assert agreements_map.get("Non-Disclosure Agreement", 0) >= 2
        assert countries_map.get("UAE", 0) >= 2
        assert industries_map.get("Technology", 0) >= 2


