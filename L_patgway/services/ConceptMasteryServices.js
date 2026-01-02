/**
 * ConceptMasteryService
 * 
 * Calculates and tracks concept mastery for students based on quiz performance
 * 
 * Rule-based calculation:
 * - Extracts concepts from quiz metadata
 * - Calculates mastery percentage per concept
 * - Tracks mastery over time
 */

const { ObjectId } = require('mongodb');
const { getDatabase } = require('../config/database');

const COLLECTION_NAME = 'concept_mastery';

/**
 * Extract concepts from activity data
 * 
 * Supports multiple formats:
 * - metadata.concepts (array)
 * - metadata.concept (string)
 * - metadata.topic (string)
 * - lesson_id (ObjectId)
 * - course_id (ObjectId)
 * - Structured content: topic_name, unit_name, module_name
 * 
 * @param {Object} activity - Activity/Content object
 * @param {string} sourceType - Type of source (quiz, lesson, assignment, content)
 * @returns {Array<string>} Array of concept names
 */
function extractConcepts(activity, sourceType = 'quiz') {
  const concepts = [];
  
  // Method 1: Explicit concepts in metadata
  if (activity.metadata?.concepts && Array.isArray(activity.metadata.concepts)) {
    concepts.push(...activity.metadata.concepts);
  } else if (activity.metadata?.concept) {
    concepts.push(activity.metadata.concept);
  }
  
  // Method 2: Topic from metadata
  if (activity.metadata?.topic) {
    concepts.push(activity.metadata.topic);
  }
  
  // Method 3: Structured content fields (from ECESE)
  if (activity.topic_name) {
    concepts.push(activity.topic_name);
  }
  if (activity.unit_name) {
    concepts.push(activity.unit_name);
  }
  if (activity.module_name) {
    concepts.push(activity.module_name);
  }
  
  // Method 4: Lesson/Course IDs (as fallback)
  if (activity.lesson_id) {
    concepts.push(`lesson_${activity.lesson_id.toString()}`);
  }
  if (activity.course_id) {
    concepts.push(`course_${activity.course_id.toString()}`);
  }
  
  // Method 5: Quiz ID as concept identifier (last resort)
  if (sourceType === 'quiz' && activity.quiz_id && concepts.length === 0) {
    concepts.push(`quiz_${activity.quiz_id.toString()}`);
  }
  
  // Remove duplicates and empty strings
  return [...new Set(concepts.filter(c => c && c.trim()))];
}

/**
 * Calculate concept mastery from ALL content sources
 * 
 * Extracts concepts from:
 * 1. Quiz completions (with scores)
 * 2. Structured content (topics, units, modules from ECESE)
 * 3. Lesson completions
 * 4. Assignment submissions
 * 5. Any activity with concept metadata
 * 
 * Rule Logic:
 * - For each concept, find all activities related to that concept
 * - Calculate average score for that concept (from quizzes)
 * - Track engagement (from lessons, assignments, etc.)
 * - Mastery = weighted average of quiz scores + engagement
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<Array<Object>>} Array of concept mastery objects
 */
