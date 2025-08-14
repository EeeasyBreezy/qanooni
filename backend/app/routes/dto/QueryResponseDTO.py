from typing import List
from pydantic import BaseModel
from app.routes.dto.QueryRowDTO import QueryRowDTO


class QueryResponseDTO(BaseModel):
    items: List[QueryRowDTO]
    limit: int
    offset: int
    total: int