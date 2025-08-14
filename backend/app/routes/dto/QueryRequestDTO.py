from pydantic import BaseModel


class QueryRequestDTO(BaseModel):
    question: str
    limit: int
    offset: int


