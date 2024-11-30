import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
    const { token } = useAuth();

    if (!token) {
        // Si no está autenticado, redirije al login
        return <Navigate to="/login" />;
    }

    return <>{children}</>; // Montar el componente protegido
};

export default ProtectedRoute;