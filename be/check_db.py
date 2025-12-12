
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import StudentSubmission, PortfolioActivity
from django.contrib.auth import get_user_model

User = get_user_model()

print("Checking submissions...")
submissions = StudentSubmission.objects.all().order_by('-id')[:5]

for s in submissions:
    print(f"ID: {s.id}")
    print(f"  Student: {s.student.username} (ID: {s.student.id})")
    print(f"  Activity Raw ID: {s.activity_id}")
    try:
        print(f"  Activity Title: {s.activity.title if s.activity else 'None'}")
    except:
        print("  Activity Title: Error accessing")
    print(f"  Status: {s.status}")
    print(f"  Compiled: {getattr(s, 'compiled', 'N/A')}")
    print(f"  Is Compilation: {getattr(s, 'is_compilation', 'N/A')}")
    print(f"  File: {s.file}")
    print(f"  Submitted At: {s.submitted_at}")
    print("-" * 30)

print(f"Total submissions: {submissions.count()}")
