/**
 * Pathway Routes
 * 
 * Defines REST API endpoints for ILPG
 * 
 * Endpoints:
 * - POST /ilpg/evaluate - Generate/evaluate pathway
 * - POST /ilpg/recalculate - Recalculate pathway
 * - GET /ilpg/:studentId - Get current pathway
 * - GET /ilpg/:studentId/history - Get pathway history
 */

const express = require('express');
const router = express.Router();
const pathwayController = require('../controllers/PathwayController');
const conceptMasteryController = require('../controllers/ConceptMasteryController');

/**
 * POST /ilpg/evaluate
 * 
 * Evaluate student and generate/update learning pathway
 * 
 * Request Body:
 * {
 *   "student_id": "string (MongoDB ObjectId)",
 *   "trigger": "optional string (quiz_completion|task_milestone|manual)"
 * }
 * 
 * Response:
 * {
 *   "success": true,
 *   "data": {
 *     "pathway": { ... },
 *     "recommendations": [ ... ],
 *     "generated_at": "ISO date string"
 *   }
 * }
 */
router.post('/evaluate', pathwayController.generatePath);

/**
 * POST /ilpg/recalculate
 * 
 * Force recalculation of pathway
 * 
 * Request Body:
 * {
 *   "student_id": "string (MongoDB ObjectId)"
 * }
 */
router.post('/recalculate', pathwayController.recalculatePath);

/**
 * GET /ilpg/mastery/:studentId
 * 
 * Get concept mastery for a student
 */
router.get('/mastery/:studentId', conceptMasteryController.getMastery);

/**
 * GET /ilpg/mastery/:studentId/concept/:conceptName
 * 
 * Get mastery for a specific concept
 */
router.get('/mastery/:studentId/concept/:conceptName', conceptMasteryController.getConceptMastery);

/**
 * GET /ilpg/:studentId
 * 
 * Get current active pathway for a student
 * 
 * Response:
 * {
 *   "success": true,
 *   "data": {
 *     "pathway": { ... }
 *   }
 * }
 */
router.get('/:studentId', pathwayController.getCurrentPath);

/**
 * GET /ilpg/:studentId/history
 * 
 * Get pathway history for a student
 * 
 * Query Parameters:
 * - limit: number (default: 10)
 * 
 * Response:
 * {
 *   "success": true,
 *   "data": {
 *     "pathways": [ ... ],
 *     "count": number
 *   }
 * }
 */
router.get('/:studentId/history', pathwayController.getPathwayHistory);

module.exports = router;