async function calculateConceptMastery(studentId) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    // 1. Fetch all quiz completions with concept data
    const quizzes = await db.collection('learning_activities')
      .find({
        user_id: studentOid,
        activity_type: 'quiz_complete',
        score: { $exists: true, $ne: null }
      })
      .toArray();

    // 2. Fetch all lesson completions
    const lessons = await db.collection('learning_activities')
      .find({
        user_id: studentOid,
        activity_type: 'lesson_complete'
      })
      .toArray();

    // 3. Fetch all assignment submissions
    const assignments = await db.collection('engagement_logs')
      .find({
        user_id: studentOid,
        activity_type: { $in: ['assignment_submit', 'lesson_complete'] }
      })
      .toArray();

    // 4. Fetch structured content the student has accessed
    // Get enrollments first
    const enrollments = await db.collection('enrollments')
      .find({ student_id: studentOid })
      .toArray();

    const moduleNames = enrollments.map(e => e.module_name);
    
    // Get structured content from enrolled modules
    const structuredContents = moduleNames.length > 0
      ? await db.collection('structured_contents')
          .find({
            module_name: { $in: moduleNames },
            approved: true,
            status: { $in: ['approved', 'published'] }
          })
          .toArray()
      : [];

    // Group all activities by concept
    const conceptScores = {};
    const conceptEngagement = {};

    // Process quizzes (with scores)
    quizzes.forEach(quiz => {
      const concepts = extractConcepts(quiz, 'quiz');
      
      concepts.forEach(concept => {
        if (!conceptScores[concept]) {
          conceptScores[concept] = {
            concept_name: concept,
            scores: [],
            total_attempts: 0,
            last_attempt: null,
            source: 'quiz'
          };
        }
        
        conceptScores[concept].scores.push(quiz.score);
        conceptScores[concept].total_attempts++;
        
        if (!conceptScores[concept].last_attempt || 
            quiz.created_at > conceptScores[concept].last_attempt) {
          conceptScores[concept].last_attempt = quiz.created_at;
        }
      });
    });

    // Process lessons (engagement tracking)
    lessons.forEach(lesson => {
      const concepts = extractConcepts(lesson, 'lesson');
      
      concepts.forEach(concept => {
        if (!conceptEngagement[concept]) {
          conceptEngagement[concept] = {
            concept_name: concept,
            engagement_count: 0,
            last_engagement: null,
            sources: []
          };
        }
        
        conceptEngagement[concept].engagement_count++;
        conceptEngagement[concept].sources.push('lesson');
        
        if (!conceptEngagement[concept].last_engagement || 
            lesson.created_at > conceptEngagement[concept].last_engagement) {
          conceptEngagement[concept].last_engagement = lesson.created_at;
        }
      });
    });

    // Process assignments
    assignments.forEach(assignment => {
      const concepts = extractConcepts(assignment, 'assignment');
      
      concepts.forEach(concept => {
        if (!conceptEngagement[concept]) {
          conceptEngagement[concept] = {
            concept_name: concept,
            engagement_count: 0,
            last_engagement: null,
            sources: []
          };
        }
        
        conceptEngagement[concept].engagement_count++;
        conceptEngagement[concept].sources.push('assignment');
        
        if (!conceptEngagement[concept].last_engagement || 
            assignment.created_at > conceptEngagement[concept].last_engagement) {
          conceptEngagement[concept].last_engagement = assignment.created_at;
        }
      });
    });

    // Process structured content (all topics/units/modules)
    structuredContents.forEach(content => {
      // Extract concepts from structured content
      const concepts = [];
      
      // Use topic_name as primary concept
      if (content.topic_name) {
        concepts.push(content.topic_name);
      }
      
      // Use unit_name as secondary concept
      if (content.unit_name) {
        concepts.push(content.unit_name);
      }
      
      // Use module_name as tertiary concept
      if (content.module_name) {
        concepts.push(content.module_name);
      }

      concepts.forEach(concept => {
        if (!conceptEngagement[concept]) {
          conceptEngagement[concept] = {
            concept_name: concept,
            engagement_count: 0,
            last_engagement: null,
            sources: []
          };
        }
        
        // Don't double-count, just mark as available content
        if (!conceptEngagement[concept].sources.includes('content')) {
          conceptEngagement[concept].sources.push('content');
        }
      });
    });

    // Merge quiz scores and engagement data
    const allConcepts = new Set([
      ...Object.keys(conceptScores),
      ...Object.keys(conceptEngagement)
    ]);

    // Calculate mastery for each concept (combining scores and engagement)
    const masteryData = Array.from(allConcepts).map(conceptName => {
      const scoreData = conceptScores[conceptName];
      const engagementData = conceptEngagement[conceptName];

      // Calculate average score from quizzes
      const averageScore = scoreData && scoreData.scores.length > 0
        ? scoreData.scores.reduce((sum, score) => sum + score, 0) / scoreData.scores.length
        : null;

      // If no quiz scores, use engagement as indicator (lower weight)
      let masteryPercentage = 0;
      if (averageScore !== null) {
        // Primary: Use quiz scores
        masteryPercentage = averageScore;
      } else if (engagementData && engagementData.engagement_count > 0) {
        // Secondary: Estimate from engagement (max 50% without quiz)
        masteryPercentage = Math.min(50, engagementData.engagement_count * 10);
      }

      // Determine mastery level
      let masteryLevel = 'beginner';
      if (masteryPercentage >= 90) masteryLevel = 'mastered';
      else if (masteryPercentage >= 75) masteryLevel = 'proficient';
      else if (masteryPercentage >= 60) masteryLevel = 'developing';
      else if (masteryPercentage >= 40) masteryLevel = 'beginner';
      else masteryLevel = 'needs_improvement';

      return {
        concept_name: conceptName,
        mastery_percentage: Math.round(masteryPercentage * 100) / 100,
        mastery_level: masteryLevel,
        total_attempts: scoreData?.total_attempts || 0,
        engagement_count: engagementData?.engagement_count || 0,
        last_attempt: scoreData?.last_attempt || engagementData?.last_engagement || null,
        recent_scores: scoreData?.scores.slice(-5) || [],
        sources: [
          ...(scoreData ? ['quiz'] : []),
          ...(engagementData?.sources || [])
        ].filter((v, i, a) => a.indexOf(v) === i) // Remove duplicates
      };
    });

    // Sort by mastery percentage (descending)
    masteryData.sort((a, b) => b.mastery_percentage - a.mastery_percentage);

    return masteryData;
  } catch (error) {
    console.error('[ConceptMastery] Error calculating mastery:', error);
    return [];
  }
}

