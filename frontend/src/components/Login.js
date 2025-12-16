/**
 * Login Component
 * Handles student and teacher authentication with role selection
 */
import React, { useState } from 'react';
import { studentAPI, authAPI } from '../services/api';
import './Login.css';

function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('student'); // 'student' or 'teacher'
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let response;
      if (role === 'student') {
        // Call student login API (auth endpoint with JWT token)
        response = await authAPI.studentLogin(email, password);
      } else {
        // Call teacher login API (auth endpoint with JWT token)
        response = await authAPI.teacherLogin(email, password);
      }
      // Store token and user data for both roles
      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      onLogin(response.user);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>ILPG</h1>
        <h2>Intelligent Learning Path Generator</h2>
        <p className="subtitle">Sign in to continue your journey</p>

        {/* Role Selection */}
        <div className="role-selection">
          <button
            type="button"
            className={`role-btn ${role === 'student' ? 'active' : ''}`}
            onClick={() => setRole('student')}
          >
            Student
          </button>
          <button
            type="button"
            className={`role-btn ${role === 'teacher' ? 'active' : ''}`}
            onClick={() => setRole('teacher')}
          >
            Teacher
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              placeholder="Enter your email"
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              placeholder="Enter your password"
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="demo-credentials">
          <p><strong>Demo Credentials:</strong></p>
          {role === 'student' ? (
            <>
              <p>Student Email: john@example.com | Password: password123</p>
              <p>Student Email: jane@example.com | Password: password123</p>
            </>
          ) : (
            <>
              <p>Teacher Email: sarah@teacher.com | Password: teacher123</p>
              <p>Teacher Email: michael@teacher.com | Password: teacher123</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;








