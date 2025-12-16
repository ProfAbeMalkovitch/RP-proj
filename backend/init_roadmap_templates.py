"""
Initialize Roadmap Templates
High-quality template seeding for knowledge-based roadmap generation
"""
from datetime import datetime
from database import roadmap_templates_collection, teachers_collection


def init_roadmap_templates():
    """Initialize database with high-quality roadmap templates"""
    
    # Get a teacher ID (assuming at least one teacher exists)
    teacher = teachers_collection.find_one({})
    teacher_id = teacher.get("teacher_id", "teacher_1") if teacher else "teacher_1"
    
    templates = [
        {
            "template_id": "template_statistics_remediation",
            "name": "Statistics Fundamentals Remediation",
            "description": "Comprehensive roadmap for students struggling with statistics concepts. Focuses on building foundational understanding through structured learning.",
            "created_by": teacher_id,
            "target_concepts": ["statistics", "data_analysis", "probability"],
            "pathway_level": "Intermediate",
            "difficulty": "beginner",
            "weak_area_focus": True,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "stat_intro",
                    "title": "Introduction to Statistics",
                    "description": "Learn the fundamentals of statistics, including basic terminology, data types, and statistical thinking. This module provides the foundation for all advanced statistical concepts.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 60,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Understand basic statistical terminology",
                        "Identify different types of data",
                        "Recognize statistical patterns"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["statistics", "foundation", "theory"]
                },
                {
                    "task_id": "stat_basics_quiz",
                    "title": "Statistics Basics Assessment Quiz",
                    "description": "Test your understanding of basic statistical concepts with this comprehensive quiz.",
                    "task_type": "quiz",
                    "order": 2,
                    "estimated_time": 30,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Assess understanding of basic concepts",
                        "Identify areas needing more practice"
                    ],
                    "quiz_id": None,  # Can be linked to actual quiz
                    "resource_url": None,
                    "prerequisites": ["stat_intro"],
                    "tags": ["statistics", "assessment", "quiz"]
                },
                {
                    "task_id": "stat_descriptive",
                    "title": "Descriptive Statistics Practice",
                    "description": "Practice calculating and interpreting mean, median, mode, variance, and standard deviation. Work through real-world examples.",
                    "task_type": "practice",
                    "order": 3,
                    "estimated_time": 90,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Calculate descriptive statistics",
                        "Interpret statistical measures",
                        "Apply concepts to real data"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_intro"],
                    "tags": ["statistics", "practice", "descriptive"]
                },
                {
                    "task_id": "stat_distributions",
                    "title": "Probability Distributions",
                    "description": "Learn about normal, binomial, and other probability distributions. Understand when and how to use each distribution.",
                    "task_type": "reading",
                    "order": 4,
                    "estimated_time": 75,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand different probability distributions",
                        "Identify appropriate distributions for scenarios",
                        "Calculate probabilities using distributions"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_basics_quiz"],
                    "tags": ["statistics", "probability", "distributions"]
                },
                {
                    "task_id": "stat_comprehensive_quiz",
                    "title": "Statistics Comprehensive Assessment",
                    "description": "Final comprehensive quiz covering all statistics fundamentals learned so far.",
                    "task_type": "quiz",
                    "order": 5,
                    "estimated_time": 45,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Comprehensive assessment of statistics knowledge",
                        "Validate learning progress"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_descriptive", "stat_distributions"],
                    "tags": ["statistics", "comprehensive", "assessment"]
                }
            ],
            "prerequisites": {
                "algebra": 0.5,
                "basic_math": 0.6
            },
            "estimated_total_time": 300,
            "learning_outcomes": [
                "Strong foundation in statistical thinking",
                "Ability to calculate and interpret descriptive statistics",
                "Understanding of probability distributions",
                "Confidence in solving basic statistics problems"
            ],
            "tags": ["statistics", "remediation", "weak-area", "fundamentals"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_algebra_remediation",
            "name": "Algebra Fundamentals Remediation",
            "description": "Step-by-step roadmap for students who need to strengthen their algebra skills. Covers from basics to intermediate concepts.",
            "created_by": teacher_id,
            "target_concepts": ["algebra", "equations", "functions"],
            "pathway_level": "Intermediate",
            "difficulty": "beginner",
            "weak_area_focus": True,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "alg_basics",
                    "title": "Algebra Basics Review",
                    "description": "Review fundamental algebraic concepts including variables, expressions, and basic operations.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 60,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Master basic algebraic operations",
                        "Understand variables and expressions",
                        "Solve simple equations"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["algebra", "basics", "foundation"]
                },
                {
                    "task_id": "alg_equations",
                    "title": "Solving Linear Equations",
                    "description": "Learn techniques for solving linear equations, including multi-step problems and word problems.",
                    "task_type": "practice",
                    "order": 2,
                    "estimated_time": 90,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Solve linear equations systematically",
                        "Apply algebraic techniques to word problems",
                        "Check solutions for accuracy"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_basics"],
                    "tags": ["algebra", "equations", "practice"]
                },
                {
                    "task_id": "alg_functions",
                    "title": "Introduction to Functions",
                    "description": "Understand what functions are, how to evaluate them, and basic function operations.",
                    "task_type": "reading",
                    "order": 3,
                    "estimated_time": 75,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Define and identify functions",
                        "Evaluate functions",
                        "Perform function operations"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_equations"],
                    "tags": ["algebra", "functions", "theory"]
                },
                {
                    "task_id": "alg_assessment",
                    "title": "Algebra Progress Assessment",
                    "description": "Comprehensive quiz to assess your algebra knowledge and identify remaining weak areas.",
                    "task_type": "quiz",
                    "order": 4,
                    "estimated_time": 45,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Assess current algebra proficiency",
                        "Identify areas for continued practice"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_functions"],
                    "tags": ["algebra", "assessment", "quiz"]
                }
            ],
            "prerequisites": {
                "basic_math": 0.6
            },
            "estimated_total_time": 270,
            "learning_outcomes": [
                "Solid understanding of algebraic fundamentals",
                "Ability to solve linear equations confidently",
                "Basic understanding of functions",
                "Foundation for advanced algebra topics"
            ],
            "tags": ["algebra", "remediation", "weak-area", "equations"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_geometry_mastery",
            "name": "Geometry Concepts Mastery",
            "description": "Advanced roadmap for students ready to master geometry concepts and problem-solving techniques.",
            "created_by": teacher_id,
            "target_concepts": ["geometry", "shapes", "angles", "measurements"],
            "pathway_level": "Excellent",
            "difficulty": "advanced",
            "weak_area_focus": False,
            "mastery_focus": True,
            "tasks": [
                {
                    "task_id": "geo_advanced",
                    "title": "Advanced Geometry Concepts",
                    "description": "Explore advanced geometric concepts including complex proofs, transformations, and coordinate geometry.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 90,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Master advanced geometric theorems",
                        "Understand coordinate geometry",
                        "Learn transformation techniques"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["geometry", "advanced", "theory"]
                },
                {
                    "task_id": "geo_problem_solving",
                    "title": "Complex Geometry Problem Solving",
                    "description": "Practice solving complex geometry problems requiring multi-step reasoning and creative thinking.",
                    "task_type": "practice",
                    "order": 2,
                    "estimated_time": 120,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Develop problem-solving strategies",
                        "Apply multiple geometric concepts",
                        "Think creatively about solutions"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["geo_advanced"],
                    "tags": ["geometry", "problem-solving", "practice"]
                },
                {
                    "task_id": "geo_project",
                    "title": "Geometry Application Project",
                    "description": "Create a real-world project applying advanced geometry concepts to solve practical problems.",
                    "task_type": "project",
                    "order": 3,
                    "estimated_time": 180,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Apply geometry to real-world scenarios",
                        "Demonstrate mastery through projects",
                        "Develop critical thinking skills"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["geo_problem_solving"],
                    "tags": ["geometry", "project", "application"]
                }
            ],
            "prerequisites": {
                "geometry": 0.8,
                "algebra": 0.7
            },
            "estimated_total_time": 390,
            "learning_outcomes": [
                "Mastery of advanced geometry concepts",
                "Ability to solve complex geometric problems",
                "Real-world application skills",
                "Expert-level geometric reasoning"
            ],
            "tags": ["geometry", "mastery", "advanced", "excellent"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_calculus_intro",
            "name": "Introduction to Calculus",
            "description": "Beginner-friendly roadmap introducing calculus concepts for students transitioning to advanced mathematics.",
            "created_by": teacher_id,
            "target_concepts": ["calculus", "derivatives", "limits"],
            "pathway_level": "Excellent",
            "difficulty": "intermediate",
            "weak_area_focus": False,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "calc_limits",
                    "title": "Understanding Limits",
                    "description": "Introduction to the fundamental concept of limits in calculus. Learn what limits are and how to evaluate them.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 90,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand the concept of limits",
                        "Evaluate basic limits",
                        "Recognize limit behaviors"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["calculus", "limits", "introduction"]
                },
                {
                    "task_id": "calc_derivatives",
                    "title": "Introduction to Derivatives",
                    "description": "Learn what derivatives are, how to calculate them, and their real-world applications.",
                    "task_type": "reading",
                    "order": 2,
                    "estimated_time": 120,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand derivatives conceptually",
                        "Calculate basic derivatives",
                        "Apply derivatives to problems"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_limits"],
                    "tags": ["calculus", "derivatives", "concepts"]
                },
                {
                    "task_id": "calc_practice",
                    "title": "Calculus Practice Problems",
                    "description": "Extensive practice with limits and derivatives to build confidence and proficiency.",
                    "task_type": "practice",
                    "order": 3,
                    "estimated_time": 150,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Master derivative calculations",
                        "Apply calculus to various problems",
                        "Build problem-solving confidence"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_derivatives"],
                    "tags": ["calculus", "practice", "problems"]
                },
                {
                    "task_id": "calc_assessment",
                    "title": "Calculus Fundamentals Assessment",
                    "description": "Comprehensive assessment of your understanding of limits and derivatives.",
                    "task_type": "quiz",
                    "order": 4,
                    "estimated_time": 60,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Assess calculus understanding",
                        "Validate learning progress"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_practice"],
                    "tags": ["calculus", "assessment", "quiz"]
                }
            ],
            "prerequisites": {
                "algebra": 0.8,
                "trigonometry": 0.7
            },
            "estimated_total_time": 420,
            "learning_outcomes": [
                "Solid understanding of limits",
                "Proficiency with basic derivatives",
                "Foundation for advanced calculus",
                "Confidence in calculus problem-solving"
            ],
            "tags": ["calculus", "introduction", "advanced", "excellent"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        }
    ]
    
    # Check if templates already exist
    existing_templates = list(roadmap_templates_collection.find({}, {"template_id": 1}))
    existing_ids = {t["template_id"] for t in existing_templates}
    
    # Insert new templates
    new_templates = [t for t in templates if t["template_id"] not in existing_ids]
    
    if new_templates:
        roadmap_templates_collection.insert_many(new_templates)
        print(f"[SUCCESS] Inserted {len(new_templates)} roadmap templates")
    else:
        print("[INFO] Roadmap templates already exist")
    
    print(f"[INFO] Total templates in database: {roadmap_templates_collection.count_documents({})}")
    
    return templates


