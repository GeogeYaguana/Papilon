import { FaGoogle, FaFacebook } from 'react-icons/fa'

interface SocialButtonProps {
  provider: 'Google' | 'Facebook'
}

export default function SocialButton({ provider }: SocialButtonProps) {
  const handleSocialLogin = () => {
    console.log(`Iniciar sesión con ${provider}`)
    // Agregar lógica de autenticación social
  }

  return (
    <button onClick={handleSocialLogin} className="socialButtonStyle">
      {provider === 'Google' && <FaGoogle className="iconStyle" />}
      {provider === 'Facebook' && <FaFacebook className="iconStyle" />}
      {provider}
    </button>
  )
}

export {} 
