import { UploadItem } from "../model/UploadItem";


export const mapFileListToUploadItemList = (files: File[] | FileList): UploadItem[] => {
  const array: File[] = Array.from(files as any);
  
  return array.map((f) => ({
    id: `${f.name}-${Date.now()}-${Math.random()}`,
    file: f,
    status: 'idle',
    progress: 0,
  }));
};


