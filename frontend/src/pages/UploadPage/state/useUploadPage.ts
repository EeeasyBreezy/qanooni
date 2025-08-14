import React from "react";
import { useUploadFiles } from "@entities/files/queries/useUploadFiles";
import { ContentTypes } from "@shared/consts/ContentTypes";
import { UploadItem } from "../model/UploadItem";
import { mapFileListToUploadItemList } from "../mapping/mapFileListToUploadItemList";

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

    const newItems = mapFileListToUploadItemList(files).filter(
        (i) =>
          allowedTypes.includes(i.file.type) ||
          /\.pdf$/i.test(i.file.name) ||
          /\.docx$/i.test(i.file.name)
      );
    const newIds = newItems.map((i) => i.id);

    setState((prev) => {
      const nextById = { ...prev.byId } as Record<string, UploadItem>;
      newItems.forEach((i) => {
        nextById[i.id] = {...i, status: "uploading"};
      });
      return { byId: nextById, order: [...newIds, ...prev.order] };
    });

    newItems.forEach((i) => void startUploadHelper(i.id, i.file));
    
  };

  const startUploadHelper = async (fileId: string, file: File) => {
    const controller = new AbortController();
    try {
        await upload({
          file: file,
          onProgress: (p) =>
            setState((prev) => {
              const existing = prev.byId[fileId];
              if (!existing) return prev;
              return {
                byId: { ...prev.byId, [fileId]: { ...existing, progress: p } },
                order: prev.order,
              };
            }),
          signal: controller.signal,
        });
        setState((prev) => {
          const existing = prev.byId[fileId];
          if (!existing) return prev;
          const updated: UploadItem = {
            ...existing,
            status: "success",
            progress: 100,
            abortController: undefined,
          };
          return {
            byId: { ...prev.byId, [fileId]: updated },
            order: prev.order,
          };
        });
      } catch (e: any) {
        setState((prev) => {
          const existing = prev.byId[fileId];
          if (!existing) return prev;
          const updated: UploadItem = {
            ...existing,
            status: controller.signal.aborted ? "aborted" : "error",
            errorMessage: e?.message ?? "Upload failed",
            abortController: undefined,
          };
          return {
            byId: { ...prev.byId, [fileId]: updated },
            order: prev.order,
          };
        });
      }
  }

  const startUpload = async (itemId: string, fileOverride?: File) => {
    let fileToUpload: File | undefined;
    const controller = new AbortController();
    setState((prev) => {
      const existing = prev.byId[itemId];
      const chosen = fileOverride ?? existing?.file;
      if (!chosen) return prev;
      fileToUpload = chosen;
      const updated: UploadItem = {
        ...(existing ?? { id: itemId, file: chosen, status: "idle" as const, progress: 0 }),
        status: "uploading",
        progress: 0,
        errorMessage: undefined,
        abortController: controller,
      };

      return { byId: { ...prev.byId, [itemId]: updated }, order: prev.order };
    });

    if (!fileToUpload) return;

    await startUploadHelper(itemId, fileToUpload);
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
