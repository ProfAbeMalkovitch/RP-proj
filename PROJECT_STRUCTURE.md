# ILPG Project Structure

## Standard Folder Organization

```
ILPG/
├── README.md                          # Main project documentation
├── .gitignore                         # Git ignore rules
├── docs/                              # All documentation
│   ├── guides/                        # User and developer guides
│   │   ├── adaptive-learning/
│   │   ├── quiz-integration/
│   │   ├── roadmap/
│   │   └── setup/
│   ├── api/                           # API documentation
│   └── troubleshooting/               # Troubleshooting guides
├── backend/
│   ├── app/                           # Main application code
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── database.py                # Database connection
│   │   ├── models/                    # Pydantic models
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── routes/                     # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── students.py
│   │   │   ├── teachers.py
│   │   │   ├── pathways.py
│   │   │   ├── quizzes.py
│   │   │   ├── results.py
│   │   │   ├── tasks.py
│   │   │   ├── analytics.py
│   │   │   ├── adaptive_learning.py
│   │   │   └── roadmap.py
│   │   ├── services/                   # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── adaptive_learning_service.py
│   │   │   └── roadmap_generation_service.py
│   │   ├── controllers/                # Request handlers
│   │   │   ├── __init__.py
│   │   │   └── auth_controller.py
│   │   ├── middleware/                 # Middleware
│   │   │   ├── __init__.py
│   │   │   └── auth_middleware.py
│   │   └── utils/                      # Utility functions
│   │       ├── __init__.py
│   │       ├── pathway_calculator.py
│   │       ├── jwt_auth.py
│   │       └── password.py
│   ├── scripts/                       # Utility scripts
│   │   ├── init_db.py                 # Database initialization
│   │   ├── init_roadmap_templates.py  # Roadmap templates init
│   │   ├── seeders/                   # Data seeders
│   │   │   ├── __init__.py
│   │   │   ├── seed_students.py
│   │   │   ├── seed_teachers.py
│   │   │   └── seed_admins.py
│   │   └── tests/                     # Test scripts
│   │       ├── test_adaptive_learning.py
│   │       ├── test_mongodb_connection.py
│   │       ├── check_admin_account.py
│   │       └── verify_seed.py
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment variables template
│   └── venv/                          # Virtual environment (gitignored)
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/                  # Authentication components
│   │   │   │   ├── Login.js
│   │   │   │   ├── StudentLogin.js
│   │   │   │   ├── TeacherLogin.js
│   │   │   │   └── AdminLogin.js
│   │   │   ├── dashboards/            # Dashboard components
│   │   │   │   ├── StudentDashboard.js
│   │   │   │   ├── TeacherDashboard.js
│   │   │   │   ├── AdminDashboard.js
│   │   │   │   ├── TaskDetail.js
│   │   │   │   └── TaskQuiz.js
│   │   │   ├── shared/                # Shared components
│   │   │   │   ├── SideNavigation.js
│   │   │   │   ├── PathwayBadge.js
│   │   │   │   ├── ConceptMasteryCard.js
│   │   │   │   └── RecommendationsCard.js
│   │   │   ├── MindMap.js
│   │   │   ├── Roadmap.js
│   │   │   ├── PathwayDetail.js
│   │   │   ├── Quiz.js
│   │   │   ├── GenerateRoadmapButton.js
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.js                 # API service layer
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── node_modules/                  # Dependencies (gitignored)
├── examples/                           # Example files
│   ├── sample_quiz.json
│   └── import_quizzes.py
└── .gitignore
```




