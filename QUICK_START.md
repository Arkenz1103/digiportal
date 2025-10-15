# Quick Start Guide - Django Backend Setup

Follow these steps to get your Django backend running:

## Step 1: Install Python Dependencies

Open a terminal in the `.be` directory and run:

```bash
cd .be

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:** You should see packages being installed (Django, djangorestframework, etc.)

---

## Step 2: Verify Installation

Check if Django is installed:

```bash
python -c "import django; print(f'Django {django.VERSION} installed successfully!')"
```

---

## Step 3: Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Expected output:**
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying api.0001_initial... OK
  ...
```

---

## Step 4: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: (your choice)
- Email: (your email)
- Password: (your password)

---

## Step 5: Start Django Development Server

```bash
python manage.py runserver
```

**Expected output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Django backend is now running at http://localhost:8000**

---

## Step 6: Start Frontend Development Server

Open a **NEW terminal** in the root directory:

```bash
# Install frontend dependencies (if not already done)
npm install

# Start Vite dev server
npm run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

✅ **Frontend is now running at http://localhost:5173**

---

## Step 7: Access the Application

Open your browser and navigate to:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

---

## Troubleshooting

### Issue: "No module named 'django'"

**Solution:** Make sure you activated the virtual environment:
```bash
cd .be
venv\Scripts\activate
```

### Issue: "django.db.utils.OperationalError: could not connect to server"

**Solution:** 
1. Make sure PostgreSQL is running
2. Check your database credentials in `.be/.env`
3. Verify the database exists:
   ```sql
   -- In PostgreSQL
   CREATE DATABASE TEST;
   ```

### Issue: "CSRF verification failed"

**Solution:** Make sure both servers are running:
- Django on port 8000
- Vite on port 5173

### Issue: "Port already in use"

**Solution:** Kill the process using the port:
```bash
# For port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# For port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

---

## Testing the Setup

### 1. Test Backend API

Visit http://localhost:8000/admin and login with your superuser credentials.

### 2. Test Frontend

Visit http://localhost:5173 - you should see the landing page.

### 3. Test Login

1. Go to http://localhost:5173/login
2. Enter your credentials
3. You should be redirected based on your role

---

## Creating Test Users

You can create test users via Django admin or Django shell:

### Via Admin Panel:
1. Go to http://localhost:8000/admin
2. Click "Users" → "Add User"
3. Fill in the details and set the role (teacher/student)

### Via Django Shell:
```bash
python manage.py shell
```

```python
from api.models import User

# Create a teacher
teacher = User.objects.create_user(
    username='teacher1',
    email='teacher@example.com',
    password='password123',
    role='teacher',
    first_name='John',
    last_name='Doe'
)

# Create a student
student = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='password123',
    role='student',
    first_name='Jane',
    last_name='Smith'
)

print("Users created successfully!")
```

---

## Daily Development Workflow

### Starting the servers:

**Terminal 1 (Backend):**
```bash
cd .be
venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
npm run dev
```

### Stopping the servers:

Press `Ctrl+C` in each terminal

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run migrations
3. ✅ Create superuser
4. ✅ Start Django server
5. ✅ Start frontend server
6. ✅ Test the application
7. 📝 Create test users (teachers and students)
8. 🎨 Customize and develop features

---

## Useful Commands

```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Run tests
python manage.py test

# Check for issues
python manage.py check
```

---

## Need Help?

- Check the [Backend README](.be/README.md)
- Review the [Migration Guide](MIGRATION_GUIDE.md)
- Check Django logs in the terminal
- Verify both servers are running

Happy coding! 🚀
