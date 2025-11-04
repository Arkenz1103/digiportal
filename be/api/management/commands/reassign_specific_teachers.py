"""
Management command to reassign specific teachers to classrooms
"""

from django.core.management.base import BaseCommand
from api.models import Classroom, User


class Command(BaseCommand):
    help = 'Reassign specific teachers to classrooms'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Reassigning specific teachers...\n')
        
        # Define the reassignments
        reassignments = [
            {
                'classroom': 'Grade 1 - B',
                'old_teacher': 'Teacher Sins',
                'new_teacher': 'jose.reyes'
            },
            {
                'classroom': 'Grade 5 - B',
                'old_teacher': 'test_teacher',
                'new_teacher': 'ana.garcia'
            },
            {
                'classroom': 'Grade 6 - A',
                'old_teacher': 'luis.hernandez',
                'new_teacher': 'eduardo.santiago'
            }
        ]
        
        success_count = 0
        
        for assignment in reassignments:
            try:
                # Find the classroom
                classroom = Classroom.objects.filter(name=assignment['classroom']).first()
                
                if not classroom:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Classroom not found: {assignment['classroom']}")
                    )
                    continue
                
                # Find the new teacher
                new_teacher = User.objects.filter(
                    username=assignment['new_teacher'],
                    role='teacher'
                ).first()
                
                if not new_teacher:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Teacher not found: {assignment['new_teacher']}")
                    )
                    continue
                
                # Get old teacher info
                old_teacher = classroom.teacher
                old_teacher_name = old_teacher.get_full_name() if old_teacher else 'None'
                
                # Clear old teacher's classroom assignment if they have one
                if old_teacher:
                    old_teacher.classroom = None
                    old_teacher.save()
                
                # Assign new teacher to classroom
                classroom.teacher = new_teacher
                classroom.save()
                
                # Update new teacher's classroom field
                new_teacher.classroom = classroom
                new_teacher.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ {classroom.name}: {old_teacher_name} → {new_teacher.get_full_name()} ({new_teacher.username})"
                    )
                )
                
                success_count += 1
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Error reassigning {assignment['classroom']}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✨ Successfully reassigned {success_count} classroom(s)!'
            )
        )
        
        # Show final summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write('UPDATED CLASSROOM ASSIGNMENTS')
        self.stdout.write('='*70 + '\n')
        
        for assignment in reassignments:
            classroom = Classroom.objects.filter(name=assignment['classroom']).first()
            if classroom and classroom.teacher:
                self.stdout.write(
                    f"📚 {classroom.name}: {classroom.teacher.get_full_name()} ({classroom.teacher.username})"
                )
