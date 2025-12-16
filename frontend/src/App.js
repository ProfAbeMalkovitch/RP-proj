/**
 * Main App Component
 * Handles routing and authentication state for students and teachers
 */
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import AdminLogin from './components/auth/AdminLogin';
import Dashboard from './components/Dashboard';
import StudentDashboard from './components/dashboards/StudentDashboard';
import TaskDetail from './components/dashboards/TaskDetail';
import TeacherDashboard from './components/TeacherDashboard';
import AdminDashboard from './components/AdminDashboard';
import PathwayDetail from './components/PathwayDetail';
import './App.css';

function App() {
  // State to track if user is logged in
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [userRole, setUserRole] = useState(null); // 'student' or 'teacher'

  // Check if user is already logged in (from localStorage)
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setUserRole(userData.role || 'student');
      setIsAuthenticated(true);
    }
  }, []);

  // Handle login
  const handleLogin = (userData) => {
    setUser(userData);
    setUserRole(userData.role || 'student');
    setIsAuthenticated(true);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  // Handle logout
  const handleLogout = () => {
    setUser(null);
    setUserRole(null);
    setIsAuthenticated(false);
    localStorage.removeItem('user');
  };

  // Determine redirect path based on user role
  const getRedirectPath = () => {
    if (!isAuthenticated) return '/login';
    if (userRole === 'admin') return '/admin/dashboard';
    if (userRole === 'teacher') return '/teacher/dashboard';
    return '/dashboard';
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/login"
            element={
              isAuthenticated ? (
                <Navigate to={getRedirectPath()} replace />
              ) : (
                <Login onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/admin/login"
            element={
              isAuthenticated && userRole === 'admin' ? (
                <Navigate to="/admin/dashboard" replace />
              ) : (
                <AdminLogin onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/dashboard"
            element={
              isAuthenticated && userRole === 'student' ? (
                <StudentDashboard student={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/dashboard/task/:taskId"
            element={
              isAuthenticated && userRole === 'student' ? (
                <TaskDetail student={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/teacher/dashboard"
            element={
              isAuthenticated && userRole === 'teacher' ? (
                <TeacherDashboard teacher={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/admin/dashboard"
            element={
              isAuthenticated && userRole === 'admin' ? (
                <AdminDashboard admin={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/admin/login" replace />
              )
            }
          />
          <Route
            path="/pathway/:pathwayId"
            element={
              isAuthenticated && userRole === 'student' ? (
                <PathwayDetail student={user} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route path="/" element={<Navigate to={getRedirectPath()} replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
