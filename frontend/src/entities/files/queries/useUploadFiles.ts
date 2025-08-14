import { useMutation } from '@tanstack/react-query';
import { uploadFile } from '../api';
import type { UploadResponseDTO } from '../dto/UploadResponseDTO';
import type { UploadRequestDTO } from '../dto/UploadRequestDTO';

interface UseUploadFilesPayload extends UploadRequestDTO {
  onProgress?: (p: number) => void;
  signal?: AbortSignal;
}

export const useUploadFiles = () => {
  return useMutation({
    mutationFn: async (params: UseUploadFilesPayload): Promise<UploadResponseDTO> => {
      return uploadFile({ file: params.file }, { onProgress: params.onProgress, signal: params.signal });
    },
  });
};


