import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Box from "@mui/material/Box";
import NavLinkButton from "@shared/components/NavLinkButton";
import UploadPage from "./pages/UploadPage";
import DashboardPage from "./pages/DashboardPage";
import QueryPage from "./pages/QueryPage";

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Box
        sx={{
          fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif",
        }}
      >
        <AppBar position="static" color="transparent" elevation={0}>
          <Toolbar>
            <Box sx={{ display: "flex", gap: 2 }}>
              <NavLinkButton to="/upload">Upload</NavLinkButton>
              <NavLinkButton to="/dashboard">Dashboard</NavLinkButton>
              <NavLinkButton to="/search">Search</NavLinkButton>
            </Box>
          </Toolbar>
        </AppBar>
        <Routes>
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/search" element={<QueryPage />} />
          <Route path="*" element={<UploadPage />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
};
