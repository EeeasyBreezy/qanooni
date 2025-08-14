from typing import Optional
from pydantic import BaseModel


class QueryRowDTO(BaseModel):
    document: str
    governing_law: Optional[str]
    agreement_type: Optional[str]
    industry: Optional[str]
    score: Optional[float]


