import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'portfolio_folders'
        ORDER BY ordinal_position
    """)
    columns = cursor.fetchall()

print("portfolio_folders table schema:")
for col_name, col_type, nullable in columns:
    print(f"  {col_name}: {col_type} (nullable: {nullable})")
