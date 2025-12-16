"""
Adaptive Learning Service
Handles mastery calculation, pathway adjustment, and content recommendations
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from database import (
    concept_mastery_collection, 
    results_collection, 
    quizzes_collection,
    students_collection,
    pathways_collection,
    question_metadata_collection,
    recommendations_collection
)
import math


class AdaptiveLearningService:
    
    @staticmethod
    def extract_concepts_from_quiz(quiz_id: str) -> List[str]:
        """Extract concepts from quiz questions"""
        quiz = quizzes_collection.find_one({"quiz_id": quiz_id})
        if not quiz:
            return []
        
        concepts = set()
        for question in quiz.get("questions", []):
            # Extract from question metadata if available
            metadata = question_metadata_collection.find_one({"question_id": question.get("question_id")})
            if metadata and metadata.get("concepts"):
                concepts.update(metadata["concepts"])
            else:
                # Fallback: extract from pathway/topic
                pathway_id = quiz.get("pathway_id", "")
                if "basic" in pathway_id.lower():
                    concepts.add("fundamentals")
                elif "intermediate" in pathway_id.lower():
                    concepts.add("intermediate_concepts")
                elif "accelerated" in pathway_id.lower():
                    concepts.add("advanced_concepts")
        
        return list(concepts)
    
    @staticmethod
    def calculate_concept_mastery(
        student_id: str, 
        concept: str, 
        quiz_results: List[Dict[str, Any]]
    ) -> float:
        """Calculate mastery score for a specific concept"""
        if not quiz_results:
            return 0.0
        
        # Filter results relevant to this concept
        concept_results = []
        for result in quiz_results:
            quiz = quizzes_collection.find_one({"quiz_id": result.get("quiz_id")})
            if quiz:
                quiz_concepts = AdaptiveLearningService.extract_concepts_from_quiz(result.get("quiz_id"))
                if concept in quiz_concepts or any(c in concept for c in quiz_concepts):
                    concept_results.append(result)
        
        if not concept_results:
            return 0.0
        
        # Get question-level performance if available
        scores = []
        for result in concept_results:
            percentage = result.get("percentage", 0)
            scores.append(percentage / 100.0)  # Convert to 0-1 scale
        
        if not scores:
            return 0.0
        
        # Weight recent performance more heavily
        recent_weight = 0.6
        historical_weight = 0.4
        
        # Sort by date (most recent first)
        sorted_results = sorted(concept_results, 
                               key=lambda x: x.get("submitted_at", datetime.min),
                               reverse=True)
        
        # Calculate recent average (last 5 results or all if less)
        recent_count = min(5, len(sorted_results))
        recent_scores = [r.get("percentage", 0) / 100.0 for r in sorted_results[:recent_count]]
        recent_avg = sum(recent_scores) / len(recent_scores) if recent_scores else 0.0
        
        # Calculate historical average
        historical_avg = sum(scores) / len(scores) if scores else 0.0
        
        # Weighted mastery score
        mastery = (recent_avg * recent_weight) + (historical_avg * historical_weight)
        
        return round(mastery, 3)
    
    @staticmethod
    def update_concept_mastery(student_id: str, quiz_result: Dict[str, Any]) -> Dict[str, Any]:
        """Update concept mastery after quiz submission"""
        quiz_id = quiz_result.get("quiz_id")
        concepts = AdaptiveLearningService.extract_concepts_from_quiz(quiz_id)
        
        # Get all quiz results for this student
        all_results = list(results_collection.find(
            {"student_id": student_id},
            {"_id": 0}
        ).sort("submitted_at", -1))
        
        # Update mastery for each concept
        mastery_doc = concept_mastery_collection.find_one({"student_id": student_id})
        
        if not mastery_doc:
            mastery_doc = {
                "student_id": student_id,
                "concepts": {},
                "last_updated": datetime.now()
            }
        
        # Calculate mastery for each concept
        overall_scores = []
        for concept in concepts:
            mastery_score = AdaptiveLearningService.calculate_concept_mastery(
                student_id, concept, all_results
            )
            
            # Get question-level stats if available
            concept_questions = 0
            concept_correct = 0
            
            for result in all_results:
                if result.get("quiz_id") == quiz_id:
                    quiz = quizzes_collection.find_one({"quiz_id": quiz_id})
                    if quiz:
                        for question in quiz.get("questions", []):
                            metadata = question_metadata_collection.find_one(
                                {"question_id": question.get("question_id")}
                            )
                            if metadata and concept in metadata.get("concepts", []):
                                concept_questions += 1
                                student_answer = result.get("answers", {}).get(
                                    question.get("question_id")
                                )
                                if student_answer == question.get("correct_answer"):
                                    concept_correct += 1
            
            # Update or create concept mastery
            if concept not in mastery_doc["concepts"]:
                mastery_doc["concepts"][concept] = {
                    "mastery_score": mastery_score,
                    "questions_answered": concept_questions,
                    "correct_answers": concept_correct,
                    "last_practiced": datetime.now().isoformat(),
                    "trend": "stable"
                }
            else:
                old_mastery = mastery_doc["concepts"][concept].get("mastery_score", 0)
                mastery_doc["concepts"][concept]["mastery_score"] = mastery_score
                mastery_doc["concepts"][concept]["questions_answered"] += concept_questions
                mastery_doc["concepts"][concept]["correct_answers"] += concept_correct
                mastery_doc["concepts"][concept]["last_practiced"] = datetime.now().isoformat()
                
                # Determine trend
                if mastery_score > old_mastery + 0.1:
                    mastery_doc["concepts"][concept]["trend"] = "improving"
                elif mastery_score < old_mastery - 0.1:
                    mastery_doc["concepts"][concept]["trend"] = "declining"
                else:
                    mastery_doc["concepts"][concept]["trend"] = "stable"
            
            overall_scores.append(mastery_score)
        
        # Calculate overall mastery
        mastery_doc["overall_mastery"] = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
        mastery_doc["last_updated"] = datetime.now()
        
        # Update or insert
        concept_mastery_collection.update_one(
            {"student_id": student_id},
            {"$set": mastery_doc},
            upsert=True
        )
        
        return mastery_doc
    
    @staticmethod
    def get_student_mastery(student_id: str) -> Dict[str, Any]:
        """Get all concept mastery for a student"""
        mastery_doc = concept_mastery_collection.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )
        
        if not mastery_doc:
            return {
                "student_id": student_id,
                "concepts": {},
                "overall_mastery": 0.0,
                "last_updated": None
            }
        
        return mastery_doc
    
    @staticmethod
    def identify_weak_areas(student_id: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """Identify concepts where student mastery is below threshold"""
        mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
        weak_areas = []
        
        for concept, data in mastery_doc.get("concepts", {}).items():
            mastery_score = data.get("mastery_score", 0)
            if mastery_score < threshold:
                weak_areas.append({
                    "concept": concept,
                    "mastery_score": mastery_score,
                    "questions_answered": data.get("questions_answered", 0),
                    "correct_answers": data.get("correct_answers", 0),
                    "trend": data.get("trend", "stable"),
                    "gap": threshold - mastery_score
                })
        
        # Sort by gap (largest gap first)
        weak_areas.sort(key=lambda x: x["gap"], reverse=True)
        return weak_areas
    
    @staticmethod
    def should_adjust_pathway(student_id: str) -> bool:
        """Determine if student pathway should be adjusted"""
        mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
        student = students_collection.find_one({"student_id": student_id})
        
        if not student or not mastery_doc:
            return False
        
        current_pathway = student.get("pathway", "Basic")
        overall_mastery = mastery_doc.get("overall_mastery", 0.0)
        concepts = mastery_doc.get("concepts", {})
        
        # Check for significant improvement (ready to upgrade)
        if overall_mastery >= 0.85 and current_pathway != "Accelerated":
            # Check for weak areas
            weak_areas = AdaptiveLearningService.identify_weak_areas(student_id, threshold=0.6)
            if len(weak_areas) == 0:  # No weak areas, ready to upgrade
                return True
        
        # Check for significant decline (might need to downgrade)
        if overall_mastery < 0.4 and current_pathway != "Basic":
            # Check if consistently struggling
            weak_areas = AdaptiveLearningService.identify_weak_areas(student_id, threshold=0.5)
            if len(weak_areas) >= len(concepts) * 0.7:  # Struggling with 70%+ concepts
                return True
        
        return False
    
    @staticmethod
    def adjust_pathway(student_id: str) -> Optional[str]:
        """Adjust student pathway based on mastery"""
        if not AdaptiveLearningService.should_adjust_pathway(student_id):
            return None
        
        mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
        student = students_collection.find_one({"student_id": student_id})
        
        if not student or not mastery_doc:
            return None
        
        current_pathway = student.get("pathway", "Basic")
        overall_mastery = mastery_doc.get("overall_mastery", 0.0)
        weak_areas = AdaptiveLearningService.identify_weak_areas(student_id, threshold=0.6)
        
        new_pathway = current_pathway
        
        # Upgrade logic
        if overall_mastery >= 0.85 and len(weak_areas) == 0:
            if current_pathway == "Basic":
                new_pathway = "Intermediate"
            elif current_pathway == "Intermediate":
                new_pathway = "Accelerated"
        
        # Downgrade logic
        elif overall_mastery < 0.4 and len(weak_areas) >= len(mastery_doc.get("concepts", {})) * 0.7:
            if current_pathway == "Accelerated":
                new_pathway = "Intermediate"
            elif current_pathway == "Intermediate":
                new_pathway = "Basic"
        
        if new_pathway != current_pathway:
            students_collection.update_one(
                {"student_id": student_id},
                {"$set": {"pathway": new_pathway}}
            )
            return new_pathway
        
        return None
    
    @staticmethod
    def generate_recommendations(student_id: str) -> List[Dict[str, Any]]:
        """Generate personalized content recommendations"""
        recommendations = []
        mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
        student = students_collection.find_one({"student_id": student_id})
        
        if not student or not mastery_doc:
            return recommendations
        
        current_pathway = student.get("pathway", "Basic")
        weak_areas = AdaptiveLearningService.identify_weak_areas(student_id, threshold=0.6)
        overall_mastery = mastery_doc.get("overall_mastery", 0.0)
        
        # Priority 1: Practice weak areas
        for weak_area in weak_areas[:3]:  # Top 3 weak areas
            concept = weak_area["concept"]
            mastery = weak_area["mastery_score"]
            
            # Find relevant quizzes/content
            relevant_quizzes = []
            for quiz in quizzes_collection.find({}, {"_id": 0}):
                quiz_concepts = AdaptiveLearningService.extract_concepts_from_quiz(quiz.get("quiz_id"))
                if concept in quiz_concepts or any(c in concept for c in quiz_concepts):
                    relevant_quizzes.append(quiz.get("quiz_id"))
            
            recommendations.append({
                "type": "practice",
                "priority": "high",
                "concept": concept,
                "content_id": relevant_quizzes[0] if relevant_quizzes else None,
                "content_type": "quiz",
                "reason": f"Mastery in {concept} is {mastery*100:.1f}% (below 60% threshold)"
            })
        
        # Priority 2: Prepare for next level
        if overall_mastery >= 0.7:
            pathway_levels = {"Basic": "Intermediate", "Intermediate": "Accelerated", "Accelerated": None}
            next_level = pathway_levels.get(current_pathway)
            
            if next_level:
                # Get prerequisites for next level
                next_pathways = list(pathways_collection.find({"level": next_level}, {"_id": 0}))
                if next_pathways:
                    recommendations.append({
                        "type": "advance",
                        "priority": "medium",
                        "concept": f"Prepare for {next_level}",
                        "content_id": next_pathways[0].get("pathway_id"),
                        "content_type": "pathway",
                        "reason": f"Ready to advance to {next_level} pathway"
                    })
        
        # Priority 3: Strengthen current level
        if overall_mastery < 0.7:
            current_pathway_quizzes = []
            for quiz in quizzes_collection.find({}, {"_id": 0}):
                if current_pathway.lower() in quiz.get("pathway_id", "").lower():
                    current_pathway_quizzes.append(quiz.get("quiz_id"))
            
            if current_pathway_quizzes:
                recommendations.append({
                    "type": "review",
                    "priority": "medium",
                    "concept": f"Strengthen {current_pathway} concepts",
                    "content_id": current_pathway_quizzes[0],
                    "content_type": "quiz",
                    "reason": f"Continue practicing {current_pathway} level content"
                })
        
        # Store recommendations
        recommendation_doc = {
            "student_id": student_id,
            "recommendations": recommendations,
            "last_updated": datetime.now()
        }
        
        recommendations_collection.update_one(
            {"student_id": student_id},
            {"$set": recommendation_doc},
            upsert=True
        )
        
        return recommendations
    
    @staticmethod
    def get_recommendations(student_id: str) -> List[Dict[str, Any]]:
        """Get stored recommendations for a student"""
        doc = recommendations_collection.find_one(
            {"student_id": student_id},
            {"_id": 0}
        )
        
        if doc:
            return doc.get("recommendations", [])
        else:
            # Generate if not exists
            return AdaptiveLearningService.generate_recommendations(student_id)








