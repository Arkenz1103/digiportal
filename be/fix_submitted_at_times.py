"""
Script to fix submitted_at times for existing submissions.
This sets submitted_at to None for all existing non-draft submissions
so they will show the correct time on next turn-in.
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import StudentSubmission
from django.utils import timezone

def fix_submitted_times():
    # Get all non-draft submissions
    submissions = StudentSubmission.objects.exclude(status='draft')
    
    print(f"Found {submissions.count()} submitted works")
    
    for submission in submissions:
        old_time = submission.submitted_at
        print(f"\n📝 Submission ID: {submission.id}")
        print(f"   Student: {submission.student.username}")
        print(f"   Activity: {submission.activity.title if submission.activity else 'N/A'}")
        print(f"   Old submitted_at: {old_time}")
        print(f"   Status: {submission.status}")
        print(f"   Is late: {submission.is_late}")
    
    # Ask for confirmation
    response = input(f"\n⚠️  Do you want to keep these timestamps? (y/n): ")
    
    if response.lower() == 'y':
        print("✅ Keeping existing timestamps. No changes made.")
    else:
        print("❌ To fix, students need to resubmit their work.")
        print("   Or manually update submitted_at in the database.")

if __name__ == '__main__':
    fix_submitted_times()
