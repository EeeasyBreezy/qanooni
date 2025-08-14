import { httpClient } from '@shared/http/httpClient';
import { filesApiPaths } from '../apiPaths';
import type { UploadResponseDTO } from '../dto/UploadResponseDTO';
import type { UploadRequestDTO } from '../dto/UploadRequestDTO';

export const uploadFile = async (
  payload: UploadRequestDTO,
  onProgress?: (progress: number) => void
): Promise<UploadResponseDTO> => {
  const form = new FormData();
  form.append('file', payload.file);

  return httpClient.post<UploadResponseDTO>(filesApiPaths.root, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => {
      if (!onProgress) return;
      if (e.total) {
        const percent = Math.round((e.loaded * 100) / e.total);
        onProgress(percent);
      }
    },
  });
};


