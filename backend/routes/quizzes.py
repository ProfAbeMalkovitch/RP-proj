"""
Quiz routes
Handles quiz data retrieval and import
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from database import quizzes_collection, pathways_collection
from models import Quiz, QuizResponse, QuizImportRequest, BulkQuizImportRequest
from middleware.auth_middleware import require_teacher, get_current_user

router = APIRouter()


@router.get("/", response_model=List[Quiz])
async def get_all_quizzes():
    """
    Get all available quizzes
    """
    quizzes = list(quizzes_collection.find({}, {"_id": 0}))
    return quizzes


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(quiz_id: str):
    """
    Get specific quiz by ID
    Returns quiz with questions (without correct answers for security)
    """
    quiz = quizzes_collection.find_one({"quiz_id": quiz_id}, {"_id": 0})
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Remove correct answers from questions for security
    quiz_for_student = quiz.copy()
    for question in quiz_for_student.get("questions", []):
        question.pop("correct_answer", None)
    
    return quiz_for_student


@router.get("/pathway/{pathway_id}", response_model=List[QuizResponse])
async def get_quizzes_by_pathway(pathway_id: str):
    """
    Get all quizzes for a specific pathway
    """
    quizzes = list(quizzes_collection.find({"pathway_id": pathway_id}, {"_id": 0}))
    
    # Remove correct answers for security
    for quiz in quizzes:
        for question in quiz.get("questions", []):
            question.pop("correct_answer", None)
    
    return quizzes


@router.post("/import", response_model=Dict[str, Any])
async def import_quiz(
    quiz_data: QuizImportRequest,
    current_user: dict = Depends(require_teacher)
):
    """
    Import a single quiz from external content provider
    Requires teacher authentication
    """
    if quizzes_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    # Verify pathway exists
    pathway = pathways_collection.find_one({"pathway_id": quiz_data.pathway_id})
    if not pathway:
        raise HTTPException(
            status_code=404,
            detail=f"Pathway '{quiz_data.pathway_id}' not found. Please create the pathway first."
        )
    
    # Check if quiz already exists
    existing_quiz = quizzes_collection.find_one({"quiz_id": quiz_data.quiz_id})
    if existing_quiz:
        raise HTTPException(
            status_code=409,
            detail=f"Quiz with ID '{quiz_data.quiz_id}' already exists. Use PUT /api/quizzes/{quiz_data.quiz_id} to update."
        )
    
    # Calculate total_points if not provided
    total_points = quiz_data.total_points
    if total_points is None:
        total_points = sum(q.points for q in quiz_data.questions)
    
    # Validate questions
    if not quiz_data.questions:
        raise HTTPException(status_code=400, detail="Quiz must have at least one question")
    
    for i, question in enumerate(quiz_data.questions):
        if not question.options:
            raise HTTPException(
                status_code=400,
                detail=f"Question {i+1} must have at least one option"
            )
        if question.correct_answer < 0 or question.correct_answer >= len(question.options):
            raise HTTPException(
                status_code=400,
                detail=f"Question {i+1}: correct_answer index out of range"
            )
    
    # Prepare quiz document
    quiz_doc = {
        "quiz_id": quiz_data.quiz_id,
        "pathway_id": quiz_data.pathway_id,
        "title": quiz_data.title,
        "description": quiz_data.description,
        "questions": [q.dict() for q in quiz_data.questions],
        "total_points": total_points
    }
    
    # Insert quiz
    try:
        quizzes_collection.insert_one(quiz_doc)
        return {
            "success": True,
            "message": f"Quiz '{quiz_data.quiz_id}' imported successfully",
            "quiz_id": quiz_data.quiz_id,
            "total_points": total_points,
            "questions_count": len(quiz_data.questions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to import quiz: {str(e)}")


@router.post("/import/bulk", response_model=Dict[str, Any])
async def import_quizzes_bulk(
    bulk_data: BulkQuizImportRequest,
    current_user: dict = Depends(require_teacher)
):
    """
    Import multiple quizzes at once from external content provider
    Requires teacher authentication
    """
    if quizzes_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    if not bulk_data.quizzes:
        raise HTTPException(status_code=400, detail="No quizzes provided")
    
    imported = []
    failed = []
    
    for quiz_data in bulk_data.quizzes:
        try:
            # Verify pathway exists
            pathway = pathways_collection.find_one({"pathway_id": quiz_data.pathway_id})
            if not pathway:
                failed.append({
                    "quiz_id": quiz_data.quiz_id,
                    "error": f"Pathway '{quiz_data.pathway_id}' not found"
                })
                continue
            
            # Check if quiz already exists
            existing_quiz = quizzes_collection.find_one({"quiz_id": quiz_data.quiz_id})
            if existing_quiz:
                failed.append({
                    "quiz_id": quiz_data.quiz_id,
                    "error": "Quiz already exists"
                })
                continue
            
            # Calculate total_points if not provided
            total_points = quiz_data.total_points
            if total_points is None:
                total_points = sum(q.points for q in quiz_data.questions)
            
            # Validate questions
            if not quiz_data.questions:
                failed.append({
                    "quiz_id": quiz_data.quiz_id,
                    "error": "Quiz must have at least one question"
                })
                continue
            
            validation_error = None
            for i, question in enumerate(quiz_data.questions):
                if not question.options:
                    validation_error = f"Question {i+1} must have at least one option"
                    break
                if question.correct_answer < 0 or question.correct_answer >= len(question.options):
                    validation_error = f"Question {i+1}: correct_answer index out of range"
                    break
            
            if validation_error:
                failed.append({
                    "quiz_id": quiz_data.quiz_id,
                    "error": validation_error
                })
                continue
            
            # Prepare quiz document
            quiz_doc = {
                "quiz_id": quiz_data.quiz_id,
                "pathway_id": quiz_data.pathway_id,
                "title": quiz_data.title,
                "description": quiz_data.description,
                "questions": [q.dict() for q in quiz_data.questions],
                "total_points": total_points
            }
            
            # Insert quiz
            quizzes_collection.insert_one(quiz_doc)
            imported.append({
                "quiz_id": quiz_data.quiz_id,
                "title": quiz_data.title,
                "questions_count": len(quiz_data.questions),
                "total_points": total_points
            })
        except Exception as e:
            failed.append({
                "quiz_id": quiz_data.quiz_id,
                "error": str(e)
            })
    
    return {
        "success": len(failed) == 0,
        "imported_count": len(imported),
        "failed_count": len(failed),
        "imported": imported,
        "failed": failed
    }


@router.post("/validate", response_model=Dict[str, Any])
async def validate_quiz_format(quiz_data: QuizImportRequest):
    """
    Validate quiz format without importing
    Useful for testing quiz structure before import
    No authentication required (validation only)
    """
    errors = []
    warnings = []
    
    # Check required fields
    if not quiz_data.quiz_id:
        errors.append("quiz_id is required")
    if not quiz_data.pathway_id:
        errors.append("pathway_id is required")
    if not quiz_data.title:
        errors.append("title is required")
    if not quiz_data.description:
        warnings.append("description is empty")
    
    # Validate questions
    if not quiz_data.questions:
        errors.append("Quiz must have at least one question")
    else:
        for i, question in enumerate(quiz_data.questions):
            if not question.question_id:
                errors.append(f"Question {i+1}: question_id is required")
            if not question.question_text:
                errors.append(f"Question {i+1}: question_text is required")
            if not question.options:
                errors.append(f"Question {i+1}: must have at least one option")
            elif len(question.options) < 2:
                warnings.append(f"Question {i+1}: has less than 2 options (recommended: 4)")
            else:
                if question.correct_answer < 0 or question.correct_answer >= len(question.options):
                    errors.append(
                        f"Question {i+1}: correct_answer index ({question.correct_answer}) "
                        f"is out of range (0-{len(question.options)-1})"
                    )
            if question.points <= 0:
                warnings.append(f"Question {i+1}: points should be greater than 0")
    
    # Calculate total points
    calculated_points = sum(q.points for q in quiz_data.questions) if quiz_data.questions else 0
    if quiz_data.total_points and quiz_data.total_points != calculated_points:
        warnings.append(
            f"total_points ({quiz_data.total_points}) doesn't match sum of question points ({calculated_points})"
        )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "calculated_total_points": calculated_points,
        "questions_count": len(quiz_data.questions) if quiz_data.questions else 0
    }




