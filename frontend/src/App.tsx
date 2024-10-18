/*import React from 'react';
import logo from './logo.svg';
import './App.css';

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
import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Registration from './screens/Register/Registration'; // Import your registration component

const LoginApp: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loggedIn, setLoggedIn] = useState(false);

    const handleLogin = () => {
        if (username === 'user' && password === 'password') {
            setLoggedIn(true);
            alert('Login successful!');
        } else {
            alert('Invalid credentials. Please try again.');
        }
    };

    const handleLogout = () => {
        setLoggedIn(false);
        setUsername('');
        setPassword('');
    };

    const handleForgotPassword = () => {
        alert('Forgot Password link clicked! Redirect to password recovery page.');
    };

    const handleRegister = () => {
      return (
        <Router>
          <Routes>
            <Route path="/register" element={<Registration />} />
          </Routes>
        </Router>
      );
    };

    if (loggedIn) {
        return (
            <div className="App">
                <p>Welcome, {username}!</p>
                <button className="button" onClick={handleLogout}>Logout</button>
            </div>
        );
    } else {
        return (
            <div className="App">
              <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
              </header>
                <h2 className="title">Login</h2>
                <input
                    type="text"
                    className="input"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    className="input"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <div className="Buttons">
                  <button className="button" onClick={handleLogin}>Ingresar</button>
                  <button className="button register" onClick={handleRegister}>Registrarse</button>
                </div>
                <a href="#" className="forgot-password" onClick={handleForgotPassword}>
                    Olvidé mi contraseña
                </a>
            </div>
        );
    }
};

export default LoginApp;