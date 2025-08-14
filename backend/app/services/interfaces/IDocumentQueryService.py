from abc import ABC, abstractmethod
from app.common.model.Pagination import Pagination
from app.services.model.SearchRow import SearchRow


class IDocumentQueryService(ABC):
    @abstractmethod
    def run_query(self, *, question: str, limit: int, offset: int) -> Pagination[SearchRow]:
        """Executes a natural-language query and returns a paginated list of rows."""
        raise NotImplementedError


