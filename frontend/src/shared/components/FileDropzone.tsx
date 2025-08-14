import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@shared/components/Typography';
import { FileExtensions } from '@shared/consts/FileExtensions';

type FileDropzoneProps = {
  onFilesSelected: (files: FileList | null) => void;
  accept?: string;
};

const FileDropzone: React.FC<FileDropzoneProps> = ({ onFilesSelected, accept = `${FileExtensions.pdf},${FileExtensions.docx}` }) => {
  const inputRef = React.useRef<HTMLInputElement | null>(null);
  const [dragOver, setDragOver] = React.useState(false);

  const openDialog = () => inputRef.current?.click();

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    onFilesSelected(e.dataTransfer.files);
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple={true}
        hidden
        onChange={(e) => onFilesSelected(e.target.files)}
      />
      <Box
        onClick={openDialog}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        sx={{
          border: '2px dashed',
          borderColor: dragOver ? 'primary.main' : 'divider',
          borderRadius: 2,
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          bgcolor: dragOver ? 'action.hover' : 'transparent',
        }}
      >
        <Typography variant="h6">Drag and drop PDF/DOCX files here, or click to select</Typography>
      </Box>
    </>
  );
};

export default FileDropzone;


