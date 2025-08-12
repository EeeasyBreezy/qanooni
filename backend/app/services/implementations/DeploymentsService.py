from app.services.interfaces.IDeploymentsService import IDeploymentsService
from app.services.model.Deployment import Deployment
from app.repositories.interfaces.IDeploymentRepository import IDeploymentRepository
from app.common.NotFoundException import NotFoundException


class DeploymentsService(IDeploymentsService):
    def __init__(self, repository: IDeploymentRepository):
        self.repository = repository

    @override
    def get_by_id(self, id: str) -> Deployment:
        res = self.repository.get_by_id(id)
        if res is None:
            raise NotFoundException("Deployment not found")

        return res

    @override
    def create(self, deployment: Deployment) -> Deployment:
        res = self.repository.create(deployment)
        return res