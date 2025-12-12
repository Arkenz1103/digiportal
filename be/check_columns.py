
import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

with connection.cursor() as cursor:
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'student_submissions'")
    columns = [col[0] for col in cursor.fetchall()]
    print("Columns in api_studentsubmission:")
    for col in columns:
        print(f" - {col}")
