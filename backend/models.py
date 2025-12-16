"""
Data models for request/response validation
Uses Pydantic for data validation
"""

from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime


class Student(BaseModel):
    """Student model"""
    student_id: str
    name: str
    email: EmailStr
    password: str  # In production, this should be hashed
    quiz_scores: List[float] = []  # Array of quiz scores (percentages)
    pathway: str = "Basic"  # Auto-calculated: Basic (0-49), Intermediate (50-74), Accelerated (75-100)
    average_score: float = 0.0
    cumulative_score: float = 0.0


class StudentResponse(BaseModel):
    """Student response model (without password)"""
    student_id: str
    name: str
    email: str
    quiz_scores: List[float]
    pathway: str
    average_score: float
    cumulative_score: float


class Pathway(BaseModel):
    """Learning pathway model"""
    pathway_id: str
    name: str
    level: str  # Basic, Intermediate, Excellent
    description: str
    content: str
    topics: List[Dict[str, Any]]  # For mind map
    roadmap: List[Dict[str, Any]]  # List of tasks
    quiz_ids: List[str]  # Associated quiz IDs


class QuizQuestion(BaseModel):
    """Individual quiz question model"""
    question_id: str
    question_text: str
    options: List[str]
    correct_answer: int  # Index of correct option
    points: int = 10


class QuizQuestionResponse(BaseModel):
    """Quiz question response model (without correct answer for security)"""
    question_id: str
    question_text: str
    options: List[str]
    points: int = 10


class Quiz(BaseModel):
    """Quiz model"""
    quiz_id: str
    pathway_id: str
    title: str
    description: str
    questions: List[QuizQuestion]
    total_points: int


class QuizResponse(BaseModel):
    """Quiz response model (without correct answers for security)"""
    quiz_id: str
    pathway_id: str
    title: str
    description: str
    questions: List[QuizQuestionResponse]
    total_points: int


class QuizSubmission(BaseModel):
    """Quiz submission model"""
    student_id: str
    quiz_id: str
    answers: Dict[str, int]  # question_id -> selected_option_index


class QuizResult(BaseModel):
    """Quiz result model"""
    result_id: str
    student_id: str
    quiz_id: str
    pathway_id: str
    score: float
    total_points: int
    percentage: float
    submitted_at: datetime
    answers: Dict[str, int]


class QuizImportRequest(BaseModel):
    """Quiz import request model for external content integration"""
    quiz_id: str
    pathway_id: str
    title: str
    description: str
    questions: List[QuizQuestion]
    total_points: Optional[int] = None  # Auto-calculated if not provided


class BulkQuizImportRequest(BaseModel):
    """Bulk quiz import request model"""
    quizzes: List[QuizImportRequest]


class Teacher(BaseModel):
    """Teacher model"""
    teacher_id: str
    name: str
    email: EmailStr
    password: str  # In production, this should be hashed


class TeacherResponse(BaseModel):
    """Teacher response model (without password)"""
    teacher_id: str
    name: str
    email: str


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str
    role: str = "student"  # "student" or "teacher"


class Admin(BaseModel):
    """Admin model"""
    admin_id: str
    name: str
    email: EmailStr
    password: str  # In production, this should be hashed


class AdminResponse(BaseModel):
    """Admin response model (without password)"""
    admin_id: str
    name: str
    email: str


class StudentProgress(BaseModel):
    """Student progress model for teacher dashboard"""
    student_id: str
    name: str
    email: str
    pathway: str
    quiz_scores: List[float]
    average_score: float
    total_quizzes_completed: int
    cumulative_score: float
    pathways: List[Dict[str, Any]] = []
    weaknesses: List[Dict[str, Any]] = []


class LoginResponse(BaseModel):
    """Login response model with JWT token"""
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]
    role: str


class PathwayStats(BaseModel):
    """Pathway statistics model"""
    pathway: str
    count: int
    percentage: float


class SystemStats(BaseModel):
    """System statistics model"""
    total_students: int
    total_teachers: int
    total_admins: int
    pathway_distribution: List[PathwayStats]
    average_scores: Dict[str, float]


