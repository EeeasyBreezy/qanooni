import time, uuid
import pytest
from pathlib import Path
from tests_integration.client.http_client import ApiClient

BASE_URL = "http://127.0.0.1:8000"
ASSETS_DIR = Path(__file__).resolve().parent / "files"

class TestDashboardAgreementTypes:
    @classmethod
    def setup_class(cls) -> None:
        cls.client = ApiClient(BASE_URL)

    def _get_count(self, items, category: str) -> int:
        for i in items:
            if i.category == category:
                return i.count
        return 0

    def _wait_for_delta(self, category: str, baseline: int, expected_delta: int, timeout_s: float = 10.0) -> None:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            items = self.client.get_agreement_types()
            if self._get_count(items, category) >= baseline + expected_delta:
                return
            time.sleep(0.25)
        raise AssertionError(f"Timed out waiting for {category} >= {baseline + expected_delta}")

    def test_agreement_types_increments_after_upload(self) -> None:
        category = "Non-Disclosure Agreement"

        # Snapshot baseline
        baseline_items = self.client.get_agreement_types()
        baseline = self._get_count(baseline_items, category)

        # Upload 2 files that should map to NDA
        pdf_path = str(ASSETS_DIR / "nda - england.docx")
        docx_path = str(ASSETS_DIR / "nda - uae.docx")
        self.client.upload_file(filepath=pdf_path,  request_id=str(uuid.uuid4()))
        self.client.upload_file(filepath=docx_path, request_id=str(uuid.uuid4()))

        # Poll until counts reflect at least +2 for NDA
        self._wait_for_delta(category, baseline, expected_delta=2, timeout_s=15.0)

        # Final sanity: the category exists and is int
        final_items = self.client.get_agreement_types()
        final_count = self._get_count(final_items, category)
        assert isinstance(final_count, int)
        assert final_count >= baseline + 2