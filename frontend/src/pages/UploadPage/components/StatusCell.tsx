import React from "react";
import Chip from "@mui/material/Chip";
import CircularProgress from "@mui/material/CircularProgress";
import type { UploadStatus } from "../model/UploadStatus";

type ChipColor =
  | "default"
  | "primary"
  | "secondary"
  | "error"
  | "info"
  | "success"
  | "warning";

const statusToLabel: Record<UploadStatus, string> = {
  idle: "Idle",
  uploading: "Uploading",
  processing: "Processing",
  processed: "Processed",
  error: "Error",
  aborted: "Aborted",
};

const statusToColor: Record<UploadStatus, ChipColor> = {
  idle: "default",
  uploading: "info",
  processing: "warning",
  processed: "success",
  error: "error",
  aborted: "warning",
};

export const StatusCell: React.FC<{ status: UploadStatus }> = ({ status }) => {
  const label = statusToLabel[status];
  const color = statusToColor[status];
  const isLoading = status === "uploading" || status === "processing";

  return (
    <Chip
      size="small"
      color={color}
      variant={color === "default" ? "outlined" : "filled"}
      icon={isLoading ? <CircularProgress size={14} /> : undefined}
      label={label}
    />
  );
};

export default StatusCell;
