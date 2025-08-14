import React from 'react';
import PageContainer from '@shared/components/PageContainer';
import Typography from '@mui/material/Typography';

const DashboardPage: React.FC = () => {
  return (
    <PageContainer>
      <Typography variant="h4" component="h1" gutterBottom>
        Dashboard
      </Typography>
    </PageContainer>
  );
};

export default DashboardPage;


