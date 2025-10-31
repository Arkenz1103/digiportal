"""
Management command to list all users in the database
"""

from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'List all users in the database with their emails and roles'

    def handle(self, *args, **options):
        self.stdout.write('Listing all users in the database...\n')
        
        # Get all users
        users = User.objects.all().order_by('role', 'email')
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in database'))
            return
        
        # Group by role
        teachers = users.filter(role='teacher')
        students = users.filter(role='student')
        admins = users.filter(role='admin')
        
        # Display teachers
        if teachers.exists():
            self.stdout.write(self.style.SUCCESS(f'\n=== TEACHERS ({teachers.count()}) ==='))
            for user in teachers:
                name = f"{user.first_name} {user.last_name}".strip() or user.username
                self.stdout.write(f'  • {name}')
                self.stdout.write(f'    Email: {user.email}')
                self.stdout.write(f'    Username: {user.username}')
                if user.department:
                    self.stdout.write(f'    Department: {user.department}')
                self.stdout.write('')
        
        # Display students
        if students.exists():
            self.stdout.write(self.style.SUCCESS(f'\n=== STUDENTS ({students.count()}) ==='))
            for user in students[:10]:  # Show first 10 students
                name = f"{user.first_name} {user.last_name}".strip() or user.username
                self.stdout.write(f'  • {name}')
                self.stdout.write(f'    Email: {user.email}')
                self.stdout.write(f'    Username: {user.username}')
                if user.id_number:
                    self.stdout.write(f'    Student ID: {user.id_number}')
                if user.grade_level and user.section:
                    self.stdout.write(f'    Class: {user.grade_level} - {user.section}')
                self.stdout.write('')
            
            if students.count() > 10:
                self.stdout.write(f'  ... and {students.count() - 10} more students')
        
        # Display admins
        if admins.exists():
            self.stdout.write(self.style.SUCCESS(f'\n=== ADMINS ({admins.count()}) ==='))
            for user in admins:
                name = f"{user.first_name} {user.last_name}".strip() or user.username
                self.stdout.write(f'  • {name}')
                self.stdout.write(f'    Email: {user.email}')
                self.stdout.write(f'    Username: {user.username}')
                self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal users: {users.count()}'))
