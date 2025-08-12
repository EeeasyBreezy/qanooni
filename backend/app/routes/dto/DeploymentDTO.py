from pydantic import BaseModel, Field
from datetime import datetime


class DeploymentDTO(BaseModel):
    id: str = Field(..., min_length=1, max_length=50, description="Deployment ID")
    name: str = Field(..., min_length=1, max_length=50, description="Deployment Name")
    description: str = Field(..., min_length=1, max_length=50, description="Deployment Description")
    created_at: datetime = Field(..., description="Deployment Creation Date")
    updated_at: datetime = Field(..., description="Deployment Last Update Date")