/**
 * Get concept mastery for a student
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @returns {Promise<Object>} Concept mastery summary
 */
async function getConceptMastery(studentId) {
  try {
    const db = await getDatabase();
    const studentOid = new ObjectId(studentId);

    // Calculate current mastery
    const masteryData = await calculateConceptMastery(studentId);

    // Get or create mastery record
    const existingRecord = await db.collection(COLLECTION_NAME)
      .findOne({ student_id: studentOid });

    const masterySummary = {
      student_id: studentId,
      concepts: masteryData,
      total_concepts: masteryData.length,
      mastered_count: masteryData.filter(c => c.mastery_level === 'mastered').length,
      proficient_count: masteryData.filter(c => c.mastery_level === 'proficient').length,
      developing_count: masteryData.filter(c => c.mastery_level === 'developing').length,
      beginner_count: masteryData.filter(c => c.mastery_level === 'beginner').length,
      needs_improvement_count: masteryData.filter(c => c.mastery_level === 'needs_improvement').length,
      average_mastery: masteryData.length > 0
        ? Math.round((masteryData.reduce((sum, c) => sum + c.mastery_percentage, 0) / masteryData.length) * 100) / 100
        : 0,
      last_updated: new Date()
    };

    // Save to database
    if (existingRecord) {
      await db.collection(COLLECTION_NAME)
        .updateOne(
          { student_id: studentOid },
          { $set: masterySummary }
        );
    } else {
      await db.collection(COLLECTION_NAME)
        .insertOne({
          ...masterySummary,
          created_at: new Date()
        });
    }

    return masterySummary;
  } catch (error) {
    console.error('[ConceptMastery] Error getting mastery:', error);
    throw error;
  }
}

/**
 * Get mastery for a specific concept
 * 
 * @param {string} studentId - Student MongoDB ObjectId string
 * @param {string} conceptName - Concept name
 * @returns {Promise<Object|null>} Concept mastery or null
 */
async function getConceptMasteryByName(studentId, conceptName) {
  try {
    const masteryData = await getConceptMastery(studentId);
    const concept = masteryData.concepts.find(
      c => c.concept_name.toLowerCase() === conceptName.toLowerCase()
    );
    return concept || null;
  } catch (error) {
    console.error('[ConceptMastery] Error getting concept mastery:', error);
    return null;
  }
}

module.exports = {
  calculateConceptMastery,
  getConceptMastery,
  getConceptMasteryByName
};

