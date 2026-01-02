/**
 * LearningPath Model
 * 
 * MongoDB schema and model for storing student learning pathways
 * 
 * Research Alignment:
 * - Stores pathway type (BASIC/BALANCED/ACCELERATION)
 * - Tracks performance metrics used for pathway calculation
 * - Maintains history of pathway changes for research analysis
 * - Links to recommended content tags
 */

const { ObjectId } = require('mongodb');
const { PATHWAY_TYPES } = require('../config/constants');

const COLLECTION_NAME = 'learning_paths';

/**
 * LearningPath Class
 * 
 * Represents a student's current learning pathway and recommendations
 */
class LearningPath {
  /**
   * Create a new LearningPath instance
   * 
   * @param {Object} data - Pathway data
   * @param {string} data.student_id - Student user ID (MongoDB ObjectId string)
   * @param {string} data.pathway_type - Pathway type (basic/balanced/acceleration)
   * @param {number} data.average_score - Average quiz score used for calculation
   * @param {number} data.task_completion_rate - Task completion percentage
   * @param {Array<string>} data.recommended_tags - Content tags for recommendations
   * @param {Object} data.performance_metrics - Detailed performance data
   * @param {Date} data.calculated_at - When pathway was calculated
   * @param {string} data.trigger - What triggered this pathway calculation
   * @param {ObjectId} data._id - MongoDB ObjectId (optional)
   */
  constructor(data) {
    this._id = data._id || new ObjectId();
    this.student_id = new ObjectId(data.student_id);
    this.pathway_type = data.pathway_type || PATHWAY_TYPES.BALANCED;
    this.average_score = data.average_score || 0;
    this.task_completion_rate = data.task_completion_rate || 0;
    this.recommended_tags = data.recommended_tags || [];
    this.performance_metrics = data.performance_metrics || {
      total_quizzes: 0,
      total_tasks: 0,
      completed_tasks: 0,
      recent_scores: [],
      last_quiz_date: null
    };
    this.calculated_at = data.calculated_at || new Date();
    this.trigger = data.trigger || 'manual';
    this.previous_pathway = data.previous_pathway || null;
    this.pathway_history = data.pathway_history || [];
    this.is_active = data.is_active !== undefined ? data.is_active : true;
  }

  /**
   * Convert to MongoDB document format
   * 
   * @returns {Object} MongoDB document
   */
  toDocument() {
    return {
      _id: this._id,
      student_id: this.student_id,
      pathway_type: this.pathway_type,
      average_score: this.average_score,
      task_completion_rate: this.task_completion_rate,
      recommended_tags: this.recommended_tags,
      performance_metrics: this.performance_metrics,
      calculated_at: this.calculated_at,
      trigger: this.trigger,
      previous_pathway: this.previous_pathway,
      pathway_history: this.pathway_history,
      is_active: this.is_active
    };
  }

  /**
   * Convert to API response format
   * 
   * @returns {Object} API response object
   */
  toResponse() {
    return {
      id: this._id.toString(),
      student_id: this.student_id.toString(),
      pathway_type: this.pathway_type,
      average_score: this.average_score,
      task_completion_rate: this.task_completion_rate,
      recommended_tags: this.recommended_tags,
      performance_metrics: {
        ...this.performance_metrics,
        last_quiz_date: this.performance_metrics.last_quiz_date 
          ? this.performance_metrics.last_quiz_date.toISOString() 
          : null
      },
      calculated_at: this.calculated_at.toISOString(),
      trigger: this.trigger,
      previous_pathway: this.previous_pathway,
      pathway_changes_count: this.pathway_history.length,
      is_active: this.is_active
    };
  }

  /**
   * Create LearningPath from MongoDB document
   * 
   * @param {Object} doc - MongoDB document
   * @returns {LearningPath} LearningPath instance
   */
  static fromDocument(doc) {
    if (!doc) return null;

    // Convert dates if they're strings
    const calculated_at = doc.calculated_at instanceof Date 
      ? doc.calculated_at 
      : new Date(doc.calculated_at);

    const last_quiz_date = doc.performance_metrics?.last_quiz_date
      ? (doc.performance_metrics.last_quiz_date instanceof Date
          ? doc.performance_metrics.last_quiz_date
          : new Date(doc.performance_metrics.last_quiz_date))
      : null;

    return new LearningPath({
      _id: doc._id,
      student_id: doc.student_id.toString(),
      pathway_type: doc.pathway_type,
      average_score: doc.average_score,
      task_completion_rate: doc.task_completion_rate,
      recommended_tags: doc.recommended_tags || [],
      performance_metrics: {
        ...doc.performance_metrics,
        last_quiz_date
      },
      calculated_at,
      trigger: doc.trigger,
      previous_pathway: doc.previous_pathway,
      pathway_history: doc.pathway_history || [],
      is_active: doc.is_active !== undefined ? doc.is_active : true
    });
  }

  /**
   * Add pathway change to history
   * 
   * @param {string} new_pathway - New pathway type
   * @param {string} reason - Reason for change
   */
  addHistoryEntry(new_pathway, reason) {
    this.pathway_history.push({
      from: this.previous_pathway || this.pathway_type,
      to: new_pathway,
      reason,
      changed_at: new Date()
    });
  }
}

module.exports = {
  LearningPath,
  COLLECTION_NAME
};










