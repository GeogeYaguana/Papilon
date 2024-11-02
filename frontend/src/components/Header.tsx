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
      <img src={papilon} alt="Your Logo" className="logo" />
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />
        <div className="searchbar">
        <input type="text"
        name="search"
        placeholder="Search..."
        value={searchQuery}
        onChange={handleSearch}/>
        <span className="searchbar-icon"><i className="fas fa-search"></i></span>
        </div>

      
      <div className="language-selector">
        <select>
          <option value="es">Español (América Latina)</option>
          <option value="en">English</option>
          {/* Add more language options as needed */}
        </select>
      </div>
      <div className="auth-buttons">
        <button className="login-button">Log In</button>
        <button className="register-button">Register</button>
      </div>
    </header>
  );
};

export default Header;