"""
Management command to fix teacher classroom assignments
This updates the User.classroom field for teachers based on Classroom.teacher
"""

from django.core.management.base import BaseCommand
from api.models import Classroom, User


class Command(BaseCommand):
    help = 'Fix teacher classroom assignments by syncing User.classroom with Classroom.teacher'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Fixing teacher classroom assignments...\n')
        
        # Get all classrooms with assigned teachers
        classrooms = Classroom.objects.filter(teacher__isnull=False)
        
        fixed_count = 0
        
        for classroom in classrooms:
            teacher = classroom.teacher
            
            # Check if teacher's classroom field matches
            if teacher.classroom != classroom:
                teacher.classroom = classroom
                teacher.save()
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Fixed: {teacher.username} ({teacher.get_full_name()}) -> {classroom.name}'
                    )
                )
            else:
                self.stdout.write(
                    f'✓ Already correct: {teacher.username} -> {classroom.name}'
                )
        
        # Check for teachers without classrooms
        teachers_without_classroom = User.objects.filter(role='teacher', classroom__isnull=True)
        
        if teachers_without_classroom.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  {teachers_without_classroom.count()} teacher(s) have no classroom assigned:'
                )
            )
            for teacher in teachers_without_classroom:
                self.stdout.write(f'   - {teacher.username} ({teacher.get_full_name()})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✨ Successfully fixed {fixed_count} teacher classroom assignments!'
            )
        )
