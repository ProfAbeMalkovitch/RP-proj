/**
 * Dashboard Component
 * Displays the three learning pathways (Basic, Intermediate, Excellent)
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { pathwayAPI } from '../services/api';
import './Dashboard.css';

function Dashboard({ student, onLogout }) {
  const [pathways, setPathways] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Fetch pathways on component mount
  useEffect(() => {
    fetchPathways();
  }, []);

  // Fetch all pathways from API
  const fetchPathways = async () => {
    try {
      const data = await pathwayAPI.getAllPathways();
      // Sort pathways by level order
      const sortedPathways = data.sort((a, b) => {
        const order = { Basic: 1, Intermediate: 2, Excellent: 3 };
        return order[a.level] - order[b.level];
      });
      setPathways(sortedPathways);
    } catch (err) {
      setError('Failed to load pathways. Please try again.');
      console.error('Error fetching pathways:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle pathway click - navigate to pathway detail
  const handlePathwayClick = (pathwayId) => {
    navigate(`/pathway/${pathwayId}`);
  };

  // Get pathway card class based on level
  const getPathwayClass = (level) => {
    const levelMap = {
      Basic: 'pathway-basic',
      Intermediate: 'pathway-intermediate',
      Excellent: 'pathway-excellent',
    };
    return levelMap[level] || '';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading">Loading pathways...</div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Learning Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {student?.name}</span>
            <span className="score">Score: {student?.cumulative_score?.toFixed(1) || 0}</span>
            <button onClick={onLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <div className="pathways-section">
        <h2>Choose Your Learning Path</h2>
        <p className="section-description">
          Select a pathway that matches your current skill level and learning goals
        </p>

        <div className="pathways-grid">
          {pathways.map((pathway) => (
            <div
              key={pathway.pathway_id}
              className={`pathway-card ${getPathwayClass(pathway.level)}`}
              onClick={() => handlePathwayClick(pathway.pathway_id)}
            >
              <div className="pathway-header">
                <h3>{pathway.name}</h3>
                <span className="pathway-level">{pathway.level}</span>
              </div>
              <p className="pathway-description">{pathway.description}</p>
              <div className="pathway-stats">
                <span>{pathway.roadmap?.length || 0} Tasks</span>
                <span>{pathway.quiz_ids?.length || 0} Quizzes</span>
              </div>
              <button className="btn btn-primary pathway-btn">Explore Pathway</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;









