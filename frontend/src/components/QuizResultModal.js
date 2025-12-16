/**
 * Quiz Result Modal Component
 * Displays quiz submission results in a popup
 */
import React from 'react';
import './QuizResultModal.css';

function QuizResultModal({ result, onClose }) {
  if (!result) return null;

  // Get performance color based on score
  const getPerformanceColor = (percentage) => {
    if (percentage >= 80) return 'performance-excellent';
    if (percentage >= 70) return 'performance-good';
    if (percentage >= 50) return 'performance-average';
    return 'performance-poor';
  };

  // Get performance label
  const getPerformanceLabel = (percentage) => {
    if (percentage >= 80) return 'Excellent';
    if (percentage >= 70) return 'Good';
    if (percentage >= 50) return 'Average';
    return 'Needs Improvement';
  };

  return (
    <div className="quiz-result-modal-overlay" onClick={onClose}>
      <div className="quiz-result-modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="quiz-result-modal-header">
          <h2>Quiz Results</h2>
          <button className="quiz-result-modal-close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="quiz-result-modal-body">
          <div className="result-summary">
            <div className="result-score">
              <span className="score-label">Your Score:</span>
              <span className={`score-value ${getPerformanceColor(result.percentage)}`}>
                {result.percentage.toFixed(1)}%
              </span>
            </div>
            <div className="result-details">
              <div className="result-detail-item">
                <span className="detail-label">Points Earned:</span>
                <span className="detail-value">{result.score} / {result.total_points}</span>
              </div>
              <div className="result-detail-item">
                <span className="detail-label">Performance:</span>
                <span className={`detail-value ${getPerformanceColor(result.percentage)}`}>
                  {getPerformanceLabel(result.percentage)}
                </span>
              </div>
              <div className="result-detail-item">
                <span className="detail-label">Submitted:</span>
                <span className="detail-value">
                  {new Date(result.submitted_at).toLocaleString()}
                </span>
              </div>
            </div>
          </div>

          <div className="result-message">
            {result.percentage >= 80 ? (
              <p className="success-message">🎉 Excellent work! You've mastered this quiz!</p>
            ) : result.percentage >= 70 ? (
              <p className="good-message">👍 Great job! You're doing well!</p>
            ) : result.percentage >= 50 ? (
              <p className="average-message">📚 Good effort! Keep practicing to improve!</p>
            ) : (
              <p className="poor-message">💪 Don't give up! Review the material and try again!</p>
            )}
          </div>
        </div>

        <div className="quiz-result-modal-footer">
          <button className="btn btn-primary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default QuizResultModal;



