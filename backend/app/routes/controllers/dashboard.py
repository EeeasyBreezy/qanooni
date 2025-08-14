from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.implementations.DocumentRepository import DocumentRepository


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(db: Session = Depends(get_db)) -> Dict[str, Dict[str, int]]:
    repo = DocumentRepository(db)
    return repo.get_aggregations()


