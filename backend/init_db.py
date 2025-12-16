"""
Database initialization script
Creates sample data for students, pathways, and quizzes
Run this script once to populate the database with initial data
"""

from database import students_collection, teachers_collection, pathways_collection, quizzes_collection, results_collection
from datetime import datetime

def init_database():
    """Initialize database with sample data"""
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    students_collection.delete_many({})
    teachers_collection.delete_many({})
    pathways_collection.delete_many({})
    quizzes_collection.delete_many({})
    results_collection.delete_many({})
    
    # Sample Students
    students = [
        {
            "student_id": "student_001",
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "cumulative_score": 0.0
        },
        {
            "student_id": "student_002",
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "password123",
            "cumulative_score": 0.0
        },
        {
            "student_id": "student_003",
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "password": "password123",
            "cumulative_score": 0.0
        }
    ]
    students_collection.insert_many(students)
    print("✓ Inserted sample students")
    
    # Sample Teachers
    teachers = [
        {
            "teacher_id": "teacher_001",
            "name": "Dr. Sarah Johnson",
            "email": "sarah@teacher.com",
            "password": "teacher123"
        },
        {
            "teacher_id": "teacher_002",
            "name": "Prof. Michael Chen",
            "email": "michael@teacher.com",
            "password": "teacher123"
        }
    ]
    teachers_collection.insert_many(teachers)
    print("✓ Inserted sample teachers")
    
    # Sample Pathways
    pathways = [
        {
            "pathway_id": "pathway_basic",
            "name": "Basic Learning Path",
            "level": "Basic",
            "description": "A foundational pathway for beginners to start their learning journey",
            "content": """
            Welcome to the Basic Learning Path! This pathway is designed for beginners who are just starting their journey.
            
            In this pathway, you will learn:
            - Fundamental concepts and terminology
            - Basic principles and best practices
            - Introduction to core tools and techniques
            - Building a strong foundation for advanced learning
            
            This pathway consists of 5 modules, each building upon the previous one. Complete all modules and quizzes to progress to the Intermediate level.
            """,
            "topics": [
                {"id": "topic_1", "name": "Introduction", "level": 0, "connections": ["topic_2"]},
                {"id": "topic_2", "name": "Fundamentals", "level": 1, "connections": ["topic_3", "topic_4"]},
                {"id": "topic_3", "name": "Core Concepts", "level": 2, "connections": ["topic_5"]},
                {"id": "topic_4", "name": "Basic Tools", "level": 2, "connections": ["topic_5"]},
                {"id": "topic_5", "name": "Practice & Review", "level": 3, "connections": []}
            ],
            "roadmap": [
                {"task_id": "task_1", "title": "Complete Introduction Module", "status": "pending", "order": 1},
                {"task_id": "task_2", "title": "Study Fundamentals", "status": "pending", "order": 2},
                {"task_id": "task_3", "title": "Learn Core Concepts", "status": "pending", "order": 3},
                {"task_id": "task_4", "title": "Practice with Basic Tools", "status": "pending", "order": 4},
                {"task_id": "task_5", "title": "Take Assessment Quiz", "status": "pending", "order": 5}
            ],
            "quiz_ids": ["quiz_basic_1", "quiz_basic_2"]
        },
        {
            "pathway_id": "pathway_intermediate",
            "name": "Intermediate Learning Path",
            "level": "Intermediate",
            "description": "An intermediate pathway for learners ready to advance their skills",
            "content": """
            Welcome to the Intermediate Learning Path! This pathway is designed for learners who have mastered the basics.
            
            In this pathway, you will learn:
            - Advanced concepts and techniques
            - Complex problem-solving strategies
            - Integration of multiple tools and methods
            - Real-world application scenarios
            
            This pathway consists of 7 modules with hands-on projects. Complete all modules and quizzes to progress to the Excellent level.
            """,
            "topics": [
                {"id": "topic_1", "name": "Advanced Fundamentals", "level": 0, "connections": ["topic_2", "topic_3"]},
                {"id": "topic_2", "name": "Complex Concepts", "level": 1, "connections": ["topic_4"]},
                {"id": "topic_3", "name": "Advanced Tools", "level": 1, "connections": ["topic_4"]},
                {"id": "topic_4", "name": "Integration", "level": 2, "connections": ["topic_5"]},
                {"id": "topic_5", "name": "Real-world Projects", "level": 3, "connections": []}
            ],
            "roadmap": [
                {"task_id": "task_1", "title": "Review Advanced Fundamentals", "status": "pending", "order": 1},
                {"task_id": "task_2", "title": "Master Complex Concepts", "status": "pending", "order": 2},
                {"task_id": "task_3", "title": "Learn Advanced Tools", "status": "pending", "order": 3},
                {"task_id": "task_4", "title": "Practice Integration", "status": "pending", "order": 4},
                {"task_id": "task_5", "title": "Complete Real-world Project", "status": "pending", "order": 5},
                {"task_id": "task_6", "title": "Take Assessment Quiz", "status": "pending", "order": 6}
            ],
            "quiz_ids": ["quiz_intermediate_1", "quiz_intermediate_2"]
        },
        {
            "pathway_id": "pathway_excellent",
            "name": "Excellent Learning Path",
            "level": "Excellent",
            "description": "An advanced pathway for expert-level learners",
            "content": """
            Welcome to the Excellent Learning Path! This pathway is designed for advanced learners ready to master expert-level skills.
            
            In this pathway, you will learn:
            - Expert-level concepts and methodologies
            - Advanced problem-solving and optimization
            - Leadership and mentoring skills
            - Innovation and research techniques
            
            This pathway consists of 10 modules with capstone projects. Complete all modules and quizzes to achieve mastery.
            """,
            "topics": [
                {"id": "topic_1", "name": "Expert Fundamentals", "level": 0, "connections": ["topic_2", "topic_3", "topic_4"]},
                {"id": "topic_2", "name": "Advanced Methodologies", "level": 1, "connections": ["topic_5"]},
                {"id": "topic_3", "name": "Optimization Techniques", "level": 1, "connections": ["topic_5"]},
                {"id": "topic_4", "name": "Leadership Skills", "level": 1, "connections": ["topic_6"]},
                {"id": "topic_5", "name": "Innovation", "level": 2, "connections": ["topic_6"]},
                {"id": "topic_6", "name": "Mastery & Research", "level": 3, "connections": []}
            ],
            "roadmap": [
                {"task_id": "task_1", "title": "Master Expert Fundamentals", "status": "pending", "order": 1},
                {"task_id": "task_2", "title": "Learn Advanced Methodologies", "status": "pending", "order": 2},
                {"task_id": "task_3", "title": "Study Optimization Techniques", "status": "pending", "order": 3},
                {"task_id": "task_4", "title": "Develop Leadership Skills", "status": "pending", "order": 4},
                {"task_id": "task_5", "title": "Work on Innovation Project", "status": "pending", "order": 5},
                {"task_id": "task_6", "title": "Complete Capstone Project", "status": "pending", "order": 6},
                {"task_id": "task_7", "title": "Take Final Assessment", "status": "pending", "order": 7}
            ],
            "quiz_ids": ["quiz_excellent_1", "quiz_excellent_2"]
        }
    ]
    pathways_collection.insert_many(pathways)
    print("✓ Inserted sample pathways")
    
    # Sample Quizzes
    quizzes = [
        {
            "quiz_id": "quiz_basic_1",
            "pathway_id": "pathway_basic",
            "title": "Basic Pathway - Quiz 1",
            "description": "Assessment quiz for basic concepts",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "What is the first step in learning any new skill?",
                    "options": ["Jump to advanced topics", "Learn fundamentals", "Skip basics", "Copy others"],
                    "correct_answer": 1,
                    "points": 10
                },
                {
                    "question_id": "q2",
                    "question_text": "Which approach is best for beginners?",
                    "options": ["Complex projects", "Simple examples", "Advanced techniques", "Expert level content"],
                    "correct_answer": 1,
                    "points": 10
                },
                {
                    "question_id": "q3",
                    "question_text": "Practice is important for:",
                    "options": ["Only experts", "Everyone", "Only beginners", "Nobody"],
                    "correct_answer": 1,
                    "points": 10
                }
            ],
            "total_points": 30
        },
        {
            "quiz_id": "quiz_basic_2",
            "pathway_id": "pathway_basic",
            "title": "Basic Pathway - Quiz 2",
            "description": "Second assessment quiz for basic concepts",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "What helps in building a strong foundation?",
                    "options": ["Skipping steps", "Consistent practice", "Rushing through", "Avoiding basics"],
                    "correct_answer": 1,
                    "points": 15
                },
                {
                    "question_id": "q2",
                    "question_text": "The best learning approach includes:",
                    "options": ["Only theory", "Only practice", "Theory and practice", "No learning"],
                    "correct_answer": 2,
                    "points": 15
                }
            ],
            "total_points": 30
        },
        {
            "quiz_id": "quiz_intermediate_1",
            "pathway_id": "pathway_intermediate",
            "title": "Intermediate Pathway - Quiz 1",
            "description": "Assessment quiz for intermediate concepts",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Intermediate learning focuses on:",
                    "options": ["Basics only", "Advanced only", "Building on fundamentals", "Starting over"],
                    "correct_answer": 2,
                    "points": 15
                },
                {
                    "question_id": "q2",
                    "question_text": "Complex problem-solving requires:",
                    "options": ["Simple solutions", "Multiple approaches", "One method", "No thinking"],
                    "correct_answer": 1,
                    "points": 15
                },
                {
                    "question_id": "q3",
                    "question_text": "Integration means:",
                    "options": ["Using one tool", "Combining multiple tools", "Avoiding tools", "Ignoring tools"],
                    "correct_answer": 1,
                    "points": 20
                }
            ],
            "total_points": 50
        },
        {
            "quiz_id": "quiz_intermediate_2",
            "pathway_id": "pathway_intermediate",
            "title": "Intermediate Pathway - Quiz 2",
            "description": "Second assessment quiz for intermediate concepts",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Real-world application helps:",
                    "options": ["Only in theory", "Understanding practical use", "Avoiding practice", "Staying theoretical"],
                    "correct_answer": 1,
                    "points": 20
                },
                {
                    "question_id": "q2",
                    "question_text": "Advanced tools should be:",
                    "options": ["Used immediately", "Learned gradually", "Avoided", "Ignored"],
                    "correct_answer": 1,
                    "points": 20
                }
            ],
            "total_points": 40
        },
        {
            "quiz_id": "quiz_excellent_1",
            "pathway_id": "pathway_excellent",
            "title": "Excellent Pathway - Quiz 1",
            "description": "Assessment quiz for excellent level concepts",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Expert-level learning involves:",
                    "options": ["Basic concepts", "Mastery and innovation", "Simple tasks", "Avoiding challenges"],
                    "correct_answer": 1,
                    "points": 20
                },
                {
                    "question_id": "q2",
                    "question_text": "Leadership in learning means:",
                    "options": ["Learning alone", "Guiding others", "Avoiding teaching", "Keeping knowledge secret"],
                    "correct_answer": 1,
                    "points": 20
                },
                {
                    "question_id": "q3",
                    "question_text": "Innovation requires:",
                    "options": ["Following only", "Creative thinking", "No thinking", "Avoiding new ideas"],
                    "correct_answer": 1,
                    "points": 25
                }
            ],
            "total_points": 65
        },
        {
            "quiz_id": "quiz_excellent_2",
            "pathway_id": "pathway_excellent",
            "title": "Excellent Pathway - Quiz 2",
            "description": "Final assessment quiz for excellent level",
            "questions": [
                {
                    "question_id": "q1",
                    "question_text": "Mastery is achieved through:",
                    "options": ["Quick learning", "Continuous practice and improvement", "One-time study", "Avoiding practice"],
                    "correct_answer": 1,
                    "points": 25
                },
                {
                    "question_id": "q2",
                    "question_text": "Research skills help in:",
                    "options": ["Finding shortcuts", "Deep understanding", "Avoiding learning", "Staying ignorant"],
                    "correct_answer": 1,
                    "points": 25
                }
            ],
            "total_points": 50
        }
    ]
    quizzes_collection.insert_many(quizzes)
    print("✓ Inserted sample quizzes")
    
    print("\n✓ Database initialization complete!")
    print(f"✓ Created {len(students)} students")
    print(f"✓ Created {len(teachers)} teachers")
    print(f"✓ Created {len(pathways)} pathways")
    print(f"✓ Created {len(quizzes)} quizzes")


if __name__ == "__main__":
    init_database()






