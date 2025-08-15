import os
import time
import uuid
from pathlib import Path
from typing import List

from tests_integration.client.http_client import ApiClient
from tests_integration.client.dtos.AggregationResultDTO import AggregationResultDTO
from tests_integration.util.db_cleaner import DatabaseCleaner


BASE_URL = os.getenv("IT_BASE_URL", "http://127.0.0.1:8000")
ASSETS_DIR = Path(__file__).resolve().parent / "files"


class TestDashboardCountries:
    @classmethod
    def setup_class(cls) -> None:
        cls.client = ApiClient(BASE_URL)
        cls.cleaner = DatabaseCleaner()
        cls._uploaded_files: List[str] = []

    @classmethod
    def teardown_class(cls) -> None:
        # Ensure any uploaded docs in this class are removed
        try:
            cls.cleaner.delete_documents_by_file_names(cls._uploaded_files)
        except Exception:
            pass

    def _get_count(self, items: List[AggregationResultDTO], country: str) -> int:
        for i in items:
            if i.category == country:
                return i.count
        return 0

    def _wait_for_delta(self, country: str, baseline: int, expected_delta: int, timeout_s: float = 15.0) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            items = self.client.get_countries()
            if self._get_count(items, country) >= baseline + expected_delta:
                return
            time.sleep(0.25)
        raise AssertionError(f"Timed out waiting for {country} >= {baseline + expected_delta}")

    def test_countries_increments_after_upload(self) -> None:
        target_country = "UAE"

        baseline_items = self.client.get_countries()
        baseline = self._get_count(baseline_items, target_country)

        pdf_path = str(ASSETS_DIR / "pdf.pdf")
        docx_path = str(ASSETS_DIR / "docx.docx")
        rid1, rid2 = str(uuid.uuid4()), str(uuid.uuid4())
        self.client.upload_file(filepath=pdf_path, request_id=rid1)
        self.client.upload_file(filepath=docx_path, request_id=rid2)
        self._uploaded_files.extend([Path(pdf_path).name, Path(docx_path).name])

        self._wait_for_delta(target_country, baseline, expected_delta=2, timeout_s=20.0)

        final_items = self.client.get_countries()
        final_count = self._get_count(final_items, target_country)
        assert final_count >= baseline + 2

