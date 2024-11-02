import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: { preventDefault: () => void; }) => {
    e.preventDefault();

    // Implement your forgot password logic here, e.g., sending a reset email
    // ...

    try {
      // Simulate successful password reset
      console.log('Password reset email sent to:', email);
      navigate('/login'); // Redirect to login page
    } catch (error) {
      setErrorMessage('Error sending reset email. Please try again.');
    }
  };

  return (
    <div>
      <h2>Forgot Password</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Reset Password</button>
        {errorMessage && <p>{errorMessage}</p>}
      </form>
    </div>
  );
};

export default ForgotPassword;