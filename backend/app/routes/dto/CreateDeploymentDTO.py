from pydantic import BaseModel, Field


class CreateDeploymentDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Deployment Name")
    description: str = Field(..., min_length=1, max_length=50, description="Deployment Description")