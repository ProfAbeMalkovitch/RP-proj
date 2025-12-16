"""
ILPG Backend - FastAPI Application
Main entry point for the Intelligent Learning Path Generator backend API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes import students, teachers, pathways, quizzes, results, auth, analytics, tasks, adaptive_learning, roadmap

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="ILPG API",
    description="Intelligent Learning Path Generator API",
    version="1.0.0"
)

# Configure CORS to allow frontend communication
# Allow all localhost ports for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(teachers.router, prefix="/api/teachers", tags=["teachers"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(pathways.router, prefix="/api/pathways", tags=["pathways"])
app.include_router(quizzes.router, prefix="/api/quizzes", tags=["quizzes"])
app.include_router(results.router, prefix="/api/results", tags=["results"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(adaptive_learning.router, prefix="/api/adaptive", tags=["adaptive-learning"])
app.include_router(roadmap.router, prefix="/api/roadmap", tags=["roadmap"])


@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {"message": "ILPG API is running"}


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



