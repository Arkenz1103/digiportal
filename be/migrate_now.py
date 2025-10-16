#!/usr/bin/env python
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')

# Setup Django
import django
django.setup()

# Import and run migrate
from django.core.management import execute_from_command_line

print("=" * 60)
print("APPLYING MIGRATIONS TO SQLITE DATABASE")
print("=" * 60)

# Execute migrate command
execute_from_command_line(['manage.py', 'migrate'])

print("=" * 60)
print("MIGRATION COMPLETE!")
print("=" * 60)
