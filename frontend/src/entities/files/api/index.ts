import { httpClient } from '@shared/http/httpClient';
import { filesApiPaths } from '../apiPaths';
import type { UploadResponseDTO } from '../dto/UploadResponseDTO';

export const uploadFiles = async (
  files: File[],
  onProgress?: (progress: number) => void
): Promise<UploadResponseDTO> => {
  const form = new FormData();
  files.forEach((f) => form.append('files', f));

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


