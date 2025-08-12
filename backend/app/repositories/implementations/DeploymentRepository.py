from app.repositories.interfaces.IDeploymentRepository import IDeploymentRepository
from app.repositories.entities.DeploymentEntity import DeploymentEntity


class DeploymentRepository(IDeploymentRepository):
    def get_by_id(self, id: str) -> DeploymentEntity:
        pass

    def create(self, entity: DeploymentEntity) -> DeploymentEntity:
        pass

    def update(self, entity: DeploymentEntity) -> DeploymentEntity:
        pass