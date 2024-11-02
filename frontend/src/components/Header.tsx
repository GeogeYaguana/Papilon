import React, { useState } from 'react';
import './Header.css'; // Import the CSS file for styling
import papilon from "../recursos/Images/LOGO_PAPILON_VERTICAL.png"

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (event: { target: { value: React.SetStateAction<string>; }; }) => {
    setSearchQuery(event.target.value);
    // Add your search logic here
  };

  return (
    <header className="header">
      <div className="logo-container">
        <img src={papilon} alt="Your Logo" className="logo" />
      </div>
      <div className="content-container">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
          <div className="searchbar">
          <input type="text"
          name="search"
          placeholder="Buscar..."
          value={searchQuery}
          onChange={handleSearch}/>
          <span className="searchbar-icon"><i className="fas fa-search"></i></span>
          </div>
        
        <div className="language-selector">
          <select className='selector'>
            <option value="es">Español (América Latina)</option>
            <option value="en">English</option>
            {/* Add more language options as needed */}
          </select>
        </div>
        <div className="auth-buttons">
          <button className="login-button">Iniciar Sesión</button>
          <button className="register-button">Registro</button>
        </div>
      </div>
      
    </header>
  );
};

export default Header;