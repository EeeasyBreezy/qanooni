import os
import uuid
from pathlib import Path
import pytest

from tests_integration.client.http_client import ApiClient, HttpError


BASE_URL = os.getenv("IT_BASE_URL", "http://127.0.0.1:8000")
ASSETS_DIR = Path(__file__).resolve().parent / "files"


class TestUploadEndpoint:
    @classmethod
    def setup_class(cls) -> None:
        cls.client = ApiClient(BASE_URL)

    def test_upload_valid_pdf(self) -> None:
        pdf_path = str(ASSETS_DIR / "pdf.pdf")
        self.client.upload_file(filepath=pdf_path, request_id=str(uuid.uuid4()))

    def test_upload_valid_docx(self) -> None:
        docx_path = str(ASSETS_DIR / "docx.docx")
        self.client.upload_file(filepath=docx_path, request_id=str(uuid.uuid4()))

    def test_upload_pdf_with_images(self) -> None:
        # reuse existing pdf fixture as binary content; assuming it contains images in repo
        pdf_path = str(ASSETS_DIR / "pdf.pdf")
        self.client.upload_file(filepath=pdf_path, request_id=str(uuid.uuid4()))

    @pytest.mark.parametrize(
        "fields, include_file",
        [
            ({}, False),  # missing file, missing request_id
            ({"request_id": str(uuid.uuid4())}, False),  # missing file
            ({}, True),  # missing request_id
        ],
    )
    def test_upload_bad_request_missing_parts(self, fields, include_file) -> None:
        file_tuple = None
        if include_file:
            # send some bytes with fake content type to ensure server sees a file part
            file_tuple = {"name": "file", "filename": "fake.bin", "content_type": "application/octet-stream", "content": b"test"}
        with pytest.raises(HttpError) as exc:
            self.client.upload_malformed(fields=fields, file_tuple=file_tuple)
        assert exc.value.status == 422

    def test_upload_fake_pdf_docx_rejected(self) -> None:
        # Fake PDF
        with pytest.raises(HttpError) as exc1:
            self.client.upload_malformed(
                fields={"request_id": str(uuid.uuid4())},
                file_tuple={"name": "file", "filename": "fake.pdf", "content_type": "application/pdf", "content": b"not a real pdf"},
            )
        assert exc1.value.status == 400

        # Fake DOCX
        with pytest.raises(HttpError) as exc2:
            self.client.upload_malformed(
                fields={"request_id": str(uuid.uuid4())},
                file_tuple={"name": "file", "filename": "fake.docx", "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "content": b"not a real docx"},
            )
        assert exc2.value.status == 400
        
    def test_upload_unsupported_valid_formats(self) -> None:
        # Valid JPEG header but unsupported format
        jpeg_bytes = b"\xFF\xD8\xFF\xE0" + b"\x00" * 100
        with pytest.raises(HttpError) as exc_jpeg:
            self.client.upload_malformed(
                fields={"request_id": str(uuid.uuid4())},
                file_tuple={
                    "name": "file",
                    "filename": "image.jpg",
                    "content_type": "image/jpeg",
                    "content": jpeg_bytes,
                },
            )
        assert exc_jpeg.value.status == 400

        # Valid legacy .doc header (OLE Compound File) but unsupported format
        doc_bytes = b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1" + b"\x00" * 100
        with pytest.raises(HttpError) as exc_doc:
            self.client.upload_malformed(
                fields={"request_id": str(uuid.uuid4())},
                file_tuple={
                    "name": "file",
                    "filename": "legacy.doc",
                    "content_type": "application/msword",
                    "content": doc_bytes,
                },
            )
        assert exc_doc.value.status == 400


