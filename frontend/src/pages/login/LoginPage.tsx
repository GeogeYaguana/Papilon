import React from 'react';
import LoginForm from '../../components/LoginForm';
import papilon from "../../recursos/Images/LOGO_PAPILON_VERTICAL.png"
import Header from '../../components/Header'

const LoginPage: React.FC = () => {
  return (
    <div className="login-page">
      <div>
        <Header /> 
      </div>
      
      <div className="login-modal">
        <img src={papilon} alt="Papilon Logo" className="logo" />
        <h1>Iniciar Sesión</h1>
        <p>¿Tienes una cuenta? Regístrate</p>
        <LoginForm />
      </div>
    </div>
  );
};

export default LoginPage;