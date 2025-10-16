# Student Submission API - Complete Backend Setup

## ✅ What Was Created

### 1. Database Table: `student_submissions`
- Stores student work submissions
- Links to activities and students
- Tracks scores, feedback, and status (unscored/scored)

### 2. Django Model: `StudentSubmission`
- Located in: `be/api/models.py`
- Fields:
  - `activity` - Foreign key to PortfolioActivity
  - `student` - Foreign key to User
  - `caption` - Text description of the work
  - `file_path` - Path to uploaded file
  - `file_type` - Type of file (image, pdf, etc.)
  - `score` - Integer score (nullable)
  - `feedback` - Teacher feedback text
  - `status` - 'unscored' or 'scored'
  - `submitted_at` - Timestamp
  - `scored_at` - Timestamp when scored

### 3. Serializer: `StudentSubmissionSerializer`
- Located in: `be/api/serializer.py`
- Includes student info and activity details

### 4. API Endpoints

#### For Students:
- **POST** `/api/activities/{activity_id}/submissions/`
  - Submit work for an activity
  - Body: `{ caption, file_path, file_type }`
  - Returns: Created submission

- **GET** `/api/activities/{activity_id}/submissions/`
  - View own submission for an activity
  - Returns: Student's submission(s)

#### For Teachers:
- **GET** `/api/activities/{activity_id}/submissions/`
  - View all submissions for an activity
  - Returns: All student submissions

- **GET** `/api/submissions/unscored/`
  - View all unscored submissions
  - Returns: All unscored submissions (for Outputs.vue)

- **PUT** `/api/submissions/{submission_id}/score/`
  - Score a submission
  - Body: `{ score, feedback }`
  - Returns: Updated submission

## 🚀 How to Use

### Step 1: Run SQL in pgAdmin
```sql
-- Execute create_submissions_table.sql
CREATE TABLE IF NOT EXISTS student_submissions (
    id SERIAL PRIMARY KEY,
    activity_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    caption TEXT,
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    score INTEGER,
    feedback TEXT,
    status VARCHAR(50) DEFAULT 'unscored',
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    scored_at TIMESTAMP,
    FOREIGN KEY (activity_id) REFERENCES portfolio_activities (id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
);
```

### Step 2: Restart Django Server
The models, serializers, views, and URLs are already updated.
Just restart the server to apply changes.

### Step 3: Frontend Integration

#### Student Submission (Sroom.vue):
```javascript
// Submit work
const submitWork = async (activityId, caption, filePath, fileType) => {
  try {
    const response = await axios.post(`/api/activities/${activityId}/submissions/`, {
      caption: caption,
      file_path: filePath,
      file_type: fileType
    });
    console.log('Submitted:', response.data);
    alert('Work submitted successfully!');
  } catch (error) {
    console.error('Error submitting:', error);
    alert('Failed to submit work');
  }
};
```

#### Teacher View Unscored (Outputs.vue):
```javascript
// Load unscored submissions
const loadUnscoredSubmissions = async () => {
  try {
    const response = await axios.get('/api/submissions/unscored/');
    unscoredSubmissions.value = response.data;
  } catch (error) {
    console.error('Error loading submissions:', error);
  }
};

// Score a submission
const scoreSubmission = async (submissionId, score, feedback) => {
  try {
    const response = await axios.put(`/api/submissions/${submissionId}/score/`, {
      score: score,
      feedback: feedback
    });
    console.log('Scored:', response.data);
    // Reload submissions
    await loadUnscoredSubmissions();
  } catch (error) {
    console.error('Error scoring:', error);
  }
};
```

## 📊 Database Schema

```
student_submissions
├── id (PK)
├── activity_id (FK → portfolio_activities)
├── student_id (FK → users)
├── caption
├── file_path
├── file_type
├── score
├── feedback
├── status ('unscored' | 'scored')
├── submitted_at
└── scored_at
```

## 🔐 Permissions

- **Students**: Can submit and view their own submissions
- **Teachers**: Can view all submissions, score them, and see unscored list

## ✨ Features

1. ✅ Students can submit work with caption and file
2. ✅ Students can update their submission (resubmit)
3. ✅ Teachers see all submissions for an activity
4. ✅ Teachers see unscored submissions in Outputs.vue
5. ✅ Teachers can score submissions with feedback
6. ✅ Automatic timestamp tracking
7. ✅ One submission per student per activity (unique constraint)
