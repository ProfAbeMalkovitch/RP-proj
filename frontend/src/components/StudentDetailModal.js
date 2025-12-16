/**
 * Student Detail Modal Component
 * Shows detailed student progress with line chart
 */
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './StudentDetailModal.css';

function StudentDetailModal({ student, onClose }) {
  const chartData = student.quiz_history || [];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Student Details: {student.name}</h2>
          <button className="modal-close-btn" onClick={onClose}>×</button>
        </div>

        <div className="modal-body">
          <div className="student-info-grid">
            <div className="info-item">
              <label>Email:</label>
              <span>{student.email}</span>
            </div>
            <div className="info-item">
              <label>Pathway:</label>
              <span className={`pathway-badge pathway-${student.pathway?.toLowerCase()}`}>
                {student.pathway}
              </span>
            </div>
            <div className="info-item">
              <label>Average Score:</label>
              <span>{student.average_score?.toFixed(1)}%</span>
            </div>
            <div className="info-item">
              <label>Total Quizzes:</label>
              <span>{student.total_quizzes || 0}</span>
            </div>
            {student.statistics && (
              <>
                <div className="info-item">
                  <label>Highest Score:</label>
                  <span>{student.statistics.highest_score}%</span>
                </div>
                <div className="info-item">
                  <label>Lowest Score:</label>
                  <span>{student.statistics.lowest_score}%</span>
                </div>
                <div className="info-item">
                  <label>Trend:</label>
                  <span className={`trend-${student.statistics.trend}`}>
                    {student.statistics.trend}
                  </span>
                </div>
              </>
            )}
          </div>

          {chartData.length > 0 && (
            <div className="chart-section">
              <h3>Quiz History</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="quiz" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="score" 
                    stroke="#667eea" 
                    strokeWidth={2}
                    name="Score (%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          <div className="quiz-scores-list">
            <h3>All Quiz Scores</h3>
            <div className="scores-grid">
              {student.quiz_scores?.map((score, index) => (
                <div key={index} className="score-item">
                  Quiz {index + 1}: <strong>{score.toFixed(1)}%</strong>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn btn-primary" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}

export default StudentDetailModal;





































