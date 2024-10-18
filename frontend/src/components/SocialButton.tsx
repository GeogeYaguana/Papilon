import React from 'react';

interface SocialButtonProps {
  provider: 'google' | 'facebook';
  onClick: () => void;
}

const SocialButton: React.FC<SocialButtonProps> = ({ provider, onClick }) => {
  const text = provider === 'google' ? 'Continuar con Google' : 'Continuar con Facebook';
  const className = `social-button ${provider}`;

  return (
    <button className={className} onClick={onClick}>
      {text}
    </button>
  );
};

export default SocialButton;