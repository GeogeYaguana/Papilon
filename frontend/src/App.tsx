import React from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './routes/routes';
import { AuthProvider } from './context/AuthContext';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
};

export default App;
