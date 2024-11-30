import React from 'react';
import { RouterProvider } from 'react-router-dom';
import router from './routes/routes';
import { AuthProvider } from './context/AuthContext';
import { GlobalProvider } from './context/GlobalContext';
import { ApiProvider } from './context/ApiContext';


const App: React.FC = () => {
  return (
    <AuthProvider>
      <GlobalProvider>
        <ApiProvider>
          <RouterProvider router={router} />
        </ApiProvider>
      </GlobalProvider>
    </AuthProvider>
  );
};

export default App;
