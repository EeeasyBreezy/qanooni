import React from "react";
import Stack from "@shared/components/Stack";
import IconButton from "@shared/components/IconButton";
import DeleteIcon from "@mui/icons-material/Delete";
import ReplayIcon from "@mui/icons-material/Replay";
import StopIcon from "@mui/icons-material/Stop";
import type { UploadStatus } from "../model/UploadStatus";

type Props = {
  status: UploadStatus;
  onAbort: () => void;
  onRetry: () => void;
  onRemove: () => void;
};

const FileActions: React.FC<Props> = ({
  status,
  onAbort,
  onRetry,
  onRemove,
}) => {
  return (
    <Stack direction="row" spacing={1} alignItems="center">
      {status === "uploading" && (
        <IconButton aria-label="abort" onClick={onAbort} size="small">
          <StopIcon fontSize="small" />
        </IconButton>
      )}
      {(status === "error" || status === "aborted") && (
        <IconButton aria-label="retry" onClick={onRetry} size="small">
          <ReplayIcon fontSize="small" />
        </IconButton>
      )}
      <IconButton aria-label="remove" onClick={onRemove} size="small">
        <DeleteIcon fontSize="small" />
      </IconButton>
    </Stack>
  );
};

export default FileActions;
