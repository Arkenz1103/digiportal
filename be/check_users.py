import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import User

print("Current users in database:")
print("-" * 60)

users = User.objects.all()
for user in users:
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Role: {user.role}")
    print(f"Is Active: {user.is_active}")
    print(f"Is Authenticated: {user.is_authenticated}")
    print("-" * 60)

if users.count() == 0:
    print("No users found. Creating test teacher...")
    user = User.objects.create_user(
        username='test_teacher',
        email='test_teacher@example.com',
        password='password123',
        role='teacher',
        first_name='Test',
        last_name='Teacher'
    )
    print(f"Created user: {user.username} (role: {user.role})")
