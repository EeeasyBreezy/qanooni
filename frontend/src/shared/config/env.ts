export type AppConfig = {
  useMocks: boolean;
  baseUrl: string;
};

const viteEnvVariables = (import.meta as any)?.env ?? {};

export const config: AppConfig = {
    useMocks: viteEnvVariables.VITE_USE_MOCKS === "enabled",
    baseUrl: viteEnvVariables.VITE_BASE_URL || "/api",
} 