# DigiPortal

A modern digital portfolio and learning management system built with Django and Vue.js.

## Tech Stack

### Backend
- **Django 5.x** - Python web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Database
- **Inertia.js** - Server-side rendering adapter

### Frontend
- **Vue.js 3** - JavaScript framework
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS framework
- **PrimeVue** - UI component library

## Features

- **Role-based Access Control** - Admin, Teacher, and Student roles
- **Authentication System** - Secure login/logout functionality
- **Teacher Portal** - Manage classes, lesson plans, and student progress
- **Student Portal** - View assignments, submit work, and track progress
- **Portfolio Management** - Organize and showcase student work
- **Real-time Updates** - Live notifications and updates

## Quick Start

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- Node.js 18 or higher
- npm or yarn

### Installation

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd .be

# Run setup script (Windows)
setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

#### 2. Frontend Setup

```bash
# From root directory
npm install
npm run dev
```

#### 3. Start Development Servers

**Backend (Terminal 1):**
```bash
cd .be
venv\Scripts\activate
python manage.py runserver
```

**Frontend (Terminal 2):**
```bash
npm run dev
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173

## Project Structure

```
digiportal/
├── .be/                    # Django backend
│   ├── api/               # Main application
│   ├── django_rest_main/  # Project settings
│   ├── manage.py
│   └── requirements.txt
├── resources/             # Frontend resources
│   ├── js/               # Vue.js components
│   └── css/              # Stylesheets
├── public/               # Public assets
├── vite.config.js        # Vite configuration
├── package.json          # Node dependencies
└── README.md            # This file
```

## Configuration

### Database Configuration

Update `.be/.env` with your PostgreSQL credentials:

```env
DB_NAME=TEST
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
```

### Environment Variables

Create `.be/.env` from `.be/.env.example` and update as needed.

## Development

### Running Migrations

```bash
cd .be
python manage.py makemigrations
python manage.py migrate
```

### Creating Test Users

```bash
python manage.py createsuperuser
```

### Admin Panel

Access the Django admin at http://localhost:8000/admin

## Documentation

For detailed documentation, see:
- [Backend Documentation](.be/README.md)
- [API Documentation](.be/API.md) (coming soon)

## License

MIT License
