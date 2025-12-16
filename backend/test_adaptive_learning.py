"""
Test script to verify Adaptive Learning Engine is working
Run this script to check if all components are functioning
"""

import sys
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = None  # Will be set after login or use existing student

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_test(test_name):
    print(f"\n▶ Testing: {test_name}")

def print_success(message):
    print(f"  ✅ {message}")

def print_error(message):
    print(f"  ❌ {message}")

def print_info(message):
    print(f"  ℹ️  {message}")

def test_api_health():
    """Test 1: Check if API is running"""
    print_test("API Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print_success("API is running")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to API: {str(e)}")
        print_info("Make sure backend server is running on port 8000")
        return False

def test_adaptive_endpoints(student_id, token):
    """Test 2: Check adaptive learning endpoints"""
    print_test("Adaptive Learning Endpoints")
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        f"/api/adaptive/mastery/{student_id}",
        f"/api/adaptive/recommendations/{student_id}",
        f"/api/adaptive/analytics/{student_id}",
        f"/api/adaptive/weak-areas/{student_id}"
    ]
    
    all_passed = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code in [200, 404]:  # 404 is OK if no data yet
                print_success(f"Endpoint accessible: {endpoint}")
                if response.status_code == 404:
                    print_info("  No data yet (this is normal for new students)")
                else:
                    data = response.json()
                    print_info(f"  Response keys: {list(data.keys())}")
            else:
                print_error(f"Endpoint failed: {endpoint} (Status: {response.status_code})")
                all_passed = False
        except Exception as e:
            print_error(f"Error accessing {endpoint}: {str(e)}")
            all_passed = False
    
    return all_passed

def test_database_collections():
    """Test 3: Check if database collections exist"""
    print_test("Database Collections Check")
    
    try:
        from database import (
            concept_mastery_collection,
            recommendations_collection,
            results_collection,
            quizzes_collection
        )
        
        collections = {
            "concept_mastery": concept_mastery_collection,
            "recommendations": recommendations_collection,
            "results": results_collection,
            "quizzes": quizzes_collection
        }
        
        all_exist = True
        for name, collection in collections.items():
            if collection is not None:
                count = collection.count_documents({})
                print_success(f"Collection '{name}' exists ({count} documents)")
            else:
                print_error(f"Collection '{name}' is None (database not connected)")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print_error(f"Error checking collections: {str(e)}")
        return False

def test_service_import():
    """Test 4: Check if adaptive learning service can be imported"""
    print_test("Adaptive Learning Service Import")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from services.adaptive_learning_service import AdaptiveLearningService
        
        print_success("AdaptiveLearningService imported successfully")
        print_info("Service class methods:")
        methods = [m for m in dir(AdaptiveLearningService) if not m.startswith('_')]
        for method in methods[:5]:  # Show first 5 methods
            print_info(f"  - {method}")
        
        return True
    except Exception as e:
        print_error(f"Failed to import service: {str(e)}")
        return False

def test_quiz_submission_integration(student_id, token):
    """Test 5: Check if quiz submission triggers adaptive learning"""
    print_test("Quiz Submission Integration Check")
    
    try:
        # Check if results endpoint includes adaptive learning fields
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/results/student/{student_id}", headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            print_success("Quiz results endpoint accessible")
            
            if isinstance(results, list) and len(results) > 0:
                latest_result = results[0]
                adaptive_fields = ['pathway_adjusted', 'new_pathway', 'recommendations_count']
                has_adaptive = any(field in latest_result for field in adaptive_fields)
                
                if has_adaptive:
                    print_success("Quiz results include adaptive learning fields")
                    print_info(f"  Latest result keys: {list(latest_result.keys())}")
                else:
                    print_info("  No adaptive fields yet (may need to submit a new quiz)")
            
            return True
        else:
            print_error(f"Results endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error checking quiz submission: {str(e)}")
        return False

def main():
    """Run all tests"""
    print_header("Adaptive Learning Engine - Verification Tests")
    print_info("This script will verify that the adaptive learning engine is properly set up.")
    print_info("Make sure backend server is running before starting tests.\n")
    
    results = []
    
    # Test 1: API Health
    results.append(("API Health", test_api_health()))
    
    # Test 2: Service Import
    results.append(("Service Import", test_service_import()))
    
    # Test 3: Database Collections
    results.append(("Database Collections", test_database_collections()))
    
    # Test 4: Endpoints (optional - requires authentication)
    print_header("Optional: Endpoint Tests (Requires Authentication)")
    print_info("To test endpoints, you need to:")
    print_info("1. Login as a student")
    print_info("2. Get the JWT token from localStorage")
    print_info("3. Update STUDENT_ID and token in this script")
    print_info("Or test manually via browser DevTools\n")
    
    # Summary
    print_header("Test Results Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All core tests passed! Adaptive Learning Engine is ready.")
        print_info("\nNext steps:")
        print_info("1. Login as a student")
        print_info("2. Take a quiz")
        print_info("3. Check dashboard for mastery scores and recommendations")
    else:
        print_error("Some tests failed. Please check the errors above.")
        print_info("Common issues:")
        print_info("- Backend server not running")
        print_info("- MongoDB not connected")
        print_info("- Missing dependencies")
    
    print("\n")

if __name__ == "__main__":
    main()


















