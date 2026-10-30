#!/usr/bin/env python
"""
Check if test_teacher has a profile picture
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import User

def check_teacher_profile():
    try:
        # Get test_teacher user
        teacher = User.objects.get(username='test_teacher')
        
        print(f"\n{'='*60}")
        print(f"Teacher Profile Information")
        print(f"{'='*60}")
        print(f"Username: {teacher.username}")
        print(f"Name: {teacher.get_full_name() or teacher.username}")
        print(f"Email: {teacher.email}")
        print(f"Role: {teacher.role}")
        print(f"Profile Picture Field: {teacher.profile_picture}")
        
        if teacher.profile_picture:
            print(f"Profile Picture Path: {teacher.profile_picture.path}")
            print(f"Profile Picture URL: {teacher.profile_picture.url}")
            print(f"File Exists: {os.path.exists(teacher.profile_picture.path)}")
        else:
            print(f"Profile Picture: None (not set)")
        
        print(f"{'='*60}\n")
        
    except User.DoesNotExist:
        print("❌ test_teacher user not found!")
        print("   Run the application first to create the test user.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_teacher_profile()
