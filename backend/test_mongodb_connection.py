"""
Quick MongoDB Connection Test
Run this to verify your MongoDB connection is working
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# Get connection string from environment or use default
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb+srv://Research:ilpg1234@students.jb1nyzd.mongodb.net/ilpg_db?retryWrites=true&w=majority&appName=Students")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ilpg_db")

print("=" * 60)
print("MongoDB Connection Test")
print("=" * 60)
print(f"\nConnection String: {MONGODB_URI.split('@')[0]}@****")
print(f"Database: {DATABASE_NAME}")
print("\nTesting connection...\n")

try:
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=15000,
    )
    
    # Test connection
    client.admin.command('ping')
    print("[SUCCESS] ✓ Connected to MongoDB!")
    
    # Get database
    db = client[DATABASE_NAME]
    
    # List collections
    collections = db.list_collection_names()
    print(f"\n[INFO] Collections found: {len(collections)}")
    if collections:
        print(f"  - {', '.join(collections[:5])}")
        if len(collections) > 5:
            print(f"  ... and {len(collections) - 5} more")
    
    # Check if teachers collection exists and has data
    if "teachers" in collections:
        teacher_count = db["teachers"].count_documents({})
        print(f"\n[INFO] Teachers in database: {teacher_count}")
        if teacher_count > 0:
            sample_teacher = db["teachers"].find_one({}, {"email": 1, "name": 1})
            print(f"  Sample: {sample_teacher.get('name', 'N/A')} ({sample_teacher.get('email', 'N/A')})")
        else:
            print("  [WARNING] No teachers found! Run: python init_db.py")
    else:
        print("\n[WARNING] 'teachers' collection does not exist!")
        print("  Run: python init_db.py to create sample data")
    
    print("\n" + "=" * 60)
    print("Connection test PASSED!")
    print("=" * 60)
    sys.exit(0)
    
except ServerSelectionTimeoutError as e:
    print(f"\n[ERROR] ✗ Connection timeout!")
    print(f"  Details: {str(e)[:200]}")
    print("\nPossible causes:")
    print("  1. MongoDB Atlas cluster is paused or deleted")
    print("  2. Your IP address is not whitelisted")
    print("  3. Incorrect connection string")
    print("\nSee MONGODB_CONNECTION_FIX.md for detailed instructions.")
    sys.exit(1)
    
except ConnectionFailure as e:
    print(f"\n[ERROR] ✗ Connection failed!")
    print(f"  Details: {str(e)[:200]}")
    print("\nPossible causes:")
    print("  1. Network connectivity issues")
    print("  2. Firewall blocking connection")
    print("  3. MongoDB service not running (if local)")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] ✗ Unexpected error!")
    print(f"  Type: {type(e).__name__}")
    print(f"  Details: {str(e)[:200]}")
    sys.exit(1)

