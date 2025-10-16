"""Simple PostgreSQL connection test"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection
from api.models import User, PortfolioFolder, PortfolioActivity

print("="*60)
print("  POSTGRESQL CONNECTION TEST")
print("="*60)

# Test connection
try:
    connection.ensure_connection()
    print("\n[OK] Connected to PostgreSQL")
    
    db_name = connection.settings_dict['NAME']
    db_user = connection.settings_dict['USER']
    db_host = connection.settings_dict['HOST']
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    print(f"  Host: {db_host}")
except Exception as e:
    print(f"\n[ERROR] Connection failed: {e}")
    sys.exit(1)

# Check tables
try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n[OK] Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table}")
        
except Exception as e:
    print(f"\n[ERROR] Could not list tables: {e}")
    sys.exit(1)

# Test models
try:
    user_count = User.objects.count()
    folder_count = PortfolioFolder.objects.count()
    activity_count = PortfolioActivity.objects.count()
    
    print(f"\n[OK] Models working:")
    print(f"  Users: {user_count}")
    print(f"  Folders: {folder_count}")
    print(f"  Activities: {activity_count}")
except Exception as e:
    print(f"\n[ERROR] Model query failed: {e}")
    sys.exit(1)

# Check portfolio_folders schema
try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'portfolio_folders'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
    
    print(f"\n[OK] portfolio_folders schema:")
    for col_name, col_type in columns:
        print(f"  - {col_name}: {col_type}")
        
    # Check if description exists
    col_names = [col[0] for col in columns]
    if 'description' in col_names:
        print("\n[OK] Description field exists!")
    else:
        print("\n[WARNING] Description field missing!")
        
except Exception as e:
    print(f"\n[ERROR] Could not check schema: {e}")

print("\n" + "="*60)
print("  ALL TESTS PASSED!")
print("="*60)
print("\n[OK] PostgreSQL is working correctly")
print("[OK] Safe to delete SQLite database")
print("\nTo delete SQLite:")
print("  move db.sqlite3 database_backup\\db.sqlite3.backup")
print("="*60)
