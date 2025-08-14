from typing import Dict, Optional
import re

from app.common.model.Pagination import Pagination
from app.repositories.interfaces.IDocumentRepository import IDocumentRepository
from app.services.interfaces.IDocumentQueryService import IDocumentQueryService
from app.services.model.SearchRow import SearchRow


class DocumentQueryService(IDocumentQueryService):
    def __init__(self, repository: IDocumentRepository):
        self._repo = repository

    def _derive_filters(self, question: str) -> Dict[str, Optional[str]]:
        q = question.lower()
        jurisdiction = None
        agreement_type = None
        if "governed by" in q:
            after = q.split("governed by", 1)[1]
            jurisdiction = after.strip().split(" ")[0].strip().strip("?.,")
        for key in [
            "nda",
            "msa",
            "service",
            "license",
            "employment",
            "lease",
            "supply",
            "dpa",
        ]:
            if key in q:
                agreement_type = key
                break
        return {"jurisdiction": jurisdiction, "agreement_type": agreement_type}

    def run_query(self, *, question: str, limit: int, offset: int) -> Pagination[SearchRow]:
        filters = self._derive_filters(question)
        fts_query = self._build_fts_query(question)
        page = self._repo.search(
            fts_query=fts_query,
            jurisdiction=filters["jurisdiction"],
            agreement_type=filters["agreement_type"],
            limit=limit,
            offset=offset,
        )
        items = [
            SearchRow(
                document=r.get("file_name", ""),
                governing_law=r.get("jurisdiction"),
                agreement_type=r.get("agreement_type"),
                industry=r.get("industry"),
                score=r.get("rank"),
            )
            for r in page.items
        ]
        return Pagination(items=items, offset=page.offset, limit=page.limit, total=page.total)

    def _build_fts_query(self, question: str) -> Optional[str]:
        # Tokenize: keep alphanumerics, drop short tokens/punctuation
        tokens = re.findall(r"[A-Za-z0-9]+", question.lower())
        tokens = [t for t in tokens if len(t) > 1]
        if not tokens:
            return None
        # Build a simple OR query with wildcard suffix to broaden matches
        # Example: token1* OR token2* OR token3*
        parts = [f"{t}*" for t in tokens]
        return " OR ".join(parts)