class TaskAssignment(BaseModel):
    """Task assignment model"""
    task_id: str
    student_id: str
    teacher_id: str
    title: str
    description: str
    due_date: str  # ISO date string
    status: str = "pending"  # pending, in-progress, completed
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    quiz_id: Optional[str] = None  # Optional associated quiz


class TaskAssignmentRequest(BaseModel):
    """Task assignment request model"""
    student_ids: List[str]
    title: str
    description: str
    due_date: str
    quiz_id: Optional[str] = None  # Optional quiz to associate with task


# Adaptive Learning Models
class ConceptMastery(BaseModel):
    """Concept mastery model"""
    student_id: str
    concept: str  # e.g., "algebra", "geometry", "statistics"
    mastery_score: float  # 0-1 scale
    questions_answered: int
    correct_answers: int
    last_practiced: datetime
    trend: str = "stable"  # improving, stable, declining


class ConceptMasteryResponse(BaseModel):
    """Concept mastery response model"""
    student_id: str
    concepts: Dict[str, ConceptMastery]
    overall_mastery: float
    last_updated: datetime


class QuestionMetadata(BaseModel):
    """Question metadata for adaptive learning"""
    question_id: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: float = 0.5  # 0-1 scale, calibrated
    concepts: List[str] = []  # Concept tags
    prerequisites: List[str] = []
    performance_stats: Optional[Dict[str, Any]] = None


class Recommendation(BaseModel):
    """Content recommendation model"""
    student_id: str
    recommendation_id: str
    type: str  # "practice", "review", "advance", "prerequisite"
    priority: str  # "high", "medium", "low"
    concept: str
    content_id: Optional[str] = None
    content_type: Optional[str] = None  # "quiz", "practice", "reading"
    reason: str
    created_at: datetime


class RecommendationsResponse(BaseModel):
    """Recommendations response model"""
    student_id: str
    recommendations: List[Recommendation]
    last_updated: datetime


# Roadmap Generation Models
class RoadmapTask(BaseModel):
    """Individual task in a roadmap template"""
    task_id: str
    title: str
    description: str
    task_type: str  # "reading", "quiz", "practice", "project", "video", "assignment"
    order: int
    estimated_time: int  # Minutes
    difficulty: str  # "beginner", "intermediate", "advanced"
    learning_objectives: List[str] = []
    quiz_id: Optional[str] = None  # If task_type is "quiz"
    resource_url: Optional[str] = None  # Links to external resources
    prerequisites: List[str] = []  # Task IDs that must be completed first
    tags: List[str] = []  # Additional tags for filtering


class RoadmapTemplate(BaseModel):
    """Roadmap template model - knowledge base for generating roadmaps"""
    template_id: str
    name: str
    description: str
    created_by: str  # Teacher ID
    target_concepts: List[str]  # e.g., ["statistics", "probability", "data_analysis"]
    pathway_level: str  # "Basic", "Intermediate", "Excellent"
    difficulty: str  # "beginner", "intermediate", "advanced"
    weak_area_focus: bool = False  # True if template is for weak area remediation
    mastery_focus: bool = False  # True if template builds on strong areas
    tasks: List[RoadmapTask]
    prerequisites: Dict[str, float] = {}  # concept: mastery_threshold (0-1)
    estimated_total_time: int  # Total minutes
    learning_outcomes: List[str] = []  # What students will achieve
    tags: List[str] = []  # For categorization and search
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0  # How many times this template has been used


class RoadmapTemplateCreate(BaseModel):
    """Model for creating a new roadmap template"""
    name: str
    description: str
    target_concepts: List[str]
    pathway_level: str
    difficulty: str
    weak_area_focus: bool = False
    mastery_focus: bool = False
    tasks: List[Dict[str, Any]]  # Simplified task structure
    prerequisites: Dict[str, float] = {}
    estimated_total_time: int
    learning_outcomes: List[str] = []
    tags: List[str] = []


