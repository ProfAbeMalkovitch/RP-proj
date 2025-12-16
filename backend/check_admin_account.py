"""Quick script to check admin accounts"""
from database import admins_collection

print("[INFO] Checking admin accounts...")
admins = list(admins_collection.find({}, {'email': 1, 'name': 1, 'admin_id': 1}))

if admins:
    print(f"\n[SUCCESS] Found {len(admins)} admin account(s):\n")
    for i, admin in enumerate(admins, 1):
        print(f"{i}. Email: {admin['email']}")
        print(f"   Name: {admin.get('name', 'N/A')}")
        print(f"   ID: {admin.get('admin_id', 'N/A')}\n")
    print("Default password: admin123")
else:
    print("\n[WARNING] No admin accounts found!")
    print("Run: python seeders/seed_admins.py")







from database import admins_collection

print("[INFO] Checking admin accounts...")
admins = list(admins_collection.find({}, {'email': 1, 'name': 1, 'admin_id': 1}))

if admins:
    print(f"\n[SUCCESS] Found {len(admins)} admin account(s):\n")
    for i, admin in enumerate(admins, 1):
        print(f"{i}. Email: {admin['email']}")
        print(f"   Name: {admin.get('name', 'N/A')}")
        print(f"   ID: {admin.get('admin_id', 'N/A')}\n")
    print("Default password: admin123")
else:
    print("\n[WARNING] No admin accounts found!")
    print("Run: python seeders/seed_admins.py")




























