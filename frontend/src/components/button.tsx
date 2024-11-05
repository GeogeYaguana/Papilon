import React from 'react';

interface ButtonProps {
  type: 'submit' | 'button';
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ type, children }) => {
  return (
    <button type={type} className="button">
      {children}
    </button>
  );
};

export default Button;
