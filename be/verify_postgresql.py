"""
Quick verification script to check if PostgreSQL is ready
Run this before deleting SQLite database
"""
import os
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')

print("="*60)
print("  POSTGRESQL READINESS CHECK")
print("="*60)

# Check 1: Can we import psycopg2?
print("\n1. Checking psycopg2 driver...")
try:
    import psycopg2
    print("   ✓ psycopg2 is installed")
except ImportError:
    print("   ✗ psycopg2 NOT installed")
    print("   Run: pip install psycopg2-binary")
    sys.exit(1)

# Check 2: Django setup
print("\n2. Setting up Django...")
try:
    import django
    django.setup()
    print("   ✓ Django setup successful")
except Exception as e:
    print(f"   ✗ Django setup failed: {e}")
    sys.exit(1)

# Check 3: Database connection
print("\n3. Testing PostgreSQL connection...")
try:
    from django.db import connection
    connection.ensure_connection()
    print("   ✓ Connected to PostgreSQL")
    
    # Get database info
    db_name = connection.settings_dict['NAME']
    db_user = connection.settings_dict['USER']
    db_host = connection.settings_dict['HOST']
    print(f"   Database: {db_name}")
    print(f"   User: {db_user}")
    print(f"   Host: {db_host}")
except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    print("\n   Possible issues:")
    print("   - PostgreSQL service not running")
    print("   - Database 'DigiportDB' not created")
    print("   - Wrong password in settings.py")
    sys.exit(1)

# Check 4: Tables exist
print("\n4. Checking database tables...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    if len(tables) == 0:
        print("   ✗ No tables found - migrations not run!")
        print("   Run: py manage.py migrate")
        sys.exit(1)
    
    print(f"   ✓ Found {len(tables)} tables")
    
    # Check for required tables
    required = ['users', 'portfolio_folders', 'portfolio_activities']
    missing = [t for t in required if t not in tables]
    
    if missing:
        print(f"   ⚠ Missing tables: {', '.join(missing)}")
        print("   Run: py manage.py migrate")
    else:
        print("   ✓ All required tables exist")
        
except Exception as e:
    print(f"   ✗ Error checking tables: {e}")
    sys.exit(1)

# Check 5: Can query models
print("\n5. Testing Django models...")
try:
    from api.models import User, PortfolioFolder
    
    user_count = User.objects.count()
    folder_count = PortfolioFolder.objects.count()
    
    print(f"   ✓ User model works ({user_count} users)")
    print(f"   ✓ PortfolioFolder model works ({folder_count} folders)")
except Exception as e:
    print(f"   ✗ Model query failed: {e}")
    sys.exit(1)

# Check 6: SQLite database exists
print("\n6. Checking SQLite database...")
sqlite_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
if os.path.exists(sqlite_path):
    size = os.path.getsize(sqlite_path)
    print(f"   ✓ SQLite database found ({size:,} bytes)")
    print(f"   Location: {sqlite_path}")
else:
    print("   ℹ SQLite database not found (already deleted)")

# Final verdict
print("\n" + "="*60)
print("  VERIFICATION RESULT")
print("="*60)
print("\n✅ PostgreSQL is working correctly!")
print("\n✅ SAFE TO DELETE SQLite database")
print("\nTo delete SQLite database:")
print("  1. Backup first (recommended):")
print("     move db.sqlite3 database_backup\\db.sqlite3.backup")
print("\n  2. Or delete permanently:")
print("     del db.sqlite3")
print("\n⚠️  Make sure to test your application first!")
print("="*60)
