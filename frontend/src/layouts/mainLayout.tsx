import React, { ReactNode } from 'react';
import Header from '../components/header';
import Footer from '../components/footer';
import '../assets/styles/mainLayout.css'
interface MainLayoutProps {
  showSearch?: boolean;
  showTitle?: boolean;
  title?: string;
  showMenu?: boolean;
  showButton?:boolean;
  children?: ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ 
  showSearch = false, 
  showTitle = true, 
  title = "My Website", 
  showMenu = true,
  showButton= true, 
  children 
}) => {
  return (
    <div>
      <Header showSearch={showSearch} showTitle={showTitle} title={title} showMenu={showMenu} showButton={showButton}/>
      <main>
        {children} 
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;

