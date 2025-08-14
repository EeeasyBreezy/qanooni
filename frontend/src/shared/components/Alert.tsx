import React from 'react';
import MuiAlert, { AlertProps as MuiAlertProps } from '@mui/material/Alert';

export type AlertProps = MuiAlertProps;

const Alert: React.FC<AlertProps> = (props) => {
  return <MuiAlert {...props} />;
};

export default Alert;


