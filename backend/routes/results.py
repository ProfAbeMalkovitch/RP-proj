"""
Results routes
Handles quiz submission, scoring, and result retrieval
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from database import quizzes_collection, results_collection, students_collection
from models import QuizSubmission, QuizResult
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.adaptive_learning_service import AdaptiveLearningService
from utils.pathway_calculator import calculate_pathway, calculate_average_score

router = APIRouter()


@router.post("/submit")
async def submit_quiz(submission: QuizSubmission):
    """
    Submit quiz answers and calculate score
    Updates student's cumulative score
    """
    # Get quiz with correct answers
    quiz = quizzes_collection.find_one({"quiz_id": submission.quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    total_points = 0
    earned_points = 0
    answers = {}
    
    for question in quiz.get("questions", []):
        question_id = question["question_id"]
        correct_answer = question["correct_answer"]
        points = question.get("points", 10)
        total_points += points
        
        student_answer = submission.answers.get(question_id)
        answers[question_id] = student_answer
        
        if student_answer == correct_answer:
            earned_points += points
    
    percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    
    # Get pathway_id from quiz
    pathway_id = quiz.get("pathway_id")
    
    # Create result document
    result_id = f"result_{datetime.now().timestamp()}"
    result = {
        "result_id": result_id,
        "student_id": submission.student_id,
        "quiz_id": submission.quiz_id,
        "pathway_id": pathway_id,
        "score": earned_points,
        "total_points": total_points,
        "percentage": percentage,
        "submitted_at": datetime.now(),
        "answers": answers
    }
    
    # Save result
    results_collection.insert_one(result)
    
    # Update student's quiz scores and pathway based on performance
    student = students_collection.find_one({"student_id": submission.student_id})
    if student:
        # Get current quiz scores
        quiz_scores = student.get("quiz_scores", [])
        
        # Add new quiz score (percentage)
        quiz_scores.append(percentage)
        
        # Calculate new average score
        average_score = calculate_average_score(quiz_scores)
        
        # Calculate pathway based on quiz performance (your part: categorization)
        new_pathway = calculate_pathway(quiz_scores)
        
        # Update cumulative score
        current_cumulative = student.get("cumulative_score", 0.0)
        new_cumulative = current_cumulative + percentage
        
        # Update student record
        update_data = {
            "quiz_scores": quiz_scores,
            "average_score": average_score,
            "pathway": new_pathway,
            "cumulative_score": new_cumulative
        }
        
        # Check if pathway changed
        old_pathway = student.get("pathway", "Basic")
        if new_pathway != old_pathway:
            result["pathway_changed"] = True
            result["old_pathway"] = old_pathway
            result["new_pathway"] = new_pathway
        
        students_collection.update_one(
            {"student_id": submission.student_id},
            {"$set": update_data}
        )
    
    # Remove _id from result before returning
    result.pop("_id", None)
    
    # Update adaptive learning system (your part: personalized guides)
    try:
        # Update concept mastery (for mind map weak areas)
        AdaptiveLearningService.update_concept_mastery(submission.student_id, result)
        
        # Check if pathway needs further adjustment based on mastery (advanced logic)
        pathway_changed_mastery = AdaptiveLearningService.adjust_pathway(submission.student_id)
        if pathway_changed_mastery and pathway_changed_mastery != new_pathway:
            # Mastery-based adjustment (more sophisticated than quiz-only)
            students_collection.update_one(
                {"student_id": submission.student_id},
                {"$set": {"pathway": pathway_changed_mastery}}
            )
            result["pathway_adjusted_by_mastery"] = True
            result["mastery_based_pathway"] = pathway_changed_mastery
        
        # Generate personalized recommendations
        recommendations = AdaptiveLearningService.generate_recommendations(submission.student_id)
        result["recommendations_count"] = len(recommendations)
    except Exception as e:
        # Don't fail quiz submission if adaptive learning fails
        print(f"Adaptive learning update failed: {str(e)}")
    
    return result


@router.get("/student/{student_id}", response_model=List[QuizResult])
async def get_student_results(student_id: str):
    """
    Get all quiz results for a specific student
    """
    results = list(results_collection.find({"student_id": student_id}, {"_id": 0}))
    # Sort by submission date (newest first)
    results.sort(key=lambda x: x.get("submitted_at", datetime.min), reverse=True)
    return results


@router.get("/quiz/{quiz_id}/student/{student_id}")
async def get_quiz_result_for_student(
    quiz_id: str, 
    student_id: str,
    after_date: Optional[str] = Query(None, description="Only return results submitted after this date (ISO format)")
):
    """
    Get specific quiz result for a student
    If after_date is provided, only return results submitted after that date (for task-specific checks)
    """
    query = {"quiz_id": quiz_id, "student_id": student_id}
    
    # If after_date is provided, filter by date (for task-specific checks)
    if after_date:
        try:
            # Handle different date formats
            after_date_clean = after_date.replace('Z', '+00:00')
            if 'T' not in after_date_clean:
                after_date_clean += 'T00:00:00'
            after_datetime = datetime.fromisoformat(after_date_clean.replace('Z', ''))
            query["submitted_at"] = {"$gte": after_datetime}
        except Exception as e:
            # Invalid date format, ignore filter
            print(f"Invalid date format for after_date filter: {e}")
    
    # Find most recent result matching criteria
    results = list(results_collection.find(query, {"_id": 0}).sort("submitted_at", -1))
    
    if not results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Return most recent result
    return results[0]


@router.delete("/result/{result_id}/student/{student_id}")
async def delete_quiz_result(result_id: str, student_id: str):
    """
    Delete a quiz result for a student
    Allows students to delete their quiz attempt and retake the quiz
    """
    # Find the result
    result = results_collection.find_one({"result_id": result_id, "student_id": student_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Delete the result
    delete_result = results_collection.delete_one({"result_id": result_id, "student_id": student_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete result")
    
    # Update student's cumulative score (subtract the deleted result's percentage)
    student = students_collection.find_one({"student_id": student_id})
    if student:
        current_score = student.get("cumulative_score", 0.0)
        # Subtract the percentage from cumulative score
        percentage = result.get("percentage", 0)
        new_score = max(0, current_score - percentage)  # Ensure score doesn't go negative
        students_collection.update_one(
            {"student_id": student_id},
            {"$set": {"cumulative_score": new_score}}
        )
    
    return {"message": "Quiz result deleted successfully", "deleted": True}











@router.get("/quiz/{quiz_id}/student/{student_id}")
async def get_quiz_result_for_student(
    quiz_id: str, 
    student_id: str,
    after_date: Optional[str] = Query(None, description="Only return results submitted after this date (ISO format)")
):
    """
    Get specific quiz result for a student
    If after_date is provided, only return results submitted after that date (for task-specific checks)
    """
    query = {"quiz_id": quiz_id, "student_id": student_id}
    
    # If after_date is provided, filter by date (for task-specific checks)
    if after_date:
        try:
            # Handle different date formats
            after_date_clean = after_date.replace('Z', '+00:00')
            if 'T' not in after_date_clean:
                after_date_clean += 'T00:00:00'
            after_datetime = datetime.fromisoformat(after_date_clean.replace('Z', ''))
            query["submitted_at"] = {"$gte": after_datetime}
        except Exception as e:
            # Invalid date format, ignore filter
            print(f"Invalid date format for after_date filter: {e}")
    
    # Find most recent result matching criteria
    results = list(results_collection.find(query, {"_id": 0}).sort("submitted_at", -1))
    
    if not results:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Return most recent result
    return results[0]


@router.delete("/result/{result_id}/student/{student_id}")
async def delete_quiz_result(result_id: str, student_id: str):
    """
    Delete a quiz result for a student
    Allows students to delete their quiz attempt and retake the quiz
    """
    # Find the result
    result = results_collection.find_one({"result_id": result_id, "student_id": student_id})
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    # Delete the result
    delete_result = results_collection.delete_one({"result_id": result_id, "student_id": student_id})
    
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete result")
    
    # Update student's cumulative score (subtract the deleted result's percentage)
    student = students_collection.find_one({"student_id": student_id})
    if student:
        current_score = student.get("cumulative_score", 0.0)
        # Subtract the percentage from cumulative score
        percentage = result.get("percentage", 0)
        new_score = max(0, current_score - percentage)  # Ensure score doesn't go negative
        students_collection.update_one(
            {"student_id": student_id},
            {"$set": {"cumulative_score": new_score}}
        )
    
    return {"message": "Quiz result deleted successfully", "deleted": True}









