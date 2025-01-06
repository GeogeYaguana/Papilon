import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/images/LOGO_PAPILON HORIZONTAL.png';

import '../assets/styles/header.css';

interface HeaderProps {
  showSearch?: boolean;
  showTitle?: boolean;
  title?: string;
  showMenu?: boolean;
  showButton?: boolean;
}

const Header: React.FC<HeaderProps> = ({ showSearch = false, showTitle = false, title = "My Website", showMenu = true, showButton = true }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="header">
      <div className="header-left">
        <Link to="" className="logo">
        <img src={Logo} alt='Logo' className="logo"/>
        </Link>
      </div>
    </header>
  );
};

export default Header;
