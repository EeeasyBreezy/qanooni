from dataclasses import dataclass


@dataclass(frozen=True)
class AggregationResultEntity:
    category: str
    count: int