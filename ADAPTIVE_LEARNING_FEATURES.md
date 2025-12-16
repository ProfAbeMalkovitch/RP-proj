# Adaptive Learning Features - Your Part of the Project

This document explains your part of the ILPG project: **Student Categorization and Personalized Learning Guides**.

## Overview

Your responsibility is to implement and maintain the adaptive learning system that:
1. **Categorizes students** into three levels based on quiz performance
2. **Generates personalized roadmaps** based on student performance
3. **Identifies weak areas** through mind maps
4. **Provides personalized recommendations** based on performance

## 1. Student Categorization System

### How It Works

Students are automatically categorized into three pathways based on their **average quiz score**:

- **Basic**: 0-49% average score
- **Intermediate**: 50-74% average score  
- **Accelerated**: 75-100% average score

### Implementation

**File**: `backend/utils/pathway_calculator.py`

```python
def calculate_pathway(quiz_scores: list) -> str:
    """
    Calculate pathway based on average quiz score
    - Basic: 0-49
    - Intermediate: 50-74
    - Accelerated: 75-100
    """
    if not quiz_scores or len(quiz_scores) == 0:
        return "Basic"
    
    average_score = sum(quiz_scores) / len(quiz_scores)
    
    if average_score < 50:
        return "Basic"
    elif average_score < 75:
        return "Intermediate"
    else:
        return "Accelerated"
```

### Automatic Updates

When a student submits a quiz:
1. Quiz score (percentage) is added to `quiz_scores` array
2. Average score is recalculated
3. Pathway is automatically updated based on new average
4. Student record is updated in database

**File**: `backend/routes/results.py` - `submit_quiz()` function

## 2. Personalized Roadmaps

### How It Works

Roadmaps are generated based on:
- Student's current pathway level
- Concept mastery scores
- Weak areas identified
- Learning progress

### Implementation

**File**: `backend/services/roadmap_generation_service.py`

The system:
1. Analyzes student's mastery data
2. Identifies weak areas (concepts below 60% mastery)
3. Matches roadmap templates to student needs
4. Generates personalized learning path with tasks

### Key Features

- **Weak Area Focus**: Prioritizes concepts where student struggles
- **Pathway Matching**: Ensures roadmap matches student's level
- **Progressive Learning**: Builds from basics to advanced
- **Adaptive**: Updates as student performance changes

## 3. Mind Map - Weak Area Identification

### How It Works

The mind map visualizes:
- **Topic mastery levels** (color-coded)
- **Weak areas** (red/orange - low mastery)
- **Strong areas** (green - high mastery)
- **Recommended topics** (highlighted)

### Implementation

**File**: `frontend/src/components/MindMap.js`

**Backend**: `backend/services/adaptive_learning_service.py`

The system:
1. Calculates mastery for each concept/topic
2. Identifies weak areas (mastery < 60%)
3. Maps concepts to visual nodes
4. Color-codes based on performance

### Weak Area Detection

**File**: `backend/services/adaptive_learning_service.py` - `identify_weak_areas()`

```python
def identify_weak_areas(student_id: str, threshold: float = 0.6):
    """
    Identify concepts where student mastery is below threshold
    Returns sorted list (largest gap first)
    """
```

## 4. Personalized Recommendations

### How It Works

Recommendations are generated based on:
- Weak areas (priority: high)
- Current pathway level
- Learning progress
- Concept mastery trends

### Implementation

**File**: `backend/services/adaptive_learning_service.py` - `generate_recommendations()`

### Recommendation Types

1. **Practice Weak Areas** (High Priority)
   - Focuses on concepts with low mastery
   - Suggests relevant quizzes/content

2. **Pathway Advancement** (Medium Priority)
   - Suggests next-level content when ready
   - Based on overall mastery improvement

3. **Strengthen Foundations** (Medium Priority)
   - For students struggling with basics
   - Suggests foundational content

4. **Advanced Topics** (Low Priority)
   - For accelerated students
   - Suggests challenging content

## Data Flow

### When Student Submits Quiz:

