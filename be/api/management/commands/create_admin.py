from django.core.management.base import BaseCommand
from api.models import User


class Command(BaseCommand):
    help = 'Create admin user with email: admin@digiportal.com, password: admin123'

    def handle(self, *args, **options):
        # Check if admin user already exists by email or username
        admin = User.objects.filter(email='admin@digiportal.com').first()
        if not admin:
            admin = User.objects.filter(username='admin').first()
        
        if admin:
            # Update existing admin user
            admin.username = 'admin'
            admin.email = 'admin@digiportal.com'
            admin.role = 'admin'
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user updated: {admin.email}'))
        else:
            # Create new admin user
            admin = User(
                username='admin',
                email='admin@digiportal.com',
                role='admin',
                first_name='System',
                last_name='Administrator',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                id_number='ADMIN001'
            )
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {admin.email}'))
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Login credentials:'))
        self.stdout.write(self.style.SUCCESS('  Email: admin@digiportal.com'))
        self.stdout.write(self.style.SUCCESS('  Password: admin123'))
