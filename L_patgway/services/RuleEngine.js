/**
 * RuleEngine Service
 * 
 * Core rule-based logic for pathway determination
 * 
 * Research Alignment:
 * - Transparent, explainable rules (no black-box logic)
 * - Rule-based categorization (NO AI/ML)
 * - Academic-standard documentation
 * 
 * Rule Logic:
 * 1. Primary Factor: Average Quiz Score
 *    - < 50 → BASIC pathway
 *    - 50-74 → BALANCED pathway
 *    - ≥ 75 → ACCELERATION pathway
 * 
 * 2. Secondary Factor: Task Completion Rate
 *    - Low completion may adjust pathway downward
 * 
 * 3. Edge Cases:
 *    - No quiz data → Default to BALANCED
 *    - Incomplete data → Use available metrics
 */

const {
  PATHWAY_TYPES,
  SCORE_THRESHOLDS,
  TASK_COMPLETION_THRESHOLDS,
  MIN_REQUIREMENTS,
  CONTENT_TAGS
} = require('../config/constants');

/**
 * Determine pathway type based on performance metrics
 * 
 * Rule Logic (Transparent):
 * 
 * PRIMARY RULE: Average Quiz Score
 *   IF averageScore < 50:
 *     → BASIC pathway
 *     → Rationale: Student needs foundational support
 *   
 *   IF 50 ≤ averageScore < 75:
 *     → BALANCED pathway
 *     → Rationale: Student progressing normally
 *   
 *   IF averageScore ≥ 75:
 *     → ACCELERATION pathway
 *     → Rationale: Student ready for advanced content
 * 
 * SECONDARY RULE: Task Completion Rate
 *   IF completionRate < 0.5 AND averageScore < 60:
 *     → Adjust to BASIC (even if score suggests BALANCED)
 *     → Rationale: Low engagement indicates need for support
 * 
 * EDGE CASE: No Data
 *   IF no quiz data available:
 *     → Default to BALANCED
 *     → Rationale: Neutral starting point
 * 
 * @param {Object} performanceData - Student performance metrics
 * @param {number} performanceData.average_score - Average quiz score (0-100)
 * @param {number} performanceData.task_completion_rate - Task completion rate (0-1)
 * @param {number} performanceData.total_quizzes - Number of quizzes completed
 * @param {number} performanceData.recent_attempts - Recent quiz attempts count
 * @returns {Object} Pathway determination result
 */
function determinePathway(performanceData) {
  const {
    average_score = 0,
    task_completion_rate = 0,
    total_quizzes = 0,
    recent_attempts = 0
  } = performanceData;

  // EDGE CASE: No quiz data available
  if (total_quizzes < MIN_REQUIREMENTS.MIN_QUIZZES) {
    return {
      pathway_type: PATHWAY_TYPES.BALANCED,
      reasoning: 'Insufficient quiz data - defaulting to BALANCED pathway',
      confidence: 'low',
      factors: {
        primary: 'default',
        secondary: null
      }
    };
  }

  let pathwayType;
  let reasoning;
  let confidence = 'high';
  const factors = {
    primary: null,
    secondary: null
  };

  // PRIMARY RULE: Average Score Classification
  if (average_score < SCORE_THRESHOLDS.BALANCED_MIN) {
    // Score < 50 → BASIC pathway
    pathwayType = PATHWAY_TYPES.BASIC;
    reasoning = `Average score of ${average_score}% indicates need for foundational support`;
    factors.primary = `score_${average_score}_below_50`;
  } else if (average_score < SCORE_THRESHOLDS.ACCELERATION_MIN) {
    // Score 50-74 → BALANCED pathway
    pathwayType = PATHWAY_TYPES.BALANCED;
    reasoning = `Average score of ${average_score}% indicates normal progression`;
    factors.primary = `score_${average_score}_50_to_74`;
  } else {
    // Score ≥ 75 → ACCELERATION pathway
    pathwayType = PATHWAY_TYPES.ACCELERATION;
    reasoning = `Average score of ${average_score}% indicates readiness for advanced content`;
    factors.primary = `score_${average_score}_above_75`;
  }

  // SECONDARY RULE: Task Completion Adjustment
  // Low completion rate may adjust pathway downward
  if (
    task_completion_rate < TASK_COMPLETION_THRESHOLDS.LOW &&
    average_score < 60 &&
    pathwayType !== PATHWAY_TYPES.BASIC
  ) {
    // Adjust to BASIC if completion is very low and score is borderline
    pathwayType = PATHWAY_TYPES.BASIC;
    reasoning += `. Low task completion rate (${(task_completion_rate * 100).toFixed(0)}%) indicates need for additional support`;
    factors.secondary = `low_completion_${task_completion_rate}`;
    confidence = 'medium';
  } else if (
    task_completion_rate < TASK_COMPLETION_THRESHOLDS.MEDIUM &&
    average_score >= SCORE_THRESHOLDS.ACCELERATION_MIN
  ) {
    // High score but low completion → may need to stay in BALANCED
    if (pathwayType === PATHWAY_TYPES.ACCELERATION) {
      pathwayType = PATHWAY_TYPES.BALANCED;
      reasoning += `. Despite high scores, task completion rate (${(task_completion_rate * 100).toFixed(0)}%) suggests maintaining standard pace`;
      factors.secondary = `completion_adjustment_${task_completion_rate}`;
      confidence = 'medium';
    }
  }

  // EDGE CASE: Very few recent attempts
  if (recent_attempts === 0 && total_quizzes > 0) {
    confidence = 'medium';
    reasoning += '. Limited recent activity - pathway may need review';
  }

  return {
    pathway_type: pathwayType,
    reasoning,
    confidence,
    factors
  };
}

