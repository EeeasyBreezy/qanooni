import React from 'react';
import Container from '@mui/material/Container';

type PageContainerProps = {
  children: React.ReactNode;
};

const PageContainer: React.FC<PageContainerProps> = ({ children }) => {
  return <Container maxWidth="md">{children}</Container>;
};

export default PageContainer;