class RoadmapTemplateUpdate(BaseModel):
    """Model for updating a roadmap template"""
    name: Optional[str] = None
    description: Optional[str] = None
    target_concepts: Optional[List[str]] = None
    pathway_level: Optional[str] = None
    difficulty: Optional[str] = None
    weak_area_focus: Optional[bool] = None
    mastery_focus: Optional[bool] = None
    tasks: Optional[List[Dict[str, Any]]] = None
    prerequisites: Optional[Dict[str, float]] = None
    estimated_total_time: Optional[int] = None
    learning_outcomes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class GeneratedRoadmap(BaseModel):
    """Generated personalized roadmap for a student"""
    roadmap_id: str
    student_id: str
    generated_at: datetime
    status: str  # "pending", "active", "completed", "archived"
    template_ids: List[str]  # Templates used to generate this roadmap
    focus_areas: List[str]  # Weak areas being addressed
    tasks: List[RoadmapTask]
    total_tasks: int
    completed_tasks: int = 0
    estimated_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    generation_reason: str  # Why this roadmap was generated
    approved_by: Optional[str] = None  # Teacher ID if manual approval
    approved_at: Optional[datetime] = None
    notes: Optional[str] = None  # Teacher or system notes


class RoadmapGenerationRequest(BaseModel):
    """Request model for generating a roadmap"""
    student_id: str
    regenerate: bool = False  # If True, generate new roadmap even if one exists
    focus_areas: Optional[List[str]] = None  # Specific concepts to focus on
    template_ids: Optional[List[str]] = None  # Force use specific templates
    max_tasks: Optional[int] = None  # Maximum number of tasks
    approval_required: bool = False  # If True, requires teacher approval


class RoadmapGenerationResponse(BaseModel):
    """Response model for roadmap generation"""
    roadmap: GeneratedRoadmap
    generation_metadata: Dict[str, Any]  # Stats about the generation process
    matching_templates: List[str]  # Template IDs that were matched
    reasoning: str  # Explanation of why this roadmap was generated




class AdminResponse(BaseModel):
    """Admin response model (without password)"""
    admin_id: str
    name: str
    email: str


class StudentProgress(BaseModel):
    """Student progress model for teacher dashboard"""
    student_id: str
    name: str
    email: str
    pathway: str
    quiz_scores: List[float]
    average_score: float
    total_quizzes_completed: int
    cumulative_score: float
    pathways: List[Dict[str, Any]] = []
    weaknesses: List[Dict[str, Any]] = []


class LoginResponse(BaseModel):
    """Login response model with JWT token"""
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]
    role: str


class PathwayStats(BaseModel):
    """Pathway statistics model"""
    pathway: str
    count: int
    percentage: float


class SystemStats(BaseModel):
    """System statistics model"""
    total_students: int
    total_teachers: int
    total_admins: int
    pathway_distribution: List[PathwayStats]
    average_scores: Dict[str, float]


class TaskAssignment(BaseModel):
    """Task assignment model"""
    task_id: str
    student_id: str
    teacher_id: str
    title: str
    description: str
    due_date: str  # ISO date string
    status: str = "pending"  # pending, in-progress, completed
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    quiz_id: Optional[str] = None  # Optional associated quiz


class TaskAssignmentRequest(BaseModel):
    """Task assignment request model"""
    student_ids: List[str]
    title: str
    description: str
    due_date: str
    quiz_id: Optional[str] = None  # Optional quiz to associate with task


# Adaptive Learning Models
class ConceptMastery(BaseModel):
    """Concept mastery model"""
    student_id: str
    concept: str  # e.g., "algebra", "geometry", "statistics"
    mastery_score: float  # 0-1 scale
    questions_answered: int
    correct_answers: int
    last_practiced: datetime
    trend: str = "stable"  # improving, stable, declining


class ConceptMasteryResponse(BaseModel):
    """Concept mastery response model"""
    student_id: str
    concepts: Dict[str, ConceptMastery]
    overall_mastery: float
    last_updated: datetime


class QuestionMetadata(BaseModel):
    """Question metadata for adaptive learning"""
    question_id: str
    topic: str
    subtopic: Optional[str] = None
    difficulty: float = 0.5  # 0-1 scale, calibrated
    concepts: List[str] = []  # Concept tags
    prerequisites: List[str] = []
    performance_stats: Optional[Dict[str, Any]] = None


class Recommendation(BaseModel):
    """Content recommendation model"""
    student_id: str
    recommendation_id: str
    type: str  # "practice", "review", "advance", "prerequisite"
    priority: str  # "high", "medium", "low"
    concept: str
    content_id: Optional[str] = None
    content_type: Optional[str] = None  # "quiz", "practice", "reading"
    reason: str
    created_at: datetime


