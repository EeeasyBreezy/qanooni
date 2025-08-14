import React from "react";
import PageContainer from "@shared/components/PageContainer";
import Typography from "@shared/components/Typography";
import Stack from "@shared/components/Stack";
import LinearProgress from "@shared/components/LinearProgress";
import IconButton from "@shared/components/IconButton";
import Button from "@shared/components/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import ReplayIcon from "@mui/icons-material/Replay";
import StopIcon from "@mui/icons-material/Stop";
import DataTable, { Column } from "@shared/components/DataTable";
import FileDropzone from "@shared/components/FileDropzone";
import { useUploadFiles } from "@entities/files/queries/useUploadFiles";

type UploadItem = {
  id: string;
  file: File;
  status: "idle" | "uploading" | "success" | "error" | "aborted";
  progress: number;
  errorMessage?: string;
  abortController?: AbortController;
};

const UploadPage: React.FC = () => {
  const [items, setItems] = React.useState<UploadItem[]>([]);

  const { mutateAsync: upload } = useUploadFiles();

  const addFiles = (files: FileList | null) => {
    if (!files) return;
    const newItems: UploadItem[] = Array.from(files)
      .filter(
        (f) =>
          [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
          ].includes(f.type) || /\.pdf$|\.docx$/i.test(f.name)
      )
      .map((f) => ({
        id: `${f.name}-${Date.now()}-${Math.random()}`,
        file: f,
        status: "idle",
        progress: 0,
      }));
    setItems((prev) => [...newItems, ...prev]);
  };

  const startUpload = async (itemId: string) => {
    setItems((prev) =>
      prev.map((i) =>
        i.id === itemId
          ? { ...i, status: "uploading", progress: 0, errorMessage: undefined }
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
  };

  const abortUpload = (itemId: string) => {
    const item = items.find((i) => i.id === itemId);
    item?.abortController?.abort();
    setItems((prev) =>
      prev.map((i) => (i.id === itemId ? { ...i, status: "aborted" } : i))
    );
  };

  const retryUpload = (itemId: string) => startUpload(itemId);
  const removeItem = (itemId: string) =>
    setItems((prev) => prev.filter((i) => i.id !== itemId));

  const columns: Column<UploadItem>[] = [
    { key: "name", header: "File", render: (r) => r.file.name },
    { key: "status", header: "Status", render: (r) => r.status },
    {
      key: "progress",
      header: "Progress",
      render: (r) => (
        <LinearProgress variant="determinate" value={r.progress} />
      ),
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <Stack direction="row" spacing={1} alignItems="center">
          {r.status === "uploading" && (
            <IconButton
              aria-label="abort"
              onClick={() => abortUpload(r.id)}
              size="small"
            >
              <StopIcon fontSize="small" />
            </IconButton>
          )}
          {(r.status === "error" || r.status === "aborted") && (
            <IconButton
              aria-label="retry"
              onClick={() => retryUpload(r.id)}
              size="small"
            >
              <ReplayIcon fontSize="small" />
            </IconButton>
          )}
          <IconButton
            aria-label="remove"
            onClick={() => removeItem(r.id)}
            size="small"
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Stack>
      ),
    },
  ];

  return (
    <PageContainer>
      <Typography variant="h4" component="h1" gutterBottom>
        Upload
      </Typography>
      <Stack spacing={2}>
        <FileDropzone onFilesSelected={addFiles} />
        <DataTable columns={columns} rows={items} getRowId={(r) => r.id} />
        {items.map(
          (i) =>
            i.status === "idle" && (
              <Button
                key={i.id}
                variant="contained"
                onClick={() => startUpload(i.id)}
              >
                Upload {i.file.name}
              </Button>
            )
        )}
      </Stack>
    </PageContainer>
  );
};

export default UploadPage;
