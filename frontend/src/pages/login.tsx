import React, { useState } from 'react';
import InputField from '../components/inputField';
import Button from '../components/button';
import SocialButton from '../components/socialButton';
import Logo from '../assets/images/LOGO_PAPILON VERTICAL.png'
import '../assets/styles/login.css';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    //lógica del login
    console.log('Login submitted', { username, password });
  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    //login social
    console.log(`${provider} login clicked`);
  };
  
  return (
    <form onSubmit={handleSubmit} className="login-form">
      <img src={Logo} alt="Logo" className="login-logo"/>
      <SocialButton provider="google" onClick={() => handleSocialLogin('google')} />
      <SocialButton provider="facebook" onClick={() => handleSocialLogin('facebook')} />
      <div className="separator">OR</div>
      <InputField
        label="Usuario o identificación"
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
      <a href="#" className="forgot-password">Olvidé mi contraseña</a>
      <Button type="submit">Iniciar Sesión</Button>
    </form>
  );
};

export default Login;
