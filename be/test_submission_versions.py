"""
Test script to verify submission version history
Run with: python test_submission_versions.py
"""

import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from api.models import StudentSubmission, SubmissionHistory

print("\n" + "="*70)
print("SUBMISSION VERSION HISTORY TEST")
print("="*70 + "\n")

# Get a sample submission
submissions = StudentSubmission.objects.all().order_by('-id')[:5]

if not submissions:
    print("❌ No submissions found in database")
else:
    print(f"Found {len(submissions)} recent submissions:\n")
    
    for sub in submissions:
        print(f"📝 Submission ID: {sub.id}")
        print(f"   Student: {sub.student.username}")
        print(f"   Activity: {sub.activity.title if sub.activity else 'Sketch Pad'}")
        print(f"   Current Version: {sub.submission_version}")
        print(f"   Resubmit Count: {sub.resubmit_count}")
        
        # Check history
        history_count = SubmissionHistory.objects.filter(submission=sub).count()
        print(f"   History Records: {history_count}")
        
        if history_count > 0:
            print(f"   📚 Version History:")
            for h in SubmissionHistory.objects.filter(submission=sub).order_by('version'):
                print(f"      - Version {h.version}: {h.caption[:30]}...")
        
        print()

print("="*70)
print("✅ TEST COMPLETE")
print("="*70 + "\n")
