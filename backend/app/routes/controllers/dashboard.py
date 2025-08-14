from typing import Dict, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.implementations.DocumentRepository import DocumentRepository
from app.repositories.entities.AggregationResultEntity import AggregationResultEntity


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(db: Session = Depends(get_db)) -> Dict[str, Dict[str, int]]:
    repo = DocumentRepository(db)
    return repo.get_aggregations()


@router.get("/agreement-types")
def get_agreement_type_counts(db: Session = Depends(get_db)) -> List[AggregationResultEntity]:
    repo = DocumentRepository(db)
    return repo.count_by_agreement_type()


@router.get("/countries")
def get_country_counts(db: Session = Depends(get_db)) -> List[AggregationResultEntity]:
    repo = DocumentRepository(db)
    return repo.count_by_country()


@router.get("/industries")
def get_industry_counts(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    sort: str = Query("desc", pattern="^(?i)(asc|desc)$"),
) -> List[AggregationResultEntity]:
    repo = DocumentRepository(db)
    return repo.count_by_industry(limit=limit, offset=offset, sort=sort)


