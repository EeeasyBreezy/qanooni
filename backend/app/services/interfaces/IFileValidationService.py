from abc import ABC, abstractmethod


class IFileValidationService(ABC):
    @abstractmethod
    def validate_and_get_mime(self, file_name: str, content: bytes) -> str:
        """
        Validates that the provided file is supported and consistent.

        - Only PDF and DOCX are supported
        - Magic bytes must match the file extension

        Returns the normalized MIME type string for the file if valid.
        Raises ValueError with a human-readable message when invalid.
        """
        pass


