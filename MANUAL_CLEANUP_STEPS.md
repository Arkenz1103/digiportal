# Manual Cleanup Steps

Since automated cleanup scripts are having issues, please follow these manual steps:

## Option 1: Using File Explorer (Easiest)

1. **Open File Explorer** and navigate to:
   ```
   c:\Users\ACER\Downloads\digiportal
   ```

2. **Create a backup folder:**
   - Right-click in the folder → New → Folder
   - Name it: `laravel_backup`

3. **Select and move these FOLDERS** to `laravel_backup`:
   - ✅ `app`
   - ✅ `bootstrap`
   - ✅ `config`
   - ✅ `database`
   - ✅ `routes`
   - ✅ `storage`
   - ✅ `tests`
   - ✅ `vendor`
   - ✅ `backend`

4. **Select and move these FILES** to `laravel_backup`:
   - ✅ `artisan`
   - ✅ `composer.json`
   - ✅ `composer.lock`
   - ✅ `phpunit.xml`
   - ✅ `.env` (root level, NOT the one in .be folder!)
   - ✅ `.env.example` (root level, NOT the one in .be folder!)

5. **DO NOT MOVE these folders/files:**
   - ❌ `.be/` - Your Django backend (KEEP THIS!)
   - ❌ `resources/` - Vue.js frontend
   - ❌ `public/` - Public assets
   - ❌ `node_modules/` - Node dependencies
   - ❌ `.git/` - Git repository
   - ❌ `package.json`, `package-lock.json`
   - ❌ `vite.config.js`, `tailwind.config.js`
   - ❌ All `.md` files (documentation)

---

## Option 2: Using Command Prompt

Open Command Prompt in the digiportal folder and run these commands one by one:

```cmd
REM Create backup folder
mkdir laravel_backup

REM Move folders
for %d in (app bootstrap config database routes storage tests vendor backend) do @if exist %d move %d laravel_backup\

REM Move files
for %f in (artisan composer.json composer.lock phpunit.xml .env .env.example) do @if exist %f move %f laravel_backup\
```

---

## After Cleanup

Your folder structure should look like this:

```
digiportal/
├── .be/                    ✅ Django backend
├── resources/              ✅ Vue.js frontend
├── public/                 ✅ Public assets
├── node_modules/           ✅ Node dependencies
├── laravel_backup/         📦 Backup of Laravel files
├── .git/                   ✅ Git repository
├── package.json            ✅ Node config
├── vite.config.js          ✅ Vite config
├── tailwind.config.js      ✅ Tailwind config
├── README.md               ✅ Documentation
├── QUICK_START.md          ✅ Documentation
└── MIGRATION_GUIDE.md      ✅ Documentation
```

---

## Verify Cleanup

After moving files, check that:

1. ✅ `laravel_backup/` folder exists and contains Laravel files
2. ✅ `.be/` folder still exists (Django backend)
3. ✅ `resources/` folder still exists (Vue.js)
4. ✅ No `app/`, `config/`, `routes/` folders in root
5. ✅ No `artisan`, `composer.json` files in root

---

## Next Steps After Cleanup

1. **Start Django Backend:**
   ```cmd
   cd .be
   venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

2. **Start Frontend (New Terminal):**
   ```cmd
   npm install
   npm run dev
   ```

3. **Test the Application:**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

---

## If Everything Works

After testing and confirming everything works:

1. You can **delete** the `laravel_backup/` folder to free up space
2. Or keep it as a backup for a few days

---

## Need Help?

If you encounter any issues:
- Check [QUICK_START.md](QUICK_START.md) for setup instructions
- Review [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for details
- Make sure PostgreSQL is running
- Verify both Django and Vite servers are running
