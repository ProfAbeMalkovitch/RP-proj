# ILPG - Intelligent Learning Path Generator

A full-stack learning management system that provides personalized learning pathways with interactive quizzes, mind maps, and roadmaps.

## Features

- **Student Authentication**: Login system for students, teachers, and admins
- **Three Learning Pathways**: Basic, Intermediate, and Accelerated levels
- **Adaptive Learning**: Automatic student categorization based on performance
- **Personalized Roadmaps**: AI-generated learning paths based on student needs
- **Mind Maps**: Visual representation of learning concepts and weak areas
- **Interactive Quizzes**: Take quizzes and get instant feedback
- **Score Tracking**: Comprehensive score tracking and analytics
- **Task Assignment**: Teachers can assign quizzes to students
- **Modern UI**: Clean and responsive user interface

## Tech Stack

### Frontend
- React 18.2.0
- React Router DOM 6.20.0
- Axios for API calls
- SweetAlert2 for notifications
- CSS3 for styling

### Backend
- Python 3.8+
- FastAPI 0.104.1
- MongoDB with PyMongo
- Pydantic for data validation
- JWT Authentication

### Database
- MongoDB (Atlas or Local)

## Project Structure

```
ILPG/
├── README.md                    # This file
├── PROJECT_STRUCTURE.md         # Detailed structure
├── .gitignore                   # Git ignore rules
│
├── docs/                        # Documentation
│   ├── guides/                  # User and developer guides
│   ├── api/                     # API documentation
│   └── troubleshooting/         # Troubleshooting guides
│
├── backend/                     # Backend (Python/FastAPI)
│   ├── main.py                  # FastAPI app entry point
│   ├── database.py              # Database connection
│   ├── models.py                # Data models
│   ├── routes/                  # API routes
│   ├── services/                # Business logic
│   ├── controllers/             # Request handlers
│   ├── middleware/              # Middleware
│   ├── utils/                   # Utilities
│   ├── scripts/                 # Utility scripts
│   │   ├── init_db.py          # Database initialization
│   │   ├── seeders/             # Data seeders
│   │   └── tests/               # Test scripts
│   └── requirements.txt        # Python dependencies
│
├── frontend/                    # Frontend (React)
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API services
│   │   └── App.js              # Main app
│   └── package.json
│
└── examples/                    # Example files
    ├── sample_quiz.json
    └── import_quizzes.py
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- MongoDB (local or Atlas)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update MongoDB URI and other settings

5. Initialize database:
```bash
python scripts/init_db.py
```

6. Start server:
```bash
python main.py
# Or
uvicorn main:app --reload
```

Backend runs on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Documentation

- **Project Structure**: See `PROJECT_STRUCTURE.md`
- **Adaptive Learning**: `docs/guides/adaptive-learning/`
- **Quiz Integration**: `docs/guides/quiz-integration/`
- **Roadmap System**: `docs/guides/roadmap/`
- **Setup Guides**: `docs/guides/setup/`
- **Troubleshooting**: `docs/troubleshooting/`

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Demo Credentials

After running `init_db.py`, you can login with:
- **Student**: `student@example.com` / `password123`
- **Teacher**: `teacher@example.com` / `password123`
- **Admin**: `admin@example.com` / `admin123`

## Key Features

### Adaptive Learning
- Automatic student categorization (Basic/Intermediate/Accelerated)
- Personalized recommendations
- Weak area identification
- Concept mastery tracking

### Roadmap Generation
- AI-powered personalized roadmaps
- Template-based generation
- Focus on weak areas
- Progressive learning paths

### Quiz System
- Interactive quizzes
- Instant feedback
- Score tracking
- Teacher-assigned tasks

## Development

### Running Tests
```bash
cd backend
python scripts/tests/test_adaptive_learning.py
python scripts/tests/test_mongodb_connection.py
```

### Database Seeding
```bash
cd backend
python scripts/seeders/seed_students.py
python scripts/seeders/seed_teachers.py
```

## Contributing

This is a research project. For contributions:
1. Follow the project structure
2. Update documentation
3. Write tests for new features
4. Follow Python/JavaScript best practices

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
- Check `docs/troubleshooting/` for common issues
- Review API documentation at `/docs` endpoint
- Check setup guides in `docs/guides/setup/`
