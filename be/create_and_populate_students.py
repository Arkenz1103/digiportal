"""
Direct SQL approach to create students table and populate data
"""
import os
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')

import django
django.setup()

from django.db import connection
import random
from datetime import date

print("=" * 70)
print("CREATING STUDENTS TABLE AND POPULATING DATA")
print("=" * 70)

# Create the students table using raw SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    grade_level INTEGER NOT NULL,
    section VARCHAR(1) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    date_of_birth DATE,
    email VARCHAR(254),
    contact_number VARCHAR(20),
    address TEXT,
    guardian_name VARCHAR(200),
    guardian_contact VARCHAR(20),
    guardian_email VARCHAR(254),
    current_average DECIMAL(5,2),
    attendance_percentage DECIMAL(5,2),
    is_active BOOLEAN DEFAULT TRUE,
    enrollment_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS students_grade_section_idx ON students(grade_level, section);
CREATE INDEX IF NOT EXISTS students_name_idx ON students(last_name, first_name);
"""

with connection.cursor() as cursor:
    print("\n✓ Creating students table...")
    cursor.execute(create_table_sql)
    print("✓ Students table created successfully!")

# Check if data already exists
with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM students")
    existing_count = cursor.fetchone()[0]
    
if existing_count > 0:
    print(f"\n✓ Database already has {existing_count} students!")
    with connection.cursor() as cursor:
        for grade in range(1, 7):
            for section in ['A', 'B']:
                cursor.execute(
                    "SELECT COUNT(*) FROM students WHERE grade_level = %s AND section = %s",
                    [grade, section]
                )
                count = cursor.fetchone()[0]
                print(f"  Grade {grade} Section {section}: {count} students")
    sys.exit(0)

print(f"\n✓ Populating student data...")

# Names data
male_first_names = ['Juan', 'Jose', 'Miguel', 'Carlos', 'Rafael', 'Gabriel', 'Daniel', 'Mark', 'John', 'Paul', 'James', 'David', 'Michael', 'Angelo', 'Christian', 'Joshua', 'Ryan', 'Kevin', 'Brian', 'Eric', 'Adrian', 'Nathan', 'Justin', 'Kenneth', 'Jerome', 'Patrick', 'Vincent', 'Albert', 'Francis', 'Carlo', 'Luis', 'Diego', 'Marco', 'Paolo', 'Enzo', 'Ethan', 'Noah', 'Liam', 'Lucas', 'Mason']
female_first_names = ['Maria', 'Ana', 'Sofia', 'Isabella', 'Gabriela', 'Andrea', 'Nicole', 'Michelle', 'Sarah', 'Jessica', 'Jennifer', 'Angela', 'Patricia', 'Elizabeth', 'Christine', 'Stephanie', 'Rachel', 'Samantha', 'Ashley', 'Kimberly', 'Grace', 'Faith', 'Hope', 'Joy', 'Angel', 'Princess', 'Queen', 'Precious', 'Divine', 'Blessing', 'Luna', 'Stella', 'Aurora', 'Bella', 'Clara', 'Emma', 'Olivia', 'Ava', 'Mia', 'Charlotte']
middle_names = ['Santos', 'Reyes', 'Cruz', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz', 'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez']
last_names = ['Dela Cruz', 'Santos', 'Reyes', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz', 'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez', 'Bautista', 'Aquino', 'Ramos', 'Villanueva', 'Santiago', 'Fernandez', 'Castro', 'Morales', 'Domingo', 'Navarro', 'Soriano', 'Mercado', 'Valencia', 'Valdez', 'Villegas', 'Salazar', 'Gutierrez', 'Aguilar', 'Padilla', 'Pascual']
guardian_first_names = ['Roberto', 'Ricardo', 'Fernando', 'Eduardo', 'Alberto', 'Rosario', 'Carmen', 'Teresa', 'Gloria', 'Linda']
barangays = ['Poblacion', 'Linangkayan', 'Mat-i', 'Mapulog', 'Maputi', 'Patag', 'Talib', 'Tuboran', 'Tagbalogo', 'Don Pedro']

student_counter = 1
current_year = 2025
created_count = 0

insert_sql = """
INSERT INTO students (
    student_id, first_name, middle_name, last_name, grade_level, section,
    gender, date_of_birth, email, contact_number, address,
    guardian_name, guardian_contact, guardian_email,
    current_average, attendance_percentage, is_active, enrollment_date
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

with connection.cursor() as cursor:
    for grade in range(1, 7):
        for section in ['A', 'B']:
            print(f"  Creating Grade {grade} Section {section} students...")
            
            for student_num in range(1, 31):
                gender = 'M' if student_num <= 15 else 'F'
                first_name = random.choice(male_first_names if gender == 'M' else female_first_names)
                middle_name = random.choice(middle_names)
                last_name = random.choice(last_names)
                student_id = f"{current_year}-{str(student_counter).zfill(5)}"
                
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
                
                cursor.execute(insert_sql, [
                    student_id, first_name, middle_name, last_name, grade, section,
                    gender, date_of_birth, email, contact_number, address,
                    guardian_name, guardian_contact, guardian_email,
                    current_average, attendance_percentage, True, enrollment_date
                ])
                
                created_count += 1
                student_counter += 1

print(f"\n✓ Successfully created {created_count} students!")

# Final summary
print(f"\n{'=' * 70}")
print("FINAL SUMMARY")
print(f"{'=' * 70}")

with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    print(f"\nTotal students in database: {total}\n")
    
    for grade in range(1, 7):
        for section in ['A', 'B']:
            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE grade_level = %s AND section = %s AND gender = 'M'",
                [grade, section]
            )
            male_count = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT COUNT(*) FROM students WHERE grade_level = %s AND section = %s AND gender = 'F'",
                [grade, section]
            )
            female_count = cursor.fetchone()[0]
            
            total_section = male_count + female_count
            print(f"Grade {grade} Section {section}: {total_section} students (M: {male_count}, F: {female_count})")

print(f"\n{'=' * 70}")
print("✓ STUDENT DATA POPULATION COMPLETE!")
print(f"{'=' * 70}")
