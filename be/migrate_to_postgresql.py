"""
Migration Script: SQLite to PostgreSQL
This script exports data from SQLite and prepares it for PostgreSQL import
"""
import os
import sys
import json
import sqlite3
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB = os.path.join(BASE_DIR, 'db.sqlite3')
BACKUP_DIR = os.path.join(BASE_DIR, 'database_backup')

def create_backup_directory():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"Created backup directory: {BACKUP_DIR}")
    return BACKUP_DIR

def export_sqlite_data():
    """Export all data from SQLite database"""
    print("\n" + "="*60)
    print("  EXPORTING DATA FROM SQLITE")
    print("="*60)
    
    if not os.path.exists(SQLITE_DB):
        print(f"ERROR: SQLite database not found at {SQLITE_DB}")
        return False
    
    try:
        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nFound {len(tables)} tables to export")
        
        backup_data = {}
        
        for table in tables:
            if table.startswith('sqlite_'):
                continue
                
            print(f"  Exporting: {table}...", end=" ")
            
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
            table_data = []
            for row in rows:
                row_dict = {}
                for key in row.keys():
                    value = row[key]
                    # Handle datetime and other types
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    row_dict[key] = value
                table_data.append(row_dict)
            
            backup_data[table] = table_data
            print(f"{len(table_data)} rows")
        
        # Save to JSON file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(BACKUP_DIR, f'sqlite_backup_{timestamp}.json')
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, default=str)
        
        print(f"\nBackup saved to: {backup_file}")
        
        conn.close()
        return backup_file
        
    except Exception as e:
        print(f"\nERROR: Failed to export data: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def generate_postgresql_setup_sql():
    """Generate SQL script to set up PostgreSQL database"""
    print("\n" + "="*60)
    print("  GENERATING POSTGRESQL SETUP SCRIPT")
    print("="*60)
    
    sql_script = """-- PostgreSQL Database Setup for DigiPortal
-- Run this script in pgAdmin or psql

-- Drop database if exists (WARNING: This will delete all data!)
DROP DATABASE IF EXISTS "DigiportDB";

-- Create database
CREATE DATABASE "DigiportDB"
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

-- Connect to the database
\\c "DigiportDB"

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE "DigiportDB" TO postgres;

-- The tables will be created automatically by Django migrations
-- Just run: py manage.py migrate

COMMENT ON DATABASE "DigiportDB" IS 'DigiPortal Application Database';
"""
    
    sql_file = os.path.join(BACKUP_DIR, 'setup_postgresql.sql')
    with open(sql_file, 'w', encoding='utf-8') as f:
        f.write(sql_script)
    
    print(f"SQL script saved to: {sql_file}")
    return sql_file

def create_migration_instructions():
    """Create detailed migration instructions"""
    print("\n" + "="*60)
    print("  CREATING MIGRATION INSTRUCTIONS")
    print("="*60)
    
    instructions = """# SQLite to PostgreSQL Migration Instructions

## Prerequisites

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Install pgAdmin (usually included with PostgreSQL)

2. **Install Python PostgreSQL Driver**
   ```bash
   pip install psycopg2
   # or if that fails:
   pip install psycopg2-binary
   ```

## Step-by-Step Migration

### Step 1: Backup SQLite Data (COMPLETED)
✓ SQLite data has been exported to JSON format
✓ Backup location: database_backup/

### Step 2: Set Up PostgreSQL Database

**Option A: Using pgAdmin (Recommended)**
1. Open pgAdmin
2. Right-click on "Databases" → Create → Database
3. Database name: `DigiportDB`
4. Owner: `postgres`
5. Click "Save"

**Option B: Using SQL Script**
1. Open pgAdmin
2. Right-click on "PostgreSQL" server → Query Tool
3. Open file: `database_backup/setup_postgresql.sql`
4. Click Execute (F5)

### Step 3: Update Django Settings
✓ Settings have been updated to use PostgreSQL
✓ Location: django_rest_main/settings.py

### Step 4: Run Django Migrations
```bash
cd .be

# Delete old migration files (optional, for clean start)
# del /s api\\migrations\\0*.py

# Create fresh migrations
py manage.py makemigrations

# Apply migrations to PostgreSQL
py manage.py migrate
```

### Step 5: Create Superuser
```bash
py manage.py createsuperuser
```

### Step 6: Import Data (Optional)
If you want to import data from SQLite:

```bash
# Use Django's dumpdata/loaddata
# Or manually import from the JSON backup
```

### Step 7: Test the Application
```bash
# Start Django server
py manage.py runserver

# Test authentication
# Test portfolio folder creation
```

### Step 8: Remove SQLite Database (Optional)
Once everything is working:
```bash
# Backup first!
move db.sqlite3 database_backup\\db.sqlite3.backup

# Or delete permanently
del db.sqlite3
```

## Verification Checklist

- [ ] PostgreSQL is installed and running
- [ ] Database "DigiportDB" exists in pgAdmin
- [ ] psycopg2 package is installed
- [ ] Django migrations completed successfully
- [ ] Can create test user
- [ ] Can create portfolio folders
- [ ] Authentication works
- [ ] All API endpoints work

## Troubleshooting

### Error: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Error: "could not connect to server"
- Check if PostgreSQL service is running
- Verify connection settings in settings.py
- Check password is correct

### Error: "database does not exist"
- Create database in pgAdmin first
- Or run the setup SQL script

### Error: "permission denied"
- Check PostgreSQL user permissions
- Verify DATABASES settings in settings.py

## Database Connection Settings

Current settings in `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DigiportDB',
        'USER': 'postgres',
        'PASSWORD': 'kumedasai',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Benefits of PostgreSQL

✓ Better performance for large datasets
✓ Advanced features (JSON fields, full-text search)
✓ Better concurrent access handling
✓ Production-ready
✓ Better data integrity
✓ Support for complex queries

## Rollback (If Needed)

If you need to rollback to SQLite:

1. Edit `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

2. Restore backup:
```bash
copy database_backup\\db.sqlite3.backup db.sqlite3
```

3. Restart Django server
"""
    
    instructions_file = os.path.join(BACKUP_DIR, 'MIGRATION_INSTRUCTIONS.md')
    with open(instructions_file, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print(f"Instructions saved to: {instructions_file}")
    return instructions_file

def main():
    """Main migration process"""
    print("\n" + "="*60)
    print("  SQLITE TO POSTGRESQL MIGRATION")
    print("="*60)
    print("\nThis script will:")
    print("  1. Export all data from SQLite")
    print("  2. Generate PostgreSQL setup script")
    print("  3. Create migration instructions")
    print("\nNOTE: Django settings have already been updated to use PostgreSQL")
    print("="*60)
    
    input("\nPress Enter to continue...")
    
    # Create backup directory
    create_backup_directory()
    
    # Export SQLite data
    backup_file = export_sqlite_data()
    
    # Generate PostgreSQL setup script
    sql_file = generate_postgresql_setup_sql()
    
    # Create instructions
    instructions_file = create_migration_instructions()
    
    # Summary
    print("\n" + "="*60)
    print("  MIGRATION PREPARATION COMPLETE")
    print("="*60)
    print("\nFiles created:")
    print(f"  1. Data backup: {backup_file if backup_file else 'FAILED'}")
    print(f"  2. SQL setup: {sql_file}")
    print(f"  3. Instructions: {instructions_file}")
    
    print("\n" + "="*60)
    print("  NEXT STEPS")
    print("="*60)
    print("\n1. Install PostgreSQL and psycopg2:")
    print("   pip install psycopg2-binary")
    print("\n2. Create database in pgAdmin:")
    print("   - Open pgAdmin")
    print("   - Create database: DigiportDB")
    print("\n3. Run Django migrations:")
    print("   py manage.py migrate")
    print("\n4. Create superuser:")
    print("   py manage.py createsuperuser")
    print("\n5. Test the application:")
    print("   py manage.py runserver")
    
    print("\nFor detailed instructions, see:")
    print(f"  {instructions_file}")
    print("="*60)

if __name__ == '__main__':
    main()
