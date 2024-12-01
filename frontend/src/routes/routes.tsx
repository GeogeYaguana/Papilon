import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../layouts/mainLayout';
import Home from '../pages/home';
import Login from '../pages/login';
import Register from '../pages/register';
import Dashboard from '../pages/dashboard';
const routes = [
  {
    path: "/login",
    element: (
      <MainLayout showSearch={false} showTitle={false} showMenu={false} showButton={false} title="Login" >
        <Login />
      </MainLayout>
    ),
  },
  {
    path: "",
    element: (
      <MainLayout showSearch={false} showTitle={false} showMenu={false}  title="Inicio">
        <Home />
      </MainLayout>
    ),
  },
  {
    path: "/register",
    element: (
      <MainLayout showSearch={false} showTitle={false} showButton={false} showMenu={false} title="register">
        <Register/>
      </MainLayout>
    ),
  },
  {
    path: "/dashboard",
    element: (
      <MainLayout showSearch={true} showTitle={true} showButton={true} showMenu={true} title="dashboard">
        <Dashboard/>
      </MainLayout>
    ),
  },
];

const router = createBrowserRouter(routes);

export default router;
