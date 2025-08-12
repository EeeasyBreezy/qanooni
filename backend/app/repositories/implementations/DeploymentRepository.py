from app.repositories.interfaces.IDeploymentRepository import IDeploymentRepository
from app.repositories.entities.DeploymentEntity import DeploymentEntity


class DeploymentRepository(IDeploymentRepository):
    def __init__(self):
        self.d = {}

    def get_by_id(self, id: str) -> DeploymentEntity:
        if id not in self.d: return None

        return self.d[id]

    def create(self, entity: DeploymentEntity) -> DeploymentEntity:
        self.d[entity.id] = entity
        return entity

    def update(self, entity: DeploymentEntity) -> DeploymentEntity:
        self.d[entity.id] = entity
        return entity

    def delete(self, id: str) -> None:
        self.d.pop(id, None)