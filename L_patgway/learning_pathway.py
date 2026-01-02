"""
Learning Pathway Module.

Rule-based learning pathway generation for students.
Categorizes students into BASIC, BALANCED, or ACCELERATION pathways.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_database


class PathwayError(Exception):
    """Base exception for pathway errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class LearningPathwayService:
    """Main learning pathway service."""
    
    # Pathway types
    PATHWAY_BASIC = 'basic'
    PATHWAY_BALANCED = 'balanced'
    PATHWAY_ACCELERATION = 'acceleration'
    
    # Score thresholds
    BASIC_MAX = 49
    BALANCED_MIN = 50
    BALANCED_MAX = 74
    ACCELERATION_MIN = 75
    
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = get_database()
        return self._db
    
    def get_student_performance(self, student_id: str) -> Dict:
        """Get student performance data for pathway calculation."""
        if self.db is None:
            return {
                'average_score': 0,
                'task_completion_rate': 0,
                'total_quizzes': 0,
                'total_tasks': 0,
                'completed_tasks': 0,
                'recent_attempts': 0,
                'last_quiz_date': None
            }
        
        try:
            student_oid = ObjectId(student_id)
            
            # Get quiz scores
            quizzes = list(self.db.learning_activities.find({
                'user_id': student_oid,
                'activity_type': 'quiz_complete',
                'score': {'$exists': True, '$ne': None}
            }))
            
            # Calculate average score
            average_score = 0
            if quizzes:
                total_score = sum(q.get('score', 0) for q in quizzes)
                average_score = (total_score / len(quizzes)) * 100
            
            # Get task completion
            tasks = list(self.db.engagement_logs.find({
                'user_id': student_oid,
                'activity_type': {'$in': ['lesson_complete', 'assignment_submit']}
            }))
            
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t.get('metadata', {}).get('status') == 'completed' or t.get('points_earned', 0) > 0])
            task_completion_rate = (completed_tasks / total_tasks) if total_tasks > 0 else 0
            
            # Recent attempts (last 7 days)
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=7)
            recent_attempts = len([q for q in quizzes if q.get('created_at', datetime.utcnow()) >= cutoff_date])
            
            # Get last quiz date
            last_quiz_date = None
            if quizzes:
                quiz_dates = [q.get('created_at') for q in quizzes if q.get('created_at')]
                if quiz_dates:
                    last_quiz_date = max(quiz_dates)
            
            return {
                'average_score': round(average_score, 2),
                'task_completion_rate': round(task_completion_rate, 2),
                'total_quizzes': len(quizzes),
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'recent_attempts': recent_attempts,
                'last_quiz_date': last_quiz_date.isoformat() if last_quiz_date else None
            }
        except Exception as e:
            print(f'[Pathway] Error getting performance: {e}')
            return {
                'average_score': 0,
                'task_completion_rate': 0,
                'total_quizzes': 0,
                'total_tasks': 0,
                'completed_tasks': 0,
                'recent_attempts': 0,
                'last_quiz_date': None
            }
    
    def determine_pathway(self, student_id: str) -> Dict:
        """
        Determine learning pathway for a student.
        
        Rule Logic:
        - BASIC: average_score < 50
        - BALANCED: 50 ≤ average_score < 75
        - ACCELERATION: average_score ≥ 75
        
        Secondary factor: Task completion rate may adjust pathway downward.
        """
        performance = self.get_student_performance(student_id)
        average_score = performance['average_score']
        task_completion_rate = performance['task_completion_rate']
        total_quizzes = performance['total_quizzes']
        
        # Edge case: No quiz data
        if total_quizzes < 1:
            return {
                'pathway_type': self.PATHWAY_BALANCED,
                'pathway_label': 'Balanced',
                'reasoning': 'Insufficient quiz data - defaulting to BALANCED pathway',
                'confidence': 'low',
                'performance': performance
            }
        
        # Primary rule: Average score classification
        if average_score < self.BALANCED_MIN:
            pathway_type = self.PATHWAY_BASIC
            pathway_label = 'Basic'
            reasoning = f'Average score of {average_score}% indicates need for foundational support'
        elif average_score < self.ACCELERATION_MIN:
            pathway_type = self.PATHWAY_BALANCED
            pathway_label = 'Balanced'
            reasoning = f'Average score of {average_score}% indicates normal progression'
        else:
            pathway_type = self.PATHWAY_ACCELERATION
            pathway_label = 'Acceleration'
            reasoning = f'Average score of {average_score}% indicates readiness for advanced content'
        
        # Secondary rule: Task completion adjustment
        if (task_completion_rate < 0.5 and average_score < 60 and 
            pathway_type != self.PATHWAY_BASIC):
            pathway_type = self.PATHWAY_BASIC
            pathway_label = 'Basic'
            reasoning += f'. Low task completion rate ({task_completion_rate*100:.0f}%) indicates need for additional support'
        
        return {
            'pathway_type': pathway_type,
            'pathway_label': pathway_label,
            'reasoning': reasoning,
            'confidence': 'high',
            'performance': performance
        }
    
    def get_student_pathway(self, student_id: str) -> Dict:
        """Get current pathway for a student."""
        try:
            pathway = self.determine_pathway(student_id)
            performance = pathway.get('performance', {})
            
            # Flatten the pathway data for frontend compatibility
            flattened_pathway = {
                'pathway_type': pathway.get('pathway_type'),
                'pathway_label': pathway.get('pathway_label'),
                'reasoning': pathway.get('reasoning'),
                'confidence': pathway.get('confidence'),
                # Flatten performance fields to top level for frontend
                'average_score': performance.get('average_score', 0),
                'task_completion_rate': performance.get('task_completion_rate', 0),
                'total_quizzes': performance.get('total_quizzes', 0),
                'total_tasks': performance.get('total_tasks', 0),
                'completed_tasks': performance.get('completed_tasks', 0),
                'recent_attempts': performance.get('recent_attempts', 0),
                'last_quiz_date': performance.get('last_quiz_date'),
                # Keep performance object for backward compatibility
                'performance': performance
            }
            
            return {
                'success': True,
                'data': flattened_pathway
            }
        except Exception as e:
            print(f'[Pathway] Error getting pathway: {e}')
            raise PathwayError(f'Failed to get pathway: {str(e)}', 500)


# Global service instance
learning_pathway_service = LearningPathwayService()

