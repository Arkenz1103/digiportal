"""
Management command to populate classroom data
"""

from django.core.management.base import BaseCommand
from api.models import Classroom, User


class Command(BaseCommand):
    help = 'Populate classroom data based on the database structure'

    def handle(self, *args, **options):
        self.stdout.write('Creating classrooms...')
        
        # Classroom data based on your database image
        classrooms_data = [
            {'grade': 1, 'section': 'A', 'room': 'Room 111', 'capacity': 30},
            {'grade': 1, 'section': 'B', 'room': 'Room 112', 'capacity': 30},
            {'grade': 2, 'section': 'A', 'room': 'Room 121', 'capacity': 30},
            {'grade': 2, 'section': 'B', 'room': 'Room 122', 'capacity': 30},
            {'grade': 3, 'section': 'A', 'room': 'Room 131', 'capacity': 30},
            {'grade': 3, 'section': 'B', 'room': 'Room 132', 'capacity': 30},
            {'grade': 4, 'section': 'A', 'room': 'Room 141', 'capacity': 30},
            {'grade': 4, 'section': 'B', 'room': 'Room 142', 'capacity': 30},
            {'grade': 5, 'section': 'A', 'room': 'Room 151', 'capacity': 30},
            {'grade': 5, 'section': 'B', 'room': 'Room 152', 'capacity': 30},
            {'grade': 6, 'section': 'A', 'room': 'Room 161', 'capacity': 30},
            {'grade': 6, 'section': 'B', 'room': 'Room 162', 'capacity': 30},
        ]
        
        created_count = 0
        
        for data in classrooms_data:
            classroom, created = Classroom.objects.get_or_create(
                grade_level=data['grade'],
                section=data['section'],
                school_year='2024-2025',
                defaults={
                    'name': f"Grade {data['grade']} - {data['section']}",
                    'room_number': data['room'],
                    'capacity': data['capacity']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'✓ Created classroom: {classroom.name} in {classroom.room_number}')
            else:
                self.stdout.write(f'• Classroom already exists: {classroom.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {created_count} classrooms!'))
        
        # Assign teachers to classrooms (if teachers exist)
        self.stdout.write('\nAssigning teachers to classrooms...')
        teachers = User.objects.filter(role='teacher')
        
        if teachers.exists():
            classrooms = Classroom.objects.all()
            teacher_index = 0
            
            for classroom in classrooms:
                if not classroom.teacher and teacher_index < len(teachers):
                    classroom.teacher = teachers[teacher_index]
                    classroom.save()
                    self.stdout.write(f'✓ Assigned {teachers[teacher_index].username} to {classroom.name}')
                    teacher_index += 1
                    
                    # Reset index if we run out of teachers
                    if teacher_index >= len(teachers):
                        teacher_index = 0
        else:
            self.stdout.write(self.style.WARNING('No teachers found to assign to classrooms'))
        
        # Update students' classroom assignments based on their grade_level and section
        self.stdout.write('\nUpdating student classroom assignments...')
        students = User.objects.filter(role='student')
        updated_count = 0
        
        for student in students:
            if student.grade_level and student.section:
                # Extract grade number from grade_level (e.g., "Grade 1" -> 1)
                try:
                    grade_num = int(student.grade_level.replace('Grade ', ''))
                    classroom = Classroom.objects.filter(
                        grade_level=grade_num,
                        section=student.section,
                        school_year='2024-2025'
                    ).first()
                    
                    if classroom:
                        student.classroom = classroom
                        student.save()
                        updated_count += 1
                        self.stdout.write(f'✓ Assigned {student.username} to {classroom.name}')
                except (ValueError, AttributeError):
                    pass
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully updated {updated_count} student assignments!'))
