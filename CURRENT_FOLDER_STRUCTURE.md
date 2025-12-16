# Current ILPG Folder Structure

## 📁 Your Current Project Structure

```
ILPG/
│
├── 📄 README.md
├── 📄 PROJECT_STRUCTURE.md
├── 📄 REORGANIZATION_INSTRUCTIONS.md
├── 📄 .gitignore
│
├── 📚 Documentation Files (Root - Need to move to docs/)
│   ├── ADAPTIVE_LEARNING_ENGINE_GUIDE.md
│   ├── ADAPTIVE_LEARNING_FEATURES.md
│   ├── ADAPTIVE_LEARNING_IMPLEMENTATION.md
│   ├── ADAPTIVE_LEARNING_TESTING_GUIDE.md
│   ├── BLACK_WHITE_CSS_THEME_GUIDE.md
│   ├── HOW_TO_CHECK_ADAPTIVE_LEARNING.md
│   ├── HOW_TO_LOGIN_AS_ADMIN.md
│   ├── MONGODB_CONNECTION_FIX.md
│   ├── QUICK_CHECK_ADAPTIVE_LEARNING.md
│   ├── QUICK_START_QUIZ_IMPORT.md
│   ├── QUIZ_INTEGRATION_GUIDE.md
│   ├── ROADMAP_GENERATION_SYSTEM.md
│   ├── ROADMAP_TEMPLATES_GUIDE.md
│   ├── SETUP.md
│   └── WHERE_TO_FIND_ADAPTIVE_LEARNING_FEATURES.md
│
├── 📁 docs/                          # Documentation folder (partially organized)
│   ├── REORGANIZATION_GUIDE.md
│   └── STRUCTURE_SUMMARY.md
│
├── 🐍 backend/                       # Backend (Python/FastAPI)
│   ├── main.py                      # FastAPI app entry point
│   ├── database.py                  # MongoDB connection
│   ├── models.py                    # Pydantic models
│   ├── requirements.txt             # Python dependencies
│   │
│   ├── 📁 routes/                   # API Routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── students.py
│   │   ├── teachers.py
│   │   ├── pathways.py
│   │   ├── quizzes.py
│   │   ├── results.py
│   │   ├── tasks.py
│   │   ├── analytics.py
│   │   ├── adaptive_learning.py
│   │   └── roadmap.py
│   │
│   ├── 📁 services/                  # Business Logic
│   │   ├── adaptive_learning_service.py
│   │   └── roadmap_generation_service.py
│   │
│   ├── 📁 controllers/               # Request Handlers
│   │   ├── __init__.py
│   │   └── auth_controller.py
│   │
│   ├── 📁 middleware/                # Middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   │
│   ├── 📁 utils/                     # Utilities
│   │   ├── __init__.py
│   │   ├── pathway_calculator.py
│   │   ├── jwt_auth.py
│   │   └── password.py
│   │
│   ├── 📁 seeders/                   # Data Seeders (should move to scripts/)
│   │   ├── __init__.py
│   │   ├── seed_students.py
│   │   ├── seed_teachers.py
│   │   └── seed_admins.py
│   │
│   ├── 📁 docs/                      # Backend docs (should move to root docs/)
│   │   ├── api/
│   │   ├── guides/
│   │   │   ├── adaptive-learning/
│   │   │   ├── quiz-integration/
│   │   │   ├── roadmap/
│   │   │   └── setup/
│   │   ├── troubleshooting/
│   │   │   ├── MONGODB_SETUP.md
│   │   │   ├── MONGODB_TROUBLESHOOTING.md
│   │   │   └── QUICK_FIX_MONGODB.md
│   │   ├── IMPLEMENTATION_GUIDE.md
│   │   └── QUICK_START.md
│   │
│   ├── 📁 backend/                   # ⚠️ Nested folder (should be removed)
│   │   └── scripts/
│   │       ├── seeders/
│   │       └── tests/
│   │
│   ├── ⚙️ Scripts (should move to scripts/ folder)
│   ├── init_db.py                    # → should be in scripts/
│   ├── init_roadmap_templates.py    # → should be in scripts/
│   ├── test_adaptive_learning.py    # → should be in scripts/tests/
│   ├── test_mongodb_connection.py   # → should be in scripts/tests/
│   ├── check_admin_account.py       # → should be in scripts/tests/
│   └── verify_seed.py               # → should be in scripts/tests/
│   │
│   └── 📁 venv/                      # Virtual environment (gitignored)
│
├── ⚛️ frontend/                      # Frontend (React)
│   ├── package.json
│   ├── package-lock.json
│   │
│   ├── 📁 public/
│   │   └── index.html
│   │
│   ├── 📁 src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   │
│   │   ├── 📁 components/
│   │   │   ├── 📁 auth/              # Authentication components
│   │   │   │   ├── AdminLogin.js
│   │   │   │   ├── StudentLogin.js
│   │   │   │   ├── TeacherLogin.js
│   │   │   │   └── Login.css
│   │   │   │
│   │   │   ├── 📁 dashboards/        # Dashboard components
│   │   │   │   ├── StudentDashboard.js
│   │   │   │   ├── StudentDashboard.css
│   │   │   │   ├── TeacherDashboard.js
│   │   │   │   ├── TeacherDashboard.css
│   │   │   │   ├── AdminDashboard.js
│   │   │   │   ├── AdminDashboard.css
│   │   │   │   ├── TaskDetail.js
│   │   │   │   ├── TaskDetail.css
│   │   │   │   ├── TaskQuiz.js
│   │   │   │   └── TaskQuiz.css
│   │   │   │
│   │   │   ├── 📁 shared/            # Shared components
│   │   │   │   ├── SideNavigation.js
│   │   │   │   ├── SideNavigation.css
│   │   │   │   ├── PathwayBadge.js
│   │   │   │   ├── PathwayBadge.css
│   │   │   │   ├── ConceptMasteryCard.js
│   │   │   │   ├── ConceptMasteryCard.css
│   │   │   │   ├── RecommendationsCard.js
│   │   │   │   └── RecommendationsCard.css
│   │   │   │
│   │   │   ├── Login.js
│   │   │   ├── Login.css
│   │   │   ├── Dashboard.js
│   │   │   ├── Dashboard.css
│   │   │   ├── MindMap.js
│   │   │   ├── MindMap.css
│   │   │   ├── Roadmap.js
│   │   │   ├── Roadmap.css
│   │   │   ├── PathwayDetail.js
│   │   │   ├── PathwayDetail.css
│   │   │   ├── Quiz.js
│   │   │   ├── Quiz.css
│   │   │   ├── QuizResultModal.js
│   │   │   ├── QuizResultModal.css
│   │   │   ├── GenerateRoadmapButton.js
│   │   │   ├── GenerateRoadmapButton.css
│   │   │   ├── StudentDetailModal.js
│   │   │   ├── StudentDetailModal.css
│   │   │   ├── StudentProgressModal.js
│   │   │   └── StudentProgressModal.css
│   │   │
│   │   └── 📁 services/
│   │       └── api.js               # API service layer
│   │
│   └── 📁 node_modules/              # Dependencies (gitignored)
│
└── 📝 examples/                      # Example files
    ├── sample_quiz.json
    └── import_quizzes.py
```

