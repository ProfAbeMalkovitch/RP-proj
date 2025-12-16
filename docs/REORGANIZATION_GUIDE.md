# Project Reorganization Guide

## Overview

The ILPG project has been reorganized to follow standard project structure conventions for better maintainability and clarity.

## New Structure

### Documentation (`docs/`)
All documentation files have been moved to the `docs/` folder:
- **Guides**: User and developer guides organized by topic
  - `adaptive-learning/` - Adaptive learning features documentation
  - `quiz-integration/` - Quiz content integration guides
  - `roadmap/` - Roadmap generation documentation
  - `setup/` - Setup and installation guides
- **API**: API documentation
- **Troubleshooting**: Troubleshooting guides and fixes

### Backend Scripts (`backend/scripts/`)
All utility scripts have been moved to `backend/scripts/`:
- **Root scripts**: `init_db.py`, `init_roadmap_templates.py`
- **Seeders**: Data seeding scripts (`seed_students.py`, `seed_teachers.py`, `seed_admins.py`)
- **Tests**: Test and verification scripts

### Backend Application (`backend/`)
Main application code remains in `backend/`:
- `main.py` - FastAPI application entry point
- `database.py` - Database connection
- `models.py` - Data models
- `routes/` - API routes
- `services/` - Business logic services
- `controllers/` - Request handlers
- `middleware/` - Middleware functions
- `utils/` - Utility functions

## Running Scripts After Reorganization

### Database Initialization
```bash
cd backend
python scripts/init_db.py
```

### Roadmap Templates Initialization
```bash
cd backend
python scripts/init_roadmap_templates.py
```

### Running Tests
```bash
cd backend
python scripts/tests/test_adaptive_learning.py
python scripts/tests/test_mongodb_connection.py
```

## Import Path Updates

Scripts in `backend/scripts/` have been updated to correctly import from the parent directory. The scripts now add the parent directory to the Python path:

```python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

## File Locations

### Documentation
- Main README: `README.md` (root)
- Project Structure: `PROJECT_STRUCTURE.md` (root)
- All other docs: `docs/` folder

### Backend Scripts
- Database init: `backend/scripts/init_db.py`
- Roadmap init: `backend/scripts/init_roadmap_templates.py`
- Seeders: `backend/scripts/seeders/`
- Tests: `backend/scripts/tests/`

### Configuration
- `.gitignore`: Root directory
- `.env.example`: `backend/.env.example`

## Benefits of New Structure

1. **Better Organization**: Related files are grouped together
2. **Clear Separation**: Scripts separated from application code
3. **Easier Navigation**: Documentation organized by topic
4. **Standard Conventions**: Follows Python/FastAPI best practices
5. **Maintainability**: Easier to find and update files

## Migration Notes

- All import paths in scripts have been updated
- Documentation links may need updating if referenced elsewhere
- CI/CD scripts may need path updates
- Team members should be notified of new script locations




