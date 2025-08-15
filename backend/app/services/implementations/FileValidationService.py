from typing import Optional

from app.common.ContentTypes import ContentType
from app.services.interfaces.IFileValidationService import IFileValidationService


class FileValidationService(IFileValidationService):
    def validate_and_get_mime(self, file_name: str, content: bytes) -> str:
        extension = self._get_extension(file_name)
        if extension not in {"pdf", "docx"}:
            raise ValueError(f"Unsupported file extension: .{extension}")

        if extension == "pdf":
            if not self._looks_like_pdf(content):
                raise ValueError("File content does not match .pdf signature")
            return ContentType.pdf

        if extension == "docx":
            if not self._looks_like_docx(content):
                raise ValueError("File content does not match .docx signature")
            return ContentType.docx

        # Should never reach here due to extension check
        raise ValueError("Unsupported file type")

    def _get_extension(self, file_name: str) -> str:
        # Handle names without dot safely
        if "." not in file_name:
            return ""
        return file_name.rsplit(".", 1)[-1].lower()

    def _looks_like_pdf(self, content: bytes) -> bool:
        # PDF files start with '%PDF-'
        return len(content) >= 5 and content[:5] == b"%PDF-"

    def _looks_like_docx(self, content: bytes) -> bool:
        # DOCX is a ZIP (PK\x03\x04 at the start) and must contain '[Content_Types].xml' later
        if len(content) < 4 or content[:4] != b"PK\x03\x04":
            return False
        # To avoid importing zipfile for performance in small uploads, do a light check that
        # the central directory or contents mention the typical docx parts.
        # This is heuristic but strong enough for validation.
        lower_sample = content[:50000].lower()
        return (
            b"[content_types].xml" in lower_sample or
            b"word/" in lower_sample
        )


