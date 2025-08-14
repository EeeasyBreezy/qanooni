import React from 'react';
import MuiIconButton, { IconButtonProps as MuiIconButtonProps } from '@mui/material/IconButton';

export type IconButtonProps = MuiIconButtonProps;

const IconButton: React.FC<IconButtonProps> = (props) => {
  return <MuiIconButton {...props} />;
};

export default IconButton;


