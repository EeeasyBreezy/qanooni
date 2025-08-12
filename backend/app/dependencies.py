from functools import lru_cache
from fastapi import Depends
from app.repositories.interfaces.IDeploymentRepository import IDeploymentRepository
from app.repositories.implementations.DeploymentRepository import DeploymentRepository
from app.services.interfaces.IDeploymentsService import IDeploymentsService
from app.services.implementations.DeploymentsService import DeploymentsService

def get_deployment_repository() -> IDeploymentRepository:
    return DeploymentRepository()

def get_deployments_service(
    repo: IDeploymentRepository = Depends(get_deployment_repository),
) -> IDeploymentsService:
    return DeploymentsService(repo)