"""Verify seeded data"""
from database import students_collection, teachers_collection, admins_collection

print("📊 Database Summary:")
print(f"  Students: {students_collection.count_documents({})}")
print(f"  Teachers: {teachers_collection.count_documents({})}")
print(f"  Admins: {admins_collection.count_documents({})}")

print("\n📚 Pathway Distribution:")
for pathway in ['Basic', 'Intermediate', 'Accelerated']:
    count = students_collection.count_documents({'pathway': pathway})
    print(f"  {pathway}: {count} students")

print("\n👥 Sample Users:")
print("\nTeachers:")
for teacher in teachers_collection.find({}, {'_id': 0, 'password': 0}).limit(3):
    print(f"  - {teacher['name']} ({teacher['email']})")

print("\nAdmins:")
for admin in admins_collection.find({}, {'_id': 0, 'password': 0}).limit(2):
    print(f"  - {admin['name']} ({admin['email']})")





































