# Roadmap Templates Guide

## Quick Start

The roadmap templates are **already created** in your database! You should be able to generate roadmaps now.

If you still get "No matching templates found", try:
1. Taking some quizzes first (to establish student profile and weak areas)
2. Wait a few seconds and try again
3. Check the server logs for any errors

## ✅ Templates Already Created

There are 4 pre-built templates in your database:

1. **Statistics Fundamentals Remediation** - For students struggling with statistics
   - Pathway Level: Intermediate
   - Focus: Weak areas
   - Concepts: statistics, data_analysis, probability

2. **Algebra Fundamentals Remediation** - For students needing algebra help
   - Pathway Level: Intermediate
   - Focus: Weak areas
   - Concepts: algebra, equations, functions

3. **Geometry Concepts Mastery** - For advanced geometry learning
   - Pathway Level: Excellent
   - Focus: Mastery building
   - Concepts: geometry, shapes, angles, measurements

4. **Introduction to Calculus** - For students ready for calculus
   - Pathway Level: Excellent
   - Focus: General learning
   - Concepts: calculus, derivatives, limits

## How Templates Match Students

Templates are matched based on:
- **Weak Areas**: If student has weak areas, templates targeting those concepts are prioritized
- **Pathway Level**: Templates match student's pathway level or slightly above
  - Basic students → Basic or Intermediate templates
  - Intermediate students → Intermediate or Excellent templates
  - Excellent students → Excellent templates
- **If no exact match**: System falls back to any active template

## Re-running Template Initialization

If you need to re-run the template initialization script:

```bash
cd backend
python init_roadmap_templates.py
```

This script is safe to run multiple times - it won't create duplicates.

## Creating Custom Templates (For Teachers)

### Option 1: Using the API

**Endpoint**: `POST /api/roadmap/templates?teacher_id={teacher_id}`

**Example Request**:
```json
{
  "name": "Custom Remediation Roadmap",
  "description": "Personalized roadmap for specific student needs",
  "target_concepts": ["algebra", "equations"],
  "pathway_level": "Intermediate",
  "difficulty": "beginner",
  "weak_area_focus": true,
  "mastery_focus": false,
  "tasks": [
    {
      "task_id": "task_1",
      "title": "Introduction to Topic",
      "description": "Learn the basics",
      "task_type": "reading",
      "order": 1,
      "estimated_time": 60,
      "difficulty": "beginner",
      "learning_objectives": ["Understand basics"],
      "prerequisites": [],
      "tags": ["basics"]
    }
  ],
  "prerequisites": {
    "basic_math": 0.5
  },
  "estimated_total_time": 120,
  "learning_outcomes": ["Strong foundation"],
  "tags": ["remediation", "custom"]
}
```

### Option 2: Direct Database Insert (Advanced)

You can add templates directly to MongoDB using the same structure as in `init_roadmap_templates.py`.

### Option 3: Modify init_roadmap_templates.py

Add your custom template to the `templates` list in `backend/init_roadmap_templates.py` and run it again.

## Template Structure

Each template includes:

- **Basic Info**: `template_id`, `name`, `description`
- **Targeting**: `target_concepts`, `pathway_level`, `difficulty`
- **Focus Flags**: `weak_area_focus`, `mastery_focus`
- **Tasks**: Array of learning tasks with:
  - `task_id`, `title`, `description`
  - `task_type`: "reading", "quiz", "practice", "project"
  - `order`, `estimated_time`, `difficulty`
  - `learning_objectives`, `prerequisites`, `tags`
- **Prerequisites**: Concept mastery thresholds required
- **Metadata**: `estimated_total_time`, `learning_outcomes`, `tags`, `is_active`

## Troubleshooting

### "No matching templates found"

**Causes**:
1. Student has no quiz results yet (no weak areas identified)
2. Pathway level mismatch
3. No active templates in database

**Solutions**:
1. Have student take some quizzes first
2. Check if templates exist: Run `init_roadmap_templates.py`
3. Verify templates are active in database
4. Try generating with `focus_areas` parameter manually

### Templates not appearing for students

- Check that `is_active: true` in database
- Verify student's pathway level matches template criteria
- Check server logs for matching logic errors

## Viewing Templates

**API Endpoint**: `GET /api/roadmap/templates`

With filters:
- `GET /api/roadmap/templates?pathway_level=Intermediate`
- `GET /api/roadmap/templates?weak_area_focus=true`
- `GET /api/roadmap/templates?teacher_id={teacher_id}`

## Next Steps

1. ✅ Templates are already created - you're ready to generate roadmaps!
2. Have students take quizzes to establish their profiles
3. Generate roadmaps - the system will automatically match templates
4. (Optional) Create custom templates for specific needs

For more details, see the API documentation at `http://localhost:8000/docs`











