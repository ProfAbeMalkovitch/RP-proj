# ILPG API Examples

## Request/Response Examples

### 1. Evaluate Student Pathway

**Endpoint:** `POST /ilpg/evaluate`

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439011",
  "trigger": "quiz_completion"
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "pathway": {
      "id": "65a1b2c3d4e5f6789abcdef0",
      "student_id": "507f1f77bcf86cd799439011",
      "pathway_type": "balanced",
      "average_score": 65.5,
      "task_completion_rate": 0.75,
      "recommended_tags": [
        "standard",
        "core-content",
        "interactive",
        "examples",
        "guided-practice"
      ],
      "performance_metrics": {
        "total_quizzes": 8,
        "total_tasks": 12,
        "completed_tasks": 9,
        "recent_attempts": 3,
        "recent_scores": [68, 72, 65],
        "last_quiz_date": "2024-01-15T10:30:00Z"
      },
      "calculated_at": "2024-01-15T10:30:00Z",
      "trigger": "quiz_completion",
      "previous_pathway": "basic",
      "pathway_changes_count": 1,
      "is_active": true
    },
    "recommendations": [
      {
        "type": "content",
        "priority": "medium",
        "title": "Continue Standard Progression",
        "description": "Follow standard curriculum with interactive content",
        "tags": ["standard", "core-content", "interactive"]
      }
    ],
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Response (Error - Missing student_id):**
```json
{
  "error": "student_id is required",
  "message": "Please provide a valid student ID"
}
```

---

### 2. Get Current Pathway

**Endpoint:** `GET /ilpg/:studentId`

**Request:**
```
GET /ilpg/507f1f77bcf86cd799439011
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "pathway": {
      "id": "65a1b2c3d4e5f6789abcdef0",
      "student_id": "507f1f77bcf86cd799439011",
      "pathway_type": "balanced",
      "average_score": 65.5,
      "task_completion_rate": 0.75,
      "recommended_tags": ["standard", "core-content", "interactive"],
      "performance_metrics": {
        "total_quizzes": 8,
        "total_tasks": 12,
        "completed_tasks": 9,
        "recent_attempts": 3,
        "recent_scores": [68, 72, 65],
        "last_quiz_date": "2024-01-15T10:30:00Z"
      },
      "calculated_at": "2024-01-15T10:30:00Z",
      "trigger": "quiz_completion",
      "previous_pathway": "basic",
      "pathway_changes_count": 1,
      "is_active": true
    }
  }
}
```

**Response (Not Found):**
```json
{
  "error": "Pathway not found",
  "message": "No active pathway found for this student. Generate one first."
}
```

---

### 3. Recalculate Pathway

**Endpoint:** `POST /ilpg/recalculate`

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439011"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pathway": { ... },
    "recommendations": [ ... ],
    "generated_at": "2024-01-15T10:30:00Z"
  },
  "message": "Pathway recalculated successfully"
}
```

---

### 4. Get Pathway History

**Endpoint:** `GET /ilpg/:studentId/history`

**Request:**
```
GET /ilpg/507f1f77bcf86cd799439011/history?limit=5
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pathways": [
      {
        "id": "65a1b2c3d4e5f6789abcdef0",
        "student_id": "507f1f77bcf86cd799439011",
        "pathway_type": "balanced",
        "average_score": 65.5,
        "calculated_at": "2024-01-15T10:30:00Z",
        "is_active": true
      },
      {
        "id": "65a1b2c3d4e5f6789abcdef1",
        "student_id": "507f1f77bcf86cd799439011",
        "pathway_type": "basic",
        "average_score": 45.2,
        "calculated_at": "2024-01-10T08:15:00Z",
        "is_active": false
      }
    ],
    "count": 2
  }
}
```

---

## Pathway Type Examples

### BASIC Pathway (Score < 50)

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439011"
}
```

**Response:**
```json
{
  "pathway": {
    "pathway_type": "basic",
    "average_score": 42.5,
    "recommended_tags": [
      "foundational",
      "basic-concepts",
      "step-by-step",
      "remedial",
      "practice-exercises",
      "review"
    ]
  },
  "recommendations": [
    {
      "type": "content",
      "priority": "high",
      "title": "Focus on Foundational Concepts",
      "description": "Review core concepts and basic principles",
      "tags": ["foundational", "basic-concepts", "review"]
    }
  ]
}
```

### ACCELERATION Pathway (Score ≥ 75)

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439012"
}
```

**Response:**
```json
{
  "pathway": {
    "pathway_type": "acceleration",
    "average_score": 87.3,
    "recommended_tags": [
      "advanced",
      "extension",
      "challenge",
      "deep-dive",
      "critical-thinking",
      "application"
    ]
  },
  "recommendations": [
    {
      "type": "content",
      "priority": "high",
      "title": "Engage with Advanced Content",
      "description": "Explore advanced topics and critical thinking exercises",
      "tags": ["advanced", "extension", "critical-thinking"]
    },
    {
      "type": "assessment",
      "priority": "medium",
      "title": "Challenge Assessments",
      "description": "Take on more complex assessments",
      "tags": ["challenge", "deep-dive"]
    }
  ]
}
```

---

## cURL Examples

### Evaluate Pathway
```bash
curl -X POST http://localhost:5002/ilpg/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "507f1f77bcf86cd799439011",
    "trigger": "quiz_completion"
  }'
```

### Get Current Pathway
```bash
curl http://localhost:5002/ilpg/507f1f77bcf86cd799439011
```

### Recalculate Pathway
```bash
curl -X POST http://localhost:5002/ilpg/recalculate \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "507f1f77bcf86cd799439011"
  }'
```

### Get Pathway History
```bash
curl "http://localhost:5002/ilpg/507f1f77bcf86cd799439011/history?limit=10"
```

### Health Check
```bash
curl http://localhost:5002/health
```

---

## Integration Examples

### From Python/Flask Backend

```python
import requests

def evaluate_student_pathway(student_id, trigger='quiz_completion'):
    """Call ILPG service to evaluate student pathway"""
    try:
        response = requests.post(
            'http://localhost:5002/ilpg/evaluate',
            json={
                'student_id': student_id,
                'trigger': trigger
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling ILPG: {e}")
        return None

# Usage
result = evaluate_student_pathway('507f1f77bcf86cd799439011', 'quiz_completion')
if result and result.get('success'):
    pathway = result['data']['pathway']
    print(f"Pathway: {pathway['pathway_type']}")
    print(f"Recommended tags: {pathway['recommended_tags']}")
```

### From React Frontend

```javascript
import ilpgService from './services/ilpgService';

// After quiz completion
const handleQuizComplete = async (studentId, quizScore) => {
  try {
    const result = await ilpgService.evaluatePathway(
      studentId,
      'quiz_completion'
    );
    
    if (result.success) {
      const { pathway, recommendations } = result.data;
      console.log(`New pathway: ${pathway.pathway_type}`);
      console.log(`Tags: ${pathway.recommended_tags.join(', ')}`);
      
      // Update UI with recommendations
      displayRecommendations(recommendations);
    }
  } catch (error) {
    console.error('Error evaluating pathway:', error);
  }
};

// Get current pathway
const loadCurrentPathway = async (studentId) => {
  try {
    const result = await ilpgService.getCurrentPathway(studentId);
    if (result.success) {
      return result.data.pathway;
    }
  } catch (error) {
    console.error('Error loading pathway:', error);
  }
  return null;
};
```










