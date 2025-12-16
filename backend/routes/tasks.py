"""
Task Assignment Routes
Handles task assignment by teachers and task retrieval by students
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
import uuid
from database import tasks_collection, students_collection, teachers_collection, quizzes_collection
from models import TaskAssignment, TaskAssignmentRequest
from middleware.auth_middleware import require_teacher, get_current_user

router = APIRouter()


@router.post("/assign")
async def assign_tasks(
    task_request: TaskAssignmentRequest,
    current_user: dict = Depends(require_teacher)
):
    """
    Assign tasks to multiple students
    Only teachers can assign tasks
    """
    if tasks_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    teacher_id = current_user.get("user_id")
    
    if not teacher_id:
        raise HTTPException(status_code=400, detail="Teacher ID not found in token")
    
    # Verify teacher exists
    teacher = teachers_collection.find_one({"teacher_id": teacher_id})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Verify all students exist
    for student_id in task_request.student_ids:
        student = students_collection.find_one({"student_id": student_id})
        if not student:
            raise HTTPException(
                status_code=404,
                detail=f"Student with ID {student_id} not found"
            )
    
    # Verify quiz exists if provided
    quiz_info = None
    if task_request.quiz_id:
        quiz = quizzes_collection.find_one({"quiz_id": task_request.quiz_id}, {"_id": 0})
        if not quiz:
            raise HTTPException(
                status_code=404,
                detail=f"Quiz with ID {task_request.quiz_id} not found"
            )
        quiz_info = {
            "quiz_id": quiz.get("quiz_id"),
            "quiz_title": quiz.get("title"),
            "quiz_description": quiz.get("description", "")
        }
    
    # Create tasks for each student
    tasks = []
    assigned_at = datetime.utcnow()
    
    for student_id in task_request.student_ids:
        task = {
            "task_id": f"task_{uuid.uuid4().hex[:12]}",
            "student_id": student_id,
            "teacher_id": teacher_id,
            "teacher_name": teacher.get("name", "Unknown Teacher"),
            "title": task_request.title,
            "description": task_request.description,
            "due_date": task_request.due_date,
            "status": "pending",
            "assigned_at": assigned_at.isoformat(),
            "completed_at": None,
            "quiz_id": task_request.quiz_id,
            "quiz_info": quiz_info
        }
        tasks.append(task)
    
    # Insert all tasks
    if tasks:
        tasks_collection.insert_many(tasks)
    
    return {
        "message": f"Successfully assigned task to {len(tasks)} student(s)",
        "tasks_assigned": len(tasks),
        "task_ids": [task["task_id"] for task in tasks]
    }


@router.get("/student/{student_id}")
async def get_student_tasks(
    student_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all tasks assigned to a student
    Students can only see their own tasks, teachers can see any student's tasks
    """
    if tasks_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    # Check if student can access this data
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Verify student exists
    student = students_collection.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get all tasks for this student
    tasks = list(tasks_collection.find(
        {"student_id": student_id},
        {"_id": 0}
    ).sort("assigned_at", -1))
    
    return {
        "student_id": student_id,
        "student_name": student.get("name"),
        "tasks": tasks,
        "total_tasks": len(tasks),
        "pending_tasks": len([t for t in tasks if t.get("status") == "pending"]),
        "completed_tasks": len([t for t in tasks if t.get("status") == "completed"])
    }


@router.get("/student/{student_id}/pending")
async def get_pending_tasks(
    student_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get only pending tasks for a student
    """
    if tasks_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    # Check if student can access this data
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get pending tasks
    tasks = list(tasks_collection.find(
        {"student_id": student_id, "status": "pending"},
        {"_id": 0}
    ).sort("due_date", 1))
    
    return {
        "student_id": student_id,
        "tasks": tasks,
        "count": len(tasks)
    }


@router.put("/{task_id}/status")
async def update_task_status(
    task_id: str,
    status: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Update task status (pending, in-progress, completed)
    Students can update their own tasks
    """
    if tasks_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    if status not in ["pending", "in-progress", "completed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status. Must be: pending, in-progress, or completed"
        )
    
    # Get task
    task = tasks_collection.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if user can update this task
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and task.get("student_id") != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Update task status
    update_data = {"status": status}
    
    if status == "completed":
        update_data["completed_at"] = datetime.utcnow().isoformat()
    
    tasks_collection.update_one(
        {"task_id": task_id},
        {"$set": update_data}
    )
    
    return {
        "message": f"Task status updated to {status}",
        "task_id": task_id,
        "status": status
    }


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: dict = Depends(require_teacher)
):
    """
    Delete a task (only teachers can delete)
    """
    if tasks_collection is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    task = tasks_collection.find_one({"task_id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    tasks_collection.delete_one({"task_id": task_id})
    
    return {
        "message": "Task deleted successfully",
        "task_id": task_id
    }

