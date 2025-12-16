"""
Roadmap Generation Service
High-standard intelligent roadmap generation engine based on knowledge base templates
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from database import (
    roadmap_templates_collection,
    generated_roadmaps_collection,
    concept_mastery_collection,
    results_collection
)
from services.adaptive_learning_service import AdaptiveLearningService


class RoadmapGenerationService:
    """Service for generating personalized roadmaps from knowledge base templates"""
    
    # Weak area threshold (concepts below this are considered weak)
    WEAK_AREA_THRESHOLD = 0.6  # 60%
    
    # Maximum tasks in a generated roadmap
    MAX_TASKS = 12
    MIN_TASKS = 6
    
    @staticmethod
    def get_student_profile(student_id: str) -> Dict[str, Any]:
        """Get comprehensive student profile for roadmap generation"""
        try:
            # Get mastery data
            mastery_data = AdaptiveLearningService.get_student_mastery(student_id)
            
            # Get weak areas
            weak_areas_list = AdaptiveLearningService.identify_weak_areas(
                student_id, threshold=RoadmapGenerationService.WEAK_AREA_THRESHOLD
            )
            weak_areas = [area['concept'] for area in weak_areas_list]
            
            # Get recommendations
            recommendations = AdaptiveLearningService.generate_recommendations(student_id)
            
            # Get completed quizzes to identify completed concepts
            completed_results = results_collection.find(
                {"student_id": student_id},
                {"quiz_id": 1, "pathway_id": 1, "submitted_at": 1, "percentage": 1}
            )
            
            # Calculate overall statistics
            concepts = mastery_data.get('concepts', {})
            mastery_scores = {}
            for concept, data in concepts.items():
                if isinstance(data, dict):
                    mastery_scores[concept] = data.get('mastery_score', 0)
                elif hasattr(data, 'mastery_score'):
                    mastery_scores[concept] = data.mastery_score
                else:
                    mastery_scores[concept] = 0
            
            # Get pathway from student data (would need students collection)
            # For now, infer from average mastery
            avg_mastery = mastery_data.get('overall_mastery', 0.5)
            if avg_mastery < 0.5:
                pathway_level = "Basic"
            elif avg_mastery < 0.75:
                pathway_level = "Intermediate"
            else:
                pathway_level = "Excellent"
            
            return {
                'student_id': student_id,
                'mastery_scores': mastery_scores,
                'weak_areas': weak_areas,
                'strong_areas': [concept for concept, score in mastery_scores.items() 
                                if score >= 0.8],
                'recommendations': recommendations,
                'pathway_level': pathway_level,
                'overall_mastery': mastery_data.get('overall_mastery', 0.5),
                'completed_results': list(completed_results)
            }
        except Exception as e:
            print(f"Error getting student profile: {e}")
            return {
                'student_id': student_id,
                'mastery_scores': {},
                'weak_areas': [],
                'strong_areas': [],
                'recommendations': [],
                'pathway_level': "Basic",
                'overall_mastery': 0.5,
                'completed_results': []
            }
    
    @staticmethod
    def find_matching_templates(student_profile: Dict[str, Any], 
                               focus_areas: Optional[List[str]] = None,
                               template_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Find roadmap templates matching student's needs"""
        try:
            weak_areas = focus_areas or student_profile.get('weak_areas', [])
            pathway_level = student_profile.get('pathway_level', 'Basic')
            mastery_scores = student_profile.get('mastery_scores', {})
            
            query = {
                'is_active': True
            }
            
            # If specific templates requested, use those
            if template_ids:
                query['template_id'] = {'$in': template_ids}
            else:
                # Build flexible query - prioritize matches but include fallbacks
                or_conditions = []
                
                # Pathway level mapping for flexibility (students can use templates from their level or slightly above)
                pathway_mapping = {
                    'Basic': ['Basic', 'Intermediate'],
                    'Intermediate': ['Intermediate', 'Excellent'],
                    'Excellent': ['Excellent']
                }
                allowed_levels = pathway_mapping.get(pathway_level, [pathway_level])
                
                # Find templates for weak areas
                if weak_areas:
                    # Templates specifically targeting weak areas
                    or_conditions.append({
                        'weak_area_focus': True,
                        'target_concepts': {'$in': weak_areas}
                    })
                    # Templates with matching concepts (even if not weak_area_focus)
                    or_conditions.append({
                        'target_concepts': {'$elemMatch': {'$in': weak_areas}},
                        'pathway_level': {'$in': allowed_levels}
                    })
                
                # Templates matching pathway level (with or without weak area focus)
                or_conditions.append({
                    'pathway_level': {'$in': allowed_levels}
                })
                
                # Combine with OR - any of these conditions can match
                if or_conditions:
                    query['$or'] = or_conditions
            
            templates = list(roadmap_templates_collection.find(query))
            
            # If still no templates found, fall back to all active templates (most flexible)
            if not templates:
                templates = list(roadmap_templates_collection.find({'is_active': True}))
            
            # Score and rank templates based on relevance
            scored_templates = []
            for template in templates:
                score = RoadmapGenerationService._calculate_template_score(
                    template, student_profile, weak_areas
                )
                template['_relevance_score'] = score
                scored_templates.append(template)
            
            # Sort by relevance score (highest first)
            scored_templates.sort(key=lambda x: x.get('_relevance_score', 0), reverse=True)
            
            return scored_templates[:5]  # Return top 5 most relevant
            
        except Exception as e:
            print(f"Error finding matching templates: {e}")
            return []
    
    @staticmethod
    def _calculate_template_score(template: Dict[str, Any], 
                                  student_profile: Dict[str, Any],
                                  weak_areas: List[str]) -> float:
        """Calculate relevance score for a template"""
        score = 0.0
        
        # Match weak areas
        template_concepts = template.get('target_concepts', [])
        weak_area_matches = len(set(template_concepts) & set(weak_areas))
        if weak_area_matches > 0:
            score += weak_area_matches * 10
        
        # Match pathway level
        if template.get('pathway_level') == student_profile.get('pathway_level'):
            score += 5
        
        # Weak area focus bonus
        if template.get('weak_area_focus') and weak_areas:
            score += 10
        
        # Check prerequisites (bonus if student meets them)
        prerequisites = template.get('prerequisites', {})
        mastery_scores = student_profile.get('mastery_scores', {})
        prerequisites_met = 0
        for concept, threshold in prerequisites.items():
            if mastery_scores.get(concept, 0) >= threshold:
                prerequisites_met += 1
        
        if prerequisites:
            prerequisite_ratio = prerequisites_met / len(prerequisites)
            score += prerequisite_ratio * 5
        
        return score
    
    @staticmethod
    def combine_templates(templates: List[Dict[str, Any]], 
                         student_profile: Dict[str, Any],
                         max_tasks: Optional[int] = None) -> Dict[str, Any]:
        """Combine multiple templates into a cohesive roadmap"""
        max_tasks = max_tasks or RoadmapGenerationService.MAX_TASKS
        combined_tasks = []
        used_task_ids = set()
        template_ids_used = []
        
        # Sort templates by relevance score
        sorted_templates = sorted(
            templates, 
            key=lambda x: x.get('_relevance_score', 0), 
            reverse=True
        )
        
        # Primary template (highest relevance)
        if sorted_templates:
            primary_template = sorted_templates[0]
            template_ids_used.append(primary_template['template_id'])
            
            # Add tasks from primary template
            for task in primary_template.get('tasks', []):
                if len(combined_tasks) >= max_tasks:
                    break
                
                task_id = task.get('task_id') or f"task_{len(combined_tasks)}"
                if task_id not in used_task_ids:
                    combined_tasks.append(task)
                    used_task_ids.add(task_id)
        
        # Add tasks from secondary templates to fill gaps
        for template in sorted_templates[1:]:
            if len(combined_tasks) >= max_tasks:
                break
            
            template_ids_used.append(template['template_id'])
            
            for task in template.get('tasks', []):
                if len(combined_tasks) >= max_tasks:
                    break
                
                task_id = task.get('task_id') or f"task_{len(combined_tasks)}"
                if task_id not in used_task_ids:
                    # Check if task adds value (not duplicate concept)
                    task_concept = task.get('title', '').lower()
                    already_has_concept = any(
                        task_concept in existing_task.get('title', '').lower() 
                        for existing_task in combined_tasks
                    )
                    
                    if not already_has_concept:
                        combined_tasks.append(task)
                        used_task_ids.add(task_id)
        
        # Renumber tasks to ensure sequential order
        for idx, task in enumerate(combined_tasks, 1):
            task['order'] = idx
        
        # Calculate estimated completion date (assuming 3-4 tasks per week)
        tasks_per_week = 4
        weeks_needed = len(combined_tasks) / tasks_per_week
        estimated_completion = datetime.now() + timedelta(weeks=int(weeks_needed))
        
        return {
            'tasks': combined_tasks,
            'template_ids': template_ids_used,
            'total_tasks': len(combined_tasks),
            'estimated_completion_date': estimated_completion,
            'generation_reason': RoadmapGenerationService._generate_reason(
                student_profile, template_ids_used
            )
        }
    
    @staticmethod
    def _generate_reason(student_profile: Dict[str, Any], 
                        template_ids: List[str]) -> str:
        """Generate human-readable reason for roadmap generation"""
        weak_areas = student_profile.get('weak_areas', [])
        
        if weak_areas:
            areas_str = ', '.join(weak_areas[:3])
            if len(weak_areas) > 3:
                areas_str += f", and {len(weak_areas) - 3} more"
            return f"Personalized roadmap focusing on weak areas: {areas_str}. Generated from {len(template_ids)} matching template(s)."
        else:
            return f"Personalized learning roadmap based on your current mastery level and pathway. Generated from {len(template_ids)} matching template(s)."
    
    @staticmethod
    def generate_roadmap(student_id: str,
                        regenerate: bool = False,
                        focus_areas: Optional[List[str]] = None,
                        template_ids: Optional[List[str]] = None,
                        max_tasks: Optional[int] = None) -> Dict[str, Any]:
        """Main method to generate a personalized roadmap for a student"""
        try:
            # Check if roadmap already exists
            existing_roadmap = generated_roadmaps_collection.find_one(
                {
                    'student_id': student_id,
                    'status': {'$in': ['pending', 'active']}
                },
                sort=[('generated_at', -1)]
            )
            
            if existing_roadmap and not regenerate:
                return {
                    'roadmap': existing_roadmap,
                    'is_new': False,
                    'message': 'Existing active roadmap found'
                }
            
            # Get student profile
            student_profile = RoadmapGenerationService.get_student_profile(student_id)
            
            # Find matching templates
            matching_templates = RoadmapGenerationService.find_matching_templates(
                student_profile, focus_areas, template_ids
            )
            
            if not matching_templates:
                return {
                    'error': 'No matching templates found. Please create templates first.',
                    'student_profile': student_profile
                }
            
            # Combine templates into roadmap
            roadmap_data = RoadmapGenerationService.combine_templates(
                matching_templates, student_profile, max_tasks
            )
            
            # Create roadmap document
            roadmap_id = str(ObjectId())
            roadmap_doc = {
                'roadmap_id': roadmap_id,
                'student_id': student_id,
                'generated_at': datetime.now(),
                'status': 'pending',  # Will be activated after approval or automatically
                'template_ids': roadmap_data['template_ids'],
                'focus_areas': student_profile.get('weak_areas', []),
                'tasks': roadmap_data['tasks'],
                'total_tasks': roadmap_data['total_tasks'],
                'completed_tasks': 0,
                'estimated_completion_date': roadmap_data['estimated_completion_date'],
                'generation_reason': roadmap_data['generation_reason'],
                'approved_by': None,
                'approved_at': None,
                'notes': None
            }
            
            # If existing roadmap, archive it
            if existing_roadmap:
                generated_roadmaps_collection.update_one(
                    {'roadmap_id': existing_roadmap['roadmap_id']},
                    {'$set': {'status': 'archived', 'archived_at': datetime.now()}}
                )
            
            # Insert new roadmap
            generated_roadmaps_collection.insert_one(roadmap_doc)
            
            # Update template usage counts
            for template_id in roadmap_data['template_ids']:
                roadmap_templates_collection.update_one(
                    {'template_id': template_id},
                    {'$inc': {'usage_count': 1}}
                )
            
            return {
                'roadmap': roadmap_doc,
                'is_new': True,
                'generation_metadata': {
                    'templates_matched': len(matching_templates),
                    'templates_used': len(roadmap_data['template_ids']),
                    'weak_areas_found': len(student_profile.get('weak_areas', [])),
                    'generation_time': datetime.now().isoformat()
                },
                'matching_templates': roadmap_data['template_ids'],
                'reasoning': roadmap_data['generation_reason']
            }
            
        except Exception as e:
            print(f"Error generating roadmap: {e}")
            import traceback
            traceback.print_exc()
            return {
                'error': f'Failed to generate roadmap: {str(e)}'
            }

