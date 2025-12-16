"""Seed admins"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import admins_collection
from utils.password import hash_password
from faker import Faker

fake = Faker()
Faker.seed(42)


def seed_admins():
    """Seed database with sample admins"""
    if admins_collection is None:
        print("❌ Database connection not available")
        return
    
    admins_collection.delete_many({})
    
    admins = [
        {
            "admin_id": "admin_001",
            "name": "Admin User",
            "email": "admin@ilpg.com",
            "password": hash_password("admin123")
        },
        {
            "admin_id": "admin_002",
            "name": fake.name(),
            "email": fake.unique.email(),
            "password": hash_password("admin123")
        }
    ]
    
    admins_collection.insert_many(admins)
    print(f"✅ Seeded {len(admins)} admins")


if __name__ == "__main__":
    seed_admins()

