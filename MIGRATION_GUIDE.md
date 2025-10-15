# Migration Guide: Laravel to Django

This guide explains the migration from Laravel/PHP backend to Django/Python backend.

## What Changed

### Backend Framework
- **Before:** Laravel 10.x (PHP)
- **After:** Django 5.x (Python)

### Key Changes

1. **Backend Location**
   - Laravel files were in the root directory
   - Django backend is now in the `.be/` directory

2. **Database**
   - Still using PostgreSQL
   - Same database name and credentials
   - Django will create its own schema

3. **Frontend**
   - Vue.js 3 with Inertia.js (unchanged)
   - Vite configuration updated to work with Django
   - No Laravel Mix or Laravel Vite Plugin

4. **Authentication**
   - Django's built-in authentication system
   - Custom User model with role field
   - Same role-based access (admin, teacher, student)

## Files Removed (Laravel/PHP)

The following Laravel-specific files are no longer needed:

- `app/` - Laravel application directory
- `bootstrap/` - Laravel bootstrap files
- `config/` - Laravel configuration
- `database/migrations/` - Laravel migrations
- `routes/` - Laravel routes
- `storage/` - Laravel storage
- `vendor/` - PHP dependencies
- `artisan` - Laravel CLI
- `composer.json` - PHP dependencies
- `composer.lock`
- `phpunit.xml` - PHP testing

**Note:** You can safely delete these files, but keep a backup first!

## New Files (Django)

### Backend Files (`.be/` directory)
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `api/` - Main Django application
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `serializer.py` - API serializers
  - `middleware.py` - Custom middleware
  - `admin.py` - Admin configuration
- `django_rest_main/` - Project settings
  - `settings.py` - Django configuration
  - `urls.py` - Root URL configuration

### Configuration Files
- `.be/.env` - Django environment variables
- `.be/.gitignore` - Django-specific gitignore
- `.be/setup.bat` - Setup script

## Migration Steps

### 1. Install Python Dependencies

```bash
cd .be
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database

Create `.be/.env` file:

```env
DB_NAME=TEST
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
```

### 3. Run Django Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Update Frontend Dependencies

```bash
# From root directory
npm install
```

### 6. Start Development Servers

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

## Route Mapping

### Laravel → Django

| Laravel Route | Django Route |
|--------------|--------------|
| `Route::inertia('/', 'Landing')` | `path('', views.landing)` |
| `Route::post('/login', [AuthController::class, 'login'])` | `path('login/', views.login_view)` |
| `Route::post('/logout', [AuthController::class, 'logout'])` | `path('logout/', views.logout_view)` |
| `Route::get('/teacher/home', ...)` | `path('teacher/home/', views.teacher_home)` |
| `Route::get('/student/newsfeed', ...)` | `path('student/newsfeed/', views.student_newsfeed)` |

## Model Mapping

### Laravel Models → Django Models

| Laravel Model | Django Model | Location |
|--------------|--------------|----------|
| `App\Models\User` | `api.models.User` | `.be/api/models.py` |
| `App\Models\LessonPlan` | `api.models.LessonPlan` | `.be/api/models.py` |
| `App\Models\Portfolio` | `api.models.PortfolioFolder` | `.be/api/models.py` |
| `App\Models\PortfolioActivity` | `api.models.PortfolioActivity` | `.be/api/models.py` |

## Middleware Mapping

### Laravel → Django

| Laravel Middleware | Django Equivalent |
|-------------------|-------------------|
| `TeacherMiddleware` | `@teacher_required` decorator |
| `StudentMiddleware` | `@student_required` decorator |
| `AdminMiddleware` | `@admin_required` decorator |

## API Changes

### Authentication

**Laravel:**
```php
Auth::attempt($credentials)
Auth::user()
Auth::logout()
```

**Django:**
```python
authenticate(request, username=username, password=password)
request.user
logout(request)
```

### Inertia Rendering

**Laravel:**
```php
return Inertia::render('Teacher/Home');
```

**Django:**
```python
from inertia import render as inertia_render
return inertia_render(request, 'Teacher/Home')
```

## Database Schema

The Django migrations will create the same database structure as Laravel:

- `users` table with role field
- `lesson_plans` table
- `portfolio_folders` table
- `portfolio_activities` table
- `sessions` table for session management

## Testing

### Laravel Tests → Django Tests

Convert Laravel tests to Django tests:

**Laravel:**
```php
public function test_user_can_login()
{
    $response = $this->post('/login', [
        'email' => 'test@example.com',
        'password' => 'password',
    ]);
    $response->assertRedirect('/teacher/home');
}
```

**Django:**
```python
def test_user_can_login(self):
    response = self.client.post('/login/', {
        'email': 'test@example.com',
        'password': 'password',
    })
    self.assertRedirects(response, '/teacher/home/')
```

## Troubleshooting

### Issue: "No module named 'inertia'"
**Solution:** Install inertia-django: `pip install inertia-django`

### Issue: "Database connection failed"
**Solution:** Check PostgreSQL is running and credentials in `.env` are correct

### Issue: "CORS errors in browser"
**Solution:** Verify CORS settings in `settings.py` and ensure frontend is running on port 5173

### Issue: "Static files not loading"
**Solution:** Run `python manage.py collectstatic` and check `STATIC_ROOT` in settings

## Benefits of Django

1. **Better Performance** - Python's async capabilities
2. **Cleaner Code** - Python's readability
3. **Rich Ecosystem** - Django packages and tools
4. **Better ORM** - Django's ORM is more powerful
5. **Admin Panel** - Built-in admin interface
6. **Security** - Django's security features

## Support

For issues or questions:
1. Check the [Django Documentation](https://docs.djangoproject.com/)
2. Review the [Backend README](.be/README.md)
3. Check Django logs: `.be/django.log`

## Rollback Plan

If you need to rollback to Laravel:
1. Keep the Laravel files in a backup
2. Restore from backup
3. Run `composer install`
4. Run `php artisan migrate`
5. Run `php artisan serve`
