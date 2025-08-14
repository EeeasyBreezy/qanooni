export type AppConfig = {
  useMocks: boolean;
};

const viteEnvVariables = import.meta as any;

export const config: AppConfig = {
    useMocks: viteEnvVariables.VITE_USE_MOCKS === "true",
}