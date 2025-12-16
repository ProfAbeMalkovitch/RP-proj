"""
Roadmap Generation API Routes
High-standard endpoints for roadmap template management and generation
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId

from database import (
    roadmap_templates_collection,
    generated_roadmaps_collection,
    teachers_collection
)
from models import (
    RoadmapTemplate,
    RoadmapTemplateCreate,
    RoadmapTemplateUpdate,
    GeneratedRoadmap,
    RoadmapGenerationRequest,
    RoadmapGenerationResponse
)
from services.roadmap_generation_service import RoadmapGenerationService

router = APIRouter()


# ==================== Template Management (Teacher) ====================

@router.post("/templates", response_model=RoadmapTemplate)
async def create_template(template_data: RoadmapTemplateCreate, teacher_id: str = Query(...)):
    """
    Create a new roadmap template
    Requires teacher authentication
    """
    try:
        # Verify teacher exists
        teacher = teachers_collection.find_one({"teacher_id": teacher_id})
        if not teacher:
            raise HTTPException(status_code=404, detail="Teacher not found")
        
        # Generate template ID
        template_id = f"template_{ObjectId()}"
        
        # Convert tasks to proper format
        formatted_tasks = []
        for idx, task in enumerate(template_data.tasks, 1):
            formatted_task = {
                "task_id": task.get("task_id") or f"{template_id}_task_{idx}",
                "title": task["title"],
                "description": task.get("description", ""),
                "task_type": task.get("task_type", "reading"),
                "order": task.get("order", idx),
                "estimated_time": task.get("estimated_time", 60),
                "difficulty": task.get("difficulty", "intermediate"),
                "learning_objectives": task.get("learning_objectives", []),
                "quiz_id": task.get("quiz_id"),
                "resource_url": task.get("resource_url"),
                "prerequisites": task.get("prerequisites", []),
                "tags": task.get("tags", [])
            }
            formatted_tasks.append(formatted_task)
        
        # Create template document
        template_doc = {
            "template_id": template_id,
            "name": template_data.name,
            "description": template_data.description,
            "created_by": teacher_id,
            "target_concepts": template_data.target_concepts,
            "pathway_level": template_data.pathway_level,
            "difficulty": template_data.difficulty,
            "weak_area_focus": template_data.weak_area_focus,
            "mastery_focus": template_data.mastery_focus,
            "tasks": formatted_tasks,
            "prerequisites": template_data.prerequisites,
            "estimated_total_time": template_data.estimated_total_time or sum(
                t.get("estimated_time", 60) for t in formatted_tasks
            ),
            "learning_outcomes": template_data.learning_outcomes,
            "tags": template_data.tags,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        }
        
        # Insert into database
        roadmap_templates_collection.insert_one(template_doc)
        
        return template_doc
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create template: {str(e)}")


@router.get("/templates", response_model=List[RoadmapTemplate])
async def get_all_templates(
    teacher_id: Optional[str] = Query(None),
    pathway_level: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    weak_area_focus: Optional[bool] = Query(None)
):
    """
    Get all roadmap templates with optional filters
    """
    try:
        query = {}
        
        if teacher_id:
            query["created_by"] = teacher_id
        
        if pathway_level:
            query["pathway_level"] = pathway_level
        
        if is_active is not None:
            query["is_active"] = is_active
        
        if weak_area_focus is not None:
            query["weak_area_focus"] = weak_area_focus
        
        templates = list(roadmap_templates_collection.find(query).sort("created_at", -1))
        
        return templates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch templates: {str(e)}")


@router.get("/templates/{template_id}", response_model=RoadmapTemplate)
async def get_template(template_id: str):
    """
    Get a specific template by ID
    """
    try:
        template = roadmap_templates_collection.find_one({"template_id": template_id})
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch template: {str(e)}")


@router.put("/templates/{template_id}", response_model=RoadmapTemplate)
async def update_template(
    template_id: str,
    update_data: RoadmapTemplateUpdate,
    teacher_id: str = Query(...)
):
    """
    Update an existing template
    Only the creator can update
    """
    try:
        # Verify template exists and teacher is creator
        template = roadmap_templates_collection.find_one({"template_id": template_id})
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        if template.get("created_by") != teacher_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this template")
        
        # Build update document
        update_doc = {"updated_at": datetime.now()}
        
        if update_data.name is not None:
            update_doc["name"] = update_data.name
        
        if update_data.description is not None:
            update_doc["description"] = update_data.description
        
        if update_data.target_concepts is not None:
            update_doc["target_concepts"] = update_data.target_concepts
        
        if update_data.pathway_level is not None:
            update_doc["pathway_level"] = update_data.pathway_level
        
        if update_data.difficulty is not None:
            update_doc["difficulty"] = update_data.difficulty
        
        if update_data.weak_area_focus is not None:
            update_doc["weak_area_focus"] = update_data.weak_area_focus
        
        if update_data.mastery_focus is not None:
            update_doc["mastery_focus"] = update_data.mastery_focus
        
        if update_data.tasks is not None:
            # Reformat tasks
            formatted_tasks = []
            for idx, task in enumerate(update_data.tasks, 1):
                formatted_task = {
                    "task_id": task.get("task_id") or f"{template_id}_task_{idx}",
                    "title": task["title"],
                    "description": task.get("description", ""),
                    "task_type": task.get("task_type", "reading"),
                    "order": task.get("order", idx),
                    "estimated_time": task.get("estimated_time", 60),
                    "difficulty": task.get("difficulty", "intermediate"),
                    "learning_objectives": task.get("learning_objectives", []),
                    "quiz_id": task.get("quiz_id"),
                    "resource_url": task.get("resource_url"),
                    "prerequisites": task.get("prerequisites", []),
                    "tags": task.get("tags", [])
                }
                formatted_tasks.append(formatted_task)
            
            update_doc["tasks"] = formatted_tasks
            update_doc["estimated_total_time"] = sum(
                t.get("estimated_time", 60) for t in formatted_tasks
            )
        
        if update_data.prerequisites is not None:
            update_doc["prerequisites"] = update_data.prerequisites
        
        if update_data.estimated_total_time is not None:
            update_doc["estimated_total_time"] = update_data.estimated_total_time
        
        if update_data.learning_outcomes is not None:
            update_doc["learning_outcomes"] = update_data.learning_outcomes
        
        if update_data.tags is not None:
            update_doc["tags"] = update_data.tags
        
        if update_data.is_active is not None:
            update_doc["is_active"] = update_data.is_active
        
        # Update in database
        roadmap_templates_collection.update_one(
            {"template_id": template_id},
            {"$set": update_doc}
        )
        
        # Fetch updated template
        updated_template = roadmap_templates_collection.find_one({"template_id": template_id})
        
        return updated_template
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update template: {str(e)}")


@router.delete("/templates/{template_id}")
async def delete_template(template_id: str, teacher_id: str = Query(...)):
    """
    Delete a template (soft delete by setting is_active=False)
    """
    try:
        # Verify template exists and teacher is creator
        template = roadmap_templates_collection.find_one({"template_id": template_id})
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        if template.get("created_by") != teacher_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this template")
        
        # Soft delete
        roadmap_templates_collection.update_one(
            {"template_id": template_id},
            {"$set": {"is_active": False, "updated_at": datetime.now()}}
        )
        
        return {"message": "Template deleted successfully", "template_id": template_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete template: {str(e)}")


# ==================== Roadmap Generation (Student) ====================

@router.post("/generate", response_model=RoadmapGenerationResponse)
async def generate_roadmap(request: RoadmapGenerationRequest):
    """
    Generate a personalized roadmap for a student
    """
    try:
        result = RoadmapGenerationService.generate_roadmap(
            student_id=request.student_id,
            regenerate=request.regenerate,
            focus_areas=request.focus_areas,
            template_ids=request.template_ids,
            max_tasks=request.max_tasks
        )
        
        if 'error' in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        roadmap = result['roadmap']
        generation_metadata = result.get('generation_metadata', {})
        matching_templates = result.get('matching_templates', [])
        reasoning = result.get('reasoning', '')
        
        return {
            "roadmap": roadmap,
            "generation_metadata": generation_metadata,
            "matching_templates": matching_templates,
            "reasoning": reasoning
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate roadmap: {str(e)}")


@router.get("/student/{student_id}", response_model=List[GeneratedRoadmap])
async def get_student_roadmaps(
    student_id: str,
    status: Optional[str] = Query(None),
    include_archived: bool = Query(False)
):
    """
    Get all roadmaps for a student
    """
    try:
        query = {"student_id": student_id}
        
        if status:
            query["status"] = status
        elif not include_archived:
            query["status"] = {"$ne": "archived"}
        
        roadmaps = list(
            generated_roadmaps_collection.find(query)
            .sort("generated_at", -1)
        )
        
        return roadmaps
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch roadmaps: {str(e)}")


@router.get("/student/{student_id}/active", response_model=GeneratedRoadmap)
async def get_active_roadmap(student_id: str):
    """
    Get the active roadmap for a student
    """
    try:
        roadmap = generated_roadmaps_collection.find_one(
            {
                "student_id": student_id,
                "status": "active"
            },
            sort=[("generated_at", -1)]
        )
        
        if not roadmap:
            raise HTTPException(status_code=404, detail="No active roadmap found")
        
        return roadmap
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch roadmap: {str(e)}")


@router.put("/roadmap/{roadmap_id}/status")
async def update_roadmap_status(
    roadmap_id: str,
    status: str = Query(..., regex="^(pending|active|completed|archived)$"),
    teacher_id: Optional[str] = Query(None)
):
    """
    Update roadmap status
    Teacher can approve (pending -> active), student can complete (active -> completed)
    """
    try:
        roadmap = generated_roadmaps_collection.find_one({"roadmap_id": roadmap_id})
        
        if not roadmap:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        update_doc = {"status": status}
        
        # If approving (pending -> active) and teacher_id provided
        if status == "active" and roadmap.get("status") == "pending" and teacher_id:
            update_doc["approved_by"] = teacher_id
            update_doc["approved_at"] = datetime.now()
        
        # If completing, set completion date
        if status == "completed":
            update_doc["actual_completion_date"] = datetime.now()
        
        generated_roadmaps_collection.update_one(
            {"roadmap_id": roadmap_id},
            {"$set": update_doc}
        )
        
        return {"message": f"Roadmap status updated to {status}", "roadmap_id": roadmap_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update status: {str(e)}")


@router.put("/roadmap/{roadmap_id}/task/{task_id}/complete")
async def mark_task_complete(roadmap_id: str, task_id: str):
    """
    Mark a task as complete in a roadmap
    """
    try:
        roadmap = generated_roadmaps_collection.find_one({"roadmap_id": roadmap_id})
        
        if not roadmap:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        # Find and update task
        tasks = roadmap.get("tasks", [])
        task_found = False
        
        for task in tasks:
            if task.get("task_id") == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now()
                task_found = True
                break
        
        if not task_found:
            raise HTTPException(status_code=404, detail="Task not found in roadmap")
        
        # Update completed tasks count
        completed_count = sum(1 for task in tasks if task.get("completed", False))
        
        # Update roadmap
        generated_roadmaps_collection.update_one(
            {"roadmap_id": roadmap_id},
            {
                "$set": {
                    "tasks": tasks,
                    "completed_tasks": completed_count,
                    "updated_at": datetime.now()
                }
            }
        )
        
        # Auto-complete roadmap if all tasks done
        if completed_count >= roadmap.get("total_tasks", 0):
            generated_roadmaps_collection.update_one(
                {"roadmap_id": roadmap_id},
                {
                    "$set": {
                        "status": "completed",
                        "actual_completion_date": datetime.now()
                    }
                }
            )
        
        return {"message": "Task marked as complete", "task_id": task_id}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark task complete: {str(e)}")


# ==================== Teacher Dashboard - Roadmap Management ====================

@router.get("/teacher/{teacher_id}/student-roadmaps")
async def get_student_roadmaps_for_teacher(
    teacher_id: str,
    status: Optional[str] = Query(None)
):
    """
    Get all student roadmaps for teacher monitoring
    """
    try:
        query = {}
        
        if status:
            query["status"] = status
        else:
            query["status"] = {"$in": ["pending", "active"]}
        
        roadmaps = list(
            generated_roadmaps_collection.find(query)
            .sort("generated_at", -1)
        )
        
        return {
            "teacher_id": teacher_id,
            "total_roadmaps": len(roadmaps),
            "roadmaps": roadmaps
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch roadmaps: {str(e)}")

