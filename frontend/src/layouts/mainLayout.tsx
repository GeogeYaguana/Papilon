import React, { ReactNode } from 'react';
import Header from '../components/header';
import Footer from '../components/footer';

interface MainLayoutProps {
  showSearch?: boolean;
  showTitle?: boolean;
  title?: string;
  showMenu?: boolean;
  children?: ReactNode;  // Hacer children opcional
}

const MainLayout: React.FC<MainLayoutProps> = ({ 
  showSearch = false, 
  showTitle = true, 
  title = "My Website", 
  showMenu = true, 
  children 
}) => {
  return (
    <div>
      <Header showSearch={showSearch} showTitle={showTitle} title={title} showMenu={showMenu} />
      <main>
        {children} {/* Renderiza el componente hijo si está presente */}
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;