```
1. Quiz Submitted
   ↓
2. Score Calculated
   ↓
3. Update quiz_scores array
   ↓
4. Calculate average_score
   ↓
5. Categorize into pathway (Basic/Intermediate/Accelerated)
   ↓
6. Update concept mastery
   ↓
7. Identify weak areas
   ↓
8. Generate recommendations
   ↓
9. Update student record
```

## Key Components

### Backend Services

1. **Pathway Calculator** (`backend/utils/pathway_calculator.py`)
   - Calculates pathway from quiz scores
   - Calculates average scores

2. **Adaptive Learning Service** (`backend/services/adaptive_learning_service.py`)
   - Concept mastery calculation
   - Weak area identification
   - Recommendation generation
   - Pathway adjustment (advanced)

3. **Roadmap Generation Service** (`backend/services/roadmap_generation_service.py`)
   - Student profile analysis
   - Template matching
   - Personalized roadmap creation

### Frontend Components

1. **Student Dashboard** (`frontend/src/components/dashboards/StudentDashboard.js`)
   - Displays pathway badge
   - Shows concept mastery card
   - Shows recommendations card
   - Displays mind map
   - Shows personalized roadmap

2. **Mind Map** (`frontend/src/components/MindMap.js`)
   - Visual representation of topics
   - Color-coded mastery levels
   - Weak area highlighting

3. **Concept Mastery Card** (`frontend/src/components/shared/ConceptMasteryCard.js`)
   - Displays mastery scores
   - Shows progress trends

4. **Recommendations Card** (`frontend/src/components/shared/RecommendationsCard.js`)
   - Lists personalized recommendations
   - Priority-based ordering

## API Endpoints

### Get Student Mastery
```
GET /api/adaptive/mastery/{student_id}
```
Returns concept mastery scores and weak areas.

### Get Recommendations
```
GET /api/adaptive/recommendations/{student_id}
```
Returns personalized recommendations.

### Generate Roadmap
```
POST /api/roadmap/generate
{
  "student_id": "...",
  "focus_areas": ["concept1", "concept2"]
}
```
Generates personalized roadmap.

## Testing Your Features

### Test Student Categorization

1. Create a test student
2. Submit quizzes with different scores:
   - Scores 0-49% → Should be "Basic"
   - Scores 50-74% → Should be "Intermediate"
   - Scores 75-100% → Should be "Accelerated"
3. Verify pathway updates automatically

### Test Mind Map

1. Submit quizzes covering different concepts
2. Check mind map visualization
3. Verify weak areas are highlighted (red/orange)
4. Verify strong areas are green

### Test Recommendations

1. Submit quizzes with low scores on specific concepts
2. Check recommendations card
3. Verify weak areas appear in recommendations
4. Verify priority ordering (weak areas first)

### Test Roadmap Generation

1. Generate roadmap for a student
2. Verify it focuses on weak areas
3. Verify it matches student's pathway level
4. Verify tasks are personalized

## Integration with Quiz Content

Your adaptive learning system works with quiz content provided by your team member:

1. **Quiz Submission** → Your system categorizes student
2. **Quiz Results** → Your system identifies weak areas
3. **Quiz Performance** → Your system generates recommendations
4. **Quiz Concepts** → Your system maps to mind map topics

## Important Notes

- **Pathway is automatically updated** after each quiz submission
- **Weak areas are recalculated** after each quiz
- **Recommendations are regenerated** based on latest performance
- **Roadmaps can be regenerated** as student improves

## Future Enhancements

Potential improvements you could add:

1. **Predictive Analytics**: Predict student success
2. **Learning Velocity**: Track improvement rate
3. **Concept Dependencies**: Map prerequisite relationships
4. **Adaptive Difficulty**: Adjust quiz difficulty based on performance
5. **Peer Comparison**: Compare with similar students

## Support

If you need to debug or modify the adaptive learning system:

1. Check `backend/services/adaptive_learning_service.py` for core logic
2. Check `backend/utils/pathway_calculator.py` for categorization
3. Check `backend/services/roadmap_generation_service.py` for roadmap logic
4. Check database collections:
   - `concept_mastery` - Mastery scores
   - `recommendations` - Generated recommendations
   - `generated_roadmaps` - Student roadmaps




