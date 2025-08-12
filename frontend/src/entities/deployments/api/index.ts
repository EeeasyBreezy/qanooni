import { httpClient } from "../../../shared/http/httpClient";
import { CreateDeploymentDTO } from "../dto/CreateDeploymentDTO";
import { DeploymentDTO } from "../dto/DeploymentDTO";
import { deploymentsApiPaths } from "../apiPaths";

export async function createDeployment(dto: CreateDeploymentDTO): Promise<DeploymentDTO> {
    const res = await httpClient.post<DeploymentDTO, CreateDeploymentDTO>(deploymentsApiPaths.deployments, dto);
    return res;
}

export async function getDeployments(offset: number, limit: number): Promise<DeploymentDTO[]> {
    const res = await httpClient.get<DeploymentDTO[]>(deploymentsApiPaths.deployments, {
        params: {
            offset,
            limit,
        },
    });
    return res;
}