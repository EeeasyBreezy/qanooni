from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SearchRow:
    document: str
    governing_law: Optional[str]
    agreement_type: Optional[str]
    industry: Optional[str]
    score: Optional[float]


