# ✅ Post to Feed Feature - Complete Implementation

## Overview
When students submit work and check "Post this output to feeds (visible to class)", their submission appears in the teacher's Notice.vue page as a pending approval.

## What Was Done

### Backend Changes

#### 1. Database Updates
**File:** `be/add_post_to_feed_column.sql`
```sql
ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS post_to_feed BOOLEAN DEFAULT FALSE;

ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50) DEFAULT 'pending';
```

#### 2. Django Model
**File:** `be/api/models.py`
- Added `post_to_feed` field (Boolean)
- Added `approval_status` field with choices: 'pending', 'approved', 'rejected'

#### 3. API Endpoints
**File:** `be/api/views.py`

**New Endpoints:**
- `GET /api/submissions/pending-approvals/` - Get all pending feed approvals
- `PUT /api/submissions/{id}/approve/` - Approve or reject a submission

**Updated Endpoint:**
- `POST /api/activities/{id}/submissions/` - Now accepts `post_to_feed` parameter

#### 4. URL Routes
**File:** `be/api/urls.py`
- Added routes for pending approvals and approval actions

### Frontend Changes

#### 1. Student Side (Sroom.vue)
**File:** `resources/js/Pages/Student/Sroom.vue`
- Updated `submitNewProduct()` to send `post_to_feed` parameter
- When checkbox is checked, submission is marked for feed posting

#### 2. Teacher Side (Notice.vue)
**File:** `resources/js/Pages/Teacher/Notice.vue`
- Loads pending approvals from API on mount
- Displays student submissions awaiting approval
- Approve/Reject buttons call API to update approval status
- Removes approved/rejected items from pending list

## Data Flow

```
Student Submits Work
    ↓
Checks "Post this output to feeds"
    ↓
POST /api/activities/{id}/submissions/
    { post_to_feed: true }
    ↓
Database: post_to_feed=true, approval_status='pending'
    ↓
Teacher Opens Notice.vue
    ↓
GET /api/submissions/pending-approvals/
    ↓
Displays in "Pending Approvals" section
    ↓
Teacher Clicks Approve/Reject
    ↓
PUT /api/submissions/{id}/approve/
    { action: 'approve' or 'reject' }
    ↓
Database: approval_status updated
    ↓
Removed from pending list
```

## How to Test

### Step 1: Run SQL in pgAdmin
```sql
ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS post_to_feed BOOLEAN DEFAULT FALSE;

ALTER TABLE student_submissions 
ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50) DEFAULT 'pending';
```

### Step 2: Restart Django Server
The models and views will auto-reload.

### Step 3: Test as Student
1. Login as student
2. Go to Portfolio → Select activity
3. Click "Turn in"
4. Add caption and upload file
5. ✅ **Check "Post this output to feeds (visible to class)"**
6. Click "Submit Work"
7. Check console - should see `post_to_feed: true`

### Step 4: Test as Teacher
1. Login as teacher
2. Go to Notice page
3. ✅ **See the student's submission in "Pending Approvals"**
4. Click to preview
5. Click "Approve" or "Reject"
6. ✅ **Submission removed from pending list**

## Database Schema

```
student_submissions
├── id
├── activity_id
├── student_id
├── caption
├── file_path
├── file_type
├── score
├── feedback
├── status ('unscored' | 'scored')
├── post_to_feed (BOOLEAN) ← NEW
├── approval_status ('pending' | 'approved' | 'rejected') ← NEW
├── submitted_at
└── scored_at
```

## API Endpoints Summary

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/activities/{id}/submissions/` | Submit work (with post_to_feed) | Student |
| GET | `/api/submissions/pending-approvals/` | Get pending feed approvals | Teacher |
| PUT | `/api/submissions/{id}/approve/` | Approve/reject submission | Teacher |

## Features

✅ Students can choose to post work to class feed  
✅ Submissions require teacher approval before appearing in feed  
✅ Teachers see all pending approvals in Notice.vue  
✅ Teachers can approve or reject with one click  
✅ Real-time updates from database  
✅ Automatic status tracking  

## Next Steps (Optional)

1. **Show approved posts in student newsfeed**
2. **Notify students when their post is approved/rejected**
3. **Add rejection reason to database**
4. **Show approval history**
