from typing import Optional


class QueryRowDTO:
    def __init__(
        self,
        document: str,
        governing_law: Optional[str],
        agreement_type: Optional[str],
        industry: Optional[str],
        score: Optional[float],
    ):
        self.document = document
        self.governing_law = governing_law
        self.agreement_type = agreement_type
        self.industry = industry
        self.score = score