## 📊 Summary

### ✅ Well Organized:
- **Frontend**: Properly structured with components, services, etc.
- **Backend Routes**: All API routes in `routes/` folder
- **Backend Services**: Business logic in `services/` folder
- **Backend Utils**: Utility functions in `utils/` folder
- **Examples**: Example files in `examples/` folder

### ⚠️ Needs Organization:
1. **Documentation**: Many `.md` files in root should be in `docs/`
2. **Backend Scripts**: Should be in `backend/scripts/` folder
3. **Nested Backend**: `backend/backend/` folder should be removed
4. **Backend Docs**: `backend/docs/` should be merged with root `docs/`

### 📋 Quick Stats:
- **Root Markdown Files**: 17 files (should be in docs/)
- **Backend Scripts**: 6 files (should be in scripts/)
- **Backend Routes**: 9 route files ✅
- **Frontend Components**: ~30+ components ✅
- **Documentation Folders**: Partially organized

## 🎯 Recommended Actions:

1. Move all root `.md` files to `docs/` organized by topic
2. Create `backend/scripts/` and move all scripts there
3. Remove `backend/backend/` nested folder
4. Merge `backend/docs/` with root `docs/`
5. Create `backend/.env.example` file

See `REORGANIZATION_INSTRUCTIONS.md` for detailed steps!




