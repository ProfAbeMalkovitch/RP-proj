"""Seed teachers"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import teachers_collection
from utils.password import hash_password
from faker import Faker

fake = Faker()
Faker.seed(42)


def seed_teachers():
    """Seed database with sample teachers"""
    if teachers_collection is None:
        print("❌ Database connection not available")
        return
    
    teachers_collection.delete_many({})
    
    teachers = [
        {
            "teacher_id": "teacher_001",
            "name": "Dr. Sarah Johnson",
            "email": "sarah@teacher.com",
            "password": hash_password("teacher123")
        },
        {
            "teacher_id": "teacher_002",
            "name": "Prof. Michael Chen",
            "email": "michael@teacher.com",
            "password": hash_password("teacher123")
        },
        {
            "teacher_id": "teacher_003",
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": hash_password("teacher123")
        }
    ]
    
    teachers_collection.insert_many(teachers)
    print(f"✅ Seeded {len(teachers)} teachers")


if __name__ == "__main__":
    seed_teachers()

