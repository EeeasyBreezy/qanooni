import { UploadStatus } from "./UploadStatus";


export type UploadItem = {
    id: string;
    file: File;
    status: UploadStatus;
    progress: number;
    errorMessage?: string;
    abortController?: AbortController;
  };
  