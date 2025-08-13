from abc import ABC, abstractmethod


class IImageProcessor(ABC):
    @abstractmethod
    def grayscale(self, image: bytes) -> bytes:
        pass

    @abstractmethod
    def denoise(self, image: bytes) -> bytes:
        pass

    @abstractmethod
    def binarize(self, image: bytes) -> bytes:
        pass