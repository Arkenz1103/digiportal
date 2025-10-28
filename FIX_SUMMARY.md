# Fix Summary: Student Post Approval System

## Problem
When students submitted work with "Post this output to feeds" checkbox checked, the submissions were not appearing in the teacher's Notice page for approval.

## Root Cause
The `approval_status` field in the `StudentSubmission` model had a default value of `'pending'` for ALL submissions, even those that didn't request feed posting. This caused confusion in the filtering logic.

## Solution

### 1. **Model Update** (`be/api/models.py`)
Changed the default `approval_status` from `'pending'` to `'approved'`:
```python
# Before:
approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='pending')

# After:
approval_status = models.CharField(max_length=50, choices=APPROVAL_CHOICES, default='approved')
```

**Logic:**
- When `post_to_feed = False`: `approval_status = 'approved'` (default, no approval needed)
- When `post_to_feed = True`: `approval_status = 'pending'` (set explicitly in views.py line 1452)

### 2. **Frontend Improvements** (`resources/js/Pages/Teacher/Notice.vue`)

#### Better Image Handling:
- Added fallback for missing images
- Better error handling with console logging
- Placeholder icon when no image is available
- Improved alt text for accessibility

#### Improved Wording:
- Changed "Sample Image" → "Student Work"
- Changed "No description provided" → "No caption provided"
- Changed "View All" → "View Full Work"
- Added student name to image alt text

#### Enhanced Display:
- Better border styling (indigo-200)
- Larger preview images (max-h-[500px])
- More informative error messages
- Student name badge at bottom of preview

### 3. **Migration File**
Created `0003_update_approval_status_default.py` to update the database schema.

## How It Works Now

### Student Workflow:
1. Student submits work for an activity
2. Student checks "Post this output to feeds" checkbox
3. Backend sets:
   - `post_to_feed = True`
   - `approval_status = 'pending'`
4. Submission appears in teacher's Notice page

### Teacher Workflow:
1. Teacher navigates to Notice page
2. Sees list of pending approvals (filtered by `approval_status='pending'`)
3. Can preview the student's work with proper image display
4. Can approve or reject with feedback
5. On approval:
   - `approval_status = 'approved'`
   - Post created in newsfeed
   - Student notified

## Database Query
The Notice page fetches submissions with:
```python
StudentSubmission.objects.filter(
    approval_status='pending',
    activity__folder__teacher=request.user
)
```

This now correctly shows only submissions that:
- Have `post_to_feed = True`
- Are waiting for teacher approval
- Belong to the teacher's classes

## Testing Steps

1. **Run Migration:**
   ```bash
   cd be
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Test as Student:**
   - Login as student
   - Go to a class room
   - Submit work for an activity
   - Check "Post this output to feeds (visible to class)"
   - Submit

3. **Test as Teacher:**
   - Login as teacher
   - Go to Notice page
   - Should see the student's submission
   - Click "Review" to see full work
   - Image should display properly
   - Approve or reject

4. **Verify:**
   - Check student newsfeed for approved post
   - Check student notifications

## Files Modified

1. `be/api/models.py` - Changed default approval_status
2. `be/api/migrations/0003_update_approval_status_default.py` - New migration
3. `resources/js/Pages/Teacher/Notice.vue` - Improved UI and image handling

## Notes

- The backend logic in `views.py` (line 1451-1452) was already correct
- The serializer was already returning all necessary fields
- The main issue was the model default value causing incorrect filtering
- Image display improvements help with debugging and user experience
