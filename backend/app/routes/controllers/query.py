from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_document_query_service
from app.routes.dto.QueryRequestDTO import QueryRequestDTO
from app.routes.dto.QueryResponseDTO import QueryResponseDTO
from app.routes.dto.QueryRowDTO import QueryRowDTO
from app.services.interfaces.IDocumentQueryService import IDocumentQueryService


router = APIRouter(prefix="/query", tags=["query"])

@router.post("", response_model=QueryResponseDTO)
def run_query(req: QueryRequestDTO, service: IDocumentQueryService = Depends(get_document_query_service)) -> QueryResponseDTO:
    page = service.run_query(question=req.question, limit=req.limit, offset=req.offset)
    return QueryResponseDTO(
        items=[
            QueryRowDTO(
                document=r.document,
                governing_law=r.governing_law,
                agreement_type=r.agreement_type,
                industry=r.industry,
                score=r.score,
            )
            for r in page.items
        ],
        limit=page.limit,
        offset=page.offset,
        total=page.total,
    )


