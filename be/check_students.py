import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from api.models import Student

print("\n" + "="*70)
print("STUDENT DATA CHECK")
print("="*70 + "\n")

total = Student.objects.count()
print(f"Total students in database: {total}\n")

if total == 0:
    print("❌ No students found! Running population script...\n")
    from django.db import connection
    import random
    from datetime import date
    
    # Quick populate
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
                print(f"✓ Done")
    
    print(f"\n✓ Created {created} students!\n")
    total = Student.objects.count()

print("Distribution by Grade and Section:")
print("-" * 70)
for grade in range(1, 7):
    for section in ['A', 'B']:
        count = Student.objects.filter(grade_level=grade, section=section).count()
        male_count = Student.objects.filter(grade_level=grade, section=section, gender='M').count()
        female_count = Student.objects.filter(grade_level=grade, section=section, gender='F').count()
        print(f"Grade {grade} Section {section}: {count} students (Male: {male_count}, Female: {female_count})")

print("\n" + "="*70)
print("Sample Students (First 10):")
print("="*70)
for student in Student.objects.all()[:10]:
    print(f"{student.student_id} | {student.first_name} {student.middle_name} {student.last_name} | Grade {student.grade_level}-{student.section} | {student.gender}")

print("\n" + "="*70)
print("✓ CHECK COMPLETE!")
print("="*70 + "\n")
