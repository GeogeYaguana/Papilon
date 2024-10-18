import React from 'react';
import LoginForm from '../../components/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <div className="login-page">
      <div className="login-modal">
        <img src="/path-to-your-logo.png" alt="Papion Logo" className="logo" />
        <h1>Iniciar Sesión</h1>
        <p>¿Tienes una cuenta? Regístrate</p>
        <LoginForm />
      </div>
    </div>
  );
};

export default LoginPage;