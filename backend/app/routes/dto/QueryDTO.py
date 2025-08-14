from typing import List, Optional
from pydantic import BaseModel


class QueryRequestDTO(BaseModel):
    question: str
    limit: int
    offset: int


class QueryRowDTO(BaseModel):
    document: str
    governing_law: Optional[str]
    agreement_type: Optional[str]
    industry: Optional[str]
    score: Optional[float]


class QueryResponseDTO(BaseModel):
    items: List[QueryRowDTO]
    limit: int
    offset: int
    total: int


