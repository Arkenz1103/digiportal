"""
Management command to populate student data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Student, User
import random
from datetime import date


class Command(BaseCommand):
    help = 'Populate student data - 30 students per section for grades 1-6'

    def handle(self, *args, **options):
        self.stdout.write('Starting student data population...')
        
        # Filipino first names (mixed gender)
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
        
        # Filipino middle names
        middle_names = [
            'Santos', 'Reyes', 'Cruz', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz',
            'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez'
        ]
        
        # Filipino last names
        last_names = [
            'Dela Cruz', 'Santos', 'Reyes', 'Garcia', 'Mendoza', 'Torres', 'Flores', 'Rivera', 'Gomez', 'Diaz',
            'Hernandez', 'Lopez', 'Gonzalez', 'Rodriguez', 'Martinez', 'Perez', 'Sanchez', 'Ramirez', 'Castillo', 'Jimenez',
            'Bautista', 'Aquino', 'Ramos', 'Villanueva', 'Santiago', 'Fernandez', 'Castro', 'Morales', 'Domingo', 'Navarro',
            'Soriano', 'Mercado', 'Valencia', 'Valdez', 'Villegas', 'Salazar', 'Gutierrez', 'Aguilar', 'Padilla', 'Pascual'
        ]
        
        # Guardian names
        guardian_first_names = ['Roberto', 'Ricardo', 'Fernando', 'Eduardo', 'Alberto', 'Rosario', 'Carmen', 'Teresa', 'Gloria', 'Linda']
        
        # Addresses in Naawan, Misamis Oriental
        barangays = [
            'Poblacion', 'Linangkayan', 'Mat-i', 'Mapulog', 'Maputi', 'Patag', 'Talib', 'Tuboran', 'Tagbalogo', 'Don Pedro'
        ]
        
        student_counter = 1
        current_year = 2025
        created_count = 0
        
        # Generate students for each grade and section
        for grade in range(1, 7):  # Grades 1-6
            for section in ['A', 'B']:  # Sections A and B
                self.stdout.write(f'Creating Grade {grade} Section {section} students...')
                
                for student_num in range(1, 31):  # 30 students per section
                    # Determine gender (roughly 50/50 split)
                    gender = 'M' if student_num <= 15 else 'F'
                    
                    # Select appropriate first name based on gender
                    if gender == 'M':
                        first_name = random.choice(male_first_names)
                    else:
                        first_name = random.choice(female_first_names)
                    
                    # Generate other names
                    middle_name = random.choice(middle_names)
                    last_name = random.choice(last_names)
                    
                    # Generate student ID (format: 2025-XXXXX)
                    student_id = f"{current_year}-{str(student_counter).zfill(5)}"
                    
                    # Check if student already exists
                    if Student.objects.filter(student_id=student_id).exists():
                        self.stdout.write(f'Student {student_id} already exists, skipping...')
                        student_counter += 1
                        continue
                    
                    # Generate date of birth (age appropriate for grade level)
                    base_age = 5 + grade
                    birth_year = current_year - base_age - random.randint(0, 1)
                    birth_month = random.randint(1, 12)
                    birth_day = random.randint(1, 28)
                    date_of_birth = date(birth_year, birth_month, birth_day)
                    
                    # Generate contact information
                    email = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}@student.naawancentral.edu.ph"
                    contact_number = f"09{random.randint(100000000, 999999999)}"
                    
                    # Generate address
                    house_number = random.randint(1, 999)
                    street = random.choice(['Rizal St.', 'Bonifacio St.', 'Mabini St.', 'Del Pilar St.', 'Luna St.'])
                    barangay = random.choice(barangays)
                    address = f"{house_number} {street}, Brgy. {barangay}, Naawan, Misamis Oriental"
                    
                    # Generate guardian information
                    guardian_first = random.choice(guardian_first_names)
                    guardian_name = f"{guardian_first} {last_name}"
                    guardian_contact = f"09{random.randint(100000000, 999999999)}"
                    guardian_email = f"{guardian_first.lower()}.{last_name.lower().replace(' ', '')}@gmail.com"
                    
                    # Generate academic performance
                    current_average = round(random.uniform(75, 98), 2)
                    attendance_percentage = round(random.uniform(85, 100), 2)
                    
                    # Calculate enrollment date
                    enrollment_date = date(2024, 6, random.randint(1, 15))
                    
                    # Create the student record
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
                    
                    # Optionally create a User account for the student
                    username = f"student{student_id.replace('-', '')}"
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password='student123',  # Default password
                            first_name=first_name,
                            last_name=last_name,
                            role='student',
                            id_number=student_id,
                            grade_level=f"Grade {grade}",
                            section=f"Section {section}"
                        )
                        student.user = user
                        student.save()
                    
                    created_count += 1
                    student_counter += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} students'))
        
        # Display summary
        total = Student.objects.count()
        self.stdout.write(f'\nSummary:')
        self.stdout.write(f'Total students in database: {total}')
        
        for grade in range(1, 7):
            for section in ['A', 'B']:
                count = Student.objects.filter(grade_level=grade, section=section).count()
                self.stdout.write(f'Grade {grade} Section {section}: {count} students')
