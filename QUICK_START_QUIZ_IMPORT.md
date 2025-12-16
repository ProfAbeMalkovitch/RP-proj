# Quick Start: Quiz Content Integration

## For Your Team Member (Quiz Content Provider)

### What You Need to Do

1. **Prepare your quiz content in JSON format** (see `examples/sample_quiz.json`)

2. **Get a teacher account** from the ILPG team to authenticate

3. **Use one of these methods to import:**

### Method 1: Using the Validation Endpoint (Recommended First Step)

Test your quiz format before importing:

```bash
curl -X POST http://localhost:8000/api/quizzes/validate \
  -H "Content-Type: application/json" \
  -d @your_quiz.json
```

### Method 2: Using Python Script

1. Update `examples/import_quizzes.py` with your teacher credentials
2. Place your quiz JSON file in the `examples/` folder
3. Run: `python examples/import_quizzes.py`

### Method 3: Using Postman/API Client

1. Login to get token: `POST /api/auth/teacher/login`
2. Import quiz: `POST /api/quizzes/import` with token in Authorization header

### Method 4: Bulk Import (Multiple Quizzes)

```bash
curl -X POST http://localhost:8000/api/quizzes/import/bulk \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "quizzes": [
      { /* quiz 1 */ },
      { /* quiz 2 */ },
      { /* quiz 3 */ }
    ]
  }'
```

## Required Quiz Format

```json
{
  "quiz_id": "unique_quiz_id",
  "pathway_id": "pathway_basic",  // Must exist in system
  "title": "Quiz Title",
  "description": "Quiz Description",
  "questions": [
    {
      "question_id": "q1",
      "question_text": "Your question here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 1,  // Index: 0=A, 1=B, 2=C, 3=D
      "points": 10
    }
  ]
}
```

## Important Notes

- ✅ `quiz_id` must be unique
- ✅ `pathway_id` must match existing pathway (check with team)
- ✅ `correct_answer` is 0-based index (0 = first option)
- ✅ Minimum 1 question per quiz
- ✅ Minimum 2 options per question (recommended: 4)

## Full Documentation

See `QUIZ_INTEGRATION_GUIDE.md` for complete details.




