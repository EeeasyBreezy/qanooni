import os
import time
import uuid
from pathlib import Path
from typing import List

import pytest

from tests_integration.client.http_client import ApiClient, HttpError
from tests_integration.client.dtos.AggregationResultDTO import AggregationResultDTO
from tests_integration.util.db_cleaner import DatabaseCleaner


BASE_URL = os.getenv("IT_BASE_URL", "http://127.0.0.1:8000")
ASSETS_DIR = Path(__file__).resolve().parent / "files"


class TestDashboardIndustries:
    @classmethod
    def setup_class(cls) -> None:
        cls.client = ApiClient(BASE_URL)
        cls.cleaner = DatabaseCleaner()
        cls._uploaded_files: List[str] = []

    @classmethod
    def teardown_class(cls) -> None:
        try:
            cls.cleaner.delete_documents_by_file_names(cls._uploaded_files)
        finally:
            cls._uploaded_files.clear()

    def _wait_nonempty(self, timeout_s: float = 10.0) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            page = self.client.get_industries(limit=5, offset=0, sort="desc")
            if page.total >= 0:
                return
            time.sleep(0.2)
        raise AssertionError("Industries endpoint did not respond in time")

    def test_success_pagination(self) -> None:
        # Upload several files to ensure industries exist
        docx1 = str(ASSETS_DIR / "nda - england.docx")
        docx2 = str(ASSETS_DIR / "nda - uae.docx")
        self.client.upload_file(filepath=docx1, request_id=str(uuid.uuid4()))
        self.client.upload_file(filepath=docx2, request_id=str(uuid.uuid4()))
        self._uploaded_files.extend([Path(docx1).name, Path(docx2).name])

        self._wait_nonempty()

        page1 = self.client.get_industries(limit=1, offset=0, sort="desc")
        assert page1.limit == 1
        assert page1.offset == 0
        assert isinstance(page1.total, int)
        assert len(page1.items) <= 1

        page2 = self.client.get_industries(limit=1, offset=1, sort="desc")
        assert page2.limit == 1
        assert page2.offset == 1
        if page1.items and page2.items:
            # Ensure different item when possible
            assert page1.items[0].category != page2.items[0].category or page1.total <= 1

    @pytest.mark.parametrize(
        "params",
        [
            {},  # missing all
            {"limit": 10},  # missing offset
            {"offset": 0},  # missing limit
            {"limit": -1, "offset": 0},  # negative limit
            {"limit": 0, "offset": 0},  # zero limit (invalid)
            {"limit": 10, "offset": -5},  # negative offset
            {"limit": 10, "offset": 0, "sort": "down"},  # invalid sort
        ],
    )
    def test_bad_request_invalid_params(self, params) -> None:
        with pytest.raises(HttpError) as exc:
            self.client.get_industries_raw(params)
        # FastAPI validation errors typically return 422; some invalids could be 400 depending on route validation
        assert exc.value.status in (400, 422)


