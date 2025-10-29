"""
Script to update student information (Student ID, Grade Level, Section)
Run this script from the Django shell or as a management command

Usage:
    python manage.py shell < update_student_info.py
"""

from api.models import User

# Update all students with default values
students = User.objects.filter(role='student')

for student in students:
    # Only update if values are null/empty
    if not student.id_number:
        # Generate a student ID (you can customize this format)
        student.id_number = f"STU{student.id:05d}"
    
    if not student.grade_level:
        # Set default grade level (customize as needed)
        student.grade_level = "Grade 1"
    
    if not student.section:
        # Set default section (customize as needed)
        student.section = "A"
    
    student.save()
    print(f"✅ Updated {student.username}: ID={student.id_number}, Grade={student.grade_level}, Section={student.section}")

print(f"\n✅ Updated {students.count()} student(s)")
