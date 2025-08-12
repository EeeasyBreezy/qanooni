export const deploymentsApiPaths = {
    deployments: "/api/deployments",
    deployment: (id: string) => `/api/deployments/${id}`,
} as const;