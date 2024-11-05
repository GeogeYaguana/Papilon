import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';
import { Outlet } from 'react-router-dom';

const MainLayout: React.FC = () => {
  return (
    <div>
      <Header />
      <main>
        <Outlet /> {/* Renderiza el componente de la ruta activa */}
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;
