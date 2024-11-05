// src/App.tsx
import React, { useState } from 'react';
import LoginPage from './pages/login/LoginPage';
import './pages/login/StylesLogin.modules.css';
import Sidenav from './components/Sidenav';
import Navbar from './components/Navbar';
import { Routes, Route, BrowserRouter } from "react-router-dom";
import Dashboard from './pages/login/DashboardMain';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Hook para manejar el estado de autenticación
  const user = { name: 'John Doe' }; // Puedes reemplazar esto con la lógica real de autenticación

  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta para la página de inicio de sesión 
                <Route path='/' element={<LoginPage />} />
        */}

        {/* Ruta para la Sidenav, que recibe props */}
        <Route path='/' element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}



