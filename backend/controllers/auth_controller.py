"""
Authentication Controller
Handles login for students, teachers, and admins with JWT
"""

from fastapi import HTTPException, status
from database import students_collection, teachers_collection, admins_collection
from utils.jwt_auth import create_access_token
from utils.password import verify_password
from models import LoginResponse
from typing import Dict


async def login_student(email: str, password: str) -> LoginResponse:
    """Authenticate student and return JWT token"""
    if students_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    # Normalize email to lowercase for case-insensitive lookup
    email_lower = email.lower().strip()
    # Try exact match first (faster), then case-insensitive regex if needed
    student = students_collection.find_one({"email": email_lower})
    if not student:
        # Try case-insensitive lookup
        student = students_collection.find_one({"email": {"$regex": f"^{email_lower}$", "$options": "i"}})
    
    if not student:
        # Check if any students exist for better error message
        total_students = students_collection.count_documents({})
        if total_students == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No students found in database. Please run: python seeders/seed_students.py"
            )
        # Get a sample email to help user
        sample = students_collection.find_one({}, {"email": 1})
        sample_email = sample.get("email", "") if sample else ""
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid email or password. Email '{email}' not found. Use a valid student email (e.g., {sample_email})"
        )
    
    # Verify password (handle both hashed and plain text for backward compatibility)
    stored_password = student.get("password", "")
    if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
        # Password is hashed
        if not verify_password(password, stored_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    else:
        # Password is plain text (backward compatibility)
        if password != stored_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    # Create JWT token
    token_data = {
        "user_id": student["student_id"],
        "email": student["email"],
        "role": "student"
    }
    access_token = create_access_token(data=token_data)
    
    # Prepare user data
    user_data = {
        "user_id": student["student_id"],
        "name": student["name"],
        "email": student["email"],
        "role": "student",
        "pathway": student.get("pathway", "Basic"),
        "quiz_scores": student.get("quiz_scores", []),
        "average_score": student.get("average_score", 0.0)
    }
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data,
        role="student"
    )


async def login_teacher(email: str, password: str) -> LoginResponse:
    """Authenticate teacher and return JWT token"""
    if teachers_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    teacher = teachers_collection.find_one({"email": email})
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password (handle both hashed and plain text for backward compatibility)
    stored_password = teacher.get("password", "")
    if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
        # Password is hashed
        if not verify_password(password, stored_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    else:
        # Password is plain text (backward compatibility)
        if password != stored_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    # Create JWT token
    token_data = {
        "user_id": teacher["teacher_id"],
        "email": teacher["email"],
        "role": "teacher"
    }
    access_token = create_access_token(data=token_data)
    
    # Prepare user data
    user_data = {
        "user_id": teacher["teacher_id"],
        "name": teacher["name"],
        "email": teacher["email"],
        "role": "teacher"
    }
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data,
        role="teacher"
    )


async def login_admin(email: str, password: str) -> LoginResponse:
    """Authenticate admin and return JWT token"""
    if admins_collection is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    admin = admins_collection.find_one({"email": email})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password (handle both hashed and plain text for backward compatibility)
    stored_password = admin.get("password", "")
    if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
        # Password is hashed
        if not verify_password(password, stored_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    else:
        # Password is plain text (backward compatibility)
        if password != stored_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
    
    # Create JWT token
    token_data = {
        "user_id": admin["admin_id"],
        "email": admin["email"],
        "role": "admin"
    }
    access_token = create_access_token(data=token_data)
    
    # Prepare user data
    user_data = {
        "user_id": admin["admin_id"],
        "name": admin["name"],
        "email": admin["email"],
        "role": "admin"
    }
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_data,
        role="admin"
    )







