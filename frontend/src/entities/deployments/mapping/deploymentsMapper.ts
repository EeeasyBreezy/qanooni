import { DeploymentDTO } from "../dto/DeploymentDTO";
import { Deployment } from "../model/Deployment";

export function deploymentDTOToDeployment(dto: DeploymentDTO): Deployment {
    return {
        id: dto.id,
        name: dto.name,
        description: dto.description,
        createdAt: dto.createdAt,
        updatedAt: dto.updatedAt,
    };
}