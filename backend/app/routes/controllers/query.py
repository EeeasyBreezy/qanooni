from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.implementations.DocumentRepository import DocumentRepository


router = APIRouter(prefix="/query", tags=["query"])


class QueryRequest(BaseModel):
    question: str
    limit: int = 50
    offset: int = 0


class QueryResponseRow(BaseModel):
    document: str
    governing_law: Optional[str]
    agreement_type: Optional[str]
    industry: Optional[str]
    score: Optional[float]


def _derive_filters(question: str) -> Dict[str, Optional[str]]:
    q = question.lower()
    jurisdiction = None
    agreement_type = None
    # naive patterns
    if "governed by" in q:
        after = q.split("governed by", 1)[1]
        jurisdiction = after.strip().split(" ")[0].strip().strip("?.,")
    # simple detection of common types
    for key in ["nda", "msa", "service", "license", "employment", "lease", "supply", "dpa"]:
        if key in q:
            agreement_type = key
            break
    return {"jurisdiction": jurisdiction, "agreement_type": agreement_type}


@router.post("")
def run_query(req: QueryRequest, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    repo = DocumentRepository(db)
    filters = _derive_filters(req.question)
    results = repo.search(
        fts_query=req.question,
        jurisdiction=filters["jurisdiction"],
        agreement_type=filters["agreement_type"],
        limit=req.limit,
        offset=req.offset,
    )
    rows: List[Dict[str, Any]] = []
    for r in results:
        rows.append(
            {
                "document": r.get("file_name"),
                "governing_law": r.get("jurisdiction"),
                "agreement_type": r.get("agreement_type"),
                "industry": r.get("industry"),
                "score": r.get("rank"),
            }
        )
    return rows


