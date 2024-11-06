import React from 'react';
import Logo from '../assets/images/LOGO_PAPILON HORIZONTAL BLANCO.png'
import Button from '../components/button';
import  '../assets/styles/home.css';
const Home: React.FC = () => {
  return (
    <div className="container">
      <img src={Logo} alt='logo' className="logo-home"/>
      <div className='description'>
      <h2>Un sistema de recompensas que permite a sus usuarios acumular puntos por cada compra realizada, para luego canjearlos por productos o servicios.</h2>
      </div>
      <Button type="button">Registrarse</Button>
    </div>
  );
};

export default Home;
