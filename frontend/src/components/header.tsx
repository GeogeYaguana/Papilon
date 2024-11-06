import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/images/LOGO_PAPILON HORIZONTAL.png';

import '../assets/styles/header.css';

interface HeaderProps {
  showSearch?: boolean;
  showTitle?: boolean;
  title?: string;
  showMenu?: boolean;
}

const Header: React.FC<HeaderProps> = ({ showSearch = false, showTitle = false, title = "My Website", showMenu = true }) => {
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
        {showMenu && (
          <button className="menu-toggle" onClick={toggleMenu}>
            ☰
          </button>
        )}

        {isMenuOpen && (
          <nav className="dropdown-menu">
            <Link to="/">Home</Link>
            <Link to="/profile">Profile</Link>
            <Link to="/settings">Settings</Link>
            {/* Puedes agregar más enlaces aquí */}
          </nav>
        )}

        {showTitle && <h1 className="title">{title}</h1>}
      </div>

      <div className="header-right">
      {showSearch && (
        <div className="search-container">
          <input type="text" placeholder="Buscar..." className="search-input" />
        </div>
      )}
        <div className='btn-container'>
        <Link to="/login" className="btn">Ingresar</Link>
        <Link to="/register" className="btn">Registrarse</Link>
        </div>
        
      </div>
    </header>
  );
};

export default Header;
