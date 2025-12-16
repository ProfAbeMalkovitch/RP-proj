# Quiz Content Integration Guide

This guide explains how to integrate quiz content from external sources into the ILPG (Intelligent Learning Path Generator) system.

## Overview

The ILPG system supports importing quiz content through REST API endpoints. You can import:
- Single quizzes
- Multiple quizzes in bulk
- Validate quiz format before importing

## API Endpoints

### Base URL
```
http://localhost:8000/api/quizzes
```

### 1. Import Single Quiz
**POST** `/api/quizzes/import`

**Authentication:** Required (Teacher token)

**Request Body:**
```json
{
  "quiz_id": "quiz_custom_1",
  "pathway_id": "pathway_basic",
  "title": "Custom Quiz Title",
  "description": "Quiz description here",
  "total_points": 50,
  "questions": [
    {
      "question_id": "q1",
      "question_text": "What is the question?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": 1,
      "points": 10
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Quiz 'quiz_custom_1' imported successfully",
  "quiz_id": "quiz_custom_1",
  "total_points": 50,
  "questions_count": 1
}
```

### 2. Import Multiple Quizzes (Bulk)
**POST** `/api/quizzes/import/bulk`

**Authentication:** Required (Teacher token)

**Request Body:**
```json
{
  "quizzes": [
    {
      "quiz_id": "quiz_custom_1",
      "pathway_id": "pathway_basic",
      "title": "Quiz 1",
      "description": "Description 1",
      "questions": [...]
    },
    {
      "quiz_id": "quiz_custom_2",
      "pathway_id": "pathway_intermediate",
      "title": "Quiz 2",
      "description": "Description 2",
      "questions": [...]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "imported_count": 2,
  "failed_count": 0,
  "imported": [
    {
      "quiz_id": "quiz_custom_1",
      "title": "Quiz 1",
      "questions_count": 5,
      "total_points": 50
    }
  ],
  "failed": []
}
```

### 3. Validate Quiz Format
**POST** `/api/quizzes/validate`

**Authentication:** Not required (validation only)

**Request Body:** Same as import single quiz

**Response:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "calculated_total_points": 50,
  "questions_count": 5
}
```

## Data Structure

### Quiz Object
```typescript
{
  quiz_id: string;           // Unique identifier (e.g., "quiz_custom_1")
  pathway_id: string;         // Must match existing pathway (e.g., "pathway_basic")
  title: string;              // Quiz title
  description: string;        // Quiz description
  total_points?: number;      // Optional - auto-calculated if not provided
  questions: Question[];      // Array of questions
}
```

### Question Object
```typescript
{
  question_id: string;         // Unique within quiz (e.g., "q1", "q2")
  question_text: string;      // The question text
  options: string[];          // Array of answer options (minimum 2, recommended 4)
  correct_answer: number;     // Index of correct option (0-based: 0, 1, 2, 3...)
  points: number;             // Points for this question (default: 10)
}
```

## Available Pathways

Before importing quizzes, ensure the pathway exists. Available pathways:
- `pathway_basic` - Basic level pathway
- `pathway_intermediate` - Intermediate level pathway
- `pathway_advanced` - Advanced level pathway
- `pathway_excellent` - Excellent level pathway

To check available pathways, use:
**GET** `/api/pathways`

## Authentication

To import quizzes, you need a teacher authentication token.

### Getting a Token

1. **Login as Teacher:**
   ```
   POST /api/auth/teacher/login
   {
     "email": "teacher@example.com",
     "password": "password123"
   }
   ```

2. **Use Token in Headers:**
   ```
   Authorization: Bearer <your_token_here>
   ```

## Example: Complete Quiz Import

### Step 1: Validate Quiz Format
```bash
curl -X POST http://localhost:8000/api/quizzes/validate \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_id": "quiz_math_1",
    "pathway_id": "pathway_basic",
    "title": "Mathematics Basics Quiz",
    "description": "Test your basic math skills",
    "questions": [
      {
        "question_id": "q1",
        "question_text": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": 1,
        "points": 10
      },
      {
        "question_id": "q2",
        "question_text": "What is 5 × 3?",
        "options": ["12", "15", "18", "20"],
        "correct_answer": 1,
        "points": 10
      }
    ]
  }'
