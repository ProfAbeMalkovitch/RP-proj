/**
 * PathwayController
 * 
 * Handles HTTP request/response logic
 * Validates input and formats output
 * Delegates business logic to PathwayService
 */

const pathwayService = require('../services/PathwayService');
const { UPDATE_TRIGGERS } = require('../config/constants');

/**
 * Generate pathway for a student
 * 
 * POST /ilpg/evaluate
 * Body: { student_id: string, trigger?: string }
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function generatePath(req, res) {
  try {
    const { student_id, trigger } = req.body;

    if (!student_id) {
      return res.status(400).json({
        error: 'student_id is required',
        message: 'Please provide a valid student ID'
      });
    }

    const validTrigger = trigger || UPDATE_TRIGGERS.MANUAL;
    const result = await pathwayService.evaluateStudent(student_id, validTrigger);

    res.status(200).json({
      success: true,
      data: result
    });
  } catch (error) {
    console.error('[ILPG Controller] Error generating pathway:', error);
    res.status(500).json({
      error: 'Failed to generate pathway',
      message: error.message
    });
  }
}

/**
 * Recalculate pathway for a student
 * 
 * POST /ilpg/recalculate
 * Body: { student_id: string }
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function recalculatePath(req, res) {
  try {
    const { student_id } = req.body;

    if (!student_id) {
      return res.status(400).json({
        error: 'student_id is required'
      });
    }

    const result = await pathwayService.evaluateStudent(
      student_id,
      UPDATE_TRIGGERS.MANUAL
    );

    res.status(200).json({
      success: true,
      data: result,
      message: 'Pathway recalculated successfully'
    });
  } catch (error) {
    console.error('[ILPG Controller] Error recalculating pathway:', error);
    res.status(500).json({
      error: 'Failed to recalculate pathway',
      message: error.message
    });
  }
}

/**
 * Get current pathway for a student
 * 
 * GET /ilpg/:studentId
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function getCurrentPath(req, res) {
  try {
    const { studentId } = req.params;

    if (!studentId) {
      return res.status(400).json({
        error: 'studentId parameter is required'
      });
    }

    const pathway = await pathwayService.getCurrentPathway(studentId);

    if (!pathway) {
      return res.status(404).json({
        error: 'Pathway not found',
        message: 'No active pathway found for this student. Generate one first.'
      });
    }

    res.status(200).json({
      success: true,
      data: {
        pathway: pathway.toResponse()
      }
    });
  } catch (error) {
    console.error('[ILPG Controller] Error getting current pathway:', error);
    res.status(500).json({
      error: 'Failed to get pathway',
      message: error.message
    });
  }
}

/**
 * Get pathway history for a student
 * 
 * GET /ilpg/:studentId/history
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function getPathwayHistory(req, res) {
  try {
    const { studentId } = req.params;
    const limit = parseInt(req.query.limit) || 10;

    if (!studentId) {
      return res.status(400).json({
        error: 'studentId parameter is required'
      });
    }

    const history = await pathwayService.getPathwayHistory(studentId, limit);

    res.status(200).json({
      success: true,
      data: {
        pathways: history.map(p => p.toResponse()),
        count: history.length
      }
    });
  } catch (error) {
    console.error('[ILPG Controller] Error getting pathway history:', error);
    res.status(500).json({
      error: 'Failed to get pathway history',
      message: error.message
    });
  }
}

module.exports = {
  generatePath,
  recalculatePath,
  getCurrentPath,
  getPathwayHistory
};










