"""
Adaptive Learning Routes
Handles mastery tracking, recommendations, and pathway adjustments
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from database import concept_mastery_collection, recommendations_collection
from middleware.auth_middleware import get_current_user
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.adaptive_learning_service import AdaptiveLearningService

router = APIRouter()


@router.get("/mastery/{student_id}")
async def get_student_mastery(
    student_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get concept mastery for a student"""
    # Check authorization
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
    
    if not mastery_doc:
        raise HTTPException(status_code=404, detail="Mastery data not found")
    
    return mastery_doc


@router.get("/weak-areas/{student_id}")
async def get_weak_areas(
    student_id: str,
    threshold: float = 0.6,
    current_user: dict = Depends(get_current_user)
):
    """Get weak areas for a student"""
    # Check authorization
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    weak_areas = AdaptiveLearningService.identify_weak_areas(student_id, threshold)
    
    return {
        "student_id": student_id,
        "weak_areas": weak_areas,
        "count": len(weak_areas),
        "threshold": threshold
    }


@router.get("/recommendations/{student_id}")
async def get_recommendations(
    student_id: str,
    regenerate: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """Get personalized recommendations for a student"""
    # Check authorization
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if regenerate:
        recommendations = AdaptiveLearningService.generate_recommendations(student_id)
    else:
        recommendations = AdaptiveLearningService.get_recommendations(student_id)
    
    return {
        "student_id": student_id,
        "recommendations": recommendations,
        "count": len(recommendations)
    }


@router.post("/adjust-pathway/{student_id}")
async def adjust_pathway_endpoint(
    student_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Manually trigger pathway adjustment"""
    # Check authorization
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    new_pathway = AdaptiveLearningService.adjust_pathway(student_id)
    
    if new_pathway:
        return {
            "message": "Pathway adjusted successfully",
            "new_pathway": new_pathway,
            "student_id": student_id
        }
    else:
        return {
            "message": "Pathway adjustment not needed",
            "student_id": student_id
        }


@router.get("/analytics/{student_id}")
async def get_learning_analytics(
    student_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get comprehensive learning analytics"""
    # Check authorization
    user_role = current_user.get("role")
    user_id = current_user.get("user_id")
    
    if user_role == "student" and user_id != student_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    mastery_doc = AdaptiveLearningService.get_student_mastery(student_id)
    weak_areas = AdaptiveLearningService.identify_weak_areas(student_id)
    recommendations = AdaptiveLearningService.get_recommendations(student_id)
    should_adjust = AdaptiveLearningService.should_adjust_pathway(student_id)
    
    return {
        "student_id": student_id,
        "overall_mastery": mastery_doc.get("overall_mastery", 0.0),
        "concepts_count": len(mastery_doc.get("concepts", {})),
        "weak_areas_count": len(weak_areas),
        "recommendations_count": len(recommendations),
        "pathway_adjustment_needed": should_adjust,
        "last_updated": mastery_doc.get("last_updated")
    }





















