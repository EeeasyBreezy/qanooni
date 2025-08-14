import React from "react";
import { useUploadFiles } from "@entities/files/queries/useUploadFiles";
import { ContentTypes } from "@shared/consts/ContentTypes";

export type UploadStatus =
  | "idle"
  | "uploading"
  | "success"
  | "error"
  | "aborted";

export type UploadItem = {
  id: string;
  file: File;
  status: UploadStatus;
  progress: number;
  errorMessage?: string;
  abortController?: AbortController;
};

export const useUploadPage = () => {
  const [items, setItems] = React.useState<UploadItem[]>([]);
  const { mutateAsync: upload } = useUploadFiles();
  const allowedTypes = [ContentTypes.pdf, ContentTypes.docx];

  const addFiles = React.useCallback((files: FileList | null) => {
    if (!files) return;
    const newItems: UploadItem[] = Array.from(files)
      .filter((f) => allowedTypes.includes(f.type) || /\.pdf$/i.test(f.name) || /\.docx$/i.test(f.name))
      .map((f) => ({
        id: `${f.name}-${Date.now()}-${Math.random()}`,
        file: f,
        status: "idle" as const,
        progress: 0,
      }));
    setItems((prev) => [...newItems, ...prev]);
  }, []);

  const startUpload = React.useCallback(
    async (itemId: string) => {
      setItems((prev) =>
        prev.map((i) =>
          i.id === itemId
            ? {
                ...i,
                status: "uploading",
                progress: 0,
                errorMessage: undefined,
              }
            : i
        )
      );
      const item = items.find((i) => i.id === itemId);
      if (!item) return;
      const controller = new AbortController();
      setItems((prev) =>
        prev.map((i) =>
          i.id === itemId ? { ...i, abortController: controller } : i
        )
      );
      try {
        await upload({
          file: item.file,
          onProgress: (p) =>
            setItems((prev) =>
              prev.map((i) => (i.id === itemId ? { ...i, progress: p } : i))
            ),
          signal: controller.signal,
        });
        setItems((prev) =>
          prev.map((i) =>
            i.id === itemId
              ? {
                  ...i,
                  status: "success",
                  progress: 100,
                  abortController: undefined,
                }
              : i
          )
        );
      } catch (e: any) {
        setItems((prev) =>
          prev.map((i) =>
            i.id === itemId
              ? {
                  ...i,
                  status: controller.signal.aborted ? "aborted" : "error",
                  errorMessage: e?.message ?? "Upload failed",
                  abortController: undefined,
                }
              : i
          )
        );
      }
    },
    [items, upload]
  );

  const abortUpload = React.useCallback(
    (itemId: string) => {
      const item = items.find((i) => i.id === itemId);
      item?.abortController?.abort();
      setItems((prev) =>
        prev.map((i) => (i.id === itemId ? { ...i, status: "aborted" } : i))
      );
    },
    [items]
  );

  const retryUpload = React.useCallback(
    (itemId: string) => {
      void startUpload(itemId);
    },
    [startUpload]
  );

  const removeItem = React.useCallback((itemId: string) => {
    setItems((prev) => prev.filter((i) => i.id !== itemId));
  }, []);

  return {
    items,
    addFiles,
    startUpload,
    abortUpload,
    retryUpload,
    removeItem,
  };
};
