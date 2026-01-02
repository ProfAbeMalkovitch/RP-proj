"""
Roadmap Service Module.

Generates AI-powered learning roadmaps based on student weaknesses
and quiz performance. Provides personalized guidance and recommendations.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from bson import ObjectId

import sys
from pathlib import Path
# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from database import get_database
from ai_service import ai_service
from .concept_mastery import concept_mastery_service
from .learning_pathway import learning_pathway_service


class RoadmapError(Exception):
    """Base exception for roadmap errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RoadmapService:
    """Main roadmap service."""
    
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            self._db = get_database()
        return self._db
    
    def identify_weak_areas(self, student_id: str) -> List[Dict]:
        """
        Identify weak areas from concept mastery data.
        
        Weak areas are concepts with:
        - Mastery < 60% (developing or below)
        - Or needs_improvement level
        """
        try:
            mastery_data = concept_mastery_service.get_concept_mastery(student_id)
            
            weak_areas = []
            for concept in mastery_data.get('concepts', []):
                if (concept['mastery_percentage'] < 60 or 
                    concept['mastery_level'] in ['beginner', 'needs_improvement']):
                    weak_areas.append({
                        'concept_name': concept['concept_name'],
                        'mastery_percentage': concept['mastery_percentage'],
                        'mastery_level': concept['mastery_level'],
                        'total_attempts': concept.get('total_attempts', 0),
                        'recent_scores': concept.get('recent_scores', []),
                        'priority': 'high' if concept['mastery_percentage'] < 40 else 'medium'
                    })
            
            # Sort by mastery percentage (lowest first - most weak)
            weak_areas.sort(key=lambda x: x['mastery_percentage'])
            
            return weak_areas
        except Exception as e:
            print(f'[Roadmap] Error identifying weak areas: {e}')
            return []
    
    def generate_roadmap_guidance(self, student_id: str) -> Dict:
        """
        Generate AI-powered roadmap guidance based on weaknesses.
        
        Creates personalized learning recommendations with:
        - Focus areas (weak concepts)
        - Study plan structure
        - Practice recommendations
        - Timeline suggestions
        """
        try:
            # Get weak areas
            weak_areas = self.identify_weak_areas(student_id)
            
            # Get pathway info
            pathway = learning_pathway_service.determine_pathway(student_id)
            
            # Get performance data
            performance = learning_pathway_service.get_student_performance(student_id)
            
            # Generate roadmap structure
            roadmap = {
                'student_id': student_id,
                'pathway_type': pathway['pathway_type'],
                'generated_at': datetime.utcnow().isoformat(),
                'weak_areas': weak_areas,
                'focus_areas': weak_areas[:5],  # Top 5 weak areas
                'study_plan': self._generate_study_plan(weak_areas, pathway),
                'recommendations': self._generate_recommendations(weak_areas, performance, pathway),
                'timeline': self._generate_timeline(weak_areas, pathway),
                'practice_schedule': self._generate_practice_schedule(weak_areas)
            }
            
            return roadmap
        except Exception as e:
            print(f'[Roadmap] Error generating roadmap: {e}')
            raise RoadmapError(f'Failed to generate roadmap: {str(e)}', 500)
    
    def _generate_study_plan(self, weak_areas: List[Dict], pathway: Dict) -> List[Dict]:
        """Generate structured study plan."""
        study_plan = []
        
        for i, area in enumerate(weak_areas[:5], 1):
            week_number = (i - 1) // 2 + 1  # 2 areas per week
            
            plan_item = {
                'week': week_number,
                'concept': area['concept_name'],
                'focus': self._get_focus_for_concept(area, pathway),
                'activities': self._get_activities_for_concept(area, pathway),
                'target_mastery': min(75, area['mastery_percentage'] + 20),  # Aim for 20% improvement
                'priority': area['priority']
            }
            study_plan.append(plan_item)
        
        return study_plan
    
    def _generate_recommendations(self, weak_areas: List[Dict], performance: Dict, pathway: Dict) -> List[Dict]:
        """Generate AI-powered personalized recommendations using AI model."""
        recommendations = []
        
        # Recommendation 1: Focus on weakest areas (AI-generated using pre-trained model)
        if weak_areas:
            weakest = weak_areas[0]
            mastery = weakest['mastery_percentage']
            pathway_type = pathway.get('pathway_type', 'balanced')
            
            # Generate AI-powered description
            ai_prompt = f"""Provide a personalized learning recommendation for a student working on the concept "{weakest['concept_name']}".

Student Performance:
- Current mastery: {mastery:.1f}%
- Learning pathway: {pathway_type}
- Total quiz attempts: {performance.get('total_quizzes', 0)}
- Average quiz score: {performance.get('average_score', 0):.1f}%

Provide a 2-3 sentence encouraging, specific recommendation that:
1. Acknowledges their current mastery level ({mastery:.1f}%)
2. Explains what this means for their learning
3. Gives clear guidance on how to improve

Be encouraging, specific, and actionable. Write in second person ("Your mastery is...")."""

            # Try AI generation, fallback to template if it fails
            description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
            if not description:
                # Fallback to template-based
                if mastery < 30:
                    description = f"Your current mastery in {weakest['concept_name']} is {mastery:.1f}%, indicating significant gaps in understanding. I recommend starting from the absolute basics and building a solid foundation. Focus on understanding core principles before attempting complex problems."
                elif mastery < 50:
                    description = f"Your mastery in {weakest['concept_name']} is {mastery:.1f}%, showing you have some understanding but need reinforcement. Focus on strengthening your grasp of fundamental concepts and their applications."
                else:
                    description = f"Your mastery in {weakest['concept_name']} is {mastery:.1f}%, which is approaching proficiency. With focused practice, you can reach mastery level. Concentrate on application and problem-solving."
            
            # Generate AI-powered action items
            action_items = ai_service.generate_action_items(
                concept_name=weakest['concept_name'],
                mastery_percentage=mastery,
                pathway_type=pathway_type,
                max_items=5
            )
            
            recommendations.append({
                'type': 'focus',
                'title': f'Priority Focus: Master {weakest["concept_name"]}',
                'description': description,
                'priority': 'high' if mastery < 40 else 'medium',
                'action_items': action_items
            })
        
        # Recommendation 2: Multiple weak areas strategy (AI-generated)
        if len(weak_areas) >= 3:
            ai_prompt = f"""Provide a learning strategy recommendation for a student with {len(weak_areas)} weak areas that need improvement.

Context:
- Number of weak areas: {len(weak_areas)}
- Learning pathway: {pathway.get('pathway_type', 'balanced')}
- Average mastery across weak areas: {sum(w['mastery_percentage'] for w in weak_areas[:5]) / min(5, len(weak_areas)):.1f}%

Provide a 2-3 sentence strategy recommendation that:
1. Acknowledges the number of areas needing work
2. Suggests a structured approach (e.g., 2 concepts per week)
3. Explains why this approach works
4. Is encouraging and practical

Write in second person. Be specific and actionable."""

            description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
            if not description:
                description = f'You have {len(weak_areas)} areas needing improvement. I recommend a structured approach: focus on 2 concepts per week, dedicating focused time to each. This prevents overwhelm while ensuring steady progress.'
            
            recommendations.append({
                'type': 'strategy',
                'title': 'Multi-Concept Learning Strategy',
                'description': description,
                'priority': 'high',
                'action_items': [
                    'Follow the weekly study plan provided below',
                    'Dedicate specific time blocks for each weak area',
                    'Track your progress weekly',
                    'Celebrate small improvements',
                    'Don\'t rush - mastery takes time'
                ]
            })
        
        # Recommendation 3: Practice frequency (AI-generated)
        quiz_count = performance.get('total_quizzes', 0)
        avg_score = performance.get('average_score', 0)
        
        if quiz_count < 3:
            ai_prompt = f"""Provide a practice recommendation for a student who has completed only {quiz_count} quiz{"es" if quiz_count != 1 else ""}.

Context:
- Quizzes completed: {quiz_count}
- Average score: {avg_score:.1f}%
- Learning pathway: {pathway.get('pathway_type', 'balanced')}

Provide a 2-3 sentence recommendation that:
1. Acknowledges their current quiz activity
2. Explains why regular practice is important
3. Suggests a specific practice frequency (e.g., 2-3 quizzes per week)
4. Is encouraging and motivating

Write in second person. Be specific."""

            description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
            if not description:
                description = f'You\'ve completed {quiz_count} quiz{"es" if quiz_count != 1 else ""}. Regular assessment is crucial for identifying knowledge gaps. I recommend taking at least 2-3 quizzes per week to track your progress effectively.'
            
            recommendations.append({
                'type': 'practice',
                'title': 'Build Consistent Practice Habits',
                'description': description,
                'priority': 'high',
                'action_items': [
                    'Schedule quiz time in your weekly calendar',
                    'Take quizzes after reviewing each concept',
                    'Analyze results to identify patterns',
                    'Focus on improving weak areas identified in quizzes',
                    'Review incorrect answers thoroughly'
                ]
            })
        elif quiz_count < 10 and avg_score < 70:
            ai_prompt = f"""Provide a quiz improvement recommendation for a student with {quiz_count} quizzes completed and an average score of {avg_score:.1f}%.

Context:
- Quizzes completed: {quiz_count}
- Average score: {avg_score:.1f}%
- Learning pathway: {pathway.get('pathway_type', 'balanced')}

Provide a 2-3 sentence recommendation that:
1. Acknowledges their quiz activity and current performance
2. Identifies areas for improvement
3. Suggests specific strategies to enhance performance
4. Emphasizes understanding over memorization

Write in second person. Be encouraging and specific."""

            description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
            if not description:
                description = f'With {quiz_count} quizzes completed and an average score of {avg_score:.1f}%, there\'s room for improvement. Focus on understanding why answers are correct or incorrect, not just memorizing.'
            
            recommendations.append({
                'type': 'practice',
                'title': 'Enhance Quiz Performance',
                'description': description,
                'priority': 'medium',
                'action_items': [
                    'Review quiz explanations carefully',
                    'Identify common mistake patterns',
                    'Practice similar problems before next quiz',
                    'Take time to understand concepts deeply',
                    'Use quizzes as learning tools, not just assessments'
                ]
            })
        
        # Recommendation 4: Pathway-specific AI guidance
        pathway_type = pathway.get('pathway_type', 'balanced')
        avg_score = performance.get('average_score', 0)
        task_completion = performance.get('task_completion_rate', 0)
        
        ai_prompt = f"""Provide a pathway-specific learning recommendation for a student on the {pathway_type} learning pathway.

Student Context:
- Learning pathway: {pathway_type}
- Average quiz score: {avg_score:.1f}%
- Task completion rate: {task_completion*100:.0f}%
- Number of weak areas: {len(weak_areas)}

Provide a 2-3 sentence recommendation that:
1. Explains what the {pathway_type} pathway means for them
2. Provides specific guidance tailored to this pathway level
3. Is encouraging and actionable
4. Acknowledges their current performance level

Write in second person. Be specific to the {pathway_type} pathway."""

        description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
        if not description:
            # Fallback templates
            if pathway_type == 'basic':
                description = 'Based on your current pathway, you\'re on a foundational learning journey. This is perfect for building strong fundamentals. Take your time, don\'t skip steps, and ensure you truly understand each concept before moving forward.'
            elif pathway_type == 'balanced':
                description = 'You\'re on a balanced learning path, which means you can handle a mix of foundational and challenging content. Maintain this balance by alternating between review and new challenges.'
            else:
                description = 'Your pathway indicates readiness for advanced content. While you have some weak areas, your overall performance suggests you can handle challenging material. Use this to deepen understanding through complex problems.'
        
        pathway_titles = {
            'basic': 'Foundational Learning Path',
            'balanced': 'Balanced Learning Approach',
            'acceleration': 'Accelerated Learning Opportunities'
        }
        
        pathway_action_items = {
            'basic': [
                'Spend 30-45 minutes daily on core concepts',
                'Use visual aids and step-by-step guides',
                'Practice with guided examples before independent work',
                'Review previous lessons weekly',
                'Ask questions when concepts are unclear',
                'Build confidence with easier problems first'
            ],
            'balanced': [
                'Mix review sessions with new content',
                'Challenge yourself with moderate difficulty problems',
                'Maintain consistent study schedule',
                'Balance theory with practical application',
                'Track progress across all concepts'
            ],
            'acceleration': [
                'Engage with advanced problem-solving exercises',
                'Explore extension topics and applications',
                'Take on complex, multi-step assessments',
                'Help explain concepts to peers (teaching reinforces learning)',
                'Connect concepts across different topics',
                'Pursue independent research on interesting areas'
            ]
        }
        
        recommendations.append({
            'type': 'pathway',
            'title': pathway_titles.get(pathway_type, 'Learning Pathway Guidance'),
            'description': description,
            'priority': 'high' if pathway_type == 'basic' else 'medium',
            'action_items': pathway_action_items.get(pathway_type, [])
        })
        
        # Recommendation 5: Performance-based insights (AI-generated)
        task_completion_rate = performance.get('task_completion_rate', 0)
        if task_completion_rate < 0.6:
            ai_prompt = f"""Provide a task completion improvement recommendation for a student with a {task_completion_rate*100:.0f}% task completion rate.

Context:
- Task completion rate: {task_completion_rate*100:.0f}%
- Completed tasks: {performance.get('completed_tasks', 0)} / {performance.get('total_tasks', 0)}
- Learning pathway: {pathway.get('pathway_type', 'balanced')}

Provide a 2-3 sentence recommendation that:
1. Acknowledges their current completion rate
2. Explains why completing tasks is important
3. Provides specific, actionable advice to improve completion
4. Is encouraging and supportive

Write in second person. Be specific and motivating."""

            description = ai_service.generate_recommendation(ai_prompt, max_tokens=200)
            if not description:
                description = f'Your task completion rate is {task_completion_rate*100:.0f}%. Completing assigned tasks is essential for building knowledge systematically. Focus on finishing what you start.'
            
            recommendations.append({
                'type': 'engagement',
                'title': 'Improve Task Completion',
                'description': description,
                'priority': 'medium',
                'action_items': [
                    'Set daily completion goals',
                    'Break large tasks into smaller steps',
                    'Remove distractions during study time',
                    'Track completion to build momentum',
                    'Reward yourself for completing tasks'
                ]
            })
        
        return recommendations
    
    def _generate_timeline(self, weak_areas: List[Dict], pathway: Dict) -> List[Dict]:
        """Generate learning timeline."""
        timeline = []
        
        # Calculate weeks needed (2 concepts per week)
        total_weeks = (len(weak_areas[:10]) + 1) // 2
        
        for week in range(1, total_weeks + 1):
            week_concepts = weak_areas[(week-1)*2:week*2]
            
            goals = []
            milestones = []
            for c in week_concepts:
                goals.append(f'Improve mastery in {c["concept_name"]} by 15-20%')
                milestones.append(f'Complete review of {c["concept_name"]}')
                milestones.append(f'Take practice quiz on {c["concept_name"]}')
            
            timeline_item = {
                'week': week,
                'focus_concepts': [c['concept_name'] for c in week_concepts],
                'goals': goals,
                'milestones': milestones
            }
            timeline.append(timeline_item)
        
        return timeline
    
    def _generate_practice_schedule(self, weak_areas: List[Dict]) -> List[Dict]:
        """Generate weekly practice schedule."""
        schedule = []
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for i, area in enumerate(weak_areas[:7]):  # One per day
            day_index = i % len(days)
            schedule.append({
                'day': days[day_index],
                'concept': area['concept_name'],
                'duration_minutes': 30 if area['mastery_percentage'] < 40 else 20,
                'activities': [
                    'Review concept materials',
                    'Complete practice exercises',
                    'Take mini-quiz'
                ]
            })
        
        return schedule
    
    def _get_focus_for_concept(self, area: Dict, pathway: Dict) -> str:
        """Get focus description for a concept."""
        mastery = area['mastery_percentage']
        
        if mastery < 40:
            return 'Build foundational understanding. Start with basic definitions and core principles.'
        elif mastery < 60:
            return 'Strengthen core concepts. Practice application of fundamental principles.'
        else:
            return 'Reinforce understanding. Focus on advanced applications and problem-solving.'
    
    def _get_activities_for_concept(self, area: Dict, pathway: Dict) -> List[str]:
        """Get recommended activities for a concept."""
        activities = []
        mastery = area['mastery_percentage']
        
        if mastery < 40:
            activities = [
                'Read foundational materials',
                'Watch explanatory videos',
                'Complete basic exercises',
                'Review with examples'
            ]
        elif mastery < 60:
            activities = [
                'Practice with guided exercises',
                'Work through examples',
                'Take practice quizzes',
                'Review common mistakes'
            ]
        else:
            activities = [
                'Advanced practice problems',
                'Application exercises',
                'Challenge assessments',
                'Peer discussion'
            ]
        
        return activities
    
    def get_roadmap(self, student_id: str) -> Dict:
        """Get complete roadmap for a student."""
        try:
            roadmap = self.generate_roadmap_guidance(student_id)
            return {
                'success': True,
                'data': roadmap
            }
        except RoadmapError as e:
            raise e
        except Exception as e:
            print(f'[Roadmap] Error getting roadmap: {e}')
            raise RoadmapError(f'Failed to get roadmap: {str(e)}', 500)


# Global service instance
roadmap_service = RoadmapService()

