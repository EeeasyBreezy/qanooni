from fastapi import APIRouter, Depends
from app.dependencies import get_document_query_service
from app.routes.dto.QueryResponseDTO import QueryResponseDTO
from app.routes.dto.QueryRowDTO import QueryRowDTO
from app.services.interfaces.IDocumentQueryService import IDocumentQueryService
from fastapi import Query


router = APIRouter(prefix="/query", tags=["query"])

@router.get("", response_model=QueryResponseDTO)
def run_query(
    question: str = Query(..., description="Natural language question"),
    limit: int = Query(..., ge=1, le=1000),
    offset: int = Query(..., ge=0),
    service: IDocumentQueryService = Depends(get_document_query_service),
) -> QueryResponseDTO:
    page = service.run_query(question=question, limit=limit, offset=offset)
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


