from fastapi import APIRouter, Query, Depends
from app.routes.dto.PostGreetDTO import PostGreetDTO
from app.services.interfaces.IDeploymentsService import IDeploymentsService
from app.dependencies import get_deployments_service  # or the singleton variant
from app.services.model.Deployment import Deployment
import uuid
from datetime import datetime

router = APIRouter(prefix="/greeting", tags=["greeting"])

@router.get("")
def greeting(name: str = Query("World", min_length=1, max_length=50)):
    return {"message": f"Hello, {name}!"}

@router.post("")
def post_greet(dto: PostGreetDTO, service: IDeploymentsService = Depends(get_deployments_service)):
    deployment = Deployment(
        id=str(uuid.uuid4()),
        name=dto.name,
        description="Some desription here",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    service.create(deployment)
    return {"message": f"Hello, {dto.name}!"}