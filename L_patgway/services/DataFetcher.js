/**
 * DataFetcher Service
 * 
 * Fetches quiz results and task performance data from MongoDB
 * Integrates with existing PMSAS and activity tracking systems
 * 
 * Integration Rules:
 * - Reads from existing collections (learning_activities, engagement_logs)
 * - Does NOT modify existing data
 * - Provides clean interface for RuleEngine
 */

const { ObjectId } = require('mongodb');
const { getDatabase } = require('../config/database');

/**
 * Fetch quiz scores for a student
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {number} limit - Maximum number of recent quizzes to fetch (default: 10)
 * @returns {Promise<Array<Object>>} Array of quiz score objects
 */
async function fetchQuizScores(studentId, limit = 10) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    // Query learning_activities collection for quiz completions
    // This integrates with existing PMSAS system
    const quizzes = await db.collection('learning_activities')
      .find({
        user_id: studentOid,
        activity_type: 'quiz_complete',
        score: { $exists: true, $ne: null }
      })
      .sort({ created_at: -1 })
      .limit(limit)
      .toArray();

    return quizzes.map(quiz => ({
      quiz_id: quiz._id.toString(),
      score: quiz.score,
      date: quiz.created_at,
      metadata: quiz.metadata || {}
    }));
  } catch (error) {
    console.error('[ILPG DataFetcher] Error fetching quiz scores:', error);
    return [];
  }
}

/**
 * Calculate average quiz score
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<number>} Average score (0-100)
 */
async function calculateAverageScore(studentId) {
  const quizzes = await fetchQuizScores(studentId, 50); // Get last 50 quizzes
  
  if (quizzes.length === 0) {
    return 0;
  }

  const totalScore = quizzes.reduce((sum, quiz) => sum + (quiz.score || 0), 0);
  return Math.round((totalScore / quizzes.length) * 100) / 100;
}

/**
 * Fetch task completion data
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<Object>} Task completion statistics
 */
async function fetchTaskCompletion(studentId) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    // Query engagement_logs for task-related activities
    // This integrates with existing engagement tracking
    const taskActivities = await db.collection('engagement_logs')
      .find({
        user_id: studentOid,
        activity_type: { $in: ['lesson_complete', 'assignment_submit'] }
      })
      .toArray();

    const totalTasks = taskActivities.length;
    const completedTasks = taskActivities.filter(
      task => task.metadata?.status === 'completed' || task.points_earned > 0
    ).length;

    const completionRate = totalTasks > 0 
      ? Math.round((completedTasks / totalTasks) * 100) / 100 
      : 0;

    return {
      total_tasks: totalTasks,
      completed_tasks: completedTasks,
      completion_rate: completionRate
    };
  } catch (error) {
    console.error('[ILPG DataFetcher] Error fetching task completion:', error);
    return {
      total_tasks: 0,
      completed_tasks: 0,
      completion_rate: 0
    };
  }
}

/**
 * Get recent quiz attempts count
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {number} days - Number of days to look back (default: 7)
 * @returns {Promise<number>} Number of quiz attempts in recent period
 */
async function getRecentAttempts(studentId, days = 7) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);

    const count = await db.collection('learning_activities')
      .countDocuments({
        user_id: studentOid,
        activity_type: 'quiz_complete',
        created_at: { $gte: cutoffDate }
      });

    return count;
  } catch (error) {
    console.error('[ILPG DataFetcher] Error fetching recent attempts:', error);
    return 0;
  }
}

/**
 * Get comprehensive performance data for a student
 * 
 * Combines quiz scores and task completion for pathway calculation
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<Object>} Complete performance data
 */
async function getStudentPerformanceData(studentId) {
  const [averageScore, taskData, recentAttempts, quizScores] = await Promise.all([
    calculateAverageScore(studentId),
    fetchTaskCompletion(studentId),
    getRecentAttempts(studentId, 7),
    fetchQuizScores(studentId, 10)
  ]);

  const lastQuizDate = quizScores.length > 0 
    ? quizScores[0].date 
    : null;

  return {
    average_score: averageScore,
    task_completion_rate: taskData.completion_rate,
    total_quizzes: quizScores.length,
    total_tasks: taskData.total_tasks,
    completed_tasks: taskData.completed_tasks,
    recent_attempts: recentAttempts,
    recent_scores: quizScores.slice(0, 5).map(q => q.score),
    last_quiz_date: lastQuizDate
  };
}

module.exports = {
  fetchQuizScores,
  calculateAverageScore,
  fetchTaskCompletion,
  getRecentAttempts,
  getStudentPerformanceData
};










