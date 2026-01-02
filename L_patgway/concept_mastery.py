"""
Concept Mastery Module.

Calculates and tracks concept mastery for students based on performance
across all content types (quizzes, lessons, assignments, structured content).
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_database


class ConceptMasteryError(Exception):
    """Base exception for concept mastery errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ConceptMasteryService:
    """Main concept mastery service."""
    
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = get_database()
        return self._db
    
    def extract_concepts(self, activity: Dict, source_type: str = 'quiz') -> List[str]:
        """
        Extract concepts from activity data.
        
        Supports multiple formats:
        - metadata.concepts (array)
        - metadata.concept (string)
        - metadata.topic (string)
        - Structured content: topic_name, unit_name, module_name
        - lesson_id, course_id (fallback)
        """
        concepts = []
        
        # Method 1: Explicit concepts in metadata
        if activity.get('metadata', {}).get('concepts') and isinstance(activity['metadata']['concepts'], list):
            concepts.extend(activity['metadata']['concepts'])
        elif activity.get('metadata', {}).get('concept'):
            concepts.append(activity['metadata']['concept'])
        
        # Method 2: Topic from metadata
        if activity.get('metadata', {}).get('topic'):
            concepts.append(activity['metadata']['topic'])
        
        # Method 3: Structured content fields (from ECESE)
        if activity.get('topic_name'):
            concepts.append(activity['topic_name'])
        if activity.get('unit_name'):
            concepts.append(activity['unit_name'])
        if activity.get('module_name'):
            concepts.append(activity['module_name'])
        
        # Method 4: Lesson/Course IDs (as fallback)
        if activity.get('lesson_id'):
            concepts.append(f"lesson_{str(activity['lesson_id'])}")
        if activity.get('course_id'):
            concepts.append(f"course_{str(activity['course_id'])}")
        
        # Method 5: Quiz ID as concept identifier (last resort)
        if source_type == 'quiz' and activity.get('quiz_id') and not concepts:
            concepts.append(f"quiz_{str(activity['quiz_id'])}")
        
        # Remove duplicates and empty strings
        return list(set([c for c in concepts if c and c.strip()]))
    
    def calculate_concept_mastery(self, student_id: str) -> List[Dict]:
        """
        Calculate concept mastery from ALL content sources.
        
        Extracts concepts from:
        1. Quiz completions (with scores)
        2. Structured content (topics, units, modules from ECESE)
        3. Lesson completions
        4. Assignment submissions
        5. Any activity with concept metadata
        """
        if self.db is None:
            return []
        
        try:
            student_oid = ObjectId(student_id)
            
            # 1. Fetch all quiz completions with concept data
            quizzes = list(self.db.learning_activities.find({
                'user_id': student_oid,
                'activity_type': 'quiz_complete',
                'score': {'$exists': True, '$ne': None}
            }))
            
            # 2. Fetch all lesson completions
            lessons = list(self.db.learning_activities.find({
                'user_id': student_oid,
                'activity_type': 'lesson_complete'
            }))
            
            # 3. Fetch all assignment submissions
            assignments = list(self.db.engagement_logs.find({
                'user_id': student_oid,
                'activity_type': {'$in': ['assignment_submit', 'lesson_complete']}
            }))
            
            # 4. Fetch structured content the student has accessed
            # Get enrollments first
            enrollments = list(self.db.enrollments.find({'student_id': student_oid}))
            module_names = [e['module_name'] for e in enrollments]
            
            # Get structured content from enrolled modules
            structured_contents = []
            if module_names:
                structured_contents = list(self.db.structured_contents.find({
                    'module_name': {'$in': module_names},
                    'approved': True,
                    'status': {'$in': ['approved', 'published']}
                }))
            
            # Group all activities by concept
            concept_scores = {}
            concept_engagement = {}
            
            # Process quizzes (with scores)
            for quiz in quizzes:
                concepts = self.extract_concepts(quiz, 'quiz')
                for concept in concepts:
                    if concept not in concept_scores:
                        concept_scores[concept] = {
                            'concept_name': concept,
                            'scores': [],
                            'total_attempts': 0,
                            'last_attempt': None
                        }
                    
                    concept_scores[concept]['scores'].append(quiz['score'])
                    concept_scores[concept]['total_attempts'] += 1
                    
                    quiz_date = quiz.get('created_at', datetime.utcnow())
                    if not concept_scores[concept]['last_attempt'] or quiz_date > concept_scores[concept]['last_attempt']:
                        concept_scores[concept]['last_attempt'] = quiz_date
            
            # Process lessons (engagement tracking)
            for lesson in lessons:
                concepts = self.extract_concepts(lesson, 'lesson')
                for concept in concepts:
                    if concept not in concept_engagement:
                        concept_engagement[concept] = {
                            'concept_name': concept,
                            'engagement_count': 0,
                            'last_engagement': None,
                            'sources': []
                        }
                    
                    concept_engagement[concept]['engagement_count'] += 1
                    concept_engagement[concept]['sources'].append('lesson')
                    
                    lesson_date = lesson.get('created_at', datetime.utcnow())
                    if not concept_engagement[concept]['last_engagement'] or lesson_date > concept_engagement[concept]['last_engagement']:
                        concept_engagement[concept]['last_engagement'] = lesson_date
            
            # Process assignments
            for assignment in assignments:
                concepts = self.extract_concepts(assignment, 'assignment')
                for concept in concepts:
                    if concept not in concept_engagement:
                        concept_engagement[concept] = {
                            'concept_name': concept,
                            'engagement_count': 0,
                            'last_engagement': None,
                            'sources': []
                        }
                    
                    concept_engagement[concept]['engagement_count'] += 1
                    concept_engagement[concept]['sources'].append('assignment')
                    
                    assign_date = assignment.get('created_at', datetime.utcnow())
                    if not concept_engagement[concept]['last_engagement'] or assign_date > concept_engagement[concept]['last_engagement']:
                        concept_engagement[concept]['last_engagement'] = assign_date
            
            # Process structured content (all topics/units/modules)
            for content in structured_contents:
                concepts = []
                if content.get('topic_name'):
                    concepts.append(content['topic_name'])
                if content.get('unit_name'):
                    concepts.append(content['unit_name'])
                if content.get('module_name'):
                    concepts.append(content['module_name'])
                
                for concept in concepts:
                    if concept not in concept_engagement:
                        concept_engagement[concept] = {
                            'concept_name': concept,
                            'engagement_count': 0,
                            'last_engagement': None,
                            'sources': []
                        }
                    
                    if 'content' not in concept_engagement[concept]['sources']:
                        concept_engagement[concept]['sources'].append('content')
            
            # Merge quiz scores and engagement data
            all_concepts = set(list(concept_scores.keys()) + list(concept_engagement.keys()))
            
            # Calculate mastery for each concept
            mastery_data = []
            for concept_name in all_concepts:
                score_data = concept_scores.get(concept_name)
                engagement_data = concept_engagement.get(concept_name)
                
                # Calculate average score from quizzes
                average_score = None
                if score_data and score_data['scores']:
                    average_score = sum(score_data['scores']) / len(score_data['scores'])
                
                # If no quiz scores, use engagement as indicator (lower weight)
                mastery_percentage = 0
                if average_score is not None:
                    # Primary: Use quiz scores
                    mastery_percentage = average_score
                elif engagement_data and engagement_data['engagement_count'] > 0:
                    # Secondary: Estimate from engagement (max 50% without quiz)
                    mastery_percentage = min(50, engagement_data['engagement_count'] * 10)
                
                # Determine mastery level
                if mastery_percentage >= 90:
                    mastery_level = 'mastered'
                elif mastery_percentage >= 75:
                    mastery_level = 'proficient'
                elif mastery_percentage >= 60:
                    mastery_level = 'developing'
                elif mastery_percentage >= 40:
                    mastery_level = 'beginner'
                else:
                    mastery_level = 'needs_improvement'
                
                sources = []
                if score_data:
                    sources.append('quiz')
                if engagement_data:
                    sources.extend(engagement_data['sources'])
                sources = list(set(sources))  # Remove duplicates
                
                mastery_data.append({
                    'concept_name': concept_name,
                    'mastery_percentage': round(mastery_percentage, 2),
                    'mastery_level': mastery_level,
                    'total_attempts': score_data['total_attempts'] if score_data else 0,
                    'engagement_count': engagement_data['engagement_count'] if engagement_data else 0,
                    'last_attempt': (score_data['last_attempt'].isoformat() if score_data and score_data['last_attempt'] else None) or 
                                   (engagement_data['last_engagement'].isoformat() if engagement_data and engagement_data['last_engagement'] else None),
                    'recent_scores': score_data['scores'][-5:] if score_data and score_data['scores'] else [],
                    'sources': sources
                })
            
            # Sort by mastery percentage (descending)
            mastery_data.sort(key=lambda x: x['mastery_percentage'], reverse=True)
            
            return mastery_data
            
        except Exception as e:
            print(f'[ConceptMastery] Error calculating mastery: {e}')
            return []
    
    def get_concept_mastery(self, student_id: str) -> Dict:
        """
        Get concept mastery for a student.
        
        Returns summary with all concepts and statistics.
        """
        if self.db is None:
            return {
                'student_id': student_id,
                'concepts': [],
                'total_concepts': 0,
                'mastered_count': 0,
                'proficient_count': 0,
                'developing_count': 0,
                'beginner_count': 0,
                'needs_improvement_count': 0,
                'average_mastery': 0,
                'last_updated': datetime.utcnow().isoformat()
            }
        
        try:
            # Calculate current mastery
            mastery_data = self.calculate_concept_mastery(student_id)
            
            mastery_summary = {
                'student_id': student_id,
                'concepts': mastery_data,
                'total_concepts': len(mastery_data),
                'mastered_count': len([c for c in mastery_data if c['mastery_level'] == 'mastered']),
                'proficient_count': len([c for c in mastery_data if c['mastery_level'] == 'proficient']),
                'developing_count': len([c for c in mastery_data if c['mastery_level'] == 'developing']),
                'beginner_count': len([c for c in mastery_data if c['mastery_level'] == 'beginner']),
                'needs_improvement_count': len([c for c in mastery_data if c['mastery_level'] == 'needs_improvement']),
                'average_mastery': round(sum(c['mastery_percentage'] for c in mastery_data) / len(mastery_data), 2) if mastery_data else 0,
                'last_updated': datetime.utcnow().isoformat()
            }
            
            return mastery_summary
            
        except Exception as e:
            print(f'[ConceptMastery] Error getting mastery: {e}')
            raise ConceptMasteryError(f'Failed to get concept mastery: {str(e)}', 500)
    
    def get_concept_mastery_by_name(self, student_id: str, concept_name: str) -> Optional[Dict]:
        """Get mastery for a specific concept."""
        try:
            mastery_data = self.get_concept_mastery(student_id)
            for concept in mastery_data['concepts']:
                if concept['concept_name'].lower() == concept_name.lower():
                    return concept
            return None
        except Exception as e:
            print(f'[ConceptMastery] Error getting concept mastery: {e}')
            return None


# Global service instance
concept_mastery_service = ConceptMasteryService()

