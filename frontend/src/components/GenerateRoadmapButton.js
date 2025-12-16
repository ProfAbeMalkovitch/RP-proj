/**
 * Generate Roadmap Button Component
 * Button to generate personalized roadmap using knowledge base
 */
import React, { useState } from 'react';
import { roadmapAPI } from '../services/api';
import './GenerateRoadmapButton.css';

function GenerateRoadmapButton({ studentId, onRoadmapGenerated }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleGenerate = async (regenerate = false) => {
    try {
      setLoading(true);
      setError('');
      setSuccess(false);
      setShowConfirm(false);

      const response = await roadmapAPI.generateRoadmap(studentId, {
        regenerate,
        max_tasks: 10
      });

      if (response.error) {
        setError(response.error);
      } else {
        setSuccess(true);
        if (onRoadmapGenerated) {
          onRoadmapGenerated(response.roadmap);
        }
        
        // Auto-hide success message after 3 seconds
        setTimeout(() => setSuccess(false), 3000);
      }
    } catch (err) {
      console.error('Error generating roadmap:', err);
      setError(err.response?.data?.detail || 'Failed to generate roadmap. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClick = () => {
    // Check if roadmap exists first
    roadmapAPI.getActiveRoadmap(studentId)
      .then(() => {
        // Roadmap exists, show confirmation
        setShowConfirm(true);
      })
      .catch(() => {
        // No active roadmap, generate new one
        handleGenerate(false);
      });
  };

  return (
    <div className="generate-roadmap-container">
      {error && (
        <div className="generate-roadmap-error">
          <span>⚠️</span>
          <p>{error}</p>
          <button onClick={() => setError('')}>✕</button>
        </div>
      )}
      
      {success && (
        <div className="generate-roadmap-success">
          <span>✓</span>
          <p>Roadmap generated successfully!</p>
        </div>
      )}

      {showConfirm && (
        <div className="generate-roadmap-confirm">
          <p>You already have an active roadmap. Generate a new one?</p>
          <div className="confirm-buttons">
            <button 
              className="btn-confirm"
              onClick={() => handleGenerate(true)}
              disabled={loading}
            >
              Yes, Generate New
            </button>
            <button 
              className="btn-cancel"
              onClick={() => setShowConfirm(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <button
        className={`generate-roadmap-btn ${loading ? 'loading' : ''}`}
        onClick={handleClick}
        disabled={loading}
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Generating Your Personalized Roadmap...
          </>
        ) : (
          <>
            <span className="btn-icon">✨</span>
            Generate My Personalized Roadmap
          </>
        )}
      </button>

      {!loading && (
        <p className="generate-roadmap-hint">
          Create a customized learning path based on your knowledge and weak areas
        </p>
      )}
    </div>
  );
}

export default GenerateRoadmapButton;





















