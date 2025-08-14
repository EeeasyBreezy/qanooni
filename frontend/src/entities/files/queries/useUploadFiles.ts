import { useMutation } from '@tanstack/react-query';
import { uploadFiles } from '../api';
import type { UploadResponseDTO } from '../dto/UploadResponseDTO';
import type { UploadRequestDTO } from '../dto/UploadRequestDTO';

interface UseUploadFilesPayload extends UploadRequestDTO {
  onProgress?: (p: number) => void;
}

export const useUploadFiles = () => {
  return useMutation({
    mutationFn: async (params: UseUploadFilesPayload): Promise<UploadResponseDTO> => {
      return uploadFiles(params.files, params.onProgress);
    },
  });
};


