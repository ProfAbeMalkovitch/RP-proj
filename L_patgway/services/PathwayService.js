/**
 * PathwayService
 * 
 * High-level service for pathway management
 * Orchestrates DataFetcher and RuleEngine
 * Handles database persistence
 */

const { ObjectId } = require('mongodb');
const { getDatabase } = require('../config/database');
const { LearningPath, COLLECTION_NAME } = require('../models/LearningPath');
const { getStudentPerformanceData } = require('./DataFetcher');
const {
  determinePathway,
  generateContentTags,
  generateRecommendations,
  validatePathwayTransition
} = require('./RuleEngine');
const { UPDATE_TRIGGERS } = require('../config/constants');

/**
 * Generate or update learning pathway for a student
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {string} trigger - What triggered this calculation (default: 'manual')
 * @returns {Promise<LearningPath>} Generated or updated pathway
 */
async function generatePathway(studentId, trigger = UPDATE_TRIGGERS.MANUAL) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    // Fetch current performance data
    const performanceData = await getStudentPerformanceData(studentId);

    // Determine pathway using rule engine
    const pathwayResult = determinePathway(performanceData);

    // Generate content tags
    const recommendedTags = generateContentTags(pathwayResult.pathway_type);

    // Get existing pathway (if any)
    const existingPathwayDoc = await db.collection(COLLECTION_NAME)
      .findOne({
        student_id: studentOid,
        is_active: true
      });

    let previousPathway = null;
    let pathwayHistory = [];

    if (existingPathwayDoc) {
      const existingPathway = LearningPath.fromDocument(existingPathwayDoc);
      previousPathway = existingPathway.pathway_type;
      pathwayHistory = existingPathway.pathway_history || [];

      // Validate transition
      const validation = validatePathwayTransition(
        previousPathway,
        pathwayResult.pathway_type,
        performanceData
      );

      if (!validation.is_valid) {
        console.warn(`[ILPG] Pathway transition validation failed: ${validation.reason}`);
      }

      // Add history entry if pathway changed
      if (previousPathway !== pathwayResult.pathway_type) {
        pathwayHistory.push({
          from: previousPathway,
          to: pathwayResult.pathway_type,
          reason: pathwayResult.reasoning,
          changed_at: new Date()
        });
      }

      // Deactivate old pathway
      await db.collection(COLLECTION_NAME)
        .updateOne(
          { _id: existingPathway._id },
          { $set: { is_active: false } }
        );
    }

    // Create new pathway
    const newPathway = new LearningPath({
      student_id: studentId,
      pathway_type: pathwayResult.pathway_type,
      average_score: performanceData.average_score,
      task_completion_rate: performanceData.task_completion_rate,
      recommended_tags: recommendedTags,
      performance_metrics: {
        total_quizzes: performanceData.total_quizzes,
        total_tasks: performanceData.total_tasks,
        completed_tasks: performanceData.completed_tasks,
        recent_attempts: performanceData.recent_attempts,
        recent_scores: performanceData.recent_scores,
        last_quiz_date: performanceData.last_quiz_date
      },
      calculated_at: new Date(),
      trigger,
      previous_pathway: previousPathway,
      pathway_history: pathwayHistory,
      is_active: true
    });

    // Save to database
    await db.collection(COLLECTION_NAME)
      .insertOne(newPathway.toDocument());

    return newPathway;
  } catch (error) {
    console.error('[ILPG PathwayService] Error generating pathway:', error);
    throw error;
  }
}

/**
 * Recalculate pathway for a student
 * 
 * Alias for generatePathway with explicit trigger
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {string} trigger - Trigger type (default: 'manual')
 * @returns {Promise<LearningPath>} Recalculated pathway
 */
async function recalculatePathway(studentId, trigger = UPDATE_TRIGGERS.MANUAL) {
  return generatePathway(studentId, trigger);
}

/**
 * Get current active pathway for a student
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<LearningPath|null>} Current pathway or null if not found
 */
async function getCurrentPathway(studentId) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    const pathwayDoc = await db.collection(COLLECTION_NAME)
      .findOne({
        student_id: studentOid,
        is_active: true
      });

    if (!pathwayDoc) {
      return null;
    }

    return LearningPath.fromDocument(pathwayDoc);
  } catch (error) {
    console.error('[ILPG PathwayService] Error getting current pathway:', error);
    throw error;
  }
}

/**
 * Get pathway history for a student
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {number} limit - Maximum number of pathways to return
 * @returns {Promise<Array<LearningPath>>} Pathway history
 */
async function getPathwayHistory(studentId, limit = 10) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    const pathwayDocs = await db.collection(COLLECTION_NAME)
      .find({ student_id: studentOid })
      .sort({ calculated_at: -1 })
      .limit(limit)
      .toArray();

    return pathwayDocs.map(doc => LearningPath.fromDocument(doc));
  } catch (error) {
    console.error('[ILPG PathwayService] Error getting pathway history:', error);
    throw error;
  }
}

/**
 * Evaluate student and return pathway recommendation
 * 
 * This is the main entry point for pathway evaluation
 * Can be called after quiz completion or task milestones
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {string} trigger - Trigger type
 * @returns {Promise<Object>} Pathway evaluation result with recommendations
 */
async function evaluateStudent(studentId, trigger = UPDATE_TRIGGERS.MANUAL) {
  try {
    // Generate or update pathway
    const pathway = await generatePathway(studentId, trigger);

    // Generate recommendations
    const performanceData = await getStudentPerformanceData(studentId);
    const recommendations = generateRecommendations(
      pathway.pathway_type,
      performanceData
    );

    return {
      pathway: pathway.toResponse(),
      recommendations,
      generated_at: new Date().toISOString()
    };
  } catch (error) {
    console.error('[ILPG PathwayService] Error evaluating student:', error);
    throw error;
  }
}

module.exports = {
  generatePathway,
  recalculatePathway,
  getCurrentPathway,
  getPathwayHistory,
  evaluateStudent
};










