"""
Teacher routes
Handles teacher authentication and student progress analytics
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from database import teachers_collection, students_collection, results_collection, quizzes_collection, pathways_collection
from models import Teacher, TeacherResponse, LoginRequest, StudentProgress

router = APIRouter()


@router.post("/login")
async def login_teacher(login_data: LoginRequest):
    """
    Authenticate teacher login
    Returns teacher data if credentials are valid
    """
    # Check if database connection is available
    if teachers_collection is None:
        raise HTTPException(
            status_code=503, 
            detail="Database not connected. Please check MongoDB connection and initialize database with: python init_db.py"
        )
    
    teacher = teachers_collection.find_one({"email": login_data.email, "password": login_data.password})
    if not teacher:
        # Check if any teachers exist (for better error message)
        teacher_count = teachers_collection.count_documents({})
        if teacher_count == 0:
            raise HTTPException(
                status_code=401, 
                detail="No teachers found in database. Please run: python init_db.py to create sample data"
            )
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Remove sensitive data
    teacher.pop("password", None)
    teacher.pop("_id", None)
    return teacher


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(teacher_id: str):
    """
    Get teacher information by ID
    """
    teacher = teachers_collection.find_one({"teacher_id": teacher_id}, {"_id": 0, "password": 0})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.get("/", response_model=List[TeacherResponse])
async def get_all_teachers():
    """
    Get all teachers (for admin/testing purposes)
    """
    teachers = list(teachers_collection.find({}, {"password": 0, "_id": 0}))
    return teachers


@router.get("/students/progress", response_model=List[StudentProgress])
async def get_all_students_progress():
    """
    Get progress data for all students
    Includes pathways, quiz results, and weaknesses
    """
    if students_collection is None or results_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    students = list(students_collection.find({}, {"password": 0, "_id": 0}))
    student_progress_list = []
    
    for student in students:
        student_id = student["student_id"]
        
        # Get all results for this student
        results = list(results_collection.find({"student_id": student_id}, {"_id": 0}))
        
        # Calculate progress
        total_quizzes_completed = len(results)
        total_score = sum(r.get("percentage", 0) for r in results)
        average_score = total_score / total_quizzes_completed if total_quizzes_completed > 0 else 0
        
        # Get pathways the student is learning
        pathway_ids = set(r.get("pathway_id") for r in results if r.get("pathway_id"))
        pathways_info = []
        
        for pathway_id in pathway_ids:
            pathway = pathways_collection.find_one({"pathway_id": pathway_id}, {"_id": 0})
            if pathway:
                # Get quiz results for this pathway
                pathway_results = [r for r in results if r.get("pathway_id") == pathway_id]
                pathway_avg = sum(r.get("percentage", 0) for r in pathway_results) / len(pathway_results) if pathway_results else 0
                
                pathways_info.append({
                    "pathway_id": pathway_id,
                    "name": pathway.get("name"),
                    "level": pathway.get("level"),
                    "quizzes_completed": len(pathway_results),
                    "average_score": pathway_avg,
                    "latest_result": max(pathway_results, key=lambda x: x.get("submitted_at", "")) if pathway_results else None
                })
        
        # Identify weaknesses (quizzes with scores below 70%)
        weaknesses = []
        for result in results:
            if result.get("percentage", 0) < 70:
                quiz_id = result.get("quiz_id")
                quiz = quizzes_collection.find_one({"quiz_id": quiz_id}, {"_id": 0})
                if quiz:
                    pathway_id = result.get("pathway_id")
                    pathway = pathways_collection.find_one({"pathway_id": pathway_id}, {"_id": 0})
                    
                    # Analyze incorrect answers
                    wrong_answers = []
                    quiz_questions = quiz.get("questions", [])
                    student_answers = result.get("answers", {})
                    
                    for question in quiz_questions:
                        question_id = question.get("question_id")
                        correct_answer = question.get("correct_answer")
                        student_answer = student_answers.get(question_id)
                        
                        if student_answer != correct_answer:
                            wrong_answers.append({
                                "question_id": question_id,
                                "question_text": question.get("question_text"),
                                "correct_answer": correct_answer,
                                "student_answer": student_answer
                            })
                    
                    weaknesses.append({
                        "quiz_id": quiz_id,
                        "quiz_title": quiz.get("title"),
                        "pathway_id": pathway_id,
                        "pathway_name": pathway.get("name") if pathway else "Unknown",
                        "score": result.get("percentage", 0),
                        "submitted_at": result.get("submitted_at"),
                        "wrong_answers": wrong_answers,
                        "weak_areas": [q.get("question_text", "") for q in wrong_answers[:3]]  # Top 3 weak areas
                    })
        
        student_progress = {
            "student_id": student_id,
            "name": student.get("name"),
            "email": student.get("email"),
            "cumulative_score": student.get("cumulative_score", 0.0),
            "pathways": pathways_info,
            "total_quizzes_completed": total_quizzes_completed,
            "average_score": average_score,
            "weaknesses": weaknesses
        }
        
        student_progress_list.append(student_progress)
    
    return student_progress_list


@router.get("/students/{student_id}/progress", response_model=StudentProgress)
async def get_student_progress(student_id: str):
    """
    Get detailed progress for a specific student
    """
    if students_collection is None or results_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    student = students_collection.find_one({"student_id": student_id}, {"password": 0, "_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get all results for this student
    results = list(results_collection.find({"student_id": student_id}, {"_id": 0}))
    
    # Calculate progress
    total_quizzes_completed = len(results)
    total_score = sum(r.get("percentage", 0) for r in results)
    average_score = total_score / total_quizzes_completed if total_quizzes_completed > 0 else 0
    
    # Get pathways the student is learning
    pathway_ids = set(r.get("pathway_id") for r in results if r.get("pathway_id"))
    pathways_info = []
    
    for pathway_id in pathway_ids:
        pathway = pathways_collection.find_one({"pathway_id": pathway_id}, {"_id": 0})
        if pathway:
            # Get quiz results for this pathway
            pathway_results = [r for r in results if r.get("pathway_id") == pathway_id]
            pathway_avg = sum(r.get("percentage", 0) for r in pathway_results) / len(pathway_results) if pathway_results else 0
            
            pathways_info.append({
                "pathway_id": pathway_id,
                "name": pathway.get("name"),
                "level": pathway.get("level"),
                "quizzes_completed": len(pathway_results),
                "average_score": pathway_avg,
                "latest_result": max(pathway_results, key=lambda x: x.get("submitted_at", "")) if pathway_results else None
            })
    
    # Identify weaknesses (quizzes with scores below 70%)
    weaknesses = []
    for result in results:
        if result.get("percentage", 0) < 70:
            quiz_id = result.get("quiz_id")
            quiz = quizzes_collection.find_one({"quiz_id": quiz_id}, {"_id": 0})
            if quiz:
                pathway_id = result.get("pathway_id")
                pathway = pathways_collection.find_one({"pathway_id": pathway_id}, {"_id": 0})
                
                # Analyze incorrect answers
                wrong_answers = []
                quiz_questions = quiz.get("questions", [])
                student_answers = result.get("answers", {})
                
                for question in quiz_questions:
                    question_id = question.get("question_id")
                    correct_answer = question.get("correct_answer")
                    student_answer = student_answers.get(question_id)
                    
                    if student_answer != correct_answer:
                        wrong_answers.append({
                            "question_id": question_id,
                            "question_text": question.get("question_text"),
                            "correct_answer": correct_answer,
                            "student_answer": student_answer
                        })
                
                weaknesses.append({
                    "quiz_id": quiz_id,
                    "quiz_title": quiz.get("title"),
                    "pathway_id": pathway_id,
                    "pathway_name": pathway.get("name") if pathway else "Unknown",
                    "score": result.get("percentage", 0),
                    "submitted_at": result.get("submitted_at"),
                    "wrong_answers": wrong_answers,
                    "weak_areas": [q.get("question_text", "") for q in wrong_answers[:3]]  # Top 3 weak areas
                })
    
    student_progress = {
        "student_id": student_id,
        "name": student.get("name"),
        "email": student.get("email"),
        "cumulative_score": student.get("cumulative_score", 0.0),
        "pathways": pathways_info,
        "total_quizzes_completed": total_quizzes_completed,
        "average_score": average_score,
        "weaknesses": weaknesses
    }
    
    return student_progress



