import os
import django
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

# Now run migrations
from django.core.management import call_command

print("Applying migrations to SQLite database...")
try:
    call_command('migrate', verbosity=2)
    print("\n✓ Migrations applied successfully!")
except Exception as e:
    print(f"\n✗ Error applying migrations: {e}")
    sys.exit(1)
