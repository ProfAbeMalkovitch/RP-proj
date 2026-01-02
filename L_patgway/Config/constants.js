/**
 * ILPG Constants Configuration
 * 
 * Defines all rule thresholds, pathway types, and configuration values
 * for the Intelligent Learning Pathway Generator.
 * 
 * Research Alignment:
 * - Rule-based pathway categorization (no AI/ML)
 * - Transparent thresholds for academic presentation
 * - Teacher-controlled content recommendations
 */

/**
 * Pathway Types
 * Three distinct learning pathways based on performance
 */
const PATHWAY_TYPES = {
  BASIC: 'basic',           // 0-49: Foundational support needed
  BALANCED: 'balanced',     // 50-74: Standard progression
  ACCELERATION: 'acceleration' // 75-100: Advanced content
};

/**
 * Performance Score Thresholds
 * 
 * Rule Logic:
 * - BASIC: Average score < 50
 *   → Student needs foundational reinforcement
 *   → Focus on core concepts and basic exercises
 * 
 * - BALANCED: 50 ≤ Average score < 75
 *   → Student progressing normally
 *   → Mix of reinforcement and new content
 * 
 * - ACCELERATION: Average score ≥ 75
 *   → Student ready for advanced material
 *   → Challenge with complex topics and extensions
 */
const SCORE_THRESHOLDS = {
  BASIC_MAX: 49,           // Maximum score for BASIC pathway
  BALANCED_MIN: 50,        // Minimum score for BALANCED pathway
  BALANCED_MAX: 74,        // Maximum score for BALANCED pathway
  ACCELERATION_MIN: 75      // Minimum score for ACCELERATION pathway
};

/**
 * Task Completion Thresholds
 * 
 * Used as secondary factor in pathway determination
 * Low completion rates may adjust pathway downward
 */
const TASK_COMPLETION_THRESHOLDS = {
  LOW: 0.5,                 // Below 50% completion
  MEDIUM: 0.7,              // 50-70% completion
  HIGH: 0.9                 // Above 70% completion
};

/**
 * Minimum Data Requirements
 * 
 * Edge case handling: What to do when insufficient data exists
 */
const MIN_REQUIREMENTS = {
  MIN_QUIZZES: 1,           // Minimum quizzes needed for pathway calculation
  MIN_TASKS: 1,             // Minimum tasks needed for consideration
  DEFAULT_SCORE: 0          // Default score when no data available
};

/**
 * Content Recommendation Tags
 * 
 * Tags used to recommend appropriate content based on pathway
 * These align with content metadata from ECESE module
 */
const CONTENT_TAGS = {
  BASIC: [
    'foundational',
    'basic-concepts',
    'step-by-step',
    'remedial',
    'practice-exercises',
    'review'
  ],
  BALANCED: [
    'standard',
    'core-content',
    'interactive',
    'examples',
    'guided-practice'
  ],
  ACCELERATION: [
    'advanced',
    'extension',
    'challenge',
    'deep-dive',
    'critical-thinking',
    'application'
  ]
};

/**
 * Pathway Update Rules
 * 
 * When to recalculate pathway:
 * - After each quiz completion
 * - After significant task completion milestone
 * - Manual trigger by teacher
 */
const UPDATE_TRIGGERS = {
  QUIZ_COMPLETION: 'quiz_completion',
  TASK_MILESTONE: 'task_milestone',
  MANUAL: 'manual',
  SCHEDULED: 'scheduled'
};

/**
 * Learning Recommendation Structure
 * 
 * Format for pathway recommendations
 */
const RECOMMENDATION_TYPES = {
  CONTENT: 'content',
  EXERCISE: 'exercise',
  REVIEW: 'review',
  ASSESSMENT: 'assessment'
};

module.exports = {
  PATHWAY_TYPES,
  SCORE_THRESHOLDS,
  TASK_COMPLETION_THRESHOLDS,
  MIN_REQUIREMENTS,
  CONTENT_TAGS,
  UPDATE_TRIGGERS,
  RECOMMENDATION_TYPES
};