Test script to verify Adaptive Learning Engine is working
Run this script to check if all components are functioning
"""

import sys
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = None  # Will be set after login or use existing student

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_test(test_name):
    print(f"\n▶ Testing: {test_name}")

def print_success(message):
    print(f"  ✅ {message}")

def print_error(message):
    print(f"  ❌ {message}")

def print_info(message):
    print(f"  ℹ️  {message}")

def test_api_health():
    """Test 1: Check if API is running"""
    print_test("API Health Check")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print_success("API is running")
            print_info(f"Response: {response.json()}")
            return True
        else:
            print_error(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to API: {str(e)}")
        print_info("Make sure backend server is running on port 8000")
        return False

def test_adaptive_endpoints(student_id, token):
    """Test 2: Check adaptive learning endpoints"""
    print_test("Adaptive Learning Endpoints")
    
    headers = {"Authorization": f"Bearer {token}"}
    endpoints = [
        f"/api/adaptive/mastery/{student_id}",
        f"/api/adaptive/recommendations/{student_id}",
        f"/api/adaptive/analytics/{student_id}",
        f"/api/adaptive/weak-areas/{student_id}"
    ]
    
    all_passed = True
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code in [200, 404]:  # 404 is OK if no data yet
                print_success(f"Endpoint accessible: {endpoint}")
                if response.status_code == 404:
                    print_info("  No data yet (this is normal for new students)")
                else:
                    data = response.json()
                    print_info(f"  Response keys: {list(data.keys())}")
            else:
                print_error(f"Endpoint failed: {endpoint} (Status: {response.status_code})")
                all_passed = False
        except Exception as e:
            print_error(f"Error accessing {endpoint}: {str(e)}")
            all_passed = False
    
    return all_passed

def test_database_collections():
    """Test 3: Check if database collections exist"""
    print_test("Database Collections Check")
    
    try:
        from database import (
            concept_mastery_collection,
            recommendations_collection,
            results_collection,
            quizzes_collection
        )
        
        collections = {
            "concept_mastery": concept_mastery_collection,
            "recommendations": recommendations_collection,
            "results": results_collection,
            "quizzes": quizzes_collection
        }
        
        all_exist = True
        for name, collection in collections.items():
            if collection is not None:
                count = collection.count_documents({})
                print_success(f"Collection '{name}' exists ({count} documents)")
            else:
                print_error(f"Collection '{name}' is None (database not connected)")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print_error(f"Error checking collections: {str(e)}")
        return False

def test_service_import():
    """Test 4: Check if adaptive learning service can be imported"""
    print_test("Adaptive Learning Service Import")
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from services.adaptive_learning_service import AdaptiveLearningService
        
        print_success("AdaptiveLearningService imported successfully")
        print_info("Service class methods:")
        methods = [m for m in dir(AdaptiveLearningService) if not m.startswith('_')]
        for method in methods[:5]:  # Show first 5 methods
            print_info(f"  - {method}")
        
        return True
    except Exception as e:
        print_error(f"Failed to import service: {str(e)}")
        return False

def test_quiz_submission_integration(student_id, token):
    """Test 5: Check if quiz submission triggers adaptive learning"""
    print_test("Quiz Submission Integration Check")
    
    try:
        # Check if results endpoint includes adaptive learning fields
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/results/student/{student_id}", headers=headers)
        
        if response.status_code == 200:
            results = response.json()
            print_success("Quiz results endpoint accessible")
            
            if isinstance(results, list) and len(results) > 0:
                latest_result = results[0]
                adaptive_fields = ['pathway_adjusted', 'new_pathway', 'recommendations_count']
                has_adaptive = any(field in latest_result for field in adaptive_fields)
                
                if has_adaptive:
                    print_success("Quiz results include adaptive learning fields")
                    print_info(f"  Latest result keys: {list(latest_result.keys())}")
                else:
                    print_info("  No adaptive fields yet (may need to submit a new quiz)")
            
            return True
        else:
            print_error(f"Results endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error checking quiz submission: {str(e)}")
        return False

def main():
    """Run all tests"""
    print_header("Adaptive Learning Engine - Verification Tests")
    print_info("This script will verify that the adaptive learning engine is properly set up.")
    print_info("Make sure backend server is running before starting tests.\n")
    
    results = []
    
    # Test 1: API Health
    results.append(("API Health", test_api_health()))
    
    # Test 2: Service Import
    results.append(("Service Import", test_service_import()))
    
    # Test 3: Database Collections
    results.append(("Database Collections", test_database_collections()))
    
    # Test 4: Endpoints (optional - requires authentication)
    print_header("Optional: Endpoint Tests (Requires Authentication)")
    print_info("To test endpoints, you need to:")
    print_info("1. Login as a student")
    print_info("2. Get the JWT token from localStorage")
    print_info("3. Update STUDENT_ID and token in this script")
    print_info("Or test manually via browser DevTools\n")
    
    # Summary
    print_header("Test Results Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All core tests passed! Adaptive Learning Engine is ready.")
        print_info("\nNext steps:")
        print_info("1. Login as a student")
        print_info("2. Take a quiz")
        print_info("3. Check dashboard for mastery scores and recommendations")
    else:
        print_error("Some tests failed. Please check the errors above.")
        print_info("Common issues:")
        print_info("- Backend server not running")
        print_info("- MongoDB not connected")
        print_info("- Missing dependencies")
    
    print("\n")

if __name__ == "__main__":
    main()


















































