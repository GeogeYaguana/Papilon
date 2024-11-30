import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../layouts/mainLayout';
import Home from '../pages/home';
import Login from '../pages/login';
import Register from '../pages/register';
import ProtectedRoute from '../components/protectedRoute';

const routes = [
  {
    path: "/login",
    element: (
      <MainLayout showSearch={false} showTitle={false} showMenu={false} showButton={false} title="Login">
        <Login />
      </MainLayout>
    ),
  },
  {
    path: "",
    element: (
      <MainLayout showSearch={false} showTitle={false} showMenu={false} title="Inicio">
        <Home />
      </MainLayout>
    ),
  },
  {
    path: "/register",
    element: (
      <MainLayout showSearch={false} showTitle={false} showButton={false} showMenu={false} title="Register">
        <Register />
      </MainLayout>
    ),
  },
  {
    path: "/protected", // Ejemplo de ruta protegida
    element: (
      <ProtectedRoute>
        <MainLayout showSearch={false} showTitle={false} showMenu={false} title="Ejemplo">
          {/* Your protected component here */}
          <h1>Protegido</h1>
        </MainLayout>
      </ProtectedRoute>
    ),
  },
  {
    path: "/dashboard",
    element: (
      <ProtectedRoute>
        <MainLayout showSearch={false} showTitle={false} showMenu={false} title="Dashboard">
          {/* Your protected component here */}
        </MainLayout>
      </ProtectedRoute>
    ),
  },
];

const router = createBrowserRouter(routes);

export default router;
