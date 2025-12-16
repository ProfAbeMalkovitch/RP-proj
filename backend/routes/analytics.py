"""
Analytics Routes
Provides data for charts and dashboards
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from database import students_collection
from middleware.auth_middleware import require_teacher, require_student, get_current_user
from utils.pathway_calculator import calculate_average_score

router = APIRouter()


@router.get("/pathway-distribution")
async def get_pathway_distribution(current_user: dict = Depends(require_teacher)):
    """
    Get pathway distribution for pie chart
    Returns count and percentage for each pathway
    """
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    total = students_collection.count_documents({})
    if total == 0:
        return []
    
    pathways = ["Basic", "Intermediate", "Accelerated"]
    distribution = []
    
    for pathway in pathways:
        count = students_collection.count_documents({"pathway": pathway})
        percentage = (count / total * 100) if total > 0 else 0
        distribution.append({
            "name": pathway,
            "value": count,
            "percentage": round(percentage, 2)
        })
    
    return distribution


@router.get("/students-per-pathway")
async def get_students_per_pathway(current_user: dict = Depends(require_teacher)):
    """
    Get students count per pathway for bar chart
    """
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    pathways = ["Basic", "Intermediate", "Accelerated"]
    data = []
    
    for pathway in pathways:
        count = students_collection.count_documents({"pathway": pathway})
        data.append({
            "pathway": pathway,
            "count": count
        })
    
    return data


@router.get("/student/{student_id}/quiz-history")
async def get_student_quiz_history(student_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get student quiz history and dashboard data
    Students can only see their own data, teachers can see any student
    Returns full student data with quiz history, statistics, and pathway
    """
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    # Check if student can access this data
    if current_user.get("role") == "student" and current_user.get("user_id") != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    student = students_collection.find_one({"student_id": student_id}, {"_id": 0, "password": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    quiz_scores = student.get("quiz_scores", [])
    total_quizzes = len(quiz_scores)
    average_score = calculate_average_score(quiz_scores)
    pathway = student.get("pathway", "Basic")
    
    # Format data for line chart
    history = []
    for i, score in enumerate(quiz_scores, 1):
        history.append({
            "quiz": f"Quiz {i}",
            "score": round(score, 2),
            "attempt": i
        })
    
    # Return full student data with quiz history
    return {
        "pathway": pathway,
        "average_score": round(average_score, 2),
        "total_quizzes": total_quizzes,
        "quiz_history": history,
        "quiz_scores": quiz_scores
    }


@router.get("/teacher/students-summary")
async def get_students_summary(current_user: dict = Depends(require_teacher)):
    """
    Get summary of all students for teacher dashboard
    """
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    students = list(students_collection.find({}, {"_id": 0, "password": 0}))
    
    summary = []
    for student in students:
        quiz_scores = student.get("quiz_scores", [])
        summary.append({
            "student_id": student["student_id"],
            "name": student["name"],
            "email": student["email"],
            "pathway": student.get("pathway", "Basic"),
            "average_score": student.get("average_score", 0.0),
            "total_quizzes": len(quiz_scores),
            "quiz_scores": quiz_scores
        })
    
    return summary


@router.get("/teacher/student/{student_id}/details")
async def get_student_details(student_id: str, current_user: dict = Depends(require_teacher)):
    """
    Get detailed student information for teacher
    """
    if students_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    student = students_collection.find_one({"student_id": student_id}, {"_id": 0, "password": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    quiz_scores = student.get("quiz_scores", [])
    
    # Calculate statistics
    total_quizzes = len(quiz_scores)
    average_score = calculate_average_score(quiz_scores)
    highest_score = max(quiz_scores) if quiz_scores else 0
    lowest_score = min(quiz_scores) if quiz_scores else 0
    
    # Trend analysis
    trend = "stable"
    if total_quizzes >= 2:
        recent_avg = sum(quiz_scores[-3:]) / min(3, len(quiz_scores))
        earlier_avg = sum(quiz_scores[:max(1, len(quiz_scores)-3)]) / max(1, len(quiz_scores)-3)
        if recent_avg > earlier_avg + 5:
            trend = "improving"
        elif recent_avg < earlier_avg - 5:
            trend = "declining"
    
    return {
        **student,
        "statistics": {
            "total_quizzes": total_quizzes,
            "average_score": round(average_score, 2),
            "highest_score": round(highest_score, 2),
            "lowest_score": round(lowest_score, 2),
            "trend": trend
        },
        "quiz_history": [
            {"quiz": f"Quiz {i+1}", "score": round(score, 2), "attempt": i+1}
            for i, score in enumerate(quiz_scores)
        ]
    }
