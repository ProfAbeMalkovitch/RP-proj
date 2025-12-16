"""
Example Python script to import quizzes into ILPG system
This script demonstrates how to integrate quiz content from external sources
"""

import requests
import json
from typing import List, Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
QUIZ_API = f"{BASE_URL}/api/quizzes"
AUTH_API = f"{BASE_URL}/api/auth/teacher/login"

# Teacher credentials (replace with actual credentials)
TEACHER_EMAIL = "teacher@example.com"
TEACHER_PASSWORD = "password123"


def get_auth_token() -> str:
    """Get authentication token for teacher"""
    response = requests.post(
        AUTH_API,
        json={"email": TEACHER_EMAIL, "password": TEACHER_PASSWORD}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("token")
    else:
        raise Exception(f"Failed to authenticate: {response.text}")


def validate_quiz(quiz_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate quiz format before importing"""
    response = requests.post(
        f"{QUIZ_API}/validate",
        json=quiz_data
    )
    return response.json()


def import_single_quiz(quiz_data: Dict[str, Any], token: str) -> Dict[str, Any]:
    """Import a single quiz"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        f"{QUIZ_API}/import",
        json=quiz_data,
        headers=headers
    )
    return response.json()


def import_bulk_quizzes(quizzes: List[Dict[str, Any]], token: str) -> Dict[str, Any]:
    """Import multiple quizzes at once"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(
        f"{QUIZ_API}/import/bulk",
        json={"quizzes": quizzes},
        headers=headers
    )
    return response.json()


def load_quiz_from_file(file_path: str) -> Dict[str, Any]:
    """Load quiz data from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Main function demonstrating quiz import"""
    print("ILPG Quiz Import Example")
    print("=" * 50)
    
    # Step 1: Authenticate
    print("\n1. Authenticating...")
    try:
        token = get_auth_token()
        print(f"✓ Authentication successful")
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return
    
    # Step 2: Load quiz from file
    print("\n2. Loading quiz data...")
    try:
        quiz_data = load_quiz_from_file("sample_quiz.json")
        print(f"✓ Loaded quiz: {quiz_data['quiz_id']}")
    except FileNotFoundError:
        print("✗ sample_quiz.json not found. Using example data...")
        quiz_data = {
            "quiz_id": "quiz_example_1",
            "pathway_id": "pathway_basic",
            "title": "Example Quiz",
            "description": "Example quiz for testing",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Example question?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 1,
                    "points": 10
                }
            ]
        }
    except Exception as e:
        print(f"✗ Failed to load quiz: {e}")
        return
    
    # Step 3: Validate quiz
    print("\n3. Validating quiz format...")
    validation_result = validate_quiz(quiz_data)
    if validation_result.get("valid"):
        print("✓ Quiz format is valid")
        if validation_result.get("warnings"):
            print("  Warnings:")
            for warning in validation_result["warnings"]:
                print(f"    - {warning}")
    else:
        print("✗ Quiz format is invalid:")
        for error in validation_result.get("errors", []):
            print(f"    - {error}")
        return
    
    # Step 4: Import quiz
    print("\n4. Importing quiz...")
    try:
        result = import_single_quiz(quiz_data, token)
        if result.get("success"):
            print(f"✓ Quiz imported successfully!")
            print(f"  Quiz ID: {result['quiz_id']}")
            print(f"  Questions: {result['questions_count']}")
            print(f"  Total Points: {result['total_points']}")
        else:
            print(f"✗ Import failed: {result.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Import failed: {e}")
    
    # Example: Bulk import
    print("\n" + "=" * 50)
    print("Example: Bulk Import")
    print("=" * 50)
    
    quizzes = [
        {
            "quiz_id": "quiz_bulk_1",
            "pathway_id": "pathway_basic",
            "title": "Bulk Quiz 1",
            "description": "First quiz in bulk import",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Question 1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 0,
                    "points": 10
                }
            ]
        },
        {
            "quiz_id": "quiz_bulk_2",
            "pathway_id": "pathway_intermediate",
            "title": "Bulk Quiz 2",
            "description": "Second quiz in bulk import",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Question 1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": 1,
                    "points": 15
                }
            ]
        }
    ]
    
    print("\nImporting multiple quizzes...")
    try:
        bulk_result = import_bulk_quizzes(quizzes, token)
        print(f"✓ Imported: {bulk_result['imported_count']} quizzes")
        print(f"✗ Failed: {bulk_result['failed_count']} quizzes")
        
        if bulk_result.get("failed"):
            print("\nFailed quizzes:")
            for failed in bulk_result["failed"]:
                print(f"  - {failed['quiz_id']}: {failed['error']}")
    except Exception as e:
        print(f"✗ Bulk import failed: {e}")


if __name__ == "__main__":
    main()




