/**
 * Concept Mastery Card Component
 * Displays concept mastery progress with visual indicators
 */
import React from 'react';
import './ConceptMasteryCard.css';

function ConceptMasteryCard({ masteryData }) {
  if (!masteryData || !masteryData.concepts) {
    return (
      <div className="concept-mastery-card">
        <p>No mastery data available yet. Complete quizzes to track your progress!</p>
      </div>
    );
  }

  const concepts = Object.entries(masteryData.concepts || {});
  const overallMastery = masteryData.overall_mastery || 0;

  const getMasteryColor = (score) => {
    if (score >= 0.8) return '#28a745'; // Green
    if (score >= 0.6) return '#17a2b8'; // Blue
    if (score >= 0.4) return '#ffc107'; // Yellow
    return '#dc3545'; // Red
  };

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving':
        return '📈';
      case 'declining':
        return '📉';
      default:
        return '➡️';
    }
  };

  return (
    <div className="concept-mastery-card">
      <div className="mastery-header">
        <h3>Concept Mastery</h3>
        <div className="overall-mastery">
          <span className="mastery-label">Overall:</span>
          <span 
            className="mastery-percentage"
            style={{ color: getMasteryColor(overallMastery) }}
          >
            {(overallMastery * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="mastery-progress-bar">
        <div
          className="mastery-fill"
          style={{
            width: `${overallMastery * 100}%`,
            backgroundColor: getMasteryColor(overallMastery)
          }}
        />
      </div>

      <div className="concepts-list">
        {concepts.length === 0 ? (
          <p className="no-concepts">Complete quizzes to see your concept mastery!</p>
        ) : (
          concepts.map(([concept, data]) => {
            const mastery = data.mastery_score || 0;
            const trend = data.trend || 'stable';
            
            return (
              <div key={concept} className="concept-item">
                <div className="concept-header">
                  <span className="concept-name">{concept.replace(/_/g, ' ').toUpperCase()}</span>
                  <span className="concept-trend" title={`Trend: ${trend}`}>
                    {getTrendIcon(trend)}
                  </span>
                </div>
                <div className="concept-progress">
                  <div className="concept-progress-bar">
                    <div
                      className="concept-progress-fill"
                      style={{
                        width: `${mastery * 100}%`,
                        backgroundColor: getMasteryColor(mastery)
                      }}
                    />
                  </div>
                  <span 
                    className="concept-score"
                    style={{ color: getMasteryColor(mastery) }}
                  >
                    {(mastery * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="concept-stats">
                  <span className="stat-text">
                    {data.correct_answers || 0} / {data.questions_answered || 0} correct
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default ConceptMasteryCard;





















