"""
Management command to show all classroom assignments
"""

from django.core.management.base import BaseCommand
from api.models import Classroom, User


class Command(BaseCommand):
    help = 'Show all classroom assignments'

    def handle(self, *args, **options):
        self.stdout.write('\n' + '='*70)
        self.stdout.write('CLASSROOM ASSIGNMENTS')
        self.stdout.write('='*70 + '\n')
        
        classrooms = Classroom.objects.all().order_by('grade_level', 'section')
        
        for classroom in classrooms:
            teacher_name = f"{classroom.teacher.get_full_name()} ({classroom.teacher.username})" if classroom.teacher else "NO TEACHER"
            student_count = User.objects.filter(classroom=classroom, role='student').count()
            
            self.stdout.write(f"📚 {classroom.name} - {classroom.room_number}")
            self.stdout.write(f"   Teacher: {teacher_name}")
            self.stdout.write(f"   Students: {student_count}/{classroom.capacity}")
            self.stdout.write("")
        
        self.stdout.write('='*70)
        self.stdout.write('SUMMARY')
        self.stdout.write('='*70)
        self.stdout.write(f"Total classrooms: {classrooms.count()}")
        self.stdout.write(f"Classrooms with teachers: {Classroom.objects.filter(teacher__isnull=False).count()}")
        self.stdout.write(f"Classrooms without teachers: {Classroom.objects.filter(teacher__isnull=True).count()}")
        self.stdout.write(f"Total teachers: {User.objects.filter(role='teacher').count()}")
        self.stdout.write(f"Assigned teachers: {User.objects.filter(role='teacher', classroom__isnull=False).count()}")
        self.stdout.write(f"Unassigned teachers: {User.objects.filter(role='teacher', classroom__isnull=True).count()}")
