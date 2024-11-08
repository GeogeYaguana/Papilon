import React from 'react';

interface SocialButtonProps {
  provider: 'google' | 'facebook';
  onClick: () => void;
}

const SocialButton: React.FC<SocialButtonProps> = ({ provider, onClick }) => {
  return (
    <button className={`social-button ${provider}`} onClick={onClick}>
      {provider === 'google' ? 'Login with Google' : 'Login with Facebook'}
    </button>
  );
};

export default SocialButton;
