import { httpClient } from '@shared/http/httpClient';
import { filesApiPaths } from '../apiPaths';
import type { UploadResponseDTO } from '../dto/UploadResponseDTO';
import type { UploadRequestDTO } from '../dto/UploadRequestDTO';

export const uploadFile = async (
  payload: UploadRequestDTO,
  options?: { onProgress?: (progress: number) => void; signal?: AbortSignal }
): Promise<UploadResponseDTO> => {
  const form = new FormData();
  form.append('file', payload.file);

  return httpClient.post<UploadResponseDTO>(filesApiPaths.root, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    signal: options?.signal,
    onUploadProgress: (e) => {
      const onProgress = options?.onProgress;
      if (e.total && onProgress) {
        const percent = Math.round((e.loaded * 100) / e.total);
        onProgress(percent);
      }
    },
  });
};


