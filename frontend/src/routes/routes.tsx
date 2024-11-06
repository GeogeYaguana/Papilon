import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../layouts/mainLayout';
import Home from '../pages/home';
import Login from '../pages/login';

const routes = [
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/home",
    element: (
      <MainLayout showSearch={false} showTitle={false} showMenu={false} title="Inicio">
        <Home /> {/* Pasa Home como children de MainLayout */}
      </MainLayout>
    ),
  },
  {
    path: "/profile",
    element: (
      <MainLayout showSearch={false} showTitle={true} title="Perfil">
        {/* Otro componente puede ir aquí como children */}
      </MainLayout>
    ),
  },
];

const router = createBrowserRouter(routes);

export default router;
