# Sketch Save & Post to Newsfeed - Fix Applied

## Problem
Student users were getting 403 (Forbidden) errors when trying to:
1. Save sketches
2. Post sketches to newsfeed

## Root Cause
The API endpoints were checking authentication but may have been failing due to:
- Session/cookie issues
- Role validation problems
- Missing error details

## Solution Applied

### 1. **Enhanced Error Logging** (`be/api/views.py`)

Added comprehensive debugging to three endpoints:

#### A. `sketch_submission_api` (POST `/api/sketch/submit/`)
- Logs user authentication status
- Logs user role
- Logs data being received
- Shows detailed error traces

#### B. `sketches_api` (GET/POST `/api/sketches/`)
- Logs authentication and role checks
- Logs sketch save operations
- Shows image data length
- Detailed error traces

#### C. Added role validation
- Now explicitly checks if user is a student
- Returns clear error messages

### 2. **What the Logs Show**

When you try to save or post a sketch, you'll see:

```
============================================================
🎨 SKETCH SUBMISSION REQUEST
============================================================
User authenticated: True
User: student_username
User role: student
📝 Data received: caption=My awesome sketch...
📝 File path length: 15234
📝 File type: image
✅ Sketch submission created: ID=45
📢 POST TO FEED: True, APPROVAL STATUS: pending
============================================================
```

Or if there's an error:
```
❌ Authentication failed!
```
or
```
❌ User is not a student!
```

## Testing Steps

### 1. **Restart Backend Server**
```bash
cd be
py manage.py runserver
```

### 2. **Test Save Sketch**
1. Login as student
2. Go to Sketch page (`localhost:5173/student/sketch`)
3. Draw something
4. Click "Save" button
5. **Check backend console** - you should see:
   ```
   💾 Saving sketch for student_username
      Title: Sketch 10/26/2025...
      Image data length: 12345
   ✅ Sketch saved: ID=123
   ```

### 3. **Test Post to Newsfeed**
1. After saving, click "Post to Newsfeed" button
2. Select a sketch
3. Add a caption
4. Click "Post"
5. **Check backend console** - you should see:
   ```
   ============================================================
   🎨 SKETCH SUBMISSION REQUEST
   ============================================================
   User authenticated: True
   User: student_name
   User role: student
   📝 Data received: caption=Check out my art...
   📝 File path length: 15234
   📝 File type: image
   ✅ Sketch submission created: ID=45
   📢 POST TO FEED: True, APPROVAL STATUS: pending
   ============================================================
   ```

### 4. **Check Teacher Notice Page**
1. Login as teacher
2. Go to Notice page
3. Should see the sketch submission in pending approvals

## Common Issues & Solutions

### Issue 1: "Authentication required" error

**Cause:** User session expired or cookies not working

**Solution:**
1. Logout and login again
2. Clear browser cookies
3. Check if you're logged in as a student (not teacher)

### Issue 2: "Only students can manage sketches" error

**Cause:** Logged in as teacher or admin

**Solution:**
- Make sure you're logged in as a student user

### Issue 3: Still getting 403 error

**Check backend console logs:**
- If it shows "User not authenticated" → Session issue, re-login
- If it shows "User is not a student" → Wrong user type
- If no logs appear → API endpoint not being reached, check URL

**Check browser console (F12):**
- Look for the actual error message
- Check Network tab for the failed request
- Look at the request headers (should include session cookie)

### Issue 4: Sketch saves but doesn't post to newsfeed

**This is expected!** Sketches posted to newsfeed need teacher approval:
1. Sketch is saved to database
2. Submission created with `approval_status='pending'`
3. Teacher must approve it in Notice page
4. Then it appears in newsfeed

## Files Modified

1. `be/api/views.py` - Added comprehensive logging and role checks:
   - `sketch_submission_api` (line 2446-2498)
   - `sketches_api` (line 2501-2555)

## What to Check

### Backend Console Should Show:
- ✅ User authentication status
- ✅ User role
- ✅ Data being processed
- ✅ Success or error messages
- ✅ Stack traces for errors

### Frontend Should Show:
- ✅ Success toast message after saving
- ✅ Sketch appears in "My Sketches" list
- ✅ Success message after posting to newsfeed

## Next Steps

1. **Restart backend server** (important!)
2. **Try to save a sketch** - watch backend console
3. **Try to post to newsfeed** - watch backend console
4. **Share the backend console output** if still getting errors

The detailed logging will tell us exactly what's failing!
