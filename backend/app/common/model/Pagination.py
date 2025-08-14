from dataclasses import dataclass
from typing import Generic, List, TypeVar


T = TypeVar("T")


@dataclass(frozen=True)
class Pagination(Generic[T]):
    items: List[T]
    offset: int
    limit: int
    total: int


