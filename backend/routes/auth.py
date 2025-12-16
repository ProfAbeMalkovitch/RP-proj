"""
Authentication Routes
Separate login endpoints for students, teachers, and admins
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from controllers.auth_controller import login_student, login_teacher, login_admin
from models import LoginResponse

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str


@router.post("/student/login", response_model=LoginResponse)
async def student_login(login_data: LoginRequest):
    """Student login endpoint"""
    return await login_student(login_data.email, login_data.password)


@router.post("/teacher/login", response_model=LoginResponse)
async def teacher_login(login_data: LoginRequest):
    """Teacher login endpoint"""
    return await login_teacher(login_data.email, login_data.password)


@router.post("/admin/login", response_model=LoginResponse)
async def admin_login(login_data: LoginRequest):
    """Admin login endpoint"""
    return await login_admin(login_data.email, login_data.password)





































