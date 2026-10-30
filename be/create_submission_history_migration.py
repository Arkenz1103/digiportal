"""
Script to create migration for SubmissionHistory model
Run this with: python create_submission_history_migration.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.core.management import call_command

print("\n" + "="*70)
print("CREATING MIGRATION FOR SUBMISSION HISTORY")
print("="*70 + "\n")

try:
    # Create migrations
    print("📝 Creating migrations...")
    call_command('makemigrations', 'api')
    print("✅ Migrations created successfully!\n")
    
    # Apply migrations
    print("📦 Applying migrations...")
    call_command('migrate', 'api')
    print("✅ Migrations applied successfully!\n")
    
    print("="*70)
    print("✅ SUBMISSION HISTORY MODEL READY!")
    print("="*70)
    print("\nYou can now:")
    print("  1. Students can resubmit up to 3 times")
    print("  2. All versions are saved in submission_history table")
    print("  3. Teachers can view any version via dropdown")
    print("\n")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}\n")
    import traceback
    traceback.print_exc()