/**
 * Generate content recommendation tags based on pathway
 * 
 * @param {string} pathwayType - Pathway type (basic/balanced/acceleration)
 * @returns {Array<string>} Recommended content tags
 */
function generateContentTags(pathwayType) {
  switch (pathwayType) {
    case PATHWAY_TYPES.BASIC:
      return [...CONTENT_TAGS.BASIC];
    case PATHWAY_TYPES.BALANCED:
      return [...CONTENT_TAGS.BALANCED];
    case PATHWAY_TYPES.ACCELERATION:
      return [...CONTENT_TAGS.ACCELERATION];
    default:
      return [...CONTENT_TAGS.BALANCED];
  }
}

/**
 * Generate learning recommendations
 * 
 * Creates structured recommendations based on pathway type
 * 
 * @param {string} pathwayType - Pathway type
 * @param {Object} performanceData - Performance metrics
 * @returns {Array<Object>} Learning recommendations
 */
function generateRecommendations(pathwayType, performanceData) {
  const recommendations = [];
  const { average_score, task_completion_rate } = performanceData;

  switch (pathwayType) {
    case PATHWAY_TYPES.BASIC:
      recommendations.push({
        type: 'content',
        priority: 'high',
        title: 'Focus on Foundational Concepts',
        description: 'Review core concepts and basic principles',
        tags: ['foundational', 'basic-concepts', 'review']
      });
      
      if (task_completion_rate < 0.5) {
        recommendations.push({
          type: 'exercise',
          priority: 'high',
          title: 'Increase Practice Exercises',
          description: 'Complete more practice exercises to build confidence',
          tags: ['practice-exercises', 'guided-practice']
        });
      }
      break;

    case PATHWAY_TYPES.BALANCED:
      recommendations.push({
        type: 'content',
        priority: 'medium',
        title: 'Continue Standard Progression',
        description: 'Follow standard curriculum with interactive content',
        tags: ['standard', 'core-content', 'interactive']
      });
      
      if (average_score >= 65 && average_score < 75) {
        recommendations.push({
          type: 'content',
          priority: 'low',
          title: 'Explore Advanced Topics',
          description: 'Consider exploring more challenging content',
          tags: ['extension', 'challenge']
        });
      }
      break;

    case PATHWAY_TYPES.ACCELERATION:
      recommendations.push({
        type: 'content',
        priority: 'high',
        title: 'Engage with Advanced Content',
        description: 'Explore advanced topics and critical thinking exercises',
        tags: ['advanced', 'extension', 'critical-thinking']
      });
      
      recommendations.push({
        type: 'assessment',
        priority: 'medium',
        title: 'Challenge Assessments',
        description: 'Take on more complex assessments',
        tags: ['challenge', 'deep-dive']
      });
      break;
  }

  return recommendations;
}

/**
 * Validate pathway transition
 * 
 * Checks if pathway change is reasonable (prevents rapid oscillation)
 * 
 * @param {string} currentPathway - Current pathway type
 * @param {string} newPathway - Proposed new pathway type
 * @param {Object} performanceData - Current performance data
 * @returns {Object} Validation result
 */
function validatePathwayTransition(currentPathway, newPathway, performanceData) {
  // Allow transition if pathways are adjacent
  const pathwayOrder = [
    PATHWAY_TYPES.BASIC,
    PATHWAY_TYPES.BALANCED,
    PATHWAY_TYPES.ACCELERATION
  ];

  const currentIndex = pathwayOrder.indexOf(currentPathway);
  const newIndex = pathwayOrder.indexOf(newPathway);

  // Allow if moving to adjacent pathway or staying same
  const isAdjacent = Math.abs(currentIndex - newIndex) <= 1;

  return {
    is_valid: isAdjacent,
    reason: isAdjacent 
      ? 'Pathway transition is within acceptable range'
      : 'Pathway jump too large - may indicate data inconsistency'
  };
}

module.exports = {
  determinePathway,
  generateContentTags,
  generateRecommendations,
  validatePathwayTransition
};










