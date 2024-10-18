import React, { useState } from 'react';
import InputField from './InputField';
import Button from './Button';
import SocialButton from './SocialButton';

const LoginForm: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle login logic here
    console.log('Login submitted', { username, password });
  };

  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    // Handle social login logic here
    console.log(`${provider} login clicked`);
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
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

export default LoginForm;
