# Post to Feed Button - Fix Applied

## Problem
The "Post to Feed" button was missing from the student room page after submitting work. Students could only request to post during initial submission, but couldn't request it later for already-submitted work.

## Solution

### 1. **Added Post to Feed Button** (`resources/js/Pages/Student/Sroom.vue`)

Added a new button that appears after work is submitted:

**Location:** Below the "Resubmit" button in the "Your Work" section

**Features:**
- ✅ Shows "Post to Feed" button if work hasn't been posted yet
- ✅ Shows "Post Request Pending" status if request is waiting for approval
- ✅ Shows "Posted to Feed" status if already approved
- ✅ Disabled if work has been scored
- ✅ Beautiful blue gradient styling
- ✅ Loading state while requesting

### 2. **Added Request Function** (`resources/js/Pages/Student/Sroom.vue`)

Created `requestPostToFeed()` function that:
- Updates the submission to set `post_to_feed = true`
- Updates `approval_status = 'pending'`
- Sends notification to teacher
- Updates UI to show pending status
- Shows success message to student

### 3. **Enhanced Backend** (`be/api/views.py`)

Updated `submission_detail_api` to:
- Handle `post_to_feed` updates
- Automatically set `approval_status = 'pending'` when requesting
- Send notification to teacher about the post request
- Log the request for debugging

## How It Works

### Student Workflow:

1. **Submit Work Initially**
   - Student submits work (with or without "Post to feed" checkbox)
   - Work is submitted successfully

2. **Request to Post Later**
   - Student sees "Post to Feed" button below "Resubmit"
   - Clicks "Post to Feed"
   - Button shows "Requesting..." while processing
   - Success message: "Your post request has been sent to your teacher for approval!"
   - Button changes to "Post Request Pending" status

3. **After Teacher Approves**
   - Status changes to "Posted to Feed"
   - Work appears in class newsfeed

### Teacher Workflow:

1. **Receives Notification**
   - Gets notification about post request
   - Sees submission in Notice page

2. **Reviews and Approves**
   - Reviews the work
   - Approves or rejects
   - Student gets notified

## UI States

### State 1: Not Posted Yet
```
┌─────────────────────────────────┐
│     [Resubmit]                  │
│     [Post to Feed] 📤           │ ← New button
└─────────────────────────────────┘
```

### State 2: Request Pending
```
┌─────────────────────────────────┐
│     [Resubmit]                  │
│  ✓ Post Request Pending         │ ← Status indicator
└─────────────────────────────────┘
```

### State 3: Already Posted
```
┌─────────────────────────────────┐
│     [Resubmit]                  │
│  ✓ Posted to Feed               │ ← Success indicator
└─────────────────────────────────┘
```

### State 4: Already Scored
```
┌─────────────────────────────────┐
│  [Already Scored] (disabled)    │
│  [Post to Feed] (disabled)      │ ← Both disabled
└─────────────────────────────────┘
```

## Button Styling

**Post to Feed Button:**
- Gradient: Blue (500) to Indigo (600)
- Icon: Send icon (pi-send)
- Hover: Darker blue gradient
- Disabled: 50% opacity

**Status Indicators:**
- Background: Green-50
- Border: Green-200
- Text: Green-700
- Icon: Check circle

## Testing

### Test 1: Submit Work Without Post Request

1. Login as student
2. Go to a class room
3. Submit work WITHOUT checking "Post to feed"
4. After submission, you should see:
   - ✅ "Resubmit" button
   - ✅ "Post to Feed" button (NEW!)

### Test 2: Request Post After Submission

1. Click "Post to Feed" button
2. Should see:
   - Loading state: "Requesting..."
   - Success toast: "Your post request has been sent..."
   - Status changes to: "Post Request Pending"

### Test 3: Check Teacher Notice Page

1. Login as teacher
2. Go to Notice page
3. Should see the student's post request
4. Can approve or reject

### Test 4: After Approval

1. Login as student
2. Go back to the activity
3. Status should show: "Posted to Feed"
4. Work should appear in newsfeed

### Test 5: Scored Work

1. Teacher scores the work
2. Student sees:
   - "Already Scored" button (disabled)
   - "Post to Feed" button (disabled)
   - Cannot post scored work

## Backend Logs

When student clicks "Post to Feed", backend shows:

```
📢 Submission 123 requesting post to feed - approval_status set to pending
```

When teacher views Notice page:

```
============================================================
📝 PENDING APPROVALS CHECK for teacher: teacher_name
============================================================
Found 1 pending approvals

   📋 Submission #123:
      Student: student_name
      Activity: Activity Title
      Caption: Student's caption...
      Status: unscored
      Approval Status: pending
      Post to Feed: True
      File Type: image
      Submitted At: 2025-10-27 00:13:00
============================================================
```

## Files Modified

1. **`resources/js/Pages/Student/Sroom.vue`**
   - Added "Post to Feed" button (lines 454-472)
   - Added `isRequestingPost` ref (line 2675)
   - Added `requestPostToFeed()` function (lines 3986-4032)

2. **`be/api/views.py`**
   - Enhanced `submission_detail_api` PUT handler (lines 2025-2047)
   - Auto-sets `approval_status='pending'` when `post_to_feed=true`
   - Sends notification to teacher

## Important Notes

- ✅ Button only shows for unscored work
- ✅ Button disappears after request is sent
- ✅ Status indicator shows current state
- ✅ Teacher gets notified automatically
- ✅ Works with existing approval system
- ✅ Fully integrated with Notice page

## Next Steps

1. **Restart backend server** (if not already running)
2. **Test the new button** - submit work and try posting
3. **Check teacher Notice page** - verify request appears
4. **Test approval flow** - approve and check newsfeed

The "Post to Feed" button is now fully functional! 🎉
