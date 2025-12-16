"""
Student routes
Handles student authentication and data retrieval
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from database import students_collection
from models import Student, StudentResponse, LoginRequest
from middleware.auth_middleware import require_student, get_current_user

router = APIRouter()


def get_student_by_id(student_id: str):
    """Helper function to get student by ID"""
    student = students_collection.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    # Remove password from response
    student.pop("password", None)
    student.pop("_id", None)
    return student


@router.post("/login")
async def login_student(login_data: LoginRequest):
    """
    Authenticate student login
    Returns student data if credentials are valid
    """
    # Check if database connection is available
    if students_collection is None:
        raise HTTPException(
            status_code=503, 
            detail="Database not connected. Please check MongoDB connection and initialize database with: python init_db.py"
        )
    
    student = students_collection.find_one({"email": login_data.email, "password": login_data.password})
    if not student:
        # Check if any students exist (for better error message)
        student_count = students_collection.count_documents({})
        if student_count == 0:
            raise HTTPException(
                status_code=401, 
                detail="No students found in database. Please run: python init_db.py to create sample data"
            )
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Remove sensitive data
    student.pop("password", None)
    student.pop("_id", None)
    return student


@router.get("/me")
async def get_current_student_data(current_user: dict = Depends(require_student)):
    """
    Get current logged-in student's data
    """
    student_id = current_user.get("user_id")
    student = students_collection.find_one({"student_id": student_id}, {"_id": 0, "password": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    """
    Get student information by ID
    """
    return get_student_by_id(student_id)


@router.get("/", response_model=List[StudentResponse])
async def get_all_students():
    """
    Get all students (for admin/testing purposes)
    """
    students = list(students_collection.find({}, {"password": 0, "_id": 0}))
    return students

