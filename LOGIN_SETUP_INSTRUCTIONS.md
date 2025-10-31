# Login Setup Instructions

## Problem
Users cannot log in because passwords are not set up properly in the database.

## Solution
Run the management commands below to set up passwords for all users.

---

## Step 1: List All Users (Optional - to see what's in the database)

Open your terminal in the backend directory and run:

```bash
cd c:\Users\ACER\Downloads\digiportal\be
python manage.py list_users
```

This will show you all users in the database with their emails and roles.

---

## Step 2: Set Up Passwords for All Users

Run this command to set default passwords for all users:

```bash
python manage.py setup_passwords
```

This will set the following default passwords:
- **Students**: `student123`
- **Teachers**: `teacher123`
- **Admins**: `admin123`

---

## Step 3: Test Login

Now you can log in using any user's email and the default password:

### Example for Student (Gabriel Mendoza):
- **Email**: `gabrielmendoza@student.naawancentral.edu.ph`
- **Password**: `student123`
- **Role**: Select "Student"

### Example for Teacher:
- **Email**: (use the email shown in list_users command)
- **Password**: `teacher123`
- **Role**: Select "Teacher"

---

## Default Passwords Summary

| Role | Default Password |
|------|-----------------|
| Student | `student123` |
| Teacher | `teacher123` |
| Admin | `admin123` |

---

## Troubleshooting

### If login still fails:

1. **Check if the email exists in the database:**
   ```bash
   python manage.py list_users
   ```

2. **Make sure you selected the correct role** (Student/Teacher) that matches the user's role in the database

3. **Check the browser console** for any error messages

4. **Verify the API endpoint is working:**
   - The login API should be at: `http://localhost:5173/api/auth/login/`

### If you need to create a specific user:

You can use Django shell to create a user manually:

```bash
python manage.py shell
```

Then in the shell:

```python
from api.models import User

# Create a teacher
teacher = User.objects.create_user(
    username='johnny.sins',
    email='johnny.sins@ncs.edu.ph',
    password='teacher123',
    role='teacher',
    first_name='Johnny',
    last_name='Sins',
    department='Arts'
)

# Create a student
student = User.objects.create_user(
    username='abigail.vao',
    email='abigail.vao@student.ncs.edu.ph',
    password='student123',
    role='student',
    first_name='Abigail',
    last_name='Vao',
    id_number='STD001',
    grade_level='Grade 1',
    section='A'
)

print("Users created successfully!")
```

---

## Security Note

⚠️ **IMPORTANT**: These are default passwords for development/testing only. 

In production, you should:
1. Force users to change their password on first login
2. Use strong password requirements
3. Never use simple default passwords like "student123"

---

## Next Steps

After setting up passwords, users can:
1. Go to the login page
2. Select their role (Student/Teacher)
3. Enter their email address
4. Enter the default password
5. Click "Sign In"

The system will authenticate them and redirect to the appropriate dashboard.
