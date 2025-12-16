"""
Student Seeder Script
Generates 150 dummy students (50 per pathway) using Faker
Pathway classification:
- Basic: 0-49 average score
- Intermediate: 50-74 average score
- Accelerated: 75-100 average score
"""

from faker import Faker
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import students_collection
from utils.pathway_calculator import calculate_pathway
from utils.password import hash_password

fake = Faker()
Faker.seed(42)  # For reproducible results
random.seed(42)


def generate_quiz_scores_for_pathway(pathway: str, num_quizzes: int = None) -> list:
    """
    Generate quiz scores that align with the target pathway
    
    Args:
        pathway: Target pathway ("Basic", "Intermediate", or "Accelerated")
        num_quizzes: Number of quiz scores to generate (default: 5-15)
    
    Returns:
        List of quiz scores (percentages)
    """
    if num_quizzes is None:
        num_quizzes = random.randint(5, 15)
    
    scores = []
    
    if pathway == "Basic":
        # Generate scores between 0-49, with average around 30-40
        for _ in range(num_quizzes):
            # Weighted towards lower scores
            score = random.choices(
                range(0, 50),
                weights=[10] * 20 + [8] * 15 + [5] * 10 + [2] * 5
            )[0]
            scores.append(float(score))
    
    elif pathway == "Intermediate":
        # Generate scores between 50-74, with average around 60-65
        for _ in range(num_quizzes):
            score = random.choices(
                range(50, 75),
                weights=[2] * 5 + [5] * 10 + [8] * 10
            )[0]
            scores.append(float(score))
    
    else:  # Accelerated
        # Generate scores between 75-100, with average around 85-90
        for _ in range(num_quizzes):
            score = random.choices(
                range(75, 101),
                weights=[2] * 5 + [5] * 10 + [10] * 10 + [8] * 1
            )[0]
            scores.append(float(score))
    
    return scores


def seed_students():
    """
    Seed database with 150 students (50 per pathway)
    """
    if students_collection is None:
        print("❌ Database connection not available")
        return
    
    # Clear existing students
    students_collection.delete_many({})
    print("✓ Cleared existing students")
    
    students = []
    pathways = ["Basic", "Intermediate", "Accelerated"]
    
    for pathway in pathways:
        print(f"\n📚 Generating 50 students for {pathway} pathway...")
        
        for i in range(50):
            # Generate quiz scores that align with pathway
            quiz_scores = generate_quiz_scores_for_pathway(pathway)
            
            # Calculate average and verify pathway
            average_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
            calculated_pathway = calculate_pathway(quiz_scores)
            
            # Ensure pathway matches (with some tolerance for randomness)
            if calculated_pathway != pathway:
                # Adjust scores to match pathway
                if pathway == "Basic" and average_score >= 50:
                    quiz_scores = [random.uniform(0, 49) for _ in quiz_scores]
                elif pathway == "Intermediate" and (average_score < 50 or average_score >= 75):
                    quiz_scores = [random.uniform(50, 74) for _ in quiz_scores]
                elif pathway == "Accelerated" and average_score < 75:
                    quiz_scores = [random.uniform(75, 100) for _ in quiz_scores]
                
                average_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
                calculated_pathway = calculate_pathway(quiz_scores)
            
            student = {
                "student_id": f"student_{pathway.lower()}_{i+1:03d}",
                "name": fake.name(),
                "email": fake.unique.email(),
                "password": hash_password("password123"),  # Default password for all students
                "quiz_scores": quiz_scores,
                "pathway": calculated_pathway,
                "average_score": round(average_score, 2),
                "cumulative_score": round(sum(quiz_scores), 2)
            }
            
            students.append(student)
    
    # Insert all students
    students_collection.insert_many(students)
    
    # Verify insertion
    total_count = students_collection.count_documents({})
    basic_count = students_collection.count_documents({"pathway": "Basic"})
    intermediate_count = students_collection.count_documents({"pathway": "Intermediate"})
    accelerated_count = students_collection.count_documents({"pathway": "Accelerated"})
    
    print(f"\n✅ Successfully seeded {total_count} students:")
    print(f"   - Basic: {basic_count} students")
    print(f"   - Intermediate: {intermediate_count} students")
    print(f"   - Accelerated: {accelerated_count} students")
    
    # Show sample students
    print("\n📋 Sample students:")
    for pathway in pathways:
        sample = students_collection.find_one({"pathway": pathway}, {"_id": 0, "password": 0})
        if sample:
            print(f"   {pathway}: {sample['name']} ({sample['email']}) - "
                  f"Avg: {sample['average_score']:.1f}%, Quizzes: {len(sample['quiz_scores'])}")


if __name__ == "__main__":
    print("🌱 Starting student seeder...")
    seed_students()
    print("\n✨ Seeding complete!")

