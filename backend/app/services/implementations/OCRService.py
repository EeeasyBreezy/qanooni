from typing import Dict, List, Tuple
from io import BytesIO

from PIL import Image
import pytesseract
from langdetect import detect, DetectorFactory

from app.services.interfaces.IOCR import IOCR


# Make langdetect deterministic
DetectorFactory.seed = 0


class OCRService(IOCR):
    ROW_BIN_SIZE_PX = 10

    def extract_text_and_tables(self, image_bytes: bytes) -> Tuple[str, str, List[List[List[str]]]]:
        image = self._load_image(image_bytes)
        ocr_data = self._run_ocr(image)
        text = self._reconstruct_text_by_lines(ocr_data)
        language = self._detect_language(text)
        tables = self._extract_tables(ocr_data)
        return language, text, tables

    def _load_image(self, image_bytes: bytes) -> Image.Image:
        return Image.open(BytesIO(image_bytes)).convert("RGB")

    def _run_ocr(self, image: Image.Image) -> Dict[str, List]:
        return pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    def _reconstruct_text_by_lines(self, data: Dict[str, List]) -> str:
        lines: Dict[Tuple[int, int, int, int], List[Tuple[int, str]]] = {}
        count_items = len(data["level"]) if "level" in data else 0
        for i in range(count_items):
            text = data["text"][i]
            conf = data["conf"][i]
            if not text or not text.strip() or conf == "-1":
                continue
            line_key = (
                data["page_num"][i],
                data["block_num"][i],
                data["par_num"][i],
                data["line_num"][i],
            )
            lines.setdefault(line_key, []).append((data["left"][i], text))

        ordered_lines: List[str] = []
        for key in sorted(lines.keys()):
            chunks = sorted(lines[key], key=lambda x: x[0])
            ordered_lines.append(" ".join([t for _, t in chunks]))
        return "\n".join(ordered_lines).strip()

    def _detect_language(self, text: str) -> str:
        if not text or not text.strip():
            return "unknown"
        try:
            sample = text[:1000]
            return detect(sample)
        except Exception:
            return "unknown"

    def _extract_tables(self, data: Dict[str, List]) -> List[List[List[str]]]:
        tables: List[List[List[str]]] = []
        try:
            count_items = len(data["level"]) if "level" in data else 0
            rows_by_y: Dict[int, List[Dict[str, int | str]]] = {}
            for i in range(count_items):
                if not data["text"][i] or data["conf"][i] == "-1":
                    continue
                top = data["top"][i]
                y_key = round(top / self.ROW_BIN_SIZE_PX)
                rows_by_y.setdefault(y_key, []).append(
                    {
                        "left": data["left"][i],
                        "right": data["left"][i] + data["width"][i],
                        "text": data["text"][i],
                    }
                )

            candidate_rows: List[List[str]] = []
            for y_key in sorted(rows_by_y.keys()):
                cells = sorted(rows_by_y[y_key], key=lambda c: c["left"])
                candidate_rows.append([str(c["text"]) for c in cells])

            if candidate_rows:
                lengths = [len(r) for r in candidate_rows if len(r) > 1]
                if lengths:
                    common = max(set(lengths), key=lengths.count)
                    table = [r for r in candidate_rows if len(r) == common]
                    if len(table) >= 2:
                        tables.append(table)
        except Exception:
            # Keep OCR robust; if table heuristic fails, just return empty tables
            return []
        return tables


