import React from 'react';
import Container from '@mui/material/Container';
import Alert from './Alert';
import Loader from './Loader';

type PageContainerProps = {
  children: React.ReactNode;
  isLoading?: boolean;
  error?: string | null;
};

const PageContainer: React.FC<PageContainerProps> = ({ children, isLoading, error }) => {
  return (
    <Container maxWidth="md">
      {isLoading ? (
        <Loader size={32} />
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        children
      )}
    </Container>
  );
};

export default PageContainer;


