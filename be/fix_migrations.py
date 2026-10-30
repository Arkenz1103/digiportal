#!/usr/bin/env python
"""
Fix inconsistent migration history by faking the api.0001_initial migration
"""
import os
import sys
import sqlite3

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')

# Setup Django
import django
django.setup()

from django.db import connection

print("=" * 70)
print("FIXING MIGRATION HISTORY")
print("=" * 70)

# Check current migration status
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT app, name FROM django_migrations 
        ORDER BY id
    """)
    migrations = cursor.fetchall()
    
    print("\nCurrent migrations in database:")
    for app, name in migrations:
        print(f"  - {app}.{name}")
    
    # Check if api.0001_initial is already recorded
    cursor.execute("""
        SELECT COUNT(*) FROM django_migrations 
        WHERE app = 'api' AND name = '0001_initial'
    """)
    api_migration_exists = cursor.fetchone()[0] > 0
    
    if not api_migration_exists:
        print("\n✓ api.0001_initial is NOT in migration history")
        print("  Adding it now (fake migration)...")
        
        # Insert the migration record
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('api', '0001_initial', datetime('now'))
        """)
        connection.commit()
        print("  ✓ Added api.0001_initial to migration history")
    else:
        print("\n✓ api.0001_initial is already in migration history")

print("\n" + "=" * 70)
print("CHECKING TABLES")
print("=" * 70)

# Check if tables exist
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name LIKE '%portfolio%'
        ORDER BY name
    """)
    tables = cursor.fetchall()
    
    print("\nPortfolio tables:")
    if tables:
        for (table_name,) in tables:
            print(f"  ✓ {table_name}")
    else:
        print("  ✗ No portfolio tables found")
        print("\n  Creating tables manually...")
        
        # Create portfolio_folders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Create portfolio_activities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS portfolio_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                file_path VARCHAR(500),
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                folder_id INTEGER NOT NULL,
                FOREIGN KEY (folder_id) REFERENCES portfolio_folders (id) ON DELETE CASCADE
            )
        """)
        
        connection.commit()
        print("  ✓ Created portfolio_folders table")
        print("  ✓ Created portfolio_activities table")

print("\n" + "=" * 70)
print("MIGRATION FIX COMPLETE!")
print("=" * 70)
print("\nYou can now restart the Django server.")
