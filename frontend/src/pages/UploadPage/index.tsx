import React from "react";
import PageContainer from "@shared/components/PageContainer";
import Typography from "@shared/components/Typography";
import Stack from "@shared/components/Stack";
import Button from "@shared/components/Button";
import DataTable from "@shared/components/DataTable";
import FileDropzone from "@shared/components/FileDropzone";
import { getColumns } from "./components/getColumns";
import { useUploadPage } from "./state/useUploadPage";

const UploadPage: React.FC = () => {
  const { items, addFiles, startUpload, abortUpload, retryUpload, removeItem } =
    useUploadPage();

  const columns = getColumns<(typeof items)[number]>({
    abortUpload,
    retryUpload,
    removeItem,
  });

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
