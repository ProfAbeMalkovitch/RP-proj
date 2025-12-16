"""
Pathway routes
Handles learning pathway information retrieval
"""

from fastapi import APIRouter, HTTPException
from typing import List
from database import pathways_collection
from models import Pathway

router = APIRouter()


@router.get("/", response_model=List[Pathway])
async def get_all_pathways():
    """
    Get all available learning pathways
    Returns list of Basic, Intermediate, and Excellent pathways
    """
    pathways = list(pathways_collection.find({}, {"_id": 0}))
    if not pathways:
        raise HTTPException(status_code=404, detail="No pathways found")
    return pathways


@router.get("/level/{level}", response_model=List[Pathway])
async def get_pathways_by_level(level: str):
    """
    Get pathways by level (Basic, Intermediate, Excellent)
    """
    pathways = list(pathways_collection.find({"level": level}, {"_id": 0}))
    if not pathways:
        raise HTTPException(status_code=404, detail=f"No pathways found for level: {level}")
    return pathways


@router.get("/{pathway_id}", response_model=Pathway)
async def get_pathway(pathway_id: str):
    """
    Get specific pathway by ID
    Returns pathway details including content, topics, roadmap, and quiz IDs
    """
    pathway = pathways_collection.find_one({"pathway_id": pathway_id}, {"_id": 0})
    if not pathway:
        raise HTTPException(status_code=404, detail="Pathway not found")
    return pathway




