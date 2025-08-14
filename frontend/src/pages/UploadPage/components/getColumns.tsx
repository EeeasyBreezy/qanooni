import type { Column } from "@shared/components/DataTable";
import LinearProgress from "@shared/components/LinearProgress";
import FileActions from "./FileActions";
import type { UploadStatus } from "../model/UploadStatus";

export type UploadRowShape = {
  id: string;
  file: File;
  status: UploadStatus;
  progress: number;
};

export const getColumns = <T extends UploadRowShape>(handlers: {
  abortUpload: (id: string) => void;
  retryUpload: (id: string) => void;
  removeItem: (id: string) => void;
}): Column<T>[] => [
  { key: "name", header: "File", render: (r) => r.file.name },
  { key: "status", header: "Status", render: (r) => r.status },
  {
    key: "progress",
    header: "Progress",
    render: (r) => <LinearProgress variant="determinate" value={r.progress} />,
  },
  {
    key: "actions",
    header: "Actions",
    render: (r) => (
      <FileActions
        status={r.status}
        onAbort={() => handlers.abortUpload(r.id)}
        onRetry={() => handlers.retryUpload(r.id)}
        onRemove={() => handlers.removeItem(r.id)}
      />
    ),
  },
];
