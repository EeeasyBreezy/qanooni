from abc import ABC, abstractmethod
from typing import List, Optional

from app.services.model.File import File


class IUploadService(ABC):
    @abstractmethod
    def upload_files(self, files: List[File]) -> List[str]:
        pass