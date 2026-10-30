import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from api.models import Student, User, Classroom

print("\n" + "="*70)
print("STUDENT COUNT CHECK")
print("="*70 + "\n")

# Check Student model counts
print("📊 STUDENT MODEL (students table):")
print("-" * 50)
total_students = Student.objects.count()
print(f"Total students: {total_students}\n")

for grade in range(1, 7):
    for section in ['A', 'B']:
        count = Student.objects.filter(grade_level=grade, section=section).count()
        print(f"  Grade {grade} - {section}: {count} students")
    print()

# Check User model counts (students with role='student')
print("\n📊 USER MODEL (users table with role='student'):")
print("-" * 50)
total_user_students = User.objects.filter(role='student').count()
print(f"Total student users: {total_user_students}\n")

# Check by classroom
print("By Classroom assignment:")
for classroom in Classroom.objects.all().order_by('grade_level', 'section'):
    count = User.objects.filter(role='student', classroom=classroom).count()
    print(f"  {classroom.name}: {count} students")

# Students without classroom
no_classroom = User.objects.filter(role='student', classroom__isnull=True).count()
print(f"  No classroom assigned: {no_classroom} students")

# Check Classroom model
print("\n📊 CLASSROOM MODEL:")
print("-" * 50)
for classroom in Classroom.objects.all().order_by('grade_level', 'section'):
    print(f"  ID: {classroom.id}, Name: {classroom.name}, Grade: {classroom.grade_level}, Section: {classroom.section}")

print("\n" + "="*70)
print("✓ CHECK COMPLETE!")
print("="*70 + "\n")
