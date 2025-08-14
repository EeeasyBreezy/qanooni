import React from 'react';
import MuiLinearProgress, { LinearProgressProps as MuiLinearProgressProps } from '@mui/material/LinearProgress';

export type LinearProgressProps = MuiLinearProgressProps;

const LinearProgress: React.FC<LinearProgressProps> = (props) => {
  return <MuiLinearProgress {...props} />;
};

export default LinearProgress;


