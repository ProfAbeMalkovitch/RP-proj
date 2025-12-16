/**
 * Recommendations Card Component
 * Displays personalized learning recommendations
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './RecommendationsCard.css';

function RecommendationsCard({ recommendations, studentId }) {
  const navigate = useNavigate();

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="recommendations-card">
        <h3>Learning Recommendations</h3>
        <p className="no-recommendations">No recommendations available. Complete quizzes to get personalized suggestions!</p>
      </div>
    );
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return '#dc3545';
      case 'medium':
        return '#ffc107';
      default:
        return '#6c757d';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'practice':
        return '💪';
      case 'review':
        return '📚';
      case 'advance':
        return '🚀';
      case 'prerequisite':
        return '🔑';
      default:
        return '📝';
    }
  };

  const handleRecommendationClick = (rec) => {
    if (rec.content_type === 'quiz' && rec.content_id) {
      // Navigate to quiz or task page
      // You can implement navigation logic here
      console.log('Navigate to:', rec.content_id);
    } else if (rec.content_type === 'pathway' && rec.content_id) {
      navigate(`/pathway/${rec.content_id}`);
    }
  };

  // Sort by priority
  const sortedRecs = [...recommendations].sort((a, b) => {
    const priorityOrder = { high: 0, medium: 1, low: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  return (
    <div className="recommendations-card">
      <div className="recommendations-header">
        <h3>📋 Personalized Recommendations</h3>
        <span className="recommendations-count">{recommendations.length}</span>
      </div>

      <div className="recommendations-list">
        {sortedRecs.map((rec, index) => (
          <div
            key={index}
            className={`recommendation-item priority-${rec.priority}`}
            onClick={() => handleRecommendationClick(rec)}
          >
            <div className="recommendation-icon">
              {getTypeIcon(rec.type)}
            </div>
            <div className="recommendation-content">
              <div className="recommendation-header-row">
                <span className="recommendation-type">{rec.type.toUpperCase()}</span>
                <span
                  className="recommendation-priority"
                  style={{ backgroundColor: getPriorityColor(rec.priority) }}
                >
                  {rec.priority}
                </span>
              </div>
              <div className="recommendation-concept">
                {rec.concept}
              </div>
              <div className="recommendation-reason">
                {rec.reason}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationsCard;





















