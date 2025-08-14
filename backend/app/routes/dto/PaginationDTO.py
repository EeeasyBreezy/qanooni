from typing import Generic, List, Sequence, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class PaginationDTO(BaseModel, Generic[T]):
    items: List[T]
    offset: int
    limit: int
    total: int


