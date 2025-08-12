import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createDeployment } from "../api";
import { CreateDeploymentDTO } from "../dto/CreateDeploymentDTO";
import { deploymentsQueryKeyFactory } from "./deploymentsQueryKeyFactory";

export function useCreateDeployment() {
    const queryClient = useQueryClient();
    
    return useMutation({
        mutationFn: (dto: CreateDeploymentDTO) => createDeployment(dto),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: deploymentsQueryKeyFactory.all });
        },
    });
}