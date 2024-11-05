
import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../layouts/mainLayout';
import Home from '../pages/home';

import Login from '../pages/login';

const routes = [
  {
    path: "",
    element: <Login />,
  },
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        path: "/home",
        element: <Home />,
      },
      
    ],
  },
];

const router = createBrowserRouter(routes);

export default router;
