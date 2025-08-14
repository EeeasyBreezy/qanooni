import React from 'react';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';

type LoaderProps = {
  size?: number;
  inline?: boolean;
};

const Loader: React.FC<LoaderProps> = ({ size = 24, inline = false }) => {
  const content = <CircularProgress size={size} />;
  if (inline) return content;
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', py: 4 }}>
      {content}
    </Box>
  );
};

export default Loader;


