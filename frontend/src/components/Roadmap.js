/**
 * Enhanced Roadmap Component
 * Displays learning tasks in a roadmap format with support for generated roadmaps
 */
import React, { useState } from 'react';
import './Roadmap.css';

function Roadmap({ roadmap, studentId, onTaskComplete }) {
  // Handle both old format (array) and new format (object with tasks)
  const roadmapData = Array.isArray(roadmap) ? roadmap : (roadmap?.tasks || roadmap?.roadmap || []);
  const roadmapInfo = Array.isArray(roadmap) ? null : roadmap;

  if (!roadmapData || roadmapData.length === 0) {
    return (
      <div className="roadmap-container">
        <p className="roadmap-empty">No roadmap available for this pathway.</p>
      </div>
    );
  }

  // Sort roadmap by order
  const sortedRoadmap = [...roadmapData].sort((a, b) => (a.order || 0) - (b.order || 0));

  // Calculate progress
  const totalTasks = sortedRoadmap.length;
  const completedTasks = sortedRoadmap.filter(task => 
    task.completed || task.status === 'completed'
  ).length;
  const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;

  // Get status icon
  const getStatusIcon = (task) => {
    if (task.completed || task.status === 'completed') return '✓';
    if (task.status === 'in-progress') return '⟳';
    return '○';
  };

  // Get status class
  const getStatusClass = (task) => {
    if (task.completed || task.status === 'completed') return 'completed';
    if (task.status === 'in-progress') return 'in-progress';
    return 'pending';
  };

  // Get task type icon
  const getTaskTypeIcon = (taskType) => {
    switch (taskType) {
      case 'quiz': return '📝';
      case 'reading': return '📖';
      case 'practice': return '✏️';
      case 'project': return '🎯';
      case 'video': return '📹';
      case 'assignment': return '📋';
      default: return '📌';
    }
  };

  // Format time
  const formatTime = (minutes) => {
    if (!minutes) return '';
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return mins > 0 ? `${hours}h ${mins}m` : `${hours}h`;
  };

  const handleTaskClick = (task) => {
    if (onTaskComplete && !task.completed && task.status !== 'completed') {
      // Call parent handler if provided
      onTaskComplete(task);
    }
  };

  return (
    <div className="roadmap-container enhanced-roadmap">
      {/* Roadmap Header with Progress */}
      {roadmapInfo && (
        <div className="roadmap-header">
          <div className="roadmap-title-section">
            <h2 className="roadmap-title">Your Personalized Learning Roadmap</h2>
            {roadmapInfo.generation_reason && (
              <p className="roadmap-reason">{roadmapInfo.generation_reason}</p>
            )}
          </div>
          {roadmapInfo.focus_areas && roadmapInfo.focus_areas.length > 0 && (
            <div className="focus-areas">
              <span className="focus-label">Focus Areas:</span>
              {roadmapInfo.focus_areas.map((area, idx) => (
                <span key={idx} className="focus-tag">{area}</span>
              ))}
            </div>
          )}
          {roadmapInfo.status && (
            <div className={`roadmap-status-badge status-${roadmapInfo.status}`}>
              {roadmapInfo.status.charAt(0).toUpperCase() + roadmapInfo.status.slice(1)}
            </div>
          )}
        </div>
      )}

      {/* Progress Bar */}
      <div className="roadmap-progress-section">
        <div className="progress-info">
          <span className="progress-text">
            Progress: {completedTasks} of {totalTasks} tasks completed
          </span>
          <span className="progress-percentage">{Math.round(progressPercentage)}%</span>
        </div>
        <div className="progress-bar-container">
          <div 
            className="progress-bar-fill"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>
      </div>

      {/* Roadmap Timeline */}
      <div className="roadmap-timeline">
        {sortedRoadmap.map((task, index) => {
          const isCompleted = task.completed || task.status === 'completed';
          const statusClass = getStatusClass(task);
          
          return (
            <div 
              key={task.task_id || task.id || index} 
              className={`roadmap-item ${statusClass} ${isCompleted ? 'completed-task' : ''}`}
              onClick={() => handleTaskClick(task)}
            >
              <div className="roadmap-marker">
                <span className={`status-icon ${statusClass}`}>
                  {getStatusIcon(task)}
                </span>
                {index < sortedRoadmap.length - 1 && <div className="timeline-line" />}
              </div>
              <div className="roadmap-content">
                <div className="task-header">
                  <div className="task-title-section">
                    {task.task_type && (
                      <span className="task-type-icon" title={task.task_type}>
                        {getTaskTypeIcon(task.task_type)}
                      </span>
                    )}
                    <h3 className="task-title">{task.title}</h3>
                  </div>
                  <div className="task-meta">
                    {task.estimated_time && (
                      <span className="task-time" title="Estimated time">
                        ⏱️ {formatTime(task.estimated_time)}
                      </span>
                    )}
                    {task.difficulty && (
                      <span className={`task-difficulty difficulty-${task.difficulty}`}>
                        {task.difficulty}
                      </span>
                    )}
                    <span className={`task-status-badge ${statusClass}`}>
                      {isCompleted ? 'Completed' : (task.status || 'Pending')}
                    </span>
                  </div>
                </div>
                
                {task.description && (
                  <p className="task-description">{task.description}</p>
                )}
                
                {task.learning_objectives && task.learning_objectives.length > 0 && (
                  <div className="learning-objectives">
                    <strong>Learning Objectives:</strong>
                    <ul>
                      {task.learning_objectives.map((objective, idx) => (
                        <li key={idx}>{objective}</li>
                      ))}
                    </ul>
                  </div>
                )}
                
                <div className="task-footer">
                  <span className="task-order">Step {task.order || index + 1}</span>
                  {task.tags && task.tags.length > 0 && (
                    <div className="task-tags">
                      {task.tags.map((tag, idx) => (
                        <span key={idx} className="task-tag">{tag}</span>
                      ))}
                    </div>
                  )}
                  {task.resource_url && (
                    <a 
                      href={task.resource_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="task-resource-link"
                      onClick={(e) => e.stopPropagation()}
                    >
                      📎 View Resource
                    </a>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Roadmap Summary */}
      {roadmapInfo && (
        <div className="roadmap-summary">
          <div className="summary-item">
            <span className="summary-label">Total Tasks</span>
            <span className="summary-value">{totalTasks}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Completed</span>
            <span className="summary-value">{completedTasks}</span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Remaining</span>
            <span className="summary-value">{totalTasks - completedTasks}</span>
          </div>
          {roadmapInfo.estimated_completion_date && (
            <div className="summary-item">
              <span className="summary-label">Est. Completion</span>
              <span className="summary-value">
                {new Date(roadmapInfo.estimated_completion_date).toLocaleDateString()}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Roadmap;