class RecommendationsResponse(BaseModel):
    """Recommendations response model"""
    student_id: str
    recommendations: List[Recommendation]
    last_updated: datetime


# Roadmap Generation Models
class RoadmapTask(BaseModel):
    """Individual task in a roadmap template"""
    task_id: str
    title: str
    description: str
    task_type: str  # "reading", "quiz", "practice", "project", "video", "assignment"
    order: int
    estimated_time: int  # Minutes
    difficulty: str  # "beginner", "intermediate", "advanced"
    learning_objectives: List[str] = []
    quiz_id: Optional[str] = None  # If task_type is "quiz"
    resource_url: Optional[str] = None  # Links to external resources
    prerequisites: List[str] = []  # Task IDs that must be completed first
    tags: List[str] = []  # Additional tags for filtering


class RoadmapTemplate(BaseModel):
    """Roadmap template model - knowledge base for generating roadmaps"""
    template_id: str
    name: str
    description: str
    created_by: str  # Teacher ID
    target_concepts: List[str]  # e.g., ["statistics", "probability", "data_analysis"]
    pathway_level: str  # "Basic", "Intermediate", "Excellent"
    difficulty: str  # "beginner", "intermediate", "advanced"
    weak_area_focus: bool = False  # True if template is for weak area remediation
    mastery_focus: bool = False  # True if template builds on strong areas
    tasks: List[RoadmapTask]
    prerequisites: Dict[str, float] = {}  # concept: mastery_threshold (0-1)
    estimated_total_time: int  # Total minutes
    learning_outcomes: List[str] = []  # What students will achieve
    tags: List[str] = []  # For categorization and search
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    usage_count: int = 0  # How many times this template has been used


class RoadmapTemplateCreate(BaseModel):
    """Model for creating a new roadmap template"""
    name: str
    description: str
    target_concepts: List[str]
    pathway_level: str
    difficulty: str
    weak_area_focus: bool = False
    mastery_focus: bool = False
    tasks: List[Dict[str, Any]]  # Simplified task structure
    prerequisites: Dict[str, float] = {}
    estimated_total_time: int
    learning_outcomes: List[str] = []
    tags: List[str] = []


class RoadmapTemplateUpdate(BaseModel):
    """Model for updating a roadmap template"""
    name: Optional[str] = None
    description: Optional[str] = None
    target_concepts: Optional[List[str]] = None
    pathway_level: Optional[str] = None
    difficulty: Optional[str] = None
    weak_area_focus: Optional[bool] = None
    mastery_focus: Optional[bool] = None
    tasks: Optional[List[Dict[str, Any]]] = None
    prerequisites: Optional[Dict[str, float]] = None
    estimated_total_time: Optional[int] = None
    learning_outcomes: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class GeneratedRoadmap(BaseModel):
    """Generated personalized roadmap for a student"""
    roadmap_id: str
    student_id: str
    generated_at: datetime
    status: str  # "pending", "active", "completed", "archived"
    template_ids: List[str]  # Templates used to generate this roadmap
    focus_areas: List[str]  # Weak areas being addressed
    tasks: List[RoadmapTask]
    total_tasks: int
    completed_tasks: int = 0
    estimated_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    generation_reason: str  # Why this roadmap was generated
    approved_by: Optional[str] = None  # Teacher ID if manual approval
    approved_at: Optional[datetime] = None
    notes: Optional[str] = None  # Teacher or system notes


class RoadmapGenerationRequest(BaseModel):
    """Request model for generating a roadmap"""
    student_id: str
    regenerate: bool = False  # If True, generate new roadmap even if one exists
    focus_areas: Optional[List[str]] = None  # Specific concepts to focus on
    template_ids: Optional[List[str]] = None  # Force use specific templates
    max_tasks: Optional[int] = None  # Maximum number of tasks
    approval_required: bool = False  # If True, requires teacher approval


class RoadmapGenerationResponse(BaseModel):
    """Response model for roadmap generation"""
    roadmap: GeneratedRoadmap
    generation_metadata: Dict[str, Any]  # Stats about the generation process
    matching_templates: List[str]  # Template IDs that were matched
    reasoning: str  # Explanation of why this roadmap was generated

