"""
Management command to assign remaining teachers to unassigned classrooms
"""

from django.core.management.base import BaseCommand
from api.models import Classroom, User


class Command(BaseCommand):
    help = 'Assign remaining teachers to unassigned classrooms'

    def handle(self, *args, **options):
        self.stdout.write('🏫 Assigning remaining teachers to classrooms...\n')
        
        # Get teachers without classrooms
        unassigned_teachers = User.objects.filter(role='teacher', classroom__isnull=True).order_by('username')
        
        # Get classrooms without teachers
        unassigned_classrooms = Classroom.objects.filter(teacher__isnull=True).order_by('grade_level', 'section')
        
        self.stdout.write(f'Found {unassigned_teachers.count()} teachers without classrooms')
        self.stdout.write(f'Found {unassigned_classrooms.count()} classrooms without teachers\n')
        
        if not unassigned_classrooms.exists():
            self.stdout.write(self.style.WARNING('⚠️  All classrooms already have teachers assigned!'))
            self.stdout.write(self.style.WARNING(f'   But there are still {unassigned_teachers.count()} unassigned teachers.'))
            self.stdout.write('\nUnassigned teachers:')
            for teacher in unassigned_teachers:
                self.stdout.write(f'   - {teacher.username} ({teacher.get_full_name()})')
            return
        
        assigned_count = 0
        
        for classroom in unassigned_classrooms:
            if unassigned_teachers.exists():
                teacher = unassigned_teachers.first()
                
                # Assign teacher to classroom
                classroom.teacher = teacher
                classroom.save()
                
                # Update teacher's classroom field
                teacher.classroom = classroom
                teacher.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Assigned: {teacher.username} ({teacher.get_full_name()}) → {classroom.name}'
                    )
                )
                
                assigned_count += 1
                
                # Refresh the queryset
                unassigned_teachers = User.objects.filter(role='teacher', classroom__isnull=True).order_by('username')
        
        # Show remaining unassigned teachers
        remaining_teachers = User.objects.filter(role='teacher', classroom__isnull=True)
        
        if remaining_teachers.exists():
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️  {remaining_teachers.count()} teacher(s) still have no classroom (not enough classrooms):'
                )
            )
            for teacher in remaining_teachers:
                self.stdout.write(f'   - {teacher.username} ({teacher.get_full_name()})')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✨ Successfully assigned {assigned_count} teachers to classrooms!'
            )
        )
