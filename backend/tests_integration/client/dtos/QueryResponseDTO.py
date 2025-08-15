from typing import List
from .PaginationDTO import PaginationDTO
from .QueryRowDTO import QueryRowDTO


class QueryResponseDTO(PaginationDTO):
    def __init__(self, items: List[QueryRowDTO], limit: int, offset: int, total: int):
        super().__init__(items=items, limit=limit, offset=offset, total=total)


