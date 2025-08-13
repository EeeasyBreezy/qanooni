import numpy as np
import cv2

from app.services.implementations.ImageProcessor import ImageProcessor

class TestImageProcessor:
    def _encode_png(self, mat: np.ndarray) -> bytes:
        ok, buf = cv2.imencode(".png", mat)
        assert ok, "Failed to encode test image"
        return buf.tobytes()


    def _decode_png(self, data: bytes, flags=cv2.IMREAD_UNCHANGED) -> np.ndarray:
        arr = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(arr, flags)
        assert img is not None, "Failed to decode output image"
        return img


    def test_grayscale_returns_single_channel_image(self):
        # Create a simple color image (BGR)
        color = np.zeros((50, 50, 3), dtype=np.uint8)
        color[:, :25] = (0, 0, 255)  # Red half
        color[:, 25:] = (0, 255, 0)  # Green half
        data = self._encode_png(color)

        proc = ImageProcessor()
        out_bytes = proc.grayscale(data)
        out = self._decode_png(out_bytes, flags=cv2.IMREAD_UNCHANGED)

        assert out.ndim == 2, "Expected single-channel grayscale output"
        assert out.shape == color.shape[:2]


    def test_denoise_reduces_noise_variance(self):
        # Start with a uniform gray image and add Gaussian noise
        base = np.full((80, 80), 128, dtype=np.uint8)
        noise = np.random.normal(0, 25, base.shape).astype(np.int16)
        noisy = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        # Convert to 3-channel BGR to match typical input
        noisy_bgr = cv2.cvtColor(noisy, cv2.COLOR_GRAY2BGR)
        data = self._encode_png(noisy_bgr)

        proc = ImageProcessor()
        out_bytes = proc.denoise(data)
        out = self._decode_png(out_bytes, flags=cv2.IMREAD_GRAYSCALE)

        std_before = float(noisy.std())
        std_after = float(out.std())
        assert std_after < std_before, f"Expected reduced noise: before={std_before}, after={std_after}"


    def test_binarize_outputs_binary_values_only(self):
        # Create a synthetic image with a bright and dark half
        left = np.full((60, 60), 40, dtype=np.uint8)
        right = np.full((60, 60), 220, dtype=np.uint8)
        gray = np.concatenate([left, right], axis=1)
        bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        data = self._encode_png(bgr)

        proc = ImageProcessor()
        out_bytes = proc.binarize(data)
        out = self._decode_png(out_bytes, flags=cv2.IMREAD_GRAYSCALE)

        uniques = np.unique(out)
        # Allow either {0,255} or a subset if thresholding collapses
        assert set(uniques.tolist()).issubset({0, 255})
        assert len(uniques) >= 1