## Quick Start

The roadmap templates are **already created** in your database! You should be able to generate roadmaps now.

If you still get "No matching templates found", try:
1. Taking some quizzes first (to establish student profile and weak areas)
2. Wait a few seconds and try again
3. Check the server logs for any errors

## ✅ Templates Already Created

There are 4 pre-built templates in your database:

1. **Statistics Fundamentals Remediation** - For students struggling with statistics
   - Pathway Level: Intermediate
   - Focus: Weak areas
   - Concepts: statistics, data_analysis, probability

2. **Algebra Fundamentals Remediation** - For students needing algebra help
   - Pathway Level: Intermediate
   - Focus: Weak areas
   - Concepts: algebra, equations, functions

3. **Geometry Concepts Mastery** - For advanced geometry learning
   - Pathway Level: Excellent
   - Focus: Mastery building
   - Concepts: geometry, shapes, angles, measurements

4. **Introduction to Calculus** - For students ready for calculus
   - Pathway Level: Excellent
   - Focus: General learning
   - Concepts: calculus, derivatives, limits

## How Templates Match Students

Templates are matched based on:
- **Weak Areas**: If student has weak areas, templates targeting those concepts are prioritized
- **Pathway Level**: Templates match student's pathway level or slightly above
  - Basic students → Basic or Intermediate templates
  - Intermediate students → Intermediate or Excellent templates
  - Excellent students → Excellent templates
- **If no exact match**: System falls back to any active template

## Re-running Template Initialization

If you need to re-run the template initialization script:

```bash
cd backend
python init_roadmap_templates.py
```

This script is safe to run multiple times - it won't create duplicates.

## Creating Custom Templates (For Teachers)

### Option 1: Using the API

**Endpoint**: `POST /api/roadmap/templates?teacher_id={teacher_id}`

**Example Request**:
```json
{
  "name": "Custom Remediation Roadmap",
  "description": "Personalized roadmap for specific student needs",
  "target_concepts": ["algebra", "equations"],
  "pathway_level": "Intermediate",
  "difficulty": "beginner",
  "weak_area_focus": true,
  "mastery_focus": false,
  "tasks": [
    {
      "task_id": "task_1",
      "title": "Introduction to Topic",
      "description": "Learn the basics",
      "task_type": "reading",
      "order": 1,
      "estimated_time": 60,
      "difficulty": "beginner",
      "learning_objectives": ["Understand basics"],
      "prerequisites": [],
      "tags": ["basics"]
    }
  ],
  "prerequisites": {
    "basic_math": 0.5
  },
  "estimated_total_time": 120,
  "learning_outcomes": ["Strong foundation"],
  "tags": ["remediation", "custom"]
}
```

### Option 2: Direct Database Insert (Advanced)

You can add templates directly to MongoDB using the same structure as in `init_roadmap_templates.py`.

### Option 3: Modify init_roadmap_templates.py

Add your custom template to the `templates` list in `backend/init_roadmap_templates.py` and run it again.

## Template Structure

Each template includes:

- **Basic Info**: `template_id`, `name`, `description`
- **Targeting**: `target_concepts`, `pathway_level`, `difficulty`
- **Focus Flags**: `weak_area_focus`, `mastery_focus`
- **Tasks**: Array of learning tasks with:
  - `task_id`, `title`, `description`
  - `task_type`: "reading", "quiz", "practice", "project"
  - `order`, `estimated_time`, `difficulty`
  - `learning_objectives`, `prerequisites`, `tags`
- **Prerequisites**: Concept mastery thresholds required
- **Metadata**: `estimated_total_time`, `learning_outcomes`, `tags`, `is_active`

## Troubleshooting

### "No matching templates found"

**Causes**:
1. Student has no quiz results yet (no weak areas identified)
2. Pathway level mismatch
3. No active templates in database

**Solutions**:
1. Have student take some quizzes first
2. Check if templates exist: Run `init_roadmap_templates.py`
3. Verify templates are active in database
4. Try generating with `focus_areas` parameter manually

### Templates not appearing for students

- Check that `is_active: true` in database
- Verify student's pathway level matches template criteria
- Check server logs for matching logic errors

## Viewing Templates

**API Endpoint**: `GET /api/roadmap/templates`

With filters:
- `GET /api/roadmap/templates?pathway_level=Intermediate`
- `GET /api/roadmap/templates?weak_area_focus=true`
- `GET /api/roadmap/templates?teacher_id={teacher_id}`

## Next Steps

1. ✅ Templates are already created - you're ready to generate roadmaps!
2. Have students take quizzes to establish their profiles
3. Generate roadmaps - the system will automatically match templates
4. (Optional) Create custom templates for specific needs

For more details, see the API documentation at `http://localhost:8000/docs`































