from dataclasses import dataclass


@dataclass(frozen=True)
class AggregationResult:
    category: str
    count: int


