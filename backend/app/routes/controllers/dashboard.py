from typing import Dict, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_document_stats_service
from app.repositories.entities.AggregationResultEntity import AggregationResultEntity
from app.services.interfaces.IDocumentStatsService import IDocumentStatsService
from app.routes.dto.AggregationResultDTO import AggregationResultDTO
from app.routes.dto.PaginationDTO import PaginationDTO


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(service: IDocumentStatsService = Depends(get_document_stats_service)) -> Dict[str, Dict[str, int]]:
    # Backward-compatible combined response
    return {
        "agreement_types": {r.category: r.count for r in service.get_agreement_type_counts()},
        "jurisdictions": {r.category: r.count for r in service.get_country_counts()},
        "industries": {r.category: r.count for r in service.get_industry_counts(limit=1000)},
    }


@router.get("/agreement-types", response_model=List[AggregationResultDTO])
def get_agreement_type_counts(service: IDocumentStatsService = Depends(get_document_stats_service)) -> List[AggregationResultDTO]:
    return [AggregationResultDTO(category=r.category, count=r.count) for r in service.get_agreement_type_counts()]


@router.get("/countries", response_model=List[AggregationResultDTO])
def get_country_counts(service: IDocumentStatsService = Depends(get_document_stats_service)) -> List[AggregationResultDTO]:
    return [AggregationResultDTO(category=r.category, count=r.count) for r in service.get_country_counts()]


@router.get("/industries", response_model=PaginationDTO[AggregationResultDTO])
def get_industry_counts(
    service: IDocumentStatsService = Depends(get_document_stats_service),
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sort: str = Query("desc", pattern="^(?i)(asc|desc)$"),
) -> PaginationDTO[AggregationResultDTO]:
    page = service.get_industry_counts(limit=limit, offset=offset, sort=sort)
    return PaginationDTO[AggregationResultDTO](
        items=[AggregationResultDTO(category=r.category, count=r.count) for r in page.items],
        offset=page.offset,
        limit=page.limit,
        total=page.total,
    )


