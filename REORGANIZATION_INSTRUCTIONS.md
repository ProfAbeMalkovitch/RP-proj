# Project Reorganization Instructions

## ✅ Completed

1. ✅ Created `docs/` folder structure
2. ✅ Created `.gitignore` file
3. ✅ Created documentation structure
4. ✅ Updated README.md

## 📋 Manual Steps Required

Due to file system constraints, please manually complete these steps:

### 1. Move Backend Scripts

Create `backend/scripts/` directory and move:

**From `backend/` to `backend/scripts/`:**
- `init_db.py`
- `init_roadmap_templates.py`

**From `backend/seeders/` to `backend/scripts/seeders/`:**
- `seed_students.py`
- `seed_teachers.py`
- `seed_admins.py`
- `__init__.py`

**From `backend/` to `backend/scripts/tests/`:**
- `test_adaptive_learning.py`
- `test_mongodb_connection.py`
- `check_admin_account.py`
- `verify_seed.py`

### 2. Update Import Paths in Scripts

After moving, update imports in moved scripts:

**In `backend/scripts/init_db.py`**, add at the top:
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**In `backend/scripts/seeders/*.py`**, update imports:
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
```

**In `backend/scripts/tests/*.py`**, add:
```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### 3. Move Documentation Files

Move all `.md` files from root to `docs/` (except README.md and PROJECT_STRUCTURE.md):

**To `docs/guides/adaptive-learning/`:**
- `ADAPTIVE_LEARNING_*.md` files

**To `docs/guides/quiz-integration/`:**
- `QUIZ_INTEGRATION*.md`
- `QUICK_START_QUIZ_IMPORT.md`

**To `docs/guides/roadmap/`:**
- `ROADMAP*.md` files

**To `docs/guides/setup/`:**
- `SETUP.md`
- `HOW_TO*.md` files

**To `docs/troubleshooting/`:**
- `MONGODB*.md` files
- `*CONNECTION*.md` files

**To `docs/` (root):**
- `BLACK_WHITE_CSS_THEME_GUIDE.md`
- `WHERE_TO_FIND*.md`
- `QUICK_CHECK*.md`

### 4. Create .env.example

Create `backend/.env.example` with:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database_name?retryWrites=true&w=majority
DATABASE_NAME=ilpg_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## 📁 Final Structure

```
ILPG/
├── README.md
├── PROJECT_STRUCTURE.md
├── .gitignore
├── docs/
│   ├── guides/
│   │   ├── adaptive-learning/
│   │   ├── quiz-integration/
│   │   ├── roadmap/
│   │   └── setup/
│   ├── api/
│   ├── troubleshooting/
│   └── *.md (other docs)
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   ├── controllers/
│   ├── middleware/
│   ├── utils/
│   └── scripts/
│       ├── init_db.py
│       ├── init_roadmap_templates.py
│       ├── seeders/
│       └── tests/
├── frontend/
└── examples/
```

## ✅ Verification

After reorganization, verify:

1. ✅ All scripts in `backend/scripts/`
2. ✅ All docs in `docs/`
3. ✅ `.gitignore` in root
4. ✅ `.env.example` in `backend/`
5. ✅ Import paths updated in scripts
6. ✅ Scripts run correctly

## 🚀 Running Scripts After Reorganization

```bash
# Database initialization
cd backend
python scripts/init_db.py

# Roadmap templates
python scripts/init_roadmap_templates.py

# Tests
python scripts/tests/test_adaptive_learning.py
```




