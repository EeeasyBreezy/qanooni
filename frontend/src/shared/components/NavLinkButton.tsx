import React from 'react';
import Button, { ButtonProps } from '@mui/material/Button';
import { NavLink, NavLinkProps } from 'react-router-dom';

type NavLinkButtonProps = {
  to: NavLinkProps['to'];
  children: React.ReactNode;
} & Omit<ButtonProps, 'component' | 'to'>;

const NavLinkButton: React.FC<NavLinkButtonProps> = ({ to, children, ...btnProps }) => {
  return (
    <Button
      {...btnProps}
      color="inherit"
      component={NavLink as unknown as React.ElementType}
      to={to as any}
      sx={{ textTransform: 'none' }}
    >
      {children}
    </Button>
  );
};

export default NavLinkButton;


