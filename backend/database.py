"""
Database connection module
Handles MongoDB connection and provides database instance
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection settings
# For MongoDB Atlas, use format: mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
# For local MongoDB, use: mongodb://localhost:27017/
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority&appName=Students")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ilpg_db")

# Create MongoDB client with additional connection options
try:
    # Simple connection - mongodb+srv:// handles SSL/TLS automatically
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000,  # 10 second timeout
        connectTimeoutMS=15000,  # 15 second connection timeout
        socketTimeoutMS=30000,  # 30 second socket timeout
        retryWrites=True,
    )
    
    # Test connection
    client.admin.command('ping')
    print("[SUCCESS] Successfully connected to MongoDB Atlas")
except Exception as e:
    error_msg = str(e)[:200]
    print(f"[ERROR] Failed to connect to MongoDB: {error_msg}")
    print("\n[IMPORTANT] MongoDB connection failed!")
    print("\nPossible issues:")
    print("1. MongoDB Atlas cluster may be paused or deleted")
    print("2. Your IP address is not whitelisted")
    print("3. Connection string is incorrect")
    print("\nQuick Fix Steps:")
    print("1. Go to: https://cloud.mongodb.com/")
    print("2. Navigate to: Network Access (left sidebar)")
    print("3. Click: 'Add IP Address' -> 'Allow Access from Anywhere' (for dev)")
    print("4. Check: Clusters -> Ensure cluster is running (not paused)")
    print("5. Verify: Database Access -> User 'Research' exists")
    print("6. Wait 1-2 minutes for changes to propagate")
    print("7. Restart this server")
    print("\nThe server will continue running, but database operations will fail until connected.")
    # Create client anyway for graceful degradation
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    except:
        client = None

# Get database instance (with safety check)
if client is not None:
    db = client[DATABASE_NAME]
    
    # Get collections
    students_collection = db["students"]
    teachers_collection = db["teachers"]
    admins_collection = db["admins"]
    pathways_collection = db["pathways"]
    quizzes_collection = db["quizzes"]
    results_collection = db["results"]
    tasks_collection = db["tasks"]
    # Adaptive Learning collections
    concept_mastery_collection = db["concept_mastery"]
    question_metadata_collection = db["question_metadata"]
    recommendations_collection = db["recommendations"]
    learning_sessions_collection = db["learning_sessions"]
    # Roadmap Generation collections
    roadmap_templates_collection = db["roadmap_templates"]
    generated_roadmaps_collection = db["generated_roadmaps"]
else:
    # Fallback: create dummy collections to prevent errors
    # These will fail on actual operations, but won't crash on import
    db = None
    students_collection = None
    teachers_collection = None
    admins_collection = None
    pathways_collection = None
    quizzes_collection = None
    results_collection = None
    tasks_collection = None
    concept_mastery_collection = None
    question_metadata_collection = None
    recommendations_collection = None
    learning_sessions_collection = None
    roadmap_templates_collection = None
    generated_roadmaps_collection = None
    print("[WARNING] Database collections not available. Please fix MongoDB connection.")

