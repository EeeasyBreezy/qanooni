from typing import Tuple

import cv2
import numpy as np

from app.services.interfaces.IImageProcessor import IImageProcessor


class ImageProcessor(IImageProcessor):
	def grayscale(self, image: bytes) -> bytes:
		bgr = self._decode_image(image)
		gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
		return self._encode_image(gray)

	def denoise(self, image: bytes) -> bytes:
		bgr = self._decode_image(image)
		gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
		denoised = cv2.fastNlMeansDenoising(gray, h=15, templateWindowSize=7, searchWindowSize=21)
		return self._encode_image(denoised)

	def binarize(self, image: bytes) -> bytes:
		bgr = self._decode_image(image)
		gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
		_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		return self._encode_image(binary)

	def _decode_image(self, image_bytes: bytes) -> np.ndarray:
		buffer = np.frombuffer(image_bytes, dtype=np.uint8)
		mat = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
		if mat is None:
			raise ValueError("Failed to decode image bytes")
		return mat

	def _encode_image(self, mat: np.ndarray, ext: str = ".png") -> bytes:
		success, buf = cv2.imencode(ext, mat)
		if not success:
			raise ValueError("Failed to encode image to bytes")
		return buf.tobytes()