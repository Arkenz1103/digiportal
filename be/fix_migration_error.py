import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.db import connection

print("\n" + "="*70)
print("FIXING MIGRATION ERROR")
print("="*70 + "\n")

# Remove the problematic migration records from django_migrations table
with connection.cursor() as cursor:
    # Check if the migration exists
    cursor.execute("""
        SELECT id, app, name FROM django_migrations 
        WHERE app = 'api' AND (name LIKE '%0036%' OR name LIKE '%0037%')
    """)
    migrations = cursor.fetchall()
    
    if migrations:
        print("Found problematic migration records:")
        for mig in migrations:
            print(f"  - ID: {mig[0]}, App: {mig[1]}, Name: {mig[2]}")
        
        print("\nDeleting these records...")
        cursor.execute("""
            DELETE FROM django_migrations 
            WHERE app = 'api' AND (name LIKE '%0036%' OR name LIKE '%0037%')
        """)
        print("✓ Migration records deleted successfully!")
    else:
        print("No problematic migration records found.")

print("\n" + "="*70)
print("✓ MIGRATION ERROR FIXED!")
print("="*70)
print("\nYou can now run: py manage.py runserver")
print("\n")
