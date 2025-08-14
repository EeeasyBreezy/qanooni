import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';

export type HttpClientOptions = {
  baseURL?: string;
  timeoutMs?: number;
  defaultHeaders?: Record<string, string>;
};

export class HttpClient {
  private readonly instance: AxiosInstance;

  constructor(options: HttpClientOptions = {}) {
    const { baseURL = '/api', timeoutMs = 30_000, defaultHeaders } = options;

    this.instance = axios.create({
      baseURL,
      timeout: timeoutMs,
      headers: {
        ...defaultHeaders,
      },
      withCredentials: false,
    });

    this.instance.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => Promise.reject(error)
    );
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const res = await this.instance.get<T>(url, config);
    return res.data;
  }

  async post<TResponse, TPayload = unknown>(
    url: string,
    data?: TPayload,
    config?: AxiosRequestConfig
  ): Promise<TResponse> {
    const res = await this.instance.post<TResponse>(url, data, config);
    return res.data;
  }

  async put<TResponse, TPayload = unknown>(
    url: string,
    data?: TPayload,
    config?: AxiosRequestConfig
  ): Promise<TResponse> {
    const res = await this.instance.put<TResponse>(url, data, config);
    return res.data;
  }

  async delete<TResponse = void>(url: string, config?: AxiosRequestConfig): Promise<TResponse> {
    const res = await this.instance.delete<TResponse>(url, config);
    return res.data as TResponse;
  }
}

export const httpClient = new HttpClient({
  baseURL: (import.meta as any)?.env?.VITE_API_BASE_URL ?? '/api',
});