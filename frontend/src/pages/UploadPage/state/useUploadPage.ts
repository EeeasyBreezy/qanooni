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

type UploadItemsState = {
  byId: Record<string, UploadItem>;
  order: string[];
};

export const useUploadPage = () => {
  const [state, setState] = React.useState<UploadItemsState>({
    byId: {},
    order: [],
  });
  const { mutateAsync: upload } = useUploadFiles();
  const allowedTypes = [ContentTypes.pdf, ContentTypes.docx];

  const addFiles = async (files: FileList | null) => {
    if (!files) return;
    const newItems: UploadItem[] = Array.from(files)
      .filter(
        (f) =>
          allowedTypes.includes(f.type) ||
          /\.pdf$/i.test(f.name) ||
          /\.docx$/i.test(f.name)
      )
      .map((f) => ({
        id: `${f.name}-${Date.now()}-${Math.random()}`,
        file: f,
        status: "idle" as const,
        progress: 0,
      }));
    const newIds = newItems.map((i) => i.id);
    setState((prev) => {
      const nextById = { ...prev.byId } as Record<string, UploadItem>;
      newItems.forEach((i) => {
        nextById[i.id] = i;
      });
      return { byId: nextById, order: [...newIds, ...prev.order] };
    });

    newIds.forEach((id) => void startUpload(id));
  };

  const startUpload = async (itemId: string) => {
    let fileToUpload: File | undefined;
    const controller = new AbortController();
    setState((prev) => {
      const existing = prev.byId[itemId];
      if (!existing) return prev;
      fileToUpload = existing.file;
      const updated: UploadItem = {
        ...existing,
        status: "uploading",
        progress: 0,
        errorMessage: undefined,
        abortController: controller,
      };
      return { byId: { ...prev.byId, [itemId]: updated }, order: prev.order };
    });
    if (!fileToUpload) return;
    try {
      await upload({
        file: fileToUpload,
        onProgress: (p) =>
          setState((prev) => {
            const existing = prev.byId[itemId];
            if (!existing) return prev;
            return {
              byId: { ...prev.byId, [itemId]: { ...existing, progress: p } },
              order: prev.order,
            };
          }),
        signal: controller.signal,
      });
      setState((prev) => {
        const existing = prev.byId[itemId];
        if (!existing) return prev;
        const updated: UploadItem = {
          ...existing,
          status: "success",
          progress: 100,
          abortController: undefined,
        };
        return {
          byId: { ...prev.byId, [itemId]: updated },
          order: prev.order,
        };
      });
    } catch (e: any) {
      setState((prev) => {
        const existing = prev.byId[itemId];
        if (!existing) return prev;
        const updated: UploadItem = {
          ...existing,
          status: controller.signal.aborted ? "aborted" : "error",
          errorMessage: e?.message ?? "Upload failed",
          abortController: undefined,
        };
        return {
          byId: { ...prev.byId, [itemId]: updated },
          order: prev.order,
        };
      });
    }
  };

  const abortUpload = (itemId: string) => {
    const existing = state.byId[itemId];
    existing?.abortController?.abort();
    setState((prev) => {
      const cur = prev.byId[itemId];
      if (!cur) return prev;
      return {
        byId: { ...prev.byId, [itemId]: { ...cur, status: "aborted" } },
        order: prev.order,
      };
    });
  };

  const retryUpload = (itemId: string) => {
    void startUpload(itemId);
  };

  const removeItem = (itemId: string) => {
    setState((prev) => {
      if (!prev.byId[itemId]) return prev;
      const nextById = { ...prev.byId } as Record<string, UploadItem>;
      delete nextById[itemId];
      const nextOrder = prev.order.filter((id) => id !== itemId);
      return { byId: nextById, order: nextOrder };
    });
  };

  const rows: UploadItem[] = state.order
    .map((id) => state.byId[id])
    .filter(Boolean) as UploadItem[];

  return {
    items: rows,
    addFiles,
    startUpload,
    abortUpload,
    retryUpload,
    removeItem,
  };
};
