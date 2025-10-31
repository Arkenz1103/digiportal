"""
Management command to set up passwords for all users
"""

from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'Set up default passwords for all users (students and teachers)'

    def handle(self, *args, **options):
        self.stdout.write('Setting up passwords for all users...')
        
        # Get all users
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in database'))
            return
        
        updated_count = 0
        
        for user in users:
            # Set default password based on role
            if user.role == 'student':
                # For students: password is "student123"
                default_password = 'student123'
            elif user.role == 'teacher':
                # For teachers: password is "teacher123"
                default_password = 'teacher123'
            else:
                # For other roles: password is "admin123"
                default_password = 'admin123'
            
            # Set the password (this will hash it properly)
            user.set_password(default_password)
            user.save()
            
            updated_count += 1
            
            self.stdout.write(
                f'✓ Updated {user.email or user.username} ({user.role}) - Password: {default_password}'
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully updated passwords for {updated_count} users!')
        )
        self.stdout.write('\nDefault passwords:')
        self.stdout.write('  - Students: student123')
        self.stdout.write('  - Teachers: teacher123')
        self.stdout.write('  - Admins: admin123')
