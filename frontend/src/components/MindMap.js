/**
 * Adaptive Personalized Mind Map Component
 * Displays topics with mastery levels, recommendations, and learning progress
 */
import React, { useState, useEffect } from 'react';
import { adaptiveAPI } from '../services/api';
import './MindMap.css';

function MindMap({ topics, studentId }) {
  const [masteryData, setMasteryData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [hoveredTopic, setHoveredTopic] = useState(null);

  // Fetch adaptive learning data when studentId is provided
  useEffect(() => {
    if (studentId) {
      fetchAdaptiveData();
    } else {
      setLoading(false);
    }
  }, [studentId]);

  const fetchAdaptiveData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [mastery, recs] = await Promise.all([
        adaptiveAPI.getMastery(studentId).catch(() => null),
        adaptiveAPI.getRecommendations(studentId).catch(() => ({ recommendations: [] }))
      ]);
      
      setMasteryData(mastery);
      setRecommendations(recs?.recommendations || []);
    } catch (err) {
      console.error('Error fetching adaptive data:', err);
      setError('Failed to load learning data. Showing basic mind map.');
    } finally {
      setLoading(false);
    }
  };

  if (!topics || topics.length === 0) {
    return (
      <div className="mindmap-container">
        <p className="mindmap-empty">No topics available for this pathway.</p>
      </div>
    );
  }

  // Normalize topic name to match concept names in mastery data
  const normalizeConceptName = (topicName) => {
    return topicName
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .replace(/\s+/g, '_')
      .trim();
  };

  // Get mastery score for a topic
  const getTopicMastery = (topic) => {
    if (!masteryData || !masteryData.concepts) return null;
    
    const topicName = normalizeConceptName(topic.name);
    
    // Try exact match first
    if (masteryData.concepts[topicName]) {
      return masteryData.concepts[topicName];
    }
    
    // Try partial match
    for (const [concept, data] of Object.entries(masteryData.concepts)) {
      if (concept.includes(topicName) || topicName.includes(concept)) {
        return data;
      }
    }
    
    // Try matching by topic name variations
    const topicWords = topicName.split('_');
    for (const [concept, data] of Object.entries(masteryData.concepts)) {
      const conceptWords = concept.split('_');
      const matchCount = topicWords.filter(word => 
        conceptWords.some(cw => cw.includes(word) || word.includes(cw))
      ).length;
      if (matchCount > 0 && matchCount >= Math.ceil(topicWords.length / 2)) {
        return data;
      }
    }
    
    return null;
  };

  // Check if topic is recommended
  const isRecommended = (topic) => {
    if (!recommendations || recommendations.length === 0) return null;
    
    const topicName = normalizeConceptName(topic.name);
    return recommendations.find(rec => {
      const recConcept = normalizeConceptName(rec.concept || '');
      return recConcept === topicName || 
             recConcept.includes(topicName) || 
             topicName.includes(recConcept);
    });
  };

  // Get mastery color based on score
  const getMasteryColor = (score) => {
    if (score === null || score === undefined) return 'gray'; // Not attempted
    if (score >= 0.8) return 'green'; // Mastered
    if (score >= 0.6) return 'blue'; // Good progress
    if (score >= 0.4) return 'yellow'; // In progress
    return 'red'; // Weak
  };

  // Get mastery status text
  const getMasteryStatus = (score) => {
    if (score === null || score === undefined) return 'Not Started';
    if (score >= 0.8) return 'Mastered';
    if (score >= 0.6) return 'Good Progress';
    if (score >= 0.4) return 'In Progress';
    return 'Weak Area';
  };

  // Get trend icon
  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving': return '📈';
      case 'declining': return '📉';
      default: return '➡️';
    }
  };

  // Group topics by level
  const topicsByLevel = {};
  topics.forEach((topic) => {
    const level = topic.level || 0;
    if (!topicsByLevel[level]) {
      topicsByLevel[level] = [];
    }
    topicsByLevel[level].push(topic);
  });

  // Render topic node with adaptive features
  const renderTopic = (topic) => {
    const mastery = getTopicMastery(topic);
    const masteryScore = mastery?.mastery_score || null;
    const recommendation = isRecommended(topic);
    const color = getMasteryColor(masteryScore);
    const status = getMasteryStatus(masteryScore);
    const isHighPriority = recommendation?.priority === 'high';

    return (
      <div
        key={topic.id || topic.name}
        className={`mindmap-node adaptive-node ${color}-node ${isHighPriority ? 'recommended-high' : recommendation ? 'recommended' : ''}`}
        data-level={topic.level}
        onMouseEnter={() => setHoveredTopic(topic)}
        onMouseLeave={() => setHoveredTopic(null)}
      >
        <div className="node-content">
          <div className="node-header">
            <span className="node-name">{topic.name}</span>
            {recommendation && (
              <span className="recommendation-badge" title={`Priority: ${recommendation.priority}`}>
                {recommendation.priority === 'high' ? '⭐' : '💡'}
              </span>
            )}
          </div>
          
          {masteryScore !== null ? (
            <>
              <div className="mastery-indicator">
                <div className="mastery-bar-container">
                  <div
                    className={`mastery-bar ${color}`}
                    style={{ width: `${(masteryScore * 100).toFixed(0)}%` }}
                  />
                </div>
                <span className="mastery-percentage">
                  {(masteryScore * 100).toFixed(0)}%
                </span>
              </div>
              
              <div className="mastery-status">
                <span className={`status-badge ${color}`}>{status}</span>
                {mastery.trend && mastery.trend !== 'stable' && (
                  <span className="trend-icon" title={`Trend: ${mastery.trend}`}>
                    {getTrendIcon(mastery.trend)}
                  </span>
                )}
              </div>
              
              {mastery.questions_answered > 0 && (
                <div className="mastery-stats">
                  {mastery.correct_answers}/{mastery.questions_answered} correct
                </div>
              )}
            </>
          ) : (
            <div className="mastery-indicator">
              <span className="not-started">Not yet attempted</span>
            </div>
          )}
          
          {recommendation && hoveredTopic === topic && (
            <div className="recommendation-tooltip">
              <strong>{recommendation.type.toUpperCase()}</strong>
              <p>{recommendation.reason}</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  // Render connections with color based on mastery
  const renderConnections = () => {
    const connections = [];
    topics.forEach((topic) => {
      if (topic.connections && topic.connections.length > 0) {
        topic.connections.forEach((connectedId) => {
          const connectedTopic = topics.find((t) => t.id === connectedId || t.name === connectedId);
          if (connectedTopic) {
            const fromMastery = getTopicMastery(topic);
            const toMastery = getTopicMastery(connectedTopic);
            const fromScore = fromMastery?.mastery_score || null;
            const toScore = toMastery?.mastery_score || null;
            
            // Determine connection strength based on mastery
            let connectionStrength = 'weak';
            if (fromScore !== null && toScore !== null) {
              const avgScore = (fromScore + toScore) / 2;
              if (avgScore >= 0.8) connectionStrength = 'strong';
              else if (avgScore >= 0.5) connectionStrength = 'medium';
            }
            
            connections.push({
              from: topic,
              to: connectedTopic,
              strength: connectionStrength
            });
          }
        });
      }
    });
    
    return connections;
  };

  const connections = renderConnections();

  if (loading) {
    return (
      <div className="mindmap-container">
        <div className="mindmap-loading">
          <p>Loading your personalized learning map...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mindmap-container adaptive-mindmap">
      {error && (
        <div className="mindmap-warning">
          <p>{error}</p>
        </div>
      )}
      
      {/* Legend */}
      {masteryData && (
        <div className="mindmap-legend">
          <h4>Mastery Status</h4>
          <div className="legend-items">
            <div className="legend-item">
              <div className="legend-color green"></div>
              <span>Mastered (80%+)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color blue"></div>
              <span>Good Progress (60-79%)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color yellow"></div>
              <span>In Progress (40-59%)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color red"></div>
              <span>Weak Area (&lt;40%)</span>
            </div>
            <div className="legend-item">
              <div className="legend-color gray"></div>
              <span>Not Started</span>
            </div>
            {recommendations.length > 0 && (
              <div className="legend-item">
                <span className="recommendation-badge">⭐</span>
                <span>Recommended</span>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="mindmap-wrapper">
        {/* Render connections first (behind nodes) */}
        <svg className="connections-layer">
          {connections.map((conn, idx) => {
            const fromTopic = conn.from;
            const toTopic = conn.to;
            const fromIndex = topics.findIndex(t => 
              (t.id || t.name) === (fromTopic.id || fromTopic.name)
            );
            const toIndex = topics.findIndex(t => 
              (t.id || t.name) === (toTopic.id || toTopic.name)
            );
            const fromLevel = fromTopic.level || 0;
            const toLevel = toTopic.level || 0;
            
            // Calculate positions (horizontal layout)
            const fromX = 150 + fromLevel * 250;
            const fromY = 100 + (fromIndex % 5) * 120;
            const toX = 150 + toLevel * 250;
            const toY = 100 + (toIndex % 5) * 120;
            
            // Connection color based on strength
            const strokeColor = {
              'strong': '#28a745',
              'medium': '#667eea',
              'weak': '#dc3545'
            }[conn.strength] || '#999';
            
            const strokeWidth = {
              'strong': 3,
              'medium': 2,
              'weak': 1.5
            }[conn.strength] || 2;
            
            return (
              <line
                key={`${fromTopic.id || fromTopic.name}-${toTopic.id || toTopic.name}-${idx}`}
                x1={fromX}
                y1={fromY}
                x2={toX}
                y2={toY}
                stroke={strokeColor}
                strokeWidth={strokeWidth}
                opacity="0.4"
                className="connection-line"
              />
            );
          })}
        </svg>

        {/* Render topic nodes by level */}
        <div className="mindmap-levels">
          {Object.keys(topicsByLevel)
            .sort((a, b) => parseInt(a) - parseInt(b))
            .map((level) => (
              <div key={level} className="mindmap-level">
                <h4 className="level-label">Level {level}</h4>
                <div className="level-topics">
                  {topicsByLevel[level].map((topic) => renderTopic(topic))}
                </div>
              </div>
            ))}
        </div>
      </div>

      {/* Summary statistics */}
      {masteryData && masteryData.overall_mastery !== undefined && (
        <div className="mindmap-summary">
          <div className="summary-item">
            <span className="summary-label">Overall Mastery:</span>
            <span className="summary-value">
              {(masteryData.overall_mastery * 100).toFixed(1)}%
            </span>
          </div>
          <div className="summary-item">
            <span className="summary-label">Topics Tracked:</span>
            <span className="summary-value">
              {Object.keys(masteryData.concepts || {}).length}
            </span>
          </div>
          {recommendations.length > 0 && (
            <div className="summary-item">
              <span className="summary-label">Recommendations:</span>
              <span className="summary-value">{recommendations.length}</span>
            </div>
          )}
        </div>
      )}

      {/* Alternative list view with mastery */}
      <div className="mindmap-list-view">
        <h3>Topic Structure & Progress</h3>
        <ul className="topic-list">
          {topics.map((topic) => {
            const mastery = getTopicMastery(topic);
            const masteryScore = mastery?.mastery_score || null;
            const recommendation = isRecommended(topic);
            const color = getMasteryColor(masteryScore);
            
            return (
              <li 
                key={topic.id || topic.name} 
                className={`topic-item ${color}-border`}
                data-level={topic.level}
              >
                <div className="topic-info">
                  <span className="topic-name">{topic.name}</span>
                  {masteryScore !== null && (
                    <span className={`topic-mastery ${color}`}>
                      {(masteryScore * 100).toFixed(0)}%
                    </span>
                  )}
                  {recommendation && (
                    <span className="topic-recommendation" title={recommendation.reason}>
                      {recommendation.priority === 'high' ? '⭐' : '💡'}
                    </span>
                  )}
                </div>
                {topic.connections && topic.connections.length > 0 && (
                  <span className="topic-connections">
                    → {topic.connections.length} connected topic(s)
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

export default MindMap;
