import React, { useState } from 'react';
import InputField from '../components/inputField';
import Button from '../components/button';
import SocialButton from '../components/socialButton';
import Logo from '../assets/images/LOGO_PAPILON VERTICAL.png';
import { Link, useNavigate } from 'react-router-dom';
import { login } from '../services/authService';
import '../assets/styles/login.css';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null); // Estado para manejar errores
  const [successMessage, setSuccessMessage] = useState<string | null>(null); // Estado para el mensaje de éxito
  const navigate = useNavigate(); // Para redirigir al usuario después del login

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null); // Reinicia el estado de error
    setSuccessMessage(null); // Reinicia el mensaje de éxito

    try {
      const { token, message } = await login(username, password); // Llama al servicio de login
      localStorage.setItem('token', token); // Guarda el token en localStorage
      setSuccessMessage(message); // Muestra el mensaje de éxito
      console.log('Inicio de sesión exitoso');
      
      // Redirige al usuario después de 2 segundos para mostrar el mensaje
      setTimeout(() => {
        navigate('/');
      }, 2000);
    } catch (err) {
      console.error('Error al iniciar sesión:', err);
      setError('Usuario o contraseña incorrectos.');
    }
  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    console.log(`${provider} login clicked`);
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <img src={Logo} alt="Logo" className="login-logo" />
      <SocialButton provider="google" onClick={() => handleSocialLogin('google')} />
      <SocialButton provider="facebook" onClick={() => handleSocialLogin('facebook')} />
      <div className="separator">OR</div>
      <InputField
        label="Usuario"
        type="text"
        id="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <InputField
        label="Contraseña"
        type="password"
        id="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {/* Muestra el error si ocurre */}
      {error && <p className="error-message">{error}</p>}
      {/* Muestra el mensaje de éxito */}
      {successMessage && <p className="success-message">{successMessage}</p>}
      <Link to="/" className="forgot-password">Olvidé mi contraseña</Link>
      <Button type="submit">Iniciar Sesión</Button>
      <Link to="/register" className="forgot-password">¿Ya estás registrado?</Link>
    </form>
  );
};

export default Login;

