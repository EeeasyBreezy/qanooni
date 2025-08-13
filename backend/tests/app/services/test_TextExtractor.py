from pathlib import Path
from shutil import which

import pytest
import fitz  # PyMuPDF

from app.services.implementations.TextExtractor import TextExtractor
from app.services.implementations.OCRService import OCRService
from app.services.implementations.ImageProcessor import ImageProcessor


FILES_DIR = Path(__file__).parent / "files"
DOCX_PATH = FILES_DIR / "word.docx"
PDF_PATH = FILES_DIR / "pdf.pdf"


class TestTextExtractor:
    @pytest.mark.skipif(not DOCX_PATH.exists(), reason="docx test file missing")
    def test_parse_docx_extracts_non_empty_text(self):
        extractor = TextExtractor(ocr_service=OCRService(ImageProcessor()))
        doc_bytes = DOCX_PATH.read_bytes()
        text = extractor.parse_docx(doc_bytes)
        expected = '''Hello, paragraph!
Hello\tRow 1
Goodbye\tRow 2'''
        assert expected == text

    @pytest.mark.skipif(not PDF_PATH.exists(), reason="pdf test file missing")
    @pytest.mark.skipif(which("tesseract") is None, reason="Tesseract not installed")
    def test_parse_pdf_extracts_text_using_real_ocr_and_pymupdf(self):
        extractor = TextExtractor(ocr_service=OCRService(ImageProcessor()))
        pdf_bytes = PDF_PATH.read_bytes()
        text = extractor.parse_pdf(pdf_bytes)
        expected = '''Hello, paragraph! 
Hello\nRow 1
Goodbye\nRow 2'''
        assert expected == text

    