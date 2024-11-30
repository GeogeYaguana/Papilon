import React, { useState, useEffect } from 'react';
import InputField from '../components/inputField';
import Button from '../components/button';
import SocialButton from '../components/socialButton';
import Logo from '../assets/images/LOGO_PAPILON VERTICAL.png';
import { Link } from 'react-router-dom';
import '../assets/styles/register.css';

const Register: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [location, setLocation] = useState('');
  const [category, setCategory] = useState('');
  const [ruc, setRuc] = useState('');
  const [passwordError, setPasswordError] = useState('');

  // Cargar datos desde localStorage cuando se monta el componente
  useEffect(() => {
    const savedUsername = localStorage.getItem('username');
    const savedRuc = localStorage.getItem('ruc');
    const savedLocation = localStorage.getItem('location');
    const savedCategory = localStorage.getItem('category');

    if (savedUsername) setUsername(savedUsername);
    if (savedRuc) setRuc(savedRuc);
    if (savedLocation) setLocation(savedLocation);
    if (savedCategory) setCategory(savedCategory);
  }, []);

  // Guardar datos en localStorage siempre que cambie la entrada
  useEffect(() => {
    localStorage.setItem('username', username);
    localStorage.setItem('ruc', ruc);
    localStorage.setItem('location', location);
    localStorage.setItem('category', category);
  }, [username, ruc, location, category]);

  // Función para manejar la validación
  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const confirmPasswordValue = e.target.value;
    setConfirmPassword(confirmPasswordValue);

    // Compara las contraseñas
    if (confirmPasswordValue !== password) {
      setPasswordError('Las contraseñas no coinciden');
    } else {
      setPasswordError('');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Si hay un error, no enviamos el formulario
    if (password !== confirmPassword) {
      setPasswordError('Las contraseñas no coinciden');
      return;
    }

    // validacion registramos al usuario
    setPasswordError('');
    console.log('Register submitted', { username, password, location, category, ruc });

    // Limpiar el almacenamiento local después de un registro exitoso
    localStorage.removeItem('username');
    localStorage.removeItem('ruc');
    localStorage.removeItem('location');
    localStorage.removeItem('category');

    // Redireccionar a Login

  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    console.log(`${provider} login clicked`);
  };

  return (
    <form onSubmit={handleSubmit} className="register-form">
      <img src={Logo} alt="Logo" className="register-logo" />
      
      {/* Botones de login social */}
      <SocialButton provider="google" onClick={() => handleSocialLogin('google')} />
      <SocialButton provider="facebook" onClick={() => handleSocialLogin('facebook')} />
      
      <div className="separator">OR</div>

      <div className='inputs-container'>
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
      <div className='inputs-container'>
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
      
      <div className='inputs-container'>
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
      
      <Button type="submit">Registrar</Button>
      <Link to="/login" className='forgot-password'>¿Ya estas registrado?</Link>
    </form>
  );
};

export default Register;
