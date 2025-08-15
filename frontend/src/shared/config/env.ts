export type AppConfig = {
  useMocks: boolean;
  baseUrl: string;
};

const viteEnvVariables = (import.meta as any)?.env ?? {};

console.log(viteEnvVariables);

export const config: AppConfig = {
    useMocks: viteEnvVariables.VITE_USE_MOCKS === "true",
    baseUrl: viteEnvVariables.VITE_BASE_URL || "/api",
} 