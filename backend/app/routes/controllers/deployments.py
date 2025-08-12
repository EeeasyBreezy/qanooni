from fastapi import APIRouter, Query, Depends
from app.services.interfaces.IDeploymentsService import IDeploymentsService
from app.dependencies import get_deployments_service  # or the singleton variant
from app.services.model.Deployment import Deployment
import uuid
from datetime import datetime
from app.routes.dto.CreateDeploymentDTO import CreateDeploymentDTO
from app.routes.dto.DeploymentDTO import DeploymentDTO

router = APIRouter(prefix="/deployments", tags=["deployments"])

@router.post("")
def create_deployment(dto: CreateDeploymentDTO, service: IDeploymentsService = Depends(get_deployments_service)) -> DeploymentDTO:
    deployment = Deployment(
        id=str(uuid.uuid4()),
        name=dto.name,
        description=dto.description,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    res = service.create(deployment)

    return DeploymentDTO(
        id=res.id,
        name=res.name,
        description=res.description,
        created_at=res.created_at,
        updated_at=res.updated_at,
    )
    