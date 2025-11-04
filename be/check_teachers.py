import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be.settings')
django.setup()

from api.models import User, Classroom

print("\n" + "="*60)
print("TEACHER CLASSROOM ASSIGNMENTS")
print("="*60 + "\n")

teachers = User.objects.filter(role='teacher').order_by('username')

for teacher in teachers:
    full_name = teacher.get_full_name() or teacher.username
    
    # Check if teacher is assigned to a classroom (as teacher)
    assigned_classroom = Classroom.objects.filter(teacher=teacher).first()
    
    # Check teacher's classroom field
    teacher_classroom = teacher.classroom
    
    print(f"Teacher: {teacher.username} ({full_name})")
    print(f"  - Classroom.teacher points to: {assigned_classroom.name if assigned_classroom else 'NONE'}")
    print(f"  - User.classroom field: {teacher_classroom.name if teacher_classroom else 'NONE'}")
    
    if assigned_classroom and teacher_classroom != assigned_classroom:
        print(f"  ⚠️  MISMATCH! Fixing...")
        teacher.classroom = assigned_classroom
        teacher.save()
        print(f"  ✅ Fixed: Now points to {assigned_classroom.name}")
    elif not assigned_classroom and not teacher_classroom:
        print(f"  ❌ NOT ASSIGNED TO ANY CLASSROOM")
    elif assigned_classroom and teacher_classroom == assigned_classroom:
        print(f"  ✅ Correctly assigned")
    
    print()

print("="*60)
print("SUMMARY")
print("="*60)
print(f"Total teachers: {teachers.count()}")
print(f"Teachers with classrooms: {User.objects.filter(role='teacher', classroom__isnull=False).count()}")
print(f"Teachers without classrooms: {User.objects.filter(role='teacher', classroom__isnull=True).count()}")
