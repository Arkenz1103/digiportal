# Cleanup Guide - Remove Laravel/PHP Files

## Overview

This guide helps you clean up unnecessary Laravel/PHP files from your project now that you're using Django backend.

## Files/Folders to Remove (Laravel/PHP)

### 📁 Folders to Remove:
- ❌ `app/` - Laravel application code
- ❌ `bootstrap/` - Laravel bootstrap files
- ❌ `config/` - Laravel configuration files
- ❌ `database/` - Laravel migrations and seeders
- ❌ `routes/` - Laravel route definitions
- ❌ `storage/` - Laravel storage (logs, cache, uploads)
- ❌ `tests/` - Laravel/PHP tests
- ❌ `vendor/` - PHP dependencies (Composer packages)
- ❌ `backend/` - Old backend folder we created initially

### 📄 Files to Remove:
- ❌ `artisan` - Laravel CLI tool
- ❌ `composer.json` - PHP dependency file
- ❌ `composer.lock` - PHP dependency lock file
- ❌ `phpunit.xml` - PHP testing configuration
- ❌ `.env` - Laravel environment variables (root level)
- ❌ `.env.example` - Laravel env example (root level)

## Files/Folders to KEEP

### ✅ Django Backend:
- ✅ `.be/` - **Your new Django backend**
  - Contains all Django code, models, views, etc.
  - Has its own `.env` file for Django settings

### ✅ Frontend:
- ✅ `resources/` - **Vue.js components and assets**
  - `resources/js/` - Vue components
  - `resources/css/` - Stylesheets
- ✅ `public/` - **Public assets**
- ✅ `node_modules/` - Node.js dependencies
- ✅ `package.json` - Node dependencies
- ✅ `package-lock.json` - Node lock file

### ✅ Configuration:
- ✅ `vite.config.js` - Vite configuration (updated for Django)
- ✅ `tailwind.config.js` - Tailwind CSS config
- ✅ `postcss.config.js` - PostCSS config

### ✅ Documentation:
- ✅ `README.md` - Main readme (updated for Django)
- ✅ `MIGRATION_GUIDE.md` - Migration documentation
- ✅ `QUICK_START.md` - Quick start guide
- ✅ `CLEANUP_GUIDE.md` - This file

### ✅ Git/Editor:
- ✅ `.git/` - Git repository
- ✅ `.gitignore` - Git ignore file
- ✅ `.gitattributes` - Git attributes
- ✅ `.editorconfig` - Editor configuration

## Cleanup Options

### Option 1: Safe Backup (Recommended)

Run the backup script that moves files to a backup folder:

```bash
backup_and_cleanup.bat
```

This will:
- Create `laravel_backup/` folder
- Move all Laravel files there
- Keep everything else intact
- You can delete the backup later if everything works

### Option 2: Direct Delete

Run the cleanup script that permanently deletes files:

```bash
cleanup_laravel.bat
```

⚠️ **Warning:** This permanently deletes files. Make sure you have a backup!

### Option 3: Manual Cleanup

Delete folders and files manually:

1. **Delete folders:**
   ```bash
   rmdir /s /q app
   rmdir /s /q bootstrap
   rmdir /s /q config
   rmdir /s /q database
   rmdir /s /q routes
   rmdir /s /q storage
   rmdir /s /q tests
   rmdir /s /q vendor
   rmdir /s /q backend
   ```

2. **Delete files:**
   ```bash
   del artisan
   del composer.json
   del composer.lock
   del phpunit.xml
   del .env
   del .env.example
   ```

## After Cleanup

Your project structure will look like this:

```
digiportal/
├── .be/                    # ✅ Django backend
│   ├── api/
│   ├── django_rest_main/
│   ├── manage.py
│   └── requirements.txt
├── resources/              # ✅ Vue.js frontend
│   ├── js/
│   └── css/
├── public/                 # ✅ Public assets
├── node_modules/           # ✅ Node dependencies
├── .git/                   # ✅ Git repository
├── package.json            # ✅ Node config
├── vite.config.js          # ✅ Vite config
├── tailwind.config.js      # ✅ Tailwind config
├── README.md               # ✅ Documentation
├── MIGRATION_GUIDE.md      # ✅ Documentation
└── QUICK_START.md          # ✅ Documentation
```

## Verification

After cleanup, verify everything works:

1. **Start Django backend:**
   ```bash
   cd .be
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Start frontend:**
   ```bash
   npm run dev
   ```

3. **Test the application:**
   - Visit http://localhost:5173
   - Try logging in
   - Check if all pages work

## Disk Space Saved

Approximate space saved by removing Laravel files:

- `vendor/` - ~50-100 MB (PHP packages)
- `node_modules/` - Keep (needed for frontend)
- `storage/logs/` - ~1-10 MB
- Other Laravel files - ~5-10 MB

**Total saved:** ~60-120 MB

## Rollback

If you used the backup script and need to rollback:

1. Stop both servers (Django and Vite)
2. Move files back from `laravel_backup/` to root
3. Run `composer install`
4. Run `php artisan serve`

## Final Notes

- ✅ Django backend is fully functional in `.be/`
- ✅ Frontend (Vue.js) remains unchanged
- ✅ All documentation is updated
- ✅ Git history is preserved
- ✅ You can always restore from Git if needed

## Questions?

- Check the [Quick Start Guide](QUICK_START.md)
- Review the [Migration Guide](MIGRATION_GUIDE.md)
- Check the [Backend README](.be/README.md)

---

**Ready to clean up?** Run `backup_and_cleanup.bat` for a safe cleanup! 🧹
