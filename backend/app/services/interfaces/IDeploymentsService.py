from abc import ABC, abstractmethod
from app.services.model.Deployment import Deployment


class IDeploymentsService(ABC):
    @abstractmethod
    def get_by_id(self, id: str) -> Deployment:
        pass

    @abstractmethod
    def create(self, deployment: Deployment) -> Deployment:
        pass