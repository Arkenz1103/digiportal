"""
Test and populate student data
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'be.settings')
django.setup()

from api.models import Student, User
from django.db import connection
import random
from datetime import date

print("=" * 60)
print("TESTING STUDENT TABLE")
print("=" * 60)

# Check if table exists
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'students'
        )
    """)
    table_exists = cursor.fetchone()[0]
    print(f"\n✓ Students table exists: {table_exists}")

if not table_exists:
    print("\n❌ ERROR: Students table does not exist!")
    print("Please run: py manage.py migrate api")
    exit(1)

# Check current student count
current_count = Student.objects.count()
print(f"✓ Current students in database: {current_count}")

if current_count >= 360:
    print(f"\n✓ Database already has {current_count} students!")
    print("\nStudent distribution:")
    for grade in range(1, 7):
        for section in ['A', 'B']:
            count = Student.objects.filter(grade_level=grade, section=section).count()
            print(f"  Grade {grade} Section {section}: {count} students")
    exit(0)

print(f"\n{'=' * 60}")
print("POPULATING STUDENT DATA")
print(f"{'=' * 60}\n")

# Filipino names
male_first_names = [
    'Juan', 'Jose', 'Miguel', 'Carlos', 'Rafael', 'Gabriel', 'Daniel', 'Mark', 'John', 'Paul',
    'James', 'David', 'Michael', 'Angelo', 'Christian', 'Joshua', 'Ryan', 'Kevin', 'Brian', 'Eric',
    'Adrian', 'Nathan', 'Justin', 'Kenneth', 'Jerome', 'Patrick', 'Vincent', 'Albert', 'Francis', 'Carlo',
    'Luis', 'Diego', 'Marco', 'Paolo', 'Enzo', 'Ethan', 'Noah', 'Liam', 'Lucas', 'Mason'
]

female_first_names = [
    'Maria', 'Ana', 'Sofia', 'Isabella', 'Gabriela', 'Andrea', 'Nicole', 'Michelle', 'Sarah', 'Jessica',
    'Jennifer', 'Angela', 'Patricia', 'Elizabeth', 'Christine', 'Stephanie', 'Rachel', 'Samantha', 'Ashley', 'Kimberly',
    'Grace', 'Faith', 'Hope', 'Joy', 'Angel', 'Princess', 'Queen', 'Precious', 'Divine', 'Blessing',
    'Luna', 'Stella', 'Aurora', 'Bella', 'Clara', 'Emma', 'Olivia', 'Ava', 'Mia', 'Charlotte'
]

middle_names = [
    'Santos', 'Reyes', 'Cruz', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz',
    'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez'
]

last_names = [
    'Dela Cruz', 'Santos', 'Reyes', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz',
    'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez',
    'Bautista', 'Aquino', 'Ramos', 'Villanueva', 'Santiago', 'Fernandez', 'Castro', 'Morales', 'Domingo', 'Navarro',
    'Soriano', 'Mercado', 'Valencia', 'Valdez', 'Villegas', 'Salazar', 'Gutierrez', 'Aguilar', 'Padilla', 'Pascual'
]

guardian_first_names = ['Roberto', 'Ricardo', 'Fernando', 'Eduardo', 'Alberto', 'Rosario', 'Carmen', 'Teresa', 'Gloria', 'Linda']

barangays = [
    'Poblacion', 'Linangkayan', 'Mat-i', 'Mapulog', 'Maputi', 'Patag', 'Talib', 'Tuboran', 'Tagbalogo', 'Don Pedro'
]

student_counter = current_count + 1
current_year = 2025
created_count = 0

# Generate students
for grade in range(1, 7):
    for section in ['A', 'B']:
        existing = Student.objects.filter(grade_level=grade, section=section).count()
        needed = 30 - existing
        
        if needed <= 0:
            print(f"✓ Grade {grade} Section {section}: Already has 30 students")
            continue
            
        print(f"Creating {needed} students for Grade {grade} Section {section}...")
        
        for student_num in range(1, needed + 1):
            gender = 'M' if student_num <= 15 else 'F'
            first_name = random.choice(male_first_names if gender == 'M' else female_first_names)
            middle_name = random.choice(middle_names)
            last_name = random.choice(last_names)
            
            student_id = f"{current_year}-{str(student_counter).zfill(5)}"
            
            # Skip if exists
            if Student.objects.filter(student_id=student_id).exists():
                student_counter += 1
                continue
            
            base_age = 5 + grade
            birth_year = current_year - base_age - random.randint(0, 1)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            date_of_birth = date(birth_year, birth_month, birth_day)
            
            email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@student.naawancentral.edu.ph"
            contact_number = f"09{random.randint(100000000, 999999999)}"
            
            house_number = random.randint(1, 999)
            street = random.choice(['Rizal St.', 'Bonifacio St.', 'Mabini St.', 'Del Pilar St.', 'Luna St.'])
            barangay = random.choice(barangays)
            address = f"{house_number} {street}, Brgy. {barangay}, Naawan, Misamis Oriental"
            
            guardian_first = random.choice(guardian_first_names)
            guardian_name = f"{guardian_first} {last_name}"
            guardian_contact = f"09{random.randint(100000000, 999999999)}"
            guardian_email = f"{guardian_first.lower()}.{last_name.lower().replace(' ', '')}@gmail.com"
            
            current_average = round(random.uniform(75, 98), 2)
            attendance_percentage = round(random.uniform(85, 100), 2)
            enrollment_date = date(2024, 6, random.randint(1, 15))
            
            student = Student.objects.create(
                student_id=student_id,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                grade_level=grade,
                section=section,
                gender=gender,
                date_of_birth=date_of_birth,
                email=email,
                contact_number=contact_number,
                address=address,
                guardian_name=guardian_name,
                guardian_contact=guardian_contact,
                guardian_email=guardian_email,
                current_average=current_average,
                attendance_percentage=attendance_percentage,
                is_active=True,
                enrollment_date=enrollment_date
            )
            
            created_count += 1
            student_counter += 1

print(f"\n{'=' * 60}")
print(f"✓ Successfully created {created_count} new students")
print(f"{'=' * 60}\n")

# Final summary
total = Student.objects.count()
print(f"FINAL SUMMARY:")
print(f"Total students in database: {total}\n")

for grade in range(1, 7):
    for section in ['A', 'B']:
        count = Student.objects.filter(grade_level=grade, section=section).count()
        male_count = Student.objects.filter(grade_level=grade, section=section, gender='M').count()
        female_count = Student.objects.filter(grade_level=grade, section=section, gender='F').count()
        print(f"Grade {grade} Section {section}: {count} students (M: {male_count}, F: {female_count})")

print(f"\n{'=' * 60}")
print("✓ STUDENT DATA POPULATION COMPLETE!")
print(f"{'=' * 60}")
