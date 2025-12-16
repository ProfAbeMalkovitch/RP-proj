/**
 * Student Progress Modal Component
 * Displays detailed student progress, pathways, and weaknesses in a popup
 */
import React from 'react';
import './StudentProgressModal.css';

function StudentProgressModal({ student, onClose }) {
  // Get performance color based on score
  const getPerformanceColor = (score) => {
    if (score >= 80) return 'performance-excellent';
    if (score >= 70) return 'performance-good';
    if (score >= 50) return 'performance-average';
    return 'performance-poor';
  };

  // Get performance label
  const getPerformanceLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 70) return 'Good';
    if (score >= 50) return 'Average';
    return 'Needs Improvement';
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Student Progress Details</h2>
          <button className="modal-close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="modal-body">
          {/* Student Info */}
          <div className="student-info-section">
            <h3>{student.name}</h3>
            <p className="student-email">{student.email}</p>
            <div className="student-overview">
              <div className="overview-item">
                <span className="overview-label">Student ID:</span>
                <span className="overview-value">{student.student_id}</span>
              </div>
              <div className="overview-item">
                <span className="overview-label">Cumulative Score:</span>
                <span className="overview-value">{student.cumulative_score.toFixed(1)}</span>
              </div>
              <div className="overview-item">
                <span className="overview-label">Quizzes Completed:</span>
                <span className="overview-value">{student.total_quizzes_completed}</span>
              </div>
              <div className="overview-item">
                <span className="overview-label">Average Score:</span>
                <span className={`overview-value ${getPerformanceColor(student.average_score)}`}>
                  {student.average_score.toFixed(1)}%
                </span>
              </div>
              <div className="overview-item">
                <span className="overview-label">Performance:</span>
                <span className={`overview-value ${getPerformanceColor(student.average_score)}`}>
                  {getPerformanceLabel(student.average_score)}
                </span>
              </div>
            </div>
          </div>

          {/* Pathways Section */}
          <div className="pathways-section">
            <h3>Learning Pathways</h3>
            {student.pathways.length > 0 ? (
              <div className="pathways-list">
                {student.pathways.map((pathway) => (
                  <div key={pathway.pathway_id} className="pathway-card">
                    <div className="pathway-header">
                      <h4>{pathway.name}</h4>
                      <span className="pathway-level">{pathway.level}</span>
                    </div>
                    <div className="pathway-stats">
                      <div className="pathway-stat">
                        <span className="stat-label">Quizzes Completed:</span>
                        <span className="stat-value">{pathway.quizzes_completed}</span>
                      </div>
                      <div className="pathway-stat">
                        <span className="stat-label">Average Score:</span>
                        <span className={`stat-value ${getPerformanceColor(pathway.average_score)}`}>
                          {pathway.average_score.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    {pathway.latest_result && (
                      <div className="pathway-latest">
                        <span>Latest Quiz: {pathway.latest_result.quiz_id}</span>
                        <span className={`score ${getPerformanceColor(pathway.latest_result.percentage)}`}>
                          {pathway.latest_result.percentage.toFixed(1)}%
                        </span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No pathways started yet</p>
            )}
          </div>

          {/* Weaknesses Section */}
          <div className="weaknesses-section">
            <h3>Student Weaknesses</h3>
            {student.weaknesses.length > 0 ? (
              <div className="weaknesses-list">
                {student.weaknesses.map((weakness, index) => (
                  <div key={index} className="weakness-card">
                    <div className="weakness-header">
                      <h4>{weakness.quiz_title}</h4>
                      <span className="weakness-pathway">{weakness.pathway_name}</span>
                    </div>
                    <div className="weakness-stats">
                      <div className="weakness-stat">
                        <span className="stat-label">Score:</span>
                        <span className={`stat-value ${getPerformanceColor(weakness.score)}`}>
                          {weakness.score.toFixed(1)}%
                        </span>
                      </div>
                      <div className="weakness-stat">
                        <span className="stat-label">Wrong Answers:</span>
                        <span className="stat-value">{weakness.wrong_answers.length}</span>
                      </div>
                      <div className="weakness-stat">
                        <span className="stat-label">Submitted:</span>
                        <span className="stat-value">
                          {new Date(weakness.submitted_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <div className="weak-areas">
                      <h5>Weak Areas:</h5>
                      <ul>
                        {weakness.weak_areas.map((area, idx) => (
                          <li key={idx}>{area}</li>
                        ))}
                      </ul>
                    </div>
                    {weakness.wrong_answers.length > 0 && (
                      <div className="wrong-answers">
                        <h5>Incorrect Answers:</h5>
                        {weakness.wrong_answers.slice(0, 3).map((answer, idx) => (
                          <div key={idx} className="wrong-answer-item">
                            <p className="question-text">{answer.question_text}</p>
                            <div className="answer-comparison">
                              <span className="correct-answer">
                                Correct: Option {answer.correct_answer + 1}
                              </span>
                              <span className="student-answer">
                                Student: Option {answer.student_answer !== null ? answer.student_answer + 1 : 'Not answered'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-data">No weaknesses identified. Student is performing well!</p>
            )}
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-primary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default StudentProgressModal;



