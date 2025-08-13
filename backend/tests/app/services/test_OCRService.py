import shutil
from pathlib import Path

import pytest

from app.services.implementations.OCRService import OCRService
from app.services.implementations.ImageProcessor import ImageProcessor


TEST_DIR = Path(__file__).parent / "files"
TEST_IMAGE = TEST_DIR / "test.png"


@pytest.mark.skipif(not TEST_IMAGE.exists(), reason="Test image not found")
@pytest.mark.skipif(shutil.which("tesseract") is None, reason="Tesseract binary not installed")
def test_ocr_smoke_extracts_some_text():
    service = OCRService(ImageProcessor())
    image_bytes = TEST_IMAGE.read_bytes()
    language, text = service.extract_text(image_bytes)

    assert language == "en"
    assert len(text) > 0


def test_reconstruct_text_by_lines_orders_words_left_to_right():
    service = OCRService(ImageProcessor())
    fake_data = {
        "level": [5, 5, 5],
        "text": ["world", "hello", "!"],
        "conf": ["95", "90", "80"],
        "page_num": [1, 1, 1],
        "block_num": [1, 1, 1],
        "par_num": [1, 1, 1],
        "line_num": [1, 1, 1],
        "left": [60, 10, 120],
        "top": [10, 10, 10],
        "width": [40, 40, 10],
        "height": [10, 10, 10],
    }

    text = service._reconstruct_text_by_lines(fake_data)
    assert text.strip() == "hello world !"


def test_detect_language_handles_empty_text():
    service = OCRService(ImageProcessor())
    assert service._detect_language("") == "unknown"