import { useState } from 'react'
import Button from '../Button'
import InputField from '../InputField'
import SocialButton from '../SocialButton'
import { loginService } from '../../services/AuthServices'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    loginService(email, password)
  }

  return (
    <div className="loginContainer">
      <form onSubmit={handleLogin}>
        <InputField
          type="email"
          placeholder="Usuario o identificación"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <InputField
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <Button text="Iniciar Sesión" type="submit" />
      </form>

      <div className="socialLogin">
        <p>O continúa con</p>
        <SocialButton provider="Google" />
        <SocialButton provider="Facebook" />
      </div>
    </div>
  )
}

export {}
