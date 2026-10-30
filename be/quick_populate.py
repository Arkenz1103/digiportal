import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.db import connection
import random
from datetime import date

print("\n" + "="*70)
print("CREATING STUDENTS TABLE")
print("="*70 + "\n")

# Create table
with connection.cursor() as cursor:
    cursor.execute("""
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
    """)
    print("✓ Table created successfully!\n")
    
    # Check existing
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"✓ Already have {count} students in database!\n")
        for g in range(1, 7):
            for s in ['A', 'B']:
                cursor.execute("SELECT COUNT(*) FROM students WHERE grade_level=%s AND section=%s", [g, s])
                c = cursor.fetchone()[0]
                print(f"  Grade {g} Section {s}: {c} students")
        sys.exit(0)

print("Populating 360 students...\n")

# Names
males = ['Juan','Jose','Miguel','Carlos','Rafael','Gabriel','Daniel','Mark','John','Paul','James','David','Michael','Angelo','Christian','Joshua','Ryan','Kevin','Brian','Eric','Adrian','Nathan','Justin','Kenneth','Jerome','Patrick','Vincent','Albert','Francis','Carlo','Luis','Diego','Marco','Paolo','Enzo','Ethan','Noah','Liam','Lucas','Mason']
females = ['Maria','Ana','Sofia','Isabella','Gabriela','Andrea','Nicole','Michelle','Sarah','Jessica','Jennifer','Angela','Patricia','Elizabeth','Christine','Stephanie','Rachel','Samantha','Ashley','Kimberly','Grace','Faith','Hope','Joy','Angel','Princess','Queen','Precious','Divine','Blessing','Luna','Stella','Aurora','Bella','Clara','Emma','Olivia','Ava','Mia','Charlotte']
middles = ['Santos','Reyes','Cruz','Garcia','Mendoza','Torres','Flores','Rivera','Gomez','Diaz','Hernandez','Lopez','Gonzalez','Rodriguez','Martinez','Perez','Sanchez','Ramirez','Castillo','Jimenez']
lasts = ['Dela Cruz','Santos','Reyes','Garcia','Mendoza','Torres','Flores','Rivera','Gomez','Diaz','Hernandez','Lopez','Gonzalez','Rodriguez','Martinez','Perez','Sanchez','Ramirez','Castillo','Jimenez','Bautista','Aquino','Ramos','Villanueva','Santiago','Fernandez','Castro','Morales','Domingo','Navarro','Soriano','Mercado','Valencia','Valdez','Villegas','Salazar','Gutierrez','Aguilar','Padilla','Pascual']
guardians = ['Roberto','Ricardo','Fernando','Eduardo','Alberto','Rosario','Carmen','Teresa','Gloria','Linda']
barangays = ['Poblacion','Linangkayan','Mat-i','Mapulog','Maputi','Patag','Talib','Tuboran','Tagbalogo','Don Pedro']

counter = 1
created = 0

with connection.cursor() as cursor:
    for grade in range(1, 7):
        for section in ['A', 'B']:
            print(f"  Creating Grade {grade} Section {section}...", end=" ")
            for num in range(1, 31):
                gender = 'M' if num <= 15 else 'F'
                first = random.choice(males if gender == 'M' else females)
                middle = random.choice(middles)
                last = random.choice(lasts)
                sid = f"2025-{str(counter).zfill(5)}"
                
                age = 5 + grade
                birth = date(2025 - age - random.randint(0,1), random.randint(1,12), random.randint(1,28))
                email = f"{first.lower()}.{last.lower().replace(' ','')}@student.naawancentral.edu.ph"
                contact = f"09{random.randint(100000000,999999999)}"
                addr = f"{random.randint(1,999)} {random.choice(['Rizal St.','Bonifacio St.','Mabini St.','Del Pilar St.','Luna St.'])}, Brgy. {random.choice(barangays)}, Naawan, Misamis Oriental"
                gname = f"{random.choice(guardians)} {last}"
                gcontact = f"09{random.randint(100000000,999999999)}"
                gemail = f"{random.choice(guardians).lower()}.{last.lower().replace(' ','')}@gmail.com"
                avg = round(random.uniform(75,98),2)
                att = round(random.uniform(85,100),2)
                enroll = date(2024,6,random.randint(1,15))
                
                cursor.execute("""
                    INSERT INTO students (student_id,first_name,middle_name,last_name,grade_level,section,gender,date_of_birth,email,contact_number,address,guardian_name,guardian_contact,guardian_email,current_average,attendance_percentage,is_active,enrollment_date,created_at,updated_at)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
                """, [sid,first,middle,last,grade,section,gender,birth,email,contact,addr,gname,gcontact,gemail,avg,att,True,enroll])
                
                counter += 1
                created += 1
            print(f"✓ 30 students created")

print(f"\n{'='*70}")
print(f"✓ SUCCESS! Created {created} students")
print(f"{'='*70}\n")

with connection.cursor() as cursor:
    cursor.execute("SELECT COUNT(*) FROM students")
    total = cursor.fetchone()[0]
    print(f"Total students: {total}\n")
    for g in range(1,7):
        for s in ['A','B']:
            cursor.execute("SELECT COUNT(*) FROM students WHERE grade_level=%s AND section=%s AND gender='M'", [g,s])
            m = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM students WHERE grade_level=%s AND section=%s AND gender='F'", [g,s])
            f = cursor.fetchone()[0]
            print(f"Grade {g} Section {s}: {m+f} students (M:{m}, F:{f})")

print(f"\n{'='*70}")
print("✓ COMPLETE!")
print(f"{'='*70}\n")
