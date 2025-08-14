import React from 'react'
import { BrowserRouter, NavLink, Route, Routes } from 'react-router-dom'
import UploadPage from './pages/UploadPage'
import DashboardPage from './pages/DashboardPage'
import SearchPage from './pages/SearchPage'

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif', padding: '1rem' }}>
        <nav style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
          <NavLink to="/upload">Upload</NavLink>
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/search">Search</NavLink>
        </nav>
        <Routes>
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="*" element={<UploadPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}


