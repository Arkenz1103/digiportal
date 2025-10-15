# 🚀 DigiPortal - Final Startup Guide

## ✅ **Everything is Ready!**

Your DigiPortal has been successfully migrated from Laravel to Django!

---

## 📋 **What You Need:**

- ✅ Django backend configured
- ✅ Vue.js frontend configured
- ✅ PostgreSQL database connected
- ✅ All routes mapped
- ✅ All connections verified

---

## 🚀 **How to Start (Every Time):**

### **Method 1: Easy Start (Recommended)**

**Double-click this file:**
```
START_SERVERS_FINAL.bat
```

This will open 2 windows automatically:
- Window 1: Django Backend
- Window 2: Vue Frontend

---

### **Method 2: Manual Start (2 Terminals)**

#### **Terminal 1 - Django Backend:**

```cmd
cd c:\Users\ACER\Downloads\digiportal\.be
py manage.py runserver
```

**You should see:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2.7, using settings 'django_rest_main.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

✅ **Leave this terminal open!**

---

#### **Terminal 2 - Vue Frontend:**

```cmd
cd c:\Users\ACER\Downloads\digiportal
npm run dev
```

**You should see:**
```
VITE v5.4.11  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  press h + enter to show help
```

✅ **Leave this terminal open!**

---

## 🌐 **Access Your Application:**

**Main Application:**
```
http://localhost:5173
```

**Admin Panel:**
```
http://localhost:8000/admin
```

**Django API:**
```
http://localhost:8000
```

---

## ⚠️ **Common Issues:**

### **Issue 1: "This localhost page can't be found" (404)**

**Cause:** Django is not running

**Solution:**
1. Check if Django terminal is open and running
2. Look for "Starting development server at http://127.0.0.1:8000/"
3. If not running, start Django: `cd .be && py manage.py runserver`

---

### **Issue 2: Blank page or loading forever**

**Cause:** Frontend can't connect to backend

**Solution:**
1. Make sure BOTH servers are running
2. Check Django terminal for errors
3. Refresh browser with Ctrl+Shift+R (hard refresh)

---

### **Issue 3: "Port already in use"**

**Cause:** Server is already running

**Solution:**

**For port 8000 (Django):**
```cmd
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

**For port 5173 (Vite):**
```cmd
netstat -ano | findstr :5173
taskkill /F /PID <PID_NUMBER>
```

---

### **Issue 4: "No module named 'django'"**

**Cause:** Django not installed

**Solution:**
```cmd
py -m pip install Django djangorestframework django-cors-headers psycopg2-binary Pillow python-decouple
```

---

### **Issue 5: Database connection error**

**Cause:** PostgreSQL not running or wrong credentials

**Solution:**
1. Check if PostgreSQL is running
2. Verify database exists: `DigiportDB`
3. Check credentials in `.be/.env`

---

## 🔍 **Verify Servers Are Running:**

### **Check Django (port 8000):**
```cmd
netstat -ano | findstr :8000
```

Should show a line with `:8000`

### **Check Vite (port 5173):**
```cmd
netstat -ano | findstr :5173
```

Should show a line with `:5173`

---

## 📊 **Server Status Checklist:**

Before visiting http://localhost:5173, verify:

- [ ] Django terminal is open
- [ ] Django shows "Starting development server"
- [ ] Vite terminal is open  
- [ ] Vite shows "Local: http://localhost:5173/"
- [ ] No error messages in either terminal
- [ ] PostgreSQL is running

---

## 🎯 **Quick Test:**

### **Test 1: Django is responding**
Visit: http://localhost:8000

You should see something (not a connection error)

### **Test 2: Frontend is serving**
Visit: http://localhost:5173

You should see your DigiPortal landing page

---

## 📝 **First Time Setup (One Time Only):**

If you haven't done these yet:

### **1. Create Superuser:**
```cmd
cd .be
py manage.py createsuperuser
```

Enter username, email, and password when prompted.

### **2. Create Test Users:**

Visit http://localhost:8000/admin and create:
- A teacher user (role: teacher)
- A student user (role: student)

---

## 🔄 **Daily Workflow:**

### **Starting Work:**
1. Open 2 terminals
2. Terminal 1: `cd .be && py manage.py runserver`
3. Terminal 2: `npm run dev`
4. Visit http://localhost:5173

### **Stopping Work:**
1. Press Ctrl+C in Django terminal
2. Press Ctrl+C in Vite terminal
3. Close terminals

---

## 📁 **Project Structure:**

```
digiportal/
├── .be/                    🐍 Django Backend
│   ├── api/               Main app
│   ├── django_rest_main/  Settings
│   └── manage.py          Django CLI
│
├── resources/             🎨 Vue.js Frontend
│   └── js/               Vue components
│
├── public/                📦 Static files
├── node_modules/          📚 Node packages
└── package.json           Node config
```

---

## ✅ **What's Working:**

- ✅ Django backend on port 8000
- ✅ Vue.js frontend on port 5173
- ✅ PostgreSQL database connected
- ✅ 18 routes mapped
- ✅ Inertia.js integration
- ✅ Role-based authentication
- ✅ All assets configured
- ✅ CORS enabled
- ✅ Hot reload working

---

## 🎊 **You're Ready!**

Everything is configured and ready to go!

**Just start both servers and visit http://localhost:5173**

---

## 📚 **Documentation:**

- `CONNECTIONS_VERIFIED.md` - All connections verified
- `ASSETS_CONNECTION_GUIDE.md` - Asset configuration
- `JSON_JS_ROUTES_VERIFIED.md` - Routes verification
- `PUBLIC_FOLDER_FIXED.md` - Public folder cleanup
- `.be/BACKEND_CLEANED.md` - Backend structure
- `CONNECTION_STATUS.md` - Overall status

---

## 🆘 **Still Having Issues?**

If the page still doesn't load:

1. **Check Django terminal** - Look for error messages
2. **Check Vite terminal** - Look for error messages
3. **Check browser console** - Press F12, look for errors
4. **Verify both servers are running** - Use netstat commands above
5. **Try hard refresh** - Ctrl+Shift+R in browser

---

## 🎯 **Success Indicators:**

You'll know it's working when you see:

1. ✅ Django terminal shows "Starting development server"
2. ✅ Vite terminal shows "Local: http://localhost:5173/"
3. ✅ Browser shows DigiPortal landing page
4. ✅ No 404 or connection errors

---

**Happy Coding! 🚀**

Your DigiPortal is now running on Django + Vue.js!
