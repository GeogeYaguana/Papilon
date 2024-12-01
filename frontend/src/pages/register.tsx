import React, { useState } from 'react';
import InputField from '../components/inputField';
import Button from '../components/button';
import SocialButton from '../components/socialButton';
import Logo from '../assets/images/LOGO_PAPILON VERTICAL.png';
import { Link,useNavigate } from 'react-router-dom';
import { register } from '../services/registerService';
import '../assets/styles/register.css';

const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [location, setLocation] = useState('');
  const [category, setCategory] = useState('');
  const [ruc, setRuc] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const navigate = useNavigate();
  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const confirmPasswordValue = e.target.value;
    setConfirmPassword(confirmPasswordValue);

    if (confirmPasswordValue !== password) {
      setPasswordError('Las contraseñas no coinciden');
    } else {
      setPasswordError('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setPasswordError('Las contraseñas no coinciden');
      return;
    }

    setPasswordError('');
    setError(null);
    setSuccessMessage(null);

    try {
      const response = await register({
        nombre: username,
        usuario_nombre: username,
        password,
        correo: `${username}@example.com`,
        tipo_usuario: category || 'local', 
        url_imagen: '',
        telefono: location, 
      });
      setSuccessMessage(response.message);
      console.log('Registro exitoso:', response.message);
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (error: unknown) {
      const err = error as Error; 
      setError(err.message || 'Error desconocido al registrar el usuario.');
      console.error('Error al registrar:', err);
    }
  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    console.log(`${provider} login clicked`);
  };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <img src={Logo} alt="Logo" className="register-logo" />
      <SocialButton provider="google" onClick={() => handleSocialLogin('google')} />
      <SocialButton provider="facebook" onClick={() => handleSocialLogin('facebook')} />
      <div className="separator">OR</div>
      <div className="inputs-container">
        <InputField
          label="Correo electronico"
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <InputField
          label="RUC"
          type="text"
          id="ruc"
          value={ruc}
          onChange={(e) => setRuc(e.target.value)}
        />
      </div>
      <div className="inputs-container">
        <InputField
          label="Contraseña"
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <InputField
          label="Confirmar Contraseña"
          type="password"
          id="confirmPassword"
          value={confirmPassword}
          onChange={handleConfirmPasswordChange}
        />
      </div>
      <div className="inputs-container">
        <InputField
          label="Ubicación"
          type="text"
          id="location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
        <InputField
          label="Categoría"
          type="text"
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
      </div>
      {passwordError && <p className="error">{passwordError}</p>}
      {error && <p className="error">{error}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}
      <Button type="submit">Registrar</Button>
      <Link to="/login" className="forgot-password">¿Ya estás registrado?</Link>
    </form>
  );
};

export default Register;