if __name__ == "__main__":
    init_roadmap_templates()





High-quality template seeding for knowledge-based roadmap generation
"""
from datetime import datetime
from database import roadmap_templates_collection, teachers_collection


def init_roadmap_templates():
    """Initialize database with high-quality roadmap templates"""
    
    # Get a teacher ID (assuming at least one teacher exists)
    teacher = teachers_collection.find_one({})
    teacher_id = teacher.get("teacher_id", "teacher_1") if teacher else "teacher_1"
    
    templates = [
        {
            "template_id": "template_statistics_remediation",
            "name": "Statistics Fundamentals Remediation",
            "description": "Comprehensive roadmap for students struggling with statistics concepts. Focuses on building foundational understanding through structured learning.",
            "created_by": teacher_id,
            "target_concepts": ["statistics", "data_analysis", "probability"],
            "pathway_level": "Intermediate",
            "difficulty": "beginner",
            "weak_area_focus": True,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "stat_intro",
                    "title": "Introduction to Statistics",
                    "description": "Learn the fundamentals of statistics, including basic terminology, data types, and statistical thinking. This module provides the foundation for all advanced statistical concepts.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 60,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Understand basic statistical terminology",
                        "Identify different types of data",
                        "Recognize statistical patterns"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["statistics", "foundation", "theory"]
                },
                {
                    "task_id": "stat_basics_quiz",
                    "title": "Statistics Basics Assessment Quiz",
                    "description": "Test your understanding of basic statistical concepts with this comprehensive quiz.",
                    "task_type": "quiz",
                    "order": 2,
                    "estimated_time": 30,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Assess understanding of basic concepts",
                        "Identify areas needing more practice"
                    ],
                    "quiz_id": None,  # Can be linked to actual quiz
                    "resource_url": None,
                    "prerequisites": ["stat_intro"],
                    "tags": ["statistics", "assessment", "quiz"]
                },
                {
                    "task_id": "stat_descriptive",
                    "title": "Descriptive Statistics Practice",
                    "description": "Practice calculating and interpreting mean, median, mode, variance, and standard deviation. Work through real-world examples.",
                    "task_type": "practice",
                    "order": 3,
                    "estimated_time": 90,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Calculate descriptive statistics",
                        "Interpret statistical measures",
                        "Apply concepts to real data"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_intro"],
                    "tags": ["statistics", "practice", "descriptive"]
                },
                {
                    "task_id": "stat_distributions",
                    "title": "Probability Distributions",
                    "description": "Learn about normal, binomial, and other probability distributions. Understand when and how to use each distribution.",
                    "task_type": "reading",
                    "order": 4,
                    "estimated_time": 75,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand different probability distributions",
                        "Identify appropriate distributions for scenarios",
                        "Calculate probabilities using distributions"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_basics_quiz"],
                    "tags": ["statistics", "probability", "distributions"]
                },
                {
                    "task_id": "stat_comprehensive_quiz",
                    "title": "Statistics Comprehensive Assessment",
                    "description": "Final comprehensive quiz covering all statistics fundamentals learned so far.",
                    "task_type": "quiz",
                    "order": 5,
                    "estimated_time": 45,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Comprehensive assessment of statistics knowledge",
                        "Validate learning progress"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["stat_descriptive", "stat_distributions"],
                    "tags": ["statistics", "comprehensive", "assessment"]
                }
            ],
            "prerequisites": {
                "algebra": 0.5,
                "basic_math": 0.6
            },
            "estimated_total_time": 300,
            "learning_outcomes": [
                "Strong foundation in statistical thinking",
                "Ability to calculate and interpret descriptive statistics",
                "Understanding of probability distributions",
                "Confidence in solving basic statistics problems"
            ],
            "tags": ["statistics", "remediation", "weak-area", "fundamentals"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_algebra_remediation",
            "name": "Algebra Fundamentals Remediation",
            "description": "Step-by-step roadmap for students who need to strengthen their algebra skills. Covers from basics to intermediate concepts.",
            "created_by": teacher_id,
            "target_concepts": ["algebra", "equations", "functions"],
            "pathway_level": "Intermediate",
            "difficulty": "beginner",
            "weak_area_focus": True,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "alg_basics",
                    "title": "Algebra Basics Review",
                    "description": "Review fundamental algebraic concepts including variables, expressions, and basic operations.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 60,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Master basic algebraic operations",
                        "Understand variables and expressions",
                        "Solve simple equations"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["algebra", "basics", "foundation"]
                },
                {
                    "task_id": "alg_equations",
                    "title": "Solving Linear Equations",
                    "description": "Learn techniques for solving linear equations, including multi-step problems and word problems.",
                    "task_type": "practice",
                    "order": 2,
                    "estimated_time": 90,
                    "difficulty": "beginner",
                    "learning_objectives": [
                        "Solve linear equations systematically",
                        "Apply algebraic techniques to word problems",
                        "Check solutions for accuracy"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_basics"],
                    "tags": ["algebra", "equations", "practice"]
                },
                {
                    "task_id": "alg_functions",
                    "title": "Introduction to Functions",
                    "description": "Understand what functions are, how to evaluate them, and basic function operations.",
                    "task_type": "reading",
                    "order": 3,
                    "estimated_time": 75,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Define and identify functions",
                        "Evaluate functions",
                        "Perform function operations"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_equations"],
                    "tags": ["algebra", "functions", "theory"]
                },
                {
                    "task_id": "alg_assessment",
                    "title": "Algebra Progress Assessment",
                    "description": "Comprehensive quiz to assess your algebra knowledge and identify remaining weak areas.",
                    "task_type": "quiz",
                    "order": 4,
                    "estimated_time": 45,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Assess current algebra proficiency",
                        "Identify areas for continued practice"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["alg_functions"],
                    "tags": ["algebra", "assessment", "quiz"]
                }
            ],
            "prerequisites": {
                "basic_math": 0.6
            },
            "estimated_total_time": 270,
            "learning_outcomes": [
                "Solid understanding of algebraic fundamentals",
                "Ability to solve linear equations confidently",
                "Basic understanding of functions",
                "Foundation for advanced algebra topics"
            ],
            "tags": ["algebra", "remediation", "weak-area", "equations"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_geometry_mastery",
            "name": "Geometry Concepts Mastery",
            "description": "Advanced roadmap for students ready to master geometry concepts and problem-solving techniques.",
            "created_by": teacher_id,
            "target_concepts": ["geometry", "shapes", "angles", "measurements"],
            "pathway_level": "Excellent",
            "difficulty": "advanced",
            "weak_area_focus": False,
            "mastery_focus": True,
            "tasks": [
                {
                    "task_id": "geo_advanced",
                    "title": "Advanced Geometry Concepts",
                    "description": "Explore advanced geometric concepts including complex proofs, transformations, and coordinate geometry.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 90,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Master advanced geometric theorems",
                        "Understand coordinate geometry",
                        "Learn transformation techniques"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["geometry", "advanced", "theory"]
                },
                {
                    "task_id": "geo_problem_solving",
                    "title": "Complex Geometry Problem Solving",
                    "description": "Practice solving complex geometry problems requiring multi-step reasoning and creative thinking.",
                    "task_type": "practice",
                    "order": 2,
                    "estimated_time": 120,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Develop problem-solving strategies",
                        "Apply multiple geometric concepts",
                        "Think creatively about solutions"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["geo_advanced"],
                    "tags": ["geometry", "problem-solving", "practice"]
                },
                {
                    "task_id": "geo_project",
                    "title": "Geometry Application Project",
                    "description": "Create a real-world project applying advanced geometry concepts to solve practical problems.",
                    "task_type": "project",
                    "order": 3,
                    "estimated_time": 180,
                    "difficulty": "advanced",
                    "learning_objectives": [
                        "Apply geometry to real-world scenarios",
                        "Demonstrate mastery through projects",
                        "Develop critical thinking skills"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["geo_problem_solving"],
                    "tags": ["geometry", "project", "application"]
                }
            ],
            "prerequisites": {
                "geometry": 0.8,
                "algebra": 0.7
            },
            "estimated_total_time": 390,
            "learning_outcomes": [
                "Mastery of advanced geometry concepts",
                "Ability to solve complex geometric problems",
                "Real-world application skills",
                "Expert-level geometric reasoning"
            ],
            "tags": ["geometry", "mastery", "advanced", "excellent"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        },
        {
            "template_id": "template_calculus_intro",
            "name": "Introduction to Calculus",
            "description": "Beginner-friendly roadmap introducing calculus concepts for students transitioning to advanced mathematics.",
            "created_by": teacher_id,
            "target_concepts": ["calculus", "derivatives", "limits"],
            "pathway_level": "Excellent",
            "difficulty": "intermediate",
            "weak_area_focus": False,
            "mastery_focus": False,
            "tasks": [
                {
                    "task_id": "calc_limits",
                    "title": "Understanding Limits",
                    "description": "Introduction to the fundamental concept of limits in calculus. Learn what limits are and how to evaluate them.",
                    "task_type": "reading",
                    "order": 1,
                    "estimated_time": 90,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand the concept of limits",
                        "Evaluate basic limits",
                        "Recognize limit behaviors"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": [],
                    "tags": ["calculus", "limits", "introduction"]
                },
                {
                    "task_id": "calc_derivatives",
                    "title": "Introduction to Derivatives",
                    "description": "Learn what derivatives are, how to calculate them, and their real-world applications.",
                    "task_type": "reading",
                    "order": 2,
                    "estimated_time": 120,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Understand derivatives conceptually",
                        "Calculate basic derivatives",
                        "Apply derivatives to problems"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_limits"],
                    "tags": ["calculus", "derivatives", "concepts"]
                },
                {
                    "task_id": "calc_practice",
                    "title": "Calculus Practice Problems",
                    "description": "Extensive practice with limits and derivatives to build confidence and proficiency.",
                    "task_type": "practice",
                    "order": 3,
                    "estimated_time": 150,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Master derivative calculations",
                        "Apply calculus to various problems",
                        "Build problem-solving confidence"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_derivatives"],
                    "tags": ["calculus", "practice", "problems"]
                },
                {
                    "task_id": "calc_assessment",
                    "title": "Calculus Fundamentals Assessment",
                    "description": "Comprehensive assessment of your understanding of limits and derivatives.",
                    "task_type": "quiz",
                    "order": 4,
                    "estimated_time": 60,
                    "difficulty": "intermediate",
                    "learning_objectives": [
                        "Assess calculus understanding",
                        "Validate learning progress"
                    ],
                    "quiz_id": None,
                    "resource_url": None,
                    "prerequisites": ["calc_practice"],
                    "tags": ["calculus", "assessment", "quiz"]
                }
            ],
            "prerequisites": {
                "algebra": 0.8,
                "trigonometry": 0.7
            },
            "estimated_total_time": 420,
            "learning_outcomes": [
                "Solid understanding of limits",
                "Proficiency with basic derivatives",
                "Foundation for advanced calculus",
                "Confidence in calculus problem-solving"
            ],
            "tags": ["calculus", "introduction", "advanced", "excellent"],
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "usage_count": 0
        }
    ]
    
    # Check if templates already exist
    existing_templates = list(roadmap_templates_collection.find({}, {"template_id": 1}))
    existing_ids = {t["template_id"] for t in existing_templates}
    
    # Insert new templates
    new_templates = [t for t in templates if t["template_id"] not in existing_ids]
    
    if new_templates:
        roadmap_templates_collection.insert_many(new_templates)
        print(f"[SUCCESS] Inserted {len(new_templates)} roadmap templates")
    else:
        print("[INFO] Roadmap templates already exist")
    
    print(f"[INFO] Total templates in database: {roadmap_templates_collection.count_documents({})}")
    
    return templates


if __name__ == "__main__":
    init_roadmap_templates()




