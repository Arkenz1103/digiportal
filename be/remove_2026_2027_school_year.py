"""
Script to remove the 2026-2027 archived school year from all teacher users
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_main.settings')
django.setup()

from api.models import SchoolYear, Classroom, User

def remove_2026_2027_school_year():
    """Remove the 2026-2027 school year and related data"""
    
    school_year_name = "2026-2027"
    
    print(f"Looking for school year: {school_year_name}")
    
    # Find all school years with this name
    school_years = SchoolYear.objects.filter(name=school_year_name)
    
    if not school_years.exists():
        print(f"No school year found with name '{school_year_name}'")
        return
    
    print(f"Found {school_years.count()} school year(s) with name '{school_year_name}'")
    
    for sy in school_years:
        print(f"  - School Year ID: {sy.id}, Teacher: {sy.teacher.username if sy.teacher else 'None'}")
    
    # Find related classrooms with this school year
    classrooms = Classroom.objects.filter(school_year=school_year_name)
    print(f"\nFound {classrooms.count()} classroom(s) with school_year '{school_year_name}'")
    
    # Delete classrooms first
    if classrooms.exists():
        classroom_count = classrooms.count()
        classrooms.delete()
        print(f"Deleted {classroom_count} classroom(s)")
    
    # Delete school years
    count = school_years.count()
    school_years.delete()
    print(f"Deleted {count} school year(s) with name '{school_year_name}'")
    
    print("\nDone! 2026-2027 school year has been removed from all teachers.")

if __name__ == '__main__':
    remove_2026_2027_school_year()
