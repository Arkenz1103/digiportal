# Testing Guide: Student Post Approval System

## What Was Fixed

### 1. **Database Model** (`be/api/models.py`)
- Changed `approval_status` default from `'pending'` to `'approved'`
- Now only submissions with `post_to_feed=True` get `approval_status='pending'`

### 2. **Backend Logging** (`be/api/views.py`)
- Added comprehensive debug logging for submission creation
- Added detailed logging for pending approvals query
- Logs will show exactly what's happening

### 3. **Frontend UI** (`resources/js/Pages/Teacher/Notice.vue`)
- Better image display with error handling
- Improved wording ("Student Work" instead of "Sample Image")
- Better error messages

## How to Test

### Step 1: Start the Backend Server

```bash
cd be
py manage.py runserver
```

**Watch the console output!** You'll see detailed logs.

### Step 2: Test as Student

1. **Login as Student**
   - Go to `localhost:5173/student/room`
   - Select a class (e.g., "Grade 1 - A")

2. **Submit Work with Post Request**
   - Click on an activity (e.g., "DD")
   - Click "Add or create" to upload work
   - Add a caption (e.g., "dd")
   - Upload an image file
   - ✅ **CHECK THE CHECKBOX**: "Post this output to feeds (visible to class)"
   - Click "Submit Work"

3. **Check Backend Console**
   You should see logs like:
   ```
   ✅ Submission created: ID=123, status=unscored, file_type=image, is_late=False, is_draft=False
   📢 POST TO FEED: True, APPROVAL STATUS: pending
   🔔 This submission should appear in teacher's Notice page!
   ```

### Step 3: Test as Teacher

1. **Login as Teacher**
   - Go to `localhost:5173/teacher/notice`

2. **Check Backend Console**
   You should see:
   ```
   ============================================================
   📝 PENDING APPROVALS CHECK for teacher: teacher_username
   ============================================================
   Found 1 pending approvals
   
      📋 Submission #123:
         Student: student_username
         Activity: DD
         Caption: dd...
         Status: unscored
         Approval Status: pending
         Post to Feed: True
         File Type: image
         Submitted At: 2025-10-26 22:10:00
   ============================================================
   ```

3. **Check Frontend**
   - You should see the submission in the "Pending Approvals" section
   - Student name, activity title, and caption should be visible
   - Thumbnail image should display
   - "Review" button should be available

4. **Review the Submission**
   - Click "Review" button
   - Full image should display
   - Student name and work details visible
   - "Approve" and "Reject" buttons available

5. **Approve the Submission**
   - Click "Approve"
   - Confirm approval
   - Submission should disappear from pending list
   - Check student newsfeed - post should appear there

## Troubleshooting

### Issue: Submission not appearing in Notice page

**Check these things:**

1. **Backend Console Logs**
   - Does it show "POST TO FEED: True"?
   - Does it show "APPROVAL STATUS: pending"?
   - If NO → The checkbox might not be working properly

2. **Database Check**
   ```bash
   cd be
   py manage.py shell
   ```
   ```python
   from api.models import StudentSubmission
   
   # Check all pending submissions
   pending = StudentSubmission.objects.filter(approval_status='pending')
   for sub in pending:
       print(f"ID: {sub.id}, Student: {sub.student.username}, Activity: {sub.activity.title if sub.activity else 'N/A'}")
       print(f"   post_to_feed: {sub.post_to_feed}, approval_status: {sub.approval_status}")
   ```

3. **Frontend Console Logs**
   - Open browser DevTools (F12)
   - Check Console tab for errors
   - Check Network tab for API calls to `/api/submissions/pending-approvals/`

### Issue: Image not displaying

**Check:**
1. File type is 'image'
2. file_path or file_url contains valid data
3. Browser console for image load errors
4. Backend logs show correct file_type

### Issue: "Failed to prepare resubmission" error

This happens when:
1. Work has already been scored by teacher
2. Maximum resubmit limit (3) reached
3. Trying to resubmit when not allowed

**Solution:**
- Don't click "Resubmit" on already submitted work
- Wait for teacher to score first
- Or submit new work instead

## Expected Behavior

### Normal Flow:
1. Student submits work → `status='unscored'`, `approval_status='approved'`
2. Work appears in teacher's "Unscored" list
3. Teacher scores it
4. Student sees score

### Post to Feed Flow:
1. Student submits work with checkbox → `status='unscored'`, `approval_status='pending'`, `post_to_feed=True`
2. Work appears in teacher's "Notice" page (Pending Approvals)
3. Teacher reviews and approves
4. Work appears in class newsfeed
5. Student gets notification

## Files Modified

1. `be/api/models.py` - Model default value
2. `be/api/views.py` - Added debug logging
3. `be/api/migrations/0034_alter_studentsubmission_approval_status.py` - Migration
4. `resources/js/Pages/Teacher/Notice.vue` - UI improvements

## Important Notes

- The migration has been applied (0034)
- All existing submissions have `approval_status='approved'` by default
- Only NEW submissions with `post_to_feed=True` will have `approval_status='pending'`
- Backend logs are very detailed now - watch them!

## If It Still Doesn't Work

1. **Restart the backend server** (Ctrl+C, then `py manage.py runserver`)
2. **Clear browser cache** (Ctrl+Shift+Delete)
3. **Check the backend console** for detailed logs
4. **Take a screenshot** of:
   - Student submission page (with checkbox checked)
   - Teacher Notice page (showing empty or with submissions)
   - Backend console logs
   - Browser console (F12)

Then share the screenshots for further debugging!
