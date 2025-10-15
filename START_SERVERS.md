# 🚀 How to Start Your Servers

## Quick Start (2 Terminals Needed)

### Terminal 1: Django Backend

1. Open **Command Prompt** or **Terminal**
2. Navigate to the `.be` folder:
   ```cmd
   cd c:\Users\ACER\Downloads\digiportal\.be
   ```
3. Run the startup script:
   ```cmd
   start_django.bat
   ```
   
   **OR manually:**
   ```cmd
   venv\Scripts\activate
   python manage.py runserver
   ```

✅ Django will start on **http://localhost:8000**

---

### Terminal 2: Vue.js Frontend

1. Open a **NEW Command Prompt** or **Terminal**
2. Navigate to the root folder:
   ```cmd
   cd c:\Users\ACER\Downloads\digiportal
   ```
3. Run the startup script:
   ```cmd
   start_frontend.bat
   ```
   
   **OR manually:**
   ```cmd
   npm run dev
   ```

✅ Frontend will start on **http://localhost:5173**

---

## ⚠️ Troubleshooting 502 Error

The 502 error means the servers aren't running. Here's how to fix it:

### Check 1: Is Django Installed?

```cmd
cd .be
venv\Scripts\activate
python -c "import django; print('Django installed!')"
```

If you see an error, install dependencies:
```cmd
pip install -r requirements.txt
```

### Check 2: Is PostgreSQL Running?

Django needs PostgreSQL to be running. 

1. Open **Services** (Win + R, type `services.msc`)
2. Find **PostgreSQL** service
3. Make sure it's **Running**

If PostgreSQL isn't installed, you can use SQLite temporarily:

Edit `.be/django_rest_main/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Check 3: Run Migrations

```cmd
cd .be
venv\Scripts\activate
python manage.py makemigrations
python manage.py migrate
```

### Check 4: Check for Errors

Start Django manually to see errors:
```cmd
cd .be
venv\Scripts\activate
python manage.py runserver
```

Look for error messages in the output.

---

## 🔍 Common Issues

### Issue: "No module named 'django'"
**Solution:**
```cmd
cd .be
venv\Scripts\activate
pip install Django djangorestframework django-cors-headers psycopg2-binary
```

### Issue: "could not connect to server"
**Solution:** PostgreSQL isn't running or wrong credentials

**Option A:** Start PostgreSQL service

**Option B:** Use SQLite (see Check 2 above)

### Issue: "Port 8000 already in use"
**Solution:** Kill the process:
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Issue: "Port 5173 already in use"
**Solution:** Kill the process:
```cmd
netstat -ano | findstr :5173
taskkill /PID <PID_NUMBER> /F
```

---

## ✅ Verify Servers Are Running

### Check Django:
Open browser: http://localhost:8000

You should see Django's default page or your app.

### Check Frontend:
Open browser: http://localhost:5173

You should see your Vue.js application.

### Check Ports:
```cmd
netstat -ano | findstr "8000 5173"
```

You should see both ports listed.

---

## 📝 First Time Setup Checklist

Before starting servers, make sure you've done:

- [ ] Installed Python dependencies: `pip install -r requirements.txt`
- [ ] Created `.env` file in `.be/` folder
- [ ] PostgreSQL is running (or switched to SQLite)
- [ ] Run migrations: `python manage.py migrate`
- [ ] Installed npm packages: `npm install`

---

## 🎯 Daily Workflow

Every time you want to work on the project:

1. **Start Django** (Terminal 1):
   ```cmd
   cd .be
   start_django.bat
   ```

2. **Start Frontend** (Terminal 2):
   ```cmd
   start_frontend.bat
   ```

3. **Open browser**: http://localhost:5173

4. **Stop servers**: Press `Ctrl+C` in each terminal

---

## 🆘 Still Not Working?

If you're still getting 502 errors:

1. Make sure BOTH terminals are open and running
2. Check for error messages in the terminal windows
3. Verify PostgreSQL is running
4. Try using SQLite instead (see Check 2 above)
5. Make sure no firewall is blocking ports 8000 or 5173

---

**Need more help?** Check the error messages in the terminal and let me know what they say!
