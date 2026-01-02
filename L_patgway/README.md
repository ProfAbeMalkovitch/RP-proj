# Intelligent Learning Pathway Generator (ILPG)

## Overview

The **Intelligent Learning Pathway Generator (ILPG)** is a rule-based system for generating personalized learning pathways for students. It categorizes students into three distinct pathways based on their quiz performance and task completion rates, then provides structured content recommendations.

## Research Alignment

This module aligns with the research project:
- **Rule-based approach** (NO AI/ML dependencies)
- **Transparent logic** for academic presentation
- **Teacher-controlled content** recommendations
- **Real-time adaptation** after assessments
- **Three pathway types**: BASIC, BALANCED, ACCELERATION

## Architecture

```
ilpg/
├── config/
│   ├── constants.js      # Rule thresholds and configuration
│   └── database.js       # MongoDB connection
├── models/
│   └── LearningPath.js   # Pathway data model
├── services/
│   ├── DataFetcher.js    # Fetches quiz/task data from MongoDB
│   ├── RuleEngine.js     # Core rule-based pathway logic
│   └── PathwayService.js # High-level pathway management
├── controllers/
│   └── PathwayController.js # HTTP request handlers
├── routes/
│   └── pathwayRoutes.js  # API route definitions
├── server.js             # Express server entry point
└── package.json          # Dependencies
```

## Rule Logic

### Primary Rule: Average Quiz Score

```
IF averageScore < 50:
  → BASIC pathway
  → Focus: Foundational support, core concepts

IF 50 ≤ averageScore < 75:
  → BALANCED pathway
  → Focus: Standard progression, mixed content

IF averageScore ≥ 75:
  → ACCELERATION pathway
  → Focus: Advanced content, challenges
```

### Secondary Rule: Task Completion Rate

- Low completion rate (< 50%) may adjust pathway downward
- High completion with high scores confirms pathway assignment

### Edge Cases

- **No quiz data**: Defaults to BALANCED pathway
- **Incomplete data**: Uses available metrics
- **Rapid changes**: Validates pathway transitions to prevent oscillation

## API Endpoints

### POST /ilpg/evaluate

Evaluate student and generate/update pathway.

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439011",
  "trigger": "quiz_completion"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "pathway": {
      "id": "...",
      "student_id": "...",
      "pathway_type": "balanced",
      "average_score": 65.5,
      "task_completion_rate": 0.75,
      "recommended_tags": ["standard", "core-content", "interactive"],
      "performance_metrics": { ... },
      "calculated_at": "2024-01-15T10:30:00Z"
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

### GET /ilpg/:studentId

Get current active pathway for a student.

**Response:**
```json
{
  "success": true,
  "data": {
    "pathway": { ... }
  }
}
```

### POST /ilpg/recalculate

Force recalculation of pathway.

**Request:**
```json
{
  "student_id": "507f1f77bcf86cd799439011"
}
```

### GET /ilpg/:studentId/history

Get pathway history for a student.

**Query Parameters:**
- `limit`: Number of pathways to return (default: 10)

## Integration

### With Existing Python Backend

The ILPG service runs as a separate Node.js microservice on port **5002**. It connects to the same MongoDB instance as the Python backend.

**From Python/Flask:**
```python
import requests

response = requests.post(
    'http://localhost:5002/ilpg/evaluate',
    json={'student_id': student_id, 'trigger': 'quiz_completion'}
)
```

### With Frontend

The frontend can call ILPG endpoints directly or through a service layer.

**Example:**
```javascript
// frontend/src/services/ilpgService.js
import axios from 'axios';

const ILPG_API_URL = 'http://localhost:5002';

export const evaluatePathway = async (studentId, trigger) => {
  const response = await axios.post(`${ILPG_API_URL}/ilpg/evaluate`, {
    student_id: studentId,
    trigger
  });
  return response.data;
};
```

## Data Integration

ILPG reads from existing MongoDB collections:

- **`learning_activities`**: Quiz scores and activity data (from PMSAS)
- **`engagement_logs`**: Task completion and engagement data

**Important**: ILPG does NOT modify existing data. It only reads and creates its own `learning_paths` collection.

## Setup

### Prerequisites

- Node.js 16+ 
- MongoDB connection (shared with Python backend)

### Installation

```bash
cd backend/ilpg
npm install
```

### Configuration

Copy `.env.example` to `.env` and configure:

```env
MONGODB_URI=your_mongodb_connection_string
ILPG_PORT=5002
```

### Running

**Development:**
```bash
npm run dev
```

**Production:**
```bash
npm start
```

Server will start on `http://localhost:5002`

## Testing

### Health Check

```bash
curl http://localhost:5002/health
```

### Evaluate Pathway

```bash
curl -X POST http://localhost:5002/ilpg/evaluate \
  -H "Content-Type: application/json" \
  -d '{"student_id": "YOUR_STUDENT_ID", "trigger": "quiz_completion"}'
```

### Get Current Pathway

```bash
curl http://localhost:5002/ilpg/YOUR_STUDENT_ID
```

## Pathway Types

### BASIC (0-49)

- **Focus**: Foundational support
- **Content Tags**: `foundational`, `basic-concepts`, `step-by-step`, `remedial`, `practice-exercises`, `review`
- **Recommendations**: Core concept review, guided practice

### BALANCED (50-74)

- **Focus**: Standard progression
- **Content Tags**: `standard`, `core-content`, `interactive`, `examples`, `guided-practice`
- **Recommendations**: Standard curriculum, interactive content

### ACCELERATION (75-100)

- **Focus**: Advanced content
- **Content Tags**: `advanced`, `extension`, `challenge`, `deep-dive`, `critical-thinking`, `application`
- **Recommendations**: Advanced topics, challenge assessments

## Research Notes

### Transparency

All rule logic is documented in code comments. No black-box algorithms. Every pathway decision can be traced to specific rules and thresholds.

### Teacher Control

Content recommendations use tags that align with teacher-uploaded content (via ECESE module). Teachers control what content is available, ILPG only recommends which tags to prioritize.

### Real-time Adaptation

Pathways are recalculated:
- After each quiz completion
- After task milestones
- On manual trigger
- On scheduled review

### Academic Presentation

Code is structured for academic review:
- Clear documentation
- Transparent rules
- No shortcuts or hacks
- Modular architecture

## Future Enhancements

Potential extensions (not implemented):
- Pathway transition analytics
- Comparative pathway effectiveness studies
- Integration with more data sources
- Pathway recommendation explanations

## License

Part of the ILPG research project.










