# Notification System Setup Guide

## ✅ Step 1: Run Database Migrations

Open your terminal and run these commands:

```bash
cd C:\Users\ACER\Downloads\digiportal\be
python manage.py makemigrations
python manage.py migrate
```

This will create the `notifications` table in your database.

## ✅ Step 2: Verify Tables Created

Check if the tables were created:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from api.models import Notification, NewsfeedPost
print("Notification table exists:", Notification.objects.model._meta.db_table)
print("NewsfeedPost table exists:", NewsfeedPost.objects.model._meta.db_table)
exit()
```

## ✅ Step 3: Test Notification Creation

### Create a Portfolio Folder (as Teacher):

1. Login as teacher
2. Go to Teacher Room
3. Click "Create New Portfolio Folder"
4. Enter folder name and description
5. Click "Create Folder"

### Check Backend Console:

You should see:
```
📢 Notifying X students about new portfolio
✅ Notification created for student: student_username
Folder created successfully - ID: X
```

### Check Student Notifications:

1. Login as student
2. Click the bell icon (🔔) in the top right
3. You should see the notification!

OR

1. Go to Student Notifications page
2. You should see the notification listed

## ✅ Step 4: Verify API Endpoints

Open browser console (F12) and check:

### When creating portfolio:
```
Network tab → Look for POST /api/portfolio/folders/
Status should be 201 Created
```

### When loading notifications:
```
Network tab → Look for GET /api/notifications/
Status should be 200 OK
Response should contain notifications array
```

## 🔍 Troubleshooting

### Error: "404 Not Found" for /api/notifications/

**Solution:** Run migrations (Step 1)

### Error: "Authentication required"

**Solution:** Make sure you're logged in. Check if session cookie exists.

### No notifications showing up

**Checklist:**
1. ✅ Migrations run successfully
2. ✅ At least one student user exists in database
3. ✅ Teacher created a portfolio folder
4. ✅ Backend console shows notification creation logs
5. ✅ Student is logged in
6. ✅ API returns notifications (check Network tab)

### Check if students exist:

```bash
python manage.py shell
```

```python
from api.models import User
students = User.objects.filter(role='student')
print(f"Number of students: {students.count()}")
for student in students:
    print(f"  - {student.username} ({student.email})")
exit()
```

## 📊 Database Schema

### Notification Table:
```
- id (primary key)
- recipient_id (foreign key to User)
- notification_type (varchar)
- title (varchar)
- message (text)
- portfolio_id (foreign key, nullable)
- activity_id (foreign key, nullable)
- submission_id (foreign key, nullable)
- is_read (boolean, default: false)
- created_at (datetime)
- read_at (datetime, nullable)
```

## 🎯 Notification Types

### Student Receives:
- `portfolio_created` - Teacher creates portfolio
- `portfolio_updated` - Teacher updates portfolio
- `portfolio_deleted` - Teacher deletes portfolio
- `activity_created` - Teacher creates activity
- `activity_updated` - Teacher updates activity
- `activity_deleted` - Teacher deletes activity
- `submission_approved` - Post approved for newsfeed
- `submission_rejected` - Post rejected
- `score_added` - Teacher adds score

### Teacher Receives:
- `submission_received` - Student submits work
- `approval_requested` - Student requests approval

## 🚀 Features

- ✅ Real-time notifications
- ✅ Unread count badge
- ✅ Mark as read functionality
- ✅ Auto-refresh every 30 seconds
- ✅ Notifications persist after entity deletion
- ✅ Color-coded by type
- ✅ Icon for each notification type
- ✅ Filter by: All, New, Unread

## 📝 API Endpoints

### GET /api/notifications/
Get all notifications for current user

**Response:**
```json
[
  {
    "id": 1,
    "notification_type": "portfolio_created",
    "title": "New Portfolio Created",
    "message": "Teacher created a new portfolio: Art Class",
    "is_read": false,
    "created_at": "2025-10-18T12:00:00Z",
    "portfolio": 1,
    "activity": null,
    "submission": null
  }
]
```

### PUT /api/notifications/
Mark notification as read

**Request:**
```json
{
  "notification_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "is_read": true,
  "read_at": "2025-10-18T12:05:00Z"
}
```

### GET /api/notifications/unread-count/
Get count of unread notifications

**Response:**
```json
{
  "count": 5
}
```

## ✨ Success Indicators

When everything is working:

1. **Backend Console:**
   ```
   📢 Notifying 3 students about new portfolio
   ✅ Notification created for student: alice
   ✅ Notification created for student: bob
   ✅ Notification created for student: charlie
   Folder created successfully - ID: 5
   ```

2. **Frontend Console (Student):**
   ```
   ✅ Loaded notifications: 5 notifications
   Unread count: 3
   ```

3. **Student UI:**
   - Bell icon shows badge with unread count
   - Clicking bell shows notification dropdown
   - Notifications page shows all notifications
   - Can filter by All/New/Unread
   - Clicking notification marks it as read

## 🎉 You're Done!

The notification system is now fully functional!
