import React from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
/*import { RouterProvider, createBrowserRouter } from 'react-router-dom';
import Registration from './screens/Register/Registration'; // Componente de registro
import ForgotPassword from './screens/Register/ForgotPassword'; // Componente de contraseña olvidada


const router = createBrowserRouter([
  {
    path: '/register',
    element: <Registration />,
  },
  {
    path: '/forgot-password',
    element: <ForgotPassword />,
  },
  // Puedes agregar más rutas aquí
]);

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
    
  );
}

export default App;
*/

import LoginApp from './screens/Login/LoginScreen';
import Registration from './screens/Register/Registration';
import ForgotPassword from './screens/Register/ForgotPassword';
import NotFound from './screens/NotFound/NotFound';

const App = () => {
  return (
    <Router>
      <div>
        <h1>Mi Aplicación React</h1>
        <Routes>
          <Route path="/" element={<LoginApp />} />
          <Route path="/registration" element={<Registration />} />
          <Route path="/forgotpassword" element={<ForgotPassword />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
};
