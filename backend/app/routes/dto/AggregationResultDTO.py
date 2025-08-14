from pydantic import BaseModel


class AggregationResultDTO(BaseModel):
    category: str
    count: int


