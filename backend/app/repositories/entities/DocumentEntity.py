from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DocumentEntity:
    id: Optional[int]
    file_name: str
    mime_type: str
    size_bytes: int
    text: str

    agreement_type: Optional[str]
    jurisdiction: Optional[str]
    industry: Optional[str]
    geography_mentioned: List[str]