```

### Step 2: Import Quiz
```bash
curl -X POST http://localhost:8000/api/quizzes/import \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <teacher_token>" \
  -d '{
    "quiz_id": "quiz_math_1",
    "pathway_id": "pathway_basic",
    "title": "Mathematics Basics Quiz",
    "description": "Test your basic math skills",
    "questions": [
      {
        "question_id": "q1",
        "question_text": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": 1,
        "points": 10
      },
      {
        "question_id": "q2",
        "question_text": "What is 5 × 3?",
        "options": ["12", "15", "18", "20"],
        "correct_answer": 1,
        "points": 10
      }
    ]
  }'
```

## Sample Quiz JSON File

Save this as `sample_quiz.json`:

```json
{
  "quiz_id": "quiz_sample_1",
  "pathway_id": "pathway_basic",
  "title": "Sample Quiz",
  "description": "This is a sample quiz for testing",
  "questions": [
    {
      "question_id": "q1",
      "question_text": "What is the capital of France?",
      "options": [
        "London",
        "Berlin",
        "Paris",
        "Madrid"
      ],
      "correct_answer": 2,
      "points": 10
    },
    {
      "question_id": "q2",
      "question_text": "Which planet is closest to the Sun?",
      "options": [
        "Venus",
        "Earth",
        "Mercury",
        "Mars"
      ],
      "correct_answer": 2,
      "points": 10
    },
    {
      "question_id": "q3",
      "question_text": "What is 10 × 5?",
      "options": [
        "40",
        "50",
        "60",
        "70"
      ],
      "correct_answer": 1,
      "points": 10
    }
  ]
}
```

## Important Notes

1. **Quiz ID Must Be Unique:** Each quiz must have a unique `quiz_id`. If you try to import a quiz with an existing ID, you'll get a 409 Conflict error.

2. **Pathway Must Exist:** The `pathway_id` must match an existing pathway. Check available pathways first.

3. **Question IDs:** `question_id` should be unique within a quiz (e.g., "q1", "q2", "q3").

4. **Correct Answer Index:** `correct_answer` is 0-based:
   - 0 = First option
   - 1 = Second option
   - 2 = Third option
   - etc.

5. **Total Points:** If `total_points` is not provided, it will be automatically calculated as the sum of all question points.

6. **Minimum Requirements:**
   - At least 1 question per quiz
   - At least 2 options per question (recommended: 4)
   - Valid `correct_answer` index (0 to options.length - 1)

## Error Handling

### Common Errors

**400 Bad Request:**
- Missing required fields
- Invalid question format
- Invalid correct_answer index

**401 Unauthorized:**
- Missing or invalid authentication token

**404 Not Found:**
- Pathway doesn't exist

**409 Conflict:**
- Quiz ID already exists

**503 Service Unavailable:**
- Database connection issue

## Integration Tips

1. **Always Validate First:** Use the `/validate` endpoint before importing to catch errors early.

2. **Bulk Import:** For multiple quizzes, use the bulk import endpoint to save time.

3. **Error Handling:** Check the `failed` array in bulk import responses to see which quizzes couldn't be imported.

4. **Pathway Planning:** Coordinate with the team to ensure pathways are created before importing quizzes.

5. **Naming Convention:** Use a consistent naming convention for quiz IDs (e.g., `quiz_subject_level_number`).

## Testing

You can test the integration using:
- **Postman:** Import the endpoints and test with sample data
- **curl:** Use command-line examples above
- **Python Script:** See `examples/import_quizzes.py` for a Python example
- **JavaScript/Node.js:** Use fetch or axios to call the API

## Support

For issues or questions:
1. Check the validation endpoint first
2. Review error messages carefully
3. Ensure all pathways exist
4. Verify authentication token is valid

## Next Steps

After importing quizzes:
1. Quizzes will automatically appear in the student dashboard
2. Students can take quizzes assigned to their pathway
3. Results will be tracked and used for adaptive learning
4. Teachers can assign quizzes as tasks




