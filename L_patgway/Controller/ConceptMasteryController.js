/**
 * ConceptMasteryController
 * 
 * Handles HTTP requests for concept mastery data
 */

const conceptMasteryService = require('../services/ConceptMasteryService');

/**
 * Get concept mastery for a student
 * 
 * GET /ilpg/mastery/:studentId
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function getMastery(req, res) {
  try {
    const { studentId } = req.params;

    if (!studentId) {
      return res.status(400).json({
        error: 'studentId parameter is required'
      });
    }

    const mastery = await conceptMasteryService.getConceptMastery(studentId);

    res.status(200).json({
      success: true,
      data: mastery
    });
  } catch (error) {
    console.error('[ConceptMastery Controller] Error:', error);
    res.status(500).json({
      error: 'Failed to get concept mastery',
      message: error.message
    });
  }
}

/**
 * Get mastery for a specific concept
 * 
 * GET /ilpg/mastery/:studentId/concept/:conceptName
 * 
 * @param {Object} req - Express request object
 * @param {Object} res - Express response object
 */
async function getConceptMastery(req, res) {
  try {
    const { studentId, conceptName } = req.params;

    if (!studentId || !conceptName) {
      return res.status(400).json({
        error: 'studentId and conceptName parameters are required'
      });
    }

    const mastery = await conceptMasteryService.getConceptMasteryByName(
      studentId,
      conceptName
    );

    if (!mastery) {
      return res.status(404).json({
        error: 'Concept mastery not found',
        message: `No mastery data found for concept: ${conceptName}`
      });
    }

    res.status(200).json({
      success: true,
      data: mastery
    });
  } catch (error) {
    console.error('[ConceptMastery Controller] Error:', error);
    res.status(500).json({
      error: 'Failed to get concept mastery',
      message: error.message
    });
  }
}

module.exports = {
  getMastery,
  getConceptMastery
};










