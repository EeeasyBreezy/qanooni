from abc import ABC, abstractmethod
from app.repositories.entities.DeploymentEntity import DeploymentEntity


class IDeploymentRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> DeploymentEntity:
        pass

    @abstractmethod
    def create(self, entity: DeploymentEntity) -> DeploymentEntity:
        pass

    @abstractmethod
    def update(self, entity: DeploymentEntity) -> DeploymentEntity:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass