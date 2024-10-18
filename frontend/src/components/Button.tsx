import React from 'react';

interface ButtonProps {
  type: 'button' | 'submit' | 'reset';
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ type, onClick, children }) => {
  return (
    <button type={type} onClick={onClick} className="button">
      {children}
    </button>
  );
};

export default Button;